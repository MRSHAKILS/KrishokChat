# P1+P2 — Farm Profile + Stage-Aware Advice (extensible agronomy framework)

- **Status:** DONE (2026-08-25) — backend + API + frontend + tests wired.
- **Spine step:** §10 flagship spine step 4 (`production/future_plan/00_SCOPE_OUTLINE.md`)
- **Depends on:** Supabase auth lane (approved, non-gating); G0–G9 account surface.
- **Blocks:** P3/P4 (history-aware, reminders), PR1 audience targeting.
- **Amendment:** none — additive account + QA-context capability, no gating.

## Goal

**P1** — a signed-in farmer can store a minimal farm profile (primary crop,
sowing date, upazila, optional note) and see the crop's **current growth stage**
computed from the sowing date. **P2** — that stage flows into the QA pipeline as
optional `farmer_context` so retrieval + generation become stage-aware.
Anonymous/DEMO_MODE behavior is byte-identical (hard rule 1): the fields are
optional, the pipeline ignores them when absent, and profile storage lives on
the already-approved Supabase lane (unconfigured → honest "unavailable", never
an error, never a gate).

## The extensibility requirement (researcher directive, 2026-08-25)

Crop-stage data is scarce today; the framework must absorb a richer dataset
later **without code changes**. Design:

```
data in                          offline build (deterministic)         runtime
──────────────────────────      ───────────────────────────────      ─────────────────────
corpus nodes (auto-extract)  ─┐
                              ├→ scripts/build_crop_calendars.py  →  ml_assets/agronomy/
curated_calendars_v1.json   ─┘   (extract + merge + validate +         crop_calendars_v1.json
(data file, researcher/human      sort; committed, reviewable diff)    (loaded from disk,
 edits to add crops; every                                              missing → feature inert)
 entry carries source+grounding)
```

- **Adding a crop later = edit the curated JSON + re-run the builder.** No
  Python changes. The calculator, API, and UI are crop-agnostic and read the
  supported-crop list from the artifact.
- Every stage entry carries `source` (citation) and `grounding`
  (`corpus-extracted` | `curated-approximation`) so downstream surfaces can
  badge approximations honestly (AGENTS.md §2.5 — no invented confidence).
- The builder's corpus extractor is deliberately generic: it scans for
  harvest/maturity windows (`বপন/রোপণের N দিন পর সংগ্রহ/পরিপক্ব`) and records
  hits with citations; today that yields potato (BARC 80–90 DAP). As the
  corpus grows, re-running the builder widens grounded coverage automatically.

## Scope — create
- `supabase/migrations/004_farm_profiles.sql` (idempotent; RLS: owner-only;
  no gating semantics; service-role writes from the backend)
- `backend/ml_assets/agronomy/curated_calendars_v1.json` (human-editable seed)
- `backend/ml_assets/agronomy/crop_calendars_v1.json` (committed artifact)
- `backend/scripts/build_crop_calendars.py` (offline builder)
- `backend/app/domain/crop_calendar.py` (pure generic calculator)
- `backend/app/infrastructure/agronomy/calendar_store.py` (fail-open loader)
- `backend/app/application/farm_profile.py` (service; PostgREST store)
- `backend/tests/test_crop_calendar.py`, `backend/tests/test_farm_profile.py`

## Scope — modify
- `backend/app/domain/contracts.py` (`QueryContext.farmer_context`)
- `backend/app/application/qa_pipeline.py` + `api/qa.py` (`_input` threading)
- `backend/app/application/generation.py` (prompt line: কৃষকের ফসল পর্যায়)
- `backend/app/api/auth.py` (GET/PUT `/api/account/farm-profile`)
- `backend/app/core/config.py` + `.env.example` (`CROP_CALENDARS_PATH`)
- frontend: `/account` (profile form + stage card), chat payload auto-attach
  (`frontend/src/lib/api.ts` + chat page)

## Do not touch
- Safety policy/verifier lanes (F1-01/F1-02), weather lane (PR1)
- Auth gating semantics, notifications schema, `dataset_release/`, `paper/`

## Invariants
- Anonymous QA requests behave exactly as today (no farmer_context field sent
  → identical prompts/retrieval — locked by a regression test).
- Stage computation is deterministic given (artifact, sowing date, today).
- Free-text `note` is PII-redacted on write (T1-04 redactor); upazila is a
  short location label, not PII.
- Unconfigured Supabase → farm-profile endpoints answer "unavailable" (503 on
  write, honest empty on read with `available: false`), matching the account
  route's philosophy.

## Verification gate (stop/go)
1. `uv run pytest tests/test_crop_calendar.py tests/test_farm_profile.py
   tests/test_pipeline.py -v` — green.
2. Full `tests/` suite — no regressions vs the PR1 baseline (376/7/2).
3. Golden replay 50/50 PASS (no farmer_context on golden items — unchanged).
4. `pnpm build` green; anonymous `/account` and `/chat` unchanged.
5. Extensibility check: add a dummy crop to a COPY of the curated file,
   re-run the builder against it, artifact + calculator pick it up (test-locked).

## Rollback
`git revert`; migration 004 is additive (drop table if ever needed). No
pipeline schema breaks — `farmer_context` is optional end-to-end.

## Verification record (2026-08-25)
- Targeted: `test_crop_calendar.py` + `test_farm_profile.py` 30 green;
  with `test_pipeline.py` 37 green.
- Full suite: **410 passed / 7 skipped / 0 failed** (PR1 baseline had 2
  pre-existing env failures — both fixed this session, see handoff:
  soil honesty fix + hermetic `/auth/me` contract test).
- Golden replay + QA smoke: PASS (anonymous lane untouched).
- Frontend: `pnpm build` green; farm-profile form + stage card on
  `/account`; chat auto-attach via `farmerContext` in `streamQuestion`.
- Migration 004 applied to the hosted project (verified via PostgREST
  schema probe: all six columns, PK, nullability match).
