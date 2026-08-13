# Paper Contribution Contract

## Contribution 1

**What is new:** A frozen Bengali agrochemical claim resource and annotation protocol that links atomic fields, applicability, polarity, uncertainty, and expert relation labels to stable source IDs and exact evidence spans.

**Why it matters:** Existing substring verification cannot distinguish a matching number from the wrong crop, formulation, denominator, interval, PHI, prohibition, or source scope.

**Experiment proof:** T05-T10 artifact reconciliation, schema freeze, expert pilot, agreement analysis, adjudicated labels, and reproducible dataset manifests. Claim only the fields and sample properties supported by released artifacts.

## Contribution 2

**What is new:** An evaluated deterministic-first hybrid verifier for this resource: parser/normalizer plus structured relation matcher, with optional NLI only as a secondary comparison.

**Why it matters:** The active verifier checks normalized dosage substrings and does not establish semantic relation support.

**Experiment proof:** E1 and E3 compare the captured lexical baseline, structured method, extraction oracle, field ablations, fixed LLM judge baseline, and optional NLI under expert gold. Report dangerous non-abstention, relation metrics, latency, and failures.

## Contribution 3

**What is new:** A calibrated selective-certification policy for evidence-linked Bengali agrochemical claims under the actual BM25-only runtime.

**Why it matters:** A categorical verifier label without calibration hides the cost tradeoff between withholding supported advice and releasing unsupported high-risk advice.

**Experiment proof:** E2 freezes development-only calibration and threshold selection, then reports test risk-coverage, AURC, calibration, false abstention, dangerous non-abstention, and threshold stability.

## Contribution 4

**What is new:** A paired safety-constrained robustness protocol that measures how reviewed dictionary normalization of standard Bangla, regional forms, and Banglish changes BM25 retrieval and relation certification while requiring safety and slot invariance.

**Why it matters:** Better retrieval can still corrupt negation, chemical identity, dosage, or harmful intent. Retrieval-only reporting misses this failure.

**Experiment proof:** E4-E6 and the E5 factorial interaction compare raw, Unicode, and dictionary conditions by paired intent. They report retrieval, safety flips, slot preservation, certification risk, subgroup results, and native-review agreement. A learned condition is optional and cannot define this contribution.

## Rejected Claims

Reject any claim that KrishokChat is the first agricultural verifier, first claim-certification method, first Bengali agricultural RAG system, first Bengali dialect/Banglish RAG study, semantic verifier in its current form, hybrid retriever, calibrated runtime, verified local Gemma performer, object detector, or source-verified vision fallback. Reject accuracy, novelty, fairness, usability, trust, agronomic outcome, and deployment claims that lack a prespecified experiment and ledger entry.
