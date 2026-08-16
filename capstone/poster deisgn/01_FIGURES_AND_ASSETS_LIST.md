# Poster Figures, Assets, and Defensible Numbers List

Every visual asset the poster needs, with its source file, planned size, and caption. Every defensible number in one place, with its citation. **Do not put any number on the poster that is not in §2 of this file.**

> **Node count:** 2,882 is the final, authoritative number for the knowledge graph (per team direction). Use 2,882 everywhere; do not use 2,120.

---

## 1. Figures and assets to produce

### 1.1 Hero pipeline diagram (B1) — the centrepiece

- **What:** Four-stage agentic pipeline. Input → Safety/Router → Retrieval → Generation → Verifier → Answer + audit log. Unsafe branch → 16123 + 999.
- **Reuse base:** `capstone/figure.png`. Redraw larger, cleaner, A0-grade. Add: audit-log box, 16123/999 branch, six safety category chips, structured-verifier label ("14-field schema, 6 relation types").
- **Source of truth:** `docs/03_safety_aware_agentic_pipeline.md`, `docs/refactor/ARCHITECTURE.md`, `backend/app/application/qa_pipeline.py`, `paper/system_evolution_plan_2026/execution_planning_2026_08_12/06_CLAIM_SCHEMA_AND_VERIFIER.md`.
- **Size:** ~250 × 290 mm.
- **Caption:** "Every query is classified before retrieval. Terminal safety categories return a canned redirect to 16123 and never reach the model. The structured verifier checks each chemical claim's 14 fields against retrieved passages. Every decision is written to a local audit log."

### 1.2 Retrieval Recall@10 bar chart (A3)

- **Numbers (AgriTrust paper):** Hybrid RRF 0.539 · BM25 0.506 (95% CI [0.474, 0.538]) · ColBERT 0.487 · Dense Gemini-001 0.464 · BGE-M3 0.408.
- **Source:** `paper/done papers/AgriTrust.pdf`; `paper/system_evolution_plan_2026/T01_PDF_EXTRACTION.md`.
- **Size:** ~130 × 90 mm.
- **Caption:** "BM25 outperforms dense retrieval by 9% (p<0.001, Wilcoxon) on Bengali. Dense collapses on colloquial farmer queries (R@10 = 0.093) but is near-perfect on formal safety queries (0.970). Hybrid RRF wins overall."
- **Style:** leaf green for top bar, bone for rest, tabular numerics.

### 1.3 Soil moisture pred-vs-actual scatter plot (C2) — NEW, real result

- **What:** Scatter plot of OOF predicted kPa vs actual kPa, with the R²=0.39 / RMSE=4.09 annotation.
- **Source file:** `backend/ml_assets/soil/pred_vs_actual.png` (already generated from the EffNet-B0 5-fold OOF run). Use directly, or regenerate a cleaner labelled version from `backend/ml_assets/soil/oof_predictions.csv`.
- **Size:** ~130 × 100 mm.
- **Caption:** "EfficientNet-B0, 5-fold cross-validation, out-of-fold predictions. R²=0.39, RMSE=4.09 kPa — a 22% improvement over the mean-predictor baseline (RMSE 5.26 kPa)."

### 1.4 AgriVision crop disease accuracy table (C1) — NEW, real result

- **What:** 5-row table: Crop × {Classes, Test Top-1, Weighted F1, Model, Edge export}.
- **Source:** `docs/disease detection/AgriVision_1.pdf` (AgriVision BD, Project Report 3, April 2026). Also confirmed in `backend/ml_assets/vision/verification_report_live.md` for the live-checked-in weights.
- **Numbers:**
  - Brassica: 11 classes, 97.29% (PyTorch) / 96.59% (ONNX), F1 0.965, YOLO26s + BrassicaHybridNet
  - Rice: 8 classes, 96.49%, F1 0.965, YOLO26n, 1.1 ms/img on T4
  - Corn: 4 classes, 97.23%, F1 0.972, YOLO26s
  - Potato: 3 classes, 95.04%, F1 0.951, YOLO26s, TFLite INT8 1.6 MB
  - Wheat: 11 classes (upgraded), 88% live (44/50 sweep), YOLO26s
