# Final Research Adjudication

**Date:** 2026-08-12  
**Status:** Frozen adjudication package  
**FINAL DECISION: OPTION B: Keep A, modify B.**

## Narrow Thesis

`Evidence-linked, relation-aware selective certification for Bengali agrochemical advice under a BM25-only runtime, with dialect/Banglish normalization evaluated as a safety-constrained robustness axis.`

Workstream A is primary. Workstream B is a secondary evaluation/protocol contribution. The plan does not require a learned normalizer. Such a model enters only if a reviewed dictionary baseline is inadequate and the learned condition passes the same intent-preservation and safety gate.

## Evidence Status

- Runtime facts trace to `../T04_BEHAVIOR_SNAPSHOT.md` and source paths recorded there.
- Artifact facts trace to `../T02_T03_ARTIFACT_INVENTORY.md`.
- Extracted local-PDF numbers trace to `../T01_PDF_EXTRACTION.md` and remain **NEEDS RECONCILIATION** until T05 links them to stable artifacts.
- Research and experiment constraints trace to `../01_CURRENT_SYSTEM_SCIENTIFIC_POSITION.md`, `../06_EVALUATION_BENCHMARK_PLAN.md`, and `../09_AGENT_TASK_GRAPH.md`.
- Root `AGENTS.md` and `docs/PAPER_POLICY.md` govern all citation and implementation work.

## Package Index

| File | Purpose |
|---|---|
| `01_IMPLEMENTATION_REALITY_AUDIT.md` | Reconciles assumed and active behavior. |
| `02_NOVELTY_ATTACK.md` | Tests the thesis against the closest current literature. |
| `03_THESIS_DECISION.md` | Freezes Option B and its stop conditions. |
| `04_HYPOTHESES.md` | Prespecifies five primary hypotheses. |
| `05_MINIMUM_EXPERIMENT_MATRIX.md` | Defines the minimum claim-bearing experiments. |
| `06_CLAIM_SCHEMA_AND_VERIFIER.md` | Freezes atomic fields, relations, and verifier design. |
| `07_ABSTENTION_AND_DIALECT_PROTOCOL.md` | Freezes risk-coverage and paired normalization protocols. |
| `08_FINAL_SYSTEM_ARCHITECTURE_CONTRACT.md` | Preserves ports, BM25, and topology while defining additions. |
| `09_PAPER_CONTRIBUTION_CONTRACT.md` | Limits the paper to four demonstrable contributions. |
| `10_REVIEWER_PREMORTEM.md` | States likely reviewer objections and minimum remedies. |
| `11_FINAL_IMPLEMENTATION_SPEC.md` | Gives ordinary agents an executable staged task graph. |
| `12_CLAIM_LEDGER.md` | Separates safe, forbidden, and unresolved claims. |
| `MEMORY.md` | Records the adjudicated state for later sessions. |
| `AGENTS.md` | Sets scoped execution and evidence rules. |

## Decision Boundary

The package rejects broad novelty claims for agricultural verification and broad novelty claims for Bengali dialect normalization. It permits a narrower claim only if the frozen evaluation shows that evidence-linked relation matching plus selective abstention improves safety-critical certification over the current lexical matcher under the actual BM25-only runtime. Retrieval gains alone cannot support a safety claim.
