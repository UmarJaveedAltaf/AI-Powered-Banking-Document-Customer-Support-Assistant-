"""Prove every Azure service responds under Entra ID auth. No keys anywhere."""
import sys
from config.settings import get_settings, credential, token_provider

s = get_settings()
results = []


def check(name, fn):
    try:
        results.append((name, "PASS", fn()))
    except Exception as e:
        results.append((name, "FAIL", f"{type(e).__name__}: {e}"))


def storage():
    from azure.storage.blob import BlobServiceClient
    c = BlobServiceClient(s.blob_endpoint, credential())
    return ", ".join(sorted(x.name for x in c.list_containers()))


def keyvault():
    from azure.keyvault.secrets import SecretClient
    c = SecretClient(s.keyvault_uri, credential())
    return ", ".join(x.name for x in c.list_properties_of_secrets())


def openai_embed():
    from openai import AzureOpenAI
    c = AzureOpenAI(azure_endpoint=s.azure_openai_endpoint,
                    api_version=s.azure_openai_api_version,
                    azure_ad_token_provider=token_provider())
    r = c.embeddings.create(model=s.azure_openai_embedding_deployment, input="ping")
    dims = len(r.data[0].embedding)
    assert dims == s.embedding_dimensions, f"expected {s.embedding_dimensions}, got {dims}"
    return f"{dims} dimensions"


def openai_chat():
    from openai import AzureOpenAI
    c = AzureOpenAI(azure_endpoint=s.azure_openai_endpoint,
                    api_version=s.azure_openai_api_version,
                    azure_ad_token_provider=token_provider())
    r = c.chat.completions.create(model=s.azure_openai_chat_deployment,
                                  messages=[{"role": "user", "content": "Reply with exactly: OK"}],
                                  max_tokens=10, temperature=0)
    return f"{r.choices[0].message.content!r} ({r.usage.total_tokens} tokens)"


def doc_intelligence():
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    DocumentIntelligenceClient(s.ai_services_endpoint, credential())
    return "client constructed"


def language():
    from azure.ai.textanalytics import TextAnalyticsClient
    c = TextAnalyticsClient(s.ai_services_endpoint, credential())
    r = c.analyze_sentiment(["This service has been excellent."], language="en")[0]
    return f"sentiment={r.sentiment} (pos={r.confidence_scores.positive:.2f})"


def search():
    from azure.search.documents.indexes import SearchIndexClient
    c = SearchIndexClient(s.search_endpoint, credential())
    names = list(c.list_index_names())
    return ", ".join(names) if names else "no indexes yet (expected)"


if __name__ == "__main__":
    print(f"\nRegion : {s.azure_region}")
    print(f"Chat   : {s.azure_openai_chat_deployment}")
    print(f"Embed  : {s.azure_openai_embedding_deployment} ({s.embedding_dimensions}d)\n")

    check("Storage / ADLS", storage)
    check("Key Vault", keyvault)
    check("OpenAI embeddings", openai_embed)
    check("OpenAI chat", openai_chat)
    check("Document Intelligence", doc_intelligence)
    check("AI Language", language)
    check("AI Search", search)

    for name, status, detail in results:
        print(f"  [{status}] {name:24} {detail}")

    failed = [r for r in results if r[1] == "FAIL"]
    print(f"\n{len(results) - len(failed)}/{len(results)} passed\n")
    sys.exit(1 if failed else 0)