- **Dataset:** ~22,544 train images, ~27,817 total, filtered to Bangladesh-relevant classes from Mendeley + Kaggle.
- **Size:** ~240 × 100 mm (treated as a graphic block).
- **Caption:** "32 disease classes across 5 crops. Models exported to ONNX FP16 + TFLite INT8/FP16 for <30 ms inference on Android edge devices."

### 1.5 Field photo, Pabna (A1)

- **Source:** `demo-assets/images/` or a Pabna photo from `dataset_release/soil_moisture/`.
- **Size:** ~130 × 90 mm.
- **Caption:** "Pabna District field campaign, May 2026 — 722 tensiometer-labeled soil photos collected over 3 days."

### 1.6 Product screenshot triptych (C3) — three screenshots, each ≥ 12 × 18 cm

1. **`/detect`** — Rice leaf → pipeline rail animating → Leaf Blast diagnosis + treatment card. Source: `frontend/src/app/(app)/detect/page.tsx`. Demo image: `demo-assets/images/` rice sample.
2. **`/chat`** — Banned-chemical query `প্যারাকোয়াট দিয়ে কীভাবে স্প্রে করব?` → 16123 canned response + trace with stages skipped. Source: `frontend/src/app/(app)/chat/page.tsx`.
3. **`/analytics`** — Safe-vs-blocked donut + category bars + CSV export. Source: `frontend/src/app/(app)/analytics/page.tsx`.

### 1.7 Benchmark composition bar (A2, optional)

- 4-track composition: General 28,993 · Treatment 11,224 · Table 25,650 · Safety 20,112 = 85,979.
- **Source:** `paper/system_evolution_plan_2026/execution_planning_2026_08_12/research_artifacts/reports/data_audit/T05_CLAIM_LEDGER_v1.md` (VERIFIED).
- **Size:** ~130 × 60 mm.

### 1.8 Comparison table (A5)

- 7-row × 4-col: Capability × {Generic chatbots, KrishokBondhu, KrishokChat}. Content in `00_POSTER_DESIGN_MASTER.md` §A5.
- **Source:** `docs/competitive-landscape.md`.
- **Size:** ~240 × 90 mm. KrishokChat column highlighted with ochre edge.

### 1.9 QR codes (C6)

- Three QR tiles, ~40 mm: Dataset (HuggingFace RaiyanKhaan/krishokChat) · Code/Demo (GitHub) · Papers (`paper/done papers/` + AgriVision report). Do NOT use the deprecated arXiv v1 ID 2606.29243.

### 1.10 Structured verifier schema visual (B3, optional)

- **What:** A compact visual of the 14-field claim schema (crop, disease, action, chemical, formulation, amount, unit, denominator, interval, PHI, polarity, applicability, uncertainty, source_id) and the 6 relation types.
- **Source:** `paper/system_evolution_plan_2026/execution_planning_2026_08_12/06_CLAIM_SCHEMA_AND_VERIFIER.md`.
- **Size:** ~120 × 80 mm.

---

## 2. Defensible numbers master list (use ONLY these on the poster)

### 2.1 Benchmark dataset (KrishokChat paper, EACL 2026)

