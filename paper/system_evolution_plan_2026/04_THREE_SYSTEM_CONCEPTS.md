# Three System Concepts

## Concept A: ClaimSafe-BN

**Research question:** Can typed agricultural relation verification and calibrated abstention reduce unsupported high-risk claims while retaining useful answers?

**Method:** Decompose an answer into claims with fields `crop, disease, action, chemical/intervention, amount, unit, denominator, interval, safety_condition, source_id`. Compare lexical matching, an LLM judge, NLI/structured verification, and a hybrid. Calibrate an answer/abstain threshold on development data only.

**Inputs:** Query, answer, retrieved passages with stable IDs, optional crop/disease context.

**Outputs:** Atomic claims; per-field values; entailed/contradicted/unsupported labels; risk class; calibrated score; `answer`, `answer_with_flags`, or `refer` action.

**Constraints:** Every chemical amount requires amount-unit-denominator relation support. Missing evidence cannot become general model knowledge. High-risk unsupported claims force abstention.

**Evaluation:** Relation F1, claim-label macro-F1, dosage exact-match and tolerance-aware relation accuracy, unsupported high-risk claim rate, ECE/Brier score, selective risk, coverage, AURC, latency.

**Contribution:** Typed Bengali agricultural claim verification and an expert-validated risk-coverage protocol.

**Engineering seam:** Extend `backend/app/ports/verifier.py`; add domain contracts and an infrastructure adapter; wire only through `backend/app/application/container.py`. Preserve routes and SSE.

## Concept B: DialectSafe-RAG

**Research question:** Does dialect/orthography normalization improve retrieval while preserving benign and harmful intent?

**Method:** Build paired standard Bangla, regional-variety, and Banglish queries. Evaluate raw input, Unicode-only normalization, lexical/dictionary normalization, and a learned or prompted normalizer only if native review approves it. Apply the same variants to retrieval and safety routing.

**Inputs:** Intent-linked query groups, corpus, relevance judgments, safety labels, normalization output.

**Outputs:** Retrieval rankings, safety decisions, normalized query, intent-preservation judgment, dialect authenticity judgment.

**Constraints:** Split by intent family before generating variants. Do not place paraphrases of one intent across train and test. A normalizer must abstain when uncertain. Never normalize after the safety decision in a way that hides the raw query from audit.

**Evaluation:** nDCG@10, Recall@k, MRR, safety macro-F1, class recall, over-refusal, under-refusal, paired intent-preservation rate, normalization harm rate, per-variety deltas, latency.

**Contribution:** Joint measurement of retrieval gain and safety regression from normalization in Bengali agricultural advice.

**Engineering seam:** Keep raw query immutable; add an optional normalizer port before query building, with both raw and normalized forms supplied to deterministic safety checks and audit. Exact placement requires a threat-model decision in Stage 2.

## Concept C: KrishokChat-Evidence System Study

**Research question:** Does the combined safety-first, claim-verified, dialect-aware system improve expert-rated evidence alignment and user-calibrated trust over the current pipeline?

**Method:** Integrate Concepts A and B after separate validation. Repair the vision evidence fallback. Run expert review and a bounded Bangladesh study comparing current and proposed outputs. Include latency and failure-path evidence.

**Evaluation:** End-to-end high-risk error, useful coverage, expert actionability, source traceability, safety intent preservation, trust calibration, comprehension, and referral recall. Avoid agronomic outcome claims.

**Contribution:** System-level evidence that two bounded modules improve a Bengali agricultural advisory pipeline.

**Risk:** Concept C can blur component causality and exceed the schedule. It is the paper narrative, not an instruction to build extra agents.

## Recommendation

Build A first, evaluate B in parallel, and integrate them only after each passes its component gate. Use C as the eight-week paper configuration. The four-week paper should report A plus a completed B benchmark even if B remains offline.
