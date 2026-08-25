# R10 — On-Device Classifier Export (U1) + Confidence-Gated Upload (U3)

- **Status:** PLANNED — NOT STARTED. Spec only; a coder agent implements it.
- **Plan ref:** `00_SCOPE_OUTLINE.md` U1/U3 + `07_ARCHITECTURE_REFINEMENT_PLAN.md` Part F + Part J item R10
- **Depends on:** R9 (offline pack + data-aware SW established the offline story this completes)
- **Blocks:** the U1 mobile-latency paper claim
- **Amendment:** none — additive on-device path; the server vision route stays the fallback and default

## Goal

Complete the mobile story: export the **existing** crop + potato disease
classifiers to an on-device INT8 format, run diagnosis **on the phone** (offline,
target < 150 ms), and **only upload the image when the on-device model is unsure**
(confidence-gated), with client-side resize→WebP→EXIF-strip first. This is the U1
+ U3 pair from doc 00.

Scope: the **crop classifier + potato disease classifier** only (the potato
spine). The other four disease classifiers (rice, wheat, corn, brassica) export
the same way later as a data/asset addition — do not do all six here.

## Hard reality checks (do not overclaim — AGENTS.md)

- **Classification only.** The checked-in artifacts are `task: classify` (the
  adapter `ultralytics_classifier.py:30` refuses to fabricate boxes). R10 exports
  *classifiers*; it must **not** claim on-device object detection.
- **No on-device generative LLM.** Doc 00 §edge-reality: generation stays
  server-side. R10 is vision-only.
- **Accuracy parity gate.** The INT8 on-device model must match the server model
  within the doc-00 tolerance (~1.5% top-1). If it does not, R10 reports the gap
  honestly and the upload gate widens — it does not ship a worse model silently.

## Two halves

### Half 1 — Export + validate (backend/offline)

- **Create** `backend/scripts/export_vision_ondevice.py` — loads the existing
  `crop_classifier/model.pt` and `potato_disease/model.pt`, exports to the target
  on-device format (Ultralytics supports TFLite/ONNX export; the locked stack
  §3 already names ONNX for inference — **verify current Ultralytics export API +
  the smallest INT8 path at implementation time**, AGENTS.md rule 7). Emit to
  `frontend/public/models/<name>_int8.<ext>` + a `class_names.json` copy + a
  `metadata.json` with export params, source `.pt` SHA, and quantization method.
- **Create** `backend/scripts/validate_ondevice_parity.py` — runs both the `.pt`
  and the exported model over the existing `ml_assets/vision/test_images/`
  matrix and writes a parity report (top-1 agreement, per-class deltas, size,
  and a measured inference time). Fails loudly if agreement is below the
  tolerance.
- These are **offline scripts**; the exported model is committed as a static
  asset (no request-time export, rule 2).

### Half 2 — Client inference + confidence gate (frontend)

> **Frontend note:** modified Next.js — read `node_modules/next/dist/docs/`
> before wiring the runtime/worker, per `frontend/AGENTS.md`; commit the
> auto-generated `nextjs-agent-rules` block with your work.

- **Create** a client inference module (WASM/WebGL runtime for the chosen format
  — e.g. onnxruntime-web or tfjs-tflite; **pick and version-pin at
  implementation time**, rule 7). Loads the cached model (precached by the R9
  SW under `/models/`), runs the crop classifier then the potato disease
  classifier on the resized image, all on-device.
- **Confidence gate (U3):** if on-device top-1 confidence ≥ threshold → show the
  diagnosis locally, **no upload**. If unsure → compress (resize → WebP → EXIF
  strip) and upload to the existing server vision route, showing the farmer *why*
  ("এই ছবিটি স্পষ্ট নয়, তাই পাঠানো হচ্ছে" — the exact transparency string doc 00
  F3 / plan F call for).
- **Modify** the detect page/flow to prefer on-device, fall back to server. The
  **server route is unchanged** and remains the path when the on-device model is
  absent, unsupported by the browser, or unsure.

## Scope — create
- `backend/scripts/export_vision_ondevice.py`
- `backend/scripts/validate_ondevice_parity.py`
- `frontend/public/models/crop_classifier_int8.*` + `potato_disease_int8.*`
  (+ class names + metadata) — committed artifacts
- `frontend/src/lib/ondevice-vision.ts` (client inference + gate)
- `backend/tests/test_ondevice_parity.py` (asserts the parity report gate)
- frontend unit test for the confidence-gate decision logic

## Scope — modify
- `frontend/src/app/(app)/detect/page.tsx` + related components — on-device-first
  with server fallback + the "uploading because unsure" transparency UI.
- `frontend/public/sw.js` — add `/models/*` to the versioned precache (same
  cache-first, versioned-filename strategy R9 uses for `/packs/`).
- `.env.example` — `ONDEVICE_CONFIDENCE_THRESHOLD` (client-read).

## Do not touch
- `ultralytics_classifier.py` / the server vision route — it stays the fallback,
  unchanged. The `task: classify` refusal guard is preserved.
- The `.pt` source artifacts (read-only inputs to export).
- Safety / QA pipeline (vision is a separate capability).

## Invariants
- On-device path is **additive**: with no model, unsupported browser, or low
  confidence, behavior falls back to today's server route exactly.
- **No detection/box claims** from classify artifacts (adapter guard mirrored in
  the export metadata).
- Exported INT8 model meets the ~1.5% top-1 parity gate vs the `.pt`, proven by
  the committed parity report; otherwise R10 reports the gap and does not claim
  U1 latency as met.
- No image leaves the device when on-device confidence ≥ threshold (U3); when it
  does upload, it is resized/stripped first.
- Export is offline; the model is a committed static asset (rule 2).

## Verification gate (stop/go)
1. `uv run python scripts/export_vision_ondevice.py` then
   `uv run python scripts/validate_ondevice_parity.py` — parity report written,
   agreement within tolerance, inference time recorded.
2. `uv run pytest tests/test_ondevice_parity.py -v` — green (gate enforced).
3. Frontend unit test: confidence gate uploads iff below threshold; EXIF strip +
   WebP applied before any upload.
4. Full backend `tests/` suite — 410/7/0 baseline held (server route untouched).
5. `pnpm build` green; manual offline: potato leaf photo diagnosed locally with a
   visible "on-device / offline" indicator; a blurry image triggers the
   transparent upload path.

## Rollback
`git revert`; remove the model assets. The detect flow reverts to server-only;
nothing server-side changed.

## External sources
- **Ultralytics export API** (TFLite/ONNX INT8) — verify current syntax + the
  smallest-size INT8 path at implementation time (rule 7).
- **Client inference runtime** (onnxruntime-web / tfjs-tflite or similar) —
  choose, verify current stable version, pin it, and note the choice in
  `frontend/README` (rule 7).

## Notes for the implementing agent
- Validate accuracy **before** touching the UI. If the INT8 model fails the
  parity gate, stop and report — a wrong on-device diagnosis is worse than a
  slower server round-trip. Do not lower the tolerance to make it pass.
- Keep the model assets small enough to precache on a cheap phone; report the
  size in metadata so R11 can surface it.
- The transparency string is a trust feature, not a nicety (plan F) — show the
  farmer why an upload is happening, in plain Bengali.
