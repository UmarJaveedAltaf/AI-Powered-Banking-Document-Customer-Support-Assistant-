"""Process a document end-to-end and persist the extracted JSON to ADLS."""
import json
import time
from azure.storage.blob import BlobServiceClient
from config.settings import get_settings, credential
from backend.extraction.doc_intelligence import fetch_blob, analyze, table_rows, needs_ocr
from backend.extraction.schema import normalise
from backend.validation.rules import summary


def store_json(payload: dict, path: str, container: str = "extracted-data") -> str:
    s = get_settings()
    bsc = BlobServiceClient(s.blob_endpoint, credential())
    bc = bsc.get_blob_client(container, path)
    bc.upload_blob(json.dumps(payload, indent=2).encode("utf-8"), overwrite=True)
    return f"{container}/{path}"


def process(blob_path: str) -> dict:
    started = time.time()
    data = fetch_blob(blob_path)
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
    out = store_json(payload, f"{app.customer_id}/{blob_path.split('/')[-1]}.json")
    payload["processing"]["output_blob"] = out
    return payload


if __name__ == "__main__":
    paths = [
        "loan/customer_1001_home_loan_application.pdf",
        "loan/customer_1002_home_loan_application.pdf",
        "loan/customer_1003_personal_loan_application.pdf",
        "loan/customer_1004_home_loan_application.pdf",
        "loan/customer_1005_personal_loan_application.pdf",
    ]
    ok = 0
    for p in paths:
        r = process(p)
        pr = r["processing"]
        ok += pr["status"] == "succeeded"
        print(f"{r['customer_id']}  {pr['fields_found']}/{pr['fields_expected']} fields  "
              f"{pr['duration_seconds']}s  {pr['status']:9}  -> {pr['output_blob']}")

    print(f"\nProcessed {len(paths)} documents, {ok} succeeded, {len(paths) - ok} partial.")
    print("\nSample deliverable JSON (C1001):")
    r = process(paths[0])
    print(json.dumps({k: r[k] for k in ("customer_id", "loan_type", "amount", "income")}, indent=2))
