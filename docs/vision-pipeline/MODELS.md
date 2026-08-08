# Vision Pipeline — Model Inventory

Complete inventory of the six models in `backend/ml_assets/vision/`. All figures
come from `verification_report.json`, produced by
`scripts/01_verify_models.py`, which extracts class names from the weights
themselves rather than from any hand-written manifest.

---

## 1. Inventory summary

| # | Model | Directory | Task | Classes | Size (MB) | Reachable | Status |
|---|---|---|---:|---:|---:|:---:|---|
| 1 | Crop classifier | `crop_classifier/` | `classify` | 6 | 12.55 | ✅ | Verified — 3 test images |
| 2 | Rice disease | `rice_disease/` | `classify` | 8 | 3.21 | ⛔ | Verified — 2 test images, but unroutable |
| 3 | Wheat disease | `wheat_disease/` | `classify` | 6* | 12.55 | ⛔ | **PLACEHOLDER** — not a wheat model |
| 4 | Corn disease | `corn_disease/` | `classify` | 4 | 11.03 | ✅ | Loads, no test images |
| 5 | Potato disease | `potato_disease/` | `classify` | 3 | 11.03 | ✅ | Verified — 2 test images |
| 6 | Brassica disease | `brassica_disease/` | `classify` | 11 | 11.05 | ✅ | Verified — 3 test images |

\* The wheat entry reports 6 classes because it is a byte-copy of the crop
classifier; those are crop classes, not wheat diseases. See §4.

Totals: **32 usable disease classes** across four real disease models, plus 6
crop classes. Combined on-disk weight footprint **61.42 MB** (decimal MB, i.e.
bytes ÷ 10⁶).

### Size distribution

```
  crop_classifier   ████████████████████████  12.55 MB
  wheat_disease     ████████████████████████  12.55 MB  (= crop_classifier)
  brassica_disease  █████████████████████     11.05 MB
  corn_disease      █████████████████████     11.03 MB
  potato_disease    █████████████████████     11.03 MB
  rice_disease      ██████                     3.21 MB
```

The rice model is roughly a quarter the size of the others while carrying the
second-largest class count. It is almost certainly a smaller YOLO scale
(`yolo11n-cls`-tier) where the rest are one step up. That makes it the fastest
model in the set — and it is the one that can never be invoked.

---

## 2. Crop classifier

**Path:** `backend/ml_assets/vision/crop_classifier/model.pt`
**Role:** Stage 1. Chooses which disease model handles the image.

| Property | Value |
|---|---|
| Task | `classify` |
| Classes | 6 |
| Size | 12.55 MB (12,545,559 bytes) |
| Output | softmax over 6 crop groups |
| Loaded | lazily, on first `/api/classify` or `/api/detect` |

### Classes

| Idx | Class | Botanical scope | Has disease model |
|---:|---|---|:---:|
| 0 | `Brassica` | *Brassica oleracea* — cabbage, cauliflower | ✅ |
| 1 | `Corn` | *Zea mays* | ✅ |
| 2 | `GourdGuava` | cucurbits + guava (heterogeneous group) | ❌ |
| 3 | `Potato` | *Solanum tuberosum* | ✅ |
| 4 | `Solanacea` | nightshades — tomato, brinjal, chilli | ❌ |
| 5 | `Wheat` | *Triticum aestivum* | ⚠ placeholder only |

`GourdGuava` merges two unrelated taxa (Cucurbitaceae and *Psidium guajava*)
into a single label. That is a dataset artefact, not a botanical grouping, and
it makes the class hard to extend — adding a gourd disease model would also
capture guava images.

### Verified predictions

| Image | Prediction | Confidence | Runner-up |
|---|---|---:|---|
| `0001.jpg` | `Solanacea` | 0.9683 | `Brassica` 0.0170 |
| `0002.jpg` | `Brassica` | 1.0000 | `Solanacea` 0.0000 |
| `0001.png` | `Brassica` | 1.0000 | `GourdGuava` 0.0000 |

