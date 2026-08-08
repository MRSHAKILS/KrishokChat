# Vision Pipeline — Workflow

Step-by-step walkthrough of the four pipeline stages, with the error branch at
each stage drawn explicitly. Source: `backend/app/services/vision_orchestrator.py`.

---

## 0. End-to-end control flow

```
                        POST /api/detect  (multipart: file)
                                    │
                                    ▼
                  ┌─────────────────────────────────┐
                  │  GATE 0 — Input validation      │
                  │  content_type.startswith("image/")
                  └────────────┬──────────────┬─────┘
                          fail │              │ pass
                               ▼              ▼
                        400 Bad Request   PIL decode → RGB
                                               │
                                               ▼
      ╔════════════════════════════════════════════════════════════╗
      ║  STAGE 1 — CROP CLASSIFICATION                             ║
      ║  crop_classifier/model.pt · 6 classes                      ║
      ╚════════════════════════════════════╤═══════════════════════╝
                                           │ crop_class, crop_conf
                                           ▼
      ╔════════════════════════════════════════════════════════════╗
      ║  STAGE 2 — DISEASE MODEL ROUTING                           ║
      ║  CROP_TO_MODEL lookup + PLACEHOLDER guard                  ║
      ╚═══════╤════════════════════╤═══════════════════╤═══════════╝
              │ None               │ placeholder       │ routable
              ▼                    ▼                   ▼
      200 "No disease model"  200 "placeholder"   continue
                                                       │
                                                       ▼
      ╔════════════════════════════════════════════════════════════╗
      ║  STAGE 3 — DISEASE DETECTION                               ║
      ║  <crop>_disease/model.pt · 3–11 classes                    ║
      ╚════════════════════════════════════╤═══════════════════════╝
                                           │ disease_class, disease_conf
                                           ▼
      ╔════════════════════════════════════════════════════════════╗
      ║  STAGE 4 — DISEASE DETAILS LOOKUP                          ║
      ║  <crop>_disease/disease_details.json                       ║
      ╚════════════════════════════════════╤═══════════════════════╝
                                           │
                                           ▼
                              200 DiseaseDetectionResponse
```

`POST /api/classify` executes Gate 0 and Stage 1 only, then returns a
`has_disease_model` boolean derived from the Stage 2 lookup — it performs the
routing decision without acting on it.

---

## 1. Stage 1 — Crop Classification

**Goal:** identify which of six crop groups the photograph shows.

```
   Image (RGB)
       │
       ▼
 ┌───────────────────────────────────────────────────────┐
 │ get_crop_classifier()                                 │
 │                                                       │
 │   _crop_classifier is None? ──no──► return cached     │
 │            │ yes                                      │
 │            ▼                                          │
 │   CROP_CLASSIFIER_PATH.exists()?                      │
 │            │                                          │
 │      no ───┴──► HTTPException(500,                    │
 │                  "Crop classifier model not found")   │
 │            │ yes                                      │
 │            ▼                                          │
 │   YOLO(path) → cache in module global                 │
 └────────────────────────┬──────────────────────────────┘
                          │
                          ▼
 ┌───────────────────────────────────────────────────────┐
 │ predict_classification(model, image)                  │
 │                                                       │
 │   results = model(image, verbose=False)[0]            │
 │   probs   = results.probs.data.cpu().numpy()          │
 │   order   = np.argsort(probs)[::-1]                   │
 │                                                       │
 │   ┌─────────────────────────────────────────────┐     │
 │   │ top_prediction : {class, confidence}        │     │
 │   │ top3           : [{class, confidence} × 3]  │     │
 │   │ all_probabilities : {class: conf} × 6       │     │
 │   └─────────────────────────────────────────────┘     │
 └────────────────────────┬──────────────────────────────┘
                          │
                          ▼
        crop_class = "Potato"      crop_conf = 0.9764
        crop_key   = "potato"      (lowercased for routing)
```

### Class vocabulary

| Index | Class | Covers |
|---:|---|---|
| 0 | `Brassica` | cabbage, cauliflower |
| 1 | `Corn` | maize |
| 2 | `GourdGuava` | gourd family + guava (mixed group) |
| 3 | `Potato` | potato |
| 4 | `Solanacea` | tomato, brinjal, chilli (nightshades) |
| 5 | `Wheat` | wheat |

