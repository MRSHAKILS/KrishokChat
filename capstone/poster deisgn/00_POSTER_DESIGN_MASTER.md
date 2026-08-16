# KrishokChat — A0 Poster Design Master Outline

**Author role:** Industry Expert + Poster Designer + Researcher + Hackathon Judge
**Target:** Innovation Challenge / Final-Year Capstone, Bangladesh
**Judging weights:** Idea 20 · Impact 20 · Business 20 · Market Readiness 20 · UI 10 · Poster 10
**Format:** A0 portrait, 841 × 1189 mm
**Spec:** Headings 48–60 pt · Body 24–32 pt single-spaced · Graphs & photos ≥ 12 × 18 cm
**Stats file:** `stats/poster_stats.yaml` — single source of truth for every number on the poster.
**2nd-run audit (2026-08-17):** Soil OOF stats independently recomputed from `oof_predictions.csv` (R²=0.3936, RMSE=4.0934 kPa confirmed). Two additional high-value novelties identified and added — see §3 A4 and C1 below.

> **Framing principle (faculty guidance):** this is a competition, not a peer review. The poster shows what we built and what we achieved. Unfinished work is framed as an **ongoing roadmap**, never as a weakness. Four main pillars carry the poster: **(1) KrishokChat — the Bengali agri QA benchmark + fine-tuned model, (2) crop disease detection + its agentic advisory pipeline, (3) soil moisture field dataset + regression model, (4) the safety-first verification architecture.** Every number below cites a source file (see `01_FIGURES_AND_ASSETS_LIST.md` and `stats/poster_stats.yaml`).

---

## 0. The single sentence a judge must take away

> **KrishokChat is a safety-first Bengali agricultural advisory system where a farmer types a question in dialect or uploads a diseased leaf photo, and receives source-cited treatment advice that has passed a four-stage verified agent pipeline — backed by an 85,979-instance provenance-traced benchmark, a 722-image field-collected soil-moisture dataset with a working EfficientNet regression model, and crop-disease classifiers achieving 95–97% top-1 accuracy across five crops — all escalating unsafe queries to the national Krishi Call Center (16123).**

A judge who reads only the title + hero strip + the four pillar headers should grasp the full scope in under 10 seconds.

---

## 1. The four pillars (the organising principle of the whole poster)

| # | Pillar | What it proves | Hero evidence on poster |
|---|---|---|---|
| **1** | **KrishokChat — Bengali Agri QA** | The research foundation: 85,979-instance benchmark, 2,882-node knowledge graph, fine-tuned Gemma-4 4-bit model, hybrid retrieval | R@10 chart, GenF1 0.314 vs 0.165 |
| **2** | **Crop Disease Detection + Agentic Pipeline** | A working multimodal product: photo → crop classifier → per-crop disease model → grounded Bengali treatment, 95–97% accuracy, edge-deployable | AgriVision accuracy table + /detect screenshot |
| **3** | **Soil Moisture — Field Dataset + Model** | Original fieldwork: 722 tensiometer-labeled photos, Pabna District, EfficientNet-B0 regression (R²=0.39, beats baseline by 22%) | pred-vs-actual scatter + dataset stats |
| **4** | **Safety-First Verification Architecture** | The novel contribution: 6-category pre-retrieval safety, structured claim verifier, 16123 escalation, audit log | Hero pipeline diagram + safety taxonomy |

Every section of the poster maps to one of these pillars. Nothing goes on the poster that does not strengthen one of the four.

---

## 2. Layout grid (A0 portrait, 3 columns)

