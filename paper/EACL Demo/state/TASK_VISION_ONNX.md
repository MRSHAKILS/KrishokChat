# TASK: Vision ONNX export, INT8 quantization, and real measurement

**Audience:** the local execution agent (has GPU/compute and permission to run long jobs).
**Author:** planning session 2026-08-30. **Do not execute any of this from a planning session.**
**Read `state/STATE.md` first** — especially §0 standing directives and §4 vision ground truth.

---

## 0. Direct answer to "can you make ONNX from the .pt?"

**Yes — and two of the six are already done.** This was mis-recorded in an earlier session as
"no ONNX exists anywhere"; that search only covered `backend/`. The real state:

- `frontend/public/models/crop_classifier.onnx` — 6,181,631 B, FP32, opset 20,
  `images [1,3,224,224]` → `output0 [1,6]`, embedded `task: classify` + class names.
- `frontend/public/models/potato_disease.onnx` — 21,798,793 B, FP32, opset 20,
  `images [1,3,224,224]` → `output0 [1,3]`.
- Both `source_pt_sha256` values in `frontend/public/models/metadata.json` match the live
  `.pt` files byte-for-byte, so these exports are **current, not stale**.

Missing: `rice_disease`, `wheat_disease`, `corn_disease`, `brassica_disease`. Missing entirely:
**any INT8 artifact** (`total_onnx_mb: 0` in E07 was measured against `backend/`, which genuinely
holds no ONNX).

**Three things block the manuscript's current vision claims, and none of them are export bugs:**

1. **The existing exporter uses the wrong input size for 3 of the 4 remaining models.**
   `backend/scripts/export_vision_ondevice.py` hardcodes `imgsz=224`. Checkpoint `train_args`
   say rice was trained at **320**, corn at **256**, brassica at **256**. Exporting those at 224
   produces a model that runs but is quietly less accurate than the `.pt` it came from.
2. **Ultralytics' native INT8 path cannot run on this machine.** `export(quantize=8)` routes to
   `ultralytics/utils/export/onnx.py::onnx_int8_quantize` → `quantize_static`, but its calibration
   loader is `Exporter.get_int8_calibration_dataloader`, which calls `check_cls_dataset(self.args.data)`
   and needs a real classification dataset with a val split. The training datasets were Kaggle /
   Google-Drive paths (`/kaggle/input/...`, `/content/drive/MyDrive/499B/Wheat`) and are **not on
   this machine**. So INT8 must be done with ONNX Runtime directly, using a hand-written
   `CalibrationDataReader` over the local `test_images/` tree.
3. **Nothing in the codebase ever loads an ONNX file.** `onnxruntime-web` is not in
   `frontend/package.json`; no `.ts`/`.tsx` references `public/models`, `InferenceSession`, or
   `onnxruntime`. Backend inference is `.pt` via `YOLO()`
   (`app/infrastructure/vision/ultralytics_classifier.py:26`). So the phrase **"INT8 ONNX
   on-device classification"** in `README.md` §1 theme 1 is currently false in three separate ways:
   not INT8, not on-device, not loaded. Exporting files does not fix this — **only wiring a runtime
   does**, and that is a frontend code change, not an experiment.

Everything needed is installed: onnx 1.22.0, onnxruntime 1.28.0 (`quantize_static` and
`quantize_dynamic` both import), onnxslim 0.1.96, torch 2.13.0+cpu, ultralytics 8.4.116.
CPU only — no CUDA. `onnxsim` is absent and not needed.

---

## 1. Choose the claim scope first (this decides how much work follows)

Do not start coding until the author picks one. Each option is internally honest; they differ in
cost and in how strong a claim the paper can make.

### Option A — Full on-device story (largest, strongest, riskiest)
Export all 6 → FP32 ONNX at correct `imgsz`, add INT8 via ORT static quantization, measure
FP32-vs-INT8 accuracy and latency on local labelled images, **and add `onnxruntime-web` to the
frontend with a real in-browser inference path.** Only this option earns the words
"on-device INT8". Costs a frontend dependency, a bundle-size hit against the existing
`size-limit` budget (First Load JS limit 650 KB gzip), and a `pnpm build` gate.

