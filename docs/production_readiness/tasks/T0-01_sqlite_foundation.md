# T0-01 — SQLite Foundation (DB Bootstrap + Migrations)

- **Status:** DONE (2026-08-17)
- **Tier:** 0 (demo-safe, pre-capstone)
- **Depends on:** nothing
- **Blocks:** T0-02, T0-03
- **Amendment:** none required

## Goal

Create the shared SQLite storage foundation: a bootstrap module that opens one database file with WAL mode, runs idempotent schema migrations, and hands out safe connections. This task introduces **no application behavior change** — nothing reads or writes the DB yet. It only exists so T0-02 (audit) and T0-03 (sessions) can swap adapters later.

## Read first

- `backend/app/ports/` — confirm the exact port names/signatures for the audit sink and session store (the README calls them `AuditSink` / `SessionStore`; verify in code, they are the consumers of this DB).
- `backend/app/infrastructure/audit/jsonl.py` and `backend/app/infrastructure/sessions/memory.py` — these are the adapters that will later move to SQLite; note their method sets so the DB schema can serve them.
- `backend/app/core/config.py` — how settings are declared (pydantic-settings), and how the audit path is resolved (`resolved_audit_log_path`) so the DB path resolves the same way.
- `backend/app/application/container.py` — where adapters are wired (future injection point; do not change it in this task).

## Invariants (do not break)

- Existing audit (JSONL) and session (memory) behavior is untouched.
- No new business tables in this task — only the migrations runner and the schema-versions table.
- The DB path must default inside the repo (`backend/data/`) and be gitignored.
- Stdlib `sqlite3` preferred. Only use `aiosqlite` if the target ports turn out to be async — then it is a new dependency and requires an internet version check (AGENTS.md §2.7) + `uv add`.

## Design

- Module: `backend/app/infrastructure/storage/__init__.py` + `sqlite.py`.
- `open_db(path)` → connection with:
  - `PRAGMA journal_mode=WAL`
  - `PRAGMA foreign_keys=ON`
  - `PRAGMA busy_timeout=5000`
  - `check_same_thread=False` if connections are shared; otherwise connection-per-call via a context manager (`db_connect()`).
- `schema_migrations(version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL)` table.
- Migration runner: ordered list of `(version, sql)`; applies each missing version in one transaction; idempotent (re-running applies nothing).
- Config (in `backend/app/core/config.py`, with `.env.example` entry + one-line comment): `SQLITE_DB_PATH` — default `backend/data/krishokchat.db` resolved relative to project root the same way `resolved_audit_log_path` is.
- Ensure `backend/data/` is in `.gitignore` (check first; add only if missing).

## Scope — create

- `backend/app/infrastructure/storage/__init__.py`
- `backend/app/infrastructure/storage/sqlite.py`
- `backend/tests/test_storage_sqlite.py` (migration applies once; re-run applies nothing; WAL on; path override honored; gitignore contains `backend/data/`)

## Scope — modify

- `backend/app/core/config.py` (one new setting)
- `.env.example` (one line, commented)
- `.gitignore` (only if `backend/data/` missing)

## Do not touch

- `backend/app/agents/`, `backend/app/services/advisory/` (legacy shims)
- `infrastructure/audit/jsonl.py`, `infrastructure/sessions/memory.py`
- `application/container.py`, `app/main.py`
- `capstone/`, `paper/`, `dataset_release/`, `frontend/`

## Rollback

Single bounded commit; revert it: `git revert <commit>`. Nothing consumes the DB yet, so there is no config rollback.

## Verification gate (stop/go)

1. `uv run python -m compileall -q backend/app` — clean.
2. `uv run python -c "from app.main import app; print(app.title)"` — imports clean.
3. `uv run pytest backend/tests/test_storage_sqlite.py -v` — all green.
4. Manual: run a tiny script that opens the DB, applies migrations twice, asserts the second run applies nothing; assert WAL files appear beside the DB.
5. Full smoke: start backend, hit `/api/safety/metrics` and `/api/qa` (stub or real LLM) — identical behavior to before.

Gate fails ⇒ STOP and report exact output.

## Definition of done

Runs locally; locked stack respected; new dep (if any) version confirmed via internet search and noted in the commit message; `.env.example` updated; commit message lists open questions; completion line added to `docs/refactor/PROJECT_HANDOFF.md`.

## Open questions

- Async vs sync port signatures (resolved during `Read first`).
- Keep DB inside repo or under `backend/data/` configurable path — resolved by the config default above.