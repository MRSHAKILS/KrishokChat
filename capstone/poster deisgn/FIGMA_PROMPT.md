# KrishokChat Poster — Figma Prompts

Two prompts. **Prompt A** builds the whole A0 poster layout. **Prompt B** builds the
architecture diagrams as native Figma vectors (replaces the GPT-generated PNGs, so the
diagrams match the poster theme instead of sitting on white rectangles).

Both are **self-contained** — paste the entire block, no extra context needed.
Every number is frozen from `poster_stats.yaml`. Figma must not invent or alter any number.

---
---

# PROMPT A — Full A0 poster layout

> Paste everything below the line into Figma Make / Figma AI.

---

Create a print-ready academic conference poster.

## Canvas
- Frame: **1189 × 841 mm LANDSCAPE** (A0). If mm unavailable use **4494 × 3179 px**.
- Page background: solid warm paper `#F4EEE1` across the ENTIRE frame. No white background anywhere.
- Outer margin: 28 mm on all sides. Gap between blocks: 14 mm.
- Design for viewing from 1.5 m. Body text must never go below 24 pt.

## Palette — use ONLY these colors
| Role | Hex |
|---|---|
| Canvas wash (whole page) | `#F4EEE1` |
| Deep leaf green (primary) | `#1F5132` |
| Mid green (secondary) | `#3E7D4F` |
| Warm ochre (data accent) | `#C2792E` |
| Soft gold (title pop) | `#F0C24E` |
| Alert red (safety ONLY) | `#C0342B` |
| Ink (text) | `#241E17` |
| Soft card | `#FBF7EE` |

## Type
- Headings: **Poppins Bold** (or Plus Jakarta Sans Bold)
- Body: **Inter Regular / Medium**
- Bengali text: **Noto Serif Bengali**
- Section header bars: white text on `#1F5132`, 34 pt bold, uppercase, slight letter-spacing.
- Body: `#241E17`, 24–26 pt. Numbers to emphasise: `#C2792E` bold.

## Design discipline (critical)
- **Low ink density.** Every block must have generous internal padding (min 18 mm) and clear breathing room. Do not fill space. Empty warm-paper space is intentional.
- One cohesive designed piece — NOT floating white boxes on grey. Cards are `#FBF7EE`, barely lighter than the canvas, with a 1 pt `#E3D8C4` border and 8 mm corner radius.
- Use exactly one accent rule style: 3 mm ochre `#C2792E` horizontal line.
- No drop shadows, no gradients, no emoji, no stock icons of robots/brains.

## STRUCTURE

### 1. HEADER BAND
Full-width rectangle, 1189 × 132 mm, at the very top (x=0, y=0), fill `#1F5132`.

Inside it:
- **Logo** placeholder on the left: 90 mm tall image slot, 40 mm left inset, vertically centered. Label it `NSU_LOGO`.
- **Two pills** on the top line right of the logo, 26 pt bold white text, rounded rectangles:
  - Pill 1, fill `#C2792E`: `CAPSTONE DESIGN & INNOVATION CHALLENGE 2026`
  - Pill 2, fill `#3E7D4F`: `TRACK: AI & AGRI-TECH`
- **Main title**, 72 pt Poppins Bold, max 2 lines. Word `KrishokChat` in `#F0C24E`, rest in white `#FFFFFF`:
  `KrishokChat — A Safety-First Bengali Agricultural Advisory System for Smallholder Farmers`
- **Subtitle**, 30 pt, color `#DCE8D8`, one line:
  `Grounded in Bangladeshi Government Sources · Runs Offline on Mid-Range Phones · Bengali + 6 Dialects`
- **Authors line**, 22 pt, color `#B9CDB4`, split left/right on one baseline:
  - Left: `Khan Raiyan Ibne Reza · Sanjana Aktar Maria · Shakil Ahmed`
  - Right: `Advisor: Dr. Sumaiya Tabassum Nimi · ECE · North South University`

Directly beneath the band: full-width 3 mm rule, `#C2792E`.

### 2. BODY — three equal columns
Below the header: three columns, each **365.7 mm** wide, 18 mm column gaps, total body height 667 mm. Columns read left → right.