```
  0001.jpg  Solanacea  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░  0.9683
  0002.jpg  Brassica   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1.0000
  0001.png  Brassica   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1.0000
```

Two of three predictions are exactly 1.0000 after 4-dp rounding. Saturated
softmax output on a 6-class problem usually indicates either a very easy test
set or overfitting; it is not by itself evidence of good generalisation. Three
images is far too small a sample to characterise accuracy — treat these numbers
as a smoke test, not a benchmark.

---

## 3. Disease models

### 3.1 Rice — `rice_disease/`

| Property | Value |
|---|---|
| Classes | 8 |
| Size | 3.21 MB (3,205,243 bytes) |
| Label style | `Rice__<Disease>` |
| Reachable via `/api/detect` | **No** — see §5 |

| Idx | Model class | KB entry (Bengali) |
|---:|---|---|
| 0 | `Rice__Bacterial_Leaf_Blight` | Bacterial Leaf Blight (ব্যাকটেরিয়াজনিত পাতা পোড়া) |
| 1 | `Rice__Brown_Spot` | Brown Spot (বাদামী দাগ রোগ) |
| 2 | `Rice__Healthy_Leaf` | Healthy (সুস্থ ধান গাছ) |
| 3 | `Rice__Leaf_Blast` | Leaf Blast (পাতা ব্লাস্ট) |
| 4 | `Rice__Leaf_Scald` | Leaf Scald (পাতা পোড়া বা লিফ স্ক্যাল্ড) |
| 5 | `Rice__Narrow_Brown_Leaf_Spot` | Narrow Brown Leaf Spot (সংকীর্ণ বাদামী দাগ রোগ) |
| 6 | `Rice__Rice_Hispa` | Rice Hispa (ধানের পামরি পোকা) |
| 7 | `Rice__Sheath_Blight` | Sheath Blight (খোল পচা বা খোল পোড়া রোগ) |

Note `Rice_Hispa` is an insect pest, not a disease — the class set mixes
pathology and entomology. That is defensible for farmer-facing advice (both need
intervention) but worth knowing when describing the model.

Verified predictions:

| Image | Prediction | Confidence |
|---|---|---:|
| `0001.jpg` | `Rice__Sheath_Blight` | 1.0000 |
| `0002.jpg` | `Rice__Sheath_Blight` | 1.0000 |

Both test images predict the same class at saturation. This tells us the model
loads and produces plausible output; it tells us nothing about discrimination
across the other seven classes.

---

### 3.2 Corn — `corn_disease/`

| Property | Value |
|---|---|
| Classes | 4 |
| Size | 11.03 MB (11,030,843 bytes) |
| Label style | **bare** — no `Corn__` prefix |
| Test images | **none** (`test_images/corn_disease/` is empty) |

| Idx | Model class | KB entry (Bengali) |
|---:|---|---|
| 0 | `Common_Rust` | Common Rust (ভুট্টার সাধারণ মরিচা রোগ) |
| 1 | `Gray_Leaf_Spot` | Gray Leaf Spot (ভুট্টার ধূসর পাতা পোড়া রোগ) |
| 2 | `Healthy` | Healthy (সুস্থ ভুট্টা গাছ) |
| 3 | `Northern_Leaf_Blight` | Northern Leaf Blight (ভুট্টার উত্তরীয় পাতা পোড়া রোগ) |

**Naming inconsistency.** Every other disease model prefixes its classes with
the crop (`Rice__`, `Potato__`, `Cabbage__`, `Cauliflower__`). Corn does not.
Its `Healthy` class is also the only unqualified `Healthy` in the system, which
makes it ambiguous if class names are ever pooled across models — for example
in a merged confusion matrix or a logging table.

The corn model has never been exercised against a real image. It loads and
reports its class names, nothing more. Before the demo, at least two corn test
images should be added to `test_images/corn_disease/` and
`01_verify_models.py` re-run.

