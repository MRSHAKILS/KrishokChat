# KrishokChat Poster — Architecture Diagram Pack (GPT image prompts)

Generate each diagram **one at a time** (one prompt = one image). Do **not** ask GPT
to draw everything in a single run — it goes blurry and invents wrong labels. Paste the
**STYLE LOCK** block at the top of every prompt so all diagrams look like one family
when you place them side by side in Canva.

Numbers here are copied from `poster_stats.yaml` (verified). Do not let GPT change them.

---

## 0. How the diagrams sit on the poster

Placement is defined in **`POSTER_MASTER_PLAN.md`** (the only plan). Summary:

The poster is **landscape A0, 3 columns**. Diagrams live in the middle/left columns:

| Poster block | Diagram | File |
|---|---|---|
| Column B — B1 root flow (largest) | Root system flow | `D0_root_system_flow.png` |
| Column B — B2 | Safety-verified QA pipeline | `D1_safety_pipeline.png` |
| Column B — B3 | Classify-then-route disease vision | `D2_disease_vision_routing.png` |
| Column A — A3 foundation | Bangladesh-grounded data | `D3_grounded_data.png` |
| (not on poster) | Soil tensiometer field→model | `D4_soil_field.png` — slides only |
| Column C — C3 | Real soil scatter (not GPT) | `E_soil_scatter.png` |

Evidence (model table, disease table, soil callout, impact) is **native Canva text/tables**,
not generated images. Keep each diagram sparse — the numbers live in Column C.

> If regenerating for the warm-paper theme, add to the STYLE LOCK:
> *"transparent OR very-light warm #F4EEE1 background"* so diagrams melt into the canvas
> instead of showing a white rectangle.

Generate **one diagram per run** — combining makes GPT blur text and invent labels.

---

## STYLE LOCK (paste at the top of EVERY prompt below)

```
STYLE: Flat 2D vector infographic, modern technical diagram. Clean, minimal, lots of
white space. White background (#FFFFFF). Rounded-rectangle nodes with 1px solid borders,
thin flat arrows/connectors, no 3D, no drop shadows, no gradients, no glow, no clip-art,
no photos. Sans-serif labels only, crisp and perfectly legible, spelled EXACTLY as given
(do not invent or paraphrase any text). Landscape orientation.

COLOR PALETTE (use only these):
- Emerald #059669  (primary / "safe" / our system)
- Amber   #D97706  (data / measurement)
- Crimson #DC2626  (safety escalation / stop)
- Sky     #0284C7  (retrieval / info)
- Ink     #0F172A  (text + dark boxes)
- Paper   #F8FAFC  (subtle fills)

Only render the nodes, arrows, and labels I specify. Do NOT add extra boxes, icons,
legends, logos, or decorative text. High resolution, print-quality, sharp edges.
```

---

## Diagram 0 — ROOT SYSTEM FLOW (hero, full-width)  ▶ aspect 16:9

> **This is the "root flow" the user asked for: one entry, three specialised sub-edges,
> all standing on one grounded foundation.**

```
[PASTE STYLE LOCK]

Draw a left-to-right system flow diagram titled "KrishokChat — one grounded system,
three farmer capabilities".

LEFT (single entry node, ink #0F172A fill, white text):
  "Bangladeshi farmer" with two small tags under it: "Web app" and "Android app".
  Below the entry, a small caption: "Bengali + 6 regional dialects".

CENTER (one arrow from the entry splits into THREE parallel capability lanes,
each a rounded rectangle with an emerald #059669 header bar):

  LANE 1 — "Bengali Q&A Advisory"
     subtitle: "4-stage safety-verified pipeline"
  LANE 2 — "Crop Disease Vision"
     subtitle: "classify crop → route to a small per-crop model"
  LANE 3 — "Soil Moisture Advisory"
     subtitle: "field tensiometer data → irrigation guidance"

BOTTOM (a single wide foundation bar spanning under all three lanes,
amber #D97706 header, paper #F8FAFC body). Label it:
  "Grounded in Bangladesh: government agronomy sources (BARC, BARI, BRRI, DAE) +
   own field data (722 tensiometer soil photos, 1,000 real farmer questions)".
  Draw three thin arrows going DOWN from each lane into this foundation bar to show
  every capability rests on the same grounded knowledge base.

RIGHT (one output node, emerald border):
  "Verified Bengali answer + source citations + safety audit log".
  Arrows from all three lanes converge into this output node.

Keep exactly these nodes. No extra icons.
```

