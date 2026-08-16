# T0-03 — Sessions → SQLite Adapter

- **Status:** NOT STARTED
- **Tier:** 0 (demo-safe, pre-capstone)
- **Depends on:** T0-01 (SQLite foundation, gate passed)
- **Blocks:** nothing
- **Amendment:** none required

## Goal

Add a SQLite-backed implementation of the session store port (`infrastructure/sessions/sqlite.py`) alongside the in-memory adapter, selectable via `SESSION_BACKEND=memory|sqlite` (**default `memory`**). Sessions survive backend restarts. TTL semantics must match the current adapter exactly.

## Read first

- `backend/app/ports/` — exact session port name + methods (the README calls it `SessionStore` with `append`; verify in code).
- `backend/app/infrastructure/sessions/memory.py` — current semantics: keys, TTL source, what is stored per session.
- `backend/app/infrastructure/storage/sqlite.py` (T0-01) — connection helper + migration runner.
- `backend/app/application/container.py` — session adapter selection point.
- `backend/app/core/config.py` — existing session TTL setting name (e.g. `SESSION_TTL_MINUTES` or similar; reuse it, do not duplicate).

## Invariants (do not break)

- Memory adapter unchanged; it stays the default.
- All endpoints that use sessions behave identically under both backends (chat history, speech/history routes if they use sessions).
- TTL expiry behavior identical (same setting, same semantics).
- No background threads/processes (task handbook: single-process rule). Cleanup is lazy: purge expired rows on each write and on startup.

## Design

- Table `sessions` (migration v3 in the T0-01 runner):
  - `session_id TEXT PRIMARY KEY`
  - `data_json TEXT NOT NULL`
  - `created_at TEXT NOT NULL`
  - `last_active_at TEXT NOT NULL`
  - index on `last_active_at` (cheap lazy purge: `DELETE FROM sessions WHERE last_active_at < ?` with `now - ttl` on each write, bounded to a few rows)
- Adapter implements the same methods as the memory adapter (get / set / append / clear / anything else the port declares) with identical semantics, including TTL checks on read.
- Wiring: `application/container.py` selects by `SESSION_BACKEND`; comment marks the switch.
- `.env.example`: `SESSION_BACKEND=memory  # memory | sqlite (adapter selected at container build time)`

## Scope — create

- `backend/app/infrastructure/sessions/sqlite.py`
- `backend/tests/test_session_sqlite.py` (set/get round-trip; append preserves history; TTL expiry on read; restart persistence — simulate by reopening the DB file)

## Scope — modify

- `backend/app/core/config.py` (one setting)
- `backend/app/application/container.py` (adapter selection only)
- `.env.example`

## Do not touch

- `backend/app/infrastructure/sessions/memory.py` (read-only here)
- Chat/QA pipeline and all route files
- `backend/app/agents/`, `backend/app/services/advisory/`
- `capstone/`, `paper/`, `dataset_release/`, `frontend/`

## Rollback

1. Config rollback: `SESSION_BACKEND=memory` → restart. Instant.
2. Commit revert: `git revert <commit>`.

## Verification gate (stop/go)

1. `uv run pytest backend/tests/test_session_sqlite.py -v` — green.
2. With `SESSION_BACKEND=sqlite`: start backend, create a session via chat, **stop the server, start it again** → session still readable, history intact.
3. TTL: insert a row with `last_active_at` older than TTL → read returns miss (same as memory adapter's expiry behavior).
4. `SESSION_BACKEND=memory` restored → demo behaves exactly as before.
5. Full smoke: QA + history endpoints with both backends return identical responses.

Gate fails ⇒ STOP and report exact output.

## Definition of done

Per AGENTS.md §6 + task handbook. `.env.example` updated; commit message notes open questions; completion line in `docs/refactor/PROJECT_HANDOFF.md`.

## Open questions

- Exact port method names/semantics (resolved during `Read first`).
- Whether any route writes sessions directly instead of through the port (check during `Read first`; if yes, that route is out of scope — flag it).