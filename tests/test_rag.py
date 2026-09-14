"""RAG accuracy and hallucination resistance. Spec Section 34: 10 + 5 tests."""
import pytest
from tests.conftest import REFUSAL

RAG_CASES = [
    ("What is the minimum employment requirement for a home loan?",
     ["3 years"], "home_loan_policy.pdf"),
    ("What documents are required for a home loan?",
     ["identity", "address", "income", "bank statement", "employment", "property"],
     "home_loan_policy.pdf"),
    ("What is the maximum home loan amount?",
     ["10,00,00,000"], "home_loan_policy.pdf"),
    ("How often must KYC be updated for a low risk customer?",
     ["10 years"], "kyc_policy.pdf"),
    ("What is the minimum age for a home loan applicant?",
     ["21"], "home_loan_policy.pdf"),
    ("What is the complaint escalation process?",
     ["branch", "nodal", "ombudsman"], "complaint_policy.pdf"),
    ("When must a suspicious transaction report be submitted?",
     ["7 working days"], "aml_policy.pdf"),
    ("What is the minimum balance for a salary account?",
     ["no minimum"], "account_opening_policy.pdf"),
    ("What is the minimum credit bureau score for a personal loan?",
     ["720"], "personal_loan_policy.pdf"),
    ("Who has authority to sanction a home loan above 3 crore?",
     ["credit committee"], "home_loan_policy.pdf"),
]

HALLUCINATION_CASES = [
    "What is the bank's policy on cryptocurrency custody?",
    "What is the minimum employment requirement for an education loan?",
    "What is the bank's policy on gold loans?",
    "What is the penalty for early closure of a fixed deposit?",
    "What are the annual charges for a safe deposit locker?",
]


@pytest.mark.parametrize("question,expected,source", RAG_CASES)
def test_rag_accuracy(ask, question, expected, source):
    r = ask(question)
    text = r["answer"].lower()
    assert r["grounded"], f"refused a question the corpus covers: {question}"
    missing = [e for e in expected if e.lower() not in text]
    assert not missing, f"missing {missing} in: {r['answer'][:200]}"
    assert any(s["file"] == source for s in r["sources"]), \
        f"expected {source} among sources"


@pytest.mark.parametrize("question", HALLUCINATION_CASES)
def test_refuses_when_uncovered(ask, question):
    r = ask(question)
    assert REFUSAL in r["answer"], \
        f"fabricated an answer for: {question}\n{r['answer'][:300]}"
    assert not r["grounded"]

