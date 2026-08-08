# Vision Pipeline — Architecture

Detailed architecture of the crop disease detection subsystem: components,
their interactions, data flow, and the model registry that binds crop labels to
model weights.

---

## 1. System overview

```
┌───────────────────────────────────────────────────────────────────────────┐
│                          CLIENT (Next.js, :3000)                          │
│                                                                           │
│   <input type="file"> ──► FormData{ file } ──► fetch(POST /api/detect)    │
└──────────────────────────────────┬────────────────────────────────────────┘
                                   │ multipart/form-data
                                   │ CORS: allow_origins=[frontend_origin]
                                   ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                     FastAPI application (:8000)                           │
│                        backend/app/main.py                                │
│                                                                           │
│   include_router(qa_router)         ← text Q&A pipeline                   │
│   include_router(vision_router)     ← THIS SUBSYSTEM                      │
│   include_router(benchmark_router)  ← precomputed research panel          │
│                                                                           │
│   NOTE: classify_router / detect_router are imported but NOT included.    │
│         They are the dead bootstrap stubs. See API_REFERENCE.md §6.       │
└──────────────────────────────────┬────────────────────────────────────────┘
                                   │
                                   ▼
┌───────────────────────────────────────────────────────────────────────────┐
│         app/api/vision.py  —  thin re-export shim (4 lines)               │
│         from app.services.vision_orchestrator import router as ...        │
└──────────────────────────────────┬────────────────────────────────────────┘
                                   │
                                   ▼
┌───────────────────────────────────────────────────────────────────────────┐
│      app/services/vision_orchestrator.py  —  the entire pipeline          │
│                                                                           │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐     │
│  │ MODEL REGISTRY   │  │ LAZY LOADERS     │  │ INFERENCE HELPER     │     │
│  │                  │  │                  │  │                      │     │
│  │ VISION_DIR       │  │ _crop_classifier │  │ predict_             │     │
│  │ CROP_CLASSIFIER_ │  │ _disease_models  │  │   classification()   │     │
│  │   PATH           │  │                  │  │                      │     │
│  │ DISEASE_MODEL_   │  │ get_crop_        │  │ → top_prediction     │     │
│  │   PATHS {5}      │  │   classifier()   │  │ → top3               │     │
│  │ CROP_TO_MODEL{7} │  │ get_disease_     │  │ → all_probabilities  │     │
│  │                  │  │   model(key)     │  │                      │     │
│  └──────────────────┘  └────────┬─────────┘  └──────────┬───────────┘     │
│                                 │                       │                 │
│  ┌──────────────────────────────┴───────────────────────┴──────────────┐  │
│  │ ENDPOINTS                                                           │  │
│  │   POST /api/classify  → Stage 1 only                                │  │
│  │   POST /api/detect    → Stages 1-2-3-4                              │  │
│  └──────────────────────────────┬──────────────────────────────────────┘  │
│                                 │                                         │
│  ┌──────────────────────────────┴──────────────────────────────────────┐  │
│  │ KNOWLEDGE BASE LOADERS                                              │  │
│  │   load_class_names(dir)       → class_names.json                    │  │
│  │   load_disease_details(key)   → disease_details.json                │  │
│  └──────────────────────────────┬──────────────────────────────────────┘  │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │ filesystem reads
                                  ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                    backend/ml_assets/vision/                              │
│                                                                           │
│   crop_classifier/     model.pt   class_names.json                        │
│   rice_disease/        model.pt   class_names.json  disease_details.json  │
│   wheat_disease/       model.pt   class_names.json  disease_details.json  │
│                        PLACEHOLDER_WARNING.json  ◄── routing guard        │
│   corn_disease/        model.pt   class_names.json  disease_details.json  │
│   potato_disease/      model.pt   class_names.json  disease_details.json  │
│   brassica_disease/    model.pt   class_names.json  disease_details.json  │
│                                                                           │
│   test_images/<model>/ *.jpg *.png *.webp                                 │
│   scripts/01_verify_models.py                                             │
│   verification_report.json                                                │
└───────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
                    ┌──────────────────────────────┐
                    │ Ultralytics YOLO runtime     │
                    │ torch ≥ 2.13 CPU inference   │
                    │ task = "classify"            │
                    └──────────────────────────────┘
```

---

## 2. Component responsibilities

