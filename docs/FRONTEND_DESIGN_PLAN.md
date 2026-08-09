# KrishokChat — Full Frontend Design Plan

> **Status:** Planning document for capstone demo + investor pitch.
> **Goal:** Transform the current minimal frontend into a professional research-institute-grade
> website that showcases both the **farmer-facing tool** and the **research methodology** behind it.
> **Last updated:** 2026-08-10

---

## 1. What We Have vs. What We Need

### Current State (6 pages, minimal content)

| Page | Route | Status | Problem |
|------|-------|--------|---------|
| Landing | `/` | Basic hero + 4 pillars | No methodology, no numbers, no visual workflow, no credibility |
| Chat | `/chat` | Working QA panel | Good UX, but no research context visible |
| Detect | `/detect` | Working vision + chat | Good UX, but pipeline not explained to judges |
| Analytics | `/analytics` | Basic safety metrics | Too sparse, no benchmark data, no paper results |
| About | `/about` | 37 lines of generic text | No team, no methodology, no publications, no fieldwork |
| Contact | `/contact` | Minimal | No real team info, no institutional links |

### What's Missing (the gap)

1. **No research methodology page** — judges/investors can't see the 284 publications, 2,882 knowledge nodes, 85,979 benchmark instances, chemical-provenance audit pipeline, or the six-dialect construction
2. **No animated pipeline visualization** — the safety-critical agentic flow (safety → retrieval → generation → verification) is the headline feature but is invisible to visitors who don't open the chat
3. **No benchmark/results showcase** — the paper's actual numbers (GenF1, TrtCor, hallucination floor, R@10) are nowhere on the site
4. **No knowledge-graph/data visualization** — the 2,882-node provenance graph, 19,768 entities, 17,501 triples are invisible
5. **No fieldwork story** — the 300 farmer interviews in Rajshahi/Natore, the five-stage ground-truth pipeline, the 69 extension-officer validations — none of this human effort is visible
6. **No team/institutional credibility** — North South University, 13 government institutions, the Hugging Face dataset link — none shown
7. **No "why we're better" narrative** — the register-gap discovery, the BM25-vs-dense finding, the hallucination floor — the research contributions that make this more than a chatbot wrapper

---

## 2. Design Philosophy

### The dual-audience problem

This site serves two audiences simultaneously:

| Audience | What they want | Where they look |
|----------|---------------|-----------------|
| **Farmers** | Quick, trustworthy advice in Bengali | `/chat`, `/detect` |
| **Judges/Investors/Researchers** | Evidence this is real research, not a wrapper | Landing page, `/research`, `/methodology`, `/data` |

### The convention for this kind of site

Research-institute + product hybrid sites (think Google AI, Hugging Face, Anthropic research pages) follow this pattern:

1. **Landing page** = product hero + one research credibility signal (a number, a pipeline, a paper link)
2. **Research/Methodology page** = the deep dive — pipeline diagrams, benchmark tables, dataset stats
3. **Data/Dataset page** = the knowledge graph, sample nodes, download links, data card
4. **Results/Benchmark page** = actual evaluation numbers, comparison tables, charts
5. **Team/About page** = real people, institutions, publications, fieldwork photos
6. **Interactive demo** = the working product (chat + detect)

### Our visual identity (already established)

The "কৃষি পত্রক" (Field Notebook) system is already defined in `globals.css`:
- Warm paper backgrounds (`#faf6ef`), not cold gray
- Leaf green (`#2f5d3a`) as primary, ochre (`#c8893c`) as active highlight
- Tiro Bangla serif for headings, Noto Sans Bengali for body
- Mixed radii (4px / 8px / 12px / 18px), not all-2xl
- Paper grain texture, hairline rules

**Rule:** every new page must use this system. No blue, no gradients, no "AI app" aesthetic.

---

## 3. Full Page Architecture (Proposed)

### Route Map (10 pages)

```
/                           Landing (redesigned — product + research credibility)
/chat                       Farmer chat (existing, keep)
/detect                     Disease diagnosis (existing, keep)
/research                   Research overview (NEW — the "why we're better" page)
  /research/methodology     Construction pipeline (NEW — animated workflow)
  /research/benchmark       Evaluation results (NEW — tables + charts)
  /research/safety          Safety-critical design (NEW — agentic pipeline animation)
/data                       Knowledge base & dataset (NEW — graph viz + data card)
/team                       Team & fieldwork (NEW — real people + field photos)
/about                      About the project (REWRITE — institutional context)
/analytics                  Safety metrics dashboard (EXISTING — enhance)
/contact                    Contact (EXISTING — keep minimal)
```

### Navigation Structure

```
Navbar (all pages):
  [Logo: কৃষক চ্যাট]  চ্যাট  |  নির্ণয়  |  গবেষণা ▾  |  উপাত্ত  |  দল  |  পরিসংখ্যান

  গবেষণা dropdown:
    - পদ্ধতি (Methodology)
    - ফলাফল (Benchmark Results)
    - নিরাপত্তা ডিজাইন (Safety Design)
```

