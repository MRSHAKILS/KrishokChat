# Soil Moisture Research Integration Plan

**Date:** 2026-08-13
**Status:** COMPLETE (2026-08-13) — P0 release package, P1 backend, P2 frontend, P3 library vision section, P4 E2E verification, P5 docs + home-page milestone hook all shipped and verified. Backend 16/16 tests green; all 10 frontend routes 200; `/api/soil/analyze` returns locked + honest trace; home timeline carries the Pabna dataset milestone. Remaining optional: R8.md risk note (graceful fallback already implemented + tested — no doc needed). History below documents the original plan for reference.
**Source project:** `E:\CSE498R\Soil Moisture Detection`
**Target project:** KrishokChat Advisory System (`D:\KrishokChat Advisory System`)

> **What this is:** a complete, staged plan for bringing the Bangladesh field-collected
> soil moisture dataset into KrishokChat as (a) a released dataset contribution and
> (b) a new "মাটির আর্দ্রতা" (soil moisture) page that mirrors the disease-detection
> pattern (upload → pipeline → result → continue chatting). Because the regression
> models are not usable yet (all negative R², best RMSE 4.76 kPa), the analyze
> capability ships **locked as future work** while the dataset itself ships now.

---

## Table of Contents

1. [Why This Is Worth Integrating](#1-why-this-is-worth-integrating)
2. [What Exists in the Source Project](#2-what-exists-in-the-source-project)
3. [Design Principles (Honesty Guardrails)](#3-design-principles-honesty-guardrails)
4. [Track A — Dataset Contribution](#4-track-a--dataset-contribution)
5. [Track B — Backend API (locked model stub)](#5-track-b--backend-api-locked-model-stub)
6. [Track C — Frontend Page (mirrors /detect)](#6-track-c--frontend-page-mirrors-detect)
7. [File-by-File Change List](#7-file-by-file-change-list)
8. [Implementation Order & Test Gates](#8-implementation-order--test-gates)
9. [Risks & Mitigations](#9-risks--mitigations)
10. [Future Work (unlock path)](#10-future-work-unlock-path)

---

## 1. Why This Is Worth Integrating

| Claim | Evidence |
|---|---|
| First of its kind for Bangladesh | 722 RGB field photos of soil with **tensiometer ground truth (kPa)**, collected over a 3-day field campaign in **Pabna District** (May 29–31, 2026). No comparable public Bangladesh field dataset exists. |
| Complete metadata | 16-column canonical manifest: soil type (6 USDA classes), land type (3), crop (14), growth stage (8), 46 measurement series, 50 unique kPa values (0.0–21.5 kPa). |
| Audited & corrected | Phase-0 audit resolved 106 kPa corrections, 12 missing IDs, 4 duplicate IDs, 1 contamination flag (P0029), series-stratified train/val/test split (472/119/131) with zero leakage. |
| Reusable asset | The dataset is the contribution; the models are not. This matches how the safety dataset (20,112 records) was already released as a standalone asset. |
| Demo value | A new "field console" capability (soil moisture) doubles as a credibility story: "we collect our own field data" — with the honest locked state showing why the model isn't live yet. |

**Model status (verified from `kaggle output/soild_moisture_experiments_frozen_fixed.ipynb`):**

| Model | RMSE (kPa) | R² |
|---|---|---|
| RandomForest (MobileNet features) | 4.7633 | −1.138 |
| XGBoost (MobileNet features) | 4.8289 | −1.198 |
| Ensemble (5 CNNs) | 5.0766 | −1.429 |
| CNN-Small | 5.1597 | −1.509 |
| ResNet-18 | 5.2145 | −1.563 |

All R² < 0 ⇒ worse than predicting the mean. **Nothing here may be presented as a working model.** The dataset, however, is release-ready.

---

## 2. What Exists in the Source Project

```
E:\CSE498R\Soil Moisture Detection\
├── agents.md                        — project conventions (folder/script naming)
├── dataset/
│   ├── raw/                         — 722 JPEG (720×1280 portrait)
│   ├── updated_dataset/
│   │   ├── correct_image/           — canonical field-team-corrected images
│   │   └── TraceData.xlsx           — 12-column field log (ground truth)
│   ├── preprocessed/
│   │   ├── image_manifest.csv       — FROZEN: 722 rows × 16 cols (single source of truth)
│   │   ├── split_assignment.csv     — FROZEN: 472/119/131 series-stratified
│   │   ├── dataset_summary.json     — summary stats
│   │   ├── series_map.json          — 46 series
│   │   ├── anomalies.json           — P0029 contamination flag
│   │   └── exif_metadata.json       — 720×1280, lighting window evidence
│   ├── scripts/                     — 16 numbered pipeline scripts (step0a..step2e)
│   └── reports/
│       ├── PHASE0_AUDIT_REPORT.md   — full integrity audit (722, 106 corrections)
│       └── preprocessing_report.md  — canonical pipeline documentation
├── kaggle output/
│   └── soild_moisture_experiments_frozen_fixed.ipynb — all experiments (negative R²)
└── literature review/
    ├── LITERATURE_REVIEW.md
    ├── RESEARCH_GAPS.md
    ├── SUPERVISOR_SUMMARY.md
    └── papers/                      — 3 reviewed papers (PLOS ONE ginseng, Zhang LG, Suud CNN)
```

**Key numbers for the dataset card (verified, do not invent more):**

| Stat | Value |
|---|---|
| Images | 722 |
| Resolution | 720×1280 portrait JPEG |
| kPa range | 0.0–21.5 kPa (50 unique values) |
| Soil types | 6 (Doash/Loam 180, Atel/Clay 156, Bele_Doash/Sandy Loam 143, Atel_Doash/Clay Loam 126, Poli/Silt 85, Bele/Sandy 32) |
| Land types | 3 (Medium 308, High 289, Low 117) |
| Crops | 14 (Rich 119, No crop 107, Jute 96, Grass 81, Mango 77, …) |
| Growth stages | 8 (Mature 280, Seedling 100, …) |
| Series | 46 (max 83, 15 singletons) |
| Split | Train 472 / Val 119 / Test 131 (series-stratified, no leakage) |
| Collection | Pabna District, May 29–31 2026, tensiometer ground truth |
| Corrections | 106 kPa (Δ>0.5), 12 missing IDs filled, 4 duplicates resolved |
| Contamination | 1 flagged (P0029, excluded from training) |

---

## 3. Design Principles (Honesty Guardrails)

These mirror AGENTS.md hard rules and the existing vision pipeline's honesty design:

1. **Never present the soil model as working.** Every surface that would show a
   prediction must first pass through a `status: "locked"` gate. No metric, no
   pretend analysis. This is the same rule as "never claim bounding boxes".
2. **All dataset stats are precomputed, loaded from disk, never computed live.**
   Mirror `GET /api/benchmark` philosophy: static JSON served by the API.
3. **The locked state is a feature, not a bug.** The UI explains *why* it's locked
   (models in development, dataset released) with real numbers (722 images,
   6 soil types, 0–21.5 kPa) — credibility through transparency.
4. **The chat continuation still works.** Farmers can ask soil-related questions
   through the existing QA pipeline (RAG corpus already contains soil/irrigation
   content). The locked analyzer never blocks the chat.
5. **No new runtime dependency, no new server.** Dataset JSON + one small router +
   frontend page. Nothing is loaded at request time except static JSON.
6. **Do not copy the 722 images into the repo.** Images stay in the source project;
   the release ships the manifest + a subset of representative thumbnails (see Track A).

---

## 4. Track A — Dataset Contribution

**Goal:** ship the soil moisture dataset as a first-class released asset, the same way
`safety_refusal_t3.jsonl` / `safety_requery_t4.jsonl` were released.

### A.1 Target layout (new)

```
KrishokChat/dataset_release/soil_moisture/
├── README.md                          ← dataset card (see A.3)
├── image_manifest.csv                 ← copy of frozen canonical manifest
├── split_assignment.csv               ← copy of frozen split
├── dataset_summary.json               ← copy
├── anomalies.json                     ← copy
├── series_map.json                    ← copy
├── reports/
│   ├── PHASE0_AUDIT_REPORT.md         ← copy
│   └── preprocessing_report.md        ← copy
├── model_status.json                  ← NEW: honest model benchmark table (from notebook)
├── thumbnails/                        ← NEW: ~12 representative sample images
│   ├── soil_grid_1.jpg … soil_grid_12.jpg
│   └── samples_manifest.json          ← mapping thumbnail → manifest row
└── preview_grid.jpg                   ← NEW: 3×4 contact-sheet for the UI
```

### A.2 Steps

1. **Copy frozen artifacts** from `E:\CSE498R\Soil Moisture Detection\dataset\preprocessed\`.
2. **Build the preview grid** — a small Python script picks 12 stratified samples
   (2 per soil type, spanning wet→dry kPa) and writes a 3×4 contact sheet
   (`preview_grid.jpg`, ~600px) + `thumbnails/` + `samples_manifest.json`.
3. **Write `model_status.json`** — the honest benchmark table from section 1,
   marked `"status": "in_development"`, `"releaseable": false`. This file is the
   single source of truth the API/UI read to show the locked state.
4. **Write the dataset card** (`README.md`) with: purpose, collection protocol,
   stats table, soil-type mapping (Bengali → USDA), split description, known
   limitations (3-day window, single site, no capture timestamps, Bele=32),
   license placeholder, citation line, and HF upload plan (TODO: link).
5. **Hugging Face upload (optional, user-driven)** — same pattern as
   `RaiyanKhaan/krishokChat`; add the resolved link to `LINKS` in constants when
   the researcher uploads it.

### A.3 Dataset card skeleton (`README.md`)

```markdown
# Bangladesh Soil Moisture Field Dataset (RGB → kPa)

First field-collected RGB soil-moisture dataset for Bangladesh:
722 tensiometer-labeled photos (0.0–21.5 kPa), 6 soil types, Pabna District.

## Stats (table from section 2)
## Collection Protocol (field log TraceData.xlsx, tensiometer)
## Files (manifest, split, series, anomalies)
## Split (472/119/131, series-stratified, leakage check PASS)
## Soil Type Map (Doash→Loam, Atel→Clay, …)
## Known Limitations (3-day window, single site, no timestamps, Sandy=32)
## Model Status (in development — negative R² table, honest)
## Citation & License (TODO)
```

---

## 5. Track B — Backend API (locked model stub)

**Goal:** a tiny, contract-correct API that serves dataset info and *refuses*
analysis with a clear `locked` status. Mirrors the layered architecture exactly.

### B.1 New domain (`backend/app/domain/soil.py`)

```python
class SoilStatus(StrEnum):
    LOCKED = "locked"          # model not available (current state)
    ANALYZED = "analyzed"      # reserved for the future regression path
    INVALID_IMAGE = "invalid_image"

class SoilStage(StrEnum):
    INTAKE = "intake"
    MOISTURE_REGRESSION = "moisture_regression"   # future
    SOIL_CLASSIFICATION = "soil_classification"   # future
    ADVISORY = "advisory"                          # future

@dataclass(frozen=True)
class SoilDatasetInfo:
    total_images: int
    kpa_range: tuple[float, float]
    soil_types: tuple[dict[str, str], ...]   # {key, bn, usda, count}
    splits: dict[str, int]                    # train/val/test
    series_count: int
    crops: tuple[str, ...]
    collection: dict[str, str]                # site, dates, instrument
    model_status: str                         # "in_development"
    model_results: tuple[dict[str, str | float], ...]  # honest table or []

@dataclass(frozen=True)
class SoilResult:
    status: SoilStatus
    info: SoilDatasetInfo | None = None
    error: str | None = None
```

### B.2 New API router (`backend/app/api/soil.py`)

| Endpoint | Behavior |
|---|---|
| `GET /api/soil/dataset` | Returns `SoilDatasetInfo` from `dataset_release/soil_moisture/` JSON files (loaded once at startup into the container). **No live computation.** |
| `POST /api/soil/analyze` | Accepts an image, runs the intake quality gate (reuse `image_quality`), then returns `{"status": "locked", ...}` with a clear error: *"Soil moisture regression model is in development. Dataset released; analysis will be enabled when the model is validated."* **Never attempts inference.** |

Router registration in `app/main.py` next to the other routers.

### B.3 Container wiring (`backend/app/application/container.py`)

- Add `soil_info: SoilDatasetInfo` (loaded from disk at startup; missing files ⇒
  fail gracefully with an empty-but-valid object, never crash the app).
- Add `soil: SoilService` — a tiny application-layer service that implements
  `analyze()` as a hard lock (returns `SoilStatus.LOCKED` regardless of input)
  and `dataset()` passthrough. Documented unlock path: swap in a real
  `SoilRunner` port adapter when weights exist.

### B.4 Schemas (`backend/app/models/schemas.py`)

Add `SoilDatasetResponse` and `SoilAnalyzeResponse` mirroring the domain objects,
with the same `status`/`agent_trace` conventions as `DetectResponse`.

### B.5 Why locked at the API, not just the UI

Defense in depth. If anyone later enables the UI button before the model is
validated, the API still refuses. This is the same discipline as the vision
pipeline's `detection_mode: "classification"` honesty field.

---

## 6. Track C — Frontend Page (mirrors /detect)

**Goal:** `frontend/src/app/(app)/soil/page.tsx` — visually and behaviorally
consistent with `/detect`, with the analyzer locked and the dataset showcased.

### C.1 Page structure (reuses detect's layout skeleton)

```
/soil  (মাটির আর্দ্রতা — Soil Moisture Field Console)
├── Left column
│   ① IntakeZone (reuse component, "photo of your field soil")
│      └── locked analyzer button — disabled, tooltip "শীঘ্রই আসছে" (coming soon)
│   ② Dataset showcase card (NEW: SoilDatasetCard)
│      ├── stat grid: ৭২২ ছবি | ৬ মাটির ধরন | ০–২১.৫ kPa | ৪৬ সিরিজ | ৭২২ জিপিএস ফিল্ড ফটো
│      ├── preview grid image (from Track A)
│      ├── soil-type chips (Doash, Atel, Bele, … with Bengali names)
│      ├── kPa histogram mini-bars (0–10 / 10–20 / 20–22)
│      └── "ডেটাসেট মুক্ত" badge + model status row: "মডেল: উন্নয়নে (লকড)"
│   ③ Future-work card (NEW: SoilLockedCard)
│      ├── lock icon + "স্বয়ংক্রিয় মাটির আর্দ্রতা নির্ণয় এখনো চালু হয়নি"
│      ├── honest model table (RMSE/R² from model_status.json, marked in_development)
│      ├── why-locked copy + what happens next
│      └── "ডেটাসেট ডাউনলোড/দেখুন" link (HF or dataset card)
│   ④ PipelineRail — SOIL_STAGES preset (intake → moisture_regression → advisory)
│      shown in "locked" visual state when the user tries the disabled button
├── Right column (same as /detect)
│   ⑤ QAPanel with soil context banner: detectedSoilType/landType (from a
│      manual selector, NOT from a model) → farmer asks soil questions via RAG
│   ⑥ ContextBanner variant: "আপনার এলাকা: পাবনা • মাটি: দোআঁশ" when selected
```

### C.2 New/changed frontend files

| File | Change |
|---|---|
| `src/app/(app)/soil/page.tsx` | NEW — detect-page skeleton, locked analyzer |
| `src/components/soil/soil-dataset-card.tsx` | NEW — dataset stats + preview grid + chips |
| `src/components/soil/soil-locked-card.tsx` | NEW — locked model explanation + honest table |
| `src/components/detect/pipeline-rail.tsx` | ADD `SOIL_STAGES` preset (3 stages) |
| `src/components/detect/context-banner.tsx` | EXTEND to accept `soilType`/`landType` props (optional, backward compatible) |
| `src/components/detect/intake-zone.tsx` | REUSE as-is (verify copy accepts custom labels or add optional props) |
| `src/lib/api.ts` | ADD `getSoilDataset()`, `analyzeSoil()` types + fetchers |
| `src/lib/constants.ts` | ADD `SOIL_STAGES` labels + soil type map (Bengali) + dataset link |
| `src/components/navbar.tsx` | ADD `/soil` to `NAV` (primary: হোম | রোগ নির্ণয় | মাটি | পরামর্শ) — keeps headline features at 4 max |
| `src/app/(marketing)/data/page.tsx` | ADD soil dataset section (stat block + link) |
| `src/app/(marketing)/research/page.tsx` | OPTIONAL: mention dataset in research assets |

### C.3 Interaction spec (exact)

1. **Page load** → `GET /api/soil/dataset` → render stats. Loading skeleton =
   existing `skeleton` component. Fetch failure = inline error card (no crash).
2. **User drops a photo** → intake validation (reuse `prepareUploadImage`) →
   preview shown → analyzer button rendered **disabled** with a lock icon and
   tooltip. Clicking it (or it can't be clicked — use `disabled`) shows the
   `SoilLockedCard` hint: "মডেল প্রস্তুত হলে এখানে ছবি থেকে আর্দ্রতা মাপা যাবে।"
3. **Dataset card** always visible on the left (below intake) regardless of photo.
4. **Right chat** — empty state uses soil-flavored suggested questions
   ("মাটিতে কখন পানি দেব?", "দোআঁশ মাটিতে ধান ভালো হয় কেন?"). If the user
   selects a soil type / land type from a small manual selector, `ContextBanner`
   shows it and `QAPanel` receives `detectedSoilType` (sent as `crop`-adjacent
   context only if the backend QA schema accepts it — otherwise keep chat
   context-free to avoid breaking the contract; see risk R5).
5. **Mobile** — same pane switcher as /detect (ডেটাসেট/ফলাফল ↔ পরামর্শ চ্যাট).

### C.4 Visual language

Reuse the existing design tokens (leaf/ochre/clay/paper/ink, `font-display`,
`surface-lift`, `control-press`). The locked card uses **ochre** (warning) not
clay (error) — it is an intentional state, not a failure. The dataset card uses
**leaf** accents. No new design system invented (per AGENTS.md §3).

---

## 7. File-by-File Change List

### New files (backend)
| File | Purpose |
|---|---|
| `backend/app/domain/soil.py` | SoilStatus/SoilStage/dataclasses |
| `backend/app/application/soil.py` | SoilService (locked analyze + dataset passthrough) |
| `backend/app/api/soil.py` | GET /api/soil/dataset, POST /api/soil/analyze |
| `backend/app/infrastructure/soil/` | loader for dataset JSON + (future) runner placeholder |
| `backend/tests/test_soil.py` | contract tests: dataset 200, analyze locked, invalid image |

### New files (frontend)
| File | Purpose |
|---|---|
| `frontend/src/app/(app)/soil/page.tsx` | the page |
| `frontend/src/components/soil/soil-dataset-card.tsx` | stats + preview |
| `frontend/src/components/soil/soil-locked-card.tsx` | locked explanation |

### New files (release)
| File | Purpose |
|---|---|
| `dataset_release/soil_moisture/README.md` | dataset card |
| `dataset_release/soil_moisture/model_status.json` | honest model table |
| `dataset_release/soil_moisture/preview_grid.jpg` | contact sheet |
| `dataset_release/soil_moisture/thumbnails/` | 12 samples + manifest |
| `scripts/build_soil_preview_grid.py` | regenerable preview builder |

### Modified files (backend)
| File | Change |
|---|---|
| `backend/app/main.py` | include soil router |
| `backend/app/application/container.py` | wire soil service + dataset info |
| `backend/app/models/schemas.py` | SoilDatasetResponse, SoilAnalyzeResponse |
| `backend/app/api/extras.py` or new router | (see soil.py — prefer new router) |

### Modified files (frontend)
| File | Change |
|---|---|
| `frontend/src/lib/api.ts` | soil fetchers/types |
| `frontend/src/lib/constants.ts` | soil labels, soil type map, dataset links |
| `frontend/src/components/detect/pipeline-rail.tsx` | SOIL_STAGES preset |
| `frontend/src/components/detect/context-banner.tsx` | optional soil props |
| `frontend/src/components/navbar.tsx` | nav entry |
| `frontend/src/app/(marketing)/data/page.tsx` | dataset section |

### No changes (locked by rules)
- `backend/app/agents/*`, `backend/app/services/advisory/*` (shims, §5.1)
- LLM adapters, retrieval, safety pipeline, session store
- `scripts/start_krishokchat_local.ps1` / demo orchestration

---

## 8. Implementation Order & Test Gates

| Phase | Work | Gate |
|---|---|---|
| **P0 — Release package** | Copy frozen artifacts; build preview grid; write model_status.json + README card | `scripts/build_soil_preview_grid.py` runs; JSON validates; stats match PHASE0 report |
| **P1 — Backend domain+API** | domain/soil.py, application/soil.py, api/soil.py, container wiring, schemas | `uv run pytest backend/tests/test_soil.py` passes; `GET /api/soil/dataset` returns exact stats; `POST /api/soil/analyze` returns `locked` even with a valid image |
| **P2 — Frontend page** | soil/page.tsx + 2 cards + api.ts/constants + rail preset | `pnpm build` clean; manual: page loads, stats render, analyzer disabled, chat answers soil question, mobile pane switcher works |
| **P3 — Navigation & marketing** | navbar entry, /data section, research mention | `pnpm build` clean; links resolve |
| **P4 — E2E verification** | run three servers; smoke /soil page; test chat; run `capture_ui_screenshots.js` if used | All servers up; page HTTP 200; no console errors |
| **P5 — Docs** | update README.md routes table, AGENTS.md note (optional), this plan → status: implemented | README consistent |

**DoD (per AGENTS.md §6):** runs locally without errors; stack unchanged; no new
dependency (if one is ever needed, version confirmed by web search + noted in
README); any new env var documented (none expected); commit message describes
what and why.

---

## 9. Risks & Mitigations

| # | Risk | Severity | Mitigation |
|---|---|---|---|
| R1 | Someone presents negative-R² models as "results" in the demo | High | `model_status.json` marked `in_development`; API refuses analysis; UI locks button; copy says "উন্নয়নে" everywhere |
| R2 | 722 images copied into repo → repo bloat / .gitignore conflicts | Medium | Only manifest + 12 thumbnails + preview grid ship; images stay in source project |
| R3 | `/api/soil/analyze` endpoint looks "dead" to reviewers | Low | Response includes a clear human-readable locked message + dataset reference; test proves the gate works |
| R4 | Dataset stats drift from source project | Low | All numbers served from copied frozen files; script regenerates; PHASE0 report is the reference |
| R5 | QA chat schema rejects soil context fields | Medium | Check `QARequest` schema first; if `crop` is the only context channel, map soil type to a safe free-form context or send no context — never break the QA contract |
| R6 | Navbar gets crowded | Low | Keep primary NAV at 4 items max; if crowded, `/soil` moves under "আরও" (MORE) |
| R7 | Preview grid licensing/consent | Low | Field team owns the data; add license line to dataset card; confirm with researcher before HF upload |
| R8 | Backend startup fails if dataset JSON missing | Medium | Container loads with graceful fallback (empty info + warning log); tests cover missing-file path |

---

## 10. Future Work (unlock path)

When the regression models are validated (target: RMSE meaningfully below the
~4.8 kPa baseline with positive R² on a held-out series):

1. **Publish weights** under `backend/ml_assets/soil/` (`.pt` + exported ONNX).
2. **Add `SoilRunner` port adapter** (Ultralytics/ONNX or torch, following the
   vision infrastructure pattern) — no route changes needed.
3. **Flip the lock**: `SoilService.analyze()` calls the runner; UI button enables;
   `model_status.json` → `"released"` with real metrics.
4. **Knowledge map**: add soil advisory content (kPa → irrigation guidance) to
   `backend/ml_assets/advisory/` so the advisory stage is grounded, matching the
   disease knowledge map pattern.
5. **Audit trail**: log soil analyzes to the same JSONL audit sink (`channel:
   "soil"`), extending the safety-metrics panel naturally.

Until then, the locked page is the honest, defensible state — and the dataset is
the contribution the community gets today.

---

*End of plan. Prepared 2026-08-13 after live verification of all three servers
(llama-server 11435, backend 8000, frontend 3100).*
