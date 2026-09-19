# Cluster 5 — Vision: Crop Disease Classification & Integration Conventions: Literature Findings (2025 → Aug 2026)

**Generated:** 2026-08-12 · **Scout:** 5 · **Status:** citation targets verified via direct fetches (arXiv abs pages, Springer/Nature/Frontiers/PMC); MARS and CropDoc unverifiable and omitted; REMOTE-CLIP, PlantCLEF 2025, AgMMU, AgroBench, SCOLD, AgriFM verified

---

## 1. Key papers

**Supervised classifiers beat VLMs in agriculture.**
- Ranario & Earles, "Are vision-language models ready to zero-shot replace supervised classification models in agriculture?", arXiv:2512.15977v3 (Dec 2025, rev. May 2026). Benchmarked open/closed VLMs on 27 AgML datasets (162 classes, 248k images). Zero-shot VLMs underperform a supervised YOLO11 baseline on every task: best VLM (Gemini-3 Pro) ≈62% under MCQA prompting; open-ended raw accuracy <25% (21%→30% under LLM semantic judging); open-source Qwen-VL-72B tops out at 42% MCQA. **Strongest evidence that KrishokTech's supervised `task: classify` pipeline is the correct anchor.**

**Vision+LLM+RAG advice pipeline.**
- Mondal, "Vision Meets Language: A RAG-Augmented YOLOv8 Framework for Coffee Disease Diagnosis and Farmer Assistance", arXiv:2505.21544 (May 2025; SN Computer Science DOI 10.1007/s42979-026-05246-4). Fine-tuned YOLOv8 detects coffee leaf diseases; disease name queries a FAISS knowledge base; Llama-3 generates grounded remedy text. **The only located published predecessor of KrishokTech's exact loop (vision→diagnosis→grounded advice) — single-crop, no grounding metric, no safety layer, no rejection behavior.**

**Hierarchical two-stage diagnosis.**
- Suwa et al., "Hierarchical Object Detection and Recognition Framework for Practical Plant Disease Diagnosis", arXiv:2407.17906 (2024). Stage-1 YOLOv7 ROI detection, stage-2 EfficientNetV2 classification, on 281k Japanese field images (4 crops, 21 classes). Beats YOLOv7-alone by 5.8–21.5 F1 points on healthy cases; macro-F1 +1.1–7.2 over EfficientNetV2. Closest precedent for the crop-router→disease-classifier hierarchy.

**Survey evidence.**
- "Recent advances in plant disease detection: challenges and opportunities", *Plant Methods*, 10.1186/s13007-025-01450-0 (Oct 2025): ICVT hits 99.94% on PlantVillage but 77.54% on PlantDoc — **a 22.4-point lab-to-field gap**.
- "A comprehensive review on AI-based crop disease detection…", *Discover Applied Sciences*, 10.1007/s42452-026-08684-0 (Apr 2026): >95% on controlled sets, significant degradation under field domain shift; fewer than one-third of public datasets carry lesion-level annotations.

**Calibration, OOD, abstention (medical domain carries the rigor).**
- López, Shamout & Rudner, "An Empirical Analysis of Calibration and Selective Prediction in Multimodal Clinical Condition Classification", arXiv:2603.02719 (CHIL 2026): selective prediction degrades reliability despite strong aggregate metrics, driven by class-dependent miscalibration — models assign high uncertainty to correct, low to incorrect predictions for underrepresented conditions. **Direct warning that naive max-softmax thresholds can invert on rare classes (the 11-class brassica regime).**
- Wundram & Baumgartner, arXiv:2508.02319 (glaucoma fundus deferral; uncertainty methods beat learned deferral under OOD corruption).
- Aperstein et al., arXiv:2509.10348 (entropy- and interval-based rejection with quantile-calibrated thresholds on PadChest/NIH ChestX-ray14/MIMIC-CXR).
- Batra et al., arXiv:2508.07617 (259-clinician study: abstention recovered accuracy but raised missed diagnoses +18%, missed treatments +35%).
- Slobodkin et al., arXiv:2502.18050 (medical abstention benchmarking; RC-AUC/FR-AUC rejection metrics).