There is no `Rice` class. See §8 issue R-1.

### Error handling — Stage 1

| Condition | Detection point | Result | Status |
|---|---|---|---|
| Non-image upload | `content_type` guard | `HTTPException(400, "File must be an image")` | 400 |
| Missing `crop_classifier/model.pt` | `get_crop_classifier()` | `HTTPException(500, "Crop classifier model not found")` | 500 |
| Corrupt image bytes | none | `PIL.UnidentifiedImageError` escapes → unhandled | 500 generic |
| Corrupt `.pt` weights | none | Ultralytics/torch exception escapes | 500 generic |
| Model returns no `.probs` | `predict_classification` returns `{"error": ...}` | caller indexes `["top_prediction"]` → `KeyError` | 500 generic |
| Missing `file` field | FastAPI validation | `422 Unprocessable Entity` | 422 |
| `content_type` is `None` | none | `AttributeError` on `.startswith` | 500 generic |

The `content_type` guard trusts a client-supplied header. A `.exe` renamed and
sent with `Content-Type: image/png` passes the gate and fails later inside PIL
with an opaque 500. Sniffing magic bytes after decode would be a two-line
improvement.

---

## 2. Stage 2 — Disease Model Routing

**Goal:** pick the crop-specific disease model, or refuse cleanly. No inference
runs in this stage; it is a dict lookup plus one filesystem probe.

```
        crop_key  (e.g. "potato")
             │
             ▼
 ┌────────────────────────────────────────────────────────────┐
 │ disease_model_key = CROP_TO_MODEL.get(crop_key)            │
 └──────────────┬─────────────────────────────────────────────┘
                │
     ┌──────────┴───────────┬───────────────────────┐
     │                      │                       │
   None                unknown key              a model key
 (gourdguava,          (.get → None,            (rice/wheat/corn/
  solanacea)            same branch)             potato/brassica)
     │                      │                       │
     └──────────┬───────────┘                       │
                ▼                                   ▼
   ┌─────────────────────────────┐   ┌──────────────────────────────────┐
   │ EARLY RETURN — 200 OK       │   │ PLACEHOLDER PROBE                │
   │ disease = "No disease model │   │ VISION_DIR /                     │
   │   available for this crop"  │   │  f"{key}_disease" /              │
   │ disease_confidence = 0.0    │   │  "PLACEHOLDER_WARNING.json"      │
   │ disease_info = None         │   │        .exists()                 │
   │ top3_diseases = []          │   └──────┬──────────────┬────────────┘
   └─────────────────────────────┘     true │              │ false
                                            ▼              ▼
                            ┌─────────────────────────┐  proceed to
                            │ EARLY RETURN — 200 OK   │  Stage 3
                            │ disease = "Disease      │
                            │  model not available    │
                            │  (placeholder)"         │
                            │ confidence = 0.0        │
                            │ disease_info = None     │
                            └─────────────────────────┘
```

### Routing table

| `crop_key` | Value | Outcome |
|---|---|---|
| `rice` | `"rice"` | routable — but unreachable, no `Rice` classifier class |
| `wheat` | `"wheat"` | blocked by placeholder guard |
| `corn` | `"corn"` | routable |
| `potato` | `"potato"` | routable |
| `brassica` | `"brassica"` | routable |
| `gourdguava` | `None` | early return, no model |
| `solanacea` | `None` | early return, no model |

Both `None` values and absent keys collapse into the same branch because
`.get()` returns `None` for a miss. That is convenient but erases a real
distinction: `gourdguava` is a *known crop we chose not to support*, whereas an
unexpected key would be *a bug in the classifier or the table*. Both surface to
the farmer as the same message.

### Error handling — Stage 2

| Condition | Handled? | Result |
|---|---|---|
| Crop has no disease model | yes, explicit | 200 with explanatory `disease` string |
| Crop is a placeholder model | yes, explicit | 200 with placeholder message |
| Unknown crop key | implicitly, via `.get()` → `None` | 200, same message as "no model" |
| `PLACEHOLDER_WARNING.json` unreadable | n/a — only `.exists()` is called | no read, cannot fail |

Both refusals return **HTTP 200**, not an error code. This is the right choice:
"this crop has no disease model" is a successful classification with a partial
answer, not a server failure. The client renders `crop` and `crop_confidence`
normally and shows the `disease` string as an explanation. A 4xx/5xx would push
the UI into an error state and discard the valid crop result.