---

### 3.3 Potato — `potato_disease/`

| Property | Value |
|---|---|
| Classes | 3 |
| Size | 11.03 MB (11,032,834 bytes) |
| Label style | `Potato__<Disease>` |

| Idx | Model class | KB entry (Bengali) |
|---:|---|---|
| 0 | `Potato__Early_Blight` | Early Blight (প্রারম্ভিক ব্লাস্ট) |
| 1 | `Potato__Healthy_Leaf` | Healthy Leaf (সুস্থ আলু পাতা) |
| 2 | `Potato__Late_Blight` | Late Blight (লেট ব্লাস্ট বা আলুর ঝুলসা রোগ) |

Verified predictions:

| Image | Prediction | Confidence | Runner-up |
|---|---|---:|---|
| `0001.jpg` | `Potato__Early_Blight` | 0.9764 | `Potato__Late_Blight` 0.0236 |
| `0002.jpg` | `Potato__Late_Blight` | 1.0000 | `Potato__Early_Blight` 0.0000 |

This is the most informative verification result in the set: the two test images
predict **different** classes, and the confusion that does exist (2.36 %) is
between early and late blight — the pair a human agronomist would also find
hardest. That is the signature of a model that has learned something real rather
than a shortcut.

Potato is the strongest candidate for the live demo path.

---

### 3.4 Brassica — `brassica_disease/`

| Property | Value |
|---|---|
| Classes | 11 (largest set) |
| Size | 11.05 MB (11,049,979 bytes) |
| Label style | `Cabbage__<X>` / `Cauliflower__<X>` |
| KB top-level field | `crop_group` (all others use `crop_name`) |

| Idx | Model class | KB entry (Bengali) |
|---:|---|---|
| 0 | `Cabbage__Alternaria_Spot` | Cabbage Alternaria Spot (বাঁধাকপির অল্টারনারিয়া দাগ) |
| 1 | `Cabbage__Black_Rot` | Cabbage Black Rot (বাঁধাকপির কালো পচা রোগ) |
| 2 | `Cabbage__Downy_Mildew` | Cabbage Downy Mildew (বাঁধাকপির ডাউনি মিলডিউ) |
| 3 | `Cabbage__Healthy_Leaf` | Cabbage Healthy (সুস্থ বাঁধাকপি) |
| 4 | `Cauliflower__Alternaria_Disease` | Cauliflower Alternaria Disease (ফুলকপির অল্টারনারিয়া রোগ) |
| 5 | `Cauliflower__Bacterial_Soft_Rot` | Cauliflower Bacterial Soft Rot (ফুলকপির ব্যাকটেরিয়াল নরম পচা রোগ) |
| 6 | `Cauliflower__Bacterial_Spot` | Cauliflower Bacterial Spot (ফুলকপির ব্যাকটেরিয়াল দাগ) |
| 7 | `Cauliflower__Black_Spot` | Cauliflower Black Spot (ফুলকপির কালো দাগ) |
| 8 | `Cauliflower__Downy_Mildew` | Cauliflower Downy Mildew (ফুলকপির ডাউনি মিলডিউ) |
| 9 | `Cauliflower__Healthy` | Cauliflower Healthy (সুস্থ ফুলকপি) |
| 10 | `Cauliflower__Nutrient_Deficiency` | Cauliflower Nutrient Deficiency (ফুলকপির পুষ্টির অভাব) |

This model is doing two jobs at once: distinguishing **species** (cabbage vs.
cauliflower) and **condition** within each. It also carries an abiotic class,
`Cauliflower__Nutrient_Deficiency`, which is a deficiency rather than a
pathogen — good for advisory coverage, but it means the model must separate
nutrient chlorosis from disease chlorosis, a genuinely hard visual distinction.

Note the asymmetry: cabbage has a `Healthy_Leaf` class, cauliflower has
`Healthy`. Same concept, two spellings, inside a single model.

