# Monitoring Queries — Application Insights

Telemetry is emitted through the OpenTelemetry span API via
`azure-monitor-opentelemetry`. Spans surface in the `dependencies` table, not
`customEvents`; the latter requires the classic Application Insights SDK. Queries
are written against `dependencies` accordingly.

Automatic instrumentation additionally captures every outbound Azure call
(OpenAI, Document Intelligence, Blob, Search) with no extra code.

Resource: `appi-bankai-alt742` · Workspace: `law-bankai-alt742` · Region: centralus

## 1. AI latency and token consumption

    dependencies
    | where name == "rag_query" and timestamp > ago(24h)
    | extend tokens = toint(customDimensions.total_tokens), ms = todouble(customDimensions.duration_ms), grounded = tostring(customDimensions.grounded)
    | summarize requests = count(), p50_ms = round(percentile(ms, 50), 0), p95_ms = round(percentile(ms, 95), 0), total_tokens = sum(tokens), ungrounded = countif(grounded == "False")

Observed: 5 requests · p50 5497ms · p95 6780ms · 5540 tokens · 1 ungrounded.

## 2. Document processing success rate

    dependencies
    | where name == "document_processed" and timestamp > ago(24h)
    | extend status = tostring(customDimensions.status), ms = todouble(customDimensions.duration_ms)
    | summarize total = count(), failed = countif(status == "failed"), avg_seconds = round(avg(ms) / 1000, 2)
    | extend success_rate_pct = round(100.0 * (total - failed) / total, 1)

Observed: 3 processed · 0 failed · 9.48s average · 100% success.

## 3. Per-service latency (automatic instrumentation)

    dependencies
    | where timestamp > ago(24h) and isnotempty(target)
    | summarize calls = count(), p95_ms = round(percentile(duration, 95), 0) by target
    | order by calls desc

Observed: OpenAI 10 calls · Cognitive Services 9 · Blob 6 · Search 5.

## 4. Grounding rate over time

    dependencies
    | where name == "rag_query" and timestamp > ago(24h)
    | extend grounded = tostring(customDimensions.grounded)
    | summarize total = count(), grounded_count = countif(grounded == "True") by bin(timestamp, 15m)
    | extend grounding_rate_pct = round(100.0 * grounded_count / total, 1)
    | render timechart

An ungrounded answer is not an error. It records the assistant correctly refusing a
question the policy corpus does not cover. This metric tracks guardrail activation,
not failure.

## Dashboard

Screenshots in `monitoring-dashboard1.png` through `monitoring-dashboard3.png`.

## Metrics tracked (spec Section 22)

Documents processed, successful, failed · average processing time · AI request count ·
AI failures · average and p95 AI response time · prompt, completion and total tokens ·
search failures · grounding rate.
