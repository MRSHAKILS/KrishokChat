# Vision Pipeline — Folder Structure

Layout of `backend/ml_assets/vision/`, the conventions it follows, and how the
orchestrator resolves paths into it.

---

## 1. Full tree

```
backend/ml_assets/vision/
│
├── crop_classifier/                    Stage 1 — routing model
│   ├── model.pt                        12.55 MB · 6 classes
│   └── class_names.json                index → class name
│
├── rice_disease/                       8 classes · unreachable (see MODELS.md §5)
│   ├── model.pt                         3.21 MB
│   ├── class_names.json
│   └── disease_details.json            Bengali KB, 8 entries
│
├── wheat_disease/                      PLACEHOLDER — not a wheat model
│   ├── model.pt                        12.55 MB · byte-copy of crop_classifier
│   ├── class_names.json                crop classes, not wheat diseases
│   ├── disease_details.json            Bengali KB, 6 entries — real content
│   └── PLACEHOLDER_WARNING.json        ◄── routing guard, blocks Stage 3
│
├── corn_disease/                       4 classes · no test images
│   ├── model.pt                        11.03 MB
│   ├── class_names.json
│   └── disease_details.json            Bengali KB, 4 entries
│
├── potato_disease/                     3 classes · best-verified
│   ├── model.pt                        11.03 MB
│   ├── class_names.json
│   └── disease_details.json            Bengali KB, 3 entries
│
├── brassica_disease/                   11 classes · largest set
│   ├── model.pt                        11.05 MB
│   ├── class_names.json
│   └── disease_details.json            Bengali KB, 11 entries
│
├── test_images/                        verification fixtures only
│   ├── crop_classifier/    0001.jpg  0002.jpg  0001.png
│   ├── rice_disease/       0001.jpg  0002.jpg
│   ├── potato_disease/     0001.jpg  0002.jpg
│   ├── brassica_disease/   0001.jpg  0002.jpg  0001.png  0002.webp
│   ├── corn_disease/       (empty)
│   └── wheat_disease/      (empty)
│
├── scripts/
│   └── 01_verify_models.py             offline verification harness
│
└── verification_report.json            last verification output
```

---

## 2. The core convention

Every model lives in a directory named `<key>_disease/`, except the classifier
which is `crop_classifier/`. Inside each, filenames are **fixed**:

| Filename | Required | Purpose |
|---|:---:|---|
| `model.pt` | yes | YOLO weights, loaded by Ultralytics |
| `class_names.json` | generated | index → class name, regenerated from weights |
| `disease_details.json` | for disease models | Bengali knowledge base |
| `PLACEHOLDER_WARNING.json` | only if fake | presence blocks the route |

This gives the orchestrator a purely computed path — no manifest, no per-model
config:

```python
VISION_DIR = Path(settings.ml_assets_dir) / "vision"

CROP_CLASSIFIER_PATH = VISION_DIR / "crop_classifier" / "model.pt"

DISEASE_MODEL_PATHS = {
    "potato": VISION_DIR / "potato_disease" / "model.pt",
    ...
}

# derived at call time, not from the registry:
VISION_DIR / f"{crop_key}_disease" / "disease_details.json"
VISION_DIR / f"{crop_key}_disease" / "PLACEHOLDER_WARNING.json"
```

Two of those four paths are built by f-string interpolation on the routing key.
The registry dict and the f-strings must therefore agree on the
`<key>_disease` naming — and nothing checks that they do. A model directory named
`potato_disease_v2/` would need edits in three separate places.

### Why "directory as unit"

The alternative — flat `weights/potato.pt`, `kb/potato.json` — would scatter one
model across several trees. Keeping weights, class map, KB, and status flag
together means a model is added or removed by touching exactly one directory,
and the placeholder flag physically cannot drift from the weights it describes.

---

## 3. File-by-file

### 3.1 `model.pt`

PyTorch checkpoint loaded by `YOLO(str(path))`. All six are classification heads
(`task=classify`), not detection heads — despite `AGENTS.md §3` describing YOLO
as the object-detection layer.

The class map is baked into the checkpoint and read as `model.names`. That makes
the weights the single source of truth for labels; `class_names.json` is a
derived cache, never an input.

`.pt` files should be treated as binary artefacts, not source. They are not
suitable for plain Git — Git LFS or an out-of-band download step is the right
handling for 61 MB of weights.

### 3.2 `class_names.json`

```json
{
  "0": "Potato__Early_Blight",
  "1": "Potato__Healthy_Leaf",
  "2": "Potato__Late_Blight"
}
```

Written by `scripts/01_verify_models.py` step 4, which dumps `model.names`
directly. Keys are stringified indices (JSON has no integer keys).

**Nothing at runtime reads these files.** `load_class_names()` exists in
`vision_orchestrator.py` but is never called — the orchestrator uses
`model.names` from the loaded weights instead. The files are documentation and
diffable evidence: a change in a model's class list shows up in a code review as
a JSON diff.

That is a reasonable role, but note the dead function should either be wired up
or deleted.

### 3.3 `disease_details.json`

The Bengali knowledge base. One file per disease model, hand-authored.

