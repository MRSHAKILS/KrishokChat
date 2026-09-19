# Vision Pipeline — KrishokTech Advisory System

Documentation for the crop disease detection subsystem: a two-stage, agentic
computer-vision pipeline that takes a farmer's leaf photograph and returns a
Bengali-language disease diagnosis with cause and treatment guidance.

---

## 1. What it does

A farmer uploads a photo of a diseased plant. The pipeline answers three
questions in sequence, each with a dedicated model or lookup:

| Question | Answered by | Output |
|---|---|---|
| *What crop is this?* | Crop classifier (YOLO classify head, 6 classes) | `Potato`, conf `0.98` |
| *Which disease model applies?* | Static routing table (`CROP_TO_MODEL`) | `potato` → `potato_disease/model.pt` |
| *What disease is present?* | Crop-specific disease classifier | `Potato__Early_Blight`, conf `0.98` |
| *What should the farmer do?* | Bengali knowledge base lookup | description, cause, solution (all `_bn`) |

The critical design choice is **routing before detection**. A single 32-class
"all diseases" model would confuse visually similar lesions across unrelated
crops (potato late blight vs. rice leaf blast both present as dark necrotic
patches). By classifying the crop first, the disease model only ever chooses
between diseases that are plausible for that crop, which shrinks the decision
space from 32 classes to between 3 and 11.

---

## 2. Where it fits in the overall system

KrishokTech has two independent user-facing capabilities that share a backend
process:

```
                       ┌──────────────────────────────┐
                       │   Next.js frontend (:3000)   │
                       └───────────┬──────────────────┘
                                   │
                    ┌──────────────┴───────────────┐
                    │                              │
              text question                  leaf photograph
                    │                              │
                    ▼                              ▼
        ┌───────────────────────┐      ┌───────────────────────┐
        │  Q&A / RAG pipeline   │      │   VISION PIPELINE     │
        │  (AGENTS.md §4)       │      │   (this document)     │
        │                       │      │                       │
        │  Safety → Retrieval   │      │  Classify → Route →   │
        │  → Generation →       │      │  Detect → Details     │
        │  Verifier             │      │                       │
        └───────────────────────┘      └───────────────────────┘
                    │                              │
                    └──────────────┬───────────────┘
                                   ▼
                       ┌──────────────────────────────┐
                       │   FastAPI backend (:8000)    │
                       │   single process, no queue   │
                       └──────────────────────────────┘
```

The vision pipeline is **not** routed through the Q&A safety agent. It accepts
an image, not free text, so the prompt-injection and self-harm categories in
`AGENTS.md §4` do not apply to it. The two pipelines are siblings, not layers.

Where they do converge: the Bengali treatment text returned by the vision
pipeline is authored in the same register as the RAG corpus, so a farmer can
follow up a diagnosis with a text question and get consistent guidance.

---

## 3. Pipeline at a glance

```
  upload image
       │
       ▼
  ┌─────────────────────┐
  │ STAGE 1             │  crop_classifier/model.pt
  │ Crop Classification │  6 classes, 12.55 MB
  └──────────┬──────────┘
             │  "Potato" (0.9764)
             ▼
  ┌─────────────────────┐
  │ STAGE 2             │  CROP_TO_MODEL dict
  │ Disease Routing     │  no inference, pure lookup
  └──────────┬──────────┘
             │  → potato_disease
             ▼
  ┌─────────────────────┐
  │ STAGE 3             │  potato_disease/model.pt
  │ Disease Detection   │  3 classes, 11.03 MB
  └──────────┬──────────┘
             │  "Potato__Early_Blight" (0.9764)
             ▼
  ┌─────────────────────┐
  │ STAGE 4             │  potato_disease/disease_details.json
  │ Details Lookup      │  Bengali description/cause/solution
  └──────────┬──────────┘
             ▼
      JSON response
```

Full diagrams, including error paths and lazy-loading behaviour, are in
[`DIAGRAMS.md`](./DIAGRAMS.md) and [`WORKFLOW.md`](./WORKFLOW.md).

---

## 4. Implementation surface

| Concern | File |
|---|---|
| Orchestration + both endpoints | `backend/app/services/vision_orchestrator.py` |
| Router re-export | `backend/app/api/vision.py` |
| App wiring / CORS | `backend/app/main.py` |
| `ml_assets_dir` setting | `backend/app/core/config.py` |
| Model weights + knowledge bases | `backend/ml_assets/vision/` |
| Verification harness | `backend/ml_assets/vision/scripts/01_verify_models.py` |
| Last verification output | `backend/ml_assets/vision/verification_report.json` |

