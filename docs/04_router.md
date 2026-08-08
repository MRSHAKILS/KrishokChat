# TASK 04 — Crop Classifier + Disease Detection Pipeline

**Read `AGENTS.md` first. Requires Task 00 (YOLO `.pt` → `.onnx` export already done in Task 00 Step 6) and Task 01 (retrieval/generation agents exist) complete. Task 02's Detection page currently runs against mocked data — this task replaces the mock with real inference.**

---

## 0. Scope

**In scope:** crop classification, per-crop YOLO disease detection, a combined `/api/detect` response, and — the part that makes this an *advisory* result instead of a bare label — reusing your existing retrieval + generation agents to turn a detected disease name into real, grounded treatment guidance pulled from `knowledge_nodes.json`, rather than a hardcoded string per disease.

**Out of scope:** retraining or improving any `.pt` model — you're integrating what already exists. Multi-disease-per-image handling beyond what YOLO already returns. A dedicated safety wrapper around the *image* pipeline (flagged as a future task in `TASK_03`'s closing note) — this task can optionally route the resulting treatment text through the existing Verifier Agent (see Step 6), which covers the main risk (an ungrounded dosage claim) without building a whole second safety system.

---

## Step 1 — Build the model registry

You already have exported `.onnx` files per crop from Task 00 Step 6, and the crop classifier weights. Before writing any inference code, make the mapping between "crop name" → "which YOLO model to load" → "which class index means which disease" explicit and reviewable, rather than scattering it across code.

1. Write `backend/app/core/model_registry.py` (or a JSON config it reads): for each crop, the path to its exported `.onnx` YOLO model and an ordered list mapping the model's class indices to human-readable disease names (in Bengali, with an English key for internal use). Pull the actual class list from however the model was originally trained (a `data.yaml`/class-names file from the original training run) — do not guess or reconstruct this from memory, get it from the source artifact.
2. Do the same for the crop classifier's output classes → crop names.
3. Note next to the registry which crops you actually have solid, high-confidence demo images for (from `demo-assets/images/`) — this list matters for Step 4's warm-loading decision.

**Verify:** the registry file is complete, matches your actual trained classes exactly (no typos, no missing/extra classes), and is reviewed by you once before anything is built on top of it — a wrong label here silently produces a wrong diagnosis with high confidence, which is a worse failure than a crash.

---

## Step 2 — Crop classifier inference service

1. **Image Quality Pre-Check:** Before passing the image to the classifier, implement a pre-check function to detect blurriness, extreme darkness/brightness, absence of a leaf, or presence of multiple leaves. If the image fails this check, reject it and prompt the user to retake a clearer close-up photo. Support manual crop selection as a fallback if detection fails repeatedly.
2. Write `backend/app/services/crop_classifier.py`: loads the classifier `.onnx` model via `onnxruntime`, exposes a function taking a preprocessed image and returning the top predicted crop + confidence score.
3. 🔎 Confirm the correct preprocessing (resize dimensions, normalization) matches exactly what the classifier was trained with — check the original training script/notebook rather than assuming standard ImageNet normalization, a mismatch here silently tanks accuracy without erroring.
4. Define a confidence threshold below which the result is treated as "crop not recognized" (per the honest-failure state specified in `docs/ui-design-masterplan.md` Section 3.3). If confidence is low, display an explicit uncertainty message (e.g., "আমি পুরোপুরি নিশ্চিত নই..." - "I am not entirely sure") and escalate to 16123 instead of forcing a low-confidence guess through to detection.

**Verify:** run the classifier against 3–5 known sample images per crop from `demo-assets/images/` and confirm correct, high-confidence predictions; run it against one clearly-wrong or blank image and confirm it correctly falls into "not recognized" rather than confidently guessing.

---

## Step 3 — Per-crop YOLO detection service

1. Write `backend/app/services/yolo_detector.py`: given a crop name and an image, loads the matching `.onnx` model per the Step 1 registry, runs detection, and returns bounding boxes + class indices + confidence, translated into human-readable disease names via the registry.
2. 🔎 Confirm the correct pre/post-processing for your exported ONNX YOLO models (input size, NMS handling) — this differs depending on which YOLO version/export settings were used in Task 00; check Ultralytics' current ONNX inference documentation for the exported format rather than assuming it's identical across YOLO versions.
3. Return results in a normalized shape (box coordinates as fractions of image width/height, not raw pixels) so the frontend can draw annotations correctly regardless of the display size the image is rendered at.