```json
{
  "potato_crop_library": {
    "crop_name": "Potato (আলু)",
    "total_classes": 3,
    "source_reference": "Screenshot provided by user",
    "classes": [
      {
        "class_name": "Early Blight (প্রারম্ভিক ব্লাস্ট)",
        "description_bn": "…",
        "cause_bn": "…",
        "solution_bn": "…"
      }
    ]
  }
}
```

| Level | Key | Notes |
|---|---|---|
| top | `<crop>_crop_library` | name varies per file; code iterates `.values()` so it does not matter |
| meta | `crop_name` | present in rice, wheat, corn, potato |
| meta | `crop_group` | **brassica only** — same role, different key |
| meta | `total_classes` | matches the model in all five files |
| meta | `source_reference` | provenance, e.g. `"Screenshot 2026-05-14 133222_2.png"` |
| array | `classes[]` | the only field the orchestrator reads |

All five files are UTF-8 and must be opened with `encoding="utf-8"` — the
orchestrator does this correctly. On Windows the default encoding would mangle
Bengali.

Three quality notes:

- **`crop_name` vs `crop_group`** — brassica is the odd one out. Nothing reads
  either field today, so the inconsistency is inert, but it will bite the first
  time a UI wants to display the crop's Bengali name.
- **`class_name` never matches the model label.** The KB stores
  `Early Blight (প্রারম্ভিক ব্লাস্ট)`; the model emits `Potato__Early_Blight`.
  This is why `disease_info` is always `null`. See `WORKFLOW.md` §4.
- **Citation markers leak into the text.** Three files contain literal
  `[cite: N]` markers inside `description_bn`, `cause_bn`, and `solution_bn` —
  an artefact of LLM-assisted authoring:

  | File | `[cite:` occurrences |
  |---|---:|
  | `brassica_disease/disease_details.json` | 136 |
  | `rice_disease/disease_details.json` | 101 |
  | `corn_disease/disease_details.json` | 54 |
  | `potato_disease/disease_details.json` | 0 |
  | `wheat_disease/disease_details.json` | 0 |

  291 markers total. They will render verbatim to farmers and should be stripped
  before the demo — a single regex pass (`\[cite:\s*\d+\]`) over the three files.

`source_reference` values point at screenshots rather than agricultural
authorities. For a system recommending fungicide application, provenance should
eventually trace to DAE / BARI / BRRI publications — worth flagging for the
research panel, where "sourced from screenshots" is a weak claim.

### 3.4 `PLACEHOLDER_WARNING.json`

Present in `wheat_disease/` only.

```json
{
  "model_name": "wheat_disease",
  "status": "PLACEHOLDER",
  "warning": "This model is a byte-identical copy of crop-classifier. It does NOT detect wheat diseases.",
  "real_classes": ["Brassica", "Corn", "GourdGuava", "Potato", "Solanacea", "Wheat"],
  "expected_classes": ["Wheat__Healthy", "Wheat__Leaf_Rust", "Wheat__Stem_Rust",
                       "Wheat__Stripe_Rust", "Wheat__Powdery_Mildew", "Wheat__Blast"],
  "action_needed": "Train a real wheat disease classifier or obtain weights",
  "sha256": "6F14484768E54F28C2EDC2C5D3858C2C1A57F18D7DE40A001A119CBC04240C94"
}
```

Only its **existence** is checked — `Path.exists()`, never `json.load()`. The
contents are for humans.

Using file presence as a feature flag is unconventional but well suited here:

- The flag lives beside the weights it describes and cannot be forgotten
  elsewhere.
- Promoting a real model is "replace `model.pt`, delete this file" — no code
  change.
- It records *why* the route is disabled, plus the SHA-256 that proves the
  duplication.

This directly satisfies `AGENTS.md §2` rule 5: rather than fabricating wheat
output, the system refuses and says so.

### 3.5 `test_images/<model>/`

Fixtures for `01_verify_models.py` only. Never read at runtime.

Naming is zero-padded sequential (`0001.jpg`, `0002.jpg`) with no ground-truth
label in the filename or any sidecar. So verification can confirm *that* a model
predicts, never *whether* it predicts correctly — a human has to read the
printed class name and judge.

Adding a `labels.json` per directory would upgrade the harness from a smoke test
to a (tiny) accuracy check:

```json
{ "0001.jpg": "Potato__Early_Blight", "0002.jpg": "Potato__Late_Blight" }
```

Coverage:

| Directory | Images | Read by harness | Gap |
|---|---:|---:|---|
| `crop_classifier/` | 3 | 3 | — |
| `rice_disease/` | 2 | 2 | — |
| `potato_disease/` | 2 | 2 | — |
| `brassica_disease/` | 4 | 3 | `.webp` not in the glob |
| `corn_disease/` | 0 | 0 | **routable path, never tested** |
| `wheat_disease/` | 0 | 0 | acceptable — placeholder |

The harness globs `*.jpg`, `*.png`, `*.jpeg` and caps at 5 images. The `.webp`
in `brassica_disease/` is silently skipped — worth noting since Pillow reads
WebP fine at runtime, so the API accepts a format the harness ignores.