### Option B — Honest FP32 deployment-artifact claim (smallest, safest)
Keep the 2 existing exports as *exported deployment artifacts*. Delete every INT8 claim and every
"on-device inference" claim from README + manuscript. Measure the **real serving path** — `.pt` via
ultralytics through `VisionPipeline` — for accuracy and latency. Nothing new is exported.

### Option C — All-six FP32, measured as deployment readiness (recommended middle)
Export all 6 at correct per-model `imgsz`, measure ORT-CPU accuracy + latency against the `.pt`
baseline, and report it as a **deployment-readiness** result ("the serving models export cleanly to
a portable runtime and retain accuracy within X pp at Y ms CPU latency"). Still delete INT8 and
on-device-inference claims. Gives a real, defensible vision number without touching the frontend.

**Recommendation: C**, upgrading to A only if the screencast is actually going to show in-browser
offline inference. B is the fallback if time is short.

---

## 2. Tasks

Tasks are ordered by dependency. `V1`–`V3` are needed by every option; `V4` is Option C/A;
`V5`–`V6` are Option A only; `V7` is unconditional cleanup.

All scripts go in
`paper/EACL Demo/experiments/E02_multimodal_diagnostic_workflow/scripts/` unless stated otherwise.
**Never overwrite the existing `run_e02_multimodal_workflow.py`** — it stays as the superseded
artifact until the real one is frozen. Use `run_real_*.py` names and `results_real*.json` outputs.

Every script must:
- run as `Set-Location backend; ..\.venv\Scripts\python.exe <path>` **or** do
  `sys.path.insert(0, str(REPO/"backend"))` and be runnable from anywhere. Prefer the latter and
  resolve the repo root from `Path(__file__).resolve().parents[...]` — **do not** hardcode
  `r"d:\KrishokTech Advisory System"` the way `run_e07_deployment_footprint.py` does (fix that too).
- record, in the output JSON: UTC timestamp, `git rev-parse HEAD`, python version, versions of
  torch/ultralytics/onnx/onnxruntime, the SHA-256 of every input artifact, and the exact machine
  CPU model + core count (`platform.processor()`, `os.cpu_count()`).
- emit **only measured values**. If something cannot be measured, emit
  `"status": "unmeasured", "reason": "<why>"` — never a plausible number (AGENTS.md rule 5).

---

### V1 — Build the labelled evaluation manifest (no inference)

**Script:** `build_vision_eval_manifest.py` → `vision_eval_manifest.json`

Walk the local labelled trees and emit one row per image: absolute path, ground-truth label from
the folder name, which disease model owns that label, expected crop family, image dimensions,
and file SHA-256.

Sources and their real contents (verified):
- `backend/ml_assets/vision/test_images/wheat_disease/` — **800 images across 11 folders**, exactly
  matching the wheat model's 11 classes (`BlackPoint` 100, `Blast` 50, `FusariumFootRot` 100,
  `Healthy` 50, `HealthyLeaf` 100, `Leaf Rust` 50, `LeafBlight` 100, `Powdery Mildew` 50,
  `Stem Rust` 50, `Stripe Rust` 50, `WheatBlast` 100).