Verified predictions:

| Image | Prediction | Confidence | Runner-up |
|---|---|---:|---|
| `0001.jpg` | `Cauliflower__Downy_Mildew` | 0.9996 | `Cabbage__Downy_Mildew` 0.0003 |
| `0002.jpg` | `Cauliflower__Healthy` | 1.0000 | `Cauliflower__Nutrient_Deficiency` 0.0000 |
| `0001.png` | `Cauliflower__Healthy` | 1.0000 | `Cauliflower__Downy_Mildew` 0.0000 |

The first result is the most encouraging signal in the whole inventory: the
model's residual uncertainty is `Cabbage__Downy_Mildew` — the *same disease on
the sibling species*. It has learned the pathology and is only mildly unsure
about the host. That is exactly the error structure you want.

---

## 4. Known issue — the wheat placeholder

`wheat_disease/model.pt` is **not a wheat disease model**. It is a byte-identical
copy of `crop_classifier/model.pt`.

Evidence:

| Check | `crop_classifier` | `wheat_disease` |
|---|---|---|
| Size (bytes) | 12,545,559 | 12,545,559 |
| Class count | 6 | 6 |
| Class names | Brassica, Corn, GourdGuava, Potato, Solanacea, Wheat | *identical* |
| SHA-256 | — | `6F14484768E54F28C2EDC2C5D3858C2C1A57F18D7DE40A001A119CBC04240C94` |

`scripts/01_verify_models.py` detects this automatically by comparing the two
class lists and emits:

```
⚠️  WHEAT DISEASE model is IDENTICAL to CROP CLASSIFIER!
    This is a placeholder — real wheat disease model needed.
```

### The guard

`wheat_disease/PLACEHOLDER_WARNING.json` marks the directory:

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

The orchestrator probes for this file **before** loading weights, so a wheat
image returns a clean 200 with
`disease = "Disease model not available (placeholder)"` and the placeholder is
never loaded into memory.

This is the correct handling. It satisfies `AGENTS.md §2` rule 5 — no fabricated
output is presented as a real diagnosis — and the failure is visible in the
response rather than silent.

### The Bengali KB is already written

`wheat_disease/disease_details.json` contains complete, real content for six
wheat conditions that the model cannot predict:

| Expected class | KB entry |
|---|---|
| `Wheat__Leaf_Rust` | Leaf Rust (পাতা মরিচা রোগ) |
| `Wheat__Stem_Rust` | Stem Rust (কাণ্ড মরিচা রোগ) |
| `Wheat__Stripe_Rust` | Stripe Rust (ডোরাকাটা মরিচা রোগ) |
| `Wheat__Blast` | Blast (গম ব্লাস্ট রোগ) |
| `Wheat__Powdery_Mildew` | Powdery Mildew (গুঁড়া মিলডিউ রোগ) |
| `Wheat__Healthy` | Healthy (সুস্থ গম গাছ) |

So the knowledge layer is ready; only the weights are missing. Dropping a real
6-class wheat classifier into the directory and deleting
`PLACEHOLDER_WARNING.json` would activate the whole route with no code change —
provided the label-matching issue in `WORKFLOW.md` §4 is fixed first.

Wheat blast is a live concern in Bangladesh, so this gap has real advisory cost,
not just demo cost.

---

## 5. Known issue — the unreachable rice model

The rice disease model is fully functional, verified, and **impossible to
invoke**.

```
   crop_classifier emits:  Brassica  Corn  GourdGuava  Potato  Solanacea  Wheat
                                                                       (no Rice)
                                       │
                                       ▼
   CROP_TO_MODEL contains:  rice → "rice"        ◄── key never produced
                            wheat, corn, potato, brassica, gourdguava, solanacea
                                       │
                                       ▼
   DISEASE_MODEL_PATHS:     rice → rice_disease/model.pt   ◄── never opened
```

