# Production Readiness — Task Execution Handbook

This folder holds agent-executable implementation briefs. One agent executes one task document, cold, in isolation. Read this handbook before touching code.

## Mandatory pre-reads (every task, no exceptions)

1. Root `AGENTS.md` — hard rules, locked stack, definition of done.
2. `docs/refactor/PROJECT_HANDOFF.md` — persistent implementation memory.
3. `docs/refactor/ARCHITECTURE.md` — port/contract boundaries.
4. The task's own `Read first` section — files you must read before editing.

## Global rules (apply to every task)

| Rule | Detail |
|---|---|
| **Additive-only** | New modules live beside old ones. Never delete or rewrite existing behavior in the same task. |
| **Config switch, safe default** | Every new path is off or equals current behavior until its gate passes. Default = today's behavior. |
| **Isolation** | Touch only the files listed in your task's scope. One concern per task — never two. |
| **Stop/go gate** | Run the exact gate commands. Any failure ⇒ STOP and report; do not fix by widening scope. |
| **Do-not-touch** | `backend/app/agents/` and `backend/app/services/advisory/` (legacy shims — AGENTS.md §5.1); safety fail-closed invariants; port signatures; the demo cache lane; `capstone/`, `paper/`, `dataset_release/`. |
| **Ports are contracts** | Verify the exact port names/signatures by reading `backend/app/ports/` — task docs use names as found in the README but you must confirm against code. |
| **New dependencies** | Search the internet for the current stable version (AGENTS.md §2.7) and record version + source in the commit message. Backend deps via `uv add`, frontend via `pnpm add`. |
| **Env vars** | Every new var goes in `.env.example` with a one-line comment, and in `backend/app/core/config.py` with a sane default. |
| **Backend must import clean** | `uv run python -m compileall -q app` and `uv run python -c "from app.main import app; print(app.title)"` must pass after every edit. |
| **Demo safety** | With `DEMO_MODE=true` and with no signed-in user, every existing route must behave exactly as before (AGENTS.md §2.1). |
| **Evidence** | Record exact commands and outputs in the commit message; update `docs/refactor/PROJECT_HANDOFF.md` with a one-line completion note. |

## Dependency graph

```
Phase A (parallel, no deps):
  T0-01 (SQLite foundation)
  T0-04 (request IDs + logging)
  T0-08 (pytest + CI)

Phase B:
  T0-02 ← T0-01
  T0-03 ← T0-01
  T0-05 ← T0-04

Phase C:
  T0-06 (failover; benefits from T0-05 telemetry, not required)
  T0-07 (versioning/keys/rate limits; independent)

Tier 1 — each requires an approved amendment BEFORE code (see roadmap §5):
  T1-01 ← T0-01 + T0-07
  T1-02, T1-03, T1-04, T1-05 — independent of each other, blocked on amendments
```

## Claiming and executing a task

1. Pick a task whose dependencies have passing gates (task doc `Depends on` section).
2. Read the four mandatory pre-reads + the task's `Read first` list.
3. Check the task's `Amendment` line: if it says REQUIRED, the task is BLOCKED until the researcher approves the amendment file.
4. Implement exactly the listed scope. Nothing else.
5. Run the gate. Gate fails ⇒ stop, report the exact command + output, do not retry creatively.
6. Gate passes ⇒ commit (bounded commit message, list open questions), update `.env.example`, add a completion line to `docs/refactor/PROJECT_HANDOFF.md`.

## Rollback guarantee per task

Every task doc lists its rollback as one of:
- **Config rollback** — set `<SWITCH>=<old value>` and restart; no code revert needed.
- **Commit revert** — `git revert <commit>`; the commit is bounded to that task's files.

If a rollback ever requires touching a file outside the task's scope list, the task doc is wrong — stop and report that too.

## Recording blockers

Blockers go in `docs/refactor/PROJECT_HANDOFF.md` (append-only) with: task ID, what failed, exact command + output, and what should happen next. Never overwrite prior entries.