- `backend/ml_assets/vision/test_images/full_library/` — **437 images across 47 folders**:
  Potato 3 classes/30 imgs, Rice 8/80, Cabbage 4/32 + Cauliflower 7/70 (= brassica's 11 classes/102),
  plus Tomato 5, Chili 4, Eggplant 5, Gourd 4, Guava 5 (these last five have **no disease model** —
  they are the correct negative/`NO_DISEASE_MODEL` set, do not score them as disease errors).
- `test_images/{crop_classifier,potato_disease,rice_disease,brassica_disease}/` — 2–4 smoke images each.

Hard facts to encode:
- **`corn_disease` has zero local test images.** Corn accuracy is **unmeasurable**. Emit
  `{"corn": {"status": "unmeasured", "reason": "no local labelled test images"}}` and make sure no
  downstream table shows a corn number.
- Folder labels in `full_library` use the `Crop__Disease` convention and match the disease models'
  `class_names.json` verbatim — assert this in code and fail loudly on any mismatch rather than
  fuzzy-matching.
- The crop classifier's 6 classes are `Brassica, Corn, GourdGuava, Potato, Solanacea, Wheat` —
  **there is no Rice class**. `vision_pipeline.py:158-165` documents the live-verified consequence:
  rice leaves classify as Wheat, and the pipeline mitigates by also running the rice model and
  letting higher confidence win. Any crop-level accuracy number must state the 6-class label space
  and treat rice as a known out-of-label-space case, not as a model error to be hidden.

**Also record but do not trust:** `test_images/test_matrix_results.json` is a real prior 437-row
crop→disease routing run with genuine confidences. Cite it as corroboration only; the paper's number
must come from a fresh run.

---

### V2 — Baseline: measure the real `.pt` serving path

**Script:** `run_real_e02a_pt_baseline.py` → `results_real_pt_baseline.json`

This is the number that describes what the deployed system actually does today, and it is required
under **every** option — including A — because the backend serves `.pt`.

- Drive `UltralyticsClassificationRunner` + `ArtifactVisionRegistry` directly (not HTTP), so the
  measurement isolates model inference from FastAPI overhead.
- Warm up each model with ≥10 discarded inferences before timing (first `YOLO()` call includes
  lazy graph build and dominates a cold p50).
- Per model report: n, top-1 accuracy, top-3 accuracy, per-class precision/recall/F1, full confusion
  matrix, and latency p50/p90/p95/p99 + mean/stdev in ms. Report **per-image single-batch latency**
  — that is the production shape.
- Additionally run the full `VisionPipeline.detect()` over the same manifest to capture the
  *routing* behaviour the paper actually wants to describe: how often `crop_threshold=0.60` and
  `disease_threshold=0.55` fire, the distribution of `VisionStatus`
  (DIAGNOSED / NOT_RECOGNIZED / NO_DISEASE_MODEL / HEALTHY / INVALID_IMAGE / MODEL_ERROR), and how
  often the wheat→rice ambiguity mitigation changes the reported crop. Pass a stub LLM so the
  advisory sub-call does not need a live model (see `STATE.md` §5 for the stub sources).
- Report `crop_hint` on and off separately — the hint path bypasses the crop classifier entirely and
  the two numbers are not comparable.

---

### V3 — Correct, reproducible FP32 ONNX export for all six

**Script:** `export_vision_onnx_all.py` (put this one in `backend/scripts/`, next to the existing
exporter, since it is a build tool and not an experiment) → writes ONNX + a
`vision_onnx_export_report.json` into the experiment folder.

Fixes to carry over from the existing `export_vision_ondevice.py`:
- Read `imgsz` **per model** from the checkpoint's `train_args` (224 / 224 / 320 / 224 / 256 / 256
  for crop / potato / rice / wheat / corn / brassica). Do not hardcode 224. Assert the exported
  graph's input shape equals the intended `imgsz` before accepting the file.
- `format="onnx", dynamic=False, simplify=True`. Let ultralytics pick the opset via
  `best_onnx_opset` (it chose 20 for the existing two); pin it explicitly in the report either way.
- Keep the existing script's good habits: deterministic JSON, SHA-256 of source `.pt` and output
  `.onnx`, embedded `task: classify`.
- **Verify class-name parity** for every model: compare the ONNX embedded `names` metadata against
  `class_names.json`. Note that `crop_classifier` and `wheat_disease` have `ck['model'] is None` and
  carry their names on `ck['ema'].names` — both were checked and **match** `class_names.json`
  exactly, but re-assert it in code so a future re-export cannot silently drift.
- Decide and document the output location. The existing two live in `frontend/public/models/`
  because they were meant for browser use. If Option C (no browser inference), a
  `backend/ml_assets/vision/onnx/` location is more honest and keeps 60+ MB of unused weights out of
  the frontend's public bundle. **Do not move the existing two without also updating
  `frontend/public/models/metadata.json`.**