| Number | Value | Source file |
|---|---|---|
| Total benchmark instances | **85,979** (4 tracks) | `T05_CLAIM_LEDGER_v1.md:30` ✅ |
| General QA | 28,993 | same, line 31 ✅ |
| Treatment QA | 11,224 (7,437 chemical-bearing, 66.3%) | same, lines 32, 37 ✅ |
| Table QA | 25,650 (6 dialects × 4,275) | same, line 34 ✅ |
| Safety | 20,112 (3,216 refusal + 16,896 re-query) | same, line 33 ✅ |
| Farmer benchmark | 1,000 (350 held-out; 300 field interviews Rajshahi & Natore; 483 FB; 217 krishibangla) | same, lines 35–36; `paper/literature review/09_ict4d_global_south.md:13` ✅ |
| Source publications | 284 | same, line 42 ✅ |
| Institutions | 13 | `paper/literature review/04_agri_ai_advisory_systems.md:22` ✅ |
| Knowledge graph nodes | **2,882** (final, authoritative) | `T01_PDF_EXTRACTION.md:358` ✅ |
| Image-linked nodes | 1,022 (35.5%) | `T05_CLAIM_LEDGER_v1.md:50` ✅ |
| Entities | 19,768 (6.9/node) | `T01_PDF_EXTRACTION.md:383` |
| Factual triples | 17,501 | same, line 384 |
| Dialects | 6 | `T05_evidence_manifest_v1.md:45` ✅ |
| Safety taxonomy | 12 categories + 6 re-query slots | `T01_PDF_EXTRACTION.md:498–499` ✅ |
| Inter-annotator κ | 0.72 (farmer+safety), 0.78 (KG-grounded) | same, line 399 |
| License | CC-BY-4.0; HuggingFace RaiyanKhaan/krishokChat | `paper/literature review/03_low_resource_nlp_bengali.md:50` ✅ |

### 2.2 Retrieval (AgriTrust paper, SIGIR-AP 2026)

| Number | Value | Source |
|---|---|---|
| Answerable queries | 900 of 1,000 | `T01_PDF_EXTRACTION.md:404` |
| Hybrid RRF R@10 | **0.539** | same, line 365 |
| BM25 R@10 | **0.506** (95% CI [0.474, 0.538]) | same, line 416 |
| ColBERT R@10 | 0.487 | same, line 430 |
| Dense Gemini-001 R@10 | 0.464 | same, line 437 |
| BGE-M3 R@10 | 0.408 | same, line 437 |
| BM25 vs Dense | +9%, p<0.001 (Wilcoxon) | same, line 416 |
| Dense on farmer queries | R@10 = 0.093 | same, line 435 |
| Dense on safety queries | R@10 = 0.970 | same, line 443 |
| BM25 cross-lingual collapse | 0.506 → 0.004 (99% drop) | same, line 418 |

### 2.3 Model fine-tuning (KrishokChat-4B)

| Number | Value | Source |
|---|---|---|
| Base | Gemma-4-E4B, 4-bit (unsloth/gemma-4-E4B-it-unsloth-bnb-4bit) | `T05_CLAIM_LEDGER_v1.md:57` ✅ |
| LoRA | r=32, α=64, dropout=0 | same, line 58 ✅ |
| 1-epoch step | 2,680 | same, line 60 ✅ |
| Effective batch | 16 (micro 4 × accum 4), max seq 4,096 | `T01_PDF_EXTRACTION.md:319` |
| Hardware | single NVIDIA L4 (24 GB, Colab Pro), bfloat16 | same, line 320 |
| General QA Token F1 (closed-book) | **0.314** (KrishokChat-4B) vs 0.165 (LLaMA-3.1-8B) | same, lines 133–136 |
| General QA significance | p ≈ 6.7×10⁻⁵ vs LLaMA-3.1-8B | same, line 323 |
| Treatment QA Correct% (closed-book) | 35.55% | same, line 205 |
| Chemical hallucination floor (oracle) | 4.05–7.00% across 6 LLMs | same, lines 101–102 |
| Safety compliance (KrishokChat-4B) | 0.31% (1/323) | same, lines 255, 272 |

### 2.4 Crop disease detection (AgriVision BD report + live verification) — NEW

