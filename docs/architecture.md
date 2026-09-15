# Architecture

Horizon National Bank — AI Document & Customer Support Assistant.

![Architecture](architecture.svg)

## Diagram (renders on GitHub)

```mermaid
flowchart TB
    U([Bank employee]) --> UI[Streamlit application<br/>9 screens]
    UI -.PII masked here.-> MASK{{Masking boundary<br/>account no · PAN · Aadhaar · name}}
    UI --> ID[/Microsoft Entra ID<br/>DefaultAzureCredential<br/>managed identity — no keys/]

    ID --> DOC
    ID --> Q

    subgraph DOC [Document path]
        direction TB
        B[(Blob / ADLS Gen2<br/>raw-documents/)] --> OCRQ{Text layer<br/>present?}
        OCRQ -- no --> READ[Document Intelligence<br/>prebuilt-read — OCR]
        OCRQ -- yes --> LAY[Document Intelligence<br/>prebuilt-layout]
        READ --> SCH[Pydantic typed schema<br/>2 years → 2.0]
        LAY --> SCH
        SCH --> RULE[[DETERMINISTIC RULE ENGINE<br/>thresholds traceable to policy clauses]]
        RULE --> JSON[(extracted-data/<br/>customer JSON)]
    end

    subgraph Q [Query path]
        direction TB
        QU[Question<br/>typed or spoken] --> EMB[Azure OpenAI<br/>text-embedding-3-small · 1536d]
        EMB --> SRCH[(Azure AI Search<br/>104 chunks · HNSW<br/>BM25 + vector + semantic)]
        SRCH --> CTX[Top-k chunks → context<br/>section heading carried inline]
        CTX --> LLM[Azure OpenAI · gpt-4.1-mini<br/>temperature 0 · strict JSON schema]
        LLM --> ANS[Grounded explanation<br/>+ citation]
    end

    RULE --> XC[[VERDICT CROSS-CHECK]]
    ANS --> XC
    XC --> OUT([status ← rule engine<br/>reason ← model<br/>human_review_required = True])

    LANG[Azure AI Language<br/>sentiment · PII detection] --> UI
    SPEECH[Azure AI Speech<br/>STT / TTS] --> QU
    UI --> OTEL[OpenTelemetry → Application Insights<br/>→ Log Analytics]

    classDef azure fill:#e8f1fb,stroke:#4a90d9,stroke-width:1.5px
    classDef det fill:#e9f7ee,stroke:#2e9e5b,stroke-width:2px
    classDef sec fill:#fff4e6,stroke:#d9932a,stroke-width:1.5px
    class B,READ,LAY,SRCH,EMB,LLM,JSON,LANG,SPEECH azure
    class RULE,XC,OUT det
    class ID,MASK sec
```

## The two paths

**Document path** turns a PDF into a verdict. Files land in ADLS Gen2, a text-layer
probe decides whether OCR is needed, Document Intelligence extracts fields, Pydantic
coerces them to real types, and a deterministic rule engine compares them against
policy thresholds. The result is persisted as JSON partitioned by customer.

**Query path** turns a question into a cited answer. The question is embedded with
the same deployment used for the corpus, hybrid retrieval returns the top chunks,
and the model writes an explanation constrained by a strict JSON schema.

The paths converge at the cross-check. `status` is copied from the rule engine and
never from the model. The model supplies `reason` — the human-readable explanation —
and nothing that affects the outcome. Agreement raises confidence; disagreement
lowers it and flags the case. Neither overrides the rules.

## Why the rule engine decides

An LLM asked to apply a numeric threshold will usually get it right and occasionally
will not, and there is no way to tell which from the output. A comparison against a
constant is correct every time and can be traced to the clause it came from.

The model is better than the rule engine at exactly one thing: explaining the
decision in language a customer would understand, with a citation. So it does that,
and only that.

## Four guardrail layers

| Layer | Mechanism | Where it runs |
|---|---|---|
| 1 | Azure AI Content Safety / Prompt Shields | Platform, before generation |
| 2 | System prompt rules 1–8 | Model instruction |
| 3 | Strict JSON schema, no `APPROVED` in the decision enum | API-constrained |
| 4 | Post-generation code guards | Python, after generation |

Layer 1 returns HTTP 400 with `jailbreak: detected` — the model never sees the
prompt. Layer 3 makes an approval structurally unrepresentable rather than merely
discouraged. Layer 4 exists because layer 2 proved unreliable: the assistant
disclosed its system prompt on one run and refused on another under identical
settings, despite an explicit instruction not to.

**The prompt states intent. Code enforces it.**

## Retrieval

| mode | top-1 | recall@5 | MRR |
|---|---|---|---|
| keyword | 7/10 | 10/10 | 0.817 |
| vector | 8/10 | 8/10 | 0.800 |
| hybrid | 8/10 | 10/10 | **0.870** |

Expanding the corpus from 7 to 12 policies *reduced* vector performance and
*improved* keyword performance. Vehicle Loan §3 and Home Loan §3 are semantically
near-identical — both state an employment minimum verified by the same means — so
embeddings place them close together. The discriminating token is the literal word
"home" versus "vehicle", which lexical search weighs and embeddings blur.

Hybrid absorbed both effects and stayed flat. That is the argument for it: not that
it wins every question, but that it is robust to corpus changes that degrade either
mode alone.

## Azure resources

| Resource | Purpose |
|---|---|
| Storage account (ADLS Gen2) | Raw documents, processed output, extracted JSON |
| Key Vault | Secret storage, RBAC authorisation, purge protection |
| AI Services (S0) | Document Intelligence, Language, Speech, OpenAI |
| `gpt-4.1-mini` | Explanation and structured output |
| `text-embedding-3-small` | 1536-dimension embeddings |
| AI Search (Basic) | Hybrid retrieval, HNSW index, semantic reranker |
| Log Analytics + Application Insights | Telemetry, latency, token spend |
| User-assigned managed identity | Application identity, 5 data-plane roles |

Region `centralus` — `eastus` is blocked by an Azure for Students regional policy.

## Data flow for the demo scenario

1. `customer_1001_home_loan_application.pdf` uploaded to `raw-documents/loan/`
2. Text layer present → `prebuilt-layout` → 27 label/value pairs
3. Normalised → `total_experience_years = 2.0`
4. Rule engine: Home Loan §3 requires 3.0 → **fails**, 6 of 7 criteria pass
5. Retrieval returns Home Loan Policy §3 as top hit
6. Model explains, citing `home_loan_policy.pdf, Section 3: Employment Eligibility`
7. Cross-check: both verdicts agree → confidence HIGH
8. `human_review_required: true`, assigned in Python