- Re-exporting `crop_classifier`/`potato_disease` will produce different bytes than the 2026-08-26
  files even with identical settings (nondeterministic graph ordering). Either leave them untouched
  and export only the 4 missing, or re-export all 6 and update `metadata.json` wholesale. **Pick
  one and write it in the report** — do not end up with a `metadata.json` that describes files
  that no longer exist.

---

### V4 — ONNX Runtime parity + latency (Options C and A)

**Script:** `run_real_e02b_onnx_parity.py` → `results_real_onnx_parity.json`

The claim this supports: *the serving models export to a portable runtime without accuracy loss,
at N ms CPU latency.* That is a real deployment-readiness result and needs no browser.

- Preprocessing must match ultralytics classification inference exactly, or parity will look broken
  for reasons that have nothing to do with ONNX: `Resize(imgsz)` → `CenterCrop(imgsz)` → RGB →
  float32 → `/255.0` → `NCHW`. (Confirmed against
  `Exporter.get_int8_calibration_dataloader`, which builds
  `T.Compose([T.Resize(cfg.imgsz), T.CenterCrop(cfg.imgsz), T.PILToTensor()])` for `task == "classify"`.)
  Ultralytics classify does **not** letterbox. Get this wrong and every parity number is garbage.
- Report **agreement rate** (fraction of images where ONNX top-1 == `.pt` top-1), max absolute
  logit/probability delta, and ONNX top-1 accuracy alongside the V2 `.pt` accuracy. Agreement should
  be ~100 % for FP32; if it is not, stop and investigate preprocessing before reporting anything.
- Latency: `ort.InferenceSession(..., providers=["CPUExecutionProvider"])`, single-image batch,
  ≥20 warm-up then ≥200 timed runs per model, report p50/p90/p95/p99. **Pin
  `sess_options.intra_op_num_threads`** and record it — unpinned thread counts make the number
  irreproducible on a different machine. Also record CPU model and core count.
- Report file sizes: `.pt` MB vs `.onnx` MB per model, and the total. This is what E07's
  `total_onnx_mb: 0` should become once the files exist in a location E07 actually scans — **update
  E07's scan roots when the export location is decided.**

---

### V5 — INT8 static quantization (Option A only)

**Script:** `quantize_vision_int8.py` (in `backend/scripts/`) → `vision_int8_report.json`

Ultralytics' INT8 path is unusable here (§0 item 2). Do it directly with ORT:

- `from onnxruntime.quantization import quantize_static, CalibrationDataReader, QuantType`.
- Write a `CalibrationDataReader` over **local** images from `test_images/`, using the *same*
  preprocessing as V4. Ultralytics warns that **>300 images** are recommended for calibration.
  Wheat has 800 (fine). Potato has 30, rice 80, brassica 102 — all **below** the recommended
  threshold. **Record the calibration n per model and state the limitation in the paper**; do not
  paper over it.
- **Calibration and evaluation must not use the same images**, or the INT8 accuracy number is
  contaminated. Split the manifest per class (stratified) into a calibration split and a held-out
  eval split, record both splits' image hashes in the report, and evaluate INT8 only on held-out.
  For potato/rice/brassica this may leave too few eval images to support a meaningful accuracy
  claim — if so, report INT8 for **wheat only** and mark the rest `unmeasured`.
- Follow ultralytics' own hard-won lesson from `onnx_int8_quantize`: exclude non-weighted ops from
  quantization (`nodes_to_exclude = [n.name for n in graph.node if n.op_type not in {"Conv","Gemm","MatMul"}]`).
  Their comment explains why — a single INT8 scale spanning wide-range and 0-1 tensors rounds scores
  to zero, and excluding by *node* rather than `op_types` still calibrates every tensor, which avoids
  an ORT crash on the uncalibrated attention Softmax. These are yolo26 models with attention; expect
  to need this.
- Report per model: INT8 file MB and the compression ratio vs FP32, top-1 accuracy delta vs FP32
  **on the held-out split**, agreement rate with FP32, and INT8 latency p50/p95 vs FP32.
- Sanity gate before accepting any INT8 artifact: if top-1 accuracy drops more than a few points or
  agreement collapses, the quantization is broken — **fix it or report FP32 only.** A broken INT8
  number is worse than no INT8 number.

