"""Document Intelligence client. prebuilt-layout for structured forms, prebuilt-read for OCR."""
import io
import pypdf
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.storage.blob import BlobServiceClient
from config.settings import get_settings, credential


def _client() -> DocumentIntelligenceClient:
    return DocumentIntelligenceClient(get_settings().ai_services_endpoint, credential())


def fetch_blob(path: str, container: str = "raw-documents") -> bytes:
    s = get_settings()
    bsc = BlobServiceClient(s.blob_endpoint, credential())
    return bsc.get_blob_client(container, path).download_blob().readall()


def needs_ocr(data: bytes, min_chars: int = 50) -> bool:
    """True when the PDF has no usable text layer."""
    try:
        r = pypdf.PdfReader(io.BytesIO(data))
        text = "".join((p.extract_text() or "") for p in r.pages)
        return len(text.strip()) < min_chars
    except Exception:
        return True


def analyze(data: bytes, model_id: str = "prebuilt-layout") -> AnalyzeResult:
    poller = _client().begin_analyze_document(
        model_id, body=data, content_type="application/octet-stream")
    return poller.result()


def table_rows(result: AnalyzeResult) -> list[dict]:
    """Two-column label/value tables -> list of {label, value}."""
    rows = []
    for t in (result.tables or []):
        grid = {}
        for c in t.cells:
            grid.setdefault(c.row_index, {})[c.column_index] = c.content.strip()
        for r in grid.values():
            label = r.get(0, "").strip().rstrip(":")
            value = r.get(1, "").strip()
            if label and value:
                rows.append({"label": label, "value": value})
    return rows


if __name__ == "__main__":
    path = "loan/customer_1001_home_loan_application.pdf"
    print(f"Fetching {path} ...")
    data = fetch_blob(path)
    print(f"  {len(data):,} bytes | needs OCR: {needs_ocr(data)}")

    print("Analyzing with prebuilt-layout ...")
    result = analyze(data)
    print(f"  pages={len(result.pages or [])} tables={len(result.tables or [])}")

    print("\nExtracted label/value pairs:")
    for row in table_rows(result):
        print(f"  {row['label']:38} = {row['value']}")
