# Thesis Decision

## Final Decision

**OPTION B: Keep A, modify B.**

**Frozen thesis:** `Evidence-linked, relation-aware selective certification for Bengali agrochemical advice under a BM25-only runtime, with dialect/Banglish normalization evaluated as a safety-constrained robustness axis.`

A is the primary research contribution. B is a secondary evaluation/protocol contribution. B does not include a learned normalizer by default.

## Attempt to Disprove

The adversarial test attacked four possible claims:

1. Agricultural numerical or contradiction verification is new. AgroLLM, DG-Eval, and Crop GraphRAG defeat this claim.
2. Claim-level groundedness or selective certification is new. RefusalBench, grounded factuality work, FRANQ, SURE-RAG, Claim-Selective Certification, and UniCR defeat this claim.
3. Bengali agricultural retrieval is new. KrishokBondhu and Cross-Lingual Bengali Agricultural RAG defeat this claim.
4. Bengali dialect, Banglish, transliteration, or code-mixed robustness evaluation is new. The BanglaLP and FIRE works plus dialect-bias research defeat this claim.

The broad A+B recommendation therefore fails novelty adjudication.

## Why A Survives Narrowly

A survives as a domain-specific empirical contribution if the study binds every certification decision to a stable source and evidence span, evaluates full agrochemical relations rather than isolated number strings, calibrates release/abstain decisions on development data, and measures dangerous pass-through on expert gold. The active runtime strengthens causal interpretability because BM25 remains fixed. Any gain then comes from extraction, relation matching, or selective policy rather than an unbuilt dense retriever.

The current lexical verifier supplies a real baseline. It cannot represent denominator, interval, PHI, polarity, applicability, source conflict, or partial support. A structured deterministic-first verifier therefore addresses a measured implementation gap. This is a testable distinction, not an assumed novelty claim.

## Why B Is Demoted

The literature already occupies Bengali dialect RAG, transliteration robustness, code-mixed IR, and dialect bias. B remains useful because normalization can alter both retrieval evidence and safety intent. Its role is to test whether A's certification result remains invariant across paired standard Bangla, regional, and Banglish forms. The default intervention is Unicode plus a reviewed dictionary. A learned normalizer is optional and must beat that baseline without violating safety gates.

## Stop Conditions

- Stop the primary paper claim if expert relation-label agreement misses the prespecified T07 gate after one guideline revision.
- Stop method superiority claims if the hybrid verifier does not improve the primary dangerous non-abstention endpoint over the lexical baseline on the untouched test split.
- Stop calibration claims if thresholds are selected or changed after test inspection, or if high-risk development support is too small for the prespecified estimator.
- Stop evidence-linked claims if stable `source_id` and exact `evidence_span` cannot be reconstructed for the evaluation set.
- Stop integrated safety claims until the source-empty vision fallback is repaired and regression tested.
- Stop subgroup conclusions where sample support is inadequate; report descriptive results only.
- Stop learned-normalizer work unless the reviewed dictionary baseline leaves a material, prespecified gap and the candidate passes intent, slot, and safety invariance gates.
- Stop release if a fresh run cannot regenerate primary tables from manifests and hashes.

## Confidence

**Decision confidence: high (0.86).** Runtime and artifact evidence strongly supports the narrowed scope. Novelty confidence is moderate until T07 verifies full texts and bibliographic details. Outcome confidence is intentionally unset: no proposed method result has been run.
