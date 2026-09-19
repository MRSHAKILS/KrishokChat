# Beat D+E — The Photo Narrows the Search; the Contradiction Stops It

**Status:** research pass 1 complete; vision stack implemented + largely measured; re-validation required after classifier update; E08 README repair required  
**Date:** 2026-09-17  
**Role in EACL story:** the only beat with a physical artifact — photo in, scoped evidence out, contradiction badged. Demo gold and the paper's most tangible novelty.

---

## 1. The human moment

The farmer can't name the disease — but they can photograph it. They write "begun gache poka" (brinjal has insects) and attach a photo. The photo shows potato late blight. A text-only system retrieves brinjal insecticides. A vision-only system diagnoses potato blight and never notices the text disagrees. Both are confident. One of them poisons the wrong crop.

KrishokTech does two things no single-modality path can:

1. **Narrows:** the photo identifies the crop first, so retrieval searches potato records instead of the whole library.
2. **Stops:** when text says brinjal and the photo says potato, the pipeline surfaces a mismatch badge and asks which crop to trust — before any chemical is named.

**Feel-line candidate:**

> The photo is not a second opinion. It is a fence around the evidence — and when the words jump the fence, the system says so.

This line is a candidate, not final paper prose.

---

## 2. What the evidence already establishes

### 2.1 Crop-disease image classification is established; scope-gated advisory is not

Plant-disease classifiers (PlantVillage lineage and successors), YOLO-family classifiers, on-device INT8 quantization, and agricultural vision-language models (AgroGPT, WACV 2025) are all prior art. AgroGPT-3B/7B beat ChatGPT-class models on fine-grained disease identification — in English, as diagnosis endpoints.

**Cannot claim as new:** a crop classifier, a disease classifier, INT8 quantization, on-device inference, or photo-based diagnosis.

What has no verified precedent in Bengali advisory: using the classifier output to **restrict the retrieval corpus before text search**, routing through calibrated tri-state gates (OOD / uncertain / confident) with Bengali recovery prompts, and **badging text-vs-image crop conflict** as a first-class pipeline event with a measured rate.

### 2.2 Multimodal contradiction handling is an open gap

Vision-language consistency work exists in general ML, but no Bengali agricultural system publishes a text-vs-image crop-conflict detection rate, and no accepted ACL/EACL demo shows image-conditioned retrieval-space reduction (verified in the Beat A lit pass — open question D3, still open). Our E08 is, to current knowledge, the first measured number in this slot.

### 2.3 On-device agricultural inference is claimed often, measured rarely

Papers routinely claim "mobile-ready" from model size alone. Our stack has what reviewers actually accept: per-model accuracy on local labeled sets, FP32-vs-`.pt` parity with deltas, INT8 with reportability gates, and browser WASM timings measured in a real browser harness — not Python timings relabeled.

---

## 3. Why vision-as-scope is load-bearing in this system

1. **It repairs Beat A's worst case.** A crop-less symptom query that text alone cannot scope (Beat B would have to ask) can be scoped by the photo instead — asking costs a turn, a photo costs nothing the farmer hasn't already offered.
2. **It prevents the exact error Beat F fears.** Cross-crop chemical binding happens when retrieval searches across crops. A crop fence before retrieval removes the error class instead of asking the verifier to catch it afterward.
3. **It handles the failure the text path cannot see.** "Begun" written confidently with a potato photo attached is invisible to text-only gating (the crop slot is *filled*, just wrong). Only cross-modal comparison catches it.
4. **It degrades honestly.** Blurry/dark photo → Bengali retry prompt. Uncertain crop (narrow margin, confusion family) → crop chips. Unknown crop → OOD refusal. Low-confidence disease → second-photo request, then 16123 escalation. Every degradation is a status, a prompt, and an audit event — never a guess.

---

## 4. What KrishokTech does out of necessity