**Plant-domain OOD/unknown rejection.**
- Dong et al., "The impact of fine-tuning paradigms on unknown plant disease recognition", *Scientific Reports*, s41598-024-66958-2 (2024): OSR/OOD benchmarks on 5 plant datasets; visual prompt tuning + max-logit reaches AUROC 94.8% at 8-shot; MSP-based detection is threshold-unstable in this domain.
- Dong et al., "Enhancing anomaly detection in plant disease recognition with knowledge ensemble", *Frontiers in Plant Science*, 10.3389/fpls.2025.1623907 (Aug 2025): frozen-generic + fine-tuned-domain score ensemble cuts VLM FPR@TPR95 from 43.88%→7.05% (16-shot).

**Multimodal agricultural benchmarks.**
- AgMMU, arXiv:2504.10568 (2025): 746 MCQ + 746 OEQ from 116k real Cooperative-Extension dialogues; AgBase 57,079 facts; fine-tuning gains up to 11.6% on OEQs.
- AgroBench, Shinoda et al., ICCV 2025 (arXiv:2507.20519): expert-annotated, 203 crops / 682 diseases; open VLMs near-random on weed identification.
- SCOLD, "A Vision-Language Foundation Model for Leaf Disease Identification", arXiv:2505.07019 (May 2025; ESWA DOI 10.1016/j.eswa.2025.130084): 186k image–caption pairs, 97 concepts; beats CLIP-L/BioCLIP/SigLIP2 zero-shot.
- AgriGPT-VL, arXiv:2510.04002 (Oct 2025): 3M-pair corpus, GRPO-aligned VLM, AgriBench-VL-4K.

**Benchmarks & foundation models.**
- PlantCLEF 2025 (LifeCLEF; hal-05319328, CEUR-WS Vol-4038 paper_235, arXiv:2509.17602): weakly-supervised multi-label quadrat identification; 1.4M training images, 2,105 expert test images; winning macro-F1 0.3648 vs 0.2873 (2024); official baseline 0.21708; leaderboard rank shifts = tuning-overfitting.
- RemoteCLIP, arXiv:2306.11029 / IEEE TGRS 62, DOI 10.1109/TGRS.2024.3390838 (background). AgriFM, arXiv:2505.21357. Foundational-models review, *Agriculture* 15(8):847, DOI 10.3390/agriculture15080847 (2025).
- Diabetic-retinopathy deployment lessons (transferable): "Customizing AI-based screening with real-world data", PMC13058676: intention-to-screen sensitivity fell to 52.7% (IDx-DR) vs 79.9% (RetCAD with Youden-tuned referral thresholds); IDx-DR rejected 25.5% of patients on image quality alone. "Autonomous AI in DR Testing — Lessons Learned", PubMed 41140908: real-world gradability 49–75%, sensitivity 87–100%.

## 2. Findings & insights

- **PlantVillage is saturated; 2025 papers sell parameter efficiency, not accuracy** (dual-branch CNN+ViT 99.71% at 4.9M params / 0.62 GFLOPs, PLOS One 10.1371/journal.pone.0321753; EfficientNetV2B0 0.997/0.96 PlantVillage/PlantDoc). Reporting raw accuracy on PlantVillage in 2026 adds no information; reviewers expect cross-domain or field evaluation.
- **The lab-to-field penalty is quantified**: 99.94%→77.54% (22.4 points) for the same model family across PlantVillage→PlantDoc. Field datasets are the credible test surfaces.
- **Zero-shot VLMs are not diagnostic systems**: ≤62% MCQA ceiling, <25% raw open-ended accuracy; supervised YOLO11 remains dominant (arXiv:2512.15977).
- **Rejection works only when calibrated per class**: plant-domain max-logit+VPT AUROC 94.8%; score-ensemble cuts FPR@TPR95 to 0.71% — but 2603.02719 documents naive thresholds degrading on rare classes, and 2508.07617 shows abstention shifts error types (missed diagnoses +18%) even when average accuracy recovers.
- **Deployment reality in DR screening**: quality-based rejection is a first-class operational lever (25.5% of patients rejected by IDx-DR); intention-to-screen sensitivity (52.7–79.9%) far below per-image accuracy; threshold tuning is population-specific.
- **PlantCLEF 2025 persistence**: even with 1.4M images and 38 teams, best sample-F1 is 0.36 — fine-grained diagnosis under domain shift remains unsolved.

