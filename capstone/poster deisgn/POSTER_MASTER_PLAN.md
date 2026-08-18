# KrishokChat — A0 Poster Master Plan (Landscape, Canva build)

**This is the ONLY planning doc. Everything else backdated was deleted.**
Build in Canva, block by block. You place; the guide directs. Approve each step before the next.

Reference: `example_poster.pdf` (last year's winner) — landscape, one warm background wash,
single strong accent, very low ink density, reads as one designed piece (not floating white boxes).
We copy that *discipline*, not its colors.

---

## 0. Locked decisions

| Decision | Value |
|---|---|
| Orientation | **Landscape A0 — 1189 × 841 mm** (winner's format) |
| Canvas px (if needed) | 4494 × 3179 px |
| Theme | Warm field-paper background wash + deep leaf-green accent (agri identity) |
| Method | Canva, one block at a time, approval gates |
| Density target | **Low** — every zone breathes; ~30–40% ink max per zone |

### Palette (save as Canva swatches — use ONLY these)

| Role | Hex | Used for |
|---|---|---|
| Canvas wash (whole page) | `#F4EEE1` | entire background — no white page |
| Deep leaf green (primary) | `#1F5132` | header band, section header bars |
| Mid green (secondary) | `#3E7D4F` | sub-accents, arrows, chart bars |
| Warm ochre (data accent) | `#C2792E` | numbers/soil highlights, thin rules |
| Soft gold (title pop) | `#F0C24E` | the word "KrishokChat" on green |
| Alert red (safety ONLY) | `#C0342B` | 16123 / escalation only |
| Ink (text) | `#241E17` | body + dark headings |
| Soft card | `#FBF7EE` | when a content box is genuinely needed |

Fonts: **Poppins / Plus Jakarta Sans** (headings, bold), **Inter** (body), **Tiro Bangla / Noto Serif Bengali** (Bengali only).

---

## 1. Geometry (measured, fits with breathing room)

```
canvas 1189 × 841 mm
outer margin: 28 mm all sides
header band: 132 mm tall (full width)
gap between blocks: 14 mm
usable width: 1133 mm
body height under band: 667 mm
3 content columns: 365.7 mm each (18 mm column gaps)
```

The body is a **classic 3-column academic poster** (like the winner). Columns read
left→right. This keeps density low and the eye guided.

---

## 2. FULL PLACEMENT MAP (what goes exactly where)

```
┌──────────────────────────────────────────────────────────────────────────┐
│  HEADER BAND (green #1F5132, full width, 132 mm)                           │
│  [NSU logo] | 2 pills | TITLE (KrishokChat gold) | subtitle | authors      │
├───────── ochre rule (#C2792E, 3 mm) ───────────────────────────────────────┤
│                                                                            │
│  COLUMN A (366 mm)      COLUMN B (366 mm)        COLUMN C (366 mm)          │
│  ── THE PROBLEM &       ── HOW IT WORKS          ── PROOF IT WORKS          │
│     WHAT WE BUILT          (architecture)           (evidence + impact)     │
│                                                                            │
│  A1 Problem strip       B1 Root system flow      C1 Model-beats-baselines  │
│     (3 short lines +        (D0 diagram, large)      table (KrishokChat-4B) │
│      1 hero stat)                                                          │
│                         B2 Safety pipeline        C2 Disease accuracy       │
│  A2 Four contributions     (D1 diagram)              table + <30ms badge    │
│     (numbered list)                                                        │
│                         B3 Disease routing        C3 Soil scatter          │
│  A3 Grounded-data          (D2 diagram)              (E_soil_scatter) +     │
│     foundation (D3)                                  22% ↓ callout          │
│                                                                            │
│                                                    C4 Impact + Business     │
│                                                       (3 tight lines)       │
├────────────────────────────────────────────────────────────────────────  ┤
│  FOOTER STRIP (green, thin): refs [1][2][3] · CC-BY-4.0 · QR · 16123/999   │
└──────────────────────────────────────────────────────────────────────────┘
```

**Why this arrangement (the story):**
- **Column A = "why + what"** — judge instantly gets the problem and our 4 contributions.
- **Column B = "how"** — the three architecture diagrams stacked, top-to-bottom = your root→sub-edge flow.
- **Column C = "proof"** — the numbers that back each claim, then impact/business.
- Soil `D4` diagram is **dropped from the poster** (redundant with the real scatter `E_soil_scatter` + your coming tensiometer field photo). Keeps density down. We keep the file for slides.

---

## 3. Per-block spec (exact content + size + color)

### HEADER BAND — green `#1F5132`, 1133 × 132 mm
- **NSU logo** left, ~90 mm tall, 40 mm left inset, vertically centered.
- **Two pills** (top): ochre `#C2792E` `CAPSTONE DESIGN & INNOVATION CHALLENGE 2026`; mid-green `#3E7D4F` `TRACK: AI & AGRI-TECH`. White text, ~26 pt bold.
- **Title** ~72 pt bold, white, with **KrishokChat** in gold `#F0C24E`, 2 lines max:
  *KrishokChat — A Safety-First Bengali Agricultural Advisory System for Smallholder Farmers*
- **Subtitle** ~30 pt, pale `#DCE8D8`, one line:
  *Grounded in Bangladeshi Government Sources · Runs Offline on Mid-Range Phones · Bengali + 6 Dialects*
- **Authors/advisor** ~22 pt, `#B9CDB4`: authors left, advisor+NSU right, same baseline.
- **Ochre rule** 3 mm full width directly beneath band.

### COLUMN A

**A1 — Problem + hero stat** (card `#FBF7EE`, ~366 × 150 mm)
- Header bar (green, ~14 mm) with white text: `THE PROBLEM`
- 3 short lines (ink, ~24 pt): ~47M farming households, little Bengali advisory · generic chatbots hallucinate unsafe pesticide doses · dialect + low-literacy shut most tools out.
- One hero number in ochre: **16123** — the real Krishi Call Center we escalate to.

**A2 — Four contributions** (card, ~366 × 200 mm)
- Header bar: `WHAT WE BUILT`
- Numbered ①–④ (each ~24 pt, number in green circle):
  ① Four-stage safety-verified agent pipeline (safety BEFORE retrieval)
  ② 14-field chemical-dosage claim verifier (fail-closed)
  ③ Two original field datasets: 722 tensiometer soil photos + 1,000 real farmer questions
  ④ 85,979-instance provenance-traced Bengali benchmark (CC-BY-4.0)

**A3 — Grounded-data foundation** (card, ~366 × 250 mm)
- Header bar: `GROUNDED IN BANGLADESH`
- Diagram **`D3_grounded_data.png`**, fit width.
- One caption line: *Every answer traces to a govt source (BARC/BARI/BRRI/DAE) or our own field data — not generic web text.*

### COLUMN B — "HOW IT WORKS" (architecture)

**B1 — Root system flow** (card, ~366 × 250 mm)
- Header bar: `ONE SYSTEM, THREE CAPABILITIES`
- Diagram **`D0_root_system_flow.png`**, largest of the three.

**B2 — Safety pipeline** (card, ~366 × 200 mm)
- Header bar: `SAFETY-FIRST ADVISORY PIPELINE`
- Diagram **`D1_safety_pipeline.png`**.
- Caption: *Unsafe queries stop before the model runs → 16123.* (16123 in red.)

**B3 — Disease routing** (card, ~366 × 155 mm)
- Header bar: `CLASSIFY CROP → ROUTE TO SMALL MODEL`
- Diagram **`D2_disease_vision_routing.png`**.
- Caption: *Tiny per-crop models (6.2 MB) — runs on mid-range phones.*

### COLUMN C — "PROOF IT WORKS"

**C1 — Model beats baselines** (card, ~366 × 175 mm) — native table
- Header bar: `OUR ON-DEVICE MODEL BEATS BIGGER MODELS`
- Table (ours row shaded mid-green tint, bold):
  | Model (Bengali QA) | Token-F1 |
  | **KrishokChat-4B (ours, 4-bit)** | **0.314** |
  | LLaMA-3.1-8B (zero-shot) | 0.165 |
  | Gemini-2.5-Flash-Lite | 0.104 |
  | Gemma-4-26B | 0.087 |
- Callout ochre: **1.9× the best zero-shot** (p≈6.7e-5).

**C2 — Disease accuracy** (card, ~366 × 165 mm) — native table
- Header bar: `CROP DISEASE — REAL FIELD IMAGES`
- Rows: Brassica 97.29 · Rice 96.49 · Corn 97.23 · Potato 95.04 · Wheat 88.00 (Top-1 %).
- Badges: `436/437` grounded Bengali treatment · `<30 ms` on-device.

**C3 — Soil result** (card, ~366 × 175 mm)
- Header bar: `SOIL MOISTURE FROM A PHOTO`
- Image **`E_soil_scatter.png`** left; right: `722 photos`, `R²=0.39`, **`22% error ↓`** vs baseline (ochre).
- *(tensiometer field photo slots here when ready.)*

**C4 — Impact + business** (card, ~366 × 130 mm)
- Header bar: `IMPACT & PATH TO SCALE`
- 3 tight lines: Health (fewer unsafe doses) · Access (offline Android, mid-range phones) · Scale (free farmer app + B2G 16123 + CC-BY-4.0 dataset).

### FOOTER STRIP — green, thin (~full width × 40 mm)
- Refs [1] KrishokChat (EACL '26) · [2] AgriTrust (SIGIR-AP '26) · [3] AgriVision BD.
- CC-BY-4.0 · `HF: RaiyanKhaan/KrishokChat` · red `16123 / 999`.
- Optional: 1–2 QR codes far right (dataset, code).

---

## 4. Diagram re-shaping notes (for GPT regen if needed)

Your D0–D4 came out on **white** backgrounds; on the `#F4EEE1` canvas they'll sit inside
soft-cards `#FBF7EE`, so a faint white edge is acceptable. **Regenerate only if a diagram
looks blurry at print size or a label is garbled.** Aspect targets for the column cards:

| Diagram | Target aspect | Current | Action |
|---|---|---|---|
| D0 root flow | ~4:3 (fits tall B1 card) | 1.82 (wide) | may re-gen taller, or place with side padding |
| D1 safety | ~16:9 wide | 2.0 | fits B2 fine |
| D2 routing | ~4:3 | 1.33 | fits B3 fine |
| D3 grounded | ~16:9 wide | 2.31 | fits A3 fine |
| D4 soil | — | — | **not used on poster** |

Regen prompts live in `DIAGRAM_PROMPTS.md` (STYLE LOCK + per-diagram). If we re-gen, add
to the STYLE LOCK: *"transparent OR very-light warm `#F4EEE1` background"* so diagrams melt
into the canvas instead of showing white rectangles.

---

## 5. Build order (approval gates)

1. **Step 1 — Header band + title** (canvas, wash, green band, logo, title, pills, rule). ← current step
2. **Step 2 — 3-column skeleton** (drop the 3 column guides + all empty header bars, verify breathing room).
3. **Step 3 — Column A** blocks (problem, contributions, D3).
4. **Step 4 — Column B** blocks (D0, D1, D2 + captions).
5. **Step 5 — Column C** blocks (tables, soil, impact).
6. **Step 6 — Footer + QR + final polish** (align, equalize gaps, contrast check).

At each gate you place it, send a note (or screenshot), I adjust wording/sizes to fit.

---

## 7. FROZEN NUMBERS — the only stats allowed on the poster

Copied from `poster_stats.yaml`. **Nothing may be invented, rounded differently, or added.**

**Headline / hero**
- `85,979` benchmark instances · 4 tracks · CC-BY-4.0
- `16123` Krishi Call Center (real, active) · `999` emergency
- `2,882` knowledge-graph nodes (never 2,120) · `19,768` entities · `17,501` triples
- `284` source publications from `13` institutions (BARC, BARI, BRRI, IRRI, DAE, CABI…)
- `6` dialects (Standard + Rajshahi, Sylhet, Chittagong, Barisal, Rangpur)
- `12` safety categories · `~47 million` farming households (context)

**Model (Bengali General QA, token-F1)**
- KrishokChat-4B (ours, Gemma-4-E4B LoRA r=32, 4-bit): **0.314**
- LLaMA-3.1-8B zero-shot: `0.165` · Gemini-2.5-Flash-Lite: `0.104` · Gemma-4-26B: `0.087`
- **1.9×** best zero-shot baseline, p ≈ `6.7e-5`
- Safety compliance violation: `0.31%` (1/323) · chemical hallucination floor across 6 LLMs: `4.05–7.00%`

**Retrieval (Recall@10, 900 answerable of 1,000 queries)**
- Hybrid RRF (ours) **0.539** · BM25 `0.506` · ColBERT `0.487` · Dense `0.464` · BGE-M3 `0.408`
- +9% over dense, p < 0.001 · dense on farmer dialect queries collapses to `0.093`

**Crop disease (top-1 accuracy, classification — never say detection/mAP/boxes)**
- Brassica `97.29%` (11 cls) · Rice `96.49%` (8) · Corn `97.23%` (4) · Potato `95.04%` (3) · Wheat `88.00%` (11)
- Edge: ONNX nano `6.2 MB` (1.1 ms) · TFLite INT8 `1.6 MB` · on-device `<30 ms`
- `436/437` (99.8%) library entries returned grounded Bengali treatment

**Soil moisture (EfficientNet-B0, 5-fold series-stratified OOF, N=693)**
- `722` tensiometer-labeled field photos, Pabna District, `0.0–21.5 kPa`, 6 USDA textures, 14 crops
- R² = `0.39` · RMSE `4.09 kPa` vs `5.26 kPa` mean baseline → **22.1% error reduction**
- Irrigation thresholds: `<10 kPa` adequate · `10–15` monitor · `>15` irrigate

**Datasets / benchmark tracks**
- General QA `28,993` · Treatment QA `11,224` (66.3% chemical-bearing) · Table QA `25,650` · Safety `20,112`
- Farmer benchmark `1,000` queries incl. `300` field interviews (Rajshahi & Natore)

**Verifier**
- `14` claim fields · `6` relation types (supported, contradicted, partially_supported, unsupported, ambiguous, not_applicable) · fail-closed

**BANNED:** end-to-end latency/throughput, mAP/IoU/bounding boxes, invented TAM/revenue,
arXiv:2606.29243, any soil number other than the EffNet OOF set, node count 2,120.

---

## 8. Files (this folder — nothing else)

| File | Purpose |
|---|---|
| `POSTER_MASTER_PLAN.md` | THIS — the only plan. Placement + palette + frozen stats + steps. |
| `FIGMA_PROMPT.md` | Self-contained prompt to generate the poster layout in Figma. |
| `DIAGRAM_PROMPTS.md` | GPT prompts for D0–D4 (regen reference). |
| `poster_stats.yaml` | Verified number source of truth. |
| `example_poster.pdf` | Winner reference (landscape, clean discipline). |
| `figures/` | D0–D4 + E_soil_scatter (D4 unused on poster). |
| `assets/nsu_logo.png` | Header logo. |
