# Vision Pipeline — API Reference

HTTP contract for the two vision endpoints. Both are defined in
`backend/app/services/vision_orchestrator.py` and mounted on the root FastAPI
app with no prefix.

| Property | Value |
|---|---|
| Base URL (dev) | `http://localhost:8000` |
| Content type (request) | `multipart/form-data` |
| Content type (response) | `application/json` |
| Authentication | none — per `AGENTS.md §2` rule 1 |
| Rate limiting | none |
| CORS | `allow_origins=[settings.frontend_origin]`, default `http://localhost:3000` |
| Interactive docs | `http://localhost:8000/docs` |

---

## 1. Endpoint summary

| Method | Path | Stages | Purpose |
|---|---|---|---|
| `POST` | `/api/classify` | 1 (+ routing check) | Identify the crop only |
| `POST` | `/api/detect` | 1 → 2 → 3 → 4 | Full diagnosis with treatment |
| `GET` | `/health` | — | Liveness probe (not vision-specific) |

Use `/api/classify` when the UI wants to show "detected crop: Potato" before
committing to a full diagnosis, or to check `has_disease_model` and decide
whether to offer the detect action at all. Use `/api/detect` for the actual
advisory result. `/api/detect` re-runs Stage 1 internally — it does not accept a
crop hint, so calling both endpoints doubles the classification work.

---

## 2. `POST /api/classify`

Runs the crop classifier and reports whether a disease model exists for the
predicted crop. Does **not** load or run any disease model.

### Request

```http
POST /api/classify HTTP/1.1
Host: localhost:8000
Content-Type: multipart/form-data; boundary=----X
```

| Field | Type | Required | Constraints |
|---|---|:---:|---|
| `file` | file | yes | `Content-Type` must start with `image/` |

No size limit, no dimension limit, and no format allow-list are enforced by the
application. Decoding is delegated to Pillow, so anything Pillow reads
(JPEG, PNG, WebP, BMP, TIFF, GIF) will work; the image is converted to RGB.

### Response `200 OK`

Schema `CropClassificationResponse`:

| Field | Type | Description |
|---|---|---|
| `crop` | `string` | Top-1 class, original casing (e.g. `"Potato"`) |
| `confidence` | `float` | Top-1 softmax probability, rounded to 4 dp |
| `top3` | `array<object>` | Three highest-probability classes, descending |
| `top3[].class` | `string` | Class name |
| `top3[].confidence` | `float` | Probability, 4 dp |
| `has_disease_model` | `boolean` | `true` if `CROP_TO_MODEL[crop.lower()]` is non-null |

```json
{
  "crop": "Potato",
  "confidence": 0.9764,
  "top3": [
    { "class": "Potato",     "confidence": 0.9764 },
    { "class": "Solanacea",  "confidence": 0.0201 },
    { "class": "Brassica",   "confidence": 0.0035 }
  ],
  "has_disease_model": true
}
```

### `has_disease_model` semantics

`true` only means a routing entry exists. It does **not** guarantee a diagnosis:

| Crop | `has_disease_model` | `/api/detect` actually yields |
|---|:---:|---|
| `Potato` | `true` | real diagnosis |
| `Brassica` | `true` | real diagnosis |
| `Corn` | `true` | real diagnosis (untested — no test images) |
| `Wheat` | `true` | placeholder refusal message |
| `GourdGuava` | `false` | "no disease model" message |
| `Solanacea` | `false` | "no disease model" message |

Wheat is the trap: the flag says `true` because `CROP_TO_MODEL["wheat"]` is
`"wheat"`, but the placeholder guard in Stage 2 blocks the actual detection. A
client that gates its "Diagnose" button purely on this flag will offer the
action for wheat and then show a refusal. If that matters to the UI, either
extend the flag to consult `PLACEHOLDER_WARNING.json`, or add a separate
`placeholder` boolean.

### Errors

| Status | Body | Cause |
|---|---|---|
| 400 | `{"detail": "File must be an image"}` | `content_type` does not start with `image/` |
| 422 | FastAPI validation object | `file` field absent from the body |
| 500 | `{"detail": "Crop classifier model not found"}` | `crop_classifier/model.pt` missing |
| 500 | `{"detail": "Internal Server Error"}` | Corrupt image, corrupt weights, or any unhandled exception |

---

## 3. `POST /api/detect`

