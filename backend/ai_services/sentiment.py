"""Sentiment analysis and complaint triage, grounded in Complaint Policy Section 4.

Severity is determined by WHAT happened (Section 4 categories), not by how strongly
the customer expressed it. Sentiment refines within a band; it does not set the band.
"""
import csv
import io
from azure.ai.textanalytics import TextAnalyticsClient
from azure.storage.blob import BlobServiceClient
from config.settings import get_settings, credential

HIGH_SIGNALS = {
    "unauthorised transaction": ("unauthorised", "unauthorized", "not authorised by me"),
    "suspected fraud": ("fraud", "fraudulent", "stolen", "scam"),
    "financial loss": ("financial loss", "money missing", "debited but"),
    "repeated failure to respond": ("nobody has responded", "no one has responded",
                                    "still not received", "for over a month",
                                    "eleven days ago", "three times", "four times"),
    "escalation threat": ("ombudsman", "legal action", "consumer court"),
    "relationship at risk": ("closing every account", "closing my account",
                             "close all my accounts", "switching to another bank"),
    "repeated contact without resolution": ("zero answers", "no answers",
                                            "two phone calls", "three visits"),
}

MEDIUM_SIGNALS = {
    "service delay": ("delayed", "pending", "still waiting", "has been pending",
                      "three weeks", "no response"),
    "documentation issue": ("keeps failing", "request failed", "cannot update",
                            "unable to submit", "never told why",
                            "without any explanation", "no reason was given",
                            "tell me the reason"),
    "incorrect charge": ("charge levied", "incorrect charge", "appears to be incorrect",
                         "wrongly charged"),
}

SLA_DAYS = {"HIGH": 1, "MEDIUM": 3, "LOW": 5}


def _client() -> TextAnalyticsClient:
    return TextAnalyticsClient(get_settings().ai_services_endpoint, credential())


def load_messages() -> list[dict]:
    s = get_settings()
    bsc = BlobServiceClient(s.blob_endpoint, credential())
    raw = bsc.get_blob_client("raw-documents", "kyc/customer_messages.csv") \
             .download_blob().readall().decode("utf-8")
    return list(csv.DictReader(io.StringIO(raw)))


def _match(text: str, groups: dict):
    low = text.lower()
    for label, terms in groups.items():
        if any(t in low for t in terms):
            return label
    return None


def classify(scores, text: str, category: str):
    hit = _match(text, HIGH_SIGNALS)
    if hit:
        return "HIGH", f"Section 4 high severity: {hit}"
    hit = _match(text, MEDIUM_SIGNALS)
    if hit:
        if scores.negative >= 0.95:
            return "HIGH", f"Section 4 medium severity ({hit}), escalated on severe dissatisfaction ({scores.negative:.2f})"
        return "MEDIUM", f"Section 4 medium severity: {hit}"
    if category == "Complaint":
        return "MEDIUM", "Section 4: logged as a complaint"
    return "LOW", "Section 4 low severity: information request or general feedback"


def analyse(rows: list[dict]) -> list[dict]:
    client = _client()
    out = []
    for i in range(0, len(rows), 5):
        batch = rows[i:i + 5]
        results = client.analyze_sentiment([r["message"] for r in batch], language="en")
        for row, res in zip(batch, results):
            if res.is_error:
                out.append({**row, "sentiment": "error", "priority": "MEDIUM",
                            "priority_reason": "analysis failed; defaulted", "sla_days": 3})
                continue
            sc = res.confidence_scores
            priority, reason = classify(sc, row["message"], row["category"])
            out.append({
                "customer_id": row["customer_id"],
                "category": row["category"],
                "message": row["message"],
                "sentiment": res.sentiment,
                "positive": round(sc.positive, 2),
                "neutral": round(sc.neutral, 2),
                "negative": round(sc.negative, 2),
                "priority": priority,
                "priority_reason": reason,
                "sla_days": SLA_DAYS[priority],
            })
    return out


if __name__ == "__main__":
    from collections import Counter

    results = analyse(load_messages())
    order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    results.sort(key=lambda r: (order[r["priority"]], -r["negative"]))

    print(f"\n{'ID':7} {'PRIORITY':9} {'SENTIMENT':9} {'NEG':>5} {'SLA':>4}  MESSAGE")
    print("-" * 110)
    for r in results:
        msg = r["message"][:58] + ("..." if len(r["message"]) > 58 else "")
        print(f"{r['customer_id']:7} {r['priority']:9} {r['sentiment']:9} "
              f"{r['negative']:5.2f} {r['sla_days']:>3}d  {msg}")

    print(f"\nPriority : {dict(Counter(r['priority'] for r in results))}")
    print(f"Sentiment: {dict(Counter(r['sentiment'] for r in results))}")

    print("\nJustification per message:")
    for r in results:
        print(f"  {r['customer_id']}  {r['priority']:7} {r['priority_reason']}")


