# Research Gaps Analysis: Soil Moisture Estimation from Images

**Project:** CSE498R - Soil Moisture Detection
**Generated:** July 2026
**Purpose:** Identify research gaps and opportunities for PhD contribution

---

## Executive Summary

After analyzing **47 papers** across 5 categories, we identified **20 significant research gaps** organized into 4 tiers:

- **Tier 1 (Critical):** 5 gaps that represent novel contributions
- **Tier 2 (High):** 5 gaps that extend existing work
- **Tier 3 (Medium):** 5 gaps that improve methodology
- **Tier 4 (Application):** 5 gaps for practical deployment

---

## Tier 1: Critical Gaps (Novel Contributions)

### Gap 1: RGB Image + Tensiometer Ground Truth Validation

**Status:** NO EXISTING STUDY

**What exists:**
- Image-based studies use lab conditions or satellite data
- Sensor studies validate sensors against each other
- No study combines RGB images with tensiometer readings

**Why it matters:**
- Tensiometers measure matric potential (kPa) - what plants actually experience
- Most studies use volumetric water content (VWC) - less directly relevant to plant stress
- Our dataset uniquely provides both RGB images AND tensiometer readings (0-101 kPa)

**Our contribution:**
- First study to predict kPa from RGB images
- Direct comparison of image-based prediction vs tensiometer measurement
- Bridge between visual and physical soil moisture assessment

**Difficulty:** Medium
**Impact:** Very High

---

### Gap 2: Field-Captured RGB Image Processing

**Status:** FAILED ATTEMPTS ONLY

**What exists:**
- Suud et al. (2026) attempted field images → FAILED (R²=0.205-0.513)
- All successful studies use controlled lab/greenhouse conditions
- Failure attributed to: inconsistent lighting, shadows, non-soil objects

**Why it matters:**
- Real-world applications require field conditions
- Lab results don't transfer to field
- Need robust preprocessing for uncontrolled environments

**Our contribution:**
- Develop preprocessing pipeline for field RGB images
- Address lighting variation, shadows, debris
- Demonstrate field-robust prediction

**Difficulty:** High
**Impact:** Very High

---

### Gap 3: Bangladesh-Specific Image-Based Study

**Status:** NO EXISTING STUDY

**What exists:**
- Bangladesh IoT studies (Dey 2024, Ahmed 2024, Sarkar 2024, Das 2025)
- Bangladesh weather-soil correlation (Banna 2024)
- NO image-based soil moisture studies

**Why it matters:**
- Bangladesh: tropical climate, specific soil types
- Major rice-producing region
- Water scarcity and irrigation challenges
- Need context-specific solutions

**Our contribution:**
- First image-based soil moisture study in Bangladesh
- Validate in tropical, monsoon climate
- Contribute to local agricultural knowledge

**Difficulty:** Low (we have the data)
**Impact:** High

---

### Gap 4: Continuous Regression from Tensiometer Scale (0-101 kPa)

**Status:** NO EXISTING STUDY

**What exists:**
- Most studies use volumetric water content (VWC)
- Classification approaches (dry/wet/extremely wet)
- Limited kPa-based studies

**Why it matters:**
- Tensiometers naturally output kPa
- Farmers think in terms of irrigation thresholds (e.g., irrigate at 60 kPa)
- Direct kPa prediction enables practical irrigation decisions

**Our contribution:**
- Direct regression from RGB to kPa
- Map visual features to matric potential
- Enable threshold-based irrigation triggers

**Difficulty:** Medium
**Impact:** High

---

### Gap 5: Multi-Depth Prediction from Single RGB Image

**Status:** LIMITED EXISTENCE

**What exists:**
- PLOS ONE (2026): predicts 3 depths from RGB
- Most studies: only surface moisture
- No study predicts root-zone from surface image

**Why it matters:**
- Surface moisture ≠ root-zone moisture
- Plants extract water from root zone
- Non-invasive deep prediction valuable

