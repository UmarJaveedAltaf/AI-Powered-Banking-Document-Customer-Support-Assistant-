"""Retrieval in three modes, plus a comparison harness for the Section 7 deliverable."""
from azure.search.documents.models import VectorizedQuery
from config.settings import get_settings
from backend.search.indexer import embed, search_client

SELECT = ["id", "content", "title", "section", "source_file", "page"]


def retrieve(question: str, mode: str = "hybrid", top: int = 5, filters: str | None = None):
    s = get_settings()
    kwargs = {"top": top, "filter": filters, "select": SELECT}

    if mode in ("keyword", "hybrid"):
        kwargs["search_text"] = question
    else:
        kwargs["search_text"] = None

    if mode in ("vector", "hybrid"):
        kwargs["vector_queries"] = [VectorizedQuery(
            vector=embed([question])[0],
            k_nearest_neighbors=top * 4,
            fields="contentVector")]

    if mode == "hybrid":
        kwargs["query_type"] = "semantic"
        kwargs["semantic_configuration_name"] = "semantic-config"

    return [dict(r) for r in search_client().search(**kwargs)]


def top_hit(question: str, mode: str) -> str:
    hits = retrieve(question, mode=mode, top=1)
    if not hits:
        return "no results"
    h = hits[0]
    return f"{h['source_file'].replace('_policy.pdf','')} / {h['section']}"


# question -> expected (source_file, section keyword)
TEST_QUESTIONS = [
    ("What is the minimum employment requirement for a home loan?",
     "home_loan_policy.pdf", "Employment Eligibility"),
    ("How long must someone have worked before getting a house loan?",
     "home_loan_policy.pdf", "Employment Eligibility"),
    ("What documents are required for a home loan?",
     "home_loan_policy.pdf", "Required Documents"),
    ("What is FOIR?", "home_loan_policy.pdf", "Income Criteria"),
    ("How often must KYC be updated?", "kyc_policy.pdf", "KYC Update Frequency"),
    ("Can a fresher get a home loan?", "home_loan_policy.pdf", "Employment Eligibility"),
    ("What is the complaint escalation process?",
     "complaint_policy.pdf", "Complaint Escalation Process"),
    ("When must a suspicious transaction be reported?",
     "aml_policy.pdf", "Reporting Timelines"),
    ("What is the minimum balance for a salary account?",
     "account_opening_policy.pdf", "Minimum Balance"),
    ("Who approves a home loan?", "home_loan_policy.pdf", "Sanction Authority"),
]


def compare(top: int = 5):
    modes = ["keyword", "vector", "hybrid"]
    scores = {m: {"hit1": 0, "hitk": 0, "mrr": 0.0} for m in modes}

    for question, want_file, want_section in TEST_QUESTIONS:
        print(f"\n{question}")
        print(f"  expect: {want_file} / ...{want_section}...")
        for m in modes:
            hits = retrieve(question, mode=m, top=top)
            rank = next((i + 1 for i, h in enumerate(hits)
                         if h["source_file"] == want_file and want_section in h["section"]), None)
            if rank == 1:
                scores[m]["hit1"] += 1
            if rank:
                scores[m]["hitk"] += 1
                scores[m]["mrr"] += 1 / rank
            got = f"{hits[0]['source_file'].replace('_policy.pdf','')} / {hits[0]['section']}" if hits else "-"
            mark = "OK  " if rank == 1 else (f"@{rank} " if rank else "MISS")
            print(f"    {m:8} {mark} {got}")

    n = len(TEST_QUESTIONS)
    print(f"\n{'=' * 58}")
    print(f"{'mode':10} {'top-1':>8} {'recall@' + str(top):>10} {'MRR':>8}")
    print("-" * 58)
    for m in modes:
        s = scores[m]
        print(f"{m:10} {s['hit1']}/{n:<6} {s['hitk']}/{n:<8} {s['mrr'] / n:>8.3f}")
    print("=" * 58)


if __name__ == "__main__":
    compare()
