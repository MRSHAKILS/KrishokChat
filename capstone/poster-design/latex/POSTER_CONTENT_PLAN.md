# KrishokChat Poster — Content & Structure Plan (MASTER)

**Status: APPROVED PLAN → implement block-by-block from this file.**
Format: A0 landscape (118.9 × 84.1 cm), 5 columns, XeLaTeX, gemini theme + krishok colors.
Header + stat ribbon exist in `krishokchat-poster.tex`; all body blocks get rebuilt per this plan.

Sources of truth: `poster_stats.yaml` (numbers), `contributions_papers.md` (research
narrative), `BUSINESS_MODEL_VERDICT.md` (economics), app codebase (deployment facts).

---

## 0. THE NARRATIVE (one sentence per column)

The poster reads left → right as one program:

> **Col 1 — WHY:** the problem, the idea (trust stack), impact, novelty.
> **Col 2 — WHAT WE BUILT (research):** three data assets in one table + real fieldwork.
> **Col 3 — PROOF:** model beats baselines, retrieval wins, disease on-device.
> **Col 4 — HOW IT WORKS (application):** measured failures → design decisions → the 4-stage architecture.
> **Col 5 — SO WHAT:** product, market readiness, business model, links.

The intellectual spine (from `contributions_papers.md` §6): **every architectural choice is
justified by a measured failure mode.** That is what separates us from "agriculture chatbot #20".

---

## 1. CRITICAL FIXES to the current skeleton

1. **FOOTER REFERENCES — MUST FIX FIRST.** Current footer cites `arXiv:2606.29243`
   (DEPRECATED, banned by project policy) and `arXiv:2608.14886` (unverified/invented —
   papers are *under review*, no arXiv IDs exist). Replace with:
   - `[1] KrishokChat: A Provenance-Traceable Multi-Task Bengali Agricultural Benchmark with Safety-Critical Chemical Advisory — EACL 2026, under review`
   - `[2] AgriTrust — SIGIR-AP 2026, under review`
   - `[3] AgriVision BD — edge crop-disease classification report, 2026`
2. **Ribbon chips** get replaced (see §3) — current chips duplicate body numbers that now have assigned homes.
3. All body blocks below REPLACE the current template blocks entirely.
4. Node count stays **2,882** (AgriTrust value) everywhere. Never 2,120/2.1k.
5. Soil = **dataset contribution only.** No soil model results (no R², no RMSE, no 22%) anywhere on the poster.
6. Disease = **classification top-1.** Never "detection", mAP, IoU, or bounding boxes.

---

## 2. RUBRIC → BLOCK COVERAGE MAP

| Criterion (pts) | Where it is earned |
|---|---|
| **Idea / novelty (20)** | Col 1: Problem + Idea (trust stack) + Novelty table · Col 4: Findings→Design table |
| **Society & environment (20)** | Col 1: Impact block (health / environment / access) |
| **Business / economics (20)** | Col 5: Free-vs-Premium diagram + 3 revenue lanes · Col 5: scaling-path economics |
| **Market readiness (20)** | Col 5: What-ships-today checklist + connectivity stats + scaling path · Col 3: on-device results |
| **UI / outlook (10)** | Col 5: Product block — screenshot triptych + Krishi Patrak features |
| **Poster itself (10)** | Whole layout: low density, clear zones, consistent palette, ribbon anchors |

Every criterion has at least one dedicated, explicitly-titled block. Judges can score by
skimming block titles alone.

---

## 3. STAT RIBBON (row 1, 6 chips — the glance layer)

Each chip anchors one criterion; these numbers are previewed here and proven in one body
block each (see ledger, §8):

| # | Number | Label | Anchors |
|---|---|---|---|
| 1 | **85,979** | benchmark instances · 4 tracks | scale/idea |
| 2 | **1.9×** | Bengali QA over best zero-shot | results |
| 3 | **95–97%** | on-device crop diagnosis | edge/market |
| 4 | **<30 ms** | offline Android inference | market readiness |
| 5 | **2 paisa** | cost per AI answer | economics |
| 6 | **16123** | human escalation, always free | trust/impact |

---

## 4. FINAL COPY — BLOCK BY BLOCK

### COLUMN 1 — THE CHALLENGE (why this work exists)

