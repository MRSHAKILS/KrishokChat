# Literature Review Summary for Supervisor Decision

**Project:** CSE498R - Soil Moisture Detection
**Student:** [Student Name]
**Supervisor:** [Supervisor Name]
**Date:** July 2026
**Purpose:** Present findings for research direction decision

---

## Executive Summary

After comprehensive analysis of **47 papers** across 5 categories, we have identified:

- **20 research gaps** (5 critical, 5 high, 5 medium, 5 application)
- **6 gaps our dataset can address** directly
- **1 unique contribution opportunity** no existing study has achieved

**Recommendation:** Proceed with research focusing on **RGB image + tensiometer validation in Bangladesh**

---

## 0. Our Dataset Summary

| Aspect | Details |
|--------|---------|
| Total Images | 722 RGB images |
| Image Size | 720×1280 pixels (portrait) |
| Format | JPEG, RGB |
| Total Size | 180 MB |
| Ground Truth | Tensiometer readings (0-101 kPa) |
| Unique kPa Values | 50 distinct values |
| Collection Period | May 30-31, 2026 |
| Location | Pabna District, Bangladesh |
| Soil Types | Agricultural field soil |
| Split | 70% train / 15% val / 15% test |

### Dataset Distribution:

| kPa Range | Images | Percentage | Status |
|-----------|--------|------------|--------|
| 0-10 kPa | ~166 | 23% | Wet |
| 10-20 kPa | ~482 | 66.8% | Optimal (dominant) |
| 20-30 kPa | ~73 | 10.1% | Dry |

**Class Imbalance Note:** 66.8% of images are in 10-20 kPa range. This is both a challenge (model may bias toward this range) and an opportunity (most agricultural scenarios operate in this range).

### Preprocessing Pipeline (Already Developed):

| Step | Script | Status |
|------|--------|--------|
| 0a | `preprocess_step0.py` | ✅ Complete |
| 0b | `normalize_filenames_step0b.py` | ✅ Complete |
| 0c | `extract_exif_step0c.py` | ✅ Complete |
| 0d | `split_planner_step0d.py` | ✅ Complete |

**Output Files:**
- `image_manifest.csv` - 722 rows, 9 columns
- `split_assignment.csv` - Train/val/test assignments
- `anomalies.json` - 12 anomalies identified
- `series_map.json` - 35 consecutive series

### Key Dataset Characteristics:

1. **No EXIF data** - Timestamps only as pixel watermarks
2. **All identical dimensions** - 720×1280 portrait
3. **Consecutive series** - 35 series of related images
4. **1 outlier flagged** - P0114_101Kpa (needs verification)
5. **4 duplicate IDs** - Kept as separate samples with suffix letters

---

## 1. Literature Landscape Overview

### 1.1 Research Categories (47 Papers)

| Category | Papers | Our Position |
|----------|--------|--------------|
| Image-Based Soil Moisture | 12 | Direct competition |
| Remote Sensing + ML/DL | 18 | Different modality |
| Ground-Based Sensors | 8 | Validates our ground truth |
| IoT Systems | 5 | Context (Bangladesh) |
| Surveys/Reviews | 4 | Background reference |

### 1.2 Geographic Distribution

| Region | Papers | Bangladesh Presence |
|--------|--------|-------------------|
| China | 14 | None |
| India | 8 | Adjacent context |
| **Bangladesh** | **5** | **IoT only, no image-based** |
| USA/Europe | 12 | Different context |

**Key Finding:** No image-based soil moisture study exists for Bangladesh.

---

## 2. Closest Related Works (Post-Mortem Analysis)

### 2.1 PLOS ONE (2026) - Image-based ML for ginseng

| Aspect | Details | Our Comparison |
|--------|---------|----------------|
| Method | DenseNet121, EfficientNetB0 | Same architectures available |
| Dataset | Greenhouse, single crop | We have field conditions |
| Ground Truth | Sensor at 3 depths | We have tensiometer (kPa) |
| Result | R²=97.3% | Our target to beat |
| Weakness | No field validation | We have field data |

**Verdict:** Strong baseline, but limited to controlled conditions.

### 2.2 Zhang et al. (2024) - LG-SWC-R3 model

| Aspect | Details | Our Comparison |
|--------|---------|----------------|
| Method | Transformer + attention | We can implement |
| Dataset | 3175 images, lab conditions | We have 722 field images |
| Result | R²=0.950 | Our target to beat |
| Weakness | Single soil type, lab only | We have field conditions |

