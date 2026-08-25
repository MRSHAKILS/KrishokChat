# 08 — Weather Data Sourcing (BMD / BAMIS / RIMES)

**Status:** RESEARCH / SOURCING DOC — no code changes. Answers the outstanding
handoff item: *"replace the PR1 sample weather snapshot with real rows."*
**Date:** 2026-08-25
**Companion:** `07_ARCHITECTURE_REFINEMENT_PLAN.md` (§Grounding Packs),
`docs/production_readiness/tasks/PR1_late_blight_weather_alert.md`.

---

## 0. What PR1 actually needs

The late-blight rule (`backend/app/domain/late_blight.py`) consumes a
**district → list of daily records** shape with exactly four fields:

| Field | Unit | Used for |
|---|---|---|
| date | ISO `YYYY-MM-DD` | Smith-period window + season gate |
| temp_min / temp_max | °C | favourable-day test |
| humidity | % RH | favourable-day test |
| rainfall | mm | supporting signal |

So we do **not** need a live weather platform. We need a **repeatable daily
snapshot** of 4 variables for the potato districts (Munshiganj, Rangpur,
Bogura, Comilla, Jashore, Dinajpur, Rajshahi, Joypurhat as a first set), fetched
by an **offline script**, committed/stored as a dated JSON artifact, and read by
the existing `infrastructure/weather/snapshot.py` loader. That respects
AGENTS.md hard rule 2 (no live scraping at request time) exactly as the
crop-calendar artifact does.

---

## 1. The four viable routes, ranked

### Route A — RIMES upazila forecast API (fastest, best fit) ✅ recommended first
`http://api.bdservers.site/` — Regional Integrated Multi-Hazard Early Warning
System, the same pipeline that feeds BAMIS. Public, documented, no key seen.

- Endpoint shape: `/upazila_forecast_recent?SOURCE=BMDWRF&PARAM=temp&PARAM=rh&PARAM=rf&PCODE=<ADM3_PCODE>`
- Multi-day: `/upazila_forecast_steps_recent?SOURCE=BMDWRF&PCODE=...` (first 4 days, all steps)
- Historical by run date: `/upazila_forecast_date?...&FDATE=YYYYMMDD`
- Sources available: `BMDWRF`, `ECMWF`, `RIMESWRF`
- Parameters we need are all present: `rf` (mm), `temp` (°C), `rh` (%), plus
  bonus `smois` (soil moisture), `tempdew`, `windspd`, `cldcvr`
- Geography: **upazila-level** via `ADM3_PCODE` from the BBS shapefile — finer
  than our current district granularity, and it matches the farm-profile
  `upazila` field we already collect (P1). That is a real upgrade, not just a
  data swap.

**Why this is the right first move:** upazila resolution + the exact three
variables + a date-addressable historical endpoint means one script produces
both the live snapshot and a backfill for validating the Smith-period rule
against past outbreaks. **Caveat to verify before relying on it:** it serves
*forecast* output (WRF), not station observations, and it is HTTP (not HTTPS) —
so fetch it in the offline job, never from the browser, and record
`source: BMDWRF` + run date in the artifact provenance.

**Action:** write `scripts/fetch_weather_snapshot.py` that pulls N districts'
upazila codes, normalizes to the `DailyWeather` shape, and writes
`ml_assets/weather/snapshot_<YYYY-MM-DD>.json` with a provenance block. Drop
`is_sample`.

### Route B — BMD AIS national dashboard (real observations, 225 AWS)
`http://ais.bmd.gov.bd:48080/` — built under the World Bank BWCSRP project,
aggregates **225 Automatic Weather Stations** plus DAE and BWDB feeds. The site
exposes an `api_manualdownload` surface.

- **Value:** these are *measured observations*, which is what a disease model
  should ideally be validated against.
- **Blocker:** the site states *"information provided is for non-commercial use
  only."* Fine for research/paper/demo, **not** fine for a commercial tier
  without written permission. Also self-described as "still needed further
  development."
- **Action:** use for **rule validation and the paper**, cite explicitly, and
  request written permission before any commercial framing.

### Route C — BAMIS district agromet bulletins (the authoritative advisory voice)
`https://www.bamis.gov.bd/` — DAE, publishes **64-district agromet advisories
twice weekly** plus a national weekly, and — critically — pre-built
**crop-weather, pest-weather and disease-weather calendars** and 487-upazila
agromet databases.

This is not primarily a numeric feed; it is the **institutional advisory
grounding** that makes our output defensible: BAMIS already publishes exact
doses with registered trade names. Two distinct uses:

1. **Corpus ingestion** (highest value): pull the district bulletins + pest/
   disease-weather calendars into the knowledge corpus as new nodes with full
   provenance. This directly feeds the §Grounding Pack path in doc 07 and grows
   the node count with *official* text rather than scraped blog content.
2. **Cross-check**: when our rule fires for Munshiganj, compare against the
   current Munshiganj bulletin. Agreement is a strong credibility claim for the
   paper; disagreement is a bug we want to find before a farmer does.

**Note:** the BAMIS project DPP expired 31 Dec 2024 per their own banner —
confirm the portal is still being updated before treating it as live.

### Route D — Official data request / paid purchase (do this in parallel)
- `https://dataportal.bmd.gov.bd/` — BMD's **Online Data Purchase** portal for
  formal historical station data.
- Institutional letter to the **DAE Agromet cell / BAMIS project office** and
  BMD requesting research access, citing the capstone and naming the exact
  variables and districts.

**Why bother if Route A is free:** a signed data-sharing acknowledgement from
DAE/BMD is worth more in a funding conversation than the data itself. It turns
"we scraped a public endpoint" into "we have an institutional data
relationship." Start the paperwork early; it moves slowly.

---

## 2. Recommended sequence

1. **Now:** Route A script → real upazila snapshot → drop `is_sample`. Bounded,
   reversible, unblocks PR1 immediately.
2. **Next:** Route C ingestion of BAMIS disease-weather calendars + district
   bulletins into the corpus (also serves doc 07's mapping-first ladder).
3. **Parallel, slow lane:** Route D letters to DAE Agromet + BMD.
4. **For the paper:** Route B observations to validate the Smith-period rule on
   historical seasons; cite non-commercial terms honestly.

## 3. Non-negotiables when this lands

- Fetch happens **offline** in a script, never in a request path.
- Every artifact carries provenance: source ID, model run (`BMDWRF`), fetch
  timestamp, endpoint, and geography codes.
- The loader **fails open** to "weather unavailable" — never fabricates a value,
  never falls back to a hardcoded number (the soil-honesty lesson).
- A forecast-derived risk alert must be labelled as forecast-derived in the
  farmer-facing UI, and must stay human-in-the-loop before broadcast (PR1
  already enforces this).
- Non-commercial-licensed data must not silently power a paid tier.
