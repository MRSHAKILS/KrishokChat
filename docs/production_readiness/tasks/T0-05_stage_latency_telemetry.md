# T0-05 — Stage Latency + Token/Cost Telemetry in Audit Records

- **Status:** DONE (2026-08-17)
- **Tier:** 0 (demo-safe, pre-capstone)
- **Depends on:** T0-04 (request IDs — for correlation; the field is nullable so T0-04 is recommended, not strictly required)
- **Blocks:** nothing
- **Amendment:** none required

## Goal

Extend audit records with per-stage timings (safety → retrieval → generation → verifier), token counts (input/output), provider name, and an estimated cost **only where a real cost basis exists**. This turns the audit log into the operations telemetry that powers `/analytics`-style panels and the B2B audit story — without changing any endpoint contract.

## Read first

- `backend/app/application/` — the QA orchestrator (or equivalent) that drives the four pipeline stages and produces audit records; find the exact file(s) where stages are called and where the audit record is assembled.
- `backend/app/ports/` — the audit port's record shape.
- `backend/app/infrastructure/audit/jsonl.py` — how records are serialized today (and T0-02's sqlite adapter if merged).
- `backend/app/models/` (schemas) — the audit record schema, if any.
- `backend/app/api/` — confirm `/api/safety/metrics` reads only fields that stay unchanged.

## Invariants (do not break)

- No existing audit field is renamed, dropped, or re-typed.
- `/api/safety/metrics` and all other response shapes are unchanged (frontend contract).
- Old records (written before this task) remain readable by every consumer.
- Safety behavior, retrieval behavior, generation, verifier: untouched.
- **Never fabricate cost**: if no price table exists for a provider, `cost_estimate` is `null`. A one-line comment in the cost helper states the source of any number used.

## Design

- Extend the audit record with optional fields:
  - `stage_timings_ms: dict[str, float]` — keys exactly `safety`, `retrieval`, `generation`, `verifier`
  - `tokens: dict[str, int]` — `input`, `output` (only where the LLM client exposes usage; else `null`)
  - `provider: str | null` — the provider that actually served generation (important once T0-06 failover lands)
  - `cost_estimate: float | null` — computed only when a cost table exists (see invariants)
  - `request_id: str | null` — populated from the T0-04 contextvar when present
- Timer helper: a small `stage_timer` context manager in the application layer (or `core/telemetry.py` if one exists — reuse).
- Serialization: both JSONL and SQLite adapters must tolerate missing fields (`None`/absent keys) for old records.

## Scope — create

- `backend/tests/test_audit_telemetry.py` (a stubbed pipeline run produces a record with all four stage timings; fields absent for old-format fixtures; `cost_estimate` null when no price table)

## Scope — modify

- The orchestrator file(s) found in `Read first` (add timers + fields only)
- The audit record assembly (schema or dict builder)
- `backend/app/infrastructure/audit/jsonl.py` (serialization of new fields — additive)
- T0-02's `audit/sqlite.py` if merged (new columns already reserved — fill them)
- No API route changes

## Do not touch

- Route handlers, metrics aggregation logic
- Safety/retrieval/generation/verifier stage logic itself (wrap, don't edit)
- `backend/app/agents/`, `backend/app/services/advisory/`
- `capstone/`, `paper/`, `dataset_release/`, `frontend/`

## Rollback

Commit revert (`git revert <commit>`) — bounded to orchestrator + serializers. No config switch needed (fields are additive).

## Verification gate (stop/go)

1. `uv run pytest backend/tests/test_audit_telemetry.py -v` — green.
2. Live run: one safe QA query with a real/stub LLM → the newest audit record contains `stage_timings_ms` with all four keys; `tokens`/`provider` present where the lane exposes them.
3. `/api/safety/metrics` response identical before/after (diff).
4. Old JSONL records still load (run the metrics endpoint against a fixture file containing pre-change records).
5. `uv run python -m compileall -q backend/app` — clean.

Gate fails ⇒ STOP and report exact output.

## Definition of done

Per AGENTS.md §6 + task handbook. Commit message notes open questions (e.g., which providers expose usage data); completion line in `docs/refactor/PROJECT_HANDOFF.md`.

## Open questions

- Which LLM lanes expose token usage today (OpenRouter yes; Ollama local often no) — resolve per lane and leave `null` where unknown.
- Whether the orchestrator is one file or split — enumerate stages exactly before editing.