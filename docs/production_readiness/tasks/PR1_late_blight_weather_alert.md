# PR1 — Weather-Triggered Potato Late-Blight Risk Alert (admin lane)

- **Status:** DONE (2026-08-25)
- **Spine step:** §10 flagship spine step 3 (`production/future_plan/00_SCOPE_OUTLINE.md`)
- **Novelty served:** PR1 competitor gap ("Plantix's promised outbreak prediction is
  aspirational"); supports the GEOPOTOTO-proven "preventive spray only when needed" story.
- **Depends on:** G0–G9 broadcast lane (shipped — announcements + bell + banners).
- **Blocks:** nothing.
- **Amendment:** none — additive admin endpoint + UI; no new hard-rule area.

## Goal

A deterministic weather-risk rule over an **offline, operator-maintained snapshot**
(never live-fetched at request time — AGENTS.md rule 2) that drafts a late-blight
advisory for high-risk districts, reviewed and published by an admin through the
EXISTING announcements composer (human-in-the-loop broadcast; amendment 02 audited).

Flow: snapshot JSON on disk → rule evaluates per-district risk →
`GET /api/admin/advisory/late-blight-risk` (require_admin, fail-closed) →
admin console "আবহাওয়া ঝুঁকি" card → one click prefills the composer → publish
via the existing announcement lane → farmers see bell row + urgent banner.

## Data honesty (AGENTS.md §2.5) and rule grounding

- The shipped snapshot is **clearly marked `is_sample: true`** with placeholder
  values (schema-valid, plausible January ranges). It exists so the demo and tests
  can run; it must be replaced with real BMD/BAMIS data by the researcher before
  any real broadcast. The endpoint surfaces `sample: true` so the UI can badge it.
- Risk rule = documented approximation of the classic **Smith period** (blight
  favourability: two consecutive days of TMIN ≥ 10°C with high humidity) using
  daily aggregates: a day is *favourable* when `tmin_c ≥ 10.0 AND rh_pct ≥ 85`
  (mean-RH proxy for the ≥90%-for-11h criterion, which daily snapshots don't
  carry). ≥2 consecutive favourable days ending at the snapshot's latest date =
  **high**; 1 = **watch**; 0 = **low**. Thresholds documented here, nothing
  claimed as a calibrated BD model.
- Corpus grounding for the advisory TEXT: CABI nodes (`CABI_POTATO_344E9F_001`,
  `CABI_POTATO_42D248_001`) state late blight is severe in cold+humid weather —
  the drafted body cites this. The draft deliberately contains **no fungicide
  dose**: dose advice must flow through the grounded QA pipeline (F1-02) or 16123,
  not a broadcast template.

## Scope — create
- `backend/app/domain/late_blight.py` (pure rule + draft; no IO)
- `backend/app/infrastructure/weather/snapshot.py` (loader; missing file → None)
- `backend/ml_assets/weather/late_blight_snapshot.json` (SAMPLE, committed)
- `backend/tests/test_late_blight.py`
- frontend: risk card section in `/admin/announcements` + `adminLateBlightRisk` in `admin-api.ts`

## Scope — modify
- `backend/app/api/admin.py` (GET `/api/admin/advisory/late-blight-risk`)
- `backend/app/core/config.py` + `.env.example` (`WEATHER_SNAPSHOT_PATH`)
- `/admin/announcements` page (card + prefill)

## Do not touch
- QA pipeline, safety policy, verifier (F1-01/F1-02 lanes)
- Notification schemas/tables (reuse existing announcement draft fields verbatim)
- `dataset_release/`, `paper/`

## Invariants
- Anonymous/demo path unchanged (admin-only route; nothing loads at startup for
  non-admin requests — the snapshot is read per admin request, cheap JSON).
- Snapshot absent/invalid → endpoint returns a clear "no snapshot" payload
  (HTTP 200 with `available: false`), never a 500.
- Deterministic: same snapshot file → same risk output (no wall-clock input;
  the snapshot's own latest date drives seasonality).

## Verification gate (stop/go)
1. `uv run pytest tests/test_late_blight.py tests/test_admin_guard.py -v` (or the
   existing admin authz suite name) — green.
2. Full `tests/` suite — no regressions vs the F1-02 baseline.
3. `pnpm build` green; `/admin/announcements` renders the card (anonymous →
   auth-guarded page behavior unchanged).
4. Spot-check: sample snapshot yields a mix of high/watch/low districts; prefill
   produces a publishable draft (kind=disease_alert, crop=আলু, cited body).

## Rollback
`git revert` — additive files + one route + one UI section. No schema, no migration.

## Completion log (2026-08-25)

- Delivered: `backend/app/domain/late_blight.py` (pure rule + Bengali advisory
  draft — cites CABI corpus nodes, deliberately contains NO fungicide dose),
  `backend/app/infrastructure/weather/snapshot.py` (fail-open loader),
  committed SAMPLE snapshot `backend/ml_assets/weather/late_blight_snapshot.json`
  (8 major potato districts × 7 days, `is_sample: true`, engineered to show all
  three tiers: 5 high / 1 watch / 2 low),
  `GET /api/admin/advisory/late-blight-risk` in `admin.py` (require_admin,
  fail-closed; risk-ordered payload with per-district composer prefill),
  `WEATHER_SNAPSHOT_PATH` in config + `.env.example`.
- Frontend: `adminLateBlightRisk` in `admin-api.ts`; `/admin/announcements` now
  renders an "আবহাওয়া ঝুঁকি — আলুর লেট ব্লাইট" card (sample badge, rule
  explanation, per-district tier chips, favourable-day counts, out-of-season
  note) with one-click "কম্পোজারে ব্যবহার করুন" prefill of the existing
  composer (kind=disease_alert, crop=আলু, severity from tier, cta=/detect).
  Human-in-the-loop preserved: nothing publishes without the admin's explicit
  action through the audited announcements lane.
- Researcher actions outstanding: replace the sample snapshot with real
  BMD/BAMIS daily rows (same schema; set `is_sample: false` + a real
  `source_note`) before any real broadcast. Refresh cadence is manual —
  the app never fetches weather at request time (AGENTS.md rule 2).

### Verification evidence
1. `tests/test_late_blight.py` — 18 passed (rule tiering incl. broken-run and
   inclusive-threshold cases, seasonality boundaries, unordered rows; loader
   fail-open + malformed-row skip + committed-sample assertions; route 401
   anonymous / admin payload risk-ordered with all three tiers / missing
   snapshot → `available: false`, HTTP 200).
2. Full `tests/` suite — **376 passed, 7 skipped, 2 failed** (the two
   documented pre-existing environmental failures only).
3. Golden replay — 50/50 invariants PASS, counts unchanged.
4. `pnpm build` green (24 routes incl. the updated admin page).