---

## 3. Stage 3 — Disease Detection

**Goal:** classify the specific disease within the routed crop's class set.

```
    disease_model_key = "potato"
             │
             ▼
 ┌───────────────────────────────────────────────────────┐
 │ get_disease_model(key)                                │
 │                                                       │
 │   key in _disease_models? ──yes──► return cached      │
 │            │ no                                       │
 │            ▼                                          │
 │   path = DISEASE_MODEL_PATHS.get(key)                 │
 │   not path or not path.exists()?                      │
 │            │                                          │
 │      yes ──┴──► HTTPException(500,                    │
 │                  f"Disease model not found for {key}")│
 │            │ no                                       │
 │            ▼                                          │
 │   YOLO(path) → _disease_models[key]                   │
 └────────────────────────┬──────────────────────────────┘
                          │
                          ▼
 ┌───────────────────────────────────────────────────────┐
 │ predict_classification(disease_model, image)          │
 │   ↑ same Image object decoded in Gate 0 —             │
 │     not re-read, not re-decoded                       │
 └────────────────────────┬──────────────────────────────┘
                          │
                          ▼
     disease_class = "Potato__Early_Blight"
     disease_conf  = 0.9764
     top3          = [Early_Blight 0.9764,
                      Late_Blight  0.0236,
                      Healthy_Leaf 0.0000]
```

### Class-set size per route

```
  brassica ████████████ 11 classes
  rice     ████████      8
  corn     ████          4
  potato   ███           3
  wheat    ░░░░░░        6  (placeholder — never reached)
```

Smaller class sets mean the routing decision has already done most of the
discrimination work. A potato image only ever has to be sorted into three
buckets.

### Error handling — Stage 3

| Condition | Detection point | Result |
|---|---|---|
| Weights file absent | `get_disease_model()` | `HTTPException(500, "Disease model not found for <key>")` |
| Key absent from `DISEASE_MODEL_PATHS` | same guard (`not path`) | same 500 |
| Corrupt weights | none | torch exception → generic 500 |
| Model without `.probs` | `predict_classification` returns error dict | `KeyError` on `["top_prediction"]` → generic 500 |
| Low confidence prediction | **not checked** | returned as a confident answer |

There is no confidence floor anywhere in the pipeline. An out-of-domain image —
a hand, a sky, a receipt — still produces a top-1 class and a rounded
confidence, and the response is structurally indistinguishable from a correct
diagnosis. For an advisory system that recommends fungicide application, that is
the most consequential gap in the workflow. See §8 issue R-4.

---

## 4. Stage 4 — Disease Details Lookup

**Goal:** attach Bengali description, cause, and treatment to the predicted
disease.

```
    disease_class = "Potato__Early_Blight"
    disease_model_key = "potato"
             │
             ▼
 ┌───────────────────────────────────────────────────────┐
 │ load_disease_details("potato")                        │
 │   path = VISION_DIR/"potato_disease"/                 │
 │            "disease_details.json"                     │
 │   exists? ──no──► return None                         │
 │   yes ──► json.load(f)   ⚠ NameError: json undefined  │
 └────────────────────────┬──────────────────────────────┘
                          │ details dict
                          ▼
 ┌───────────────────────────────────────────────────────┐
 │ for crop_data in details.values():        ← 1 entry   │
 │     for cls in crop_data.get("classes", []):          │
 │         if cls["class_name"] == disease_class:        │
 │             disease_info = cls                        │
 │             break        ← escapes inner loop only    │
 └────────────────────────┬──────────────────────────────┘
                          │
                          ▼
              disease_info = matching dict | None
```

### Knowledge base shape

```
potato_disease/disease_details.json
└── "potato_crop_library"              ← key name varies per crop
    ├── "crop_name":        "Potato (আলু)"
    ├── "total_classes":    3
    ├── "source_reference": "..."
    └── "classes": [
          { "class_name":     "Early Blight (আগাম ধসা রোগ)",
            "description_bn": "…",
            "cause_bn":       "…",
            "solution_bn":    "…" },
          …
        ]
```

The `brassica` file uses `crop_group` instead of `crop_name`; the rest use
`crop_name`. Nothing reads either field, so the inconsistency is currently inert.

