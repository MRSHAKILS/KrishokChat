# 03 — Personalization & Proactive Advisory

**Parent:** `00_SCOPE_OUTLINE.md` (§4 personalization, §5 proactive; spine steps 3 & 4)
**Status:** PLANNING — no code changes.

---

## 1. Why this layer matters (evidence)

The strongest causal evidence in digital agri-advisory says the value lives in **personalization to conditions** and **timely push**, not generic Q&A:

- **PxD Odisha RCT** (13,675 farmers): personalization to weather/agro-conditions → up to **9.4% more yield**, **21% less severe crop loss**, ROI **$12–19 per $1** ([PxD Odisha](https://precisiondev.org/wp-content/uploads/2025/02/Odisha_RCT_02052025.pdf)).
- **ACI Fosholi (BD):** 9–16% rice yield gains with stage-keyed advice.
- **Timing matters:** 24h-ahead alerts beat 1h-ahead (PxD).

A pull-only chatbot only helps a farmer who *already knows* they have a problem. Personalization + push closes that gap.

---

## 2. Personalization scopes

| # | Scope | Farmer profit | Effort | Notes |
|---|---|---|---|---|
| **P1** | **Farm profile** (crop, upazila/agro-ecological zone, plot size, sowing date, soil) | The minimal input set that drives *all* downstream personalization | **Cheap** | PxD collects exactly this. Tie to existing (non-gating) Supabase auth. |
| **P2** | **Crop-calendar / growth-stage-aware advice** (advice keyed to sowing date + current stage) | Right advice at the right week | Cheap–Medium | BAMIS crop/pest/disease-weather calendars are pre-built. |
| P3 | **History-aware follow-ups** (assistant remembers this farmer's past problems) | Continuity; no re-explaining | Medium | Sessions adapter (T0-03) already exists. |
| P4 | **Personalized reminders** (spray/fertilizer/irrigation windows) | Addresses inattention, not just knowledge | Large | Evidence mixed (Uganda null); needs scheduling infra. Defer. |

**Hard rule (AGENTS.md #1):** anonymous / `DEMO_MODE=true` users must keep working exactly as today. Profile is **additive**, tied to the already-approved non-gating auth lane. No feature gating by default.

---

## 3. Proactive / push advisory scopes

BD flagship precedent: **Wheat Blast Early Warning System** (CIMMYT + BWMRI + BMD + DAE) — weather-model spore-risk → growth-stage-tailored fungicide advisory (+ PPE + "consult DAE") to 14,500+ officers ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12350828/)).

| # | Scope | Farmer profit | Effort | Competitor gap? |
|---|---|---|---|---|
| **PR1** | **Weather-triggered disease-risk alert for ONE crop** (potato late blight first) | Preventive spray *only when needed* → higher yield + less fungicide (GEOPOTATO proof) | Medium | **Yes** — Plantix's promised outbreak prediction is aspirational, not shipped |
| PR2 | **Predictive region-arrival pest alerts** ("pest coming to your area next week", Agrio-style) | Early warning before infestation | Large | **Yes** — globally rare |

**Data sources (all snapshot-able → no live-scraping rule violation):**
- BMD WRF gridded forecasts + Agromet bulletins
- BAMIS 64-district advisories with pre-built pest/disease-weather calendars
- Satellite (MODIS / Sentinel-1) as ACI IDSS used

**PR1 mechanism (potato late blight):** reuse the DAE Wheat Blast EWS rule template — a weather-risk rule (temp + humidity + leaf-wetness thresholds) evaluated against a **precomputed BMD/BAMIS snapshot**, producing a stage-aware advisory pushed to farmers in high-risk upazilas (targeted via the P1 profile), broadcast through the existing admin lane (see `04_ADMIN_OPERATOR_ROLES.md`, A3).

---

## 4. Suggested build order

1. **P1 farm profile** (cheap, unlocks everything) — spine step 4.
2. **P2 stage-aware advice** keyed to sowing date + BAMIS calendar.
3. **PR1 potato late-blight weather-risk alert** from a BMD/BAMIS snapshot — spine step 3.
4. (Later) P3 history-aware follow-ups.
5. (Deferred) P4 reminders, PR2 predictive pest arrival.

## 5. Guardrails

- Additive only; anonymous/demo path unchanged; no gating.
- Weather/pesticide data is **snapshotted**, never live-scraped.
- Redact BD phone numbers / Bengali digits in any stored profile (privacy adapter T1-04 already exists).
- No new required env var without updating `.env.example`.
