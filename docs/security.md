# Security Implementation

Meridian National Bank AI Assistant. Every control below is implemented and
verifiable in the live environment.

## 1. Microsoft Entra ID authentication

No component authenticates with a key or connection string. All access flows
through Entra ID tokens obtained by `DefaultAzureCredential`.

    az login  ->  Entra ID token  ->  Storage, Key Vault, AI Services, Search

`verify.py` demonstrates this: seven services respond, no secret in any file.

**What it prevents.** A leaked key grants indefinite standing access. Entra ID
tokens expire in roughly one hour and are bound to an identity that can be
revoked centrally.

**Evidence.** `verify.py` output, 7/7 passing.

## 2. Managed identity

A user-assigned managed identity (`id-bankai-app`) holds the application's
permissions. The Azure AI Search service additionally has a system-assigned
identity for its outbound calls.

| Principal | Resource | Role | Why |
|---|---|---|---|
| App (UAMI) | Storage | Storage Blob Data Contributor | Read raw, write processed and extracted |
| App (UAMI) | Key Vault | Key Vault Secrets User | Read secrets at runtime |
| App (UAMI) | AI Search | Search Index Data Contributor | Query and upload |
| App (UAMI) | AI Services | Cognitive Services OpenAI User | Chat and embeddings |
| App (UAMI) | AI Services | Cognitive Services User | Document Intelligence, Language, Speech |
| Search (SMI) | Storage | Storage Blob Data Reader | Read policy blobs |
| Search (SMI) | AI Services | Cognitive Services OpenAI User | Vectorization |

Every role is the narrowest that permits the operation. No principal holds
Contributor or Owner at any data plane.

**What it prevents.** Credentials that must be created, distributed, rotated and
eventually leaked. A managed identity has no secret to steal.

**Evidence.** `docs/rbac-matrix.md`, generated from the live environment.

## 3. The control plane is not the data plane

Subscription Owner does not grant permission to read a blob. Data-plane roles are
assigned separately, per resource.

This caused a real failure during implementation: filesystem creation returned
`AuthorizationPermissionMismatch` despite Owner rights, until
`Storage Blob Data Contributor` was assigned and allowed to propagate.

**What it prevents.** Administrative access silently conferring data access. An
administrator who can manage a storage account cannot necessarily read customer
documents.

## 4. Azure Key Vault

Vault `kv-bankai-alt742`, RBAC authorisation mode, purge protection enabled,
7-day soft-delete retention.

Only true secrets are stored. Endpoints, deployment names and index names are
configuration and live in `.env`, which is gitignored.

**Incident during implementation.** The AI Services key was echoed to the
terminal by `az keyvault secret set` without `-o none`, exposing it in a
transcript. It was regenerated within seconds:

    az cognitiveservices account keys regenerate -n <account> -g <rg> --key-name key1

**Zero application impact**, because no component authenticates with that key. It
exists only as a documented fallback. This is the strongest available argument
for managed identity: the blast radius of a leaked credential is proportional to
how much the system depends on it, and here it was nil.

## 5. Transport and network

- Storage: TLS 1.2 minimum, public blob access disabled
- All service endpoints HTTPS only
- AI Services uses a custom subdomain, which is required for Entra ID token auth
- Azure AI Search configured with `aadOrApiKey` and
  `http401WithBearerChallenge`

## 6. Data protection

Masking happens at the **presentation boundary**, not at storage.

    extracted-data/  ->  full values, RBAC protected
                         (a bank needs the real account number)
             |
             v
    UI and LLM prompts  ->  masked
                            XXXXXXX1234, XXXXX234F, R**** S*****

Two layers, because neither alone is sufficient:

1. **Azure AI Language PII detection** catches unstructured identifiers. It
   correctly identified the customer name at confidence 1.00 and the account
   number at 0.75.
2. **Domain rules** catch structured identifiers the service does not model:
   customer IDs (`C1001`), IFSC codes, Indian PAN format.

A bug found during implementation demonstrates why both are needed: an early
version of `mask_fields` applied only the regex rules, so `Rahul Sharma` passed
through unmasked. Names cannot be matched by pattern; the service catches them,
the rules do not.

**What it prevents.** Customer identifiers reaching a screen, a log, or a model
prompt. The model never receives an unmasked account number, so it cannot repeat
one regardless of how it is prompted.

## 7. Encryption at rest

Azure Storage service-side encryption with Microsoft-managed keys, enabled by
default. Confirmed by `request_server_encrypted: true` on every write.

## 8. Cost and blast-radius control

Azure AI Search is torn down between working sessions via
`infra/search-down.ps1` and rebuilt with `infra/search-up.ps1`. A deleted service
cannot be attacked, and on a fixed-credit subscription an idle hourly resource is
itself a risk to availability.

## Not implemented, and why

**Private endpoints and VNet integration.** Correct for production. Out of scope
for a capstone on an Azure for Students subscription, which restricts networking
features, and would prevent local development entirely.

**Disabling local auth** (`--disable-local-auth`, `--allow-shared-key-access false`).
The natural next step. Deferred because the Key Vault fallback path and some CLI
tooling still reference keys; enabling it would be a one-line change per resource
once those are removed.

**Customer-managed encryption keys.** Microsoft-managed keys are sufficient for
this threat model. CMK matters when key custody must be provable to a regulator.

## Verification

    python verify.py                 # 7/7 services over Entra ID
    az role assignment list --scope <resource-id>   # per-resource RBAC
    git log -p | grep -Ei "key|secret|password"     # no credentials in history

Removal is not straightforward. `az role assignment delete --assignee <id>`
resolves the principal in Microsoft Graph before deleting, and an orphaned
assignment by definition references a principal that no longer exists:

    Cannot find user or service principal in graph database for '<id>'

The assignment must be deleted by its own resource ID instead:

    $id = az role assignment list --scope <scope> --query "[?principalId=='<orphan>'].id" -o tsv
    az role assignment delete --ids $id

An orphaned assignment is therefore harder to remove than it was to create,
which is precisely why these accumulate in long-lived subscriptions.
