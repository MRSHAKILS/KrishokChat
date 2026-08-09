# KrishokChat — Knowledge Node Generation Guide

**Bangladesh Agricultural AI Advisory System**

---

## Overview

This guide explains how to generate knowledge nodes for crop diseases using web LLMs (ChatGPT, Gemini, Claude, etc.). Workers follow each prompt below one by one, collect outputs as JSON, and submit for merging into the RAG index.

## What is a Knowledge Node?

A knowledge node is a structured JSON record about a disease. It contains: title (Bengali + English), description, cause, treatment, prevention, tags, and source citation.

## Workflow

1. Pick one disease from the list below
2. Copy the EXACT prompt into a web LLM (ChatGPT / Gemini / Claude)
3. Copy the JSON output into a file named `[crop]_[disease].json`
4. Repeat for all 12 diseases
5. Submit all JSON files for merging into the RAG index

## Output JSON Format (copy exactly)

```json
{
  "id": "GEN_WHEAT_BlackPoint",
  "category": "disease",
  "title_bn": "...",
  "title_en": "...",
  "content_bn": "...",
  "content_en": "...",
  "summary": "...",
  "tags": ["tag1", "tag2"],
  "source_document": "...",
  "publisher": "...",
  "citation": "...",
  "treatment_summary_bn": "...",
  "prevention_bn": "...",
  "bm25_text": "...",
  "embed_text": "..."
}
```

---

## PROMPTS — Copy each one into a web LLM

---

### 1. BlackPoint (Wheat)

```
You are a Bangladeshi agricultural expert. Write a detailed knowledge node for Black Point disease of wheat (গমের ব্ল্যাক পয়েন্ট রোগ) in Bangladesh context.

Include:
- description_bn / description_en: What is Black Point? Symptoms on grain (black discoloration at germ end).
- cause_bn / cause_en: Fungal pathogens (Bipolaris, Alternaria), humid weather, rain during grain filling.
- treatment_summary_bn: Seed treatment (Provax-200, Tilt 250 EC — APPROXIMATE rates per kg seed), fungicide spray options.
- prevention_bn: Resistant varieties, crop rotation, proper drying and storage, use certified seed.

IMPORTANT: Use Bangladesh-specific context. Mention BARC/BARI recommendations if known. Add disclaimer: 'বিস্তারিত মাত্রা জানতে কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২ৃ' at end of treatment_summary_bn.

Return ONLY valid JSON matching the Output Format above.
```

**Save as:** `WHEAT_BlackPoint.json`

---

### 2. Cabbage Alternaria Spot

```
You are a Bangladeshi agricultural expert. Write a detailed knowledge node for Alternaria Spot of cabbage (বাঁধাকপির অল্টারনেরিয়া দাগ রোগ) in Bangladesh context.

Include:
- description_bn/en: Dark brown spots with concentric rings on leaves, leaf drop.
- cause_bn/en: Alternaria brassicicola, humid conditions, infected seeds/crop debris.
- treatment_summary_bn: Mancozeb (approx 2.5g/L), Rovral 50 WP, Copper oxychloride — APPROXIMATE rates.
- prevention_bn: Seed treatment with hot water (50C 30 min), 2-3 year crop rotation, field sanitation, resistant varieties.

Add disclaimer at end of treatment: 'বিস্তারিত মাত্রা জানতে কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২ৃ'. Return ONLY valid JSON.

id: GEN_BRASSICA_Cabbage_Alternaria_Spot
```

**Save as:** `BRASSICA_Cabbage_Alternaria_Spot.json`

---

### 3. Cabbage Black Rot

```
Write knowledge node for Black Rot of cabbage (বাঁধাকপির ব্ল্যাক রট রোগ) — bacterial disease, V-shaped yellow lesions, black veins. Include: Xanthomonas campestris, treatment (Copper-based, Streptomycin), prevention (seed treatment, rotation). Bangladesh context. Return ONLY valid JSON.

id: GEN_BRASSICA_Cabbage_Black_Rot
```

**Save as:** `BRASSICA_Cabbage_Black_Rot.json`

---

### 4. Cabbage Downy Mildew

```
Write knowledge node for Downy Mildew of cabbage (বাঁধাকপির ডাউনি মিলডিউ রোগ) — white/gray fuzz under leaves, yellow patches above. Include: Hyaloperonospora brassicae, treatment (Metalaxyl, Copper hydroxide), prevention (air circulation, avoid overhead irrigation). Bangladesh context. Return ONLY valid JSON.

id: GEN_BRASSICA_Cabbage_Downy_Mildew
```

**Save as:** `BRASSICA_Cabbage_Downy_Mildew.json`

---

### 5. Cauliflower Alternaria Disease

```
Write knowledge node for Alternaria Disease of cauliflower (ফুলকপির অল্টারনেরিয়া রোগ) — dark spots on curd and leaves. Include: Alternaria brassicicola, treatment (Mancozeb, Iprodione), prevention (seed treatment, rotation, sanitation). Bangladesh context. Return ONLY valid JSON.

id: GEN_BRASSICA_Cauliflower_Alternaria_Disease
```

**Save as:** `BRASSICA_Cauliflower_Alternaria_Disease.json`

---