---

## 4. Page-by-Page Detailed Design

### 4.1 Landing Page (`/`) — REDESIGN

**Goal:** In 10 seconds, a visitor should understand: this is a Bengali agri-AI tool AND it's backed by real research.

**Sections (top to bottom):**

#### Section A: Hero (existing, enhanced)
- Keep the current hero text + CTA buttons
- **ADD:** A floating stat strip below the hero with 4 key numbers:
  - `২,৮৮২` জ্ঞান নোড (knowledge nodes)
  - `৮৫,৯৭৯` বেঞ্চমার্ক ইনস্ট্যান্স (benchmark instances)
  - `২৮৪` সরকারি প্রকাশনা (government publications)
  - `৬` উপভাষা (dialects)
- **ADD:** A subtle animated mini-pipeline (4 dots connected by lines: নিরাপত্তা → তথ্য → উত্তর → যাচাই) that lights up sequentially on a loop, 3-second cycle
- **IMAGE NEEDED:** A hero background image — a real Bangladesh field photo (paddy field with a farmer) — ask Gemini to generate a warm, documentary-style image

#### Section B: "How it works" — Animated Pipeline (NEW)
- A full-width horizontal animated workflow showing the 4-stage agentic pipeline:
  ```
  [কৃষকের প্রশ্ন] → [১. নিরাপত্তা] → [২. তথ্য সংগ্রহ] → [৩. উত্তর তৈরি] → [৪. যাচাই] → [উত্তর]
  ```
- Each stage is a card with: icon, Bengali name, 1-line English subtitle, 2-line description
- On scroll-into-view (Motion `whileInView`), the stages light up sequentially with a connecting line that draws left-to-right
- Below the pipeline: "প্রতিটি উত্তর এই চার ধাপে আসে" (every answer comes through these four steps)
- **INTERACTIVE:** Clicking a stage opens a modal/expandable section with more detail:
  - Safety: 12-category taxonomy, 16123 helpline, canned response examples
  - Retrieval: BM25 over 2,882 nodes, provenance-locked, citation-level traceability
  - Generation: Gemma-4 fine-tuned, source-grounded prompt, no fabrication
  - Verification: dosage-level audit, Bengali numeral normalization, flag/unverified system

#### Section C: Research Credibility Strip (NEW)
- 3 cards side by side:
  1. **"প্রমাণ-ভিত্তিক"** — "প্রতিটি উত্তর সরকারি প্রকাশনা থেকে, উৎসসহ" — icon: document with checkmark
  2. **"নিরাপত্তা-সচেতন"** — "১২-শ্রেণীর নিরাপত্তা ট্যাক্সোনমি, রাসায়নিক প্রমাণ-অডিট" — icon: shield
  3. **"বহু-উপভাষিক"** — "৬টি আঞ্চলিক উপভাষায়, ফসল-নির্দিষ্ট" — icon: speech bubbles
- Each card links to the relevant `/research/*` page

#### Section D: "কেন আমরা ভিন্ন" (Why we're different) (NEW)
- A comparison table or side-by-side card layout:
  | | সাধারণ চ্যাটবট | কৃষক চ্যাট |
  |---|---|---|
  | উৎস | ওয়েব থেকে অনুমান | ২৮৪ সরকারি প্রকাশনা |
  | নিরাপত্তা | নেই | ১২-শ্রেণী ট্যাক্সোনমি |
  | রাসায়নিক | অনিয়ন্ত্রিত | প্রমাণ-অডিটযোগ্য |
  | উপভাষা | শুধু প্রমিত | ৬ উপভাষা |
  | ট্রেস | অস্বচ্ছ | উৎস আইডি + পৃষ্ঠা নম্বর |

#### Section E: Live Demo CTA (existing, keep)
- Two big buttons: "ছবি দিন নির্ণয় করুন" → `/detect`, "বাংলায় প্রশ্ন করুন" → `/chat`

#### Section F: Helpline strip (existing, keep)

#### Section G: Footer (enhanced — see §4.10)

---

### 4.2 Research Overview (`/research`) — NEW

**Goal:** The "why we're better" page. This is where judges spend 2 minutes reading.

**Sections:**

#### A. Research Summary Hero
- Title: "প্রমাণ-ভিত্তিক বাংলা কৃষি এআই" (Provenance-grounded Bengali Agri-AI)
- Subtitle: "২৮৪ সরকারি প্রকাশনা, ২,৮৮২ জ্ঞান নোড, ৮৫,৯৭৯ মূল্যায়ন ইনস্ট্যান্স"
- 3 CTA buttons: পদ্ধতি / ফলাফল / নিরাপত্তা ডিজাইন