```
┌───────────────────────────────────────────────────────────────┐
│  ROW 0 — TITLE BLOCK (full width, ~130 mm)                     │  54 pt title
│  Title · Authors · Affiliation · Institution logos             │  26 pt authors
├───────────────────────────────────────────────────────────────┤
│  ROW 1 — VALUE-PROPOSITION STRIP + HERO STAT RIBBON (full,~100mm)│  28 pt hook
│  One-line hook · 6 killer-number chips                          │  38 pt numbers
├──────────────────────┬──────────────────────┬─────────────────┤
│  COLUMN A (~250 mm)  │  COLUMN B (~250 mm)  │  COLUMN C (250mm)│
│                      │                      │                 │
│  PILLAR 1: KRISHOKCHAT│  PILLAR 4: SAFETY   │  PILLAR 2: DISEASE│
│  1. Problem + impact  │  ARCHITECTURE (hero) │  DETECTION        │
│  2. Benchmark + KG    │  4-stage pipeline    │  AgriVision table │
 │  3. Retrieval eval   │  DIAGRAM (tall,       │  + /detect shot   │
│  4. Model results     │   spans col B)        │                 │
│                      │  Safety taxonomy +    │  PILLAR 3: SOIL   │
│  PILLAR 4 (cont.)    │  16123 branch         │  Dataset + model  │
│  Novelty + 4 contribs│  Structured verifier  │  Scatter plot     │
│                      │  schema                │  + stats          │
│                      │                      │                 │
│                      │  PILLAR 2+3 mini-     │  PRODUCT + IMPACT  │
│                      │  flows (vision+soil   │  3 screenshots    │
│                      │  into pipeline)       │  + impact points  │
│                      │                      │                 │
│                      │                      │  BUSINESS + ROADMAP│
│                      │                      │  + QR codes       │
├──────────────────────┴──────────────────────┴─────────────────┤
│  ROW 3 — FOOTER (full width, ~35 mm): refs · contact · license  │  18 pt
└───────────────────────────────────────────────────────────────┘
```

**Reading-order logic:** Row 0–1 lands the thesis in 8 seconds. Column A proves the research foundation (Pillar 1). Column B is the hero — the safety architecture (Pillar 4) as the largest diagram, with the structured verifier schema showing the SOTA approach. Column C carries the multimodal product (Pillar 2 disease detection, Pillar 3 soil), then product screenshots, impact, business, and roadmap. A judge who reads only Columns A+B gets the research + architecture; a judge who reads only Column C sees the working product + field data.

---

## 3. Section-by-section content, copy, and sizing

---

### ROW 0 — TITLE BLOCK (full width, ~130 mm)

- **Title** — 54 pt bold:
  > **KrishokChat: A Safety-First Agentic Agricultural Advisory System for Bangladeshi Smallholder Farmers**

- **Subtitle** — 30 pt:
  > Field-collected crop-disease and soil-moisture datasets, a four-stage verified Bengali AI pipeline, and an 85,979-instance provenance-traced benchmark

- **Authors** — 24 pt: `[Author names] · [Advisor]`
- **Affiliation** — 22 pt: `[Department, University, Bangladesh]`
- **Logos** — institution + funding, top-right, ~30 mm.

**Scores:** Poster 10, Idea 20.

---

### ROW 1 — VALUE-PROPOSITION STRIP + HERO STAT RIBBON (full width, ~100 mm)

- **Hook line** — 28 pt bold (left):
  > The first Bengali agricultural assistant that **classifies safety before retrieval**, **verifies every chemical claim against government sources**, **diagnoses crop diseases from photos at 95–97% accuracy**, and **estimates soil moisture from field images** — built on a published 85,979-instance benchmark and escalating unsafe queries to the national Krishi Call Center (16123).

- **Hero stat ribbon** — 6 chips, numbers 40 pt bold, labels 20 pt:

| Chip | Number | Label |
|---|---|---|
| 1 | **85,979** | benchmark instances · 4 tracks |
| 2 | **95–97%** | crop disease top-1 accuracy |
| 3 | **R²=0.39** | soil moisture regression (EffNet-B0) |
| 4 | **4-stage** | safety-verified agent pipeline |
| 5 | **16123** | Krishi Call Center escalation |
| 6 | **2 papers** | EACL 2026 · SIGIR-AP 2026 (under review) |

**Scores:** Idea 20, Poster 10, Market 20 (scale signal).

---

### COLUMN A — PILLAR 1: KRISHOKCHAT (the research foundation)

#### A1. The Problem + Impact (~30 pt heading, ~130 mm)

**Heading:** **The Problem**

