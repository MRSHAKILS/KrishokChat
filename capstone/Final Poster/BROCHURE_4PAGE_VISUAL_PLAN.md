# KrishokChat Judge Handout
## Four-Page Double-Sided Visual Plan

**Recommended production format:** one A3 landscape sheet, printed double-sided, folded once to A4 portrait panels. This creates four readable A4 pages and avoids asking judges to handle a long booklet.

**Target reading time:** 90 seconds for a fast scan; 3 minutes for a careful read after the live demo.

**Purpose:** the handout is a visual memory aid for the 3–4 minute presentation. It is not a paper summary, a technical manual, or a second poster.

**Story spine:**

```text
We listened to farmers
        -> found a capacity and trust gap
        -> measured why generic AI fails
        -> built the evidence and retrieval foundation
        -> built a safety-first multimodal product
        -> defined a supervised market entry
```

---

## 1. Physical Format and Folding

### Recommended print

- Sheet: A3 landscape, 420 x 297 mm.
- Finished panels: A4 portrait, 210 x 297 mm.
- Fold: one vertical fold at the centre.
- Bleed: follow the print vendor’s specification; use at least 3 mm if no specification exists.
- Safe area: keep text and QR codes away from fold and trim edges.
- Paper: matte or silk, 150–200 gsm; avoid high-gloss paper because judges will read under exhibition lighting.
- QR codes: minimum 28–30 mm square with quiet zone; test from the printed sheet.

### Panel order

**Outside of the sheet, left to right:**

1. Back cover / next step.
2. Front cover.

**Inside of the sheet, left to right:**

3. The real story: field discovery to research.
4. The product: safety, vision, proof, and market path.

The exact imposition may be changed by the print vendor, but the finished folded object must open from the cover into the chronological inside spread.

---

## 2. Design Rule: One Panel, One Question

Each panel must answer one judge question immediately:

| Panel | Judge question | Main visual |
|---|---|---|
| Front cover | What is KrishokChat? | product promise + farmer/phone image |
| Inside left | Why did you build it? | field-to-research timeline |
| Inside right | How does it work and why trust it? | three live flows + safety architecture |
| Back cover | Can it become a real service? | institutional business model + pilot path |

Do not place a full architecture, full benchmark, full market model, and four screenshots on the same panel. The poster already carries the broad overview; the handout should make the causal story easier to remember.

---

## 3. Panel 1 — Front Cover

### Primary message

> **KrishokChat**  
> Bengali agricultural advice built from farmer questions, Bangladesh-focused evidence, and safety-first AI.

### Supporting line

> **Listen to the field. Ground the answer. Protect the farmer.**

### Visual composition

Use a real field/interview photograph as the dominant image. Place a narrow phone screenshot strip over the image or along its edge containing three tiny states:

1. Bengali question;
2. safety refusal;
3. crop-photo diagnosis.

Do not use a generic AI-generated farmer image if the real field photograph is available. The cover should feel like a product born from fieldwork, not a stock technology advertisement.

### Four small cover anchors

- `300` face-to-face farmer-interview questions;
- `85,979` provenance-traced benchmark instances;
- safety before retrieval;
- free farmer access with institutional deployment path.

Do not put all model metrics on the cover.

### Footer

- team and institution names;
- project version/date;
- one QR code labelled `Try the working system`;
- small text: `Capstone project · Bengali agricultural advisory`.

---

## 4. Panel 2 — Inside Left: The Real Story

### Panel title

> **We started with farmers, not models.**

### Visual centerpiece: five-step timeline

Use a large, simple timeline occupying the upper 60% of the panel:

```text
[1] Listen
300 face-to-face interview questions
        |
[2] Expand
1,000 real farmer questions from interviews + online farmer sources
        |
[3] Measure
Baseline models showed weak Bengali transfer and chemical-risk failures
        |
[4] Build evidence
85,979 provenance-traced instances + 284 official publications
        |
[5] Build the product
Safety-first chat + crop/disease classification + grounded advisory
```

Use numbered circles and one short sentence per step. No paragraph longer than 35 words.

### Middle visual: “Why generic AI was not enough”

Create three large result tiles:

**Tile A — Grounding problem**

`4.05–7.00%`  
Chemical hallucination remained under oracle evidence in the evaluated model set.

**Tile B — Bengali model result**

`0.165 -> 0.314 token-F1`  
Best listed zero-shot baseline versus KrishokChat-4B on the stated general-QA comparison.

**Tile C — Safety problem**

`0.31%`  
Standalone fine-tuned model’s tested safety-compliance rate; this is why safety became an external application boundary.

Each tile must carry a tiny evidence tag: `paper result` or `benchmark result`. Do not imply these are full-application safety metrics.

### Lower visual: research asset strip

Use four small icons or documentary thumbnails:

1. official publications → provenance-traced knowledge;
2. farmer language → real-world benchmark;
3. soil photograph + tensiometer → field dataset;
4. retrieval channels → hybrid + local fallback.

Caption:

> **The research did not sit beside the product. It determined the product’s boundaries.**

### Exact panel copy

> Farmers describe what they see: yellow leaves, spots, wilting, insects, or water stress. Official publications describe crops and interventions in a different register. Our work connects those two worlds while keeping the evidence and safety decision visible.

### What this panel earns

- Idea/novelty: field-first problem discovery;
- social impact: farmer access and safety need;
- research credibility: baseline results caused concrete design changes.

---

## 5. Panel 3 — Inside Right: The Working Product

### Panel title

> **From farmer input to a controlled advisory path**

This panel is the live-demo companion. It must let a judge understand the three screens while the team demonstrates them.

### Top half: central safety architecture

Use a clean, code-generated diagram occupying approximately 45% of the panel:

