"""Upload a file supplied at runtime, then process it end to end."""
import time
from azure.storage.blob import BlobServiceClient
from config.settings import get_settings, credential
from backend.extraction.doc_intelligence import analyze, table_rows, needs_ocr
from backend.extraction.schema import normalise
from backend.validation.rules import summary
from backend.extraction.pipeline import store_json
from backend.common.telemetry import tracked

PREFIX_BY_KIND = {"loan_application": "loan", "bank_statement": "statements",
                  "identity": "identity", "policy": "policies", "other": "loan"}


def upload_bytes(data: bytes, filename: str, kind: str = "loan_application") -> str:
    """Put an uploaded file into raw-documents/<prefix>/<filename>."""
    s = get_settings()
    prefix = PREFIX_BY_KIND.get(kind, "loan")
    path = f"{prefix}/{filename}"
    cc = BlobServiceClient(s.blob_endpoint, credential()).get_container_client("raw-documents")
    cc.upload_blob(path, data, overwrite=True,
                   metadata={"doc_class": kind, "uploaded": "runtime"})
    return path


@tracked("document_processed")
def process_bytes(data: bytes, blob_path: str) -> dict:
    """Same pipeline as backend.extraction.pipeline.process, but on in-memory bytes."""
    started = time.time()
    ocr = needs_ocr(data)
    model = "prebuilt-read" if ocr else "prebuilt-layout"
    result = analyze(data, model_id=model)
    app = normalise(table_rows(result), source_file=blob_path)
    checks = summary(app)

    payload = {
        "customer_id": app.customer_id,
        "loan_type": app.loan_type.upper().replace(" ", "_"),
        "amount": app.requested_amount,
        "income": app.monthly_income,
        "extraction": app.model_dump(),
        "validation": checks,
        "processing": {
            "source_blob": blob_path,
            "model_id": model,
            "ocr_required": ocr,
            "pages": len(result.pages or []),
            "fields_expected": app.fields_expected,
            "fields_found": app.fields_found,
            "duration_seconds": round(time.time() - started, 2),
            "status": "succeeded" if app.fields_found == app.fields_expected else "partial",
        },
    }
    payload["processing"]["output_blob"] = store_json(
        payload, f"{app.customer_id}/{blob_path.split('/')[-1]}.json")
    return payload


def upload_and_process(data: bytes, filename: str, kind: str = "loan_application") -> dict:
    return process_bytes(data, upload_bytes(data, filename, kind))


def corpus_stats() -> dict:
    """Live counts for the dashboard."""
    s = get_settings()
    cc = BlobServiceClient(s.blob_endpoint, credential()).get_container_client("raw-documents")
    counts = {}
    for b in cc.list_blobs():
        if b.size > 0:
            counts[b.name.split("/")[0]] = counts.get(b.name.split("/")[0], 0) + 1

    try:
        from backend.search.indexer import search_client
        chunks = search_client().get_document_count()
    except Exception:
        chunks = 0

    return {
        "policies": counts.get("policies", 0),
        "applications": counts.get("loan", 0),
        "scanned": counts.get("statements", 0) + counts.get("identity", 0),
        "indexed_chunks": chunks,
        "total_blobs": sum(counts.values()),
    }