**Verdict:** Strong methodology, but lab-only validation.

### 2.3 Suud et al. (2026) - CNN FAILURE

| Aspect | Details | Our Comparison |
|--------|---------|----------------|
| Method | CNN, ResNet-50 | Same architectures |
| Dataset | 200 field images | We have 722 (3.6× more) |
| Result | R²=0.205-0.513 (FAILED) | We must avoid this |
| Failure Cause | Insufficient data, no preprocessing | We have preprocessing pipeline |

**Verdict:** CAUTIONARY TALE - validates our approach (more data, preprocessing).

---

## 3. Research Gaps We Can Address

### 3.1 Critical Gaps (Novel Contributions)

| Gap | Status | Our Capability |
|-----|--------|---------------|
| RGB + Tensiometer validation | No existing study | ✅ We have both |
| Field-captured RGB processing | Only failed attempts | ✅ We have field images |
| Bangladesh image-based study | No existing study | ✅ We have Bangladesh data |
| kPa regression from images | No existing study | ✅ We have kPa measurements |
| Multi-depth prediction | Limited existence | ⚠️ Limited depth variation |

### 3.2 Our Unique Advantages

1. **Tensiometer ground truth:** Measures matric potential (kPa) - what plants actually experience
2. **Field conditions:** Real agricultural setting, not lab
3. **Bangladesh context:** Tropical, monsoon climate - underrepresented
4. **722 images:** Larger than most studies (200-629 images)
5. **Preprocessing pipeline:** Already developed and tested

---

## 4. Proposed Research Direction

### 4.1 Primary Research Question

> **"Can field-captured RGB images predict soil matric potential (kPa) for irrigation decision-making in tropical agriculture?"**

### 4.2 Specific Objectives

1. **Objective 1:** Develop RGB-to-kPa regression model
   - Target: R² > 0.85, RMSE < 10 kPa
   - Method: Transfer learning (DenseNet121, ResNet50)

2. **Objective 2:** Validate in field conditions
   - Compare with tensiometer readings
   - Test across different lighting conditions

3. **Objective 3:** Develop preprocessing pipeline
   - Soil segmentation
   - Lighting normalization
   - Non-soil object removal

4. **Objective 4:** Interpret model decisions
   - SHAP/LIME analysis
   - Identify predictive visual features

### 4.3 Expected Contributions

1. **First study** to predict kPa from RGB images
2. **First image-based** soil moisture study in Bangladesh
3. **Field-validated** methodology (not just lab)
4. **Practical tool** for irrigation decisions

---

## 5. Risk Assessment

### 5.1 Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Field images too noisy | Medium | High | Aggressive preprocessing |
| Model overfits | Medium | Medium | Cross-validation, augmentation |
| Low R² in field | High | High | Compare with simple baselines |
| Tensiometer-image mismatch | Low | Medium | Verify spatial correspondence |

### 5.2 Data Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Insufficient data | Low | High | Augmentation, transfer learning |
| Class imbalance | High | Medium | Weighted loss, resampling |
| Limited depth variation | Medium | Medium | Focus on surface prediction |

### 5.3 Mitigation Strategies

1. **If field images fail:** Fall back to lab subset analysis
2. **If R² low:** Compare with color-feature regression as baseline
3. **If overfitting:** Use simpler models (Random Forest, SVR)
4. **If tensiometer mismatch:** Verify with manual gravimetric measurements

---

## 6. Comparison with Alternatives

### Option A: RGB + Tensiometer (Recommended)

| Pros | Cons |
|------|------|
| Novel contribution | Field images challenging |
| Bangladesh context | Tensiometer limitations |
| Practical application | Limited depth variation |
| Strong ground truth | |

### Option B: Remote Sensing Approach

| Pros | Cons |
|------|------|
| Established methods | Not image-based |
| Large datasets available | Satellite resolution limits |
| Many baselines | No tensiometer validation |

### Option C: IoT Sensor Fusion

| Pros | Cons |
|------|------|
| Bangladesh context exists | Not image-based |
| Low-cost solutions | Multiple papers already |
| Practical deployment | Less novel |

**Recommendation:** Option A is most novel and aligns with our dataset.

---

## 7. Specific Challenges to Address

### 7.1 Dataset Challenges:

| Challenge | Impact | Solution |
|-----------|--------|----------|
| Class imbalance (66.8% in 10-20 kPa) | Model bias toward dominant range | Weighted loss, oversampling minority classes |
| No EXIF timestamps | Cannot track temporal patterns | Use pixel watermarks if needed |
| 1 outlier (101 kPa) | May skew model | Verify with field team, exclude if invalid |
| Limited depth variation | Cannot predict subsurface | Focus on surface prediction only |
| 2-day collection period | Limited temporal diversity | Acknowledge as limitation |

### 7.2 Technical Challenges:

| Challenge | Impact | Solution |
|-----------|--------|----------|
| Field images have varying lighting | Inconsistent features | Histogram equalization, normalization |
| Non-soil objects in images | Noise in features | Soil segmentation preprocessing |
| Tensiometer accuracy (±5 kPa) | Label noise | Use as ground truth, acknowledge uncertainty |
| Image resolution (720×1280) | High computation | Resize to 224×224 for training |
| Windows encoding (cp1252) | Script errors | Avoid Unicode in print statements |

### 7.3 Methodological Challenges:

| Challenge | Impact | Solution |
|-----------|--------|----------|
| Small dataset (722 images) | Overfitting risk | Transfer learning, augmentation, regularization |
| No public benchmark | Cannot compare directly | Publish dataset for future work |
| Single soil type | Limited generalization | Acknowledge, test transferability if possible |
| kPa vs VWC different scales | Comparison difficulty | Focus on kPa regression, note VWC studies |

---

## 8. Expected Deliverables

### 8.1 Research Deliverables:

| Deliverable | Description | Timeline |
|-------------|-------------|----------|
| Preprocessing pipeline | Soil segmentation, normalization | Week 1-2 |
| Baseline models | Color regression, Random Forest | Week 3-4 |
| Transfer learning models | DenseNet121, ResNet50, EfficientNetB0 | Week 5-6 |
| Advanced models | Attention-based, ensemble stacking | Week 7-8 |
| Interpretability analysis | SHAP/LIME, feature importance | Week 9 |
| Error analysis | Per-sample visualization, failure cases | Week 10 |
| Paper draft | Conference or journal format | Week 11-12 |

### 8.2 Code Deliverables:

| Deliverable | Description |
|-------------|-------------|
| `train_model.py` | Main training script with all models |
| `evaluate_model.py` | Evaluation and visualization |
| `preprocess_images.py` | Image preprocessing pipeline |
| `utils.py` | Helper functions |
| `configs/` | Model configurations |
| `results/` | Trained models, plots, metrics |

### 8.3 Documentation Deliverables:

| Deliverable | Description |
|-------------|-------------|
| Paper manuscript | 8-10 pages (conference) or 12-15 pages (journal) |
| README.md | Project documentation |
| API documentation | Model usage guide |
| Dataset documentation | For public release |

---

## 9. Timeline and Milestones

### Phase 1: Data Preparation (2 weeks)
- [ ] Finalize preprocessing pipeline
- [ ] Generate train/val/test splits
- [ ] Implement augmentation pipeline

### Phase 2: Baseline Models (3 weeks)
- [ ] Implement color feature regression
- [ ] Implement transfer learning (DenseNet121, ResNet50)
- [ ] Establish baseline R², RMSE

### Phase 3: Advanced Models (4 weeks)
- [ ] Implement attention-based model
- [ ] Implement ensemble stacking
- [ ] Hyperparameter optimization

### Phase 4: Analysis and Writing (3 weeks)
- [ ] SHAP/LIME interpretability analysis
- [ ] Error analysis and visualization
- [ ] Write paper draft

**Total Timeline:** 12 weeks

---

## 10. Resource Requirements

### Computational:
- GPU access for training (Colab Pro or university cluster)
- Storage: ~10 GB for dataset + models

### Software:
- Python, PyTorch/TensorFlow
- OpenCV for preprocessing
- SHAP/LIME for interpretability

### Human:
- Supervisor guidance on methodology
- Weekly progress meetings

---

## 11. Decision Points for Supervisor

### 11.1 Approve Research Direction?

- [ ] **Yes:** Proceed with RGB + tensiometer approach
- [ ] **No:** Consider alternative approaches
- [ ] **Modify:** Adjust scope or objectives

### 11.2 Scope Decisions:

- [ ] **Include multi-depth prediction?** (More complex, but higher impact)
- [ ] **Include smartphone app?** (More practical, but more work)
- [ ] **Include transfer learning?** (More generalizable, but more experiments)

### 11.3 Publication Target:

- [ ] **Conference paper:** 6-8 pages, faster publication
- [ ] **Journal paper:** 10-15 pages, more comprehensive
- [ ] **Thesis chapter:** Full treatment of the topic

---

## 12. Expected Paper Structure

### Section Breakdown (Target: 8-10 pages for conference):

| Section | Content | Estimated Length |
|---------|---------|-----------------|
| 1. Introduction | Problem, motivation, contributions | 1 page |
| 2. Related Work | Image-based SM, sensor methods, ML/DL | 1.5 pages |
| 3. Dataset | Description, preprocessing, splits | 1 page |
| 4. Methodology | Models, architecture, training | 1.5 pages |
| 5. Experiments | Setup, baselines, ablation | 1 page |
| 6. Results | Main results, comparison, analysis | 1.5 pages |
| 7. Discussion | Interpretation, limitations, future work | 1 page |
| 8. Conclusion | Summary, contributions | 0.5 page |

### Key Results to Report:

| Metric | Target | Baseline (Color Regression) |
|--------|--------|-----------------------------|
| R² | > 0.85 | ~0.60-0.70 |
| RMSE | < 10 kPa | ~15-20 kPa |
| MAE | < 8 kPa | ~12-15 kPa |

### Models to Implement:

| Model | Type | Purpose | Priority |
|-------|------|---------|----------|
| Color Feature Regression | Simple baseline | Establish lower bound | HIGH |
| Random Forest | ML baseline | Compare with DL | HIGH |
| DenseNet121 | Transfer learning | Primary model | HIGH |
| ResNet50 | Transfer learning | Comparison | MEDIUM |
| EfficientNetB0 | Transfer learning | Lightweight option | MEDIUM |
| Attention-based CNN | Custom | Novel contribution | MEDIUM |
| Ensemble Stacking | Fusion | Best performance | LOW |

---

## 13. Appendix: Key References

### Must-Read Papers:
1. PLOS ONE (2026) - Image-based ML for soil moisture
2. Zhang et al. (2024) - LG-SWC-R3 model
3. Suud et al. (2026) - CNN failure analysis
4. Hossain et al. (2023) - Smartphone ML
5. Indian soils study (2025) - Interpretable ML

### Background Papers:
6. HESS (2024) - DL for soil moisture survey
7. Sensors (2023) - Sensor comparison
8. Bangladesh IoT studies (2024-2025)

### Our Dataset Files:
- `literature review/LITERATURE_REVIEW.md` - Full review (47 papers)
- `literature review/RESEARCH_GAPS.md` - 20 gaps identified
- `literature review/papers/` - Detailed post-mortems

---

## 14. Quick Reference: Dataset Location

```
E:\CSE498R\Soil Moisture Detection\
├── dataset\
│   ├── raw\           # 722 original images
│   ├── clean\         # 722 normalized images
│   ├── preprocessed\  # CSVs, JSONs, splits
│   │   ├── image_manifest.csv
│   │   ├── split_assignment.csv
│   │   ├── anomalies.json
│   │   └── series_map.json
│   ├── scripts\       # Preprocessing pipeline
│   └── metadata\      # Annotation template
├── literature review\
│   ├── LITERATURE_REVIEW.md
│   ├── RESEARCH_GAPS.md
│   ├── SUPERVISOR_SUMMARY.md
│   └── papers\
└── docs\
```

---

## 15. Final Recommendation

### Primary Recommendation:

**Proceed with RGB + Tensiometer research in Bangladesh**

**Rationale:**
1. Novel contribution (no existing study)
2. Strong ground truth (tensiometer kPa)
3. Field validation (not just lab)
4. Bangladesh context (underrepresented)
5. Practical application (irrigation decisions)

### Expected Outcome:

> **"First study to predict soil matric potential (kPa) from field-captured RGB images in a tropical agricultural context, validated against tensiometer ground truth."**

### Success Criteria:

- R² > 0.85 (vs tensiometer)
- RMSE < 10 kPa
- Field-validated methodology
- Interpretable model decisions

---

**Prepared by:** Literature Review Analysis
**Date:** July 2026
**Status:** Ready for supervisor review

---

*End of Summary*