| Number | Value | Source |
|---|---|---|
| Crops | 5 (Brassica, Rice, Corn, Potato, Wheat) | `docs/disease detection/AgriVision_1.pdf` ✅ |
| Total disease classes | 32 (Brassica 11 + Rice 8 + Corn 4 + Potato 3 + Wheat 6); live system wheat upgraded to 11 → 37 total | AgriVision PDF + `verification_report_live.md` ✅ |
| Training images | ~22,544 train / ~27,817 total | AgriVision PDF Table 2 ✅ |
| Brassica test Top-1 | **97.29%** (PyTorch) / 96.59% (ONNX, 410 imgs) | AgriVision PDF ✅ |
| Rice test Top-1 | **96.49%** (YOLO26n, 342 imgs) | same ✅ |
| Corn test Top-1 | **97.23%** (YOLO26s, 940 imgs) | same ✅ |
| Potato test Top-1 | **95.04%** (YOLO26s) | same ✅ |
| Potato MCC / Kappa | 0.9176 / 0.9173 | same ✅ |
| Wheat live sweep | 44/50 (88%), 11 classes, 50/50 (100%) with Bengali treatment | `backend/ml_assets/vision/verification_report_live.md:23` ✅ |
| 437-image library | Bengali disease info 436/437 (99.8%) | same, line 30 ✅ |
| BrassicaHybridNet | EffNet-B1 + ViT SE, 7.3M params, 93.45% test, TFLite FP16 13.98 MB | AgriVision PDF ✅ |
| Edge export | ONNX FP16 + TFLite INT8/FP16, <30 ms/image on Android | same ✅ |
| Rice inference | 1.1 ms/image on T4 GPU | same ✅ |
| Potato TFLite size | 1.6 MB INT8 | same ✅ |
| Crop classifier (live) | 6 families (Brassica, Corn, GourdGuava, Potato, Solanacea, Wheat) | `verification_report_live.md:43` ✅ |

### 2.5 Soil moisture — Field dataset + EffNet-B0 model (NEW, real results)

| Number | Value | Source |
|---|---|---|
| Raw images | 722 tensiometer-labeled RGB (0.0–21.5 kPa) | `dataset_release/soil_moisture/README.md:7` ✅ |
| Usable after dedup | 693 (29 duplicate images removed) | `backend/ml_assets/soil/Runed_soil_effnetB0.ipynb` output ✅ |
| Location | Pabna District, 3-day campaign May 29–31, 2026 | `README.md:5–6` ✅ |
| Soil types | 6 USDA-equivalent (Doash, Atel, Bele, Bele_Doash, Atel_Doash, Poli) | `README.md:15`; notebook output ✅ |
| Crops | 14 | `dataset_summary.json:34–47` ✅ |
| Growth stages | 8 | same ✅ |
| Split | Series-stratified, leakage-checked, 5-fold CV | notebook + README ✅ |
| Model | EfficientNet-B0, 4.17M params | notebook output ("4171645 total params") ✅ |
| Tuning | Optuna, 15 trials, SmoothL1Loss, 15 epochs | notebook Optuna logs ✅ |
| **Overall OOF RMSE** | **4.09 kPa** | Computed from `oof_predictions.csv` ✅ |
| **Overall OOF MAE** | **3.19 kPa** | Computed from `oof_predictions.csv` ✅ |
| **Overall OOF R²** | **0.39** | Computed from `oof_predictions.csv` ✅ |
| Mean baseline RMSE | 5.26 kPa (R²=0.0) | Computed ✅ |
| **Improvement** | **22% RMSE reduction over baseline** | Computed ✅ |
| Per-fold R² | 0.521 (best, fold 0), 0.441, 0.401, 0.353, 0.224 | Computed ✅ |
| Per-soil MAE range | 2.98 (Atel, best) – 3.92 (Bele) kPa | notebook output ✅ |
| Per-crop MAE range | 1.89 (Lechee, best) – 4.37 (Betel_Nut) kPa | notebook output ✅ |
| Scatter plot file | `backend/ml_assets/soil/pred_vs_actual.png` | ✅ |

### 2.6 Safety architecture (the SOTA approach)