## 3. Research gaps

1. **No pipeline-level evaluation of "classification → grounded treatment advice" exists.** Mondal (2505.21544) is the only located vision→RAG-advice system; it reports no grounding metric, no hallucination audit, no safety routing, no rejection state. AgMMU/AgroBench evaluate VLM factuality but not closed-form two-stage pipelines. **KrishokTech's differentiator: verifier-flagged claims (dosages) as an explicit, measured artifact — no existing paper measures this.**
2. **Selective prediction/calibration is unstudied at the system level for fine-grained multi-crop disease classifiers.** Plant-domain OOD work benchmarks algorithms, not deployed thresholds on a 35-class, class-imbalanced, multi-crop hierarchy; medical work (2603.02719) proves class-dependent miscalibration breaks naive rejection on rare classes. **KrishokTech lever: per-class calibrated thresholds over its 35 disease classes with coverage-vs-error tradeoffs (risk-coverage/AURC-style metrics) — precedented in chest X-ray (2509.10348), unclaimed in agriculture.**
3. **Hierarchical crop-router→disease-classifier error propagation is unquantified.** HODRF validates two-stage design but for detection+classification, not router-then-classifier. PlantCLEF shows how much hierarchy + domain shift costs. **KrishokTech lever: router-error and classifier-error decomposition with honest rejection states (low-confidence → 16123 helpline), mirroring DR screening's ungradable-image protocol.**

## 4. Conventions

- **Datasets**: PlantVillage (38-class, saturated) for comparability, but credibility requires PlantDoc, field corpora, or self-collected field images; stratified 5-fold routine; per-class precision/recall/F1 and confusion matrices expected; XAI (Grad-CAM) near-mandatory in applied journals.
- **Architecture reporting**: parameters, FLOPs, latency, quantization/mobile feasibility stated explicitly; Ultralytics YOLO `classify` models are acceptable baselines/backbones (BioData Mining 10.1186/s13040-025-00497-y).
- **Benchmark papers**: grouped error analysis, per-class and per-task breakdowns, expert annotation provenance, leaderboard-overfitting caution.
- **Systems papers**: pipeline diagrams, per-stage metrics, deployment constraints, audit trails; medical-style deployment reporting (intention-to-screen sensitivity, image-rejection rate, threshold calibration on held-out sets, referral-adherence) is the quality bar transferable from DR screening.
- **Safety framing**: abstention/deflection to human escalation with quantified coverage is now a legitimate evaluation dimension (2508.19322 AT-CXR, 2508.02319).

## 5. Positioning recommendations for KrishokTech

- Anchor on supervised classification: cite arXiv:2512.15977 as direct 2026 evidence that off-the-shelf VLMs cannot replace YOLO11-class supervised models, validating the locked Ultralytics `classify` stack.
- Make honest failure a headline: per-class calibrated rejection thresholds + OOD score over the 35 disease classes as coverage-vs-error curves (AURC/risk@80% convention from 2509.10348); pre-empt the 2603.02719 failure mode by evaluating rejection per class, not aggregate.
- Position the RAG+verifier advice loop as the first measured treatment-grounding pipeline from a vision classifier: report grounding/verification rates on the 437-image Bengali set (99.8% info-coverage; Mondal precedent's missing metrics).
- Frame evaluations deployment-style with DR-screening conventions: per-crop accuracy, cross-crop confusion, reject/deflect rate (to 16123), and the 22.4-point lab-to-field gap as the problem statement.
- For the industry/application track: the multi-crop, low-resource, Bengali-language combination is unoccupied in 2025–2026 VLM benchmark literature (AgMMU, AgroBench) — an explicit supervised 6→35 hierarchical classifier vs zero-shot VLM comparison on the team's own corpus, with measured Bengali-advice grounding, is a defensible novel evaluation.