#### B. Two Papers Side-by-Side
- Two cards:
  1. **KrishokChat (EACL 2026)** — "৮৫,৯৭৯-ইনস্ট্যান্স বাংলা কৃষি বেঞ্চমার্ক, ৪ ট্র্যাক, রাসায়নিক প্রমাণ-অডিট"
     - Link to paper PDF, Hugging Face dataset
  2. **AgriTrust (SIGIR-AP 2026)** — "২,৮৮২-নোড প্রমাণ-ভিত্তিক রিট্রিভাল বেঞ্চমার্ক, ৫ আর্কিটেকচার, ৬ এম্বেডিং"
     - Link to paper PDF

#### C. Key Findings (animated counters)
- 4 big animated numbers that count up on scroll:
  - `৪.০৫–৭.০০%` — রাসায়নিক হ্যালুসিনেশন ফ্লোর (even with oracle evidence)
  - `০.৩১৪` — ফাইন-টিউনড GenF1 (vs 0.165 best zero-shot)
  - `০.৫৩৯` — হাইব্রিড R@10 (BM25+Dense fusion)
  - `০.৭২` — ইন্টার-অ্যানোটেটর κ (farmer query gold mapping)

#### D. Contribution Summary
- 4 numbered contributions (from the paper):
  1. ৮৫,৯৭৯-ইনস্ট্যান্স, ৪-ট্র্যাক বেঞ্চমার্ক
  2. প্রমাণ-সংরক্ষণকারী কনস্ট্রাকশন পাইপলাইন
  3. নিরাপত্তা-সচেতন ট্র্যাক পেয়ারিং (chemical trace + refusal taxonomy)
  4. ১,০০০-কোয়েরি রিয়েল-ওয়ার্ল্ড ফার্মার বেঞ্চমার্ক

---

### 4.3 Methodology Page (`/research/methodology`) — NEW

**Goal:** Show the construction pipeline — how 284 PDFs became 85,979 benchmark instances.

**Sections:**

#### A. Pipeline Visualization (animated, full-width)
- A horizontal flow diagram, 5 stages, animated on scroll:
  ```
  [২৮৪ সরকারি PDF]
       ↓ OCR + Markdown
  [২,৬৮০ সেকশন প্যাসেজ]
       ↓ Header-guided segmentation
  [২,৯৪৬ সিম্যান্টিক ইউনিট]
       ↓ Generation cell + intent pairing
  [৮৫,৯৭৯ ইনস্ট্যান্স]
       ↓ Quality gates (G1-G5)
  [৪ ট্র্যাক রিলিজ]
  ```
- Each stage: card with number (animated count-up), label, 1-line description
- Connecting arrows draw sequentially (Motion SVG path animation)
- **IMAGE NEEDED:** If we can get the original `figure_1.png` from the paper, use it. Otherwise, build this as an HTML/CSS/Motion animated diagram (preferred for web).

#### B. The 4 Tracks (tabbed or card layout)
- 4 cards, one per track:
  1. **সাধারণ জ্ঞান QA** — 28,993 instances — "রাসায়নিক-মুক্ত জ্ঞান পরীক্ষণ"
  2. **চিকিৎসা QA** — 11,224 instances — "নিরাপত্তা-সংবেদনশীল রাসায়নিক পরামর্শ"
     - Sub-stat: 7,437 (66.3%) carry chemical_trace
  3. **নিরাপত্তা QA** — 20,112 instances — "১২-শ্রেণী প্রত্যাখ্যান + EVPI রি-কোয়েরি"
     - Sub-stat: 3,216 T3 refusal + 16,896 T4 re-query
  4. **টেবিল QA** — 25,650 instances — "৩-স্তরের কাঠামোগত রিজনিং"

#### C. Design Principles (4 cards)
- "উত্তর নির্যাসিত, তৈরি নয়" (Answers extracted, never generated)
- "বৈচিত্র্য নমুনায়িত, টেমপ্লেট নয়" (Diversity sampled, not templated)
- "কনটেন্ট টোকেন ফ্রোজেন" (Content tokens frozen across dialects)
- "প্রতিটি ইনস্ট্যান্স প্রমাণ-লকড" (Each instance provenance-locked)

#### D. Knowledge Node Construction (from AgriTrust paper)
- The 3-layer node structure:
  - Natural-language content
  - Structured agricultural facts (entities, triples)
  - Provenance (source, page, organization)
- Stats: 2,882 nodes, 19,768 entities (6.9/node), 17,501 triples, 1,022 image-linked (35.5%)
- **INTERACTIVE:** A sample knowledge node card — show a real node JSON with expandable fields
- The closed-loop refinement: Gemini generates → GPT-5-Nano verifies → regenerate if ≤3 → 283 nodes (9.8%) refined

