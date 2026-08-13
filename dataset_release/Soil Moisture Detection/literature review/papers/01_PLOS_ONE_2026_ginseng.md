# Paper Post-Mortem: Image-based ML for customized soil moisture management

**Published:** PLOS ONE, February 2026
**URL:** https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0341904
**Relevance:** HIGHEST - Closest methodology to our work

---

## 1. Research Question and Motivation

**Question:** Can RGB images of soil surface predict soil moisture at different depths for customized crop management?

**Motivation:**
- Conventional smart farming applies uniform treatments to all crops
- Crop growth varies due to microenvironments and physiological differences
- Need non-invasive methods to monitor soil conditions at individual plant level

**Gap Addressed:** Lack of non-invasive, plant-level soil moisture monitoring

---

## 2. Dataset Details

| Aspect | Details |
|--------|---------|
| Crop | Wild-simulated ginseng (model crop) |
| Image Source | iPhone 12 Pro RGB camera |
| Sensor Depths | 3 cm, 10 cm, 15 cm |
| Environment | Controlled greenhouse |
| Lighting | Natural (1:00 PM - 3:00 PM) |
| Image Processing | OpenCV, resize to 224×224, normalize 0-1 |
| Color Space | RGB preserved (no grayscale/HSV conversion) |

**Strengths:**
- Multi-depth sensor data
- Real smartphone camera used
- Natural lighting conditions

**Weaknesses:**
- Controlled greenhouse only
- Single crop type (ginseng)
- No field validation
- Limited depth range (0-15 cm)

---

## 3. Methods Used

### Models Tested (6 architectures):

| Model | Type | Parameters | Best Performance |
|-------|------|-----------|------------------|
| DenseNet121 | Dense connectivity | 8.08M | R²=97.3%, RMSE=4.14 |
| EfficientNetB0 | Compound scaling | 5.36M | R²=96.9%, RMSE=4.14 |
| ResNet50 | Residual blocks | 25.6M | Good |
| InceptionV3 | Inception modules | 23.8M | Good |
| MobileNetV2 | Lightweight | 3.4M | Moderate |
| NASNetMobile | Neural architecture search | 5.3M | Moderate |
| Random Forest | Ensemble (depth layers) | - | R²=90.6%, RMSE=4.97 |

### Architecture:
```
Input (224×224×3) → Pre-trained CNN → Global Average Pooling 
→ Dense(1024, ReLU) → Dense(1, Linear) → Output
```

### Training:
- Transfer learning from ImageNet
- Modified final layers for regression
- Hyperparameters: trial-and-error

**Strengths:**
- Comprehensive model comparison
- Transfer learning approach
- Both surface and depth prediction

**Weaknesses:**
- No hyperparameter optimization strategy
- No cross-validation mentioned
- No ablation studies

---

## 4. Key Results

### Surface Moisture Prediction:

| Model | R² | RMSE | MAE | Parameters |
|-------|-----|------|-----|-----------|
| DenseNet121 | 97.3% | 4.14 | 2.07 | 8.08M |
| EfficientNetB0 | 96.9% | - | 2.14 | 5.36M |
| Random Forest | 90.6% | 4.97 | - | - |

### Key Findings:
1. DenseNet121 best overall (R²=97.3%)
2. Dense connectivity enables feature reuse
3. Surface image can predict subsurface moisture
4. Upper-layer moisture predicts deeper layers

---

## 5. Limitations Acknowledged by Authors

1. **Controlled conditions:** "Future studies should validate across diverse crops and soil types"
2. **Single crop:** Used only ginseng as model crop
3. **Limited spectral data:** "Integrate additional spectral data to enhance robustness"
4. **No field validation:** Tested only in greenhouse

---

## 6. Limitations NOT Acknowledged (Hidden Weaknesses)

### 6.1 Methodological Concerns:

1. **No cross-validation:** Single train/test split, no k-fold
2. **No statistical significance:** No confidence intervals or p-values
3. **No comparison with simple baselines:** Didn't compare with color histogram regression
4. **Hyperparameter selection:** "Trial-and-error" is not rigorous

### 6.2 Data Concerns:

5. **No data augmentation mentioned:** May overfit to specific conditions
6. **No temporal variation:** Single time-point images
7. **No lighting variation:** Fixed time window (1-3 PM)
8. **No soil type diversity:** Single soil in greenhouse

### 6.3 Experimental Design:

9. **Sensor placement:** Sensors at fixed depths, not randomized
10. **Image-sensor pairing:** Assumed spatial correspondence
11. **No noise analysis:** How robust to image noise?
12. **No occlusion handling:** What if plants block soil?

---

## 7. Experimental Design Flaws

### 7.1 Potential Overfitting Risk:
- DenseNet121 (8.08M parameters) on limited greenhouse data
- No validation curve shown
- No early stopping mentioned

### 7.2 Spatial Correspondence Assumption:
- Assumes image pixels correspond to sensor depths
- No validation of this assumption
- Could be spurious correlation

### 7.3 Temporal Confounding:
- Images captured at same time as sensor readings
- May learn time-specific patterns, not moisture
- No temporal separation of train/test

---

## 8. Comparison with Baselines

### What They Compared:
- 6 deep learning architectures
- Random Forest for depth layers

### What They Did NOT Compare:
1. **Simple color features:** RGB mean, HSV statistics
2. **Traditional ML with handcrafted features:** Color histograms, texture features
3. **Linear regression:** Baseline performance
4. **Physical models:** Soil water retention curves

**Fairness Concern:** Comparing only complex models may overstate performance

---

## 9. Reproducibility Concerns

### 9.1 Missing Details:
- Exact dataset size not specified
- Train/test split ratio not mentioned
- Hyperparameters not reported
- Random seed not specified

### 9.2 Code Availability:
- No code repository mentioned
- No model weights shared

### 9.3 Data Availability:
- No dataset shared
- No data collection protocol described

---

## 10. What They Did NOT Try But Should Have

1. **Cross-validation:** Essential for small datasets
2. **Data augmentation:** Would improve generalization
3. **Attention visualization:** Would explain what features matter
4. **Simple baselines:** Color-based regression
5. **Uncertainty quantification:** Confidence intervals
6. **Temporal validation:** Different time points
7. **Lighting variation:** Different lighting conditions
8. **Multi-crop validation:** Generalizability

---

## 11. Relevance to Our Work

### What We Can Learn:

1. **DenseNet121 architecture:** Good baseline for RGB soil moisture
2. **Transfer learning works:** ImageNet pre-training beneficial
3. **Sensor-imagery pairing:** Valid approach for multi-depth prediction
4. **RGB is sufficient:** No need for multispectral in controlled conditions

### What We Should Do Differently:

1. **Add cross-validation:** k-fold for robust evaluation
2. **Test in field conditions:** Not just greenhouse
3. **Compare with simple baselines:** Color features + regression
4. **Use tensiometer ground truth:** Not just VWC
5. **Report uncertainty:** Confidence intervals

---

## 12. Key Takeaways for PhD Research

### Positive:
- RGB images CAN predict soil moisture (R²=97.3%)
- Transfer learning from ImageNet is effective
- DenseNet121 is a strong baseline
- Multi-depth prediction is feasible

### Cautionary:
- Greenhouse results may not transfer to field
- Need rigorous validation (cross-validation, statistics)
- Simple baselines may perform comparably
- Dataset diversity is critical

### Actionable:
1. Use DenseNet121 as baseline model
2. Implement k-fold cross-validation
3. Test in field conditions
4. Compare with color-based regression
5. Report confidence intervals

---

*End of Post-Mortem*
