"""OCR for image-only documents via prebuilt-read."""
import re
from backend.extraction.doc_intelligence import fetch_blob, analyze, needs_ocr


def ocr_text(data: bytes) -> str:
    result = analyze(data, model_id="prebuilt-read")
    return "\n".join(line.content
                     for page in (result.pages or [])
                     for line in (page.lines or []))


PATTERNS = {
    "account_number": re.compile(r"Account Number\s*:?\s*(\d{6,18})", re.I),
    "customer_name": re.compile(r"Customer Name\s*:?\s*([A-Z][A-Za-z .]+)", re.I),
    "customer_id": re.compile(r"Customer ID\s*:?\s*(C\d{4})", re.I),
    "pan": re.compile(r"\b([A-Z]{5}\d{4}[A-Z])\b"),
    "ifsc": re.compile(r"IFSC Code\s*:?\s*([A-Z]{4}\d{7})", re.I),
    "statement_period": re.compile(r"Statement Period\s*:?\s*(.+)", re.I),
    "closing_balance": re.compile(r"Closing Balance\s*:?\s*(\d+)", re.I),
    "date_of_birth": re.compile(r"Date of Birth\s*:?\s*(\d{2}/\d{2}/\d{4})", re.I),
}


def extract_fields(text: str) -> dict:
    out = {}
    for name, rx in PATTERNS.items():
        m = rx.search(text)
        if m:
            out[name] = m.group(1).strip()
    return out


def process_scanned(blob_path: str) -> dict:
    data = fetch_blob(blob_path)
    ocr = needs_ocr(data)
    text = ocr_text(data)
    return {
        "source_blob": blob_path,
        "ocr_required": ocr,
        "characters_recovered": len(text),
        "fields": extract_fields(text),
        "raw_text": text,
    }


if __name__ == "__main__":
    for path in ["statements/customer_1001_bank_statement_scanned.pdf",
                 "statements/customer_1001_identity_card_scanned.pdf"]:
        r = process_scanned(path)
        print(f"\n{'=' * 70}")
        print(f"{path.split('/')[-1]}")
        print(f"  text layer present : {not r['ocr_required']}")
        print(f"  characters via OCR : {r['characters_recovered']:,}")
        print("=" * 70)
        for k, v in r["fields"].items():
            print(f"  {k:20} {v}")
        print("\n  First 8 lines recovered:")
        for line in r["raw_text"].splitlines()[:8]:
            print(f"    {line}")