```text
photo + optional text
  ↓
image_quality gate (size/brightness/variance → Bengali retry prompt)
  ↓
crop source decision: user-verified hint bypasses classifier (farmers know their crop);
  otherwise 10-class classifier with tri-state gate:
    OOD (p1 < ood_thresh) → refuse + retry prompt
    UNCERTAIN (margin/threshold/confusion-family) → crop chips in Bengali
    CONFIDENT → route to that crop's disease model(s)
  ↓
disease model(s) at per-model calibrated thresholds;
  narrow margin → one-shot second-photo recovery → else 16123 escalation
  ↓
DIAGNOSED → QA advisory with crop+disease pre-bound + seed sources + verifier flags;
  KB fallback if the LLM is unavailable
  ↓
TEXT PRESENT? compare text crop vs image crop:
  mismatch → badge + confirm-crop before any chemical (qa_pipeline cross-modal halt)
```

Classification-only honesty is a design rule, not a limitation to hide: the checked-in artifacts are classifiers, so the workflow reports confidence and never manufactures bounding boxes.

---

## 5. Current implementation evidence

### Implemented (real code, read 2026-09-17)

- `backend/app/application/vision_pipeline.py` (488 lines) — full workflow above: quality gate, hint bypass, tri-state crop gate with confusion-family risk (solanaceae/poaceae), per-model disease thresholds, second-image recovery, healthy/unknown handling, QA advisory with bound crop+disease + seed sources + verifier flags, KB fallback, full trace + audit.
- `backend/app/application/qa_pipeline.py` L386 — cross-modal contradiction halt (text crop vs image crop → clarification, INTERACTIVE_CLARIFICATION + A4).
- Browser path: `onnxruntime-web/wasm` lazy chunk behind `NEXT_PUBLIC_VISION_ONDEVICE_ENABLED`, `vision-ondevice.ts` preprocessing, `detect/page.tsx` wiring, `frontend/public/models/` artifacts (per STATE V6; re-verify after classifier update).

### Measured (frozen artifacts, 2026-08-30)

- Per-model top-1 on local labeled sets: potato 0.900 (n=30), rice 0.925 (n=80), wheat 0.941 (n=800), brassica 0.912 (n=102), crop-router 0.941 — `results_real_pt_baseline.json`.
- 100% FP32-vs-`.pt` agreement, max delta 5e-05, n=1,237 — `results_real_onnx_parity.json`.
- INT8: 4 accepted by parity gate; only crop (n=578) + wheat (n=400) reportable; rice rejected (2.5pp drop); corn unmeasured — `vision_int8_report.json`.
- WASM single-thread p50 26–265ms in real browser harness (Playwright + static server) vs Python ORT-CPU 4–20ms — both measured, never substituted.
- E08 cross-modal: **68/80 = 85.0%** divergence under conflicting crop hint, real `.pt` + BM25-StubLLM harness, per-image records — `results_real_crossmodal.json` (DONE_REAL, seed 42).

### Corrections discovered in this pass (must be fixed, not hidden)