| Component | Responsibility | Does **not** do |
|---|---|---|
| `main.py` | App construction, CORS, router registration, lifespan hook | Model preloading — the lifespan hook is an empty `yield` |
| `api/vision.py` | Re-export the orchestrator's router | Any logic; it is a 4-line shim |
| `vision_orchestrator.py` | Registry, lazy loading, both endpoints, KB lookup | Persistence, logging, audit trail |
| `core/config.py` | Supplies `ml_assets_dir` (default `backend/ml_assets`) | Any vision-specific setting |
| `ml_assets/vision/` | Weights, class maps, Bengali KBs, test fixtures | Version pinning or model provenance metadata |
| `scripts/01_verify_models.py` | Offline verification; regenerates `class_names.json` from weights | Runtime participation |

### 2.1 Why the router lives in `services/`

`vision_orchestrator.py` declares `router = APIRouter()` and defines both HTTP
endpoints inline. This collapses the API layer and the service layer into one
file, which contradicts the folder structure in `AGENTS.md §5` where
`api/classify.py` and `api/detect.py` were meant to hold the routes.

For a 7-day demo the collapse is defensible — there is exactly one consumer and
no reuse pressure. It becomes a problem the moment anything other than an HTTP
handler needs to run a crop classification, because the inference helpers are
now co-located with `HTTPException` raises. `get_crop_classifier()` raising
`HTTPException(500, ...)` means the model loader is only callable from inside a
request context.

---

## 3. Data flow

### 3.1 `POST /api/detect` — the full path

```
 STEP  ACTOR                    DATA IN                    DATA OUT
 ────  ───────────────────────  ─────────────────────────  ──────────────────────────
  1    FastAPI                  multipart body             UploadFile
  2    detect_disease()         UploadFile.content_type    guard: must start "image/"
  3    await file.read()        UploadFile                 bytes
  4    PIL.Image.open()         bytes (io.BytesIO)         Image (RGB)
  5    get_crop_classifier()    —                          YOLO instance (cached)
  6    predict_classification() Image                      {top_prediction, top3, all}
  7    .lower()                 "Potato"                   "potato"
  8    CROP_TO_MODEL[...]       "potato"                   "potato"  (or None)
  9    Path.exists()            PLACEHOLDER_WARNING.json   bool guard
 10    get_disease_model()      "potato"                   YOLO instance (cached)
 11    predict_classification() Image                      {top_prediction, top3, all}
 12    load_disease_details()   "potato"                   dict | None
 13    linear scan              disease_class              matching class dict | None
 14    Pydantic serialise       fields                     DiseaseDetectionResponse
```

Note step 4: the **same** decoded `Image` object is passed to both models. The
image is decoded once and never re-read from bytes, which is the right call —
but it also means both models see identical preprocessing, and Ultralytics
handles resize/normalise internally per model.

### 3.2 Transformation detail — `predict_classification`

```
Image (RGB, any size)
   │
   ▼  model(image, verbose=False)[0]
Results object
   │
   ├── .probs is not None ──► classification path
   │      │
   │      ▼  .data.cpu().numpy()
   │   probs: np.ndarray, shape (n_classes,)
   │      │
   │      ▼  np.argsort(probs)[::-1]
   │   top_indices: descending confidence order
   │      │
   │      ├──► top_prediction  = names[top_indices[0]], round(4)
   │      ├──► top3            = first 3 of top_indices
   │      └──► all_probabilities = {name: prob} for every class
   │
   └── .probs is None ──────► {"error": "Model did not return probabilities"}
                              ⚠ returned as a dict, then indexed with
                                ["top_prediction"] by the caller → KeyError
```

The error branch is a latent crash rather than a handled failure. Every model
currently ships with `task=classify`, so `.probs` is always populated and the
branch never fires — but it would fire immediately if a genuine detection model
(bounding boxes, `.boxes`) were dropped into the registry, which is exactly what
`AGENTS.md §3` anticipates for YOLO.

### 3.3 Stage 4 lookup traversal

`disease_details.json` nests one level deeper than the lookup needs:

```
{
  "potato_crop_library": {          ← top-level key, name varies per crop
    "crop_name": "...",
    "total_classes": 3,
    "source_reference": "...",
    "classes": [                    ← the array that gets scanned
      { "class_name": "...", "description_bn": "...",
        "cause_bn": "...", "solution_bn": "..." },
      ...
    ]
  }
}
```

The orchestrator iterates `details.values()` (one entry) then
`crop_data["classes"]`, comparing `cls["class_name"] == disease_class`.

