# Paper Post-Mortem: CNN Classification FAILURE Analysis

**Published:** Jurnal Teknik Pertanian Lampung, April 2026
**Authors:** Suud et al.
**URL:** https://jurnal.fp.unila.ac.id/index.php/jtp/article/view/11703
**Relevance:** CRITICAL - Shows what CAN go wrong

---

## 1. Research Question and Motivation

**Question:** Can CNN classify soil moisture levels from in-situ RGB soil surface images?

**Motivation:**
- Computer vision offers real-time field monitoring
- Sensor-based measurements are limited
- Need non-invasive field assessment

**Goal:** Classify soil moisture into 2-4 categories

---

## 2. Dataset Details

| Aspect | Details |
|--------|---------|
| Total Images | 200 field-captured images |
| Location | Rainfed agricultural area |
| Conditions | Uncontrolled field environment |
| Categories | 2, 3, or 4 moisture levels |
| Resolution | Not specified |

**Critical Weakness:**
- **Only 200 images** - extremely small dataset
- **Field conditions** - uncontrolled lighting, debris
- **No preprocessing** - raw images used

---

## 3. Methods Used

### Models Tested:

| Model | Architecture | Approach |
|-------|-------------|----------|
| Traditional CNN | Custom architecture | Classification |
| ResNet-50 | 50-layer residual network | Transfer learning |

### Training:
- Standard classification setup
- 2, 3, and 4 category experiments
- No data augmentation mentioned

---

## 4. Key Results (THE FAILURE)

### Accuracy Degradation:

| Categories | CNN Accuracy | ResNet-50 Accuracy |
|------------|-------------|-------------------|
| 2 classes | 0.513 | 0.487 |
| 3 classes | 0.389 | 0.312 |
| 4 classes | 0.256 | 0.205 |

### RMSE Values:
- CNN: 0.433 - 0.507
- ResNet-50: 0.433 - 0.507

### Interpretation:
- **Random baseline for 2 classes = 0.50**
- CNN at 0.513 is **barely above random**
- **Models completely failed to learn**

---

## 5. Why The Models FAILED

### 5.1 Data Issues:

1. **Insufficient data:** 200 images far too small for deep learning
2. **Class imbalance:** Uneven distribution across moisture levels
3. **No augmentation:** Limited training examples
4. **Single location:** No geographic diversity

### 5.2 Environmental Issues:

5. **Inconsistent lighting:** Natural light varies dramatically
6. **Shadows:** Clouds, plants, objects cast shadows
7. **Non-soil objects:** Debris, leaves, rocks in images
8. **Surface heterogeneity:** Uneven soil appearance

### 5.3 Methodological Issues:

9. **Classification approach:** Moisture is continuous, not categorical
10. **No preprocessing:** Raw images without cleaning
11. **No feature engineering:** Relied solely on CNN
12. **No baseline comparison:** Didn't test simple color features

### 5.4 Fundamental Problem:

**"Soil moisture-related features are not sufficiently distinguishable under uncontrolled field conditions"**

---

## 6. Authors' Acknowledged Limitations

1. "Environmental variability dominates the visual signal"
2. "Inconsistent lighting, illumination, and non-soil objects"
3. "RGB-based in-situ imagery has limitations"
4. "Advanced pre-processing techniques needed"

---

## 7. What This Paper Teaches Us

### 7.1 Critical Lessons:

| Lesson | Implication |
|--------|------------|
| 200 images insufficient | Need 500+ minimum |
| Field images very different from lab | Must handle uncontrolled conditions |
| Classification wrong approach | Should use regression |
| RGB alone may not be enough | Consider additional features |
| Simple augmentation not enough | Need soil-specific preprocessing |

### 7.2 What Would Have Helped:

1. **More data:** 1000+ images minimum
2. **Preprocessing:** Soil segmentation, shadow removal
3. **Regression instead of classification:** Moisture is continuous
4. **Simple baselines:** Color histogram regression
5. **Data augmentation:** Rotation, flip, brightness, moisture simulation
6. **Controlled lighting:** Use consistent lighting conditions

---

## 8. How to Avoid The Same Pitfalls

### 8.1 Data Strategy:

| Instead of... | Do this... |
|---------------|-----------|
| 200 images | 500+ images |
| Raw field images | Preprocessed (segmented, normalized) |
| Single location | Multiple locations |
| No augmentation | Heavy augmentation |

### 8.2 Methodology:

| Instead of... | Do this... |
|---------------|-----------|
| Classification | Regression |
| Raw RGB | Color features + deep learning |
| No preprocessing | Soil segmentation pipeline |
| No baselines | Compare with color regression |

### 8.3 Evaluation:

| Instead of... | Do this... |
|---------------|-----------|
| Single train/test | k-fold cross-validation |
| Accuracy only | RMSE, MAE, R², MAPE |
| No uncertainty | Confidence intervals |
| No error analysis | Per-sample error visualization |

---

## 9. Relevance to Our Work

### Our Advantages Over This Study:

1. **722 images** (vs 200) - 3.6× more data
2. **Tensiometer ground truth** - precise measurements
3. **Controlled acquisition** - consistent conditions
4. **Regression approach** - appropriate for continuous variable
5. **Preprocessing pipeline** - already developed

### Our Risks to Mitigate:

1. **Field conditions:** Images captured in field, not lab
2. **Lighting variation:** Different times of day
3. **Non-soil objects:** May be debris in images
4. **Class imbalance:** 66.8% in 10-20 kPa range

### Recommended Safeguards:

1. **Soil segmentation:** Remove non-soil regions
2. **Lighting normalization:** Histogram equalization
3. **Heavy augmentation:** Rotation, flip, brightness, contrast
4. **Simple baselines:** Compare with color feature regression
5. **Cross-validation:** k-fold for robust evaluation

---

## 10. Key Takeaways for PhD Research

### Critical Warnings:

⚠️ **Field RGB images are MUCH harder than lab images**
⚠️ **200 images is insufficient for deep learning**
⚠️ **Classification is wrong approach for continuous variables**
⚠️ **RGB alone may not capture moisture differences**

### Actionable Insights:

✅ **Use 500+ images minimum** (we have 722)
✅ **Use regression, not classification**
✅ **Preprocess aggressively** (segmentation, normalization)
✅ **Compare with simple baselines** (color regression)
✅ **Use cross-validation** (k-fold)
✅ **Report multiple metrics** (RMSE, MAE, R²)

### Our Defense Against Failure:

1. **Tensiometer ground truth** provides precise labels
2. **Preprocessing pipeline** handles image quality
3. **Larger dataset** (722 vs 200)
4. **Regression approach** matches problem nature
5. **Multiple baselines** ensure fair comparison

---

## Conclusion

This paper is a **cautionary tale** that validates our approach:
- We have more data (722 vs 200)
- We have better labels (tensiometer vs visual)
- We use regression (not classification)
- We have preprocessing pipeline

**If we fail, it won't be for the same reasons.**

---

*End of Post-Mortem*
