"""Section-aware chunking. Each chunk carries its document title and section heading."""
import io
import re
import pypdf
import tiktoken
from config.settings import get_settings

ENC = tiktoken.get_encoding("cl100k_base")
HEADING = re.compile(r"^(\d{1,2})\.\s+([A-Z][A-Za-z ,\-]{3,70})$", re.M)

TITLES = {
    "home_loan_policy.pdf": "Home Loan Policy 2026",
    "personal_loan_policy.pdf": "Personal Loan Policy 2026",
    "kyc_policy.pdf": "KYC Policy 2026",
    "credit_card_policy.pdf": "Credit Card Policy 2026",
    "account_opening_policy.pdf": "Account Opening Policy 2026",
    "aml_policy.pdf": "Anti-Money Laundering Policy 2026",
    "complaint_policy.pdf": "Customer Complaint Policy 2026",
    "vehicle_loan_policy.pdf": "Vehicle Loan Policy 2026",
    "fair_practices_code.pdf": "Fair Practices Code 2026",
    "data_privacy_policy.pdf": "Customer Data Privacy Policy 2026",
    "digital_banking_policy.pdf": "Digital Banking Policy 2026",
    "collection_and_recovery_policy.pdf": "Collection and Recovery Policy 2026",
}


def pdf_pages(data: bytes) -> list[str]:
    return [(p.extract_text() or "") for p in pypdf.PdfReader(io.BytesIO(data)).pages]


def split_sections(text: str) -> list[tuple[str, str]]:
    marks = [(m.start(), f"Section {m.group(1)}: {m.group(2).strip()}")
             for m in HEADING.finditer(text)]
    if not marks:
        return [("General", text.strip())]
    out = []
    for i, (pos, head) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        body = text[pos:end].strip()
        if body:
            out.append((head, body))
    return out


def window(tokens: list[int], size: int, overlap: int):
    step = max(size - overlap, 1)
    for i in range(0, max(len(tokens), 1), step):
        yield tokens[i:i + size]
        if i + size >= len(tokens):
            break


def chunk_document(data: bytes, source_file: str) -> list[dict]:
    s = get_settings()
    title = TITLES.get(source_file, source_file)
    pages = pdf_pages(data)
    full = "\n".join(pages)
    chunks, ci = [], 0

    for section, body in split_sections(full):
        probe = body[:60].replace("\n", " ")[:40]
        page = next((n + 1 for n, p in enumerate(pages) if probe and probe in p.replace("\n", " ")), 1)
        for w in window(ENC.encode(body), s.chunk_tokens, s.chunk_overlap):
            text = ENC.decode(w)
            chunks.append({
                "id": f"{source_file.replace('.pdf', '').replace('_', '-')}-{ci}",
                "content": f"[{title} - {section}]\n{text}",
                "title": title,
                "section": section,
                "source_file": source_file,
                "page": page,
                "chunk_index": ci,
            })
            ci += 1
    return chunks


if __name__ == "__main__":
    from backend.extraction.doc_intelligence import fetch_blob

    total = 0
    for f in TITLES:
        chunks = chunk_document(fetch_blob(f"policies/{f}"), f)
        total += len(chunks)
        secs = sorted({c["section"] for c in chunks})
        print(f"\n{f}  ->  {len(chunks)} chunks, {len(secs)} sections")
        for s in secs:
            print(f"    {s}")

    print(f"\nTotal chunks: {total}")

    hl = chunk_document(fetch_blob("policies/home_loan_policy.pdf"), "home_loan_policy.pdf")
    emp = [c for c in hl if "Employment Eligibility" in c["section"]]
    print(f"\n--- Employment Eligibility chunk (page {emp[0]['page']}) ---")
    print(emp[0]["content"][:600])