Full pipeline: crop classification, routing, disease classification, Bengali
knowledge base lookup.

### Request

```http
POST /api/detect HTTP/1.1
Host: localhost:8000
Content-Type: multipart/form-data; boundary=----X
```

| Field | Type | Required | Constraints |
|---|---|:---:|---|
| `file` | file | yes | `Content-Type` must start with `image/` |

Identical to `/api/classify`. There is no optional `crop` override — Stage 1
always runs.

### Response `200 OK`

Schema `DiseaseDetectionResponse`:

| Field | Type | Nullable | Description |
|---|---|:---:|---|
| `crop` | `string` | no | Crop from Stage 1 |
| `crop_confidence` | `float` | no | Stage 1 top-1 probability, 4 dp |
| `disease` | `string` | no | Disease class **or** a human-readable refusal message |
| `disease_confidence` | `float` | no | Stage 3 probability, 4 dp; `0.0` on refusal |
| `disease_info` | `object` | **yes** | Bengali KB entry, or `null` |
| `top3_diseases` | `array<object>` | no | Three highest disease probabilities; `[]` on refusal |

`disease_info` object, when present:

| Field | Type | Description |
|---|---|---|
| `class_name` | `string` | Human label with Bengali gloss |
| `description_bn` | `string` | Symptom description in Bengali |
| `cause_bn` | `string` | Causal agent and conditions in Bengali |
| `solution_bn` | `string` | Treatment and prevention in Bengali |

### 3.1 Success — full diagnosis

**Intended** response once the Stage 4 label matching is fixed
(`WORKFLOW.md` §4):

```json
{
  "crop": "Potato",
  "crop_confidence": 0.9764,
  "disease": "Potato__Early_Blight",
  "disease_confidence": 0.9764,
  "disease_info": {
    "class_name": "Early Blight (প্রারম্ভিক ব্লাস্ট)",
    "description_bn": "প্রারম্ভিক ব্লাস্ট আলু গাছের একটি সাধারণ ছত্রাকজনিত রোগ …",
    "cause_bn": "এই রোগের মূল কারণ হলো Alternaria solani ছত্রাক …",
    "solution_bn": "রোগ প্রতিরোধী জাত চাষ এবং ফসল পর্যায়ক্রম অনুসরণ …"
  },
  "top3_diseases": [
    { "class": "Potato__Early_Blight",  "confidence": 0.9764 },
    { "class": "Potato__Late_Blight",   "confidence": 0.0236 },
    { "class": "Potato__Healthy_Leaf",  "confidence": 0.0 }
  ]
}
```

**Actual** current response — `disease_info` is `null` because the model label
`Potato__Early_Blight` never string-matches the KB's
`Early Blight (প্রারম্ভিক ব্লাস্ট)`:

```json
{
  "crop": "Potato",
  "crop_confidence": 0.9764,
  "disease": "Potato__Early_Blight",
  "disease_confidence": 0.9764,
  "disease_info": null,
  "top3_diseases": [
    { "class": "Potato__Early_Blight",  "confidence": 0.9764 },
    { "class": "Potato__Late_Blight",   "confidence": 0.0236 },
    { "class": "Potato__Healthy_Leaf",  "confidence": 0.0 }
  ]
}
```

Clients must treat `disease_info: null` as expected and render a fallback,
not as an error.

### 3.2 Refusal — crop has no disease model

Returned for `GourdGuava` and `Solanacea`. Status is **200**, not an error — the
crop classification succeeded and is worth showing.

```json
{
  "crop": "Solanacea",
  "crop_confidence": 0.9683,
  "disease": "No disease model available for this crop",
  "disease_confidence": 0.0,
  "disease_info": null,
  "top3_diseases": []
}
```

### 3.3 Refusal — placeholder model

Returned for `Wheat`.

```json
{
  "crop": "Wheat",
  "crop_confidence": 0.9421,
  "disease": "Disease model not available (placeholder)",
  "disease_confidence": 0.0,
  "disease_info": null,
  "top3_diseases": []
}
```

### 3.4 Distinguishing success from refusal

The two refusal cases are signalled only by the **content of the `disease`
string**. There is no `status` field, no enum, and no boolean. A client must
either compare against the two literal strings or infer refusal from
`disease_confidence == 0.0 && top3_diseases.length == 0`.

Both approaches are brittle. Adding a discriminator would make the contract
self-describing:

```json
{ "status": "ok" | "no_model" | "placeholder", ... }
```

This is worth doing before the frontend is written against the current shape.

### Errors

| Status | Body | Cause |
|---|---|---|
| 400 | `{"detail": "File must be an image"}` | Bad `content_type` |
| 422 | FastAPI validation object | `file` field absent |
| 500 | `{"detail": "Crop classifier model not found"}` | Stage 1 weights missing |
| 500 | `{"detail": "Disease model not found for <crop>"}` | Stage 3 weights missing |
| 500 | `{"detail": "Internal Server Error"}` | `NameError` from the missing `json` import (currently every Stage 4 call), corrupt image, corrupt weights |

---

## 4. Example requests

### 4.1 Classify a crop

```bash
curl -X POST http://localhost:8000/api/classify \
  -F "file=@backend/ml_assets/vision/test_images/crop_classifier/0002.jpg"
```

### 4.2 Full diagnosis — potato

```bash
curl -X POST http://localhost:8000/api/detect \
  -F "file=@backend/ml_assets/vision/test_images/potato_disease/0001.jpg"
```

### 4.3 Full diagnosis — brassica

```bash
curl -X POST http://localhost:8000/api/detect \
  -F "file=@backend/ml_assets/vision/test_images/brassica_disease/0001.jpg"
```

### 4.4 Pretty-printed output

```bash
curl -sS -X POST http://localhost:8000/api/detect \
  -F "file=@backend/ml_assets/vision/test_images/potato_disease/0001.jpg" \
  | python -m json.tool --no-ensure-ascii
```

`--no-ensure-ascii` keeps the Bengali readable instead of printing `\uXXXX`
escapes.

### 4.5 Timing a cold vs. warm request

```bash
# cold — includes weight loading
curl -o /dev/null -sS -w "cold: %{time_total}s\n" \
  -X POST http://localhost:8000/api/detect \
  -F "file=@backend/ml_assets/vision/test_images/potato_disease/0001.jpg"

# warm — models cached in process
curl -o /dev/null -sS -w "warm: %{time_total}s\n" \
  -X POST http://localhost:8000/api/detect \
  -F "file=@backend/ml_assets/vision/test_images/potato_disease/0002.jpg"
```

### 4.6 Verifying the 400 guard

```bash
echo "not an image" > /tmp/notimage.txt
curl -i -X POST http://localhost:8000/api/detect \
  -F "file=@/tmp/notimage.txt;type=text/plain"
# → HTTP/1.1 400 Bad Request
#   {"detail":"File must be an image"}
```

Note this guard trusts the declared `type=`. Sending the same text file as
`type=image/png` passes the check and fails inside Pillow with a bare 500.

### 4.7 PowerShell equivalent

```powershell
$path = "backend\ml_assets\vision\test_images\potato_disease\0001.jpg"
$form = @{ file = Get-Item -LiteralPath $path }
Invoke-RestMethod -Uri "http://localhost:8000/api/detect" -Method Post -Form $form |
    ConvertTo-Json -Depth 5
```

### 4.8 Browser fetch

```ts
async function detect(file: File) {
  const body = new FormData();
  body.append("file", file);

  const res = await fetch("http://localhost:8000/api/detect", {
    method: "POST",
    body,                       // do NOT set Content-Type; the browser
  });                           // must supply the multipart boundary

  if (!res.ok) throw new Error(`detect failed: ${res.status}`);
  return res.json();
}
```

### 4.9 Health check

```bash
curl http://localhost:8000/health
# {"status":"ok","version":"0.1.0"}
```

`/health` does not touch any model. A healthy response says nothing about
whether the weights are present or loadable.

---

## 5. Client integration notes

### 5.1 Handling the response

```
  response.disease_confidence === 0.0 && response.top3_diseases.length === 0
      │
      ├── yes ──► refusal: show crop + confidence, render `disease` as an
      │           explanatory message, hide the treatment panel
      │
      └── no  ──► diagnosis: show crop, disease, confidence
                     │
                     ├── disease_info !== null ──► render Bengali
                     │                              description / cause / solution
                     └── disease_info === null ──► fallback: show the disease
                                                    name only, plus a link to
                                                    Krishi Call Center 16123
```

The `disease_info === null` fallback is not hypothetical — it is the current
behaviour of every successful request. Build it.

### 5.2 Agent trace

