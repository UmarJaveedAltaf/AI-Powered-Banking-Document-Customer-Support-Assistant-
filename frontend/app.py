"""Bank AI Assistant - Streamlit front end."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from frontend.helpers import (ask_policy, search_policies, process_document,
                              assess_customer, run_ocr, analyse_messages,
                              list_blobs, mask_display, PRIORITY_COLOUR,
                              live_stats, handle_upload, synthesise)

st.set_page_config(page_title="Meridian Bank AI Assistant", page_icon="MB",
                   layout="wide", initial_sidebar_state="collapsed")

st.markdown("""<style>
#MainMenu, footer {visibility: hidden;}
section[data-testid="stSidebar"] {display: none;}
.block-container {padding-top: 4.2rem; padding-bottom: 3rem; max-width: 1360px;}
header[data-testid="stHeader"] {background: rgba(14,17,23,0.92); backdrop-filter: blur(6px);}
div[data-testid="stToolbar"] {right: 1rem;}
.hero {background: linear-gradient(135deg, #102540 0%, #0d1520 100%);
       border: 1px solid #1e3a5f; border-radius: 14px;
       padding: 42px 46px; margin: 6px 0 22px 0;}
.hero h1 {font-size: 2.45rem; margin: 0 0 12px 0; color: #fff; letter-spacing: -0.6px;}
.hero p {font-size: 1.02rem; color: #9fb3c8; margin: 0; max-width: 760px; line-height: 1.65;}
.brand {font-size: 1.1rem; font-weight: 700; letter-spacing: 1.2px;
        color: #fff; padding-top: 4px; line-height: 1.2;}
.brand span {color: #4da3ff;}
.brand small {display: block; font-size: 0.68rem; font-weight: 400;
              letter-spacing: 0.4px; color: #7d8fa3; margin-top: 2px;}
.navrule {border-bottom: 1px solid #1f2733; margin: 6px 0 20px 0;}
.card-title {font-size: 1.02rem; font-weight: 600; color: #e6edf3; margin-bottom: 6px;}
.card-desc {font-size: 0.84rem; color: #8b9cb0; line-height: 1.5; min-height: 58px;}
.pill {display: inline-block; padding: 2px 10px; border-radius: 20px;
       font-size: 0.7rem; background: #132b1e; color: #4ade80; border: 1px solid #1e4030;}
.pagehead {font-size: 1.9rem; font-weight: 700; color: #fff; margin: 0 0 4px 0;}
.pagesub {color: #8b9cb0; font-size: 0.92rem; margin-bottom: 20px;}
</style>""", unsafe_allow_html=True)

PAGES = ["Home", "Dashboard", "Upload", "Analysis", "Policy AI",
         "Sentiment", "Voice", "Search", "Monitoring"]

CARDS = [
    ("Dashboard", "Corpus size, indexed chunks and retrieval benchmarks."),
    ("Upload", "Drop a PDF. Extract fields, validate against policy, store JSON."),
    ("Analysis", "Assess an application. Rule engine verdict plus a cited explanation."),
    ("Policy AI", "Ask a policy question. Grounded answers with source citations."),
    ("Sentiment", "Triage customer messages by Complaint Policy severity."),
    ("Voice", "Speak a question, hear a grounded answer."),
    ("Search", "Compare keyword, vector and hybrid retrieval. Run OCR."),
    ("Monitoring", "Telemetry, latency, token spend and grounding rate."),
]

if "page" not in st.session_state:
    st.session_state.page = "Home"


def goto(page):
    st.session_state.page = page


brand_col, nav_col = st.columns([2.3, 9])
with brand_col:
    st.markdown("<div class='brand'>MERIDIAN <span>AI</span>"
                "<small>NATIONAL BANK</small></div>", unsafe_allow_html=True)
with nav_col:
    cols = st.columns(len(PAGES))
    for col, page in zip(cols, PAGES):
        col.button(page, key=f"nav_{page}", on_click=goto, args=(page,),
                   use_container_width=True,
                   type="primary" if st.session_state.page == page else "secondary")

st.markdown("<div class='navrule'></div>", unsafe_allow_html=True)
screen = st.session_state.page


def page_header(title, subtitle):
    st.markdown(f"<div class='pagehead'>{title}</div>"
                f"<div class='pagesub'>{subtitle}</div>", unsafe_allow_html=True)


def sources_panel(sources):
    with st.expander(f"Sources ({len(sources)} chunks retrieved)"):
        for s in sources:
            st.markdown(f"**{s['file']}** - {s['section']} "
                        f"(page {s['page']}, score {s['score']})")


# ---------------------------------------------------------------------- HOME
if screen == "Home":
    st.markdown("""<div class='hero'>
      <h1>Banking Document &amp; Customer Support Assistant</h1>
      <p>Processes customer documents, answers policy questions from approved
      sources, and triages customer messages. Every verdict comes from a
      deterministic rule engine; the model supplies the explanation and the
      citation, and no decision is made without human review.</p>
    </div>""", unsafe_allow_html=True)

    stats = live_stats()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Policy documents", stats["policies"])
    m2.metric("Indexed chunks", stats["indexed_chunks"])
    m3.metric("Customer applications", stats["applications"])
    m4.metric("Scanned documents", stats["scanned"])

    st.write("")
    for row in range(0, len(CARDS), 4):
        cols = st.columns(4)
        for col, (page, desc) in zip(cols, CARDS[row:row + 4]):
            with col:
                with st.container(border=True):
                    st.markdown(f"<div class='card-title'>{page}</div>"
                                f"<div class='card-desc'>{desc}</div>",
                                unsafe_allow_html=True)
                    st.button("Open", key=f"card_{page}", on_click=goto,
                              args=(page,), use_container_width=True)

    st.write("")
    st.markdown("<span class='pill'>Azure OpenAI</span> "
                "<span class='pill'>AI Search</span> "
                "<span class='pill'>Document Intelligence</span> "
                "<span class='pill'>AI Language</span> "
                "<span class='pill'>Speech</span> "
                "<span class='pill'>ADLS Gen2</span> "
                "<span class='pill'>Key Vault</span> "
                "<span class='pill'>Managed Identity</span> "
                "<span class='pill'>Application Insights</span>",
                unsafe_allow_html=True)


# ----------------------------------------------------------------- DASHBOARD
elif screen == "Dashboard":
    page_header("Dashboard", "Corpus, index and retrieval benchmarks.")

    stats = live_stats()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Policy documents", stats["policies"], f"{stats['indexed_chunks']} chunks")
    c2.metric("Customer applications", stats["applications"], "extracted and validated")
    c3.metric("Scanned documents", stats["scanned"], "OCR required")
    c4.metric("Total in ADLS", stats["total_blobs"], "raw-documents")

    if stats["indexed_chunks"] == 0:
        st.warning("The search index is empty. Run infra/search-up.ps1, then "
                   "index_schema and indexer.")

    st.divider()
    left, right = st.columns([1.1, 1])
    with left:
        st.subheader("Pipeline")
        st.code("""Upload -> Blob / ADLS Gen2
      -> Document Intelligence
      -> typed schema
      -> rule engine  ->  verdict
                          |
Policy PDFs -> chunks -> embeddings -> AI Search
                          |
                     Azure OpenAI -> explanation + citation""", language=None)
    with right:
        st.subheader("Design principles")
        st.markdown("""
- The rule engine decides. The model explains and cites.
- Both verdicts are cross-checked; disagreement lowers confidence.
- `human_review_required` is enforced in code, never by prompt.
- The structured output schema has no approval value.
- No keys in code. Entra ID managed identity throughout.
- PII masked at the presentation boundary, before the model sees it.
""")

    st.divider()
    st.subheader("Retrieval mode comparison")
    st.caption("Ten questions with known ground truth. Full results in "
               "docs/retrieval-comparison.txt")
    st.table({"mode": ["keyword", "vector", "hybrid"],
              "top-1": ["7/10", "8/10", "8/10"],
              "recall@5": ["10/10", "8/10", "10/10"],
              "MRR": [0.817, 0.800, 0.870]})


# -------------------------------------------------------------------- UPLOAD
elif screen == "Upload":
    page_header("Document Upload",
                "Upload -> Blob Storage -> Document Intelligence -> validate -> JSON")

    tab_new, tab_existing = st.tabs(["Upload a file", "Process an existing document"])
    result = None

    with tab_new:
        uploaded = st.file_uploader("Drop a PDF here", type=["pdf"])
        kind = st.selectbox("Document type",
                            ["loan_application", "bank_statement", "identity", "policy"],
                            format_func=lambda k: k.replace("_", " ").title())
        if uploaded is not None:
            st.caption(f"{uploaded.name} - {uploaded.size:,} bytes")
            if st.button("Upload and process", type="primary", key="btn_upload"):
                with st.spinner("Uploading, extracting, validating..."):
                    try:
                        result = handle_upload(uploaded.getvalue(), uploaded.name, kind)
                        st.session_state["last_upload"] = result
                        live_stats.clear()
                    except Exception as e:
                        st.error(f"Processing failed: {type(e).__name__}: {e}")

    with tab_existing:
        docs = list_blobs("loan/")
        chosen = st.selectbox("Customer application", docs,
                              format_func=lambda p: p.split("/")[-1])
        if st.button("Process document", type="primary", key="btn_existing"):
            with st.spinner("Extracting and validating..."):
                result = process_document(chosen)
                st.session_state["last_upload"] = result

    result = result or st.session_state.get("last_upload")

    if result:
        pr, ex, v = result["processing"], result["extraction"], result["validation"]
        st.divider()
        st.success(f"Processed in {pr['duration_seconds']}s -> {pr['source_blob']}")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Customer", ex["customer_id"])
        c2.metric("Fields", f"{pr['fields_found']}/{pr['fields_expected']}")
        c3.metric("Criteria met", f"{v['passed_count']}/{v['total_count']}")
        c4.metric("Model", pr["model_id"].replace("prebuilt-", ""))

        if pr["ocr_required"]:
            st.info("No text layer detected. Routed to OCR via prebuilt-read.")

        st.subheader("Extracted fields (masked)")
        st.json(mask_display({k: val for k, val in ex.items()
                              if k not in ("documents_submitted", "source_file",
                                           "fields_expected", "fields_found")}))

        st.subheader("Policy validation")
        for c in v["criteria"]:
            colour = "#4ade80" if c["passed"] else "#f87171"
            icon = "PASS" if c["passed"] else "FAIL"
            st.markdown(
                f"<span style='color:{colour};font-weight:600'>{icon}</span> "
                f"**{c['name']}** - required {c['required']}, actual {c['actual']}"
                + ("" if c["passed"] else
                   f"<br><small style='color:#8b9cb0'>{c['policy_ref']}, {c['section']}</small>"),
                unsafe_allow_html=True)

        if v["failed_criteria"]:
            st.warning(f"Not met: {', '.join(v['failed_criteria'])}. "
                       "Referred to a credit officer.")

        st.subheader("Stored JSON")
        st.code(pr["output_blob"])


# ------------------------------------------------------------------ ANALYSIS
elif screen == "Analysis":
    page_header("Document Analysis",
                "Rule engine verdict, cross-checked against a cited model explanation.")

    docs = list_blobs("loan/")
    chosen = st.selectbox("Customer application", docs,
                          format_func=lambda p: p.split("/")[-1])

    if st.button("Assess against policy", type="primary"):
        with st.spinner("Extracting, validating, retrieving, explaining..."):
            st.session_state["assessment"] = assess_customer(chosen)

    r = st.session_state.get("assessment")
    if r:
        met = r["status"] == "MEETS_REQUIREMENT"
        (st.success if met else st.error)(
            f"{r['customer']} - {r['requirement']}: "
            f"{r['status'].replace('_', ' ').lower()}")

        c1, c2, c3 = st.columns(3)
        c1.metric("Customer value", r["customer_value"])
        c2.metric("Policy requires", r["policy_requirement"])
        c3.metric("Confidence", r["confidence"])

        st.subheader("Explanation")
        st.info(r["reason"])
        st.caption(f"Source: {r['source']}, {r['section']}")

        st.subheader("Verdict cross-check")
        a, b = st.columns(2)
        a.metric("Rule engine", r["rule_engine_verdict"].replace("_", " "))
        b.metric("Model", r["llm_verdict"].replace("_", " "))
        if r["verdicts_agree"]:
            st.success("Verdicts agree. Confidence raised.")
        else:
            st.warning("Verdicts disagree. Flagged for manual review.")

        st.error("human_review_required: true - no automated approval or rejection.")

        with st.expander("All criteria"):
            for c in r["_all_criteria"]["criteria"]:
                st.markdown(("PASS " if c["passed"] else "FAIL ") +
                            f"**{c['name']}** - {c['actual']} vs {c['required']}")


# ------------------------------------------------------------------ POLICY AI
elif screen == "Policy AI":
    page_header("Policy Assistant",
                "Answers grounded in approved policy documents, with citations.")

    SAMPLES = [
        "What documents are required for a home loan?",
        "What is the minimum employment requirement?",
        "How often must KYC be updated?",
        "What is the complaint escalation process?",
        "When must a suspicious transaction be reported?",
        "What is the bank's cryptocurrency policy?",
    ]
    picked = st.selectbox("Example questions", ["(type your own)"] + SAMPLES)
    question = st.text_input("Question",
                             value="" if picked.startswith("(") else picked)

    c1, c2 = st.columns([3, 1])
    mode = c1.radio("Retrieval mode", ["hybrid", "vector", "keyword"], horizontal=True)
    top = c2.slider("Chunks", 3, 10, 5)

    if st.button("Ask", type="primary") and question:
        with st.spinner("Retrieving and generating..."):
            st.session_state["policy_answer"] = ask_policy(question, mode, top)

    r = st.session_state.get("policy_answer")
    if r:
        if r["grounded"]:
            st.markdown(r["answer"])
        else:
            st.warning(r["answer"])
            st.caption("Refusal is correct when the corpus does not cover the question.")

        m1, m2, m3 = st.columns(3)
        m1.metric("Grounded", "yes" if r["grounded"] else "no")
        m2.metric("Chunks used", len(r["sources"]))
        m3.metric("Tokens", r["usage"].get("total_tokens", 0))
        sources_panel(r["sources"])


# ------------------------------------------------------------------ SENTIMENT
elif screen == "Sentiment":
    page_header("Customer Sentiment",
                "Triage grounded in Customer Complaint Policy, Section 4.")

    if st.button("Analyse all messages", type="primary"):
        with st.spinner("Analysing..."):
            st.session_state["sentiment"] = analyse_messages()

    rows = st.session_state.get("sentiment")
    if rows:
        order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        rows = sorted(rows, key=lambda r: (order[r["priority"]], -r["negative"]))
        counts = {p: sum(1 for r in rows if r["priority"] == p)
                  for p in ("HIGH", "MEDIUM", "LOW")}

        c1, c2, c3 = st.columns(3)
        c1.metric("High priority", counts["HIGH"], "1 day SLA")
        c2.metric("Medium", counts["MEDIUM"], "3 day SLA")
        c3.metric("Low", counts["LOW"], "5 day SLA")
        st.divider()

        for r in rows:
            with st.container(border=True):
                st.markdown(
                    f"<span style='color:{PRIORITY_COLOUR[r['priority']]};"
                    f"font-weight:700'>{r['priority']}</span> &nbsp; "
                    f"**{r['customer_id']}** &nbsp; "
                    f"<small style='color:#8b9cb0'>{r['category']} · {r['sentiment']} "
                    f"({r['negative']:.2f} neg) · {r['sla_days']}d</small>",
                    unsafe_allow_html=True)
                st.write(r["message"])
                st.caption(r["priority_reason"])


# ---------------------------------------------------------------------- VOICE
elif screen == "Voice":
    page_header("Voice Assistant", "Speech to text, grounded RAG, speech out.")

    st.info("Browser microphone capture is unavailable in Streamlit. Type a "
            "question, or tick the box below if running locally with a microphone.")

    question = st.text_input("Question",
                             value="What documents are required for a personal loan?")
    use_mic = st.checkbox("Capture from the local microphone instead")

    if st.button("Ask", type="primary"):
        from backend.ai_services.voice_assistant import ask_by_voice
        with st.spinner("Listening..." if use_mic else "Retrieving and generating..."):
            r = ask_by_voice(question=None if use_mic else question, speak_reply=False)
        if not r["ok"]:
            st.error(r["error"])
        else:
            st.session_state["voice"] = r

    r = st.session_state.get("voice")
    if r:
        st.success(f"Heard: {r['question']}")
        with st.spinner("Synthesising..."):
            audio = synthesise(r["spoken"])
        if audio:
            st.audio(audio, format="audio/wav")
            st.caption(f"{len(r['spoken'])} characters spoken. Citation stripped "
                       "and text capped for listenability.")
        st.subheader("Full answer")
        st.markdown(r["answer"])
        sources_panel(r["sources"])


# --------------------------------------------------------------------- SEARCH
elif screen == "Search":
    page_header("Search Documents",
                "Compare keyword, vector and hybrid retrieval. Run OCR on scanned files.")

    query = st.text_input("Search query",
                          value="How long must someone have worked before getting a house loan?")
    top = st.slider("Results per mode", 1, 10, 3)

    if st.button("Search all three modes", type="primary") and query:
        st.session_state["search"] = {m: search_policies(query, m, top)
                                      for m in ("keyword", "vector", "hybrid")}

    res = st.session_state.get("search")
    if res:
        cols = st.columns(3)
        for col, mode in zip(cols, ["keyword", "vector", "hybrid"]):
            with col:
                st.subheader(mode)
                for i, h in enumerate(res[mode], 1):
                    with st.container(border=True):
                        st.markdown(f"**{i}. {h['source_file'].replace('_policy.pdf', '')}**")
                        st.caption(f"{h['section']} · {h.get('@search.score', 0):.4f}")
                        st.text(h["content"][:170].replace("\n", " ") + "...")

    st.divider()
    st.subheader("OCR: image-only documents")
    scanned = list_blobs("statements/")
    doc = st.selectbox("Scanned document", scanned,
                       format_func=lambda p: p.split("/")[-1])

    if st.button("Run OCR"):
        with st.spinner("Reading pixels..."):
            st.session_state["ocr"] = run_ocr(doc)

    o = st.session_state.get("ocr")
    if o:
        c1, c2 = st.columns(2)
        c1.metric("Text layer", "none" if o["ocr_required"] else "present")
        c2.metric("Characters recovered", f"{o['characters_recovered']:,}")
        a, b = st.columns(2)
        a.subheader("Extracted")
        a.json(o["fields"])
        b.subheader("Masked for display")
        b.json(mask_display(o["fields"]))
        with st.expander("Raw OCR text"):
            st.text(o["raw_text"])


# ----------------------------------------------------------------- MONITORING
elif screen == "Monitoring":
    page_header("Monitoring",
                "Telemetry from this session. Full history in Application Insights.")

    from backend.common.telemetry import dashboard, events
    d = dashboard()

    st.subheader("Documents")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Processed", d["documents_processed"])
    c2.metric("Successful", d["documents_successful"])
    c3.metric("Failed", d["documents_failed"])
    c4.metric("Avg time", f"{d['avg_document_processing_ms'] / 1000:.2f}s")

    st.subheader("AI requests")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Requests", d["ai_requests"])
    c2.metric("Failures", d["ai_failures"])
    c3.metric("Avg response", f"{d['avg_ai_response_ms'] / 1000:.2f}s")
    c4.metric("Total tokens", f"{d['total_tokens']:,}")

    st.subheader("Grounding")
    c1, c2 = st.columns(2)
    c1.metric("Grounding rate", f"{d['grounding_rate_pct']:.1f}%")
    c2.metric("Refusals", d["ungrounded_answers"])
    st.caption("A refusal is the guardrail firing, not an error.")

    if d["ai_requests"] == 0 and d["documents_processed"] == 0:
        st.info("No activity yet this session. Use the other screens, then return here.")

    with st.expander("Event log"):
        for e in events()[-25:]:
            st.text(f"{e['event']:20} {e.get('status', ''):10} "
                    f"{e.get('duration_ms', 0):>8.0f}ms")