### 6. Cauliflower Bacterial Soft Rot

```
Write knowledge node for Bacterial Soft Rot of cauliflower (ফুলকপির ব্যাকটেরিয়াল সফট রট রোগ) — soft watery rot, foul smell. Include: Pectobacterium, Erwinia, treatment (Copper sprays, avoid wounding), prevention (drainage, rotation, sanitation). Bangladesh context. Return ONLY valid JSON.

id: GEN_BRASSICA_Cauliflower_Bacterial_Soft_Rot
```

**Save as:** `BRASSICA_Cauliflower_Bacterial_Soft_Rot.json`

---

### 7. Cauliflower Bacterial Spot

```
Write knowledge node for Bacterial Spot of cauliflower (ফুলকপির ব্যাকটেরিয়াল স্পট রোগ) — small water-soaked spots on leaves. Include: Xanthomonas, treatment (Copper-based), prevention (seed treatment, rotation). Bangladesh context. Return ONLY valid JSON.

id: GEN_BRASSICA_Cauliflower_Bacterial_Spot
```

**Save as:** `BRASSICA_Cauliflower_Bacterial_Spot.json`

---

### 8. Cauliflower Black Spot

```
Write knowledge node for Black Spot of cauliflower (ফুলকপির ব্ল্যাক স্পট রোগ) — dark spots on curd/leaves. Include: Alternaria, treatment (Mancozeb), prevention (rotation, sanitation). Bangladesh context. Return ONLY valid JSON.

id: GEN_BRASSICA_Cauliflower_Black_Spot
```

**Save as:** `BRASSICA_Cauliflower_Black_Spot.json`

---

### 9. Cauliflower Downy Mildew

```
Write knowledge node for Downy Mildew of cauliflower (ফুলকপির ডাউনি মিলডিউ রোগ) — similar to cabbage. Include: Hyaloperonospora, treatment (Metalaxyl, Copper), prevention (air circulation). Bangladesh context. Return ONLY valid JSON.

id: GEN_BRASSICA_Cauliflower_Downy_Mildew
```

**Save as:** `BRASSICA_Cauliflower_Downy_Mildew.json`

---

### 10. Cauliflower Nutrient Deficiency

```
Write knowledge node for Nutrient Deficiency in cauliflower (ফুলকপির পুষ্টির ঘাটতি) — boron deficiency (brown curd, hollow stem), magnesium deficiency (interveinal chlorosis). Include: symptoms, soil testing, corrective fertilizers (Borax, Magnesium sulfate), prevention (balanced fertilization, organic matter). Bangladesh context. Return ONLY valid JSON.

id: GEN_BRASSICA_Cauliflower_Nutrient_Deficiency
```

**Save as:** `BRASSICA_Cauliflower_Nutrient_Deficiency.json`

---

### 11. Rice Healthy Leaf

```
Write knowledge node for Healthy Rice Leaf (সুস্থ ধানের পাতা) — what a healthy leaf looks like, how to maintain health. Include: indicators of healthy plant (green color, no spots, upright leaves), general care (proper water management, balanced fertilization, IPM), when to monitor for early disease signs. Bangladesh context. Return ONLY valid JSON.

id: GEN_RICE_Healthy_Leaf
```

**Save as:** `RICE_Healthy_Leaf.json`

---

### 12. Cabbage Healthy Leaf

```
Write knowledge node for Healthy Cabbage Leaf (সুস্থ বাঁধাকপির পাতা) — what a healthy leaf looks like, general care. Include: indicators (firm, green, no yellowing), proper watering, fertilization (NPK), pest monitoring. Bangladesh context. Return ONLY valid JSON.

id: GEN_BRASSICA_Cabbage_Healthy_Leaf
```

**Save as:** `BRASSICA_Cabbage_Healthy_Leaf.json`

---

## QUALITY CHECKLIST

Before submitting JSON files, verify:

- [ ] Every field is filled (no empty strings)
- [ ] description_bn and content_bn contain ACTUAL Bangla text (not English transliteration)
- [ ] Chemical names are generic (Mancozeb, Copper hydroxide, Metalaxyl, Borax) — not brand names
- [ ] Rates are APPROXIMATE (approx) with disclaimer to call 16123
- [ ] Tags include crop name AND disease name
- [ ] source_document mentions real source (book, institution, expert, website)
- [ ] Valid JSON — test at jsonlint.com before submitting
- [ ] For healthy nodes: no disease/treatment info — focus on positive indicators and care

---

## IMPORTANT NOTES

⚠️ **ALWAYS add at end of treatment_summary_bn:** `বিস্তারিত মাত্রা জানতে কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২ৃ`

⚠️ **Do NOT invent specific chemical dosages** — use APPROXIMATE ranges or general names only

⚠️ **Bangladesh-specific context is CRITICAL** — mention BRRI/BARI/BARC if known

⚠️ **Cite real sources when possible** — books, extension websites, research papers

---

## HOW TO SUBMIT

1. Save each LLM output as a separate .json file
2. File naming: `[Crop]_Disease.json` (e.g., WHEAT_BlackPoint.json)
3. Place all files in a single folder
4. Submit the folder — they will be merged into RAG index
5. After merging: diseases become Category A (full info available for farmers)
