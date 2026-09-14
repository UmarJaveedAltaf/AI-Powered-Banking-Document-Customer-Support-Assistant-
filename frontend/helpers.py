"""Cached wrappers so Streamlit reruns don't re-hit Azure on every interaction."""
import streamlit as st


@st.cache_data(ttl=600, show_spinner=False)
def ask_policy(question: str, mode: str, top: int):
    from backend.rag.pipeline import answer
    return answer(question, mode=mode, top=top)


@st.cache_data(ttl=600, show_spinner=False)
def search_policies(question: str, mode: str, top: int):
    from backend.search.retrieval import retrieve
    return retrieve(question, mode=mode, top=top)


@st.cache_data(ttl=600, show_spinner=False)
def process_document(blob_path: str):
    from backend.extraction.pipeline import process
    return process(blob_path)


@st.cache_data(ttl=600, show_spinner=False)
def assess_customer(blob_path: str):
    from backend.validation.assessment import assess
    return assess(blob_path)


@st.cache_data(ttl=600, show_spinner=False)
def run_ocr(blob_path: str):
    from backend.extraction.ocr import process_scanned
    return process_scanned(blob_path)


@st.cache_data(ttl=600, show_spinner=False)
def analyse_messages():
    from backend.ai_services.sentiment import analyse, load_messages
    return analyse(load_messages())


@st.cache_data(ttl=60, show_spinner=False)
def list_blobs(prefix: str):
    from azure.storage.blob import BlobServiceClient
    from config.settings import get_settings, credential
    s = get_settings()
    cc = BlobServiceClient(s.blob_endpoint, credential()).get_container_client("raw-documents")
    return sorted(b.name for b in cc.list_blobs(name_starts_with=prefix) if b.size > 0)


def mask_display(fields: dict):
    from backend.ai_services.masking import mask_fields
    return mask_fields(fields)


PRIORITY_COLOUR = {"HIGH": "#d13438", "MEDIUM": "#c19c00", "LOW": "#107c10"}