```text
Farmer question or crop photo
              |
              v
      [1 Safety / Router]
              |
    +---------+----------+
    |                    |
 safe_agri          terminal / risky
    |                    |
    v                    v
[2 Retrieval]       STOP + referral
hybrid RRF          16123 / 999
BM25 fallback
    |
    v
[3 Generation]
Bengali answer
    |
    v
[4 Verifier]
    |
    v
answer + sources + trace + audit
```

### Architecture caption

> **A risky query is stopped before retrieval. A safe query must pass through evidence retrieval, generation, verification, and local audit.**

### Bottom half: three compact live-demo modules

Use three horizontal modules or a three-column strip, each with one screenshot and one sentence.

#### Module 1 — Safety refusal

Screenshot: `demo-assets/screenshots/03_chat_safety_refusal.png`

Caption:

> `প্যারাকোয়াট দিয়ে কীভাবে স্প্রে করব?` → retrieval and generation skipped → `১৬১২৩`

#### Module 2 — Grounded chat

Screenshot: `demo-assets/screenshots/02_chat_grounded.png`

Caption:

> Bengali question → Bangladesh-focused sources → streamed answer → verifier result.

#### Module 3 — Photo advisory

Screenshot: `demo-assets/screenshots/04_detect_diagnosis.png`

Caption:

> image quality → crop/disease classification → grounded Bengali advisory.

Required wording beneath the module:

> **Vision models classify; the advisory path supplies the treatment context.**

### Small proof rail

Place three compact numbers below the modules:

- `95–97%` selected crop top-1 results, with task/context named;
- `<30 ms` edge inference claim only with the verified device context;
- `436/437` Bengali disease-information returns in the live library matrix.

Do not put `6 MB` beside every model. Use the actual model-size range if the final evidence packet supports it, or omit the size from the handout.

### What this panel earns

- Idea/novelty: controlled pipeline and multimodal routing;
- poster/UI: the live screens are easy to connect to the presentation;
- social impact: unsafe advice is redirected to a real help channel;
- market readiness: lightweight field-oriented product experience.

---

## 6. Panel 4 — Back Cover: Market and Next Step

### Panel title

> **Free for farmers. Built to serve institutions.**

### Top visual: value and revenue flow

```text
Every farmer
free Bengali advisory + diagnosis
              |
              v
 Safety + grounded advisory + local audit
       /              |              \
     B2G             B2B           Data/API
  16123 triage   extension and    research, agri-fintech,
  and escalation district insight   insurance, integrations
```

Add a banner:

> **Nobody pays to remain safe. The safety boundary is shared across access tiers.**

### Three revenue lanes, one sentence each

**B2G — Government and extension**  
AI triage in front of the 16123 service: answer routine, grounded questions and escalate uncertain or high-risk cases with an audit trail.

**B2B — Agro-business and NGO partners**  
Advisory, branded channels, and district-level analytics for extension teams, agro-dealers, seed companies, and NGOs.

**Data/API — Research and agricultural services**  
Provenance-traced benchmark resources, field datasets, and a grounded advisory API for approved integrations.

### Middle visual: “What is ready for a supervised pilot?”

Use a checklist with green markers:

- web application and Android-oriented workflow;
- safety-before-retrieval contract;
- precomputed retrieval assets;
- local audit and analytics;
- crop/disease classification workflow;
- production start/readiness path.

Next-step arrows in ochre:

- one district extension-office pilot;
- expert review of flagged and escalated answers;
- corpus licensing and governance;
- device/field validation;
- voice/IVR and dialect expansion.

Do not call this a limitations section. Call it `Pilot path`.

### Bottom economics callout

> **Planning economics:** approximately `0.02 BDT` per model answer under the stated API-token assumption. Start with a low-fixed-cost hosted lane; move to local self-hosting as volume and concurrency justify it.

Do not print an unsupported revenue projection or a guaranteed GPU capacity number without the provider/date/throughput assumptions beside it.

### Closing statement

> **The first customer is not an individual farmer. The first customer is the organization that needs to serve many farmers safely.**

### Footer

- QR: try app;
- QR: code;
- QR: dataset;
- QR: research/reference page;
- team/advisor/contact.

---

## 7. What Must Not Be Added

- no full literature review;
- no 14-field table with all field names in tiny type;
- no full 85,979-row dataset breakdown;
- no soil regression chart unless the final evidence packet explicitly approves it;
- no claim that the model or current product is “100% safe”;
- no “object detection,” bounding boxes, mAP, or IoU;
- no claim that all unsupported questions are automatically rejected;
- no claim that independent water, yield, health, or trust outcomes have already been measured;
- no deprecated paper identifier or unapproved public paper link;
- no crowded business-model pricing cards.

---

## 8. Production Sequence

### Step 1 — Freeze the evidence

Approve one number set for the handout. Each number gets one home; do not repeat it in every panel.

### Step 2 — Prepare the code diagrams

Generate the safety architecture and revenue flow in SVG/PDF using code or LaTeX. Generate the charts from a small data file so labels cannot be hallucinated.

### Step 3 — Prepare the real screenshots

Use the existing screenshots listed above. Re-capture only if the current UI differs from the final demo.

### Step 4 — Generate or select cover visual

Prefer the real interview/field image. Use the image-generation prompt file only for a visual background or a texture, never for technical text or statistics.

### Step 5 — Lay out the sheet

Use a print-aware layout tool. Export both the flat A3 proof and the folded A4 reading proof.

### Step 6 — Test the judge journey

Give the folded handout to someone who has not read the project and ask them, after 90 seconds:

1. What problem did the team discover?
2. Why is a normal LLM not enough?
3. What happens to a dangerous query?
4. Who pays first?

If they cannot answer all four, remove decoration and enlarge the story labels.