> Rural Bangladesh has ~47 million farming households with limited access to reliable Bengali-language advisory. The national Krishi Call Center (16123) received 92,094 calls in FY 2025–26 — a fraction of the need.
>
> LLM-based advisory tools can hallucinate pesticide dosages. In our benchmark, six architecturally different LLMs keep a **4.05–7.00% chemical-hallucination floor even under oracle evidence**. A wrong dose can burn a crop, poison a farmer, or contaminate soil and water.
>
> KrishokChat closes this gap with a safety-first pipeline that stops unsafe queries before generation, verifies every dosage against government sources, and grounds answers in a 2,882-node knowledge graph from 284 government publications.

**Figure:** small field photo (Pabna / paddy), ≥ 12 × 18 cm. Caption: "Pabna District field campaign, May 2026."

**Scores:** Impact 20, Idea 20.

#### A2. The Benchmark + Knowledge Graph (~30 pt heading, ~140 mm)

**Heading:** **85,979-Instance Provenance-Traced Benchmark**

**Body (24 pt) + small composition bar:**
> Four tracks, CC-BY-4.0, released on HuggingFace (RaiyanKhaan/krishokChat):
> - **General QA:** 28,993 instances
> - **Treatment QA:** 11,224 (7,437 chemical-bearing, 66.3% — provenance-traced)
> - **Table QA:** 25,650 (6 dialects × 4,275, 3 complexity levels)
> - **Safety:** 20,112 (12-category taxonomy + 6 re-query slots)
>
> **Knowledge graph:** 2,882 nodes, 19,768 entities (6.9/node), 17,501 factual triples, 1,022 image-linked nodes (35.5%). Sources: 284 government publications, 13 institutions (BARC, BARI, DAE, CABI, …). Inter-annotator κ = 0.72 (farmer+safety), 0.78 (KG-grounded).
>
> **Farmer benchmark:** 1,000 real queries — 300 via structured field interviews in Rajshahi & Natore, 483 from farmer Facebook groups, 217 from krishibangla.com.

**Scores:** Idea 20, Market 20 (published assets).

#### A3. Retrieval Evaluation (~28 pt heading, ~120 mm)

**Heading:** **Hybrid Retrieval Wins on Bengali**

**Figure: R@10 bar chart (≥ 12 × 18 cm)** — 5 architectures over 900 answerable queries:
- Hybrid RRF: **0.539**
- BM25: **0.506** (95% CI [0.474, 0.538])
- ColBERT: 0.487
- Dense Gemini-001: 0.464
- BGE-M3: 0.408

**Caption (22 pt):** "BM25 outperforms dense retrieval by 9% (p<0.001, Wilcoxon) on Bengali — dense collapses on colloquial farmer queries (R@10 = 0.093) but is near-perfect on formal safety queries (0.970). Hybrid RRF wins overall."

**Scores:** Idea 20, Poster 10 (real chart).

#### A4. Fine-Tuned Model Results (~28 pt heading, ~120 mm)

**Heading:** **KrishokChat-4B: Fine-Tuned Gemma-4 4-bit**

**Small table (24 pt):** Closed-book General QA Token F1:
| Model | GenF1 | Treatment Correct% |
|---|---|---|
| **KrishokChat-4B** (Gemma-4-E4B 4-bit, LoRA r=32, 1 epoch) | **0.314** | 35.55% |
| LLaMA-3.1-8B (best zero-shot) | 0.165 | 12.43% |
| Gemini-2.5-Flash-Lite | 0.104 | 43.64% |
| Gemma-4-26B | 0.087 | 38.73% |

**Body (22 pt):**
> KrishokChat-4B achieves **1.9× the General F1** of the best zero-shot baseline (p ≈ 6.7×10⁻⁵). Trained on a single NVIDIA L4 (24 GB), bfloat16, effective batch 16, max seq 4,096.
>
> **Safety compliance:** KrishokChat-4B incorrectly complied with a harmful safety-test request in only **0.31% of cases (1/323)** — the lowest across all tested models. This directly supports the safety-first framing.
>
> **The hallucination floor (key motivator for Pillar 4):** 4.05–7.00% chemical hallucination persists across all 6 LLMs even under oracle evidence. This is NOT a weakness — it is the proof that a structured verifier is necessary and our contribution is non-redundant.

