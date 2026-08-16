# T0-02 — Audit → SQLite Adapter

- **Status:** NOT STARTED
- **Tier:** 0 (demo-safe, pre-capstone)
- **Depends on:** T0-01 (SQLite foundation, gate passed)
- **Blocks:** nothing
- **Amendment:** none required

## Goal

Add a SQLite-backed implementation of the audit port (`infrastructure/audit/sqlite.py`) alongside the existing JSONL adapter, selectable via `AUDIT_BACKEND=jsonl|sqlite` (**default `jsonl`**). Include an idempotent backfill script that imports existing JSONL records. The `/api/safety/metrics` endpoint must return identical numbers regardless of backend.

## Read first

- `backend/app/ports/` — exact audit port name + methods.
- `backend/app/infrastructure/audit/jsonl.py` — the record fields it writes (keep every field, add new ones only).
- `backend/app/infrastructure/storage/sqlite.py` (T0-01) — migration runner usage.
- `backend/app/application/container.py` — where the audit adapter is selected; the switch belongs here.
- `backend/app/api/` — the endpoint(s) that read audit data for `/api/safety/metrics`, `/api/history`, `/api/audit/events` (if present) so the SQLite adapter can serve identical reads.
- `backend/app/core/config.py` — where `AUDIT_BACKEND` joins the settings.

## Invariants (do not break)

- JSONL adapter code and behavior unchanged (it stays the default).
- Safety fail-closed pipeline untouched.
- Metrics/history endpoint response shapes unchanged (frontend contract).
- Audit stays local — same machine, no network.
- New fields may be added to the record but no existing field may be renamed, dropped, or re-typed.

## Design

- Table `audit_records` (migration v2 in the T0-01 runner):
  - `id INTEGER PRIMARY KEY AUTOINCREMENT`
  - all fields the JSONL record has today (flat columns where scalar; JSON text columns where nested — mirror exactly)
  - `timestamp TEXT` (ISO) — indexed
  - `category TEXT` — indexed (drives metrics counts)
  - `request_id TEXT` (nullable for now; populated from T0-04 once merged)
  - `stage_timings_ms TEXT` / `token_usage TEXT` / `provider TEXT` — nullable, reserved for T0-05
- Adapter implements the same methods as the JSONL adapter (append/log + any read methods). Use the T0-01 connection helper.
- Backfill: `backend/scripts/backfill_audit_jsonl_to_sqlite.py` — reads the JSONL file (path from `resolved_audit_log_path`), inserts rows; idempotent by `(timestamp, query_hash)` unique index or by truncate-and-reload when `--force` is passed.
- Wiring: `application/container.py` builds `AuditSqliteSink` when `AUDIT_BACKEND == "sqlite"`, else the JSONL sink. A one-line comment marks the switch.
- `.env.example`: `AUDIT_BACKEND=jsonl  # jsonl | sqlite (adapter selected at container build time)`

## Scope — create

- `backend/app/infrastructure/audit/sqlite.py`
- `backend/scripts/backfill_audit_jsonl_to_sqlite.py`
- `backend/tests/test_audit_sqlite.py` (write → read round-trip; metrics counts equal JSONL counts on same fixture data; backfill idempotency)

## Scope — modify

- `backend/app/core/config.py` (one setting)
- `backend/app/application/container.py` (adapter selection only)
- `.env.example`

## Do not touch

- `backend/app/infrastructure/audit/jsonl.py` (read-only in this task)
- Safety pipeline, retrieval, generation, verifier
- Any API route file (metrics endpoint itself)
- `backend/app/agents/`, `backend/app/services/advisory/`
- `capstone/`, `paper/`, `dataset_release/`, `frontend/`

## Rollback

1. Config rollback: `AUDIT_BACKEND=jsonl` → restart. Instant, no code revert.
2. Commit revert: `git revert <commit>` (bounded to this task's files).

## Verification gate (stop/go)

1. `uv run pytest backend/tests/test_audit_sqlite.py -v` — green.
2. With `AUDIT_BACKEND=sqlite`: run 3 live queries (1 safe, 1 banned-chemical, 1 off-topic) → rows appear in SQLite with correct categories.
3. `GET /api/safety/metrics` returns identical counts under sqlite vs jsonl (same fixture dataset, run both, diff).
4. Backfill: point at the existing audit log → record count matches JSONL line count; run again → no duplicates.
5. `AUDIT_BACKEND=jsonl` restored → everything behaves as before (demo default).

Gate fails ⇒ STOP and report exact output. Do not "fix" by changing the metrics endpoint.

## Definition of done

Per AGENTS.md §6 + task handbook: runs locally, `.env.example` updated, commit message lists open questions, completion line in `docs/refactor/PROJECT_HANDOFF.md`.

## Open questions

- Whether history/audit read endpoints exist today and their exact queries (resolved during `Read first`).
- Whether `request_id` correlation should be backfilled from old records (no — leave null, T0-04+ only).