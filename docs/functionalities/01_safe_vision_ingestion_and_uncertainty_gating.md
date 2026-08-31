# 01 — Safe Vision Ingestion & Calibrated Uncertainty Gate

> **Module Ref:** Module 1 / Perception Layer E02  
> **Status:** Verified & Integrated (`backend/app/application/vision_pipeline.py`, `backend/app/domain/vision.py`)  
> **Test Suite:** `backend/tests/test_vision.py` (9 / 9 Passed)

---

## 1. Architectural Motivation & Problem Formulation

Standard end-to-end vision-language models often hallucinate confident crop diagnoses on out-of-distribution (OOD) foliage, weeds, or low-quality close-ups. In agricultural advisory, misidentifying a crop (e.g. diagnosing a tomato leaf as a potato plant) can lead to toxic chemical cross-application.

KrishokChat implements a **Calibrated Tri-State Decision Gate** and **Margin-Based Second-Image Request** directly over ONNX edge models.

---

## 2. Tri-State Decision Thresholds & Empirical Calibration

Let $\mathbf{p} = [p_1, p_2, \dots, p_K]$ be the softmax probability vector sorted in descending order ($p_1 \ge p_2 \ge \dots \ge p_K$), and let $\Delta = p_1 - p_2$ denote the top-1/top-2 margin.

```
                                  [ Uploaded Leaf Image ]
                                             │
                                             ▼
                                [ 6-Class Family Crop Classifier ]
                 (Brassica, Corn, GourdGuava, Potato, Solanacea, Wheat)
                                             │
                       ┌─────────────────────┼─────────────────────┐
                       │                     │                     │
                       ▼                     ▼                     ▼
               [ State A: Confident ]   [ State B: Uncertain ] [ State C: OOD / Unknown ]
               p1 >= 0.90 & Δ >= 0.20   0.40 <= p1 < 0.90      p1 < 0.40
                       │                 or Δ < 0.20               │
                       │                     │                     ▼
                       │                     ▼            [ Halt Disease Pipeline ]
                       │             [ Bengali Prompt ]   [ Return Clear Rejection ]
                       │             [ Quick Reply Chips] [ 0 LLM Cost ]
                       │                     │
                       ▼                     ▼
                [ Route to Crop-Specific Disease ONNX Classifier ]
```

### Calibrated Operating State Definitions (`VisionGateConfig`):
1. **State A — Confident Crop Classification:**
   $$\max(p_i) \ge 0.90 \quad \land \quad (p_1 - p_2) \ge 0.20 \quad \land \quad \neg\text{ConfusionRisk}$$
   * Action: Confidently routes the image tensor to the crop-specific disease classifier (e.g., Potato, Rice, Tomato).
2. **State B — Uncertain / Ambiguous Crop:**
   $$0.40 \le \max(p_i) < 0.90 \quad \lor \quad (p_1 - p_2) < 0.20 \quad \lor \quad \text{ConfusionRisk}$$
   * Action: Sets `VisionStatus.UNCERTAIN`, attaches candidate crops (`suggested_crops = [top_1, top_2]`), and returns an interactive Bengali confirmation prompt with quick-reply buttons (*"ছবিটি দেখে আলু বা টমেটো/বেগুন গোত্রের গাছ মনে হচ্ছে। নিচে আপনার সঠিক ফসলটি নির্বাচন করুন।"*).
3. **State C — Out-of-Distribution / Unknown Crop:**
   $$\max(p_i) < 0.40$$
   * Action: Sets `VisionStatus.OUT_OF_DISTRIBUTION`, halts disease models cleanly without generating false diagnoses, and informs the farmer:
     > *"ছবিটি আমাদের সমর্থিত ফসলের সাথে পর্যাপ্ত মিলছে না। অনুগ্রহ করে আক্রান্ত ফসলের পরিষ্কার ছবি দিন।"*

---

## 3. Empirical Calibration Metrics (Layer E02)

Evaluated across 436 real test artifacts (`backend/ml_assets/vision/test_images/full_library`):

* **Expected Calibration Error (ECE):** $0.1233$ ($12.33\%$) for 6-Class Crop Classifier; $0.2294$ for Disease Models.
* **Brier Score:** $0.1331$ (Crop) / $0.2236$ (Disease).
* **Safe Automation Trade-Off (at $C=0.90, M=0.20$):**
  * Auto-Accept Rate: $81.71\%$ ($286/350$ in-distribution cases automated).
  * Farmer Clarification Rate: $18.00\%$ ($63/350$ deferred to interactive confirmation chips).
  * Out-of-Distribution Rejection: $95.3\%$ safe containment on non-target species (Guava, Gourd).

---

## 4. Disease Margin Calibration & Second-Image Request

When a crop disease model classifies symptoms with a narrow margin between two distinct pathologies:
$$(p_1 - p_2) < 0.15 \quad \land \quad p_1 < 0.80$$
* Action: Sets `requires_second_image = True` and `VisionStatus.REQUIRES_SECOND_IMAGE`.
* Prompts the farmer to upload a clear close-up of the underside of the affected leaf or stem to disambiguate subtle fungal lesions (e.g., Early Blight vs. Late Blight).

---

## 5. Latency & Resource Footprint

* **WASM On-Device Execution:** $26\text{--}265\,\text{ms}$ single-threaded browser inference.
* **Server-Side ONNX Runtime:** $4\text{--}20\,\text{ms}$ CPU inference.
* **Token Cost:** $0$ LLM tokens.