**Our contribution:**
- Predict multiple depths from single RGB image
- Validate against tensiometer at different depths
- Develop depth-aware model architecture

**Difficulty:** High
**Impact:** Very High

---

## Tier 2: High-Priority Gaps (Extensions)

### Gap 6: Attention Mechanism for Soil Moisture

**Status:** LIMITED EXISTENCE

**What exists:**
- Zhang et al. (2024): LG-SWC-R3 with attention
- No other attention-based soil moisture studies

**Our contribution:**
- Apply Transformer attention to RGB soil moisture
- Visualize attention maps for interpretability
- Compare with CNN-based approaches

**Difficulty:** Medium
**Impact:** Medium-High

---

### Gap 7: Ensemble Stacking for Image-Based Prediction

**Status:** NO EXISTING STUDY

**What exists:**
- SABM stacking successful in remote sensing (R²=0.861)
- No stacking for image-based soil moisture

**Our contribution:**
- Apply stacking ensemble to RGB models
- Combine DenseNet, ResNet, EfficientNet
- Improve robustness and accuracy

**Difficulty:** Medium
**Impact:** Medium-High

---

### Gap 8: Interpretable ML for Visual Feature Analysis

**Status:** LIMITED EXISTENCE

**What exists:**
- Indian soils study uses IML
- No other interpretability studies

**Our contribution:**
- SHAP/LIME analysis for soil moisture
- Identify which visual features predict moisture
- Color? Texture? Moisture patterns?

**Difficulty:** Medium
**Impact:** Medium

---

### Gap 9: Data Augmentation for Soil Images

**Status:** NO SYSTEMATIC STUDY

**What exists:**
- Basic augmentation (flip, rotate, brightness)
- No comparison of augmentation strategies

**Our contribution:**
- Systematic comparison of augmentation methods
- Soil-specific augmentation (moisture simulation)
- Optimal augmentation pipeline

**Difficulty:** Low
**Impact:** Medium

---

### Gap 10: Transfer Learning Across Soil Types

**Status:** LIMITED EXISTENCE

**What exists:**
- Singh et al. (2025): transfer learning for satellite data
- No transfer learning for RGB soil images

**Our contribution:**
- Train on one soil, test on another
- Cross-region model transferability
- Few-shot learning for new soils

**Difficulty:** High
**Impact:** Medium-High

---

## Tier 3: Medium-Priority Gaps (Methodology)

### Gap 11: Large-Scale Public RGB Soil Moisture Dataset

**Status:** DOES NOT EXIST

**What exists:**
- Small private datasets (200-3175 images)
- No standardized benchmark

**Our contribution:**
- Publish our dataset (722 images + tensiometer readings)
- Standardized evaluation protocol
- Enable reproducible research

**Difficulty:** Low
**Impact:** High

---

### Gap 12: Temporal Dynamics in RGB Images

**Status:** NO EXISTING STUDY

**What exists:**
- Time-series in satellite data
- Single time-point in RGB studies

**Our contribution:**
- Temporal analysis of soil images
- Diurnal variation effects
- Weather impact on visual appearance

**Difficulty:** Medium
**Impact:** Medium

---

### Gap 13: Multi-Resolution Comparison

**Status:** NO SYSTEMATIC STUDY

**What exists:**
- Different studies use different resolutions
- No comparison study

**Our contribution:**
- Test multiple resolutions (224×224 to 1024×1024)
- Optimal resolution for prediction
- Resolution vs accuracy trade-off

**Difficulty:** Low
**Impact:** Low-Medium

---

### Gap 14: Lighting Condition Robustness

**Status:** LIMITED EXISTENCE

**What exists:**
- Hossain et al. (2023): direct vs indirect sunlight
- No other lighting studies

**Our contribution:**
- Systematic lighting variation study
- Shadow removal techniques
- Illumination normalization

**Difficulty:** Medium
**Impact:** Medium

---

### Gap 15: Non-Soil Object Segmentation

**Status:** NO SYSTEMATIC STUDY

