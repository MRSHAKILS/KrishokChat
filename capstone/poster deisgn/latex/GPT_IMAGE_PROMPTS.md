# GPT Image Prompts — for the LaTeX poster (current palette)

These prompts match the **actual poster theme**: white background, deep leaf green,
ochre accent, clay-red reserved for safety. Paste ONE prompt per run. Save outputs to
`latex/img/` under the filename given.

## STYLE LOCK — paste at the top of EVERY prompt

```
Create a clean flat vector infographic diagram for a professional academic poster
(A0 print). Style rules:
- Background: pure white #FFFFFF.
- Palette ONLY: deep leaf green #2F5D3A (primary boxes/arrows), pale green #EDF3EE
  (light fills), ochre #C2793C (accent highlights), clay red #A8542B (safety/stop
  elements ONLY), dark ink #1A1611 (text), light grey #DCE5DE (borders/dividers).
- Flat 2D vector style. No gradients, no shadows, no 3D, no glow, no photos,
  no emoji, no robot or brain icons, no cartoon mascots.
- Rounded rectangles (small corner radius), 2px borders, generous white space.
- Sans-serif font (Lato-like), high contrast, ALL spelling exactly as given —
  do not paraphrase or add words.
- Minimal text: only the exact labels provided. No extra captions.
- Legible when printed ~21 cm wide.
```

---

## PROMPT 1 — FREE vs PREMIUM tiers  ← REQUIRED (replaces placeholder)

Target: **wide landscape 2:1** (request 2000×1000 px). Prints at 212 × 106 mm.
Save as: `img/tiers_free_premium.png`

```
A side-by-side comparison infographic, two large rounded panels of equal size with a
thin gap between them, on a white background.

LEFT PANEL — header bar in deep leaf green #2F5D3A with white bold text "FREE — EVERY FARMER".
Body (pale green #EDF3EE fill, ink text) with 4 short rows, each with a small green
check icon:
- "Grounded answers — no LLM"
- "On-device photo diagnosis"
- "Safety gate + 16123"
- "Works offline"

RIGHT PANEL — header bar in ochre #C2793C with white bold text "PREMIUM — INSTITUTIONS & PRO".
Body (white fill, ink text) with 3 short rows, each with a small ochre star icon:
- "Everything in Free"
- "Open-ended AI advisory"
- "Priority + voice"

BOTTOM BANNER — a full-width rounded bar in clay red #A8542B with white bold text,
spanning under BOTH panels:
"Safety gate & 16123 escalation — identical in both tiers"

Clean flat vector, no gradients, no shadows, white background.
```

**Placement:** Column 5 → `Business Model` block. In `krishokchat-poster.tex`, replace
the whole `\figbox{11.0cm}{FREE vs PREMIUM ...}` placeholder with:
`\includegraphics[width=\linewidth]{tiers_free_premium.png}`

---

## PROMPT 2 — 4-stage safety pipeline  ← OPTIONAL upgrade (currently native TikZ)

Only generate this if you want a prettier hero than the built-in TikZ version. The
TikZ version is already crisp and text-perfect — GPT may mangle small text, so compare
before swapping. Target: **portrait-ish 1:1.05** (request 1400×1470 px). Prints at
~200 × 210 mm.
Save as: `img/architecture_pipeline.png`

```
A vertical flowchart on a white background, read top to bottom.

Nodes (rounded rectangles, deep leaf green #2F5D3A fill, white text, one per row,
connected by thick green downward arrows):
1. Top node, pale green fill #EDF3EE with green border: "FARMER QUERY" with small
   grey subtitle "Bengali · any dialect · text or voice"
2. "1 SAFETY / ROUTER" subtitle "6 categories · fail-closed"
3. "2 HYBRID RETRIEVAL" subtitle "BM25 + dense · RRF · top-5"
4. "3 GENERATION" subtitle "KrishokChat-4B · 4-bit · Bengali"
5. "4 VERIFIER" subtitle "14 fields · 6 relations · fail-closed"
6. Final node, darker green fill: "GROUNDED ANSWER + CITATIONS"

RIGHT SIDE — from node 1, a thick clay red #A8542B arrow branching right into a
red-bordered white box with red bold text: "STOP" and small red lines
"banned chemical / self-harm / injection" then "→ 16123" and "→ 999".

BOTTOM RIGHT — a small dashed green-bordered box: "AUDIT LOG → ANALYTICS" connected
to node 4 by a thin dashed green arrow.

Flat vector, white background, no shadows.
```

**Placement:** Column 4 → `System Architecture` block. Replace the entire
`tikzpicture` environment with `\includegraphics[width=\linewidth]{architecture_pipeline.png}`
(keep the caption line under it).

---

## PROMPT 3 — Classify-then-route vision  ← OPTIONAL regen (replaces D2 PNG)

Current `D2_disease_vision_routing.png` works but uses the older warm-paper palette.
Regenerate only for palette consistency. Target: **4:3 landscape** (1600×1200 px).
Prints at 212 × 159 mm.
Save as: `img/vision_routing.png`

```
A left-to-right flow diagram on a white background.

Left: rounded rectangle with green border, ink text "FARMER PHOTO" with a small
generic leaf-image icon (simple flat leaf shape, green).
Thick green arrow to a second box: "CROP CLASSIFIER" (pale green fill).
Then the flow fans out to FIVE small equal boxes in a vertical stack, each deep
green fill with white text: "Rice", "Brassica", "Corn", "Potato", "Wheat" — each
with tiny grey subtitle "per-crop model".
All five converge with green arrows into a final box on the right, dark green fill,
white bold text: "GROUNDED BENGALI TREATMENT".
One small ochre #C2793C tag attached below the fan: "6 MB models · <30 ms on phone".

Flat vector, white background, no shadows, no extra text.
```

**Placement:** Column 4 → `Vision: Classify, Then Route` block. Replace
`\includegraphics[width=\linewidth]{D2_disease_vision_routing.png}` with
`{vision_routing.png}`.

---

## PROMPT 4 — Grounded data foundation  ← OPTIONAL regen (replaces D3 PNG)

Same rationale as Prompt 3. Target: **wide 2.3:1** (2000×870 px). Prints 212 × 92 mm.
Save as: `img/grounded_data.png`

```
A left-to-right provenance flow diagram on a white background.

FAR LEFT: a vertical stack of six small grey-bordered white boxes, ink text:
"BARC", "BARI", "BRRI", "IRRI", "DAE", "CABI", with a bracket labelled in small
grey text "284 publications · 13 institutions".
Green arrow to CENTER box: deep green fill, white bold text "KNOWLEDGE GRAPH",
small white subtitle "2,882 nodes · 17,501 triples".
Green arrow to RIGHT box: deep green fill, white bold text "BENCHMARK",
small white subtitle "85,979 instances · 4 tracks · CC-BY-4.0".
BELOW the right box, a separate ochre #C2793C-bordered box: "FIELD DATA" with
subtitle "722 soil photos · 1,000 farmer queries", with a short ochre arrow
feeding up into the BENCHMARK box.

Flat vector, white background, generous spacing, no shadows.
```

**Placement:** Column 2 → `Grounded in Bangladesh` block. Replace
`\includegraphics[width=\linewidth]{D3_grounded_data.png}` with `{grounded_data.png}`.

---

## Priority order

1. **Prompt 1 (tiers)** — the only REQUIRED one; a placeholder box is waiting for it.
2. Prompt 2 (architecture) — nice-to-have; TikZ fallback already in place.
3. Prompts 3 & 4 — palette-consistency regens only if time allows.

After generating: drop files into `latex/img/`, tell me, and I swap the references +
recompile + re-audit.