The routing key `crop_key` is derived from the classifier's own output via
`.lower()`. Since the classifier has no `Rice` class, `crop_key` can never be
`"rice"`, so the `rice` entries in both dictionaries are dead code.

This matters more than a normal dead branch, because rice is the dominant crop
in Bangladesh and the rice model is the best-equipped in the inventory: 8
classes, covering the major rice pathologies plus hispa, at a quarter the file
size of its peers.

Two ways out:

1. **Retrain the crop classifier with a `Rice` class** (7 classes). Correct, but
   requires a labelled rice crop dataset and a retraining cycle.
2. **Expose rice via a manual override** — accept an optional `crop` form field
   on `/api/detect` that bypasses Stage 1. Cheap, and it makes the rice model
   demonstrable immediately. It also gives the demo a way to show any specific
   model on demand.

Option 2 is the pragmatic 7-day answer; option 1 is the right long-term fix.

---

## 6. Label convention audit

Inconsistent naming across the six models is the root cause of the Stage 4
lookup failure documented in `WORKFLOW.md` §4.

| Model | Convention | Example | Healthy class |
|---|---|---|---|
| `crop_classifier` | bare CamelCase | `GourdGuava` | n/a |
| `rice_disease` | `Rice__` prefix | `Rice__Leaf_Blast` | `Rice__Healthy_Leaf` |
| `corn_disease` | **no prefix** | `Common_Rust` | `Healthy` |
| `potato_disease` | `Potato__` prefix | `Potato__Late_Blight` | `Potato__Healthy_Leaf` |
| `brassica_disease` | species prefix | `Cabbage__Black_Rot` | `Cabbage__Healthy_Leaf` **and** `Cauliflower__Healthy` |
| `wheat_disease` | n/a (placeholder) | — | — |

Three separate spellings of the healthy state exist: `Healthy`,
`Healthy_Leaf`, and both inside one model. Any downstream logic that wants to
answer "is this plant healthy?" — a badge in the UI, a metric on the poster —
has to special-case all three.

Recommended target convention, applied at the KB layer rather than by retraining:

```
<Crop>__<Condition_In_Snake_Case>
  Corn__Common_Rust
  Corn__Healthy
  Cauliflower__Healthy
```

Since the KB is hand-authored JSON, adding a machine-readable `model_class`
field alongside the human `class_name` would fix Stage 4 without touching any
weights:

```json
{
  "class_name": "Early Blight (প্রারম্ভিক ব্লাস্ট)",
  "model_class": "Potato__Early_Blight",
  "description_bn": "…"
}
```

That is 32 small edits and removes the need for fuzzy string normalisation
entirely.

---

## 7. Performance characteristics

### 7.1 Measured

Only class counts, file sizes, and per-image predictions on 10 test images have
been measured. **No latency, throughput, accuracy, precision, recall, or
confusion-matrix data exists** for any model in this repository.

Per `AGENTS.md §2` rule 5, the following are explicitly **not** available and
must not be quoted on the poster or in the demo:

- `TODO` — top-1 accuracy for each model
- `TODO` — macro F1 / per-class recall
- `TODO` — inference latency (p50 / p95) on demo hardware
- `TODO` — cold-start load time per model
- `TODO` — held-out test set size and provenance
- `TODO` — training dataset source, size, and split methodology

If the research panel needs vision metrics, they must be produced by an actual
evaluation run, not estimated from the 10 verification images.

### 7.2 Structural characteristics

These follow from the code and file sizes and can be stated safely.

| Characteristic | Value | Source |
|---|---|---|
| Inference device | CPU | `.cpu()` hardcoded in `predict_classification` |
| Precision | FP32 (default `.pt`) | no quantisation applied |
| Format | PyTorch `.pt` via Ultralytics | not the ONNX path in `AGENTS.md §3` |
| Models loaded per `/api/detect` | 2 | classifier + one disease model |
| Inference calls per `/api/detect` | 2 | same decoded image passed to both |
| Image decodes per request | 1 | decoded once in Gate 0 |
| Peak resident weights (all loaded) | ~61 MB + torch overhead | sum of file sizes |
| Typical resident weights (demo path) | ~23.6 MB | classifier + one disease model |
| Concurrency | serialised | blocking torch call inside `async def` |