Every block = soft card `#FBF7EE` with a **green section header bar** across its top (14 mm tall, `#1F5132`, white uppercase text).

---

#### COLUMN A — "why + what"

**A1 · header bar `THE PROBLEM`** (card ≈ 366 × 150 mm)
Three body lines, 24 pt:
- `~47 million farming households in Bangladesh, almost no Bengali-language advisory.`
- `Generic chatbots hallucinate unsafe pesticide doses — measured 4.05–7.00% chemical hallucination across 6 LLMs.`
- `Dialect and low literacy lock most farmers out of existing tools.`

Then one hero number, right-aligned, `#C2792E`, 60 pt bold with 22 pt caption beneath:
`16123` / caption `Krishi Call Center — the real national helpline we escalate to`

**A2 · header bar `WHAT WE BUILT`** (card ≈ 366 × 200 mm)
Four numbered items. Each number in a filled `#1F5132` circle (white numeral), text 24 pt ink:
1. `Four-stage safety-verified agent pipeline — unsafe queries stop BEFORE any retrieval runs.`
2. `14-field chemical-dosage claim verifier with 6 relation types, fail-closed on missing evidence.`
3. `Two original field datasets: 722 tensiometer-labeled soil photos (Pabna) + 1,000-query farmer benchmark (300 field interviews).`
4. `85,979-instance provenance-traced Bengali benchmark across 4 tracks, released CC-BY-4.0.`

**A3 · header bar `GROUNDED IN BANGLADESH`** (card ≈ 366 × 250 mm)
- Image slot, full card width, labeled `D3_grounded_data`.
- Caption beneath, 22 pt italic ink: `Every answer traces to a government source (BARC · BARI · BRRI · IRRI · DAE · CABI) or our own field data — not generic web text.`
- Small inline stat strip, 24 pt, numbers in `#C2792E`: `2,882 KG nodes · 19,768 entities · 17,501 triples · 284 publications · 13 institutions`

---

#### COLUMN B — "how it works" (architecture)

**B1 · header bar `ONE SYSTEM, THREE CAPABILITIES`** (card ≈ 366 × 250 mm)
- Largest image slot, labeled `D0_root_system_flow`.
- Caption 22 pt: `Bengali advisory · crop-disease diagnosis · soil-moisture estimation, on one grounded data foundation.`

**B2 · header bar `SAFETY-FIRST ADVISORY PIPELINE`** (card ≈ 366 × 200 mm)
- Image slot labeled `D1_safety_pipeline`.
- Caption 22 pt with `16123` in `#C0342B` bold: `Unsafe queries stop before the model runs → 16123. Six safety categories, fail-closed, every decision written to a local audit log.`

**B3 · header bar `CLASSIFY CROP → ROUTE TO SMALL MODEL`** (card ≈ 366 × 155 mm)
- Image slot labeled `D2_disease_vision_routing`.
- Caption 22 pt: `Tiny per-crop models — 6.2 MB ONNX, 1.6 MB TFLite INT8, under 30 ms on-device.`

---

#### COLUMN C — "proof it works"

**C1 · header bar `OUR ON-DEVICE MODEL BEATS BIGGER MODELS`** (card ≈ 366 × 175 mm)
Native table, 2 columns, 24 pt. Header row fill `#1F5132` white text. **Our row** fill `#E4EEE3`, bold, left edge marked with a 3 mm `#C2792E` bar:

| Model (Bengali QA) | Token-F1 |
|---|---|
| **KrishokChat-4B (ours, 4-bit, on-device)** | **0.314** |
| LLaMA-3.1-8B (zero-shot) | 0.165 |
| Gemini-2.5-Flash-Lite | 0.104 |
| Gemma-4-26B | 0.087 |

Callout beneath, `#C2792E` bold 28 pt: `1.9× the best zero-shot baseline (p ≈ 6.7e-5)`
Small line, 22 pt: `Safety compliance violation: 0.31% (1 of 323 tests).`

**C2 · header bar `CROP DISEASE — REAL FIELD IMAGES`** (card ≈ 366 × 165 mm)
Native table, 24 pt, same header styling:

| Crop | Classes | Top-1 |
|---|---|---|
| Brassica | 11 | 97.29% |
| Corn | 4 | 97.23% |
| Rice | 8 | 96.49% |
| Potato | 3 | 95.04% |
| Wheat | 11 | 88.00% |

Two badges below, rounded, fill `#3E7D4F`, white 22 pt: `436/437 grounded Bengali treatments (99.8%)` and `<30 ms on-device`.
IMPORTANT: label this **classification top-1 accuracy**. Never write detection, mAP, IoU, or bounding boxes.

**C3 · header bar `SOIL MOISTURE FROM A PHOTO`** (card ≈ 366 × 175 mm)
Two-part row: left 55% = image slot labeled `E_soil_scatter`; right 45% = stacked stats, numbers `#C2792E` bold 34 pt with 20 pt labels:
- `722` photos, Pabna District
- `R² = 0.39` · `RMSE 4.09 kPa`
- `22% error reduction` vs mean baseline (5.26 kPa)

Caption 20 pt: `EfficientNet-B0, 5-fold series-stratified out-of-fold, N=693. Irrigation guide: <10 kPa adequate · 10–15 monitor · >15 kPa irrigate.`

**C4 · header bar `IMPACT & PATH TO SCALE`** (card ≈ 366 × 130 mm)
Three tight lines, 24 pt, each starting with a bold `#1F5132` keyword:
- `Health — refusing unsafe agrochemical queries and verifying dosages cuts pesticide misuse and accidental poisoning.`
- `Access — offline-capable Android edge models reach households in the connectivity gap.`
- `Scale — free farmer app · B2G AI front-end to 16123 (92,094 calls FY25-26) · CC-BY-4.0 dataset licensing.`

---

### 3. FOOTER STRIP
Full-width rectangle at the very bottom, 40 mm tall, fill `#1F5132`. White/pale 20 pt text in one row, three groups:
- Left: `[1] KrishokChat — EACL 2026 (under review)   [2] AgriTrust — SIGIR-AP 2026 (under review)   [3] AgriVision BD — Project Report 2026`
- Middle: `Dataset & code released CC-BY-4.0 · HF: RaiyanKhaan/KrishokChat-Advisory-System`
- Right: two 40 × 40 mm QR placeholders labeled `QR_DATASET` and `QR_CODE`, plus `Helplines 16123 / 999` with the numbers in `#F0C24E`.

## Hard constraints
- Do NOT invent any statistic. Use only the numbers written above.
- Do NOT add: end-to-end latency, throughput, mAP, IoU, bounding boxes, market size, revenue projections, or any arXiv ID.
- Do NOT use the words: groundbreaking, revolutionary, cutting-edge, state-of-the-art, comprehensive, robust, seamless, leverage, empower, transform, AI-powered, next-generation. No emoji.
- Never label anything a "limitation" — ongoing work is `Roadmap`.
- Keep all five image slots as clearly named empty placeholders so images can be dropped in.

---
---

# PROMPT B — Architecture diagrams as native Figma vectors

Generate these **one at a time**. Paste the STYLE LOCK plus one diagram block.

## STYLE LOCK (include with every diagram)

---
Create a clean flat vector diagram for a printed academic poster. Style rules:
- Background: **transparent**, or if a fill is required, warm paper `#F4EEE1` (never white).
- Flat 2D only. No 3D, no gradients, no drop shadows, no glow, no photo textures, no emoji, no cartoon mascots, no robot or brain icons.
- Palette ONLY: deep green `#1F5132`, mid green `#3E7D4F`, ochre `#C2792E`, alert red `#C0342B`, ink `#241E17`, soft card `#FBF7EE`, border `#E3D8C4`.
- Boxes: 8 px corner radius, 2 px border, label inside. Arrows: 3 px solid with clean triangular heads; ochre for the main path, red only for safety stops.
- Font: Inter / Poppins, sans-serif, high contrast. Labels must be short and spelled EXACTLY as given — do not paraphrase, translate, or add words.
- Few words. Legible when printed at roughly 360 mm wide.
- Reproduce every number exactly as written. Invent nothing.
---