**Scores:** Idea 20, Market 20.

#### A5. Novelty + Four Contributions (~30 pt heading, ~130 mm)

**Heading:** **What We Built — Four Contributions**

**Mini comparison table (24 pt):**
| Capability | Generic chatbots | KrishokBondhu | **KrishokChat** |
|---|---|---|---|
| Safety classify before retrieval | ✗ | ✗ | **✓** |
| Structured dosage verifier | ✗ | ✗ | **✓** |
| Audit log + metrics panel | ✗ | ✗ | **✓** |
| Bengali + 6 dialects | partial | voice only | **text + dialect** |
| Published 85,979 benchmark | ✗ | pilot only | **✓** |
| Photo → grounded treatment (95–97%) | partial | ✗ | **✓** |
| Field soil-moisture dataset + model | ✗ | ✗ | **✓** |

**Four contributions (28 pt sub-head + 24 pt bullets):**
> 1. **A four-stage safety-verified agent pipeline** — Safety/Router → Retrieval → Generation → Verifier — where unsafe categories stop the pipeline before any retrieval.
> 2. **A structured claim verifier** with a 14-field atomic claim schema and 6 relation types, checking each chemical amount/unit/denominator/PHI against retrieved evidence (the SOTA approach — see Pillar 4).
> 3. **Two original field-collected Bengali datasets** — 722 tensiometer-labeled soil-moisture images (Pabna) + 1,000-query farmer benchmark (300 field interviews, Rajshahi & Natore).
> 4. **An 85,979-instance provenance-traced benchmark** across 4 tracks, released CC-BY-4.0, enabling third-party validation.

**Scores:** Idea 20 (core of the idea score), Poster 10.

---

### COLUMN B — PILLAR 4: SAFETY ARCHITECTURE (the hero column)

#### B1. Four-Stage Agentic Pipeline — HERO DIAGRAM (~30 pt heading, figure ~290 mm)

**Heading:** **The System: Four-Stage Safety-Verified Pipeline**

**Figure (the centrepiece, ~250 × 290 mm — well above 12 × 18 cm):**

```
   কৃষকের প্রশ্ন / পাতার ছবি
   Farmer query / leaf photo
            │
            ▼
  ┌─────────────────────────┐
  │ 1. SAFETY / ROUTER       │  6 categories:
  │    classify BEFORE       │  safe_agri · banned_chemical
  │    retrieval             │  self_harm · off_topic
  └────────────┬────────────┘  prompt_injection · low_conf
   unsafe?      │ safe
       │        │
       ▼        ▼
  [16123 +     ┌─────────────────────────┐
   999 +       │ 2. RETRIEVAL            │  BM25 + FAISS dense
   medical     │  hybrid over 2,882 KG   │  RRF fusion, top-5
   help]       │  nodes / 284 govt pubs  │  Bengali + dialect
  (stop)       └────────────┬────────────┘
                            ▼
               ┌─────────────────────────┐
               │ 3. GENERATION           │  Gemma-4-E4B 4-bit
               │  grounded, streamed     │  LoRA r=32, Bengali
               └────────────┬────────────┘
                            ▼
               ┌─────────────────────────┐
               │ 4. VERIFIER              │  structured claim
               │  14-field schema, 6      │  entailment vs sources
               │  relation types          │  annotate-and-drop
               └────────────┬────────────┘
                            ▼
            উত্তর + উৎস + নিরাপত্তা ফ্ল্যাগ
            Answer + sources + safety flags
                            │
                            ▼
               ┌─────────────────────────┐
               │ AUDIT LOG (local JSONL)  │  → /analytics panel
               └─────────────────────────┘
```

**Caption (24 pt):** "Every query is classified before retrieval. Terminal safety categories return a canned redirect to 16123 and never reach the model. The structured verifier checks each chemical claim's 14 fields against retrieved passages. Every decision is written to a local audit log powering the /analytics panel."