### The label mismatch

Stage 3 emits model labels. Stage 4 stores human labels. They never compare
equal:

| Model label (Stage 3) | KB `class_name` (Stage 4) | Match? |
|---|---|---|
| `Potato__Early_Blight` | `Early Blight (আগাম ধসা রোগ)` | ✗ |
| `Potato__Late_Blight` | `Late Blight (নাবি ধসা …)` | ✗ |
| `Potato__Healthy_Leaf` | `Healthy Leaf (সুস্থ পাতা)` | ✗ |
| `Rice__Brown_Spot` | `Brown Spot (বাদামি দাগ রোগ)` | ✗ |
| `Common_Rust` | `Common Rust (সাধারণ মরিচা রোগ)` | ✗ |
| `Cauliflower__Downy_Mildew` | `Cauliflower Downy Mildew (…)` | ✗ |

`disease_info` is therefore `null` in **every** successful response. The
pipeline runs, predicts correctly, and then silently drops the entire treatment
payload — the part the farmer actually needs.

A normalisation function would close it:

```python
def normalise(label: str) -> str:
    return label.replace("__", " ").replace("_", " ").strip().lower()

# match on normalise(cls["class_name"].split("(")[0]) == normalise(disease_class)
```

`Cauliflower__Downy_Mildew` → `cauliflower downy mildew`, and the KB's
`Cauliflower Downy Mildew (ফুলকপির …)` → strip the paren gloss →
`cauliflower downy mildew`. Match. This holds for all 32 classes; the corn set
needs the missing `Corn__` prefix accounted for, since its model labels are bare
(`Common_Rust`) while its KB entries are also bare (`Common Rust (…)`) — so corn
happens to work under the same rule.

### Error handling — Stage 4

| Condition | Handled? | Result |
|---|---|---|
| `json` not imported | **no** | `NameError` → generic 500 on every call reaching Stage 4 |
| KB file missing | yes | `load_disease_details` returns `None`, `disease_info` stays `None` |
| No matching `class_name` | yes, by omission | `disease_info` is `None`, response still 200 |
| Malformed JSON | no | `json.JSONDecodeError` escapes |
| `classes` key absent | yes | `.get("classes", [])` defaults to empty list |
| Wrong encoding | mitigated | opened with `encoding="utf-8"` — required for Bengali |

Issue R-2 (`json` never imported) means Stage 4 currently crashes the request
before the mismatch in the previous section can even manifest. Fix the import
first, then the label matching.

---

## 5. Worked example — potato early blight

```
INPUT   backend/ml_assets/vision/test_images/potato_disease/0001.jpg

Gate 0  content_type = "image/jpeg"                      ✓ pass
        PIL decode → RGB                                 ✓

Stage 1 crop_classifier cold load                        +12.55 MB
        probs → Potato 0.9764 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░
                Late…  n/a
        crop_class = "Potato"   crop_key = "potato"

Stage 2 CROP_TO_MODEL["potato"] → "potato"               ✓ routable
        potato_disease/PLACEHOLDER_WARNING.json          ✗ absent
        → proceed

Stage 3 potato_disease cold load                         +11.03 MB
        Potato__Early_Blight 0.9764 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░
        Potato__Late_Blight  0.0236 ▓
        Potato__Healthy_Leaf 0.0000

Stage 4 load potato_disease/disease_details.json
        scan 3 entries for "Potato__Early_Blight"
        → no match (KB stores "Early Blight (আগাম ধসা রোগ)")
        disease_info = None

OUTPUT  { "crop": "Potato", "crop_confidence": 0.9764,
          "disease": "Potato__Early_Blight",
          "disease_confidence": 0.9764,
          "disease_info": null,                ← should be the Bengali payload
          "top3_diseases": [...] }
```

---

## 6. Error handling summary

### 6.1 By HTTP status

| Status | Trigger | Where |
|---|---|---|
| 200 | Full success | Stage 4 |
| 200 | Crop has no disease model | Stage 2 |
| 200 | Crop maps to a placeholder model | Stage 2 |
| 400 | `content_type` does not start with `image/` | Gate 0 |
| 422 | `file` field missing from multipart body | FastAPI validation |
| 500 | Crop classifier weights missing | Stage 1 |
| 500 | Disease model weights missing | Stage 3 |
| 500 | Any unhandled exception (PIL, torch, `NameError`, `KeyError`) | anywhere |

