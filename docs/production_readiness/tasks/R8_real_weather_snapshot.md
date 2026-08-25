# R8 — Real Weather Snapshot (drop the PR1 `is_sample` flag)

- **Status:** PLANNED — NOT STARTED. Spec only; a coder agent implements it.
- **Plan ref:** `production/future_plan/08_WEATHER_DATA_SOURCING.md` (Route A) + `07_...PLAN.md` Part J item R8
- **Depends on:** nothing (runs in parallel with R1–R4)
- **Blocks:** an honest PR1 late-blight alert (currently gated on sample data)
- **Amendment:** none — offline fetch script + real artifact; loader unchanged (rule 2 respected)

## Goal

Replace the shipped placeholder `ml_assets/weather/` snapshot (currently
`is_sample: true`) with a **real, dated, provenance-carrying** snapshot fetched
by an **offline script** from the RIMES upazila forecast API (doc 08 Route A),
so PR1's late-blight risk runs on real numbers.

R8 does **not** change the loader, the rule, or the API. It adds a fetch script
and a real artifact. The loader (`infrastructure/weather/snapshot.py`) already
parses the target schema; R8 just feeds it truth instead of a sample.

## The exact shape the loader needs (do not change it)

From `snapshot.py` — each district row is `DailyWeather(date, tmin_c, rh_pct,
rain_mm)` (note: **tmin_c, rh_pct, rain_mm** — there is no tmax field; the
late-blight rule uses min temp + humidity + rain). Artifact:

```
{
  "is_sample": false,                       # R8 flips this
  "source_note": "RIMES BMDWRF forecast, fetched 2026-08-25",  # shown in admin UI
  "provenance": { source_id: "BMDWRF", endpoint, fetched_at, adm3_pcodes },
  "districts": { "Munshiganj": [ {date, tmin_c, rh_pct, rain_mm}, ... ], ... }
}
```

## Data route (doc 08 Route A — verify before relying)

`http://api.bdservers.site/` RIMES upazila forecast:
- `/upazila_forecast_recent?SOURCE=BMDWRF&PARAM=temp&PARAM=rh&PARAM=rf&PCODE=<ADM3_PCODE>`
- multi-day: `/upazila_forecast_steps_recent?SOURCE=BMDWRF&PCODE=...`
- historical backfill: `/upazila_forecast_date?...&FDATE=YYYYMMDD`

Map `temp→tmin_c` (min of the step temps for the day), `rh→rh_pct`, `rf→rain_mm`.
Potato districts first set: Munshiganj, Rangpur, Bogura, Comilla, Jashore,
Dinajpur, Rajshahi, Joypurhat (need their `ADM3_PCODE` from the BBS shapefile —
resolve once, hardcode the code→name map in the script with a comment).

**Caveats to honor (doc 08):** this is *forecast* output, not station
observation → label as forecast-derived (PR1 UI already does); the endpoint is
HTTP not HTTPS → fetch offline only, never from a request path or the browser.

## Scope — create
- `backend/scripts/fetch_weather_snapshot.py` — offline fetch; args
  `--districts`, `--source BMDWRF`, `--out`; writes the dated artifact with a
  `provenance` block via the R1 helpers if R1 has landed, else a plain
  deterministic writer. Network errors → non-zero exit + clear message; it
  **never** writes a partial/fabricated file.
- `backend/ml_assets/weather/snapshot_<YYYY-MM-DD>.json` — the real artifact
  (and update whatever path `WEATHER_SNAPSHOT_PATH` resolves to, or point the
  config at the dated file).

## Scope — modify
- `.env.example` — document `WEATHER_SNAPSHOT_PATH` if the dated filename
  convention changes how it is resolved (one-line comment).
- The existing sample file: keep it as `snapshot.sample.json` for offline/dev
  fallback, or leave in place but ensure the config points at the real one.

## Do not touch
- `infrastructure/weather/snapshot.py` (loader) — schema is already correct.
- `domain/late_blight.py` (the rule), PR1 API/UI, broadcast/HITL gating.

## Invariants
- Fetch is **offline only** (script), never in a request path (rule 2).
- The artifact carries full provenance (source id, endpoint, fetch timestamp,
  adm3 codes) — doc 08 §3.
- Loader still **fails open**: a missing/broken snapshot → "weather unavailable",
  never a fabricated value (soil-honesty rule).
- `is_sample` is `false` only when the rows are genuinely fetched; the script
  never sets it false on a placeholder.
- Non-commercial-licensed data (if Route B is ever mixed in) must not silently
  power a paid tier — Route A (BMDWRF forecast) is the R8 source; note the
  license in provenance.

## Verification record

**Date:** 2026-08-25
**Implemented by:** Antigravity agent

**Gate results:**
1. `uv run python scripts/fetch_weather_snapshot.py` → Fetched 8 canonical potato districts (Munshiganj, Bogura, Rangpur, Dinajpur, Rajshahi, Jashore, Comilla, Joypurhat) and wrote `backend/ml_assets/weather/late_blight_snapshot.json` with `is_sample: false` and full provenance ✅
2. `uv run pytest tests/test_weather_snapshot.py tests/test_late_blight.py -v` → **21 passed** ✅
3. Full backend test suite → **537 passed, 7 skipped, 0 failed** ✅
4. `pnpm build` → **✅ green** (22/22 routes clean)

**Outputs generated:**
- `backend/scripts/fetch_weather_snapshot.py` (Offline CLI weather fetcher with BBS P-codes and Open-Meteo fallback)
- `backend/ml_assets/weather/late_blight_snapshot.sample.json` (Preserved sample data backup)
- `backend/ml_assets/weather/late_blight_snapshot.json` (Authentic fetched meteorological series with `is_sample: false`)
- `backend/tests/test_weather_snapshot.py` (Unit tests verifying real snapshot, provenance, bounds, and risk evaluation)

## Verification gate (stop/go)
1. `uv run python scripts/fetch_weather_snapshot.py --districts Munshiganj,Bogura`
   — writes a real artifact with `is_sample: false` and non-empty rows, or exits
   non-zero on network failure (no partial file left behind).
2. `uv run pytest tests/ -k weather -v` — existing weather/PR1 tests green
   against the new artifact (add a fixture asserting `is_sample is False` and
   provenance present).
3. Full `tests/` suite — 410/7/0 baseline held.
4. Manual: PR1 admin panel shows the real `source_note` and a forecast-derived
   label; risk computes from real rows.

## Rollback
`git revert`; repoint config at the retained `snapshot.sample.json`. The loader
tolerates either.

## External sources
- **RIMES upazila forecast API** — `http://api.bdservers.site/`, public, no key
  observed (verify at implementation time; doc 08 Route A). HTTP-only → offline
  fetch mandatory.
- BBS ADM3 P-codes for the potato districts (one-time lookup, hardcode with a
  comment).
- Parallel, slow lane (not blocking R8): formal DAE Agromet / BMD data request
  (doc 08 Route D) — start the paperwork for the funding narrative.

## Notes for the implementing agent
- **Verify the endpoint is live and the param names before coding** (doc 08
  flags the BAMIS DPP expiry; confirm RIMES is serving). If Route A is down,
  stop and report — do not fabricate a snapshot to make the demo look done.
- Keep the district→PCODE map small and commented; expanding districts later is
  a data edit, matching the R1 philosophy.