Note that `backend/app/api/classify.py` and `backend/app/api/detect.py` still
contain the original `not_implemented` stubs from the bootstrap task. They are
**not** registered in `main.py` and are dead code; the live implementations of
both routes live in `vision_orchestrator.py`. See
[`API_REFERENCE.md`](./API_REFERENCE.md) §6.

---

## 5. Model inventory summary

Six `.pt` files, all YOLO **classification** heads (`task=classify`) — despite
`AGENTS.md §3` describing YOLO as the object-detection layer, no model in this
pipeline emits bounding boxes.

| Model | Classes | Size | Status |
|---|---:|---:|---|
| `crop_classifier` | 6 | 12.55 MB | Verified |
| `rice_disease` | 8 | 3.21 MB | Verified |
| `corn_disease` | 4 | 11.03 MB | Loaded, untested |
| `potato_disease` | 3 | 11.03 MB | Verified |
| `brassica_disease` | 11 | 11.05 MB | Verified |
| `wheat_disease` | 6 | 12.55 MB | **PLACEHOLDER — not a real model** |

Sizes are decimal megabytes (bytes ÷ 10⁶), matching `verification_report.json`.

Full class listings, per-model confidences and the wheat placeholder details
are in [`MODELS.md`](./MODELS.md).

---

## 6. Known issues

These are documented from the current source, not speculation. Each is
expanded in the relevant document.

| # | Issue | Impact | Detail in |
|---|---|---|---|
| 1 | `json` is used but never imported in `vision_orchestrator.py` | Stage 4 raises `NameError` on every call that reaches it | `WORKFLOW.md` §6 |
| 2 | `app/api/vision.py` imports `router` under an alias and never rebinds it, so `from app.api.vision import router` fails | Backend will not start | `API_REFERENCE.md` §6 |
| 3 | `wheat_disease/model.pt` is a byte-identical copy of `crop_classifier/model.pt` | Wheat diagnosis is impossible; guarded by `PLACEHOLDER_WARNING.json` | `MODELS.md` §4 |
| 4 | `crop_classifier` has no `Rice` class, but `CROP_TO_MODEL` and `DISEASE_MODEL_PATHS` both route `rice` | The 8-class rice model is unreachable via `/api/detect` | `MODELS.md` §5 |
| 5 | `corn_disease` class names lack a `Corn__` prefix, unlike every other model | Stage 4 lookup key mismatch risk | `MODELS.md` §3 |
| 6 | `CROP_TO_MODEL` lacks `gourdguava`/`solanacea` disease models | Two of six classifier outputs are dead ends | `WORKFLOW.md` §2 |
| 7 | No confidence threshold anywhere | A 0.21-confidence crop guess routes as confidently as a 1.00 one | `WORKFLOW.md` §6 |
| 8 | 291 literal `[cite: N]` markers in three Bengali knowledge bases | Renders verbatim to farmers | `FOLDER_STRUCTURE.md` §3.3 |

---

## 7. Document map

| Document | Read it for |
|---|---|
| [`ARCHITECTURE.md`](./ARCHITECTURE.md) | Component diagram, data flow, model registry internals |
| [`WORKFLOW.md`](./WORKFLOW.md) | Stage-by-stage walkthrough with error branches |
| [`MODELS.md`](./MODELS.md) | Every model, every class name, performance data |
| [`API_REFERENCE.md`](./API_REFERENCE.md) | Endpoint contracts, schemas, curl examples |
| [`FOLDER_STRUCTURE.md`](./FOLDER_STRUCTURE.md) | What lives under `ml_assets/vision/` and why |
| [`DIAGRAMS.md`](./DIAGRAMS.md) | All ASCII diagrams collected in one place |

---

## 8. Quick start

```bash
# from repo root
cd backend
uv sync

# verify all six models load and emit real class names
uv run python ml_assets/vision/scripts/01_verify_models.py

# start the API
uv run fastapi dev app/main.py
```

Then:

```bash
curl -X POST http://localhost:8000/api/detect \
  -F "file=@backend/ml_assets/vision/test_images/potato_disease/0001.jpg"
```

Issues #1 and #2 in §6 must be fixed before the server will start and before
`/api/detect` can complete. Both are one-line changes.