1. **Classifier is 10-class WITH Rice — manuscript right, code comments + STATE stale.** Disk `class_names.json`: Cabbage, Cauliflower, Chili, Eggplant, Gourd, Guava, Others, Potato, Rice, Tomato. But `vision_pipeline.py` comments still say "6-class crop classifier… trained without Rice" and describe a wheat→rice mitigation for a world without Rice; STATE.md §4 also says 6 classes. Git log shows post-freeze commits ("classifier-updated", "chilli trained"). **Consequence: E02 parity/accuracy numbers were measured on older checkpoints and must be re-run before the paper.** Also verify whether the wheat-mitigation path still triggers correctly with Rice present.
2. **E08 README documents the wrong experiment.** It claims "100.0% conflict detection" and describes `run_e21.py` (the 4000-query simulation also sitting in E08's scripts folder). The real runner is `run_real_e08_crossmodal.py` and the real number is 85.0%. **Fix: rewrite the README to the real runner; move or delete the stray `run_e21.py`; never quote 100%.**
3. **E08's "detection" needs precise framing.** The runner defines `mismatch_detected` as output divergence between the image-only run and the conflicting-hint run (crop or status differs). That proves conflicts propagate visibly instead of being silently absorbed — it is not yet a measurement of the user-facing badge rate on real text+image pairs. The 12/80 non-divergent cases need a cause analysis (which statuses, which families).
4. **Chilli model path unresolved.** No `class_names.json` under `backend/ml_assets/vision/chilli/` (naming may differ: chili vs chilli). Resolve before any chilli claim.

### Not yet measured

- E02 re-run on current checkpoints (P0 — see experiment plan).
- User-facing badge trigger rate on real text-crop vs image-crop pairs through the QA pipeline (P1 — the number the paper's S3 vignette actually needs).
- Retrieval-space reduction attributable to the image fence: same query with/without image scope, gold-in-scope + candidate-count delta (P1 — the "fence" claim needs this, else it's architecture prose).
- Second-photo recovery success rate; OOD refusal precision on non-crop images.

---

## 6. Defensible novelty statement — conditional on re-validation

Do **not** claim:

> First on-device crop-disease diagnosis. / 100% conflict detection. / 10-crop anything without the re-run.

Conditional, defensible wording:

> Photo-based diagnosis is established; KrishokTech uses the photo as a retrieval fence. A tri-state gated classifier routes each image to one crop's disease models — with Bengali recovery prompts at every degradation — and the resulting crop pre-binds the advisory query while the text crop is checked against it: on 80 conflicting image–hint pairs the pipeline visibly diverges in 68 cases instead of silently merging, and every model ships with measured accuracy, parity, INT8 reportability, and real browser timings.

Conditions: E02 re-run on current checkpoints; E08 framed as divergence-with-badge-path; README repaired.

---

## 7. Candidate paper paragraph sequence

1. **Opening:** the farmer who can't name the disease but can photograph it; the brinjal-text/potato-photo trap.
2. **Failure:** text-only retrieval poisons the wrong crop; vision-only diagnosis never sees the disagreement.
3. **Design response:** fence (crop-gated routing + pre-bound advisory query) + badge (cross-modal halt + confirm-crop) + honest degradation in Bengali at every step.
4. **Evidence:** per-model accuracy + 100% parity + INT8 reportability + WASM timings + 68/80 divergence, each scoped to its artifact.
5. **Demo payoff:** reviewer uploads a potato-leaf photo under brinjal text, watches the badge appear before any chemical — the most filmable 20 seconds of the screencast.

---

## 8. Reviewer objections to pre-empt

- "PlantVillage did this" → diagnosis, yes; retrieval fencing + conflict badging with rates, no.
- "85% of what, exactly?" → divergence definition stated; badge-rate study (P1) upgrades it to the user-visible claim.
- "Your README says 100%" → repaired; the real artifact always said 85%.
- "Checkpoints changed after E02" → disclosed; re-run is P0 and in the plan.
- "10-class vs 6-class?" → 10-class current; stale comments fixed; re-run confirms.
- "WASM numbers are Python numbers" → no: separate browser harness, both reported, never substituted.
- "INT8 for all models?" → no: only crop+wheat reportable; rice rejected; corn unmeasured. The gate is the story, not the compression.

---

## 9. Decision after Beat D+E pass 1

**Keep D+E as contribution C2 — the most demonstrable, most filmable, least contested novelty.** But it is gated on the E02 re-run: no vision number enters the paper until it is re-measured on current checkpoints. The README repair and the divergence-framing fix are editorial and immediate.

Next: **Beat C+G (cost ladder + last-mile)** — the deployment soul: tier economics, offline/SMS/16123, and the "advice that can't arrive is useless" close. Then synthesis: kill-list, `problems_we_solved.md`, `paper_outline.md`.

---

## 10. Questions for the project team

1. Approve the E02 re-run on current checkpoints (all 6 models + parity + INT8 gates + browser timings)?
2. Confirm the chilli model directory name and class list for the record.
3. Should the wheat→rice mitigation stay, given the classifier now has Rice — or is it legacy to remove?
4. Approve rewriting the E08 README to the real runner and removing/relocating the stray `run_e21.py`?
5. Is the text+image badge-rate study (P1) in scope for this paper, or does E08-divergence + implemented badge path suffice?