### 6.2 Handled vs unhandled

```
  HANDLED — explicit, actionable
  ├── non-image content type               → 400, clear message
  ├── missing crop classifier              → 500, clear message
  ├── missing disease model                → 500, names the crop
  ├── no disease model for crop            → 200, partial answer preserved
  ├── placeholder model                    → 200, partial answer preserved
  ├── KB file absent                       → disease_info = null
  └── KB has no matching class             → disease_info = null

  UNHANDLED — leaks a generic 500
  ├── corrupt / non-decodable image        → PIL.UnidentifiedImageError
  ├── content_type is None                 → AttributeError
  ├── corrupt or incompatible weights      → torch / Ultralytics exception
  ├── model without .probs                 → KeyError on ["top_prediction"]
  ├── json not imported (R-2)              → NameError, every Stage 4 call
  └── malformed disease_details.json       → JSONDecodeError
```

### 6.3 What the farmer sees

Every unhandled case produces FastAPI's default
`{"detail": "Internal Server Error"}`. There is no fallback message, no
Bengali error string, and no guidance to retake the photograph. For a live
demo, a corrupt or oversized upload becomes an unexplained failure on screen.

The minimum viable fix is a single `try/except` around the decode-and-infer
block returning a 422 with an instruction to re-upload a clearer photo.

---

## 7. Cold start behaviour

`main.py` defines a lifespan hook that does nothing:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
```

So the first request pays for weight loading:

```
  t=0     POST /api/detect arrives
  │
  ├─ torch import already warm (module import time)
  ├─ YOLO(crop_classifier)        ~1–3 s cold      ◄── first user waits
  ├─ inference                    ~50–200 ms
  ├─ YOLO(potato_disease)         ~1–3 s cold      ◄── first user waits
  ├─ inference                    ~50–200 ms
  └─ KB read + scan               <5 ms
  t≈2–6 s  response

  second request, same crop:
  t=0 ─► cached ─► inference ─► inference ─► KB ─► t≈100–400 ms
```

For the 3–4 minute investor demo this is the highest-risk behaviour in the
subsystem: the very first image upload — the one being demonstrated — is the
slow one. Warming the crop classifier plus the crops that will actually be
demoed inside the lifespan hook removes the risk entirely:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    get_crop_classifier()
    for key in ("potato", "brassica", "corn"):
        get_disease_model(key)
    yield
```

Cost: a few seconds at boot and ~46 MB resident. Benefit: the demo never shows a
multi-second stall. Note that `get_*` raise `HTTPException` outside a request
context, so warming should be wrapped in `try/except` or the loaders refactored
to raise plain exceptions.

---

## 8. Open issues affecting the workflow

| ID | Issue | Stage | Severity | Fix size |
|---|---|---|---|---|
| R-1 | `crop_classifier` has no `Rice` class, so the 8-class rice model is unreachable | 2 | High | Retrain classifier, or accept rice is out of scope and remove the route |
| R-2 | `json` used but never imported | 4 | Blocking | one line |
| R-3 | Model labels never match KB `class_name`, so `disease_info` is always `null` | 4 | High | ~5 lines, normalisation helper |
| R-4 | No confidence threshold at any stage | 1, 3 | High | ~10 lines, plus an "uncertain" response shape |
| R-5 | `app/api/vision.py` never binds `router`, so the import in `main.py` fails | boot | Blocking | one line |
| R-6 | `wheat_disease` is a copy of the crop classifier | 2 | Known, guarded | Train real model |
| R-7 | Corrupt-image and generic exceptions leak bare 500s | all | Medium | one `try/except` |
| R-8 | Blocking inference inside `async def` serialises the API | 1, 3 | Medium | `run_in_threadpool` |
| R-9 | No cold-start warming | 1, 3 | Medium (demo risk) | ~5 lines in lifespan |
| R-10 | Vision decisions are never logged; no audit trail | all | Low for demo | Reuse the Q&A JSONL logger |

R-2 and R-5 must be fixed before the pipeline runs at all. R-3 must be fixed
before the pipeline is *useful*, since without it the treatment advice — the
entire point of the feature — never reaches the response.
