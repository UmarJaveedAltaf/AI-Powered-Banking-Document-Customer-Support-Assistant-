"""PII masking at the presentation boundary. Storage keeps full values; the UI and
the model never see them."""
import re
from azure.ai.textanalytics import TextAnalyticsClient
from config.settings import get_settings, credential

# Domain identifiers Azure AI Language will not catch on its own.
RULES = [
    ("pan", re.compile(r"\b([A-Z]{5}\d{4}[A-Z])\b"),
     lambda m: "XXXXX" + m.group(1)[-4:]),
    ("ifsc", re.compile(r"\b([A-Z]{4}0\d{6})\b"),
     lambda m: m.group(1)[:4] + "XXXXXXX"),
    ("account_number", re.compile(r"\b(\d{9,18})\b"),
     lambda m: "X" * (len(m.group(1)) - 4) + m.group(1)[-4:]),
    ("customer_id", re.compile(r"\b(C\d{4})\b"),
     lambda m: "CXXX" + m.group(1)[-1]),
    ("aadhaar", re.compile(r"\b(\d{4}\s\d{4}\s\d{4})\b"),
     lambda m: "XXXX XXXX " + m.group(1)[-4:]),
]

MASKED_KEYS = {"pan", "account_number", "customer_id", "aadhaar", "ifsc",
               "date_of_birth", "mobile", "email", "address", "customer_name"}


def mask_rules(text: str) -> str:
    for _, rx, fn in RULES:
        text = rx.sub(fn, text)
    return text


def mask_language(texts: list[str]) -> list[str]:
    """Azure AI Language PII detection. Max 5 documents per request."""
    client = TextAnalyticsClient(get_settings().ai_services_endpoint, credential())
    out = []
    for i in range(0, len(texts), 5):
        batch = texts[i:i + 5]
        for doc in client.recognize_pii_entities(batch, language="en"):
            out.append(doc.redacted_text if not doc.is_error else batch[len(out) % 5])
    return out


def mask(text: str, use_language_service: bool = True) -> str:
    """Layered: service-detected PII first, then domain rules."""
    if use_language_service:
        try:
            text = mask_language([text])[0]
        except Exception:
            pass          # rules below still apply
    return mask_rules(text)


NAME_KEYS = {"customer_name", "applicant_name", "father_name"}


def mask_name(name: str) -> str:
    parts = str(name).split()
    return " ".join(p[0] + "*" * (len(p) - 1) if len(p) > 1 else p for p in parts)


def mask_fields(fields: dict) -> dict:
    """Mask a dict of extracted values for UI display."""
    out = {}
    for k, v in fields.items():
        if k in NAME_KEYS:
            out[k] = mask_name(v)
        elif k in MASKED_KEYS:
            out[k] = mask_rules(str(v))
        else:
            out[k] = v
    return out


def detect_entities(text: str) -> list[dict]:
    """What the Language service found, for the responsible-AI writeup."""
    client = TextAnalyticsClient(get_settings().ai_services_endpoint, credential())
    doc = client.recognize_pii_entities([text], language="en")[0]
    if doc.is_error:
        return []
    return [{"text": e.text, "category": e.category, "confidence": round(e.confidence_score, 2)}
            for e in doc.entities]


if __name__ == "__main__":
    from backend.extraction.ocr import process_scanned

    r = process_scanned("statements/customer_1001_bank_statement_scanned.pdf")

    print("=== EXTRACTED (stored in extracted-data, RBAC protected) ===")
    for k, v in r["fields"].items():
        print(f"  {k:20} {v}")

    print("\n=== MASKED (what the UI and the model see) ===")
    for k, v in mask_fields(r["fields"]).items():
        print(f"  {k:20} {v}")

    print("\n=== PII DETECTED BY AZURE AI LANGUAGE ===")
    sample = "\n".join(r["raw_text"].splitlines()[:12])
    for e in detect_entities(sample):
        print(f"  {e['category']:18} {e['text']:24} confidence={e['confidence']}")

    print("\n=== FULL TEXT, LAYERED MASKING ===")
    for line in mask(sample).splitlines():
        print(f"  {line}")

    leaked = [s for s in ("90210041234", "ABCDE1234F") if s in mask(sample)]
    print(f"\n  leaked identifiers: {leaked or 'none'}")