**This comparison never matches.** The model emits machine labels
(`Potato__Early_Blight`); the KB stores human labels with Bengali glosses
(`Early Blight (আগাম ধসা)`). There is no normalisation step. `disease_info` is
therefore `null` in every response. See `WORKFLOW.md` §5 for the mapping table
that would be needed.

The `break` also only escapes the inner loop, so with multiple top-level keys
the scan would continue after a match — harmless today, wrong in principle.

---

## 4. Model registry

### 4.1 Registry structures

Three module-level constants define the entire routing behaviour.

```python
VISION_DIR = Path(settings.ml_assets_dir) / "vision"

CROP_CLASSIFIER_PATH = VISION_DIR / "crop_classifier" / "model.pt"

DISEASE_MODEL_PATHS = {
    "rice":     VISION_DIR / "rice_disease"     / "model.pt",
    "wheat":    VISION_DIR / "wheat_disease"    / "model.pt",
    "corn":     VISION_DIR / "corn_disease"     / "model.pt",
    "potato":   VISION_DIR / "potato_disease"   / "model.pt",
    "brassica": VISION_DIR / "brassica_disease" / "model.pt",
}

CROP_TO_MODEL = {
    "rice":       "rice",
    "wheat":      "wheat",
    "corn":       "corn",
    "potato":     "potato",
    "brassica":   "brassica",
    "gourdguava": None,
    "solanacea":  None,
}
```

`VISION_DIR` is built from a **relative** default (`backend/ml_assets`), so
every path resolves against the process working directory. The backend must be
launched from the repository root, not from `backend/`. Nothing enforces this.

### 4.2 Registry coverage matrix

| Classifier output | `.lower()` key | In `CROP_TO_MODEL`? | Routes to | Weights exist? | Reachable? |
|---|---|---|---|---|---|
| `Brassica` | `brassica` | yes | `brassica_disease` | yes | ✅ |
| `Corn` | `corn` | yes | `corn_disease` | yes | ✅ |
| `GourdGuava` | `gourdguava` | yes → `None` | — | n/a | ⛔ no model |
| `Potato` | `potato` | yes | `potato_disease` | yes | ✅ |
| `Solanacea` | `solanacea` | yes → `None` | — | n/a | ⛔ no model |
| `Wheat` | `wheat` | yes | `wheat_disease` | placeholder | ⛔ blocked by guard |
| *(none)* | `rice` | yes | `rice_disease` | yes | ⛔ **unreachable** |

Only **three of six** classifier outputs produce a real diagnosis. The rice
model — the best-verified of the disease models at 8 classes and 3.21 MB — can
never be selected, because `crop_classifier` has no `Rice` class to emit.

### 4.3 Lazy initialisation

```
module import time
   │
   ├── _crop_classifier = None          ← no weights touched
   └── _disease_models  = {}            ← no weights touched
                                            memory: ~0
   ▼
first POST /api/classify or /api/detect
   │
   ├── get_crop_classifier()
   │      exists? ──no──► HTTPException(500, "Crop classifier model not found")
   │      yes ──► YOLO(path) ──► _crop_classifier              +12.55 MB
   ▼
first POST /api/detect that routes to potato
   │
   └── get_disease_model("potato")
          in cache? ──yes──► return
          no ──► exists? ──no──► HTTPException(500, "Disease model not found ...")
                 yes ──► YOLO(path) ──► _disease_models["potato"]  +11.03 MB
```

Cached in plain module-level globals. Consequences:

- **Process-local.** Multiple uvicorn workers each hold their own copies. At
  full saturation that is 12.55 + 3.21 + 11.03 + 11.03 + 11.05 + 12.55 ≈ 61 MB
  of weights per worker, plus torch runtime overhead.
- **No eviction.** Once loaded, a model stays for the process lifetime. Fine
  for a demo, unbounded in principle.
- **Not thread-safe.** Two concurrent first-requests for the same crop can both
  observe a cache miss and both construct a `YOLO`. The loser's instance is
  garbage-collected; the cost is a duplicated load, not corruption.
- **Cold-start latency lands on the first user.** The `lifespan` hook in
  `main.py` is an empty `yield`, so nothing warms up at boot. For a live demo
  this is the single highest-risk behaviour in the subsystem — see
  `WORKFLOW.md` §7.

### 4.4 Placeholder guard

Routing consults the filesystem, not the registry, to detect a fake model:

