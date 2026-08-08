# Advisory Workflow — Full Plan

> Objective: Detect crop+disease from image, show grounded info from RAG, then optionally "Chat more" with Gemini-2.5-Flash-Lite via OpenRouter, using detected attributes to narrow retrieval and handle missing knowledge gracefully.

---

## Current Data Inventory

### YOLO-detectable diseases (per crop model)

| Crop | Model | Detectable classes (YOLO output) | Healthy classes | Disease classes |
|---|---|---|---|---|
| Rice | rice_disease | 8 | Rice__Healthy_Leaf (1) | 7: Bacterial_Leaf_Blight, Brown_Spot, Leaf_Blast, Leaf_Scald, Narrow_Brown_Leaf_Spot, Rice_Hispa, Sheath_Blight |
| Wheat | wheat_disease | 11 | Healthy, HealthyLeaf (2) | 9: BlackPoint, Blast, FusariumFootRot, Leaf Rust, LeafBlight, Powdery Mildew, Stem Rust, Stripe Rust, WheatBlast |
| Potato | potato_disease | 3 | Potato__Healthy_Leaf (1) | 2: Early_Blight, Late_Blight |
| Brassica | brassica_disease | 11 | Cabbage__Healthy_Leaf, Cauliflower__Healthy (2) | 9: Cabbage__{Alternaria_Spot, Black_Rot, Downy_Mildew}, Cauliflower__{Alternaria_Disease, Bacterial_Soft_Rot, Bacterial_Spot, Black_Spot, Downy_Mildew, Nutrient_Deficiency} |
| Corn | corn_disease | 4 | Healthy (1) | 3: Common_Rust, Gray_Leaf_Spot, Northern_Leaf_Blight |
| Solanacea/GourdGuava | (no model) | — | — | routed to nearest (Potato/Brassica) |

**Total YOLO-disease classes: 35** (excluding healthy).

### RAG Knowledge Nodes

| Category | Count |
|---|---|
| disease | 244 |
| pest | 351 |
| fertilizer | 376 |
| general | 510 |
| cultivation_practice | 357 |
| variety | 106 |
| cropping_system | 52 |
| post_harvest | 51 |
| seed_tech | 24 |
| irrigation | 21 |
| food_safety | 15 |
| ipm | 11 |
| herbicide | 1 |
| machinery | 1 |
| **Total** | **2120** |

---

## The Architecture (what we're building)

```
┌─────────────────────────────────────────────────────────────┐
│  STAGE 1: DETECTION (YOLO — already working)                │
│  Image → crop_classifier → specific disease model          │
│  Output: {crop, disease, confidence}                        │
│  Show: disease name + description/solution from RAG         │
└──────────────────────────┬──────────────────────────────────┘
                           │ user clicks "Chat more"
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 2: INTENT CLASSIFICATION (Gemini-2.5-Flash-Lite)     │
│  Query → precheck (regex: self-harm/injection/banned)       │
│         → Gemini intent JSON {intent, safety_flag}           │
│  Intents: treatment, prevention, general_info,             │
│           variety, fertilizer, off_topic, unsafe            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 3: FILTERED RETRIEVAL                                │
│  Query + (crop, disease, intent) → narrow BM25 search      │
│  Search space reduced by crop+disease+intent tags           │
│  → top-k relevant knowledge nodes                           │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 4: CONTEXT ASSEMBLY + GENERATION                     │
│  Build prompt with:                                         │
│    - detected crop + disease (from Stage 1)                 │
│    - retrieved nodes (from Stage 3)                         │
│    - intent (from Stage 2)                                  │
│    - MISSING-INFO handling (see below)                      │
│  → Gemini-2.5-Flash-Lite → stream answer                    │
└─────────────────────────────────────────────────────────────┘
```

---

## KEY DESIGN: Missing-Info Handling

The 35 YOLO-detectable diseases do NOT all have matching RAG knowledge nodes. We must handle this explicitly:

### Category A — Full info available (YOLO disease ↔ RAG node with description + solution)
- Pass full context to generator
- Generator can answer treatment/solution