**What exists:**
- Suud et al. acknowledges this as failure cause
- No robust segmentation solution

**Our contribution:**
- Soil segmentation models
- Debris/plant removal
- Clean soil region extraction

**Difficulty:** Medium
**Impact:** Medium-High

---

## Tier 4: Application Gaps

### Gap 16: Smartphone App for Farmers

**Status:** RESEARCH ONLY

**What exists:**
- Research prototypes
- No deployed apps

**Our contribution:**
- Develop mobile app prototype
- Real-time moisture estimation
- Farmer-friendly interface

**Difficulty:** High
**Impact:** Very High

---

### Gap 17: Real-Time RGB Monitoring System

**Status:** NO EXISTING SYSTEM

**What exists:**
- IoT systems with physical sensors
- No image-based real-time systems

**Our contribution:**
- Camera + edge computing system
- Continuous monitoring
- Alert system for irrigation

**Difficulty:** High
**Impact:** High

---

### Gap 18: Irrigation Scheduling from RGB Images

**Status:** NO EXISTING SYSTEM

**What exists:**
- Moisture estimation studies
- Irrigation scheduling from sensor data
- No image-to-irrigation pipeline

**Our contribution:**
- Link moisture prediction to irrigation decisions
- Threshold-based triggers
- Water saving potential

**Difficulty:** High
**Impact:** Very High

---

### Gap 19: Multi-Crop Validation

**Status:** LIMITED EXISTENCE

**What exists:**
- Single crop studies (ginseng, rice, etc.)
- No crop-agnostic validation

**Our contribution:**
- Test across multiple crop types
- Crop-agnostic model development
- Generalizable solution

**Difficulty:** Medium
**Impact:** Medium

---

### Gap 20: Cost-Benefit Analysis

**Status:** NO EXISTING STUDY

**What exists:**
- Cost mentioned in sensor studies
- No comparison of image vs sensor approaches

**Our contribution:**
- Economic feasibility study
- ROI comparison: image vs sensor
- Scalability analysis

**Difficulty:** Low
**Impact:** Medium-High

---

## Recommended Research Directions

### For This PhD Project (Priority Order):

1. **Gap 1 + 3 + 4:** RGB + tensiometer in Bangladesh (Novel + Context + Practical)
2. **Gap 2:** Field-robust image processing (Addresses real-world challenge)
3. **Gap 5:** Multi-depth prediction (Extends scientific contribution)
4. **Gap 11:** Publish dataset (Enables future research)
5. **Gap 8:** Interpretable ML (Explains model behavior)

### For Future Work:

6. **Gap 7:** Ensemble stacking (Improves accuracy)
7. **Gap 10:** Transfer learning (Enables generalization)
8. **Gap 16:** Smartphone app (Practical deployment)
9. **Gap 18:** Irrigation scheduling (Real-world impact)

---

## Alignment with Our Dataset

| Gap | Our Dataset Support | Status |
|-----|-------------------|--------|
| Gap 1: RGB + Tensiometer | 722 images + kPa readings | ✅ READY |
| Gap 2: Field conditions | Images captured in field | ✅ READY |
| Gap 3: Bangladesh context | Pabna District, Bangladesh | ✅ READY |
| Gap 4: kPa regression | 0-101 kPa range | ✅ READY |
| Gap 5: Multi-depth | 10-20 kPa dominant | ⚠️ Limited |
| Gap 11: Public dataset | 722 images available | ✅ READY |

---

## Conclusion

**Our dataset is uniquely positioned to address 6 of the 20 identified research gaps.**

The most promising contribution would be:
> **"First study to predict soil matric potential (kPa) from field-captured RGB images in a tropical agricultural context, validated against tensiometer ground truth."**

This addresses:
- Novel methodology (RGB → kPa)
- Real-world conditions (field, not lab)
- Specific context (Bangladesh tropical agriculture)
- Practical application (irrigation decisions)

---

*End of Research Gaps Analysis*
