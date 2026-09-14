"""Embed policy chunks and upload them to the search index."""
from openai import AzureOpenAI
from azure.search.documents import SearchClient
from config.settings import get_settings, credential, token_provider
from backend.search.chunker import chunk_document, TITLES
from backend.extraction.doc_intelligence import fetch_blob


def _openai() -> AzureOpenAI:
    s = get_settings()
    return AzureOpenAI(azure_endpoint=s.azure_openai_endpoint,
                       api_version=s.azure_openai_api_version,
                       azure_ad_token_provider=token_provider())


def embed(texts: list[str], batch: int = 64) -> list[list[float]]:
    s = get_settings()
    client = _openai()
    vectors = []
    for i in range(0, len(texts), batch):
        r = client.embeddings.create(model=s.azure_openai_embedding_deployment,
                                     input=texts[i:i + batch])
        vectors.extend(d.embedding for d in r.data)
        print(f"  embedded {min(i + batch, len(texts))}/{len(texts)}")
    return vectors


def search_client() -> SearchClient:
    s = get_settings()
    return SearchClient(s.search_endpoint, s.search_index_name, credential())


def build_and_upload() -> int:
    all_chunks = []
    for source_file in TITLES:
        chunks = chunk_document(fetch_blob(f"policies/{source_file}"), source_file)
        all_chunks.extend(chunks)
        print(f"  {source_file:32} {len(chunks):>3} chunks")

    print(f"\nEmbedding {len(all_chunks)} chunks ...")
    vectors = embed([c["content"] for c in all_chunks])
    for chunk, vec in zip(all_chunks, vectors):
        chunk["contentVector"] = vec

    print("\nUploading ...")
    client = search_client()
    uploaded = 0
    for i in range(0, len(all_chunks), 500):
        results = client.upload_documents(all_chunks[i:i + 500])
        uploaded += sum(1 for r in results if r.succeeded)
        for r in results:
            if not r.succeeded:
                print(f"  FAILED {r.key}: {r.error_message}")
    return uploaded


if __name__ == "__main__":
    n = build_and_upload()
    print(f"\nUploaded {n} documents.")

    import time
    time.sleep(3)
    print(f"Index now contains {search_client().get_document_count()} documents.")