### 3.6 `scripts/01_verify_models.py`

Standalone offline harness. Resolves `VISION_DIR` from its own file location
(`Path(__file__).resolve().parent.parent`), so it runs correctly from any
working directory — unlike the orchestrator, which depends on CWD (§4).

Per model it checks existence, loads weights, extracts and **writes**
`class_names.json`, reports `task`, runs up to 5 test images handling both
`.probs` and `.boxes` result shapes, and finally compares wheat's class list
against the crop classifier to detect the placeholder automatically.

The numbered `01_` prefix matches the convention in
`ml_assets/rag_index/scripts/`, implying a future `02_`, `03_` sequence
(export to ONNX, benchmark, and so on).

### 3.7 `verification_report.json`

Machine-readable output of the last harness run. Structure per model:

```json
{
  "potato_disease": {
    "name": "potato_disease",
    "classes": ["Potato__Early_Blight", "Potato__Healthy_Leaf", "Potato__Late_Blight"],
    "task": "classify",
    "model_size_mb": 11.03,
    "predictions": [
      { "image": "0001.jpg", "predicted_class": "Potato__Early_Blight",
        "confidence": 0.9764, "top3": [...] }
    ]
  }
}
```

`model_size_mb` is absent for `corn_disease` and `wheat_disease` because the
harness returns early — before recording size — when a model has no test images.
So an empty `test_images/` directory costs you the size field too.

This file is the source of every figure in `MODELS.md`. It is a generated
artefact and should be regenerated, never hand-edited.

---

## 4. Path resolution and the CWD dependency

```
settings.ml_assets_dir  =  "backend/ml_assets"      ← relative, from config.py
                                    │
                                    ▼
VISION_DIR = Path("backend/ml_assets") / "vision"
                                    │
                                    ▼
        resolved against the process working directory
```

The default is a **relative** path, so the backend must be started from the
repository root:

```bash
# correct — VISION_DIR resolves to <repo>/backend/ml_assets/vision
cd "D:\KrishokTech Advisory System"
uv run --directory backend fastapi dev app/main.py

# wrong — resolves to <repo>/backend/backend/ml_assets/vision
cd backend
uv run fastapi dev app/main.py
#   → HTTPException(500, "Crop classifier model not found")
```

The failure mode is a 500 with a message that reads like missing weights, when
the real cause is the working directory. That is a poor error for a live demo.

Two robust fixes:

1. **Anchor to the source tree** — derive the path from `__file__` the way the
   verification script does:
   ```python
   BACKEND_ROOT = Path(__file__).resolve().parents[2]
   VISION_DIR = BACKEND_ROOT / "ml_assets" / "vision"
   ```
2. **Set an absolute path in `.env`** — `ML_ASSETS_DIR=D:/KrishokTech Advisory System/backend/ml_assets`,
   with the variable documented in `.env.example` per `AGENTS.md §2` rule 4.

Option 1 removes the failure class entirely and needs no environment setup.

---

## 5. Adding a new crop

To add, for example, tomato:

```
1.  mkdir backend/ml_assets/vision/tomato_disease/
2.  cp <trained weights> tomato_disease/model.pt
3.  author tomato_disease/disease_details.json   (UTF-8, classes[] array)
4.  add to DISEASE_MODEL_PATHS:
        "tomato": VISION_DIR / "tomato_disease" / "model.pt"
5.  add to CROP_TO_MODEL:
        "tomato": "tomato"
6.  ensure crop_classifier emits a "Tomato" class      ◄── the hard part
7.  mkdir test_images/tomato_disease/ and add ≥2 images
8.  add "tomato_disease" to MODELS in 01_verify_models.py
9.  run the harness — regenerates class_names.json and the report
```

Steps 4, 5, and 8 are three separate hand-edits that must stay in sync with the
directory name. This is the main structural weakness of the layout: the
filesystem convention is strong enough to be discovered automatically, but the
code hardcodes it instead.

A directory scan would eliminate steps 4, 5, and 8:

```python
DISEASE_MODEL_PATHS = {
    d.name.removesuffix("_disease"): d / "model.pt"
    for d in VISION_DIR.iterdir()
    if d.is_dir() and d.name.endswith("_disease")
}
```

Step 6 remains genuinely hard — it needs a retrained crop classifier — and is
the same blocker that makes the existing rice model unreachable
(`MODELS.md` §5).

---

## 6. Version control

| Path | Track in Git? | Rationale |
|---|---|---|
| `*/model.pt` | LFS or out-of-band | 61 MB of binaries; plain Git will bloat the repo |
| `*/class_names.json` | yes | tiny, diffable, catches silent class changes |
| `*/disease_details.json` | yes | hand-authored source content |
| `*/PLACEHOLDER_WARNING.json` | yes | it *is* the status record |
| `test_images/**` | yes | small, and verification is meaningless without them |
| `scripts/*.py` | yes | source |
| `verification_report.json` | yes | generated, but useful as a reviewable snapshot |

Weights are the only real decision. Given a 7-day scope with a single engineer,
keeping them out of Git and documenting a download or copy step in
`backend/README.md` is simpler than introducing LFS mid-project.