**Block 1.1 — "The Problem"** (~80 mm)
> Bangladesh's ~47 million farming households have no reliable advisory in their own
> language. Undetected crop disease costs 20–40% of yield. A wrong pesticide dose can
> poison a family and contaminate the water supply — and a generic chatbot, asked for a
> dosage, will always answer, right or wrong.

**Block 1.2 — "The Idea: an Evidence-Grounded Trust Stack"** (~75 mm)
> Not a chatbot with an agriculture prompt. A layered trust stack, built on our own
> research: official publications → machine-readable knowledge graph → provenance-verified
> retrieval → a safety gate **before** the model ever runs → dosage verification → an
> answer with citations, or human escalation.
>
> Every layer exists because our measurements showed it must (→ column 4).

**Block 1.3 — "Impact: Safety, Environment, Access"** (~115 mm, three bold-led rows)
> **Health.** Unsafe agrochemical queries are refused and escalated — to the 16123 Krishi
> Call Center and 999 — in every tier of the product. Safety is never paywalled.
>
> **Environment.** Source-verified dosing cuts over-application of pesticide and
> fertiliser. Independent Bangladesh sensor-irrigation trials report up to 63% water and
> 50% urea savings — the direction our soil-vision lane targets.
>
> **Access.** Runs in Bengali — standard and dialect — with voice input, offline on the
> mid-range Android phones farmers already own.

**Block 1.4 — "What Exists vs What We Added"** (~135 mm, novelty table — keep current rows)
| Capability | Generic chatbots | KrishokBondhu | KrishokChat |
|---|:---:|:---:|:---:|
| Safety check before retrieval | – | – | ● |
| 14-field dosage verifier | – | – | ● |
| Audit log + analytics panel | – | – | ● |
| Bengali + 6 dialects (text) | ○ | voice only | ● |
| Published 85,979 benchmark | – | pilot only | ● |
| Photo → grounded treatment | ○ | – | ● |
| Field soil dataset | – | – | ● |

