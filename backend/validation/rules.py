"""Deterministic policy validation. The verdict comes from here, never from the LLM."""
from dataclasses import dataclass, asdict


@dataclass
class Criterion:
    name: str
    policy_ref: str
    section: str
    required: str
    actual: str
    passed: bool

    def dict(self) -> dict:
        return asdict(self)


HOME_LOAN = {
    "min_total_experience_years": 3.0,
    "min_current_employer_months": 6.0,
    "min_monthly_income": 50000,
    "min_loan_amount": 500000,
    "max_loan_amount": 100000000,
    "max_foir_pct": 50.0,
    "min_bureau_score": 700,
}

PERSONAL_LOAN = {
    "min_total_experience_years": 2.0,
    "min_current_employer_months": 12.0,
    "min_monthly_income": 30000,
    "min_loan_amount": 50000,
    "max_loan_amount": 4000000,
    "max_foir_pct": 55.0,
    "min_bureau_score": 720,
}

POLICY_FILE = {"Home Loan": "home_loan_policy.pdf", "Personal Loan": "personal_loan_policy.pdf"}


def estimate_emi(principal: int, years: int, annual_rate: float = 0.09) -> float:
    if not years:
        return 0.0
    r, n = annual_rate / 12, years * 12
    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)


def foir_pct(app) -> float:
    if not app.monthly_income:
        return 0.0
    emi = estimate_emi(app.requested_amount, app.tenure_years or (7 if app.loan_type == "Personal Loan" else 20))
    return round(100 * (app.monthly_obligations + emi) / app.monthly_income, 1)


def validate(app) -> list[Criterion]:
    rules = HOME_LOAN if app.loan_type == "Home Loan" else PERSONAL_LOAN
    pf = POLICY_FILE.get(app.loan_type, "home_loan_policy.pdf")
    out = []

    def add(name, section, required, actual, passed):
        out.append(Criterion(name, pf, section, required, actual, passed))

    add("Total employment history", "Section 3: Employment Eligibility",
        f"{rules['min_total_experience_years']:g} years",
        f"{app.total_experience_years:g} years",
        app.total_experience_years >= rules["min_total_experience_years"])

    add("Current employer tenure", "Section 3: Employment Eligibility",
        f"{rules['min_current_employer_months']:g} months",
        f"{app.current_employer_months:g} months",
        app.current_employer_months >= rules["min_current_employer_months"])

    add("Net monthly income", "Section 4: Income Criteria",
        f"INR {rules['min_monthly_income']:,}", f"INR {app.monthly_income:,}",
        app.monthly_income >= rules["min_monthly_income"])

    add("Loan amount within limits", "Section 5: Loan Amount and Tenure",
        f"INR {rules['min_loan_amount']:,} to {rules['max_loan_amount']:,}",
        f"INR {app.requested_amount:,}",
        rules["min_loan_amount"] <= app.requested_amount <= rules["max_loan_amount"])

    f = foir_pct(app)
    add("FOIR (advisory)", "Section 4: Income Criteria",
        f"at most {rules['max_foir_pct']:g}% (rate assumption not in policy)",
        f"{f:g}% (estimated)", True)

    if app.bureau_score is not None:
        add("Credit bureau score", "Section 7: Credit Assessment",
            str(rules["min_bureau_score"]), str(app.bureau_score),
            app.bureau_score >= rules["min_bureau_score"])

    missing = [k for k, v in app.documents_submitted.items() if not v]
    add("Required documents", "Section 6: Required Documents",
        "all submitted",
        "all submitted" if not missing else f"missing: {', '.join(missing)}",
        not missing)

    return out


def summary(app) -> dict:
    crit = validate(app)
    failed = [c for c in crit if not c.passed]
    return {
        "customer_id": app.customer_id,
        "loan_type": app.loan_type,
        "criteria": [c.dict() for c in crit],
        "passed_count": len(crit) - len(failed),
        "total_count": len(crit),
        "failed_criteria": [c.name for c in failed],
        "overall": "ALL_CRITERIA_MET" if not failed else "CRITERIA_NOT_MET",
        "human_review_required": True,
    }


if __name__ == "__main__":
    from backend.extraction.doc_intelligence import fetch_blob, analyze, table_rows
    from backend.extraction.schema import normalise

    for path in ["loan/customer_1001_home_loan_application.pdf",
                 "loan/customer_1004_home_loan_application.pdf",
                 "loan/customer_1005_personal_loan_application.pdf"]:
        app = normalise(table_rows(analyze(fetch_blob(path))), source_file=path)
        s = summary(app)
        print(f"\n{'=' * 74}")
        print(f"{s['customer_id']}  {app.customer_name}  |  {s['loan_type']}")
        print("=" * 74)
        for c in s["criteria"]:
            mark = "PASS" if c["passed"] else "FAIL"
            print(f"  [{mark}] {c['name']:26} required {c['required']:28} actual {c['actual']}")
            if not c["passed"]:
                print(f"         -> {c['policy_ref']}, {c['section']}")
        print(f"\n  {s['overall']}  ({s['passed_count']}/{s['total_count']})")
        print(f"  human_review_required: {s['human_review_required']}")




