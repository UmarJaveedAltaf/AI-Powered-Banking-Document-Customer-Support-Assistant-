"""End-to-end assessment: extract -> validate -> retrieve -> explain -> cross-check."""
from backend.extraction.doc_intelligence import fetch_blob, analyze, table_rows
from backend.extraction.schema import normalise
from backend.validation.rules import validate, summary
from backend.rag.pipeline import answer_structured

VERDICT = {True: "MEETS_REQUIREMENT", False: "DOES_NOT_MEET_REQUIREMENT"}


def assess(blob_path: str, criterion_name: str = "Total employment history") -> dict:
    app = normalise(table_rows(analyze(fetch_blob(blob_path))), source_file=blob_path)
    crit = next(c for c in validate(app) if c.name == criterion_name)

    question = (f"Does a customer with {crit.actual} of {criterion_name.lower()} "
                f"satisfy the {app.loan_type.lower()} requirement?")
    llm = answer_structured(
        question,
        extra_context=f"[applicant record: {criterion_name} = {crit.actual}]")

    rule_verdict = VERDICT[crit.passed]
    agree = llm["decision"] == rule_verdict

    return {
        "customer": app.customer_id,
        "customer_name": app.customer_name,
        "requirement": crit.name,
        "customer_value": crit.actual,
        "policy_requirement": crit.required,
        "status": rule_verdict,
        "reason": llm["reason"],
        "source": crit.policy_ref,
        "section": crit.section,
        "rule_engine_verdict": rule_verdict,
        "llm_verdict": llm["decision"],
        "verdicts_agree": agree,
        "confidence": "HIGH" if agree else "LOW",
        "human_review_required": True,
        "_all_criteria": summary(app),
    }


if __name__ == "__main__":
    import json

    result = assess("loan/customer_1001_home_loan_application.pdf")
    public = {k: v for k, v in result.items() if not k.startswith("_")}
    print("\n" + json.dumps(public, indent=2))

    s = result["_all_criteria"]
    print(f"\nFull assessment: {s['passed_count']}/{s['total_count']} criteria met")
    for name in s["failed_criteria"]:
        print(f"  FAILED: {name}")

    if not result["verdicts_agree"]:
        print("\n  WARNING: rule engine and model disagree. Flagged for review.")