**Reuse:** `capstone/figure.png` exists — redraw larger and cleaner for A0, add the audit-log box, the 16123/999 branch, and the structured-verifier label.

**Scores:** Idea 20, Poster 10, UI 10, Market 20.

#### B2. Safety Taxonomy + 16123 Branch (~28 pt heading, ~100 mm)

**Heading:** **Six-Way Safety Classification**

**Body (24 pt):**
> A deterministic rule pre-filter runs first; an LLM structured-output call classifies the rest. Unknown categories and classifier outages **fail closed** to `low_confidence` — never permission to retrieve or generate.

**Six chips (24 pt, 2 × 3 grid):**
- `safe_agri` → proceed
- `banned_or_restricted_chemical` → 16123 redirect
- `self_harm_or_poisoning_risk` → 999 + 16123 + medical help
- `off_topic` → scope message
- `prompt_injection` → silent refusal
- `low_confidence` → 16123 referral

**Scores:** Idea 20, Impact 20.

#### B3. Structured Claim Verifier — The SOTA Approach (~28 pt heading, ~110 mm)

**Heading:** **Structured Dosage Verification (SOTA)**

**Body (24 pt):**
> The verifier goes beyond lexical matching. Each generated answer is split into **atomic claims**, each with a **14-field schema**: crop, disease, action, chemical, formulation, amount, unit, denominator, interval, PHI/safety, polarity, applicability, uncertainty, source_id.
>
> Every claim is matched against retrieved evidence through one of **6 relation types**: `supported` · `contradicted` · `partially_supported` · `unsupported` · `ambiguous` · `not_applicable`.
>
> **Safety-critical claims** (any error that could change chemical identity, dose, exposure, timing, or PHI) require all fields present and supported. Missing evidence → **abstain** (annotate-and-drop). The verifier is **deterministic-first** — a parser/normalizer + structured relation matcher + fail-closed safety policy — with optional NLI as a bounded resolver, never as gold.

**Small schema box (22 pt, optional visual):** show the 14 fields as a compact list or a small radial diagram.

**Scores:** Idea 20 (this is the research novelty), Market 20.

---

### COLUMN C — PILLARS 2 + 3, PRODUCT, IMPACT, BUSINESS

#### C1. Pillar 2: Crop Disease Detection (~30 pt heading, ~200 mm)

**Heading:** **Crop Disease Detection — 95–97% Accuracy**

**Body (24 pt):**
> Five crop families, 37 disease classes (live system), ~22,544 training images filtered to Bangladesh-relevant diseases from Mendeley + Kaggle sources. Models trained on Kaggle (Tesla T4/P100), exported to **ONNX FP16 + TFLite INT8/FP16** for **<30 ms inference on Android** edge devices.

**AgriVision accuracy table (24 pt — the real results):**
| Crop | Classes | Test Top-1 | Weighted F1 | Model | Edge |
|---|---|---|---|---|---|
| **Brassica** | 11 | **97.29%** | 0.965 | YOLO26s + HybridNet | ONNX 21.8 MB |
| **Rice** | 8 | **96.49%** | 0.965 | YOLO26n (nano) | ONNX 6.2 MB, 1.1 ms/img |
| **Corn** | 4 | **97.23%** | 0.972 | YOLO26s | ONNX 21.8 MB |
| **Potato** | 3 | **95.04%** | 0.951 | YOLO26s | TFLite INT8 1.6 MB |
| **Wheat** | 11 | **88%** (live sweep) | — | YOLO26s (upgraded) | ONNX |

**Figure:** one disease-classification screenshot or a sample leaf-photo grid (≥ 12 × 18 cm).

**One-line product note (24 pt):**
> In KrishokChat, the /detect page routes a photo: crop classifier → per-crop disease model → Bengali treatment advice from the knowledge map → same 4-stage verifier. Live-verified: wheat 44/50 (88%) correct diagnosis, **50/50 (100%) Bengali treatment returned**. 437-image library: 436/437 (99.8%) Bengali treatment info. These are production pipeline results, not training metrics.