```
VISION_DIR / f"{disease_model_key}_disease" / "PLACEHOLDER_WARNING.json"
   exists ──► short-circuit with a 200 response carrying
              disease = "Disease model not available (placeholder)"
```

Only `wheat_disease/` carries this file. The guard is checked **before**
`get_disease_model()`, so the placeholder weights are never loaded — which is
why wheat costs zero memory despite being 12.55 MB on disk.

Using file presence as a feature flag is unusual but has a real advantage here:
removing the flag is how you promote a real model, and it cannot drift from the
weights directory because it lives inside it.

---

## 5. Component interaction sequence

```
Client        FastAPI       orchestrator      registry        YOLO         disk
  │              │               │               │             │            │
  ├─POST /detect─►               │               │             │            │
  │              ├──handler──────►               │             │            │
  │              │               ├─content_type guard          │            │
  │              │               ├─read() + PIL decode         │            │
  │              │               │               │             │            │
  │              │               ├─get_crop_classifier()───────►            │
  │              │               │               ├─cache miss──┤            │
  │              │               │               ├─────────────┼─read .pt──►│
  │              │               │               │◄────────────┼────────────┤
  │              │               │◄──YOLO────────┤             │            │
  │              │               ├─predict_classification()────►            │
  │              │               │◄──probs──────────────────────┤           │
  │              │               │                                          │
  │              │               ├─CROP_TO_MODEL[key]  (in-memory dict)     │
  │              │               ├─PLACEHOLDER_WARNING.json exists?─────────►
  │              │               │◄──False──────────────────────────────────┤
  │              │               │                                          │
  │              │               ├─get_disease_model(key)──────►            │
  │              │               │               ├─cache miss──┤            │
  │              │               │               ├─────────────┼─read .pt──►│
  │              │               │◄──YOLO────────┤             │            │
  │              │               ├─predict_classification()────►            │
  │              │               │◄──probs──────────────────────┤           │
  │              │               │                                          │
  │              │               ├─load_disease_details(key)────────────────►
  │              │               │◄──JSON───────────────────────────────────┤
  │              │               ├─linear scan for class_name match         │
  │              │               │                                          │
  │              │◄──Pydantic────┤                                          │
  │◄──200 JSON───┤               │                                          │
```

Every step is synchronous and blocking. The handlers are declared `async def`,
but `YOLO.__call__` is CPU-bound synchronous torch work executed directly in the
event loop — it is not offloaded to a threadpool. A single inference therefore
blocks all other requests on that worker for its full duration.

For a single-presenter demo this is invisible. Under any concurrency it
serialises the entire API, including the unrelated Q&A endpoints.

---

## 6. Architectural properties

| Property | Current state | Notes |
|---|---|---|
| Statefulness | Stateless per request, except model cache | No session, no DB |
| Persistence | None | Vision decisions are **not** written to the `AGENTS.md §4` audit log |
| Observability | None | No logging, no timing, no metrics |
| Concurrency | Serialised by blocking inference in async handlers | See §5 |
| Failure mode | `HTTPException(500)` for missing weights; unhandled exceptions otherwise | See `WORKFLOW.md` §6 |
| Configuration | One setting (`ml_assets_dir`), relative path | No thresholds, no device selection |
| Device | CPU implicit | `.cpu()` is hardcoded in `predict_classification` |
| Model format | `.pt` (PyTorch) | `AGENTS.md §3` specifies ONNX export; `onnxruntime` is a dependency but unused here |

### 6.1 Deviations from `AGENTS.md`

Recording these rather than silently accepting them, per `AGENTS.md §2` rule 6.

| Locked decision | Actual | Assessment |
|---|---|---|
| YOLO `.pt` exported to ONNX for inference | `.pt` loaded directly via Ultralytics | Flag for review. ONNX would cut cold-start and drop the torch dependency, but costs export work `scripts/export_yolo_models.py` has not done. |
| YOLO used for *object detection* | All six models are `task=classify` | Flag for review. The poster/demo language should say "classification", not "detection", or the models should be retrained with boxes. |
| Routes in `api/classify.py`, `api/detect.py` | Routes in `services/vision_orchestrator.py`; the API files are dead stubs | Low risk, but the dead stubs should be deleted to avoid confusion. |
| Audit trail for pipeline decisions | Q&A pipeline only; vision logs nothing | Flag for review if the safety-metrics panel is meant to include image queries. |
