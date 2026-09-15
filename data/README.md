# Horizon National Bank — Capstone Dataset

Synthetic corpus for an AI-powered banking document and customer support assistant.
All entities, customers and identifiers are fictional. No real personal data.

## Contents

| Folder | Files | Purpose |
|---|---|---|
| `policy-documents/` | 12 PDFs | RAG corpus. Text layer present, numbered sections. 104 sections total. |
| `customer-documents/` | 20 PDFs | Document Intelligence extraction. Two-column label/value tables. |
| `scanned-documents/` | 6 PDFs | **Image only, zero text layer.** Forces genuine OCR. |
| `customer-messages/` | 1 CSV | 60 messages for sentiment analysis and triage. |
| `tests/` | 7 JSON | Test case definitions with expected outcomes. |

## Policy corpus

home_loan_policy.pdf (13 sections) · personal_loan_policy.pdf (10) · kyc_policy.pdf (9) ·
credit_card_policy.pdf (8) · account_opening_policy.pdf (7) · aml_policy.pdf (8) ·
complaint_policy.pdf (8) · vehicle_loan_policy.pdf (9) · fair_practices_code.pdf (8) ·
data_privacy_policy.pdf (9) · digital_banking_policy.pdf (7) ·
collection_and_recovery_policy.pdf (8)

## Load-bearing values

These are referenced by the rule engine and the test suite. Changing them breaks tests.

- **Home Loan §3** — 3 years total employment, 6 months with current employer
- **Home Loan §4** — INR 50,000 minimum monthly income, FOIR 50 percent
- **Home Loan §5** — INR 5,00,000 to INR 10,00,00,000
- **Home Loan §6** — six required documents
- **Home Loan §7** — bureau score 700
- **Home Loan §9** — no automated approval or rejection
- **Personal Loan §3** — 2 years total, 12 months current employer
- **Personal Loan §7** — bureau score 720
- **KYC §4** — 2 / 8 / 10 year updation by risk band
- **Complaint §3** — four escalation levels; **§4** — three severity bands
- **AML §3** — INR 10,00,000 cash threshold; **§4** — 7 working days for an STR

## The demo scenario

**C1001, Rahul Sharma** — Home Loan, INR 75,00,000, income INR 1,25,000,
bureau 744, **2 years total employment**.

Fails exactly one criterion: Home Loan Policy §3 requires 3 years. Every other
criterion passes, so the verdict is unambiguous.

Other notable cases: C1004 fails only on bureau score (698 vs 700). C1005 fails
current-employer tenure (8 months vs 12) and bureau score (669 vs 720). C1013 has
9 months total employment against the credit card requirement of 1 year.

## Deliberate absences

The following topics appear nowhere in the corpus, so that refusal tests remain valid:
cryptocurrency, education loans, gold loans, fixed deposits, safe deposit lockers.
A system that answers questions on these has hallucinated.

## OCR verification

`customer_1001_bank_statement_scanned.pdf` contains account number `90210041234`,
PAN `ABCDE1234F` and IFSC `MNBK0000412` **as pixels only**. Recovering those strings
proves OCR ran rather than a hidden text layer being read.

## Regenerating

    python regenerate_dataset.py

Requires `reportlab` and `Pillow`. Output is deterministic (seed 7).

## Retrieval benchmark

Measured over 10 questions with known ground truth, against the full 12-policy,
104-chunk corpus.

| mode | top-1 | recall@5 | MRR |
|---|---|---|---|
| keyword | 7/10 | 10/10 | 0.817 |
| vector | 8/10 | 8/10 | 0.800 |
| hybrid | 8/10 | 10/10 | **0.870** |

Against the earlier 7-policy corpus the figures were keyword 0.703, vector 0.850,
hybrid 0.875. Expanding the corpus **reduced vector performance and improved
keyword performance**.

Vector recall fell because Vehicle Loan Policy Section 3 and Home Loan Policy
Section 3 are semantically near-identical: both state an employment minimum
verified by the same means. Embeddings encode meaning, so the two chunks sit close
together in vector space. The discriminating token is the literal word "home"
versus "vehicle", which lexical search weighs and embeddings blur.

Keyword performance improved because the expanded policies contain more
distinctive terms per section, giving BM25 more signal.

Hybrid retrieval absorbed both effects and remained flat. This is the argument for
hybrid: not that it wins every question, but that it is robust to changes in corpus
composition that degrade either mode alone.
