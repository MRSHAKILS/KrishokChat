# 02 — Disease / Crop Coverage Priorities

**Parent:** `00_SCOPE_OUTLINE.md` (§3, spine step 6)
**Status:** PLANNING — no code changes.
**Constraint from the researcher:** cover the disease/pest types where farmers *actually* face problems.

---

## 1. The coverage gap (what the current models miss)

Current classifiers = **leaf diseases only** for potato, rice, wheat, corn, brassica.

**Two gaps drive the biggest real losses:**
1. **Insect pests** — the app cannot see them, yet pests cause the largest single-crop losses and the worst pesticide overuse.
2. **The high-pesticide vegetables** — brinjal and chili, where farmers spray dozens of times a season with retailer-driven (conflicted) advice.

The architecture already supports adding a crop model + `disease_details.json` + `class_names.json` **without touching the pipeline** — so coverage extends incrementally.

---

## 2. Ranked priorities

| Priority | Crop / target | Farmer impact (loss / harm) | Effort | Notes |
|---|---|---|---|---|
| **1** | **Maize — Fall armyworm** (detection + IPM/dose) | ~37.7% avg loss, present in ~35 districts; fastest-growing cereal; **zero pest coverage today**; damage highly visual (ideal for image model) | Medium | First pest model. High national impact. |
| **2** | **Potato — late-blight weather-risk forecasting** | 25–57% loss; largest cash crop (~7.5M farmers); proven BD ROI (GEOPOTATO: +USD 173–220/ha with *less* fungicide) | Medium | Diagnosis already exists → add forecasting (see `03_PERSONALIZATION_PROACTIVE.md`). This is the spine crop. |
| **3** | **Rice — insect pests** (brown planthopper, stem borer deadheart/whitehead, rice hispa) | Rice = #1 crop; pests cause 44–62% outbreak losses; current rice model has *no* insects; big IPM/resurgence upside | Medium | Add classes to existing rice model + ETL "don't spray yet" IPM. |
| 4 | **Brinjal — shoot & fruit borer** (+ wilt) | Up to 86% loss; worst pesticide crisis (up to ~84 sprays/season) → maximum value from safety/dose/IPM agents | Medium | Best showcase for the safety pipeline. |
| 5 | **Chili — anthracnose** | ~99% of chili farmers affected; near-zero disease literacy | Medium | |
| 6 | **Tomato — late blight** (+ borer) | High-value; late blight **reuses the potato *P. infestans* model** + forecasting | Low marginal | Cheap add once potato spine exists. |
| 7 | Rice false smut / sheath rot; wheat-blast forecasting; mango anthracnose; banana Panama wilt | Complete the set / regional value | Varies | Deprioritize jute (pests aren't leaf-imagery). |

---

## 3. Every diagnosis must carry BD-grounded action (not just a label)

A disease/pest label alone is not useful — and not novel. The differentiated value is pairing each diagnosis with **BD-approved dose + timing + IPM**, grounded in official sources:

- **BAMIS** — publishes exact doses + registered trade names + pest/disease-weather calendars (e.g. [BAMIS pests](https://www.bamis.gov.bd/en/pests/1/all/76/)).
- **BRRI / BARI** — crop-specific recommendations.
- **Krishi Projukti Hatboi** (BARC handbook) — the national technology reference.
- **PPW registered-pesticide + banned/HHP list** — for the dosage verifier (see `06_PAPER_NOVELTY.md`, N1/N5).

This grounding is exactly where the safety/verifier pipeline turns a label into differentiated, safe advice.

---

## 4. Suggested build order

1. Ground the **potato** advisory (diagnosis already exists) in BD dose/timing/IPM — proves the pattern (spine step 2).
2. **Maize FAW** — first new pest model (priority 1).
3. **Rice insect pests** added to the existing rice model (priority 3).
4. **Brinjal** + **chili** (priorities 4–5) — the pesticide-crisis showcase.
5. **Tomato late blight** — cheap reuse of potato model.
6. Tier-3 completeness as time allows.

## 5. Guardrails

- No object-detection / bounding-box claims from `classify` artifacts.
- Do not fabricate loss figures — cite BD sources or mark `TODO`.
- New crop = new model + `disease_details.json` + `class_names.json`; do not fork the pipeline.
- Every diagnosis routes through the existing safety/verifier flow.
