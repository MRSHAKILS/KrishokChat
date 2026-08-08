# Vision Pipeline — Diagrams

All ASCII diagrams for the vision subsystem, collected for reference and for
lifting into the poster or demo slides.

**Contents**

1. [End-to-end pipeline flow](#1-end-to-end-pipeline-flow)
2. [Agentic workflow — crop → disease → details](#2-agentic-workflow--crop--disease--details)
3. [Model loading and lazy initialisation](#3-model-loading-and-lazy-initialisation)
4. [Request/response lifecycle](#4-requestresponse-lifecycle)
5. [Routing decision tree](#5-routing-decision-tree)
6. [Error propagation map](#6-error-propagation-map)
7. [Class-space narrowing](#7-class-space-narrowing)
8. [Poster-sized summary](#8-poster-sized-summary)

---

## 1. End-to-end pipeline flow

```
        ┌───────────────────┐
        │      FARMER       │
        │  photographs a    │
        │  diseased leaf    │
        └─────────┬─────────┘
                  │
                  ▼
     ┌─────────────────────────┐
     │  Next.js frontend       │
     │  file input → FormData  │
     └────────────┬────────────┘
                  │  POST /api/detect
                  │  multipart/form-data
                  ▼
╔══════════════════════════════════════════════════════════════════════╗
║                     FastAPI  ·  vision_orchestrator                  ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║   ┌────────────────────────────────────────────────────────────┐     ║
║   │ GATE 0 · INPUT VALIDATION                                  │     ║
║   │   content_type.startswith("image/")   ──fail──► 400        │     ║
║   │   await file.read()          → bytes                       │     ║
║   │   Image.open(BytesIO).convert("RGB")  → Image              │     ║
║   └───────────────────────────┬────────────────────────────────┘     ║
║                               │  ONE decode, reused by both models   ║
║                               ▼                                      ║
║   ┌────────────────────────────────────────────────────────────┐     ║
║   │ STAGE 1 · CROP CLASSIFICATION                              │     ║
║   │   crop_classifier/model.pt   ·  6 classes  ·  12.55 MB     │     ║
║   │   → crop="Potato"  conf=0.9764                             │     ║
║   └───────────────────────────┬────────────────────────────────┘     ║
║                               │  crop_key = crop.lower()             ║
║                               ▼                                      ║
║   ┌────────────────────────────────────────────────────────────┐     ║
║   │ STAGE 2 · ROUTING            (no inference — dict + stat)  │     ║
║   │   CROP_TO_MODEL[crop_key]                                  │     ║
║   │   PLACEHOLDER_WARNING.json exists?                         │     ║
║   └──────┬─────────────────┬───────────────────┬───────────────┘     ║
║          │ None            │ placeholder       │ routable            ║
║          ▼                 ▼                   ▼                     ║
║    200 "no model"    200 "placeholder"    ┌─────────────────────┐    ║
║    (partial answer)  (partial answer)     │ STAGE 3 · DISEASE   │    ║
║                                           │  <crop>_disease/    │    ║
║                                           │  3–11 classes       │    ║
║                                           │  → Early_Blight     │    ║
║                                           │    0.9764           │    ║
║                                           └──────────┬──────────┘    ║
║                                                      ▼               ║
║                                           ┌─────────────────────┐    ║
║                                           │ STAGE 4 · DETAILS   │    ║
║                                           │  disease_details    │    ║
║                                           │    .json lookup     │    ║
║                                           │  → বাংলা advice     │    ║
║                                           └──────────┬──────────┘    ║
╚══════════════════════════════════════════════════════╪═══════════════╝
                                                       ▼
                                        ┌──────────────────────────┐
                                        │  200 JSON                │
                                        │  crop, confidence,       │
                                        │  disease, confidence,    │
                                        │  disease_info (Bengali), │
                                        │  top3_diseases           │
                                        └──────────────────────────┘
```

---

## 2. Agentic workflow — crop → disease → details

Each stage answers one question and hands a narrowed problem to the next. This
is the diagram to put on the poster.

```
   ┌──────────────────────────────────────────────────────────────────┐
   │  Q1  "What crop is this?"                                        │
   │                                                                  │
   │      ┌──────────────────┐                                        │
   │      │ CROP CLASSIFIER  │   search space: 6 crop groups          │
   │      │   YOLO classify  │                                        │
   │      └────────┬─────────┘                                        │
   │               │                                                  │
   │   Brassica · Corn · GourdGuava · Potato · Solanacea · Wheat      │
   └───────────────┼──────────────────────────────────────────────────┘
                   │  answer: Potato (0.9764)
                   ▼
   ┌──────────────────────────────────────────────────────────────────┐
   │  Q2  "Which specialist should look at it?"                       │
   │                                                                  │
   │      ┌──────────────────┐                                        │
   │      │  ROUTING TABLE   │   no model, no inference               │
   │      │  CROP_TO_MODEL   │   pure lookup + placeholder probe      │
   │      └────────┬─────────┘                                        │
   │               │                                                  │
   │      potato → potato_disease/model.pt                            │
   └───────────────┼──────────────────────────────────────────────────┘
                   │  answer: the 3-class potato specialist
                   ▼
   ┌──────────────────────────────────────────────────────────────────┐
   │  Q3  "What is wrong with it?"                                    │
   │                                                                  │
   │      ┌──────────────────┐                                        │
   │      │ DISEASE MODEL    │   search space: 3 classes, not 32      │
   │      │   YOLO classify  │                                        │
   │      └────────┬─────────┘                                        │
   │               │                                                  │
   │   Early_Blight · Healthy_Leaf · Late_Blight                      │
   └───────────────┼──────────────────────────────────────────────────┘
                   │  answer: Potato__Early_Blight (0.9764)
                   ▼
   ┌──────────────────────────────────────────────────────────────────┐
   │  Q4  "What should the farmer do about it?"                       │
   │                                                                  │
   │      ┌──────────────────┐                                        │
   │      │ KNOWLEDGE BASE   │   no model — curated Bengali JSON      │
   │      │ disease_details  │                                        │
   │      └────────┬─────────┘                                        │
   │               │                                                  │
   │   description_bn · cause_bn · solution_bn                        │
   └───────────────┼──────────────────────────────────────────────────┘
                   ▼
              ADVISORY RESPONSE
```

### Why routing beats one big model

```
   MONOLITHIC                            ROUTED (this system)
   ──────────                            ────────────────────

   image                                 image
     │                                     │
     ▼                                     ▼
   ┌───────────────────┐                 ┌──────────────┐
   │  ONE 32-class     │                 │  6-class     │
   │  disease model    │                 │  crop model  │
   └────────┬──────────┘                 └──────┬───────┘
            │                                   │
            ▼                                   ▼
   must separate:                        ┌──────────────┐
     potato late blight                  │  3-class     │
     vs rice leaf blast                  │  potato model│
     vs corn N. leaf blight              └──────┬───────┘
     — all dark necrotic lesions                │
     on unrelated hosts                         ▼
                                         only separates:
   confusable across hosts                 early vs late blight
   32-way decision                         vs healthy
                                           — genuinely related, and
                                             host is already fixed
                                           3-way decision
```

The observed brassica result supports this: the model's residual uncertainty on
`Cauliflower__Downy_Mildew` was `Cabbage__Downy_Mildew` (0.0003) — the same
disease on the sibling species. Errors stay inside the correct pathology.

---

## 3. Model loading and lazy initialisation

### 3.1 State machine per model

```
        ┌─────────────┐
        │   UNLOADED  │   module import: _crop_classifier = None
        │             │                  _disease_models  = {}
        │  0 MB RAM   │
        └──────┬──────┘
               │  first request needing this model
               ▼
        ┌─────────────┐
        │  RESOLVING  │   path.exists()?
        └──┬───────┬──┘
      no   │       │  yes
           ▼       ▼
   ┌──────────┐  ┌─────────────┐
   │  ERROR   │  │   LOADING   │   YOLO(str(path))
   │ HTTP 500 │  │  ~1–3 s     │   blocking, on the event loop
   └──────────┘  └──────┬──────┘
                        │
                        ▼
                 ┌─────────────┐
                 │   CACHED    │   module-level global
                 │  ~3–12 MB   │   never evicted
                 └──────┬──────┘
                        │  every later request
                        ▼
                 ┌─────────────┐
                 │  INFERRING  │   ~50–200 ms
                 └──────┬──────┘
                        │
                        └──► back to CACHED
```

### 3.2 Cache growth over a demo session

```
  REQUEST                     LOADED THIS REQUEST      RESIDENT WEIGHTS
  ─────────────────────────   ─────────────────────    ────────────────
  (process start)             —                        ░░░░░░░░░░   0.00 MB

  1  POST /classify           crop_classifier          ███░░░░░░░  12.55 MB
                              +12.55

  2  POST /detect  potato     potato_disease           █████░░░░░  23.58 MB
                              +11.03  (classifier cached)

  3  POST /detect  potato     nothing                  █████░░░░░  23.58 MB
                              cache hit ×2

  4  POST /detect  brassica   brassica_disease         ████████░░  34.63 MB
                              +11.05

  5  POST /detect  wheat      nothing                  ████████░░  34.63 MB
                              guard fires before load

  6  POST /detect  corn       corn_disease             ██████████  45.66 MB
                              +11.03

  ceiling under current routing ....................... 45.66 MB
  + rice, if it ever becomes reachable ................ 48.87 MB
```

Wheat is the interesting row: 12.55 MB on disk, 0 MB resident, because
`PLACEHOLDER_WARNING.json` is checked before `get_disease_model()`.

### 3.3 Cold start — the demo risk

```
  NOW (empty lifespan hook)

  demo request #1  ├──── load classifier ────┬─ infer ─┬── load disease ──┬─ infer ─┤
                   │◄────── 1–3 s ──────────►│         │◄──── 1–3 s ─────►│         │
                   └──────────────────── 2–6 s total, on screen ────────────────────┘

  demo request #2  ├─ infer ─┬─ infer ─┤
                   └── 100–400 ms ─────┘


  WITH LIFESPAN WARMING

  server boot      ├──── load classifier + demo crops ────┤   audience sees nothing
                   └───────────── 3–8 s ──────────────────┘

  demo request #1  ├─ infer ─┬─ infer ─┤
                   └── 100–400 ms ─────┘
```

The first upload in the demo is currently the slow one. Warming in `lifespan`
moves that cost to boot. See `WORKFLOW.md` §7.

### 3.4 Concurrency hazard

```
  time ──────────────────────────────────────────────────►

  req A   ─── get_disease_model("potato") ───┐
              key in _disease_models? NO     │
                                             ├── YOLO(...) ── 2 s ──┐
  req B   ─── get_disease_model("potato") ───┤                      ├─► _disease_models["potato"] = B
              key in _disease_models? NO     │                      │   (A's instance orphaned, GC'd)
                                             └── YOLO(...) ── 2 s ──┘

  outcome: correct results, duplicated load, transient 2× memory
```

Check-then-set on a plain dict with an `await`-free but slow body. Not
corrupting, just wasteful. A `threading.Lock` or preloading removes it.

---

## 4. Request/response lifecycle

```
 CLIENT          FASTAPI         ORCHESTRATOR       CACHE        TORCH        DISK
   │                │                  │              │            │            │
   │ POST /detect   │                  │              │            │            │
   ├───────────────►│                  │              │            │            │
   │                │ route match      │              │            │            │
   │                ├─────────────────►│              │            │            │
   │                │                  │              │            │            │
   │                │      ┌───────────┤ GATE 0                    │            │
   │                │      │ content_type guard                    │            │
   │                │      │ read() → bytes                        │            │
   │                │      │ PIL decode → RGB Image                │            │
   │                │      └───────────┤                           │            │
   │                │                  │              │            │            │
   │                │      ┌───────────┤ STAGE 1      │            │            │
   │                │      │ get_crop_classifier()───►│            │            │
   │                │      │                     miss ├───────────────────────► │
   │                │      │                          │◄── .pt bytes ─────────┤ │
   │                │      │                          ├───────────►│            │
   │                │      │◄──── YOLO instance ──────┤            │            │
   │                │      │ predict_classification() ────────────►│            │
   │                │      │◄──── probs[6] ───────────────────────┤             │
   │                │      │ "Potato" 0.9764                       │            │
   │                │      └───────────┤                           │            │
   │                │                  │              │            │            │
   │                │      ┌───────────┤ STAGE 2      │            │            │
   │                │      │ CROP_TO_MODEL["potato"] → "potato"    │            │
   │                │      │ PLACEHOLDER_WARNING.json ────────────────────────► │
   │                │      │◄──── False ──────────────────────────────────────┤ │
   │                │      └───────────┤                           │            │
   │                │                  │              │            │            │
   │                │      ┌───────────┤ STAGE 3      │            │            │
   │                │      │ get_disease_model()─────►│            │            │
   │                │      │                     miss ├───────────────────────► │
   │                │      │                          │◄── .pt bytes ─────────┤ │
   │                │      │◄──── YOLO instance ──────┤            │            │
   │                │      │ predict_classification() ────────────►│            │
   │                │      │◄──── probs[3] ───────────────────────┤             │
   │                │      │ "Potato__Early_Blight" 0.9764         │            │
   │                │      └───────────┤                           │            │
   │                │                  │              │            │            │
   │                │      ┌───────────┤ STAGE 4      │            │            │
   │                │      │ disease_details.json ────────────────────────────► │
   │                │      │◄──── KB dict ────────────────────────────────────┤ │
   │                │      │ linear scan classes[]                 │            │
   │                │      │ → no match (label mismatch) → null    │            │
   │                │      └───────────┤                           │            │
   │                │                  │              │            │            │
   │                │◄─ Pydantic ──────┤                           │            │
   │◄─ 200 JSON ────┤                  │              │            │            │
```

### Timing profile

```
  cold request
  ├─ validate + decode      ▏           ~10–50 ms
  ├─ LOAD classifier        ████████    ~1–3 s
  ├─ inference 1            ▎           ~50–200 ms
  ├─ routing                ▏           <1 ms
  ├─ LOAD disease model     ████████    ~1–3 s
  ├─ inference 2            ▎           ~50–200 ms
  └─ KB read + scan         ▏           <5 ms

  warm request
  ├─ validate + decode      ▏
  ├─ inference 1            ▎
  ├─ routing                ▏
  ├─ inference 2            ▎
  └─ KB read + scan         ▏
```

Durations are structural estimates, not measurements. No latency benchmark
exists — see `MODELS.md` §7.1.

### Blocking behaviour

```
  event loop, single worker
  ═════════════════════════════════════════════════════════════════════►

  req A  ├──────── inference (blocking torch) ────────┤
  req B         ╎ queued, cannot progress            ╎├─── inference ───┤
  /health       ╎ queued                             ╎                  ├─┤
                └────────── B and /health stall ─────┘

  handlers are `async def`, but YOLO.__call__ never yields
```

---

## 5. Routing decision tree

```
                          crop_class from Stage 1
                                    │
                                    ▼
                        crop_key = crop_class.lower()
                                    │
                                    ▼
                      ┌─────────────────────────────┐
                      │ CROP_TO_MODEL.get(crop_key) │
                      └──────────────┬──────────────┘
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        │                            │                            │
        ▼                            ▼                            ▼
   returns None                 returns a key              key absent → None
   (gourdguava,                 (rice/wheat/corn/          (unexpected label)
    solanacea)                   potato/brassica)                  │
        │                            │                            │
        │                            ▼                            │
        │              ┌──────────────────────────┐               │
        │              │ <key>_disease/           │               │
        │              │ PLACEHOLDER_WARNING.json │               │
        │              │        .exists()         │               │
        │              └──────┬────────────┬──────┘               │
        │                true │            │ false                │
        │                     ▼            ▼                      │
        │        ┌──────────────────┐   ┌──────────────────┐      │
        │        │ 200 "placeholder"│   │  RUN STAGE 3     │      │
        │        │ wheat only       │   │  then STAGE 4    │      │
        │        └──────────────────┘   └──────────────────┘      │
        │                                                         │
        └────────────────────┬────────────────────────────────────┘
                             ▼
                ┌────────────────────────────┐
                │ 200 "No disease model      │
                │  available for this crop"  │
                └────────────────────────────┘
```

### Reachability

```
  crop_classifier can emit         routing outcome
  ────────────────────────         ───────────────────────────────────────
  Brassica    ──────────────────►  brassica_disease  (11 cls)   ✅ works
  Corn        ──────────────────►  corn_disease      ( 4 cls)   ✅ works, untested
  Potato      ──────────────────►  potato_disease    ( 3 cls)   ✅ works
  GourdGuava  ──────────────────►  None                         ⛔ refusal
  Solanacea   ──────────────────►  None                         ⛔ refusal
  Wheat       ──────────────────►  placeholder guard            ⛔ refusal

  (nothing)   ─ ─ ─ ─ ─ ─ ─ ─ ─►  rice_disease      ( 8 cls)   ⛔ UNREACHABLE
                                    ▲
                                    └── no `Rice` class exists in the classifier,
                                        so crop_key can never be "rice"

  3 of 6 classifier outputs produce a real diagnosis.
```

---

## 6. Error propagation map

```
  ENTRY
    │
    ▼
  ┌─────────────────────┐
  │ file field missing  │──────────────────────► 422 Unprocessable Entity
  └──────────┬──────────┘                        (FastAPI validation)
             ▼
  ┌─────────────────────┐
  │ content_type not    │──────────────────────► 400 "File must be an image"
  │ image/*             │                        ✅ handled
  └──────────┬──────────┘
             ▼
  ┌─────────────────────┐
  │ content_type = None │──────────────────────► 500 AttributeError
  └──────────┬──────────┘                        ⚠ unhandled
             ▼
  ┌─────────────────────┐
  │ PIL cannot decode   │──────────────────────► 500 UnidentifiedImageError
  └──────────┬──────────┘                        ⚠ unhandled
             ▼
  ┌─────────────────────┐
  │ classifier weights  │──────────────────────► 500 "Crop classifier model
  │ missing             │                            not found"   ✅ handled
  └──────────┬──────────┘
             ▼
  ┌─────────────────────┐
  │ weights corrupt     │──────────────────────► 500 torch exception
  └──────────┬──────────┘                        ⚠ unhandled
             ▼
  ┌─────────────────────┐
  │ model has no .probs │──────────────────────► 500 KeyError
  └──────────┬──────────┘                        ⚠ unhandled
             ▼
  ┌─────────────────────┐
  │ no disease model    │──────────────────────► 200 partial answer  ✅ handled
  │ for crop            │
  └──────────┬──────────┘
             ▼
  ┌─────────────────────┐
  │ placeholder model   │──────────────────────► 200 partial answer  ✅ handled
  └──────────┬──────────┘
             ▼
  ┌─────────────────────┐
  │ disease weights     │──────────────────────► 500 "Disease model not
  │ missing             │                            found for <crop>"  ✅
  └──────────┬──────────┘
             ▼
  ┌─────────────────────┐
  │ json not imported   │──────────────────────► 500 NameError
  └──────────┬──────────┘                        ⛔ BLOCKING BUG
             ▼
  ┌─────────────────────┐
  │ KB file missing     │──────────────────────► 200, disease_info = null  ✅
  └──────────┬──────────┘
             ▼
  ┌─────────────────────┐
  │ no class_name match │──────────────────────► 200, disease_info = null
  └──────────┬──────────┘                        ⚠ currently ALWAYS taken
             ▼
        200 SUCCESS
```

Legend — ✅ explicit handling · ⚠ leaks a generic 500 or silently degrades ·
⛔ blocking defect.

---

## 7. Class-space narrowing

What the routing step buys, per crop:

```
   all disease classes in the system ....... 32
   ══════════════════════════════════════════════════════════════════

   after routing to:

   brassica   ███████████                    11 / 32   ( 34 % )
   rice       ████████                        8 / 32   ( 25 % )   unreachable
   wheat      ██████                          6 / 32   ( 19 % )   placeholder
   corn       ████                            4 / 32   ( 13 % )
   potato     ███                             3 / 32   (  9 % )

   the crop classifier itself:
   crops      ██████                          6 classes
```

A potato image is reduced from a 32-way decision to a 3-way decision by one
6-way classification. The routing model is doing cheap, coarse work so the
disease models can do expensive, fine work on a constrained problem.

---

## 8. Poster-sized summary

Compact version for a slide or poster panel.

```
 ┌────────────────────────────────────────────────────────────────────┐
 │            KRISHOKCHAT · CROP DISEASE VISION PIPELINE              │
 ├────────────────────────────────────────────────────────────────────┤
 │                                                                    │
 │   📷 leaf photo                                                    │
 │        │                                                           │
 │        ▼                                                           │
 │   ┌──────────────────┐                                             │
 │   │ 1. WHICH CROP?   │  YOLO classifier · 6 crop groups            │
 │   └────────┬─────────┘  Potato ······················ 97.6 %       │
 │            ▼                                                       │
 │   ┌──────────────────┐                                             │
 │   │ 2. WHICH MODEL?  │  routing table · 0 ms · no inference        │
 │   └────────┬─────────┘  → potato specialist (3 classes)            │
 │            ▼                                                       │
 │   ┌──────────────────┐                                             │
 │   │ 3. WHICH DISEASE?│  crop-specific YOLO classifier              │
 │   └────────┬─────────┘  Early Blight ················ 97.6 %       │
 │            ▼                                                       │
 │   ┌──────────────────┐                                             │
 │   │ 4. WHAT TO DO?   │  curated Bengali knowledge base             │
 │   └────────┬─────────┘  লক্ষণ · কারণ · প্রতিকার                    │
 │            ▼                                                       │
 │   🌾 advisory in Bengali                                           │
 │                                                                    │
 ├────────────────────────────────────────────────────────────────────┤
 │  4 disease models · 32 disease classes · 6 crop groups             │
 │  routing narrows a 32-way problem to a 3-to-11-way problem         │
 │  unsupported crops and placeholder models refuse, never guess      │
 └────────────────────────────────────────────────────────────────────┘
```

Two claims are safe to make on a poster and are supported by
`verification_report.json`: the routing architecture, and the error structure
observed on brassica (residual confusion stayed within the same disease across
sibling species). Accuracy percentages are **not** available — see
`MODELS.md` §7.1 before quoting any metric.
