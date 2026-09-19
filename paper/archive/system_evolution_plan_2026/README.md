# KrishokTech System Evolution Plan 2026

> **Execution routing:** This directory contains the original proposal and verified T01-T04 context. It is not the current task queue. All local agents must execute from `execution_planning_2026_08_12/README.md` and `execution_planning_2026_08_12/11_FINAL_IMPLEMENTATION_SPEC.md`. Where the two layers differ, the dated execution package supersedes this parent plan.

## Decision in one sentence

Preserve the current safety-first pipeline and evaluate two bounded additions: (A) a structured Bengali agricultural claim and dosage verifier with calibrated risk-coverage abstention, and (B) dialect-sensitive retrieval with safety-preserving normalization.

## Evidence policy

- **Implemented** means confirmed in active code under `backend/app/application/`, `domain/`, `ports/`, or `infrastructure/`.
- **Documented** means stated in repository documentation but not established by an executable artifact.
- **Literature-supported** means supported by `paper/literature review/`; this does not establish local performance.
- **TODO/unverified** marks every numerical claim from the two authoritative local PDFs until extraction and reconciliation against stable local artifacts.
- Never cite or reuse the deprecated paper prohibited by `AGENTS.md` and `docs/PAPER_POLICY.md`.

Authoritative team paper filenames:

- `paper/done papers/KrishokTech__A_Provenance_Traceable_Multi_Task_Bengali_Agricultural_Benchmark_with_Safety_Critical_Chemical_Advisory.pdf`
- `paper/done papers/AgriTrust.pdf`

## Index

| File | Purpose |
|---|---|
| `01_CURRENT_SYSTEM_SCIENTIFIC_POSITION.md` | Implemented, planned, and claimed system position |
| `02_LANDSCAPE_GAPS_COMPETITIVE.md` | Consolidated literature taxonomy, gaps, and competitors |
| `03_CANDIDATE_DIRECTIONS.md` | Twenty scored research directions |
| `04_THREE_SYSTEM_CONCEPTS.md` | Complete concepts A, B, and C |
| `05_RECOMMENDED_ARCHITECTURE.md` | Current and proposed flows, seams, and change matrix |
| `06_EVALUATION_BENCHMARK_PLAN.md` | Evaluation-first benchmark, metrics, statistics, and artifacts |
| `07_BANGLADESH_HUMAN_STUDY.md` | Expert and farmer study protocol |
| `08_ROADMAP_4_TO_8_WEEKS.md` | Stages 0-10 with four- and eight-week scopes |
| `09_AGENT_TASK_GRAPH.md` | Ordinary-agent executable task graph and parallel lanes |
| `10_PAPER_BLUEPRINT.md` | Paper structure, claims, tables, figures, and evidence gates |
| `11_REVIEWER_ATTACK.md` | Skeptical review and mitigations |
| `12_FINAL_DECISION.md` | Exact build, conditional, and do-not-build decisions |
| `MEMORY.md` | Persistent status and next action |
| `AGENTS.md` | Scoped execution rules |

## Source map

- Research-grounding input: `paper/literature review/00_SCOPE_AND_ANGLES.md` through `10_SYNTHESIS_GAPS_POSITIONING.md`.
- Designated research-gap input: `paper/literature review/11_RESEARCH_GAPS_competitive_matrix.md`.
- Runtime contracts: `docs/refactor/PROJECT_HANDOFF.md`, `ARCHITECTURE.md`, and `REFACTOR_PLAN.md`.
- Exact active seams: `backend/app/application/container.py`, `qa_pipeline.py`, `vision_pipeline.py`; `backend/app/ports/verifier.py`, `retriever.py`; `backend/app/infrastructure/verification/dosage.py`, `retrieval/bm25.py`.

## Use order

Use `09_AGENT_TASK_GRAPH.md` only as historical rationale. Execute the amended graph in `execution_planning_2026_08_12/11_FINAL_IMPLEMENTATION_SPEC.md`. The independent local-model serving lane is defined in `execution_planning_2026_08_12/13_LOCAL_MODEL_INTEGRATION_PLAN.md` and its dated amendment; it does not authorize research implementation.