**Verify:** run detection against known sample images for each crop and confirm boxes land visually on the correct diseased region when plotted (a quick throwaway script that draws the boxes and saves the image is enough to eyeball this — don't skip visually checking, a detector that runs without errors but draws boxes in the wrong place is a worse demo failure than an honest error).

---

## Step 4 — Warm-loading strategy

Loading every crop's YOLO model into memory simultaneously may or may not fit your available RAM/VRAM alongside the already-loaded Gemma GGUF — check this rather than assuming.

1. Add classifier + YOLO model loading to the backend's startup lifecycle (same `lifespan` pattern used for Gemma warm-loading in Task 01), so cold-load latency never happens on a live request.
2. If loading every crop's model simultaneously is memory-tight: prioritize warm-loading only the crops you identified in Step 1.3 as having solid demo images, and implement lazy-load-with-cache for the rest (load on first request, keep in memory after) — accept that a crop outside your curated demo set may have a slower first request, since it won't be part of your live demo path anyway. This is the same "Demo Mode" principle from the original masterplan: protect the exact path you'll show live, be honest about the rest.

**Verify:** startup logs confirm every prioritized model loaded successfully before the server starts accepting requests; a request for a prioritized crop never triggers a visible load delay.

---

## Step 5 — Combined `/api/detect` endpoint

1. Write `backend/app/api/detect.py`: accepts an uploaded image, runs the classifier first — if below the Step 2 confidence threshold, return the "crop not recognized" result immediately without running any YOLO model. Otherwise, run the matched crop's YOLO detector and return crop + disease + boxes + confidence.
2. Keep `backend/app/api/classify.py` as a separate, simpler standalone endpoint too (useful for testing/debugging in isolation) — but the frontend's real detection flow calls the combined `/api/detect` endpoint, not two separate round trips, to keep the request count and latency down.
3. Match the response shape to whatever Task 02 Step 6.2 documented as the expected mock shape — if this task's real shape needs to differ, update that comment in the frontend code to match reality rather than leaving it stale.

**Verify:** one `curl` multipart upload against `/api/detect` with a known sample image returns the correct combined result end-to-end.

---

## Step 6 — Grounded treatment lookup (reuse the existing RAG pipeline)

This is the step that turns "we detected a disease" into "we're giving advice," and it's free architecturally because you already built retrieval + generation + verification in Tasks 01 and 03.

1. Once a disease is identified, construct a query from it (e.g. crop name + disease name + "treatment"/চিকিৎসা) and pass it directly into the existing `retrieval_agent.py` + `generation_agent.py` from Task 01/03 — the same knowledge base, same grounding behavior, no new logic needed.
2. Decide whether to route this system-constructed query through the full Safety/Router Agent from Task 03 or skip straight to retrieval: since this query isn't raw user text, the injection/off-topic categories are irrelevant, but running it through anyway is cheap and keeps a consistent audit trail (see Step 8) — lean toward including it unless the added latency is a real problem in Step 9's testing.
3. **Do** run the resulting treatment text through the Verifier Agent from Task 03 Step 5 — dosage claims are exactly the risk category it exists to catch, and disease-treatment advice is precisely where an ungrounded number is most consequential.
4. Attach this generated, verified treatment text into the `AdvisoryCard` payload returned by `/api/detect`, alongside the raw detection result.

**Verify:** a detected disease produces treatment guidance that's clearly grounded in `knowledge_nodes.json` content (not generic model knowledge), carries the correct `ConfidenceBadge` state from the verifier, and reads naturally as one coherent advisory result rather than two stitched-together outputs.

---

## Step 7 — Frontend wiring

1. In the Detection page built in Task 02 Step 6, replace the mocked fetch with a real call to `/api/detect`.
2. Update the scanning/processing animation and (if you extended `AgentTraceStepper` to support it) show real stages: Classifying crop → Detecting disease → Retrieving treatment.
3. Confirm the "crop not recognized" state, the annotated bounding-box overlay, and the diagnosis `AdvisoryCard` (now with real, grounded treatment content and a real confidence badge) all render correctly against live backend responses.

**Verify:** the full flow — upload a real photo, watch it classify, detect, and return grounded treatment advice — works end to end through the actual UI, matching the Task 02 design reference, with no mock data remaining in the request path.

---

## Step 8 — Audit logging (reuse Task 03's log)

1. Log each detection request to the same audit log used in Task 03 (`audit_log.py`) — crop, disease, confidence, whether the treatment text was flagged by the verifier, timestamp. Reuse the existing log format/fields where they apply rather than building a second logging system.
2. This feeds the same Research-page safety metrics section from Task 03 Step 9 — worth extending that section to show detection-pipeline counts alongside the chat-pipeline counts, for one coherent "responsible AI" story on the poster instead of two disconnected ones.

**Verify:** running the Step 9 test set below produces corresponding log entries.

---

## Step 9 — Test set and latency check

1. Run the full pipeline against every image in `demo-assets/images/` for every crop you prioritized in Step 4 — confirm correct crop, correct disease, sensible box placement, and grounded, verified treatment text for each.
2. Deliberately test one image of a crop you know is *not* in your classifier's trained set — confirm the "not recognized" path triggers correctly rather than a false match.
3. Time the full pipeline end to end (upload → classify → detect → treatment lookup → response) for your prioritized demo images specifically — this is the number that matters for your 3–4 minute window. If it's slow, the likely culprits in order of probability: unnecessary reprocessing/resizing, the treatment-lookup LLM call (check whether streaming it to the UI as it's generated, same as the chat pipeline, would make it feel faster even at the same actual latency), or a model that ended up lazy-loaded instead of warm-loaded per Step 4.

---

## Step 10 — Report back

Write `TASK_04_REPORT.md`:
- Confirm the model registry (Step 1) was reviewed against the real trained class lists, not reconstructed from memory.
- Which crops are warm-loaded vs. lazy-loaded, and why.
- Whether treatment queries route through the full Safety/Router Agent or skip straight to retrieval, and the latency difference observed.
- **Vision Metrics Reporting:** Document Crop classifier top-1/top-3 accuracy, disease detection mAP@50, precision/recall, ONNX vs PyTorch latency comparisons, and treatment grounding rates.
- Full Step 9 test results and end-to-end latency numbers for your prioritized demo crops.
- Anything that deviated from Task 02's originally-mocked response shape, and confirmation the frontend comment was updated to match.

**Stop here.** This closes out the last major backend pipeline. What's left after this task is demo rehearsal, latency hardening against real numbers (the original masterplan's Day 6), and polish — not new functionality.