**⚑ 2nd-run addition — missed high-value novelty:** The **100% Bengali treatment coverage** (wheat 50/50, library 436/437 = 99.8%) is a product-readiness stat that no competing system has. It shows the knowledge map → advisory chain works end-to-end in Bengali. Add this as a bullet to the product note.

**Scores:** Idea 20, Market 20, Impact 20.

#### C2. Pillar 3: Soil Moisture — Field Dataset + Model (~30 pt heading, ~170 mm)

**Heading:** **Soil Moisture — Field-Collected Dataset + Regression Model**

**Body (24 pt):**
> **Original fieldwork:** 722 tensiometer-labeled RGB soil photos, 0.0–21.5 kPa, 6 USDA soil types, 14 crops, 8 growth stages. Pabna District, 3-day campaign (May 29–31, 2026). Series-stratified split, leakage-checked.

**Figure: pred-vs-actual scatter plot (≥ 12 × 18 cm)** — use `backend/ml_assets/soil/pred_vs_actual.png`.

**Soil model results table (24 pt — independently verified from oof_predictions.csv, 2026-08-17):**
| Metric | EffNet-B0 (5-fold OOF, N=693) | Mean baseline |
|---|---|---|
| **RMSE** | **4.09 kPa** | 5.26 kPa |
| **MAE** | **3.19 kPa** | — |
| **R²** | **0.39** | 0.00 |
| **Improvement** | **22% RMSE reduction** | — |

**Body (22 pt):**
> EfficientNet-B0 (4.17 M params), Optuna-tuned (15 trials), SmoothL1Loss, 15 epochs, 5-fold cross-validation. Per-fold R² ranges 0.22–0.52; best fold R²=0.52. Per-soil-type MAE: Atel (Clay) 2.98 kPa (best) → Bele (Sandy) 3.92 kPa. Per-crop MAE: Lechee 1.89 kPa (best) → Betel_Nut 4.37 kPa.
>
> In KrishokChat, the /soil page showcases the dataset and the regression model powers an irrigation-advisory lane.
>
> **⚑ 2nd-run addition — show in table or caption:** 693 usable samples after removing 29 duplicates. 46 series (plot locations), series-stratified splits prevent leakage. These procedural rigour details signal original fieldwork quality and can defend against a judge asking "how do you know these results generalise?".

**Scores:** Idea 20 (original fieldwork + model), Impact 20, Market 20.

#### C3. The Working Product (~30 pt heading, ~200 mm)

**Heading:** **The Working Application**

**Three screenshots (≥ 12 × 18 cm each), 22 pt captions:**
1. **`/detect` — Photo diagnosis + agent trace.** Rice leaf → pipeline rail animates → Leaf Blast diagnosis + grounded treatment. *Caption: "Photo → crop → disease → grounded Bengali treatment."*
2. **`/chat` — Safety contrast.** Banned-chemical query → immediate 16123 redirect; trace shows retrieval/generation/verifier **skipped**. *Caption: "Unsafe queries stop before any model generation."*
3. **`/analytics` — Live audit dashboard.** Safe-vs-blocked donut + category bars + CSV export. *Caption: "Every decision locally audited."*

**Product note (24 pt):**
> Bengali-first UI ("কৃষি পত্রক" field-notebook design system), Motion-animated agent trace on every query, voice input (bn-BD), offline-capable demo cache, Ctrl+K command palette, sunlight high-contrast mode.

**Scores:** UI 10, Market 20, Poster 10.

#### C4. Impact on Society & Environment (~30 pt heading, ~100 mm)

**Heading:** **Impact**

> **Health & safety:** refusing unsafe agrochemical queries + verifying dosages against government sources reduces the risk of pesticide misuse, accidental poisoning, and self-harm — redirecting at-risk users to 16123 and 999.
>
> **Environment:** source-grounded dosage advice lowers over-application of pesticide and fertilizer, reducing soil and water contamination.
>
> **Access:** ~47 million farming households; a laptop-deployable, offline-capable system reaches the connectivity gap cloud-only tools cannot. Edge-deployable disease models (<30 ms on Android) extend reach to smartphones.

**Scores:** Impact 20.

#### C5. Business Model & Market Readiness (~30 pt heading, ~100 mm)

