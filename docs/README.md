# Documentation

| File | What it is |
|---|---|
| `architecture.md` | Architecture diagram (Mermaid, renders on GitHub) and design rationale |
| `architecture.svg` | Landscape architecture diagram, for screen |
| `architecture-a4.pdf` | A4 print version, for the report |
| `architecture-a4.svg` | A4 source |
| `architecture-a4.html` | Print wrapper — open in a browser, Ctrl+P, Save as PDF |
| `security.md` | Entra ID, managed identity, Key Vault, RBAC, data protection, and three incidents found during implementation |
| `rbac-matrix.md` | Role assignments per resource, generated from the live environment |
| `monitoring-queries.md` | KQL for the Application Insights dashboard, with observed results |
| `monitoring-dashboard1-3.png` | Dashboard screenshots |
| `test-results.txt` | Full pytest output, 30 tests passing |
| `retrieval-comparison.txt` | Keyword vs vector vs hybrid over 10 questions with known ground truth |

## Findings worth reading

**`security.md`** — an orphaned role assignment that is harder to delete than it was
to create, a leaked key rotated with zero application impact, and a system prompt
disclosure that a prompt-level instruction failed to prevent. All three fixed,
all three documented.

**`retrieval-comparison.txt`** — expanding the corpus from 7 to 12 policies *reduced*
vector performance and *improved* keyword performance. Hybrid absorbed both and
held flat. That is the argument for hybrid: robustness, not peak accuracy.
