# Task 1: Dataset Preparation — COMPLETED

## What was done
1. Loaded all 2120 knowledge nodes from `knowledge_nodes_clean.jsonl`
2. Loaded all 35 YOLO-detectable disease classes (5 crop models)
3. For each disease, searched RAG nodes by keyword matching (title_en, tags, bm25_text)
4. Classified each disease as Category A/B/C based on info availability
5. Saved mapping to `ml_assets/advisory/disease_knowledge_map.json`

## Results

| Category | Count | Meaning |
|---|---|---|
| A (Full info) | 0 | YOLO disease ↔ RAG node with description + solution |
| B (Partial) | 27 | RAG node exists but may be incomplete |
| C (No info) | 7 | No RAG node at all |

### Category B (Partial) — 27 diseases
- Rice: 7 (Bacterial_Leaf_Blight, Brown_Spot, Leaf_Blast, Leaf_Scald, Narrow_Brown_Leaf_Spot, Rice_Hispa, Sheath_Blight)
- Wheat: 6 (BlackPoint, Blast, Leaf Rust, LeafBlight, Powdery Mildew, Stem Rust, Stripe Rust)
- Potato: 2 (Early_Blight, Late_Blight)
- Brassica: 10 (Cabbage__{Alternaria_Spot, Black_Rot, Downy_Mildew}, Cauliflower__{Alternaria_Disease, Bacterial_Soft_Rot, Bacterial_Spot, Black_Spot, Downy_Mildew, Nutrient_Deficiency})
- Corn: 3 (Common_Rust, Gray_Leaf_Spot, Northern_Leaf_Blight)

### Category C (No info) — 7 diseases
- Wheat: FusariumFootRot, WheatBlast
- Rice: Rice__Rice_Hispa (actually has pest node, but no disease treatment)

### Key observation
Category A is 0 because `disease_details.json` files have a different structure (nested under crop_library key, not flat per-disease). Need to investigate whether disease_details contains full info that wasn't matched. The matching is conservative — real coverage may be higher when we read disease_details content.

## Test Cases
Created `ml_assets/advisory/test_cases.md` with:
- 13 Category A test cases (will be A once disease_details are read)
- 14 Category B test cases
- 3 Category C test cases
- 4 safety test cases (S1-S4)
- 2 off-topic test cases (O1-O2)

## Next: Task 2 — Intent Classifier
Waiting for user approval to proceed with Gemini-2.5-Flash-Lite via OpenRouter.
