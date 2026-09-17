# Crop-Slot Labeling — Team Instructions (30–45 min)

**File:** `crop_slot_labeling_sheet_200.json` (200 real farmer queries, seed-42 stratified: 100 FB-group + 60 field + 40 web).  
**Your job:** fill `human_crop` per row. The extractor already found a crop in 63 rows (shown in `extractor_crop` — just confirm or correct); **137 rows need your judgment.**

## Labels
- `human_crop`: one of rice/potato/tomato/brinjal/chilli/wheat/maize/cabbage/cauliflower — the crop the farmer is asking about — or EMPTY string if no crop is determinable.
- `human_unclear`: set to `true` if even you cannot tell (these rows are excluded from hazard scoring and counted separately — "unclear" is a valid, valuable answer).
- `notes`: optional (dialect form, ambiguous symptom, multi-crop, etc.).

## Rules
- Judge the QUERY TEXT ONLY (column `query`). Do not use the gold answer.
- If the query names no crop but the symptom/context implies exactly one crop unambiguously, label it AND set `human_unclear` to `false` — then add note "inferred".
- If two people label: second reviewer independently fills a copy; disagreements resolved by discussion; report raw agreement in one line appended to this file.
- Do NOT tune, retrain, or edit any map/threshold based on what you see. System is frozen.

## What happens next
Labeled rows with a crop value → N01b paired blind/gated hazard run (same frozen recipe). Rows with EMPTY crop → gating-behavior analysis (halted or not?). Unclear rows → reported as ambiguity rate.
