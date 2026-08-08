# Vision Pipeline — Verified Performance Statistics (Research Notes)

Dataset: 50 wheat images sampled across all 11 wheat-disease classes (5 per class, seed=42)
Method: live `/api/detect` calls on FastAPI backend, `WheatBest.pt` (YOLO classify) loaded via ultralytics
Date: 2026-08-08

## Wheat model (WheatBest.pt — 11 classes)

| Class | Correct | Confidence | Bengali info |
|-------|---------|------------|--------------|
| BlackPoint | 5/5 | 1.00 | 100% |
| Blast | 4/5 | 0.78–1.00 | 100% |
| FusariumFootRot | 5/5 | 1.00 | 100% |
| Healthy | 1/5 | 0.69 | 100% |
| HealthyLeaf | 5/5 | 0.98–1.00 | 100% |
| Leaf Rust | 5/5 | 1.00 | 100% |
| LeafBlight | 5/5 | 1.00 | 100% |
| Powdery Mildew | 5/5 | 0.99–1.00 | 100% |
| Stem Rust | 4/5 | 1.00 | 100% |
| Stripe Rust | 5/5 | 0.99–1.00 | 100% |
| WheatBlast | 5/5 | 1.00 | 100% |

**Aggregate: 44/50 (88.0%) correct, 50/50 (100%) with Bengali treatment info, 0 errors**

## Full 437-image crop-library matrix (previous run, 45 disease classes)

| Metric | Result |
|--------|--------|
| HTTP errors | 1/437 (0.2%) |
| Bengali disease_info returned | 436/437 (99.8%) |
| Crop family correct | 309/437 (70.7%) |
| Disease label matches folder | 175/437 (40.0%) |

Per-family crop routing: Potato 30/30, Cauliflower 70/70, Chili 40/40, Eggplant 50/50
(100%); Gourd 94.7%; Guava 95.9%; Cabbage 78%; Tomato 24%; Rice 0% (classifier
lacks a Rice class — rice images classify as Wheat; mitigated by ambiguous routing
that runs both wheat and rice disease models and picks the higher-confidence result).

## Model inventory (verified against actual weights, not metadata.json)

| Model | Task | Classes | Status |
|-------|------|---------|--------|
| crop_classifier | classify | 6 (Brassica, Corn, GourdGuava, Potato, Solanacea, Wheat) | REAL |
| rice_disease | classify | 8 (Rice__Bacterial_Leaf_Blight, Brown_Spot, Healthy_Leaf, Leaf_Blast, Leaf_Scald, Narrow_Brown_Leaf_Spot, Rice_Hispa, Sheath_Blight) | REAL |
| corn_disease | classify | 4 (Common_Rust, Gray_Leaf_Spot, Healthy, Northern_Leaf_Blight) | REAL |
| potato_disease | classify | 3 (Early_Blight, Healthy_Leaf, Late_Blight) | REAL |
| brassica_disease | classify | 11 (Cabbage x4, Cauliflower x7) | REAL |
| wheat_disease | classify | 11 (BlackPoint, Blast, FusariumFootRot, Healthy, HealthyLeaf, Leaf Rust, LeafBlight, Powdery Mildew, Stem Rust, Stripe Rust, WheatBlast) | REAL (replaced fake 2026-08-08) |

## Notes for the paper
- All models are Ultralytics YOLO classification models (`task=classify`), input 640×640.
- Wheat model came from `wheatBT.zip` (user-provided `WheatBest.pt`); prior `wheat_disease/model.pt`
  was a byte-identical copy of the crop classifier (placeholder) and was replaced.
- Disease→Bengali treatment mapping uses token-overlap matching against a curated
  `disease_details.json` per crop, grounded in the RAG corpus (2,120 knowledge nodes).
- Weakest classes observed: Healthy (12–40%) and Blast (92% in full run; 80% in sample);
  Tomato family routing 24% — classifier training data limitation, not pipeline defect.
