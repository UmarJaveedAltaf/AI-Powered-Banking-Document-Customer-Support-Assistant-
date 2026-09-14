"""Index the poisoned document so injection tests exercise real retrieval."""
from backend.search.chunker import chunk_document
from backend.search.indexer import embed, search_client

POISON_FILE = "poisoned_policy.pdf"


def index_poison(path: str = "data/poisoned_policy.pdf") -> int:
    with open(path, "rb") as f:
        chunks = chunk_document(f.read(), POISON_FILE)
    for c, v in zip(chunks, embed([c["content"] for c in chunks])):
        c["contentVector"] = v
    search_client().upload_documents(chunks)
    return len(chunks)


def remove_poison() -> int:
    sc = search_client()
    hits = list(sc.search(search_text="*", filter=f"source_file eq '{POISON_FILE}'",
                          select=["id"], top=100))
    if hits:
        sc.delete_documents([{"id": h["id"]} for h in hits])
    return len(hits)


if __name__ == "__main__":
    import sys, time
    if "--remove" in sys.argv:
        print(f"Removed {remove_poison()} poisoned chunks.")
    else:
        print(f"Indexed {index_poison()} poisoned chunks.")
    time.sleep(3)
    print(f"Index now contains {search_client().get_document_count()} documents.")

