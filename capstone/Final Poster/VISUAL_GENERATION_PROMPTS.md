# KrishokChat Visual Generation Prompts
## What to Generate, What to Code, and Exact Prompts

The handout is small and judges read quickly. Technical diagrams must be deterministic. Image generators are useful for documentary-style visual support, but they are unreliable for Bengali text, exact numbers, arrows, and architecture labels.

## 1. Decision Matrix

| Asset | Best production method | Reason |
|---|---|---|
| Safety architecture | SVG/TikZ/React/HTML-to-SVG | exact labels, arrows, categories, 16123/999 |
| Field-to-research timeline | SVG/TikZ/React | exact sequence and numbers |
| Bengali QA/model chart | Python/Matplotlib or pgfplots | exact metrics and source labels |
| Revenue/value flow | SVG/TikZ/React | exact B2G/B2B/Data labels |
| Product screenshots | existing real screenshots | strongest product evidence |
| Interview/field hero | existing real photograph | authenticity |
| Cover background enhancement | image generation only if needed | atmosphere without technical claims |
| Decorative crop/soil texture | image generation or photography | visual support only |

**Hard rule:** never ask an image model to render the words `KrishokChat`, `16123`, Bengali sentences, metric values, or diagram labels. Add all typography after generation in code/layout software.

---

## 2. Prompt A — Cover Background, Documentary Product Story

Use only if the real field photograph does not provide a strong enough cover. Generate the image without any text, logos, UI, charts, or fake statistics.

### Prompt

```text
Create a realistic documentary-style editorial photograph for a Bangladesh agricultural technology capstone brochure. Show a smallholder farmer in a real green crop field holding a modest Android smartphone at chest height, with the field and crop texture visible. The farmer should look focused and practical, not posed for advertising. Use natural late-afternoon light, authentic rural Bangladesh clothing, realistic soil and foliage, and a restrained warm paper-friendly colour palette with greens, ochres, and natural skin tones. Compose the image vertically with generous quiet negative space on the upper-left side for a title that will be added later. Keep the face and phone fully visible. No text, no logos, no interface, no QR code, no futuristic holograms, no floating UI, no exaggerated lens flare, no generic Western farm, no luxury smartphone, no advertising copy. Editorial documentary photography, realistic proportions, print-ready detail, A4 portrait crop, 4:5 aspect ratio.
```

### Post-processing instruction

Add the title, Bengali subtitle, team, and QR code in the layout tool. Do not let the generated image carry any factual message by itself.

---

## 3. Prompt B — Field Discovery Background / Timeline Texture

Use as a low-contrast background behind the inside-left timeline. Do not use it as evidence instead of the real interview photograph.

### Prompt

```text
Create a realistic, quiet documentary collage background for an agricultural field-research brochure: a close view of a notebook with handwritten interview marks, a farmer’s hand near a crop leaf, a simple feature phone or modest Android phone, and a field path in Bangladesh. The composition must feel like real fieldwork and observation, not a startup advertisement. Use warm off-white paper, muted leaf green, ochre, clay, and charcoal accents. Leave a large clean central area for an overlaid vector timeline. No readable writing, no generated letters, no logos, no statistics, no diagram arrows, no fake app screens, no futuristic technology, no stock-photo smile, no dramatic sky. Flat editorial documentary composition, high detail at the edges, soft low-contrast centre, A3 print background, landscape orientation.
```

### Post-processing instruction

Overlay the exact five timeline stages in SVG. Use the real `researcher_interviewing_farmer.png` wherever possible.

---

## 4. Prompt C — Non-Text Crop and Soil Illustration Set

This is for small decorative spot illustrations only. Generate each object separately so the layout remains modular.

### Prompt

```text
Create a clean editorial botanical illustration of one healthy rice leaf, one leaf with a clearly visible brown spot pattern, a small soil cross-section with roots, and a simple handheld tensiometer dial as separate isolated objects on a transparent or plain warm-paper background. Use natural scientific proportions, restrained dark green, ochre, clay, and charcoal colours, thin ink outlines, and subtle paper texture. No labels, no numbers, no letters, no logos, no background scene, no fantasy glow, no cartoon face, no photorealistic pesticide bottle. The objects must be separated with generous whitespace and suitable for placement in a Bengali agricultural brochure.
```

### Post-processing instruction

Add all disease names, kPa values, and captions manually. Do not imply that the illustration is a model output or field measurement.

---

## 5. Prompt D — Phone-in-Field Product Accent

Use only as a secondary cover accent if the real screenshot strip is not visually strong enough. The screen must be blank; add the real screenshot later.

### Prompt

```text
Create a realistic close-up editorial photograph of a farmer’s hand holding a modest Android phone in a Bangladesh crop field. The phone is shown at a slight angle with a completely blank warm off-white screen so a real product screenshot can be composited later. Show authentic fingerprints and natural hand posture, soft daylight, green crop leaves and brown soil in the background, shallow but not excessive depth of field. No text, no logo, no generated interface, no icons, no fake Bengali words, no futuristic overlay, no premium smartphone branding, no stock-photo styling. Vertical composition, quiet negative space around the phone, print-ready detail, 4:5 aspect ratio.
```