`AGENTS.md §4` calls for a visible stepper. The vision pipeline maps naturally
onto four steps, and the response carries enough information to reconstruct
which ones ran:

| Step label | Completed when |
|---|---|
| ফসল শনাক্তকরণ (Identifying crop) | `crop` is present |
| মডেল নির্বাচন (Selecting model) | always — routing is instantaneous |
| রোগ শনাক্তকরণ (Detecting disease) | `disease_confidence > 0` |
| পরামর্শ প্রস্তুত (Preparing advice) | `disease_info !== null` |

Because the API is a single blocking request with no streaming, the frontend
cannot animate these from real progress events. Either animate optimistically on
a timer, or add a streaming variant later.

### 5.3 Safety framing

The vision pipeline does not pass through the safety agent from
`AGENTS.md §4` — that agent classifies text, and this endpoint takes an image.
However, `solution_bn` text can recommend named fungicides and pesticides. Any
UI rendering that text should carry the same Krishi Call Center **16123**
redirect that the Q&A pipeline uses, so chemical guidance always has a human
escalation path attached.

---

## 6. Known issues in the API layer

### 6.1 `app/api/vision.py` does not export `router` — startup fails

```python
"""Vision API routers for crop classification and disease detection."""
from app.services.vision_orchestrator import router as vision_router

__all__ = ["router"]
```

The import binds the name `vision_router`, but `__all__` advertises `router`,
which is never defined in this module. `main.py` does:

```python
from app.api.vision import router as vision_router
```

That raises at import time:

```
ImportError: cannot import name 'router' from 'app.api.vision'
```

Confirmed by executing the import against the current tree. **The backend does
not start.** Fix — drop the alias:

```python
from app.services.vision_orchestrator import router

__all__ = ["router"]
```

### 6.2 Missing `json` import — every Stage 4 call raises

`vision_orchestrator.py` calls `json.load()` in `load_class_names()` and
`load_disease_details()` but never imports `json`. Every `/api/detect` request
that reaches Stage 4 raises `NameError` and returns a bare 500.

Fix — add `import json` to the stdlib import block.

### 6.3 Dead stub routers

`app/api/classify.py` and `app/api/detect.py` still contain the bootstrap
placeholders:

```python
@router.post("/api/classify")
async def classify_endpoint():
    return {"status": "not_implemented", "message": "TASK_04 will implement this endpoint"}
```

`main.py` imports both (`classify_router`, `detect_router`) but never calls
`include_router` on them, so they are inert. They are still a hazard: anyone
adding `app.include_router(classify_router)` would silently shadow or duplicate
the real routes depending on registration order. Delete both files and remove
the imports.

### 6.4 No request size limit

Neither endpoint bounds the upload. A large TIFF will be read fully into memory
via `await file.read()`, then decoded by Pillow, then held as an RGB array. On a
demo laptop a sufficiently large upload is an OOM.

Adding a size check before decode is cheap:

```python
MAX_BYTES = 10 * 1024 * 1024
if len(contents) > MAX_BYTES:
    raise HTTPException(413, "Image too large (max 10 MB)")
```

### 6.5 No confidence floor in the contract

The response has no way to express "I am not confident". An out-of-domain image
returns a top-1 class with a rounded confidence and is structurally identical to
a correct diagnosis. Given that `solution_bn` can recommend chemical
application, a `low_confidence` response variant — mirroring the Q&A pipeline's
category of the same name — belongs in this contract.

### 6.6 Blocking inference in async handlers

Both handlers are `async def`, but `YOLO.__call__` is synchronous CPU work run
directly on the event loop. One in-flight inference blocks every other request
on the worker, including `/health` and the Q&A endpoints. Wrapping the two
inference calls in `fastapi.concurrency.run_in_threadpool` restores
responsiveness.

### 6.7 Summary

| # | Issue | Severity | Fix size |
|---|---|---|---|
| 6.1 | `router` not exported → backend will not start | **Blocking** | 1 line |
| 6.2 | `json` not imported → Stage 4 always 500s | **Blocking** | 1 line |
| 6.3 | Dead stub routers | Low | delete 2 files |
| 6.4 | No upload size limit | Medium | 3 lines |
| 6.5 | No low-confidence response variant | High (advisory safety) | ~15 lines |
| 6.6 | Blocking inference serialises the API | Medium | 2 lines |