### Category B — Partial info (YOLO disease ↔ RAG node but incomplete)
- Pass what we have
- Flag to generator: "এই রোগের সম্পূর্ণ তথ্য নেই, শুধু [যা আছে] জানা যাচ্ছে"
- Generator must NOT hallucinate the missing parts

### Category C — No info (YOLO disease ↔ NO RAG node at all)
- Pass to generator: "দুঃখিত, এই রোগের কোনো তথ্য আমাদের ডাটাবেসে নেই"
- Treatment-related: gently refer to **Krishi Call Center 16123**
- Basic info (what crop, what disease name): can state without hallucination

### The mapping task
We must build `disease_knowledge_map.json` that maps each of the 35 YOLO disease classes to:
- matching RAG node IDs (if any)
- info completeness: full / partial / none
- for partial: which fields are missing (description? solution? prevention?)

---

## Execution Plan (one task at a time)

### Task 1: DATASET PREPARATION ← CURRENT
**Goal:** Build the disease↔knowledge mapping + test cases.

**Sub-steps:**
1. Load all YOLO disease classes (35, excluding healthy)
2. For each, search RAG nodes (bm25_text / title_en / content_en) for matches
3. Classify each as Category A / B / C
4. Build `disease_knowledge_map.json` with:
   ```json
   {
     "Rice__Brown_Spot": {
       "category": "A",
       "node_ids": ["B5_xxx"],
       "has_description": true,
       "has_solution": true,
       "has_prevention": true
     },
     "Corn__Common_Rust": {
       "category": "C",
       "node_ids": [],
       "note": "no knowledge in RAG"
     }
   }
   ```
5. Generate `test_cases.md` — at least 2 examples per category (A/B/C) × multiple crops = ~10-12 test cases
6. Clean up: remove any floating scripts, ensure folder structure is correct

**Folder:** `backend/app/services/advisory/` (new) + `backend/ml_assets/advisory/` (data artifacts)

### Task 2: INTENT CLASSIFIER (Gemini-2.5-Flash-Lite via OpenRouter)
**After Task 1 is approved.**

### Task 3: FILTERED RETRIEVAL
**After Task 2 is approved.**

### Task 4: GENERATOR + MISSING-INFO PROMPT
**After Task 3 is approved.**

### Task 5: FRONTEND WIRING
**After Task 4 is approved.**

---

## Folder Structure (target)

```
backend/app/services/advisory/
    __init__.py
    intent_classifier.py      # Gemini-2.5-Flash-Lite via OpenRouter
    filtered_retrieval.py     # crop+disease+intent → narrow BM25
    context_assembler.py      # build prompt with missing-info handling
    generator.py              # Gemini streaming answer

backend/ml_assets/advisory/
    disease_knowledge_map.json    # 35 diseases → RAG nodes (Category A/B/C)
    test_cases.md                 # validation cases

docs/advisory_workflow/
    PLAN.md                   # this file
    TASK1_DATASET.md          # Task 1 spec + results
    TASK2_INTENT.md
    TASK3_RETRIEVAL.md
    TASK4_GENERATOR.md
    TASK5_FRONTEND.md
```

---

## Test Cases (draft — to be filled after mapping)

| # | Crop | Detected Disease | Category | Intent | Expected behavior |
|---|---|---|---|---|---|
| 1 | Potato | Late_Blight | ? | treatment | Full solution from RAG |
| 2 | Rice | Brown_Spot | ? | prevention | Prevention info |
| 3 | Wheat | BlackPoint | ? | treatment | ... |
| 4 | Corn | Common_Rust | ? | treatment | Category C → refer 16123 |
| 5 | Brassica | Cauliflower__Downy_Mildew | ? | general | ... |
| ... | ... | ... | ... | ... | ... |

---

## Safety & Quality Rules
- **Gemini model: ONLY `gemini-2.5-flite` via OpenRouter** — no other model
- **No hallucination on missing info** — explicit instructions in generator prompt
- **Treatment without knowledge → refer 16123** — never make up chemical dosages
- **Self-harm / banned chemicals → precheck blocks before any API call**
- **No floating scripts** — every file goes in its designated folder
- **Document after each task** — what was done, what's left, open questions
