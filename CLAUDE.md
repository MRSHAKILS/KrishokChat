# CLAUDE.md — pointer file

This project is governed by `AGENTS.md`. Read it fully before doing any work — it wins on conflict.

Trace roots (added 2026-08-27):

- `AGENTS.md` — hard rules, locked stack, folder structure, definition of done, two-track map (production vs paper).
- `docs/refactor/PROJECT_HANDOFF.md` → `docs/refactor/ARCHITECTURE.md` → `docs/refactor/REFACTOR_PLAN.md` — implementation memory.
- `docs/production_readiness/tasks/R_SERIES_EXECUTION_INDEX.md` — production roadmap (R1–R13 done; R13 grounded chunk fallback dark-launched 2026-08-27 under Amendment 03, flag `CHUNK_FALLBACK_ENABLED` default-off until experiment E26 is accepted).
- `experiments/registry.yaml` — canonical experiment trace (E02–E13 done; E14–E26 planned incl. CEA-pivot, unique-idea, training, and chunk-fallback layers).
- `experiments/ACCEPTANCE_PROTOCOL.md` + `experiments/IMPLEMENTATION_AND_AGGREGATION_PLAN.md` — run→verify→real-app-check→accept lifecycle; CEA-pivot plan.
- `paper/manifest.yaml` — paper folder trace; `docs/PAPER_POLICY.md` — citation/ban policy (arXiv:2606.29243 forbidden); `paper/manuscript/CLAIM_LEDGER_FREEZE.md` — S/F/U claim gates.
- Two-track rule: production code (`backend/`, `frontend/`) never reads `paper/`, `research_artifacts/`, `experiments/` at runtime; research harnesses may import backend offline only.
- External data origin (read-only): `E:\CSE498R\Agri-LLM\KrishokChat` — app depends only on mirrors under `backend/ml_assets/`.

Historical note: this file previously held a 2026-08-09 session summary describing a five-phase
advisory-workflow sprint (Gemini-key generation, `backend/app/services/advisory/` as live code).
That architecture was superseded by the `application/domain/ports/infrastructure` refactor — the old
paths are compatibility shims only (AGENTS.md §5.1). Do not restore the old summary; it was stale
and mojibake-corrupted (non-UTF-8 encoding).