---

## Diagram 1 — SAFETY-VERIFIED QA PIPELINE (sub-edge of Lane 1)  ▶ aspect 4:3

```
[PASTE STYLE LOCK]

Draw a left-to-right 4-stage pipeline titled "Safety-first advisory pipeline".
Four rounded-rectangle stages connected by arrows, numbered 1–4:

  1  "Safety Router"     (emerald)  caption: "classify BEFORE any retrieval"
  2  "Hybrid Retrieval"  (sky)      caption: "BM25 + dense (RRF) over govt sources"
  3  "Generation"        (emerald)  caption: "KrishokChat-4B (on-device Gemma-4 4-bit)"
  4  "Claim Verifier"    (emerald)  caption: "14-field dosage check, 6 relations"

From stage 1, draw ONE red #DC2626 branch arrow pointing DOWN to a red node:
  "Unsafe / self-harm / banned chemical → stop, escalate to Krishi Call Center 16123
   (retrieval, generation, verifier all bypassed)".

After stage 4, one arrow to a final emerald-bordered node:
  "Grounded Bengali advisory + citations".
Under stage 4 a small ink node: "every decision logged to local audit trail".

Exactly these nodes. No extra boxes.
```

**Why this matters (poster caption, ≤20 words):** *Unsafe queries are stopped before the
model ever runs — safety is a gate, not an afterthought.*

---

## Diagram 2 — CLASSIFY-THEN-ROUTE DISEASE VISION (sub-edge of Lane 2)  ▶ aspect 4:3

> **The user's priority: crop is classified first, then routed to a smaller specialised
> model — efficient enough for mid-range / low-end phones.**

```
[PASTE STYLE LOCK]

Draw a top-to-bottom routing diagram titled "Classify the crop first, then route to a
small specialised model".

TOP: input node (ink) "Leaf photo from phone camera".
Arrow down to:
  "Crop Classifier" (emerald)  caption: "lightweight — identifies the crop".

From the Crop Classifier, draw a fan-out of arrows to a ROW of five small
rounded-rectangle model nodes (emerald border, small), each labelled:
  "Rice model"     under-text "ONNX nano · 6.2 MB · 1.1 ms"
  "Brassica model" under-text "ONNX · 21.8 MB"
  "Corn model"     under-text "ONNX · 21.8 MB"
  "Potato model"   under-text "TFLite INT8 · 1.6 MB"
  "Wheat model"    under-text "ONNX"

Below the five models, one merge arrow into an emerald-bordered output node:
  "Disease name → grounded Bengali treatment (from govt sources)".

At the bottom, a thin amber #D97706 caption bar:
  "Runs on-device, under 30 ms — built for mid-range phones, works offline".

Exactly these nodes. Do not invent disease names or accuracy numbers here.
```

**Why this matters (caption ≤20 words):** *One small router picks the crop, then a tiny
per-crop model runs — no giant model, so it fits a mid-range phone.*

---

## Diagram 3 — BANGLADESH-GROUNDED DATA FOUNDATION (sub-edge / foundation)  ▶ aspect 4:3

```
[PASTE STYLE LOCK]

Draw a left-to-right "grounding" diagram titled "Grounded in Bangladesh".

LEFT column, three stacked source nodes (amber #D97706 border):
  "Govt agronomy sources"  under-text "BARC · BARI · BRRI · DAE — 284 publications, 13 institutions"
  "Own field soil data"    under-text "722 tensiometer photos, Pabna district"
  "Real farmer questions"  under-text "1,000 queries, 300 field interviews"

All three arrow into a CENTER node (emerald #059669, larger):
  "Provenance-traced knowledge base"
  under-text "2,882 knowledge nodes · every answer traceable to a source".

From the center, one arrow RIGHT to an ink node:
  "85,979-instance public benchmark (CC-BY-4.0), 4 tracks, 6 dialects".

Exactly these nodes. No extra icons.
```

**Why this matters (caption ≤20 words):** *Every answer traces back to a real Bangladeshi
government source or our own field data — not generic web text.*

