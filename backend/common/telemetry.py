"""Application Insights telemetry. Tracks the metrics required by Section 22."""
import functools
import time
from config.settings import get_settings

_configured = False
_tracer = None
_local_events: list[dict] = []          # in-process mirror, for the UI dashboard


def init() -> bool:
    """Configure Azure Monitor once. Returns False if no connection string."""
    global _configured, _tracer
    if _configured:
        return _tracer is not None

    _configured = True
    conn = get_settings().applicationinsights_connection_string
    if not conn:
        print("  telemetry: no connection string, local-only mode")
        return False

    try:
        from azure.monitor.opentelemetry import configure_azure_monitor
        from opentelemetry import trace
        configure_azure_monitor(connection_string=conn, logger_name="bankai")
        _tracer = trace.get_tracer("bankai")
        return True
    except Exception as e:
        print(f"  telemetry: disabled ({type(e).__name__}: {e})")
        return False


def record(event: str, **attrs):
    """Emit one event to App Insights and keep a local copy."""
    entry = {"event": event, "timestamp": time.time(), **attrs}
    _local_events.append(entry)

    if not init():
        return entry

    with _tracer.start_as_current_span(event) as span:
        for k, v in attrs.items():
            if v is not None:
                span.set_attribute(k, v)
    return entry


def tracked(event: str):
    """Decorator: time a function, record success or failure."""
    def outer(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            started = time.time()
            try:
                result = fn(*args, **kwargs)
            except Exception as e:
                record(event, status="failed", duration_ms=round((time.time() - started) * 1000, 1),
                       error_type=type(e).__name__)
                raise
            attrs = {"status": "succeeded",
                     "duration_ms": round((time.time() - started) * 1000, 1)}
            if isinstance(result, dict):
                if "usage" in result and isinstance(result["usage"], dict):
                    attrs["prompt_tokens"] = result["usage"].get("prompt_tokens")
                    attrs["completion_tokens"] = result["usage"].get("completion_tokens")
                    attrs["total_tokens"] = result["usage"].get("total_tokens")
                if "grounded" in result:
                    attrs["grounded"] = result["grounded"]
                if "sources" in result:
                    attrs["chunks_retrieved"] = len(result["sources"])
                    if result["sources"]:
                        attrs["top_score"] = result["sources"][0].get("score")
                for key in ("status", "ocr_required", "fields_found", "fields_expected"):
                    if key in result.get("processing", {}):
                        attrs[f"doc_{key}"] = result["processing"][key]
            record(event, **attrs)
            return result
        return inner
    return outer


def events(event_name: str | None = None) -> list[dict]:
    return [e for e in _local_events if event_name is None or e["event"] == event_name]


def dashboard() -> dict:
    """Section 22 metrics, computed from local events."""
    docs = events("document_processed")
    ai = events("rag_query")
    searches = events("search_query")

    def avg(rows, key):
        vals = [r[key] for r in rows if r.get(key) is not None]
        return round(sum(vals) / len(vals), 1) if vals else 0.0

    doc_failed = sum(1 for d in docs if d.get("status") == "failed")
    ai_failed = sum(1 for a in ai if a.get("status") == "failed")
    ungrounded = sum(1 for a in ai if a.get("grounded") is False)

    return {
        "documents_processed": len(docs),
        "documents_successful": len(docs) - doc_failed,
        "documents_failed": doc_failed,
        "avg_document_processing_ms": avg(docs, "duration_ms"),
        "ai_requests": len(ai),
        "ai_failures": ai_failed,
        "avg_ai_response_ms": avg(ai, "duration_ms"),
        "search_queries": len(searches),
        "search_failures": sum(1 for s in searches if s.get("status") == "failed"),
        "total_tokens": sum(a.get("total_tokens") or 0 for a in ai),
        "prompt_tokens": sum(a.get("prompt_tokens") or 0 for a in ai),
        "completion_tokens": sum(a.get("completion_tokens") or 0 for a in ai),
        "ungrounded_answers": ungrounded,
        "grounding_rate_pct": round(100 * (len(ai) - ungrounded) / len(ai), 1) if ai else 0.0,
    }
