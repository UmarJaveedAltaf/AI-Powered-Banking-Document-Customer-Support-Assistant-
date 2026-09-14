"""Normalise raw Document Intelligence output into a typed, validated schema."""
import re
from pydantic import BaseModel, Field


class LoanApplication(BaseModel):
    customer_id: str
    customer_name: str
    loan_type: str
    requested_amount: int
    monthly_income: int
    monthly_obligations: int = 0
    employment_type: str
    total_experience_years: float
    current_employer_months: float = 0
    bureau_score: int | None = None
    tenure_years: int | None = None
    documents_submitted: dict[str, bool] = Field(default_factory=dict)
    source_file: str = ""
    fields_expected: int = 0
    fields_found: int = 0


def parse_inr(v: str) -> int:
    return int(re.sub(r"[^\d]", "", v or "") or 0)


def parse_years(v: str) -> float:
    v = (v or "").lower()
    y = re.search(r"(\d+(?:\.\d+)?)\s*year", v)
    m = re.search(r"(\d+)\s*month", v)
    return (float(y.group(1)) if y else 0.0) + (int(m.group(1)) / 12 if m else 0.0)


def parse_months(v: str) -> float:
    return round(parse_years(v) * 12, 1)


def parse_int(v: str) -> int | None:
    d = re.sub(r"[^\d]", "", v or "")
    return int(d) if d else None


FIELD_MAP = {
    "Customer ID": ("customer_id", str.strip),
    "Applicant Name": ("customer_name", str.strip),
    "Loan Type": ("loan_type", str.strip),
    "Employment Type": ("employment_type", str.strip),
    "Requested Loan Amount": ("requested_amount", parse_inr),
    "Net Monthly Income": ("monthly_income", parse_inr),
    "Existing Monthly Obligations": ("monthly_obligations", parse_inr),
    "Total Employment History": ("total_experience_years", parse_years),
    "Experience with Current Employer": ("current_employer_months", parse_months),
    "Credit Bureau Score": ("bureau_score", parse_int),
    "Requested Tenure": ("tenure_years", parse_int),
}

DOC_LABELS = ["Identity Proof", "Address Proof", "Income Proof",
              "Bank Statements (6 months)", "Employment Proof", "Property Documents"]


def normalise(rows: list[dict], source_file: str = "") -> LoanApplication:
    data, docs, found = {}, {}, 0
    for row in rows:
        label, value = row["label"], row["value"]
        if label in FIELD_MAP:
            key, fn = FIELD_MAP[label]
            data[key] = fn(value)
            found += 1
        elif label in DOC_LABELS:
            v = value.lower().strip()
            if v.startswith("not applicable") or v.startswith("n/a"):
                continue
            docs[label] = v.startswith("submitted")
    data["documents_submitted"] = docs
    data["source_file"] = source_file
    data["fields_expected"] = len(FIELD_MAP)
    data["fields_found"] = found
    return LoanApplication(**data)


if __name__ == "__main__":
    from backend.extraction.doc_intelligence import fetch_blob, analyze, table_rows

    path = "loan/customer_1001_home_loan_application.pdf"
    app = normalise(table_rows(analyze(fetch_blob(path))), source_file=path)

    print(f"\nExtraction: {app.fields_found}/{app.fields_expected} fields\n")
    for k, v in app.model_dump().items():
        if k != "documents_submitted":
            print(f"  {k:26} {v!r}")
    print("\n  documents_submitted:")
    for k, v in app.documents_submitted.items():
        print(f"    {'OK ' if v else 'MISSING'} {k}")


