# T1-05 — Safety Depth (Multi-Turn Context, Red-Team CI, Review Lane)

- **Status:** BLOCKED — amendment review required (see below)
- **Tier:** 1 (post-capstone)
- **Depends on:** T0-08 (CI + golden gate — the red-team suite plugs into it), T0-01/T0-02 (review lane storage)
- **Blocks:** nothing
- **Amendment:** REVIEW REQUIRED — the review lane stores verifier-flagged advisories for human review (a small new data surface, default-off). No hard-rule change expected; the researcher must approve that default-off design and the multi-turn context window size.

## Goal

Close the three admitted safety gaps: (1) **multi-turn safety context** — the classifier sees the last N turns so a rephrased banned query in turn 2 cannot slip through; (2) **red-team CI** — a replay suite over the adversarial `dataset_release/safety/` records (12 categories, 9 patterns, 6 dialects, 144 over-refusal tests) asserting refusal invariants on every PR; (3) **review lane** — verifier-flagged advisories land in a default-off queue a human can triage, which is itself a B2B trust feature.

## Read first

- `backend/app/application/` — the safety classifier call site and the verifier; how turns are passed today (single-turn).
- `backend/app/infrastructure/audit/` — where flagged records could attach (or a new table via the T0-01 runner).
- `dataset_release/safety/` — `safety_refusal_t3.jsonl` (3,216 T3 records incl. 144 over-refusal tests) + `safety_requery_t4.jsonl` (16,896) — READ-ONLY fixtures.
- `backend/tests/` + `backend/scripts/replay_golden.py` (T0-08) — where the red-team suite plugs in.
- `backend/app/core/config.py` — settings style.

## Invariants (do not break)

- The single-turn behavior is the default; multi-turn context is additive (`SAFETY_CONTEXT_TURNS=1` default = today).
- Canned responses (16123 redirect, calm tone, supportive self-harm framing) are unchanged.
- Review lane is **off by default** (`REVIEW_QUEUE_ENABLED=false`) — flagging behavior unchanged until enabled.
- Red-team suite asserts the same invariants the safety dataset encodes: refusal for banned/self-harm categories, normal answer for safe categories, no over-refusal regressions beyond the dataset's own expected set.
- Dataset files are fixtures only — never modified, never "improved" by the pipeline.

## Design

- **Multi-turn context:** at the classifier call site, pass the last `SAFETY_CONTEXT_TURNS` (default 1) user turns + assistant canned responses (when applicable) as context, with explicit instruction that earlier turns may not weaken the current-turn classification. Timestamps/order preserved. Session data comes from the session store (T0-03 adapter).
- **Red-team CI:** `backend/scripts/replay_safety_redteam.py` — samples (or uses, with `--full`) the T3 refusal records through the stub LLM lane; asserts: banned/self-harm → refusal path; safe_agri → normal path; over-refusal fixtures → the dataset's expected behavior (allowed to refuse per dataset labels — assert against the record's `expected_action` field, never hardcode). Wired as a CI job in the T0-08 workflow; local runnable with `--limit N`.
- **Review lane:** migration — `flagged_advisories(id, request_id, session_id, query, answer, verifier_flags_json, status, created_at)` (status: `open` → `resolved`/`dismissed`); the verifier writes to it only when `REVIEW_QUEUE_ENABLED=true`; `GET /api/v1/review/queue` (auth-gated by T0-07 keys, read-only list, default 403 when disabled). No UI in this task.

## Scope — create

- `backend/scripts/replay_safety_redteam.py`
- `backend/tests/test_safety_multi_turn.py` (rephrase attempt in turn 2 still refused; safe turn after refused turn still answered)
- `backend/tests/test_review_lane.py` (flag lands only when enabled; queue endpoint 403 when disabled)
- migration (flagged_advisories) via the T0-01 runner

## Scope — modify

- safety classifier call site (context window, additive)
- verifier (write to lane when enabled)
- `backend/app/core/config.py` (+ `SAFETY_CONTEXT_TURNS`, `REVIEW_QUEUE_ENABLED`), `.env.example`
- CI workflow (T0-08) — red-team job

## Do not touch

- Canned response texts, 16123 messaging, fail-closed paths
- `dataset_release/` contents
- `backend/app/agents/`, `backend/app/services/advisory/`
- `capstone/`, `paper/`, `frontend/`

## Rollback

1. Settings rollback: `SAFETY_CONTEXT_TURNS=1`, `REVIEW_QUEUE_ENABLED=false` → restart → today's behavior.
2. Commit revert (bounded).

## Verification gate (stop/go)

1. `uv run pytest backend/tests/test_safety_multi_turn.py backend/tests/test_review_lane.py -v` — green.
2. Multi-turn: banned query in turn 1 refused; rephrased in turn 2 → still refused; safe follow-up answered.
3. Red-team: `uv run python backend/scripts/replay_safety_redteam.py --limit 50` — all invariants hold.
4. Review lane enabled: verifier-flagged advisory appears in queue with flags; disabled: queue returns 403, no rows written.
5. Full demo smoke with defaults — identical to pre-change.

Gate fails ⇒ STOP and report exact output.

## Definition of done

Per AGENTS.md §6 + task handbook. Amendment note approved (context window + default-off design); commit message lists open questions; completion line in `docs/refactor/PROJECT_HANDOFF.md`.

## Open questions

- Context window size (proposal: 3 turns; researcher approves).
- Who may access the review queue endpoint and with which key role (default: admin only, wired in T1-01).