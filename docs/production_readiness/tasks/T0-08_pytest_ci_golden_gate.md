# T0-08 — pytest Declaration + CI + Golden Regression Gate

- **Status:** NOT STARTED
- **Tier:** 0 (demo-safe, pre-capstone)
- **Depends on:** nothing (tests may be written against current behavior)
- **Blocks:** nothing
- **Amendment:** none required

## Goal

Make the existing ad-hoc regression work (19/19 smoke suite and similar scripts in `backend/scripts/` and `backend/tests/`) a declared, CI-enforced gate: add pytest to dev dependencies, convert the highest-value smoke checks into pytest functions (keeping the scripts), add a GitHub Actions workflow (backend tests + frontend `pnpm build` + a golden-invariant replay), and write a mechanical golden replay that asserts **invariants only** — never fabricated scores.

## Read first

- `backend/pyproject.toml` — current deps (no dev group exists; add one).
- `backend/scripts/` — existing smoke/regression scripts (the 19/19 suite referenced in planning docs) to convert/reuse.
- `backend/tests/` — what exists already.
- `dataset_release/benchmark/golden_stats_v1.json` — 46 items, 2 evaluators, `pending_scores` (read-only; do NOT modify).
- `dataset_release/safety/safety_refusal_t3.jsonl` — the T3 refusal records (12 categories) usable as red-team fixtures later; this task only replays the golden set.
- `frontend/package.json` — build/typecheck scripts for the CI frontend job.

## Invariants (do not break)

- **Never assert human-evaluated scores** (the golden items' `pending_scores` are unanswered — CI must not invent them). The golden gate asserts mechanical invariants only:
  - 12/12 unanswerable golden items produce the safe/canned refusal path (no normal answer)
  - verifier flags appear for the 6/45 items the existing eval marked as flag-worthy (verify the actual count in the file; the number here is from earlier analysis — confirm against the JSON)
  - no pipeline exception on any replay
- Scripts in `backend/scripts/` are kept, not deleted (some may become thin wrappers around test functions).
- CI must run offline-capable: golden replay uses the stub LLM lane (no API keys in CI).
- No secrets in CI config; no fabrication; no `.env` needed to run the backend test suite.

## Design

- `uv add --dev pytest pytest-asyncio httpx` (versions confirmed via internet search per AGENTS.md §2.7; record version + source in commit).
- `backend/tests/` gains: converted smoke tests + `test_golden_invariants.py`.
- `backend/scripts/replay_golden.py`:
  - loads `golden_stats_v1.json`, replays each item through the pipeline with the stub LLM lane,
  - asserts the invariant list above,
  - prints a machine-readable summary; exits non-zero on any invariant failure.
- `.github/workflows/ci.yml`:
  - `backend` job: checkout → `uv sync --dev` → `uv run pytest backend/tests` → `uv run python -m compileall -q backend/app`
  - `frontend` job: checkout → `pnpm install` → `pnpm build` (the passing gate today; lint optional and time-boxed)
  - `golden` job: `uv run python backend/scripts/replay_golden.py --assert-invariants`
- All three jobs independent (parallel) — one failing job must not block the others' results.

## Scope — create

- `.github/workflows/ci.yml`
- `backend/scripts/replay_golden.py`
- `backend/tests/test_golden_invariants.py`
- Converted test files (from the smoke scripts)

## Scope — modify

- `backend/pyproject.toml` (dev group only)
- `frontend/package.json` — only if a `build` script is missing (verify first; do not touch otherwise)
- No runtime code changes

## Do not touch

- Any production module, route, or adapter
- `dataset_release/` contents (read-only)
- `backend/scripts/` existing scripts (they stay; only add new files)
- `capstone/`, `paper/`, `frontend/` source

## Rollback

Commit revert (`git revert <commit>`). CI is additive; no runtime impact.

## Verification gate (stop/go)

1. `uv run pytest backend/tests -v` — green locally (new + existing tests).
2. `uv run python backend/scripts/replay_golden.py --assert-invariants` — passes locally.
3. `pnpm build` — green (unchanged from today).
4. CI YAML is valid (parse with a YAML linter or `actionlint` if available; note the tool in the commit).
5. Confirmed the golden replay uses the stub lane — no network call, no key in CI.

Gate fails ⇒ STOP and report exact output.

## Definition of done

Per AGENTS.md §6 + task handbook. Commit message lists versions + sources of new dev deps and open questions; completion line in `docs/refactor/PROJECT_HANDOFF.md`.

## Open questions

- Exact number of flag-worthy golden items (read the JSON; do not trust the count above blindly).
- Whether any smoke script depends on a live LLM (if so, it is skipped in CI via a `LIVE_LLM` marker — do not delete it).