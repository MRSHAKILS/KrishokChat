# Project Memory

## Executive Summary

KrishokChat is a Bangladesh-focused Bengali agricultural advisory prototype with safety-before-retrieval QA and classification-based vision routing. The research plan preserves that architecture and tests two bounded modules: structured agricultural claim/dosage verification with calibrated abstention, and dialect-sensitive retrieval with safety-preserving normalization.

## Research Objective

Measure whether typed evidence relations reduce unsupported high-risk advice and whether normalization improves dialect/Banglish retrieval without changing safety intent.

## Selected Research Gap

The designated gap input is `paper/literature review/11_RESEARCH_GAPS_competitive_matrix.md`. Selected gaps are calibrated abstention in Bengali agricultural QA, safety-monotone refusal, agricultural claim/dosage relation verification, and unmeasured dialect retrieval/safety behavior.

## Success Criteria

Expert-adjudicated labels; baseline comparisons; risk-coverage curves; paired dialect retrieval/safety metrics; native authenticity and intent review; reproducible manifests/hashes; no source-empty treatment marked verified.

## Current Project Status

Stage 0 evidence reconciliation COMPLETE (T01-T04). Ready for T05 reconciliation and T07 schema freeze. Current runtime wires BM25 only (no dense/FAISS), lexical dosage verifier only (no semantic verification), safety-before-retrieval enforced, 11/11 tests passing. Hybrid retrieval and local Gemma performance remain unverified at runtime.

## Completed Milestones

- Read repository rules and mandatory handoff documents.
- Reviewed the current literature package and designated research-gap file.
- Inspected active QA, verifier, container, benchmark, and vision seams.
- Defined concepts, architecture, evaluation, human study, roadmap, task graph, paper gates, and final decision.
- **T01:** Both authoritative PDFs extracted (PyMuPDF, 265+103 claims). PDF hashes: KrishokChat=75cca13c..., AgriTrust=9b30b769...
- **T02:** 158,764 records across 222.8 MB external dataset located and verified. 9 in-repo dataset files verified. 2 bit-identical copies confirmed. dataset_release/ absent from workspace root.
- **T03:** BM25 index (17MB) + corpus tokenizer (4.7MB) present. FAISS/dense NOT built. 6 vision models (57.3MB total, all classify). Gemma LoRA checkpoint (279MB adapter, r=32, alpha=64, base=unsloth/gemma-4-E4B-it).
- **T04:** All 14 behavior checks CONFIRMED with exact code quotes. 11/11 tests pass. Vision fallback defect confirmed (solution_bn stamped "verified" with empty sources).

## Pending Milestones

T05 (PDF reconciliation), T06 (vision defect fix), T07 (schema freeze), T08-T26 in `09_AGENT_TASK_GRAPH.md`.

## Known Risks (updated)

- FAISS/dense index not built — hybrid retrieval is NOT available at runtime.
- Vision fallback stamps KB text as "verified" with empty treatment_sources — must fix before any claim.
- Safety splits sum to 18,418, not 20,112 (splits are a proper subset).
- Expert and native-dialect reviewer availability is unknown.
- Human study requires ethics approval and safe recruitment.

## Open Questions (resolved)

- Dataset location: Found at `E:\CSE498R\Agri-LLM\KrishokChat\krishokchat_dataset_main` and `agritrust knowledge nodes`.
- PDF claims: 265+103 raw claims extracted, all NEEDS RECONCILIATION for T05.
- Hybrid retrieval: NOT built. Only BM25 is active.
- Gemma: LoRA adapter exists but serving/quality unverified.

## Next Recommended Action

Run T05 (reconcile PDF numbers against dataset/artifact counts) and T07 (freeze claim schema, annotation guide, primary endpoints). T06 (vision defect fix) can run in parallel.
