"""Upload the sample dataset to ADLS Gen2 under raw-documents/."""
from pathlib import Path
from azure.storage.blob import BlobServiceClient
from config.settings import get_settings, credential

PREFIX = {
    "policy-documents": "policies",
    "customer-documents": "loan",
    "scanned-documents": "statements",
    "customer-messages": "kyc",
}


def upload_all(root: str = "data") -> int:
    s = get_settings()
    cc = BlobServiceClient(s.blob_endpoint, credential()).get_container_client("raw-documents")
    n = 0
    for folder, prefix in PREFIX.items():
        src = Path(root, folder)
        if not src.exists():
            print(f"  SKIP {folder} (not found)")
            continue
        for f in sorted(src.glob("*.*")):
            with open(f, "rb") as fh:
                cc.upload_blob(f"{prefix}/{f.name}", fh, overwrite=True,
                               metadata={"doc_class": folder.replace("-", "_")})
            print(f"  {prefix}/{f.name}  ({f.stat().st_size:,} bytes)")
            n += 1
    return n


if __name__ == "__main__":
    total = upload_all()
    print(f"\nUploaded {total} files.")