---

### V6 — Wire in-browser inference (Option A only)

Without this, "on-device" cannot be written. This is production frontend work, so it belongs on a
branch under the R-series gates, not in the paper folder.

- Add `onnxruntime-web` to `frontend/package.json`. **Confirm the current stable version by
  searching the npm registry / official docs at install time** — AGENTS.md rule 7 forbids
  version-from-memory — and note the version and source in the commit message.
- Implement a client module that loads `/models/<name>.onnx` via `InferenceSession`, replicates the
  V4 preprocessing in the browser (canvas resize + center-crop + `/255` + NCHW), runs inference, and
  maps `output0` through `<name>_classes.json`.
- Gate it behind a flag, default off, per the project's dark-launch convention (see the
  `CHUNK_FALLBACK_ENABLED` precedent in AGENTS.md).
- **Watch the bundle budget.** `frontend/package.json` sets a `size-limit` of 650 KB gzip First Load
  JS (baseline 621 KB, W7 target 200 KB). `onnxruntime-web`'s WASM artifacts must be lazy-loaded, not
  pulled into First Load, or `pnpm size` fails.
- Standing gates apply before merge: full backend suite green with no new failures vs baseline
  (the 5 `scripts/test_live_e2e.py` failures are environmental — they need a live server), golden
  replay 50/50, `pnpm build` green.
- Then measure real in-browser latency (Playwright is already a devDependency) and report device,
  browser, and whether WASM SIMD/threads were active. **Do not reuse the Python ORT-CPU number as a
  browser number** — they are different runtimes.

---

### V7 — Documentation and claim cleanup (unconditional, do this regardless of option)

- `paper/EACL Demo/README.md` §1 theme 1: **"INT8 ONNX crop/disease classification"** is false today
  (not INT8, not loaded by any code). Rewrite to match whichever option is chosen. Also drop the
  header's "ALL 8 EXPERIMENTS EXECUTED AND VERIFIED" / "100% Executed, Verified & Committed" — six
  of the eight are simulations (`STATE.md` §2).
- Manuscript: delete **96.4 % crop ID** (it is an intent-classifier crop-slot number, not vision),
  **91.2 % potato disease** (exists nowhere), and the illustrative **0.94** Late Blight confidence.
  Replace with V2/V4 measurements or with nothing.
- `tab4_deployment_footprint.tex`: **2.63 GB disk / 3.70 GB RAM** must become the real numbers.
  E07 measured 187.3 MB minimal deployment with `total_onnx_mb: 0`; that ONNX figure changes once
  V3 lands and E07's scan roots are updated.
- Fix `run_e07_deployment_footprint.py`'s hardcoded `WS = Path(r"d:\KrishokTech Advisory System")`
  → resolve from `__file__`.
- Every vision claim must say **classification, not detection**. There is no detection artifact;
  `ultralytics_classifier.py:30-33` actively refuses to fabricate boxes and AGENTS.md §3 says the
  checked-in artifacts are `task: classify`. Do not write "object detection" or "bounding box".
- Append results to `E02_multimodal_diagnostic_workflow/README.md` and register every new file in
  `paper/EACL Demo/manifest.yaml`.
- Update `state/STATE.md` §8 after each task lands — that file is how the next session survives
  compaction.

---

## 3. Acceptance criteria

A task is done when all of the following hold:

1. The script runs to completion with `backend\.venv\Scripts\python.exe` and writes its JSON.
2. Every number in that JSON came from an actual measurement in that run. No literal constants.
   A reviewer can `grep` the script for suspicious float literals and find only thresholds and
   config, never results.
3. The JSON records git HEAD, timestamps, library versions, input SHA-256s, and machine CPU info.
4. Unmeasurable quantities are explicitly `unmeasured` with a reason (corn accuracy, and possibly
   INT8 for potato/rice/brassica).
5. `README.md` for the layer and `paper/EACL Demo/manifest.yaml` are updated.
6. `state/STATE.md` §8 reflects the new state.
7. Nothing under `paper/CEA Paper/` was read, modified, or referenced.