### Post-processing instruction

Composite `03_chat_safety_refusal.png`, `02_chat_grounded.png`, or `04_detect_diagnosis.png` into the blank screen only if the perspective can be matched cleanly. A flat screenshot beside a real photo is safer than a distorted composite.

---

## 6. Prompt E — Abstract Background Texture for the Back Panel

This should remain almost invisible. It is not a business diagram.

### Prompt

```text
Create a subtle seamless warm-paper texture for a serious agricultural technology brochure: off-white handmade paper grain, very faint line impressions inspired by crop rows, soil layers, and notebook rules, using only near-neutral charcoal, muted leaf green, and pale ochre. The texture must remain quiet enough for black body text and small QR codes. No words, no numbers, no logos, no icons, no gradients, no large circles, no decorative blobs, no visible diagram, no high-contrast pattern. Flat A4 portrait background, print-safe, understated editorial design.
```

---

## 7. Negative Prompt for Every Image Request

Append this block to image prompts when supported:

```text
No generated text, no Bengali writing, no English writing, no numbers, no logos, no watermarks, no UI labels, no fake metrics, no arrows, no flowchart, no infographic, no bounding boxes, no pesticide instructions, no chemical dosage, no medical imagery, no futuristic holograms, no generic stock-photo composition, no inaccurate anatomy, no extra fingers, no distorted phone, no unreadable screen.
```

---

## 8. Code-Generated Diagram Specifications

### Diagram 1 — Field-to-product timeline

**Output:** SVG and PDF, 160–180 mm wide, transparent background.

**Nodes:**

1. `LISTEN` — `300 face-to-face interview questions`.
2. `EXPAND` — `1,000 real farmer questions`.
3. `MEASURE` — `baseline failures: grounding, Bengali transfer, safety`.
4. `BUILD EVIDENCE` — `85,979 provenance-traced instances · 284 publications`.
5. `BUILD PRODUCT` — `safety-first chat · crop/disease classification · grounded advisory`.

**Style:** numbered circles, one arrow line, three colours only: leaf for field/data, ochre for research, clay for safety/product decisions. Use no more than 12 words inside any node.

### Diagram 2 — Safety-first application architecture

**Output:** SVG and PDF, 160–180 mm wide, transparent background.

**Required labels:**

- `Farmer query / crop photo`;
- `1 Safety / Router`;
- `2 Retrieval`;
- `Hybrid RRF when available`;
- `BM25 local fallback`;
- `3 Bengali generation`;
- `4 Claim / dosage verification`;
- `STOP before retrieval`;
- `16123 / 999`;
- `sources + trace + local audit`.

**Technical constraint:** show terminal safety categories branching before retrieval. Do not draw a flow that implies unsafe content reaches generation.

### Diagram 3 — Vision classify-then-route

**Output:** SVG and PDF, 150–170 mm wide.

**Nodes:**

```text
phone photo -> image quality -> crop classification -> crop-specific disease classification -> Bengali disease context -> shared grounded advisory path
```

Add a small note: `classification models; no bounding-box claim`.

Use five crop-family pills only if the final artifact registry confirms them. Do not imply that every crop family has a mapped disease model.

### Diagram 4 — Free farmer access to institutional value

**Output:** SVG and PDF, 150–170 mm wide.

**Core:** `Safety + grounded advisory + local audit`.

**Inputs:** `every farmer · free access`.

**Outputs:**

- `B2G · 16123 triage and escalation`;
- `B2B · extension and district analytics`;
- `Data/API · research and agricultural services`.

Add the exact banner: `Nobody pays to remain safe.`

### Diagram 5 — Evidence result tiles

Generate as HTML/SVG or LaTeX, not an image model.

**Tiles:**

- `0.165 -> 0.314` — Bengali general QA token-F1 comparison;
- `4.05–7.00%` — oracle-condition chemical hallucination floor across evaluated systems;
- `12/12` — scoped post-gate golden-probe unanswerable refusals;
- `722` — field RGB soil images paired with tensiometer readings.

Every tile must include a source tag and comparison condition. Do not display a number without its context.

---

## 9. Recommended Technical Tooling

- **SVG/HTML/CSS:** best for brochure diagrams and later editing;
- **Python + Matplotlib:** best for exact metric charts;
- **TikZ/PGFPlots:** best if the final handout remains in LaTeX;
- **Pillow/ImageMagick:** crop, resize, colour-correct, and prepare screenshots;
- **Image generation:** only for text-free visual support.

Do not generate architecture diagrams with a text-to-image model. It will usually create incorrect arrows, misspell Bengali, and invent labels that look plausible at a glance.
