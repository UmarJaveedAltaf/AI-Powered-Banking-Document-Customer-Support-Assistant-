"""Generate representative traffic, then print the Section 22 dashboard."""
from backend.common.telemetry import init, dashboard, events
from backend.extraction.pipeline import process
from backend.rag.pipeline import answer

QUESTIONS = [
    "What documents are required for a home loan?",
    "How often must KYC be updated?",
    "What is the complaint escalation process?",
    "What is the bank's cryptocurrency policy?",          # expected refusal
    "What is the minimum employment requirement?",
]

DOCUMENTS = [
    "loan/customer_1001_home_loan_application.pdf",
    "loan/customer_1002_home_loan_application.pdf",
    "loan/customer_1003_personal_loan_application.pdf",
]


if __name__ == "__main__":
    print("Telemetry to App Insights:", "enabled" if init() else "local only")

    print(f"\nProcessing {len(DOCUMENTS)} documents ...")
    for d in DOCUMENTS:
        r = process(d)
        print(f"  {r['customer_id']}  {r['processing']['duration_seconds']}s")

    print(f"\nRunning {len(QUESTIONS)} AI queries ...")
    for q in QUESTIONS:
        r = answer(q)
        print(f"  grounded={str(r['grounded']):5}  {r['usage']['total_tokens']:>5} tokens  {q[:48]}")

    d = dashboard()
    print("\n" + "-" * 47)
    print("        AI APPLICATION MONITORING")
    print("-" * 47)
    print(f"  Documents processed        {d['documents_processed']:>10}")
    print(f"  Successful                 {d['documents_successful']:>10}")
    print(f"  Failed                     {d['documents_failed']:>10}")
    print(f"  Avg processing time        {d['avg_document_processing_ms'] / 1000:>9.2f}s")
    print(f"  AI requests                {d['ai_requests']:>10}")
    print(f"  AI failures                {d['ai_failures']:>10}")
    print(f"  Avg AI response time       {d['avg_ai_response_ms'] / 1000:>9.2f}s")
    print(f"  Prompt tokens              {d['prompt_tokens']:>10,}")
    print(f"  Completion tokens          {d['completion_tokens']:>10,}")
    print(f"  Total tokens               {d['total_tokens']:>10,}")
    print(f"  Ungrounded answers         {d['ungrounded_answers']:>10}")
    print(f"  Grounding rate             {d['grounding_rate_pct']:>9.1f}%")
    print("-" * 47)
    print(f"\n{len(events())} events emitted.")