**Heading:** **Business Model & Market Readiness**

> **Monetization lanes:**
> 1. **Freemium + B2B** — free advisory + diagnosis for farmers; paid audit/analytics dashboard for agro-dealers, SAAOs, extension officers. *Evidence: PxD 7.8M users; ACI IDSS/Fosholi €3.5M 2025 target.*
> 2. **Government partnership (B2G)** — AI front-end to the 16123 Krishi Call Center (triage + escalation). The audit engine is the least-commoditized trust asset.
> 3. **Dataset + API licensing** — 85,979 benchmark + 722-image soil dataset (CC-BY-4.0) enable third-party validation and an advisory API for agri-fintech.
>
> **Market readiness:** working end-to-end prototype (chat + vision + soil + audit + research panel), two papers under peer review, datasets published, edge-deployable models. Business model framework under development for the capstone.

**Scores:** Business 20, Market 20.

#### C6. Roadmap / Ongoing Work + QR Codes (~28 pt heading, ~80 mm)

**Heading:** **Roadmap & Access**

> **Ongoing:** voice-output (TTS) for low-literacy users; extended dialect coverage; B2B pilot with an extension office; soil-model refinement for higher-accuracy irrigation advisories.

**Three QR codes (~40 mm each, 20 pt labels):**
- **Dataset** → HuggingFace `RaiyanKhaan/krishokChat`
- **Code / Demo** → GitHub repo
- **Papers** → KrishokChat (EACL 2026) + AgriTrust (SIGIR-AP 2026), under review

**Scores:** Market 20 (roadmap signals momentum), Poster 10.

---

### ROW 3 — FOOTER (full width, ~35 mm, 18 pt)

> References: KrishokChat (EACL 2026, under review) · AgriTrust (SIGIR-AP 2026, under review) · AgriVision BD (Project Report 3, 2026). Datasets CC-BY-4.0. Built at [University], Bangladesh. Contact: [email]. · Acknowledgements: Krishi Call Center 16123; 13 source institutions.

---

## 4. Reading-order rationale (competition timing)

Judges spend 30–90 seconds per poster. The reading order is engineered for that:

1. **0–8 s (Row 0–1):** Title + hook + 6 stat chips → they know the scope and scale.
2. **8–25 s (Column A):** Problem + benchmark + retrieval + model + novelty → the research foundation (Pillar 1, Idea 20).
3. **25–50 s (Column B):** Hero pipeline diagram + safety taxonomy + structured verifier → the architecture and the SOTA contribution (Pillar 4, Idea 20 + Poster 10).
4. **50–80 s (Column C top):** Disease detection table (95–97%) + soil scatter (R²=0.39) + product screenshots → the working product from research (Pillars 2+3, Market 20 + UI 10).
5. **80–100 s (Column C bottom):** Impact + business + roadmap + QR → society + sustainability + verifiability (Impact 20 + Business 20 + Market 20).

---

## 5. What NOT to put on the poster (space-wasters & AI-flag triggers)

- **Generic process descriptions** — "we used machine learning / NLP to…" → replace with named methods (BM25Okapi k1=2.2; EfficientNet-B0; YOLO26s-cls).
- **Empty intensifiers** — groundbreaking, revolutionary, comprehensive, robust, cutting-edge, state-of-the-art, seamless, leverage, empower, delve, realm, tapestry, navigate the landscape, it's worth noting, plays a crucial role. (Full list in `02_ANTI_AI_FLAG_AND_PROOF_CHECKLIST.md`.)
- **Buzzword stacks** — "AI-powered, cloud-native, scalable, end-to-end solution" → strip to the one differentiator.
- **Long methodology prose** — the pipeline diagram replaces 500 words.
- **The full tech-stack table** — keep the one-liner. A 15-row stack table is space with no judging value.
- **The old negative-R² soil model table** — we now have positive R²=0.39 results. Show those.
- **Decorative emoji** — none.
- **"In conclusion / To summarize"** — posters do not need essay transitions.
- **Symmetric empty bullet triples** ("Analyzing…, Optimizing…, Enhancing…") — if a bullet has no number or named system, cut it.
- **The deprecated arXiv v1 (2606.29243)** — do not cite. Use the two local papers + the AgriVision report.
- **Weakness displays** — frame unfinished work as "ongoing" / "roadmap," never as "limitation" or "not yet working." This is a competition.