#### E. Chemical-Provenance Audit Pipeline
- Vertical animated flow (from the paper's TikZ figure):
  ```
  Generated Response
       ↓
  Chemical Mention Extraction
       ↓
  Canonical Normalization (210-entry alias dictionary)
       ↓
  Compare Against chemical_trace array
       ↓
  Verdict: Correct / Omission / Hallucination
  ```
- Side panel: the 7 safety-critical domains (fertilizer, disease, pest, IPM, seed tech, food safety, herbicide)

---

### 4.4 Benchmark Results (`/research/benchmark`) — NEW

**Goal:** Show the actual evaluation numbers. This is the credibility page.

**Sections:**

#### A. Main Results Table
- The RQ1/RQ2 table from the KrishokChat paper (Table 3):
  - 6 models × 4 metrics (GenF1, GenHal, TrtCor, TrtHal) × 2 conditions (CB, Oracle)
- Styled as a clean data table with:
  - Best values highlighted in leaf green
  - SFT model row separated by a rule
  - Footnote with significance marker
- **INTERACTIVE:** Toggle between "Closed-Book" and "Oracle" columns

#### B. Retrieval Results (from AgriTrust)
- Table: 5 architectures × 5 metrics (R@1, R@5, R@10, MRR, nDCG@10)
- Highlight: Hybrid RRF = 0.539, BM25 = 0.506, Dense = 0.464
- **CHART NEEDED:** A bar chart comparing R@10 across architectures (can be built with a simple CSS/Motion bar chart, no chart library needed)

#### C. The Register Gap Discovery (key finding)
- A visual showing the bimodal dense retrieval pattern:
  - Farmer queries: R@10 = 0.093 (near failure)
  - Safety queries: R@10 = 0.970 (near perfect)
- **CHART:** A diverging bar chart — farmer on left (short bar), safety on right (long bar)
- Caption: "৯৬.৪% কোয়েরির জ্যাকার্ড < ০.১০ — ফার্মার ভাষা আনুষ্ঠানিক ভাষার চেয়ে ভিন্ন"

#### D. Cross-Lingual Collapse
- 3-row table: BN→BN, EN→BN (cross-lingual), EN→EN
- Show BM25 collapse: 0.506 → 0.004 (99% drop)
- Show Dense survival: 0.464 → 0.425 (8% drop)
- **CHART:** A line/bar showing the collapse

#### E. Farmer Benchmark Results
- Table: 6 models × 2 metrics (Token F1, Halluc%)
- 350 real farmer queries
- Caption: "৩০০টি মাঠ সাক্ষাৎকার থেকে সংগৃহীত প্রশ্ন"

#### F. The Hallucination Floor (key finding)
- A callout box: "এমন পরিপূর্ণ অরাকল তথ্য থাকা সত্ত্বেও ৪.০৫–৭.০০% রাসায়নিক হ্যালুসিনেশন থেকে যায়"
- This is the unsolved problem — showing it builds credibility

---

### 4.5 Safety Design (`/research/safety`) — NEW

**Goal:** This is the headline feature for the poster/demo. Show the safety-critical agentic design.

**Sections:**

#### A. The 4-Stage Agentic Pipeline (ANIMATED — the centerpiece)
- Full-width, large animated diagram:
  ```
  User Query
       ↓
  [1] Safety/Router Agent
       ├─ unsafe → canned response + 16123 + stop
       └─ safe ↓
  [2] Retrieval Agent (BM25 over 2,882 nodes)
       ↓
  [3] Generation Agent (Gemma-4, source-grounded)
       ↓
  [4] Verifier Agent (dosage audit, grounding check)
       ↓
  Answer + Sources + Trace
  ```
- **Animation:** On page load or scroll-into-view:
  1. A "query" dot travels down the pipeline
  2. At stage 1, it branches: one path shows "unsafe → blocked" (red), the other "safe → continue" (green)
  3. The safe path continues through stages 2, 3, 4 with the dot traveling
  4. Each stage card highlights as the dot passes
  5. Final output card appears with answer + sources + trace
- **INTERACTIVE:** A toggle to switch between "safe query" and "unsafe query" demo paths
  - Safe: "আলুর দেরি ব্লাইট কীভাবে প্রতিরোধ করব?" → full pipeline
  - Unsafe: "প্যারাকোয়াট কীভাবে বেশি খাব?" → blocked at stage 1

#### B. 12-Category Safety Taxonomy
- A grid of 12 cards (from the paper's Table 6):
  - chemical_misuse, scope_unknown_pest, scope_missing_crop, dosage_safety
  - diagnostic_overshoot, veterinary_scope, human_medical_scope, financial_advice
  - legal_scope, dialect_discrimination, over_promise, ethical_boundary
- Each card: category name (EN + BN), refusal trigger, severity tier (minor/severe)
- Color-coded: severe = clay/border, minor = ochre/soft

#### C. EVPI Re-Query Slots (T4)
- The 6 slots ranked by Discriminative Power:
  - crop (0.91), symptom (0.84), onset (0.62), severity (0.45), growth_stage (0.38), chemical_history (0.31)
- **CHART:** A horizontal bar chart showing DP values, animated on scroll

#### D. Chemical-Provenance Audit
- The audit pipeline (same as methodology page but focused on safety)
- The 210-entry alias dictionary
- The correct/omission/hallucination verdict system
- Sample: a real treatment record with its chemical_trace array

#### E. Canned Safe Responses
- 3 example responses:
  - Banned chemical → 16123 redirect
  - Self-harm → 999 + 16123 + medical help
  - Low confidence → 16123 redirect
- Show these as chat bubbles to demonstrate tone

#### F. Audit Trail
- Explanation: every classification logged locally (JSONL), powers the metrics panel
- Link to `/analytics` to see live audit data

---

### 4.6 Data & Dataset (`/data`) — NEW

**Goal:** Show the knowledge base and dataset as a tangible resource.

**Sections:**

#### A. Dataset Overview
- Large stat cards:
  - `২,৮৮২` জ্ঞান নোড
  - `১৯,৭৬৮` এনটিটি
  - `১৭,৫০১` ফ্যাক্টুয়াল ট্রিপল
  - `১,০২২` ইমেজ-লিঙ্কড নোড (35.5%)
  - `৯১৫` অনন্য ফসল
  - `৭০৪` রোগ ভ্যারিয়েন্ট
  - `২,৭২৯` রাসায়নিক/কীটনাশক এনটিটি

#### B. Knowledge Graph Visualization (INTERACTIVE)
- **IMAGE NEEDED:** A network/graph visualization of the knowledge graph
  - Ask Gemini to generate a node-link diagram showing the 13-category taxonomy
  - Or build a simple D3.js / CSS-based interactive graph (preferred)
- Categories with node counts:
  - Variety (695), Cultivation Practice (570), Disease (430), Pest (380)
  - down to Food Safety (18)
- **INTERACTIVE:** Click a category → show sample nodes from that category

#### C. Sample Knowledge Node (INTERACTIVE)
- A card showing a real knowledge node from the corpus:
  - `id`: `DAE_PEST_1206A0_001`
  - `title_bn`: আলুর দেরি ব্লাইট
  - `content_bn`: [real content excerpt]
  - `source_document`: Potato Disease Manuals (Plantwise)
  - `publisher`: CABI
  - `citation`: CABI. Late blight. Potato Disease Manuals.
  - `entities`: [Phytophthora infestans, potato, late blight]
  - `chemical_trace`: [Mancozeb, Metalaxyl]
- Expandable JSON view

#### D. Source Institutions
- Logos/names of the 13 institutions:
  - BARC, BARI, DAE, DLS, DoF, CDB, NARS, SRDI, BSRTI, MoA, CABI, IRRI, WorldFish
- **IMAGE NEEDED:** Institution logos (if available) or a clean text grid

#### E. Dataset Access
- Links to:
  - Hugging Face: `https://huggingface.co/datasets/RaiyanKhaan/KrishokChat-145k`
  - Paper PDF (KrishokChat)
  - Paper PDF (AgriTrust)
- License: CC-BY-4.0

#### F. Data Card
- A summary card (like the paper's Figure 2) with all key properties

---

### 4.7 Team & Fieldwork (`/team`) — NEW

**Goal:** Show the real people and real fieldwork behind this.

**Sections:**

#### A. Team
- 3 team member cards:
  - Khan Raiyan Ibne Reza — North South University
  - Sumaiya Tabassum Nimi — North South University
  - Omar-Ibne Shahid — North South University
- **IMAGE NEEDED:** Team photos (or professional avatars if photos unavailable)
- Supervisors/faculty advisors (if any)

#### B. Fieldwork Story
- "রাজশাহী ও নাটোর জেলায় ৩০০ জন কৃষকের সাথে মাঠ পর্যায়ের সাক্ষাৎকার"
- The 5-stage ground-truth pipeline:
  1. Query parsing → attribute tuple
  2. Corpus indexing (crop, symptom, category)
  3. Attribute intersection (2,946 → 5-15 candidates)
  4. Expert annotator selects single unit
  5. Reference answer generated from verified unit
- **IMAGE NEEDED:** Field photos — farmers, fields, interview scenes
  - Ask Gemini to generate documentary-style images if real photos unavailable
- The 69 extension-officer validations (100% raw agreement)

#### C. Institutional Partners
- North South University
- 13 government/research institutions (listed)

#### D. Publications
- Two papers:
  1. KrishokChat — EACL 2026 (Data Resource & Benchmark Track)
  2. AgriTrust — SIGIR-AP 2026
- Links to PDFs, arXiv, Hugging Face

---

### 4.8 About Page (`/about`) — REWRITE

**Goal:** Institutional context, not generic text.

**Sections:**
- Project mission (1 paragraph)
- The gap: Bangladesh has 230M Bengali speakers, insufficient extension officers
- The approach: provenance-grounded, safety-aware, dialect-inclusive
- The status: research prototype, not production (explicit non-deployment statement)
- Links to `/research`, `/data`, `/team`

---

### 4.9 Analytics Page (`/analytics`) — ENHANCE

**Goal:** Make the existing metrics dashboard richer.

**Enhancements:**
- Add a category breakdown chart (bar chart of by_category)
- Add a timeline chart (queries over time)
- Add a "safety coverage" donut showing % safe vs blocked
- Keep the recent queries list
- Add a link: "পদ্ধতি দেখুন" → `/research/safety`

---

### 4.10 Footer (all pages) — ENHANCE

**Structure:**
```
[Logo + tagline]
    পণ্য: চ্যাট | নির্ণয় | পরিসংখ্যান
    গবেষণা: পদ্ধতি | ফলাফল | নিরাপত্তা | উপাত্ত
    প্রতিষ্ঠান: দল | সম্পর্কে | যোগাযোগ
    সম্পদ: Hugging Face | Paper 1 | Paper 2 | GitHub

[License: CC-BY-4.0 | গবেষণা প্রোটোটাইপ | © 2026 North South University]
```

---

## 5. Animated Workflows — Technical Specification

### 5.1 Landing Page Mini-Pipeline (Section A)
- **Component:** `<MiniPipeline />`
- **Tech:** Motion `whileInView` + SVG path animation
- **Behavior:** 4 dots (সুরক্ষা → তথ্য → উত্তর → যাচাই), connected by a line. On scroll-into-view, dots light up sequentially (200ms each), line draws between them. Loops every 5 seconds.
- **Size:** ~60px height, full width

### 5.2 Landing Page Full Pipeline (Section B)
- **Component:** `<PipelineFlow />`
- **Tech:** Motion stagger + SVG connectors
- **Behavior:** 5 cards in a row. On scroll-into-view, cards fade in left-to-right (100ms stagger). Connecting lines draw between cards. Clicking a card expands a detail panel below.
- **Size:** ~200px height per card, full width

### 5.3 Methodology Construction Pipeline (Section A)
- **Component:** `<ConstructionPipeline />`
- **Tech:** Motion + animated counters + SVG flow
- **Behavior:** 5 vertical/horizontal stages. Numbers count up (0 → 284, 0 → 2680, etc.) on scroll-into-view. Arrows between stages animate (draw sequentially).

### 5.4 Safety Agentic Pipeline (THE centerpiece)
- **Component:** `<AgenticPipelineAnimation />`
- **Tech:** Motion + SVG path + state machine
- **Behavior:**
  1. A "query" dot enters from top
  2. Arrives at Safety Agent → branches into two paths
  3. Toggle: "safe query" (dot takes green path down) vs "unsafe query" (dot takes red path to "blocked" card)
  4. Safe path: dot travels through Retrieval → Generation → Verifier
  5. Each stage card highlights (bg color change + scale) as dot passes
  6. Final: "Answer + Sources + Trace" card appears
- **Duration:** ~4 seconds for full safe path, ~2 seconds for unsafe path
- **Interactive:** Toggle button to switch query type, replay button

### 5.5 Benchmark Charts
- **Components:** `<BarChart />`, `<DivergingBarChart />`, `<HorizontalBarChart />`
- **Tech:** CSS + Motion (no chart library — keeps bundle small)
- **Behavior:** Bars grow from 0 to value on scroll-into-view, values count up

---

## 6. Images & Diagrams Needed from Gemini

> **Note:** I cannot see images directly. Please generate these and place them in
> `frontend/public/images/`. I'll wire them into the components.

| # | Image | Purpose | Where it goes | Prompt for Gemini |
|---|-------|---------|---------------|-------------------|
| 1 | **Hero field photo** | Landing hero background | `/` Section A | "Documentary-style photo of a Bangladesh paddy field at golden hour, a farmer in distance, warm tones, no text" |
| 2 | **Construction pipeline diagram** | Methodology page | `/research/methodology` Section A | "Clean infographic: 284 PDFs → 2,686 passages → 2,946 semantic units → 85,979 instances → 4 tracks. Horizontal flow, warm paper background, leaf green and ochre accents, Bengali labels" — OR use the paper's `figure_1.png` directly |
| 3 | **Knowledge graph visualization** | Data page | `/data` Section B | "Network graph visualization, 13 clusters representing agricultural categories, nodes connected by edges, warm color scheme, dark text on light background" |
| 4 | **Safety taxonomy grid** | Safety page | `/research/safety` Section B | "12-card grid, each card showing a safety category with icon, warm paper background, clay/ochre color coding for severity" — OR build as HTML/CSS |
| 5 | **Agentic pipeline diagram** | Safety page | `/research/safety` Section A | "Vertical flowchart: User Query → Safety Agent (branch: unsafe/blocked vs safe/continue) → Retrieval → Generation → Verifier → Answer. Clean, modern, warm tones" — OR build as animated HTML/SVG |
| 6 | **Team photo or avatar set** | Team page | `/team` Section A | "Professional headshots or minimal illustrated avatars for 3 researchers, warm tones" |
| 7 | **Fieldwork photos** | Team page | `/team` Section B | "Documentary-style photos: farmer interview in Bangladesh field, paddy field, agricultural extension scene, warm documentary tone" |
| 8 | **Institution logos** | Data page | `/data` Section D | Logos of BARC, BARI, DAE, etc. — or use a clean text grid |
| 9 | **Chemical audit pipeline** | Methodology + Safety | `/research/methodology` Section E | "Vertical flowchart: Response → Extraction → Normalization → Compare → Verdict. Clean, warm tones" — OR build as HTML |
| 10 | **Data card** | Data page | `/data` Section F | Use the paper's `dataset_card.png` directly, or recreate as HTML |

> **Priority:** Images 1, 3, 5, 7 are the most impactful. The rest can be built as HTML/CSS/Motion components (which is actually better for web — scalable, animatable, no file size cost).

---

## 7. Implementation Priority & Phasing

### Phase 1: Credibility Layer (highest impact for demo)
1. `/research` — Research overview (2 minutes to build credibility)
2. `/research/safety` — Animated agentic pipeline (the poster feature)
3. Landing page redesign (add stat strip + mini-pipeline + comparison table)
4. `/team` — Team + fieldwork (human element)

### Phase 2: Depth Layer
5. `/research/methodology` — Construction pipeline animation
6. `/research/benchmark` — Results tables + charts
7. `/data` — Knowledge graph + sample node

### Phase 3: Polish Layer
8. `/about` rewrite
9. `/analytics` enhancement
10. Footer enhancement
10. Navbar dropdown for গবেষণা

### Phase 4: Images Integration
11. Wire in Gemini-generated images as they become available
12. Replace HTML diagrams with images where images are better (field photos, team photos)

---

## 8. Key Numbers to Surface (from both papers)

### KrishokChat Paper
| Metric | Value | Where to show |
|--------|-------|---------------|
| Total benchmark instances | 85,979 | Landing, Research, Methodology |
| General QA | 28,993 | Methodology |
| Treatment QA | 11,224 | Methodology, Safety |
| Safety QA | 20,112 | Safety |
| Table QA | 25,650 | Methodology |
| Farmer Benchmark | 1,000 (350 eval) | Team, Benchmark |
| Source publications | 284 | Everywhere |
| Institutions | 13 | Data, Team |
| Dialects | 6 | Landing, Methodology |
| SFT model GenF1 | 0.314 | Benchmark |
| Best zero-shot GenF1 | 0.165 | Benchmark |
| Hallucination floor | 4.05–7.00% | Benchmark, Safety |
| Chemical-bearing records | 7,437 (66.3%) | Safety, Methodology |
| Safety taxonomy categories | 12 | Safety |
| EVPI slots | 6 | Safety |
| Alias dictionary | 210 entries | Safety |
| Field interviews | 300 (Rajshahi+Natore) | Team |
| Extension officer validation | 69 (100% agreement) | Team |

### AgriTrust Paper
| Metric | Value | Where to show |
|--------|-------|---------------|
| Knowledge nodes | 2,882 | Landing, Data, Methodology |
| Image-linked nodes | 1,022 (35.5%) | Data |
| Entities | 19,768 | Data |
| Factual triples | 17,501 | Data |
| Unique crops | 915 | Data |
| Disease variants | 704 | Data |
| Chemical entities | 2,729 | Data, Safety |
| Queries | 1,000 (900 answerable) | Benchmark |
| Inter-annotator κ (farmer+safety) | 0.72 | Benchmark, Team |
| Inter-annotator κ (KG) | 0.78 | Benchmark |
| Human audit κ | 0.81 | Methodology |
| BM25 R@10 | 0.506 | Benchmark |
| Dense R@10 | 0.464 | Benchmark |
| Hybrid RRF R@10 | 0.539 | Benchmark |
| Dense on farmer queries | 0.093 | Benchmark (register gap) |
| Dense on safety queries | 0.970 | Benchmark (register gap) |
| BM25 cross-lingual collapse | 0.506 → 0.004 | Benchmark |
| Configuration audit (task type) | 7× R@10 drop | Benchmark |
| Node verification | Gemini gen → GPT-5-Nano verify | Methodology |
| Refined nodes | 283 (9.8%) | Methodology |

---

## 9. Conventions & Rules

### Visual
- Use existing "কৃষি পত্রক" design system (globals.css) — no deviations
- All new pages: `bg-paper` background, `text-ink` text, `font-display` headings
- Charts: CSS-based, no chart library (keeps bundle small, matches aesthetic)
- Diagrams: HTML/SVG/Motion animated (preferred) over static images
- Images: only for photos (field, team, hero) and complex visualizations (graph)

### Content
- All user-facing text in Bengali (with English subtitles where helpful for judges)
- Numbers in Bengali numerals (০-৯) on display, Arabic numerals in data tables
- Every claim must be traceable to one of the two papers — no fabrication
- If a number isn't in the papers, leave a `TODO` placeholder

### Technical
- New pages go in `frontend/src/app/(marketing)/` or `(app)/` based on audience
- Research pages = `(marketing)` (public, no app chrome needed)
- Reuse existing components: `PipelineRail`, `ConfidenceBadge`, `SourceList`
- New components go in `frontend/src/components/research/`
- Motion animations: use existing `enter`, `stagger`, `dur`, `ease` from `@/lib/motion`
- No new dependencies unless absolutely necessary

### Motion
- All animations use Motion (formerly Framer Motion) — already in the stack
- `whileInView` for scroll-triggered animations
- Stagger children for sequential reveals
- SVG path animation for connecting lines/arrows
- Animated counters for key numbers

---

## 10. What I Need From You

Before I start building, I need:

1. **Images from Gemini** (see §6) — at minimum:
   - Hero field photo (#1)
   - Fieldwork photos (#7)
   - Team photos (#6)
   - The rest I can build as HTML/CSS/Motion

2. **Confirmation on priority** — should I start with Phase 1 (Research + Safety + Landing redesign + Team)?

3. **Paper PDFs** — are the paper PDFs linkable? If the papers are under review (anonymous), should I link to arXiv or omit?

4. **Hugging Face link** — the paper mentions `https://huggingface.co/datasets/RaiyanKhaan/KrishokChat-145k` — is this public?

5. **Team details** — any faculty advisors or supervisors to list? Any specific roles/titles for the 3 authors?

---

## 11. Open Questions

- Should the research pages be in Bengali, English, or bilingual? (Current plan: Bengali primary, English subtitles for key terms — helps judges who don't read Bengali)
- Should we add a blog/publications section for future papers?
- Should the analytics page show benchmark results too, or keep it focused on live safety metrics?
- Should we add a "try the API" section for developers?

---

> **Next action:** Confirm priorities and provide images. Then I build Phase 1.

---

## 12. Enhancement Proposal (2026-08-10 audit)

### Issues found in re-verification

**A. Navigation gaps (critical)**
- `/team` and `/data` have NO navbar link — only discoverable via footer or `/research` page
- Research sub-pages (`/research/methodology`, `/research/benchmark`, `/research/safety`) not in navbar
- Convention violation: Allen Institute / Carnegie Science pattern = ≤2 clicks to any page

**B. Bad Bengali/English code-mixing (critical)**
- English technical terms written in Bengali script are awkward and meaningless:
  - `কনস্ট্রাকশন` (Construction) → should be `নির্মাণ` or keep "Construction" in English
  - `ডিজাইন` (Design) → should be `নকশা` or keep "Design"
  - `রিট্রিভাল` (Retrieval) → should be `তথ্য সংগ্রহ` (already used elsewhere, inconsistent)
  - `জেনারেশন` (Generation) → should be `উত্তর তৈরি`
  - `ভেরিফায়ার` (Verifier) → should be `যাচাই`
  - `ক্লাসিফিকেশন` → should be `শ্রেণীবিন্যাস`
  - `নর্মালাইজেশন` → should be `মানকীকরণ`
  - `অ্যানোটেটর` → should be `নির্দেশক` or keep "Annotator"
  - `প্রোটোকল` → should be `প্রটোকল` or keep "Protocol"
  - `সেগমেন্টেশন` → should be `খণ্ডায়ন`
  - `রিফাইনমেন্ট` → should be `পরিমার্জন`
  - `অ্যাগ্রিগেশন` → should be `সমষ্টি`
- **Convention**: Keep proper Bengali words for common concepts; keep English technical terms (BM25, RAG, LLM, API) in English script within Bengali text. Never transliterate English words into Bengali script.

**C. Home page too plain**
- Needs: animated timeline/workflow section, weather widget, helpline registration form, more visual variety
- Hero image overlay still suboptimal
- Missing "story" sections that build emotional connection

**D. Color visibility**
- Ink colors deepened but some `text-ink-soft` on `bg-paper-2` still low contrast
- Need WCAG AA compliance check

### Proposed enhancements (Phase 4)

1. **Fix navbar** — add দল (Team), উপাত্ত (Data), research dropdown
2. **Fix all Bengali transliterations** — replace with proper Bengali or English-in-script
3. **Rebuild home page** with:
   - Modern hero with better image treatment (darker scrim, text on solid panel)
   - Animated timeline section (research journey: 2024 → 2026)
   - Weather widget (new backend endpoint using Gemini, token-efficient)
   - Helpline registration form (collects name/phone/district, stores locally)
   - "Live impact" section with animated counters
   - Testimonial/quote section (farmer quotes from fieldwork)
4. **Add `/api/weather` backend endpoint** — Gemini-powered, token-efficient
5. **Add `/api/helpline/register` backend endpoint** — local storage only
6. **Color audit** — ensure WCAG AA contrast on all text/bg combinations

### Execution order
1. Fix navbar (quick)
2. Fix all Bengali transliterations (batch replace)
3. Add weather + helpline backend endpoints
4. Rebuild home page with new sections
5. Final verification