---

## Diagram 4 — SOIL TENSIOMETER FIELD → MODEL (optional inset)  ▶ aspect 3:2

> Use this only if there's room. Otherwise just place the real tensiometer-in-field
> photo (coming) next to the existing soil scatter figure.

```
[PASTE STYLE LOCK]

Draw a simple 3-step left-to-right flow titled "From the field to an irrigation call".

  STEP 1 (amber): "Tensiometer reading in the field" under-text "0–21.5 kPa, Pabna, 6 soil textures"
  STEP 2 (emerald): "EfficientNet-B0 model" under-text "predicts soil moisture from the photo"
  STEP 3 (ink → colour-coded): "Irrigation advice" showing three small stacked chips:
        green "< 10 kPa: adequate"
        amber "10–15 kPa: monitor"
        red   "> 15 kPa: irrigate now"

Exactly these three steps plus the three advice chips. No extra boxes.
```

---

## Generation tips (so GPT doesn't hallucinate)

1. **One diagram per run.** Never combine. Regenerate a single diagram if one label is wrong.
2. **If a label comes out garbled**, re-run with: *"Re-draw identical layout; fix the text
   so it reads exactly: <paste the exact label>."* Image models often need 2–3 tries for clean text.
3. **Keep counts small.** Each of these has ≤7 nodes on purpose — that's the sweet spot for legible AI diagrams.
4. **Consistency:** the STYLE LOCK palette + "flat vector, white background" keeps all five
   looking like one set in Canva. Place them on a white poster background with the same 1px card borders.
5. **Numbers are frozen.** Anything not in these prompts (accuracies, F1, etc.) belongs in
   the stats half as text/tables — don't let the image model render those numbers.

---

## The EVIDENCE half — data that stays as text/tables (NOT GPT)

These are the "second half, side by side" facts. Render as clean tables/charts in the
poster (most already exist in `poster.html`). Listed here so you can lay them out beside
the diagrams.

### KrishokChat-4B beats the baselines (General QA, token-F1) — the headline table

| Model | Token-F1 | Note |
|---|---|---|
| **KrishokChat-4B (ours, on-device 4-bit)** | **0.314** | fine-tuned, Bengali agri |
| LLaMA-3.1-8B (zero-shot) | 0.165 | larger, general |
| Gemini-2.5-Flash-Lite | 0.104 | hosted API |
| Gemma-4-26B | 0.087 | much larger base |

Callout: **1.9× over the best zero-shot baseline** (p ≈ 6.7e-5). Our small on-device
model beats far larger and hosted models on Bengali agriculture.

### Retrieval (Recall@10, 900 answerable queries)
Hybrid RRF **0.539** · BM25 0.506 · ColBERT 0.487 · Dense 0.464 · BGE-M3 0.408.
Callout: hybrid +9% over dense (p < 0.001); generic dense retrieval collapses on farmer
dialect queries (0.093) — grounding + lexical matters for Bangla.

### Crop disease (top-1 accuracy)
Brassica 97.29% · Rice 96.49% · Corn 97.23% · Potato 95.04% · Wheat 88.00%.
Live library coverage: 436/437 (99.8%) returned grounded Bengali treatment.

### Soil moisture (EfficientNet-B0, 5-fold OOF, N=693)
R² = 0.39 · RMSE 4.09 kPa vs 5.26 kPa mean baseline → **22.1% error reduction**.

---

## What we published (novelty anchor — put near the diagrams)

- **Paper 1 — KrishokChat (EACL 2026, under review):** the 85,979-instance
  provenance-traced Bengali agri benchmark + safety-critical chemical advisory. This is
  the *dataset & benchmark* contribution (its own paper).
- **Paper 2 — AgriTrust (SIGIR-AP 2026, under review):** the structured claim-grounding
  verifier (14 fields, 6 relations) — the *safety verification* contribution.
- **AgriVision BD (project report):** the classify-then-route edge disease vision.

Framing line for the poster: *"Others have built agri chatbots. Ours is grounded to
Bangladeshi government sources, verified for chemical-dosage safety, and small enough to
run on a mid-range phone in Bengali and its dialects — and every layer is backed by a
published dataset or paper."*
```