## D0 — Root system flow (Column B1, target ratio ~4:3, portrait-ish)
One shared foundation at the bottom feeding three capability branches above it.

- Bottom foundation bar, fill `#1F5132`, white text: `GROUNDED DATA FOUNDATION`, with a smaller line beneath inside the same bar: `2,882 KG nodes · 284 publications · 13 institutions (BARC, BARI, BRRI, IRRI, DAE)`
- Three ochre arrows rising from the foundation into three equal cards side by side:
  1. `BENGALI ADVISORY` — sub-labels: `Hybrid retrieval → KrishokChat-4B → verifier`, `Token-F1 0.314`
  2. `CROP DISEASE` — sub-labels: `Photo → crop classifier → per-crop model`, `95–97% top-1`
  3. `SOIL MOISTURE` — sub-labels: `Field photo → EfficientNet-B0`, `R² 0.39 · 22% error ↓`
- Above the three cards, one wide receiving bar, fill `#3E7D4F`, white text: `ONE BENGALI INTERFACE · 6 DIALECTS · OFFLINE-CAPABLE ANDROID`
- Small ochre tag attached to the advisory card: `Safety checked BEFORE retrieval`

## D1 — Safety-first advisory pipeline (Column B2, target ratio ~16:9 wide)
A left-to-right four-stage pipeline with an early exit.

- Stage boxes in order, each numbered: `1 SAFETY / ROUTER`, `2 RETRIEVAL`, `3 GENERATION`, `4 VERIFIER`
- Sub-label under each: stage 1 `6 categories · fail-closed`; stage 2 `BM25 + dense, RRF fusion, top-5`; stage 3 `KrishokChat-4B, 4-bit, streamed Bengali`; stage 4 `14 fields · 6 relations`
- Output box on the far right, green: `GROUNDED BENGALI ANSWER + SOURCES`
- **Red early-exit branch** from stage 1 dropping downward to a red-bordered box: `UNSAFE → STOP` with sub-lines `Banned chemical · self-harm risk · prompt injection` and `→ 16123 Krishi Call Center · 999 emergency`. Make it visually obvious this exit happens before stage 2.
- Small ochre note under stage 4: `Missing evidence → abstain`
- Small grey box beneath the whole row: `Every decision → local audit log (JSONL) → analytics dashboard`

## D2 — Classify crop, then route (Column B3, target ratio ~4:3)
- Left: box `FARMER PHOTO`
- Arrow into: box `CROP CLASSIFIER`
- Then a fan-out of five small labeled boxes: `Rice`, `Brassica`, `Corn`, `Potato`, `Wheat`, each with its own tiny sub-label `per-crop model`
- All five converge with arrows into a green output box: `GROUNDED BENGALI TREATMENT` with sub-line `436/437 library entries (99.8%)`
- Ochre side tag: `6.2 MB ONNX · 1.6 MB TFLite INT8 · <30 ms on-device`

## D3 — Grounded data foundation (Column A3, target ratio ~16:9 wide)
Left-to-right provenance flow.

- Left column, stacked small boxes labeled: `BARC`, `BARI`, `BRRI`, `IRRI`, `DAE`, `CABI Plantwise`, with a bracket label `284 publications · 13 institutions`
- Arrow into middle box: `KNOWLEDGE GRAPH` with sub-lines `2,882 nodes`, `19,768 entities`, `17,501 factual triples`
- Arrow into right box: `BENCHMARK — 85,979 instances, CC-BY-4.0` with four sub-lines: `General QA 28,993`, `Treatment QA 11,224 (66.3% chemical-bearing)`, `Table QA 25,650`, `Safety 20,112`
- Below the benchmark box, a separate ochre-bordered box: `OUR OWN FIELD DATA` with sub-lines `722 tensiometer soil photos (Pabna)` and `1,000 farmer queries (300 field interviews, Rajshahi & Natore)`, arrow feeding up into the benchmark box.

## Not needed
`D4_soil_field` is not used on the poster (the real scatter plot `E_soil_scatter` covers it). Skip it.