| Number | Value | Source |
|---|---|---|
| Safety categories | 6 (safe_agri, banned_chemical, self_harm, off_topic, prompt_injection, low_confidence) | `AGENTS.md §4`; `backend/app/domain/enums.py` ✅ |
| Claim schema fields | 14 (crop, disease, action, chemical, formulation, amount, unit, denominator, interval, PHI, polarity, applicability, uncertainty, source_id) | `06_CLAIM_SCHEMA_AND_VERIFIER.md` ✅ |
| Relation types | 6 (supported, contradicted, partially_supported, unsupported, ambiguous, not_applicable) | same ✅ |
| Verifier approach | Deterministic-first: parser/normalizer + structured relation matcher + fail-closed safety policy; optional NLI as bounded resolver | same ✅ |
| Fail-closed rule | Missing evidence → abstain; safety-critical claims need all fields | same ✅ |
| Audit log | Local JSONL, `backend/app/logs/safety_audit.jsonl`, surfaced via /analytics | `docs/03_safety_aware_agentic_pipeline.md` ✅ |
| 16123 helpline | Real, currently active government Krishi Call Center | `frontend/src/lib/constants.ts:15`; `docs/competitive-landscape.md` ✅ |

### 2.7 Impact / market context

| Number | Value | Source |
|---|---|---|
| Farming households lacking Bengali advisory | ~47 million | `capstone/synopsis.tex:88` |
| Krishi Call Center 16123 volume | 92,094 calls FY 2025–26; ~180–200/day | `docs/competitive-landscape.md:14` |
| Monetization comparators | PxD 7.8M users; ACI IDSS/Fosholi €3.5M 2025 target | `docs/competitive-landscape.md §c` |
| Disease yield loss if undetected | 20–40% | `docs/disease detection/AgriVision_1.pdf` (intro) |

### 2.8 Papers

| Paper | Venue | Status | Source |
|---|---|---|---|
| KrishokChat — Provenance-Traceable Multi-Task Bengali Benchmark with Safety-Critical Chemical Advisory | EACL 2026 | under review | `paper/done papers/KrishokChat__…Benchmark_with_Safety_Critical_Chemical_Advisory.pdf` |
| AgriTrust | SIGIR-AP 2026 | under review | `paper/done papers/AgriTrust.pdf` |
| AgriVision BD — Multi-Crop Leaf Disease Detection for Edge-Device Deployment | Project Report 3, April 2026 | done | `docs/disease detection/AgriVision_1.pdf` |

> **Do not cite arXiv:2606.29243** (deprecated, invalid per `docs/PAPER_POLICY.md`).

---

## 3. Numbers to NEVER put on the poster (not measured / not in sources)

These are explicitly unmeasured or not in the cited sources. Stating them would be fabrication.

- **End-to-end latency / throughput** for the live system (not measured).
- **mAP / IoU / bounding-box counts** (vision is classification-only — frame as "classification" not "detection" when discussing boxes; the AgriVision accuracies are top-1 classification accuracy, which IS measured and IS fine to cite).
- **Invented TAM / SAM / SOM / revenue projection** (not built — qualitative business lanes only with comparator evidence).
- **The deprecated arXiv v1** (2606.29243) — do not cite.
- **Any soil numbers other than the EffNet-B0 5-fold OOF results** (RMSE 4.09 kPa, R²=0.39). Do not cite RandomForest/XGBoost/Ensemble/CNN-Small/ResNet numbers from `kaggle output/soild_moisture_experiments_frozen_fixed.ipynb` — only the EffNet-B0 results go on the poster.
- **The "110-word dialect map"** (unrecoverable in repo) — cite "6 dialects" from the benchmark instead.
- **Crop classifier top-1 accuracy on the live runtime** beyond the wheat sweep and library matrix (the AgriVision paper accuracies are the training-evaluation results; the live runtime verification is the 88% wheat sweep + 99.8% library coverage).

**Framing rule:** if a judge asks for something not yet measured, the answer is "ongoing work" or "part of the roadmap" — never "we don't have it." This is a competition.