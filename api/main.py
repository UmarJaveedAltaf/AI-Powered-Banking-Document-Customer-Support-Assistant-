"""FastAPI layer over the existing backend.

Every endpoint returns the exact shape the web frontend expects. The backend
modules are imported unchanged; nothing here reimplements logic.

Run:  uvicorn api.main:app --reload --port 8000
Docs: http://localhost:8000/docs
"""
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from azure.storage.blob import BlobServiceClient
from config.settings import get_settings, credential

app = FastAPI(
    title="Horizon National Bank - AI Assistant API",
    description="Document processing, grounded policy retrieval, sentiment triage "
                "and speech, over Azure AI services. The rule engine decides; the "
                "model explains and cites.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

AUDIO_DIR = Path("data/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


class AskRequest(BaseModel):
    question: str
    mode: str = "hybrid"
    top: int = 5


class BlobRequest(BaseModel):
    blob: str


class VoiceRequest(BaseModel):
    question: str
    speak: bool = True


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "service": "horizon-bank-ai"}


@app.get("/stats", tags=["system"])
def stats():
    from backend.ingestion.runtime_upload import corpus_stats
    return corpus_stats()


@app.get("/monitoring", tags=["system"])
def monitoring():
    from backend.common.telemetry import dashboard
    return dashboard()


@app.get("/documents", tags=["documents"])
def list_documents(prefix: str = "loan/"):
    s = get_settings()
    cc = BlobServiceClient(s.blob_endpoint, credential()).get_container_client("raw-documents")
    return {"blobs": sorted(b.name for b in cc.list_blobs(name_starts_with=prefix) if b.size > 0)}


def _mask_extraction(payload: dict) -> dict:
    from backend.ai_services.masking import mask_fields
    ex = payload["extraction"]
    keep = {k: v for k, v in ex.items()
            if k not in ("documents_submitted", "source_file",
                         "fields_expected", "fields_found")}
    payload["extraction"] = mask_fields(keep)
    return payload


@app.post("/documents/process", tags=["documents"])
async def process_document(file: UploadFile | None = File(None),
                           blob: str | None = Form(None),
                           kind: str = Form("loan_application")):
    try:
        if file is not None:
            from backend.ingestion.runtime_upload import upload_and_process
            data = await file.read()
            result = upload_and_process(data, file.filename, kind)
        elif blob:
            from backend.extraction.pipeline import process
            result = process(blob)
        else:
            raise HTTPException(400, "Supply either a file or a blob path.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"{type(e).__name__}: {e}")
    return _mask_extraction(result)


@app.post("/documents/assess", tags=["documents"])
def assess_document(req: BlobRequest):
    from backend.validation.assessment import assess
    try:
        r = assess(req.blob)
    except Exception as e:
        raise HTTPException(500, f"{type(e).__name__}: {e}")
    out = {k: v for k, v in r.items() if not k.startswith("_")}
    out["all_criteria"] = r.get("_all_criteria", {})
    return out


@app.post("/ocr", tags=["documents"])
def run_ocr(req: BlobRequest):
    from backend.extraction.ocr import process_scanned
    from backend.ai_services.masking import mask_fields
    try:
        r = process_scanned(req.blob)
    except Exception as e:
        raise HTTPException(500, f"{type(e).__name__}: {e}")
    r["fields_masked"] = mask_fields(r["fields"])
    return r


@app.post("/policy/ask", tags=["policy"])
def policy_ask(req: AskRequest):
    from backend.rag.pipeline import answer
    try:
        return answer(req.question, mode=req.mode, top=req.top)
    except Exception as e:
        raise HTTPException(500, f"{type(e).__name__}: {e}")


@app.post("/policy/ask-structured", tags=["policy"])
def policy_ask_structured(req: AskRequest):
    from backend.rag.pipeline import answer_structured
    try:
        return answer_structured(req.question, mode=req.mode, top=req.top)
    except Exception as e:
        raise HTTPException(500, f"{type(e).__name__}: {e}")


@app.get("/search", tags=["policy"])
def search(q: str, top: int = 3):
    from backend.search.retrieval import retrieve
    out = {}
    for mode in ("keyword", "vector", "hybrid"):
        try:
            out[mode] = [{
                "source_file": h["source_file"],
                "section": h["section"],
                "page": h.get("page"),
                "score": round(h.get("@search.score", 0), 4),
                "content": h["content"],
            } for h in retrieve(q, mode=mode, top=top)]
        except Exception as e:
            out[mode] = {"error": f"{type(e).__name__}: {e}"}
    return out


@app.get("/sentiment/analyse", tags=["sentiment"])
def sentiment_analyse():
    from backend.ai_services.sentiment import analyse, load_messages
    try:
        rows = analyse(load_messages())
    except Exception as e:
        raise HTTPException(500, f"{type(e).__name__}: {e}")
    order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    return sorted(rows, key=lambda r: (order.get(r["priority"], 3), -r["negative"]))


@app.post("/voice/ask", tags=["voice"])
def voice_ask(req: VoiceRequest):
    from backend.ai_services.voice_assistant import ask_by_voice
    from backend.ai_services.speech import speak
    try:
        r = ask_by_voice(question=req.question, speak_reply=False)
    except Exception as e:
        raise HTTPException(500, f"{type(e).__name__}: {e}")
    if not r["ok"]:
        raise HTTPException(502, r.get("error", "speech pipeline failed"))

    if req.speak:
        name = f"{uuid.uuid4().hex[:12]}.wav"
        res = speak(r["spoken"], to_file=str(AUDIO_DIR / name))
        r["audio_url"] = f"http://localhost:8000/voice/audio/{name}" if res.get("ok") else None
    else:
        r["audio_url"] = None
    return r


@app.get("/voice/audio/{name}", tags=["voice"])
def voice_audio(name: str):
    path = AUDIO_DIR / name
    if not path.exists() or ".." in name or "/" in name:
        raise HTTPException(404, "audio not found")
    return FileResponse(path, media_type="audio/wav")