### 7.3 Memory growth by usage

```
  process start              0 MB weights
    │
    ├─ first /api/classify        +12.55  ──►  12.55 MB
    ├─ first potato detect        +11.03  ──►  23.58 MB
    ├─ first brassica detect      +11.05  ──►  34.63 MB
    ├─ first corn detect          +11.03  ──►  45.66 MB
    ├─ wheat detect                +0.00  ──►  45.66 MB  (guard blocks load)
    └─ rice detect                 +0.00  ──►  45.66 MB  (unreachable)

  ceiling under current routing: 45.66 MB
  ceiling if rice becomes reachable: 48.87 MB
```

Nothing is ever evicted. For a demo process this is fine; the ceiling is low and
bounded by the number of models, not by traffic.

### 7.4 Latency shape

Not measured, but the structure is known:

```
  request N=1 (cold)   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  weight load dominates
  request N=2 (warm)   ▓▓                        inference only
  request N=3 (warm)   ▓▓
```

The first request to each crop pays the load cost once. See `WORKFLOW.md` §7 for
the lifespan-warming mitigation.

---

## 8. Verification harness

`backend/ml_assets/vision/scripts/01_verify_models.py` is the source of truth
for everything in this document.

What it does, per model:

1. Confirms `model.pt` exists and records its size.
2. Loads it through `YOLO()` and reports success or the exception.
3. Extracts `model.names` — the real class map baked into the weights.
4. **Writes `class_names.json`** into the model directory, overwriting any
   stale hand-written version.
5. Reports `model.task`.
6. Runs up to 5 test images from `test_images/<model>/`, handling both the
   `.probs` (classification) and `.boxes` (detection) result shapes.
7. Appends everything to `verification_report.json`.
8. Cross-checks wheat against the crop classifier and warns if identical.

Run it:

```bash
cd backend
uv run python ml_assets/vision/scripts/01_verify_models.py
```

Because step 4 regenerates `class_names.json` from the weights, those files can
never drift from reality — a good property. Note that the script reads
`.jpg`/`.png`/`.jpeg` only, so the `.webp` file in
`test_images/brassica_disease/` is silently skipped.

### Test image coverage

| Model | Images | Formats | Exercised |
|---|---:|---|:---:|
| `crop_classifier` | 3 | jpg, png | ✅ |
| `rice_disease` | 2 | jpg | ✅ |
| `potato_disease` | 2 | jpg | ✅ |
| `brassica_disease` | 4 | jpg, png, webp | ✅ (3 of 4 — webp skipped) |
| `corn_disease` | 0 | — | ❌ |
| `wheat_disease` | 0 | — | ❌ |

Adding corn test images is the single highest-value gap to close before the
demo, since corn is a routable path that has never produced a prediction.

---

## 9. Action list

| Priority | Action | Blocks |
|---|---|---|
| P0 | Add `model_class` field to all 32 KB entries, or add label normalisation | Treatment advice never reaches the response |
| P1 | Add ≥2 corn test images and re-run verification | Untested live route |
| P1 | Decide rice strategy — retrain classifier or add manual crop override | 8-class model unusable |
| P2 | Train or obtain real wheat disease weights; delete the placeholder guard | Wheat advisory coverage |
| P1 | Strip 291 `[cite: N]` markers from the rice, corn, and brassica KBs | Markers render verbatim to farmers |
| P2 | Normalise the three `Healthy` spellings | Downstream aggregation |
| P3 | Run a real evaluation and fill the `TODO` metrics in §7.1 | Research panel credibility |
| P3 | Evaluate ONNX export per `AGENTS.md §3` | Stack compliance, cold start |
