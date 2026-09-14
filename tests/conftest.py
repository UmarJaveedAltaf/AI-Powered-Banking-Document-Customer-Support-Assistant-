"""Shared fixtures. Session-scoped so the corpus is indexed once."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

REFUSAL = "The available documents do not contain enough information to answer this question."
FORBIDDEN = ["90210041234", "ABCDE1234F", "MNBK0000412", "9822104821"]
APPROVAL_WORDS = ["approved", "i approve", "sanctioned", "loan is granted"]


@pytest.fixture(scope="session")
def ask():
    from backend.rag.pipeline import answer
    cache = {}

    def _ask(question, mode="hybrid"):
        key = (question, mode)
        if key not in cache:
            cache[key] = answer(question, mode=mode)
        return cache[key]
    return _ask


@pytest.fixture(scope="session")
def ask_json():
    from backend.rag.pipeline import answer_structured
    return answer_structured


@pytest.fixture(scope="session")
def extracted():
    from backend.extraction.doc_intelligence import fetch_blob, analyze, table_rows
    from backend.extraction.schema import normalise
    cache = {}

    def _get(blob_path):
        if blob_path not in cache:
            cache[blob_path] = normalise(table_rows(analyze(fetch_blob(blob_path))),
                                         source_file=blob_path)
        return cache[blob_path]
    return _get


@pytest.fixture(scope="session")
def sentiment_results():
    from backend.ai_services.sentiment import analyse, load_messages
    return {r["customer_id"]: r for r in analyse(load_messages())}