---

## 6. Colour, type, and visual rules (carry the product's identity onto the poster)

The product has a deliberate design system ("কৃষি পত্রক" / Field Notebook, `frontend/src/app/globals.css`). **The poster must look like the product.**

- **Palette:** paper `#faf6ef` · paper-2 `#f2ebdc` · bone `#e7dfd0` · ink `#1a1611` · leaf `#2f5d3a` (headings, arrows, "verified") · ochre `#c8893c` (stat ribbon, active stage) · clay `#a8542b` (16123 branch, "flagged").
- **Type:** Tiro Bangla / Noto Serif Bengali (title, headings); Noto Sans Bengali + Inter/Source Sans (body); tabular numerics for all stats/tables.
- **Visual language:** flow arrows in leaf green; unsafe branch in clay; audit-log box in bone with ochre edge; rounded-box + hairline-border cards like the product.
- **Contrast:** body text meets WCAG AA. No pale grey on white.

---

## 7. Figure-size compliance check

| Figure | Planned size (mm) | Compliant (≥12×18 cm)? |
|---|---|---|
| Hero pipeline diagram (B1) | ~250 × 290 | ✓ |
| R@10 bar chart (A3) | ~130 × 90 | ✓ |
| Field photo, Pabna (A1) | ~130 × 90 | ✓ |
| AgriVision accuracy table (C1) | ~240 × 100 | ✓ |
| Soil pred-vs-actual scatter (C2) | ~130 × 100 | ✓ |
| Disease leaf sample (C1) | ~130 × 90 | ✓ |
| Product screenshot triptych (C3) | 3 × (~140 × 200) | ✓ each |
| Comparison table (A5) | ~240 × 90 | ✓ |
| QR codes (C6) | 3 × ~40 × 40 | n/a |

All graphs and photos meet the 12 × 18 cm floor.

---

## 8. Build sequence (what to do, in order)

1. **Confirm numbers** against `01_FIGURES_AND_ASSETS_LIST.md`.
2. **Produce the hero pipeline diagram** first (B1) — redraw `capstone/figure.png` larger, add the audit-log box, the 16123/999 branch, and the structured-verifier label.
3. **Make the soil scatter plot** (C2) — use `backend/ml_assets/soil/pred_vs_actual.png` directly, or regenerate a cleaner version from `oof_predictions.csv`.
4. **Make the R@10 bar chart** (A3) from the AgriTrust numbers.
5. **Build the AgriVision accuracy table** (C1) from the PDF numbers.
6. **Capture the three product screenshots** (C3): /detect, /chat banned query, /analytics.
7. **Write final copy** from the blocks in §3, then run `02_ANTI_AI_FLAG_AND_PROOF_CHECKLIST.md`.
8. **Lay out** in Figma / Illustrator / Inkscape on the 3-column A0 grid. Place the hero diagram first.
9. **Print proof at A3** (50% scale), read from 2 m. Fix hierarchy. Print A0 on matte paper.

---

## 9. One-page TL;DR

> Title + hook + 6 stat chips across the top (85,979 / 95–97% / R²=0.39 / 4-stage / 16123 / 2 papers). Column A: Pillar 1 (KrishokChat) — problem, benchmark, retrieval chart, model table, novelty + 4 contributions. Column B: Pillar 4 (Safety) — the big four-stage pipeline diagram with the 16123 stop-branch and audit log, the 6 safety categories, the structured 14-field claim verifier (SOTA). Column C: Pillars 2+3 (Disease + Soil) — AgriVision 95–97% accuracy table + soil scatter plot (R²=0.39) + three product screenshots + impact + business + roadmap + QR codes. Warm field-notebook palette. No buzzwords, no emoji, every number sourced, unfinished work framed as a roadmap. A judge gets the thesis in 8 seconds and the full scope in 90.