*(85,979 here is the table's identity, sanctioned by ledger rule — one glance + one table.)*

**Block 1.5 — "Ongoing & Next"** (~60 mm, roadmap framing — never "limitations")
> Voice output for low-literacy users · extended dialect coverage · soil-vision refinement
> toward irrigation advisories · district-level pilot with an extension office.

---

### COLUMN 2 — RESEARCH FOUNDATION (what we built scientifically)

**Block 2.1 — "Three Research Assets, One Foundation"** (~175 mm) — THE merged dataset table:

| Asset | Scale | Ground truth & provenance |
|---|---|---|
| **Benchmark** (4 tracks) | 85,979 instances | General QA 28,993 · Treatment 11,224 (66.3% chemical-bearing) · Table 25,650 · Safety 20,112 — every instance citation-traced |
| **Knowledge graph** | 2,882 nodes · 17,501 triples | 19,768 entities extracted from 284 publications · 13 institutions (BARC, BARI, BRRI, DAE…) |
| **Farmer-language benchmark** | 1,000 queries | 300 face-to-face interviews (Rajshahi & Natore) + farmer groups · 6 dialects |
| **Soil-moisture dataset** | 722 field RGB images | paired tensiometer readings 0–21.5 kPa · 6 USDA textures · 14 crops · 46 leakage-checked series · Pabna, May 2026 |

Caption: *All released CC-BY-4.0 on Hugging Face.*

**Block 2.2 — Grounded-data diagram slot** (~95 mm)
Existing `figures/D3_grounded_data.png` (2.31:1 → ~200×88 mm at column width).
Caption: *From official publications to provenance-traced retrieval nodes.*

**Block 2.3 — "Built From the Field, Not the Web"** (~130 mm)
- Two real photos side by side (~90 mm): `researcher_interviewing_farmer.png` + one soil
  photo from the dataset (user will supply tensiometer field photo later if preferred).
- Three bullets:
  > **Page-level provenance** — every answer traceable to a publication and page.
  > **Physical ground truth** — tensiometer kPa readings, not annotator opinion.
  > **Series-stratified splits** — no near-duplicate leakage between train and test.

---

### COLUMN 3 — MEASURED RESULTS (the proof)

**Block 3.1 — "Our On-Device Model Beats Far Larger Ones"** (~155 mm) — native pgfplots bar chart:
- Horizontal bars, token-F1, Bengali general QA:
  KrishokChat-4B (ours, 4-bit) **0.314** (leaf green) · LLaMA-3.1-8B 0.165 · Gemini-2.5-Flash-Lite 0.104 · Gemma-4-26B 0.087 (grey).
- Callout: **1.9× the best zero-shot baseline (p ≈ 6.7e-5)**
- Sub-line: *LoRA fine-tune of Gemma-4-E4B; 4-bit quantised — deployable on-device.*

**Block 3.2 — "Retrieval: Hybrid Beats Every Single Method"** (~105 mm) — mini bar chart:
- Recall@10, 900 answerable farmer queries: Hybrid RRF (ours) **0.539** · BM25 0.506 ·
  ColBERT 0.487 · Dense 0.464 · BGE-M3 0.408.
- Sub-line: *+9% over dense retrieval (p < 0.001, Wilcoxon).*

**Block 3.3 — "Crop Disease, On-Device"** (~135 mm) — table with solobars:
| Crop | Top-1 | |
|---|---|---|
| Brassica (11 cls) | 97.29% | ▮▮▮▮▮ |
| Corn (4 cls) | 97.23% | ▮▮▮▮▮ |
| Rice (8 cls) | 96.49% | ▮▮▮▮ |
| Potato (3 cls) | 95.04% | ▮▮▮▮ |
| Wheat (live sweep) | 88.00% | ▮▮▮▮ |

Badge row: **436/437** grounded Bengali treatment returned (99.8%) · **1.6–21.8 MB** models · **<30 ms** on Android.

**Block 3.4 — "Safety Behaviour"** (~55 mm, mini block)
> 1 of 323 unsafe test queries leaked through — **0.31% non-compliance**. Fail-closed by
> design: missing evidence means abstain.

Footnote under column 3 (small): *Test sets: benchmark held-out split · 900 answerable
queries · per-crop held-out images. Disease = classification top-1.*

---

### COLUMN 4 — FROM FINDINGS TO ARCHITECTURE (the application)

**Block 4.1 — "Four Measured Failures → Four Design Decisions"** (~135 mm) — THE core table:

| Measured failure | Our design answer |
|---|---|
| LLMs hallucinate chemical dosages at 4.05–7.00% **even with gold evidence** | Safety gate **before** retrieval + 14-field fail-closed verifier |
| Dense retrieval collapses on farmer language: R@10 0.970 formal → 0.093 colloquial | Hybrid BM25 + dense, RRF fusion |
| 92% of formal entities never appear in farmer queries — *পাতা হলুদ হয়ে যাচ্ছে* ≠ "Yellow Mosaic Virus" | Register-aware retrieval across 6 dialects |
| The national helpline answered 92,094 calls last year | AI triage: auto-answer routine, escalate high-risk to humans |

*(The Bengali example sentence stays — it is the single most authentic detail on the poster.)*

**Block 4.2 — "System Architecture"** (~240 mm) — HERO diagram slot
- Preferred: **native TikZ** (crisp at A0). Fallback: `figures/D1_safety_pipeline.png`.
- Content spec: vertical 4-stage pipeline —
  **[1 Safety/Router]** 6 categories · fail-closed → red branch: banned chemical /
  self-harm → **STOP → 16123 / 999** → **[2 Hybrid Retrieval]** BM25+dense RRF, top-5 →
  **[3 Generation]** KrishokChat-4B, 4-bit, streamed Bengali → **[4 Verifier]** 14 fields ·
  6 relations · fail-closed → grounded answer + citations.
  Side rail: every decision → **audit log** → /analytics dashboard.
- Caption: *Unsafe categories stop at stage 1 — retrieval, generation and verification never run.*

**Block 4.3 — "Vision: Classify, Then Route"** (~155 mm)
- Existing `figures/D2_disease_vision_routing.png` (1.33:1 → ~190×143 mm).
- Caption (no numbers — they live in Col 3): *One photo → crop router → a small per-crop
  classifier → grounded Bengali treatment. The whole vision stack ships inside the app —
  no server, no network needed.*

---

### COLUMN 5 — PRODUCT · MARKET · MODEL

**Block 5.1 — "The Product — Krishi Patrak (কৃষি পত্রক)"** (~145 mm)
- Screenshot triptych (real, from `docs/ui_audit/screenshots/`): safety refusal in /chat ·
  photo diagnosis in /detect · audit dashboard in /analytics. Phone-framed, ~62×110 mm each.
- Copy: *Bengali-first web + Android. Every query shows its live agent trace; voice input;
  sunlight high-contrast mode for field use; offline-capable.*

**Block 5.2 — "Market Readiness"** (~130 mm, three bold-led rows)
> **What ships today.** Full-stack web app and Android app · on-device disease models that
> run with no network · live safety pipeline with audit dashboard · 437-entry treatment
> library verified end-to-end in live testing.
>
> **Why offline-first wins this market.** 73.4% of households own a smartphone, but only
> 43.6% of rural residents use the internet. An advisory app that needs the network loses
> half its users on arrival.
>
> **Scaling path.** Launch on a hosted API (≈2 paisa per answer); at volume, one rented GPU
> (~$497/month) serves ~13 million answers monthly.

**Block 5.3 — "Business Model: Free for Farmers, Paid by Institutions"** (~245 mm)
- **Free-vs-Premium diagram slot, 4:3 landscape (~200×150 mm)** — GPT-generated later. Content spec:
  - LEFT panel "FREE — for every farmer": mapped answers straight from the grounded
    knowledge base (no LLM — cannot hallucinate) · on-device photo diagnosis · safety gate · offline.
  - RIGHT panel "PREMIUM — full advisory": everything in Free + open-ended conversation on
    our fine-tuned model · priority · voice.
  - Bottom banner across both: **"The safety gate and 16123 escalation are identical in
    both tiers — nobody pays to stay safe."**
- Three lanes beneath (compact):
  > **B2G.** AI triage front-end for the Krishi Call Center — routine questions answered
  > automatically, high-risk cases escalated with a full audit trail. The audit log is the
  > trust asset for DAE / a2i.
  > **B2B.** Analytics dashboard for agro-dealers, seed companies and NGOs: district-level
  > insight into what farmers ask and which diseases surge. (ACI's Fosholi monetises its
  > 2.6M users the same way.)
  > **Licensing.** The 85,979-instance benchmark and 722-image soil dataset — CC-BY-4.0 for
  > research, commercial licence for agri-fintech and insurers.

**Block 5.4 — "Papers, Code & Data"** (~85 mm)
- Three QR codes (~35 mm): dataset (HF) · code (GitHub) · papers PDF.
- Refs [1][2][3] as fixed in §1 + repo handles.

**FOOTER (gemini theme):** refs + GitHub + HF + `Emergency triage: 16123 / 999`. No arXiv IDs.

---

## 5. FIGURE / IMAGE INVENTORY

| ID | What | Source | Size (mm) | Status |
|---|---|---|---|---|
| RIB | 6 stat chips | native LaTeX | row 1 | rebuild |
| T-ASSETS | merged dataset table | native LaTeX | ~200×140 | to build |
| T-NOVEL | novelty ✓/–/○ table | native LaTeX | ~200×110 | exists, keep |
| T-FIND | findings→design table | native LaTeX | ~200×115 | to build |
| C-MODEL | model bar chart | native pgfplots | ~200×120 | to build |
| C-RETR | retrieval mini-bars | native pgfplots | ~200×75 | to build |
| T-DISEASE | disease table + solobars | native LaTeX | ~200×100 | exists, keep |
| D-ARCH | 4-stage pipeline hero | **TikZ preferred** / fallback `D1_safety_pipeline.png` | ~200×220 | to build |
| D-ROUTE | classify-then-route | existing `D2_disease_vision_routing.png` | 190×143 | have |
| D-GROUND | grounded data flow | existing `D3_grounded_data.png` | 200×88 | have |
| IMG-FIELD | interview + soil photos | real photos | 2× ~95×65 | have |
| IMG-PRODUCT | 3 app screenshots | real, `docs/ui_audit/screenshots/` | 3× 62×110 | have |
| IMG-TIERS | free vs premium panel | **GPT later** (style-locked) | 200×150 (4:3) | to generate |
| QR ×3 | dataset / code / papers | generate | 35×35 each | to generate |

Note: `D0_root_system_flow.png` and `E_soil_scatter.png` are **not used** (redundant /
soil-model deprioritised). Keep files on disk for slides.

Path note: add `\graphicspath{{../figures/}{./assets/}{./img/}}` and copy screenshots/photos into `latex/img/`.

---

## 6. COLUMN VERTICAL BUDGET (usable ≈ 655 mm per column)

| Col | Blocks | Content total | Verdict |
|---|---|---|---|
| 1 | 80+75+115+135+60 | ~500 | comfortable |
| 2 | 175+95+130 | ~435 | breathing room (feature, not bug — winner poster was 0–8% ink) |
| 3 | 155+105+135+55 | ~475 | comfortable |
| 4 | 135+240+155 | ~555 | full — the architecture column |
| 5 | 145+130+245+85 | ~640 | tightest; trim order: QR row → screenshot pair → tier-diagram height |

---

## 7. WHAT WE DELIBERATELY EXCLUDE

- Soil model metrics (R², RMSE, 22%) — soil appears only as a dataset asset.
- End-to-end latency / throughput claims; mAP / IoU / bounding boxes.
- Invented market size / revenue projections; any arXiv ID (incl. banned 2606.29243).
- Node count 2,120 (only 2,882); old soil numbers; "110-word dialect map".
- No "limitations" section — only "Ongoing & Next".

---

## 8. NUMBER-ALLOCATION LEDGER (strict no-repetition)

**Rules:** (a) every number has ONE body home; (b) the ribbon is the glance layer — a chip
number may reappear in its single evidence block, never in prose twice; (c) `16123` is the
only sanctioned recurring element (ribbon + Impact + footer — it is the safety signature).

| Number | Home (single) |
|---|---|
| 47M · 20–40% yield loss | Col 1 Problem |
| 63% water / 50% urea (external trial) | Col 1 Impact (attributed, downstream) |
| 85,979 + 4 track counts + 66.3% | Col 2 assets table (+ ribbon chip, + novelty table row label) |
| 2,882 · 17,501 · 19,768 · 284 · 13 | Col 2 assets table only |
| 1,000 · 300 · 6 dialects | Col 2 assets table only |
| 722 · 0–21.5 kPa · 6 textures · 14 crops · 46 series | Col 2 assets table only |
| 0.314 · 0.165 · 0.104 · 0.087 · 1.9× · p≈6.7e-5 | Col 3 bar chart (+ribbon 1.9×) |
| 0.539 · 0.506 · 0.487 · 0.464 · 0.408 · +9% | Col 3 retrieval chart |
| 97.29 / 97.23 / 96.49 / 95.04 / 88.00 | Col 3 disease table (+ribbon 95–97%) |
| 436/437 · 1.6–21.8 MB · <30 ms | Col 3 badges (+ribbon <30 ms) |
| 0.31% (1/323) | Col 3 safety mini-block |
| 4.05–7.00% · 0.970→0.093 · 92% · Bengali example | Col 4 findings table |
| 92,094 calls | Col 4 findings table |
| 73.4% smartphone · 43.6% rural internet | Col 5 market readiness |
| 2 paisa · $497/mo · 13M answers | Col 5 scaling path (+ribbon 2 paisa) |
| 2.6M Fosholi users | Col 5 B2B lane |
| 16123 / 999 | ribbon + Col 1 Impact + footer (sanctioned) |

---

## 9. IMPLEMENTATION ORDER (one step per run, compile after each)

1. **Fix footer refs + rebuild ribbon** → compile. *(removes banned arXiv ID)*
2. **Column 1** all five blocks → compile.
3. **Column 2** assets table + D3 + field photos → compile.
4. **Column 3** pgfplots charts + disease table + safety mini → compile.
5. **Column 4** findings table + TikZ pipeline hero + D2 → compile.
6. **Column 5** screenshots + market + business (with placeholder box for tier diagram) + QR/links → compile.
7. **Polish pass**: density audit against ledger, spacing, alignment, font-size check for 1.5 m reading.

Parallel (not blocking LaTeX): generate free-vs-premium diagram + QR codes via GPT/external; supply tensiometer photo when available.

---

## 10. OPEN ITEMS FOR USER

1. Confirm the ribbon chip set (§3) — it changes from the current one.
2. Tensiometer field photo — when it arrives, it replaces/augments the Col 2 soil photo.
3. Free-vs-premium diagram: confirm 4:3 landscape (200×150 mm) fits your vision, or you prefer 3:4 vertical elsewhere.
4. Screenshots: confirm the three chosen (chat-safety / detect / analytics) or swap.
