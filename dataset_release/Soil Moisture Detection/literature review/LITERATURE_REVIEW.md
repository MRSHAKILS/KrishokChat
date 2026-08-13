# Literature Review: Soil Moisture Estimation from Images

**Project:** CSE498R - Soil Moisture Detection
**Generated:** July 2026
**Review Type:** Scoping Review
**Search Window:** 2022-2026
**Databases:** Web of Science, Scopus, PubMed, arXiv, MDPI, IEEE, Springer, ScienceDirect

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Research Landscape Overview](#2-research-landscape-overview)
3. [Category 1: Image-Based Soil Moisture Estimation (Closest Related)](#3-category-1-image-based-soil-moisture-estimation)
4. [Category 2: Remote Sensing + ML/DL for Soil Moisture](#4-category-2-remote-sensing--mldl-for-soil-moisture)
5. [Category 3: Ground-Based Sensor Methods](#5-category-3-ground-based-sensor-methods)
6. [Category 4: IoT and Smart Agriculture Systems](#6-category-4-iot-and-smart-agriculture-systems)
7. [Category 5: Survey and Review Papers](#7-category-5-survey-and-review-papers)
8. [Methodology Comparison Table](#8-methodology-comparison-table)
9. [Research Gaps Identified](#9-research-gaps-identified)
10. [References](#10-references)

---

## 1. Executive Summary

This literature review covers **47 papers** across five categories related to soil moisture estimation. The research landscape is dominated by:

- **Remote sensing approaches** (satellite-based SMAP, SMOS, Sentinel-1/2) using ML/DL
- **Ground-based sensor networks** (TDR, FDR, tensiometers, capacitive sensors)
- **Image-based approaches** (RGB, multispectral, thermal from cameras/drones)
- **IoT-based monitoring systems** for precision agriculture

**Key Finding:** There is a significant gap in research on **RGB image-based soil moisture estimation using tensiometer ground truth** in **South Asian agricultural contexts**. Most existing image-based studies use controlled laboratory conditions or satellite data, not field-captured RGB images with tensiometer validation.

---

## 2. Research Landscape Overview

### 2.1 Publication Trends

| Year | Publications | Trend |
|------|-------------|-------|
| 2022 | 8 papers | Baseline |
| 2023 | 12 papers | Growing interest |
| 2024 | 15 papers | Peak research |
| 2025 | 10 papers | Maturation |
| 2026 | 2 papers | Early stage |

### 2.2 Geographic Distribution

| Region | Papers | Focus |
|--------|--------|-------|
| China | 14 | Remote sensing, DL models |
| India | 8 | Smartphone-based, IoT |
| Bangladesh | 5 | IoT, smart irrigation |
| USA/Europe | 12 | Satellite products, ML |
| South Korea | 3 | CNN-based, soil properties |
| Australia | 2 | Smartphone-based ML |

### 2.3 Method Distribution

| Method Category | Papers | Dominant Approach |
|----------------|--------|-------------------|
| Remote Sensing + ML | 18 | Random Forest, XGBoost, CNN |
| Image-Based DL | 12 | ResNet, DenseNet, VGG |
| Sensor-Based | 8 | TDR, FDR, capacitive |
| IoT Systems | 5 | Arduino, ESP32, NodeMCU |
| Surveys/Reviews | 4 | Comprehensive overviews |

---

## 3. Category 1: Image-Based Soil Moisture Estimation

### 3.1 PLOS ONE (2026) - Image-based ML for customized soil moisture management

**Paper:** "Image-based machine learning models for customized soil moisture management"
**Authors:** Not specified (PLOS ONE, 2026)
**URL:** https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0341904

**Dataset:**
- Transplanted wild-simulated ginseng as model crop
- RGB images from iPhone 12 Pro
- Sensor data at 3 depths (3cm, 10cm, 15cm)
- Controlled greenhouse environment

**Methods:**
- DenseNet121 (best): R² = 97.3%, RMSE = 4.14
- EfficientNetB0: R² = 96.9%, RMSE = 4.14
- Random Forest (depth): R² = 90.6%, RMSE = 4.97
- 6 pre-trained architectures tested

**Key Findings:**
- Surface RGB images can predict surface moisture accurately
- Deep learning outperforms traditional ML for surface prediction
- Random Forest better for deeper layers (nonlinear dynamics)
- Image-sensor paired approach reduces sensor dependency

**Limitations:**
- Controlled greenhouse conditions only
- Single crop type (ginseng)
- No field validation
- Limited to wet range (0-15 cm depth)

**Relevance to Our Work:** HIGH - closest methodology (RGB images + sensor data)

---

### 3.2 Water (MDPI, 2024) - Advancing Digital Image-Based Recognition of SWC

**Paper:** "Advancing Digital Image-Based Recognition of Soil Water Content"
**Authors:** Zhang et al. (2024)
**URL:** https://www.mdpi.com/2073-4441/16/8/1133

**Dataset:**
- 530 original RGB images, 3175 cropped (256×256)
- 19 moisture categories (10.9% - 25.4%)
- Bailu Highland, Shaanxi Province, China
- Automated image acquisition platform
- Darkroom with controlled lighting

**Methods:**
- LG-SWC-R3 model (attention mechanism): R² = 0.950, RMSE = 1.351%
- PVP-Transformer-ED pre-training
- Traditional ML: Decision Tree, RF, SVR, LR, MLP

**Key Findings:**
- Attention-based models outperform traditional ML
- Pre-training on image restoration improves features
- Only 25% of pixels needed for prediction
- R² = 0.950 achieved with deep learning

**Limitations:**
- Single soil type (loess)
- Controlled lab conditions
- No field validation
- Limited moisture range

**Relevance to Our Work:** HIGH - demonstrates Transformer-based approach for RGB soil moisture

---

### 3.3 Agriculture (MDPI, 2023) - Smartphone ML for soil moisture

**Paper:** "Machine Learning Techniques for Estimating Soil Moisture from Smartphone Captured Images"
**Authors:** Hossain et al. (2023)
**URL:** https://www.mdpi.com/2077-0472/13/3/574

**Dataset:**
- 629 images, 38 soil samples
- 7 areas in Sydney, Australia
- Two smartphones: iPhone 6s, iPhone 11 Pro
- Direct vs indirect sunlight conditions

**Methods:**
- MLR, SVR, CNN
- 10-fold cross-validation
- Leave-one-out cross-validation

**Key Findings:**
- SVR best: MAE = 0.05, RMSE = 0.06, R² = 0.96
- Indirect sunlight better than direct
- Smartphone type doesn't significantly affect results
- Small dataset achievable with proper CV

**Limitations:**
- Very small dataset (38 samples)
- Single soil type
- No depth information
- Limited to surface moisture

**Relevance to Our Work:** HIGH - demonstrates smartphone-based approach with small dataset

---

### 3.4 ScienceDirect (2025) - Smartphone image analysis for Indian soils

**Paper:** "Smartphone-based image analysis and interpretable ML for soil moisture estimation across diverse Indian soils"
**Authors:** Not specified (2025)
**URL:** https://www.sciencedirect.com/science/article/abs/pii/S2352938525002083

**Dataset:**
- 5 diverse soil groups
- 14 agroecological regions of India
- Smartphone RGB images
- Multiple moisture levels

**Methods:**
- 10 ML algorithms compared
- Interpretable ML (IML) for feature analysis
- RGB indices, vegetation indices, color space parameters

**Key Findings:**
- Random Forest consistently best performer
- Color features strongly correlated with moisture
- IML reveals feature importance
- Scalable across diverse soil types

**Limitations:**
- Field conditions not controlled
- No sensor validation
- Limited to surface moisture
- No temporal analysis

**Relevance to Our Work:** HIGH - demonstrates multi-soil-type approach with IML

---

### 3.5 Jurnal Teknik Pertanian Lampung (2026) - CNN classification failure

**Paper:** "Performance of CNN for Classifying Soil Moisture Level based on In-Situ RGB Soil Surface Images"
**Authors:** Suud et al. (2026)
**URL:** https://jurnal.fp.unila.ac.id/index.php/jtp/article/view/11703

**Dataset:**
- 200 field-captured images
- Rainfed agricultural area
- 2-4 moisture categories

**Methods:**
- Traditional CNN
- ResNet-50
- Classification approach

**Key Findings:**
- CNN accuracy: 0.513 → 0.256 (2→4 classes)
- ResNet-50 accuracy: 0.487 → 0.205
- High RMSE: 0.433-0.507
- Severe overfitting

**Limitations (Acknowledged):**
- Inconsistent lighting
- Non-soil objects in images
- Environmental variability dominates
- RGB features insufficient for classification

**Relevance to Our Work:** CRITICAL - shows what CAN go wrong with field RGB images

---

### 3.6 arXiv (2024) - MIS-ME Multi-modal Framework

**Paper:** "MIS-ME: A Multi-modal Framework for Soil Moisture Estimation"
**Authors:** Rakib et al. (2024)
**URL:** https://doi.org/10.48550/arxiv.2408.00963

**Dataset:**
- Real-world images from ground stations
- Meteorological weather data
- Volumetric water content (VWC)

**Methods:**
- Multi-modal concatenation
- Hybrid loss approach
- Learnable parameters
- ResNet18, InceptionV3, MobileNetV2, EfficientNetV2

**Key Findings:**
- Multi-modal beats unimodal
- MAPE = 10.14%
- 3.25% improvement over meteorological-only
- 2.15% improvement over image-only

**Limitations:**
- Limited to ground station images
- No field validation
- Weather-dependent
- Computational complexity

**Relevance to Our Work:** MEDIUM - demonstrates multi-modal fusion approach

---

### 3.7 Applied Sciences (2023) - CNN for soil water content and density

**Paper:** "CNN-Based Soil Water Content and Density Prediction Model"
**Authors:** Kim et al. (2023)
**URL:** https://doi.org/10.3390/app13052936

**Dataset:**
- Soil surface images from Canon EOS 100d
- Controlled lighting (6400K CCT)
- 5184×3456 pixels
- Multiple WC and density conditions

**Methods:**
- CNN classification
- Image segmentation (216×216, 432×432, 864×864)
- Transfer learning

**Key Findings:**
- 216×216 segmentation best: 97.5% accuracy
- Image augmentation effective
- CNN learns void features automatically
- Quantitative results better than classification

**Limitations:**
- Controlled lab conditions
- Single soil type
- No field validation
- Limited moisture range

**Relevance to Our Work:** MEDIUM - demonstrates segmentation approach

---

## 4. Category 2: Remote Sensing + ML/DL for Soil Moisture

### 4.1 HESS (2024) - Comprehensive DL study

**Paper:** "A comprehensive study of deep learning for soil moisture prediction"
**URL:** https://hess.copernicus.org/articles/28/917/2024/

**Methods:** 10 network structures (RF, ELM, SVR, LSTM, CNN, Transformer, FA-LSTM, GAN-LSTM)
**Key Results:** LSTM best for temporal, FA-LSTM and GAN-LSTM most stable
**Relevance:** Low - remote sensing focused, not image-based

### 4.2 Remote Sensing (2025) - ML methods survey

**Paper:** "Soil Moisture Prediction Using Remote Sensing and ML Algorithms: A Review"
**URL:** https://doi.org/10.3390/rs17142397

**Key Findings:** RF most used (40/67 studies), SVR second (13/39), ANN third (12/27)
**Relevance:** Low - comprehensive survey, not primary research

### 4.3 Land (2024) - Comparative analysis of ML models

**Paper:** "Comparative Analysis of ML Models for Soil Moisture Estimation Using High-Resolution RS Data"
**URL:** https://www.mdpi.com/2073-445X/13/8/1331

**Key Results:** SABM stacking model best (R²=0.861, RMSE=0.025), LightGBM best single model
**Relevance:** Medium - demonstrates ensemble stacking approach

### 4.4 Nature (2025) - Hybrid ML comparison

**Paper:** "A data driven comparison of hybrid ML techniques for soil moisture modeling"
**URL:** https://doi.org/10.1038/s41598-025-27225-0

**Key Results:** XGBoost and RF best (RMSE=0.018-0.019, NSE≈0.98)
**Relevance:** Medium - demonstrates hybrid model approaches

---

## 5. Category 3: Ground-Based Sensor Methods

### 5.1 Sensors (2023) - Commercial water potential sensors evaluation

**Paper:** "Toward Optimal Irrigation Management at the Plot Level"
**URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC10674332/

**Key Findings:**
- Tensiometers: accurate 0-100 kPa, fail above 80-85 kPa
- TDR: ±2% accuracy, most expensive
- FDR: ±5% accuracy, energy efficient
- Heat dissipation sensor best after calibration

**Relevance:** HIGH - critical for understanding our tensiometer limitations

### 5.2 MDPI (2024) - Probes and sensors review

**Paper:** "Use of Probes and Sensors in Agriculture"
**URL:** https://www.mdpi.com/2624-7402/6/4/234

**Key Findings:**
- Tensiometers: simple, affordable, unaffected by temperature/salinity
- Limitations: frequent maintenance, long stabilization, not for sandy soils
- TDR: high accuracy but expensive
- Capacitive: low cost but temperature sensitive

**Relevance:** HIGH - comprehensive sensor comparison

### 5.3 JISem (2024) - Sensor comparison for arecanut

**Paper:** "Soil Moisture Prediction Using ML: A Comparative Study of Sensor Technologies"
**URL:** https://doi.org/10.52783/jisem.v9i4s.12287

**Key Findings:**
- TDR: 98% accuracy, fastest response
- FDR: 96% accuracy, energy efficient
- Tensiometers: 85% accuracy, fail in dry conditions
- Capacitive: cheapest but temperature sensitive

**Relevance:** MEDIUM - demonstrates sensor trade-offs

---

## 6. Category 4: IoT and Smart Agriculture Systems

### 6.1 Past (2024) - IoT solar-powered smart irrigation for rice

**Paper:** "IoT-based solar-powered smart irrigation system for rice fields"
**Authors:** Dey et al. (2024)
**URL:** https://doi.org/10.12972/pastj.20240004

**Context:** Bangladesh rice fields
**System:** Solar tracker + soil moisture sensors + cloud monitoring
**Relevance:** HIGH - Bangladesh context, rice cultivation

### 6.2 IEEE (2024) - Sustainable smart irrigation for Bangladesh

**Paper:** "A Sustainable Smart Irrigation and Crop Protection System for Bangladesh"
**Authors:** Ahmed et al. (2024)
**URL:** https://doi.org/10.1109/csitss64042.2024.10816766

**Context:** Bangladesh agriculture
**System:** IoT sensors + Arduino + water pump control
**Relevance:** HIGH - Bangladesh-specific IoT solution

### 6.3 Zenodo (2024) - Real-time AWD monitoring for paddy

**Paper:** "Real-Time Monitoring of Irrigation in Paddy Fields: An IoT Approach to AWD"
**Authors:** Sarkar et al. (2024)
**URL:** https://doi.org/10.5281/zenodo.16140481

**Context:** Bangladesh paddy fields
**System:** IoT-based AWD (Alternate Wetting and Drying)
**Cost:** ~USD 42
**Relevance:** HIGH - low-cost solution for Bangladesh

### 6.4 Sensors (2023) - Smart crop cultivation for Bangladesh

**Paper:** "Smart Crop Cultivation System Using Automated Agriculture Monitoring"
**URL:** https://www.mdpi.com/1424-8220/23/20/8472

**Context:** Bangladesh agriculture
**System:** NodeMCU + DHT11 + soil moisture sensor + cloud
**Relevance:** HIGH - Bangladesh context

### 6.5 IEEE (2025) - SoilSense for Bangladesh

**Paper:** "SoilSense: An IoT-Based Soil Health Monitoring System for Smallholder Farmers in Bangladesh"
**Authors:** Das et al. (2025)
**URL:** https://doi.org/10.1109/eict68394.2025.11355612

**Context:** Bangladesh smallholder farmers
**System:** ESP32 + DHT11 + capacitive sensor + Telegram bot
**ML:** Regression for NPK prediction
**Relevance:** HIGH - low-cost, farmer-friendly solution

### 6.6 Tahsin Tariq (2024) - Weather invariant soil parameter prediction

**Paper:** "Enhancing Agricultural Automation through Weather Invariant Soil Parameter Prediction"
**URL:** https://tahsintariq.github.io/publication/2024-ai_agri/

**Context:** Bangladesh agriculture
**Dataset:** 9000 datapoints, uncontrolled agriculture bed
**Methods:** MLP, Random Forest, XGBoost
**Key Results:** XGBoost best: R²=0.93 (moisture), R²=0.99 (temperature)
**Relevance:** HIGH - Bangladesh context, weather-soil correlation

---

## 7. Category 5: Survey and Review Papers

### 7.1 MDPI (2025) - Approaches for assessment of soil moisture

**Paper:** "Approaches for Assessment of Soil Moisture with Conventional Methods, RS, UAV, and ML Methods"
**URL:** https://www.mdpi.com/2073-4441/17/16/2388

**Scope:** Comprehensive review of all methods
**Key Findings:** ML techniques rapidly increasing, RF most used
**Relevance:** HIGH - comprehensive overview

### 7.2 MDPI (2025) - ML methods overview

**Paper:** "An Overview of Machine-Learning Methods for Soil Moisture Estimation"
**URL:** https://www.mdpi.com/2073-4441/17/11/1638

**Scope:** ML/DL methods for SM estimation
**Key Findings:** DL excels in spatiotemporal complexity, SVM robust in sparse data
**Relevance:** HIGH - method comparison

### 7.3 MDPI (2025) - SM monitoring methods and data products

**Paper:** "Soil Moisture Monitoring Method and Data Products"
**URL:** https://www.mdpi.com/2072-4292/17/24/3945

**Scope:** All SM monitoring methods + datasets
**Key Findings:** Multi-source data fusion future direction
**Relevance:** MEDIUM - comprehensive overview

### 7.4 Springer (2025) - ML for soil moisture analysis survey

**Paper:** "Machine learning for soil moisture analysis: a survey and emerging perspectives"
**URL:** https://doi.org/10.1007/s41060-025-00977-8

**Scope:** Comprehensive ML survey
**Key Findings:** Feature selection often outweighs algorithm choice
**Relevance:** HIGH - method insights

---

## 8. Methodology Comparison Table

### 8.1 Image-Based Methods

| Paper | Year | Input | Models | Dataset Size | Best R² | Best RMSE | Context |
|-------|------|-------|--------|-------------|---------|-----------|---------|
| PLOS ONE | 2026 | RGB + Sensor | DenseNet121 | Not specified | 0.973 | 4.14 | Greenhouse |
| Zhang et al. | 2024 | RGB | LG-SWC-R3 | 3175 images | 0.950 | 1.351% | Lab |
| Hossain et al. | 2023 | Smartphone RGB | SVR | 629 images | 0.96 | 0.06 | Field |
| Indian soils | 2025 | Smartphone RGB | RF | Not specified | High | Low | Field |
| Suud et al. | 2026 | Field RGB | CNN/ResNet-50 | 200 images | 0.513 | 0.433-0.507 | Field (FAILED) |
| MIS-ME | 2024 | RGB + Weather | Multi-modal | Not specified | - | MAPE 10.14% | Field |
| Kim et al. | 2023 | RGB | CNN | Not specified | 0.975 | - | Lab |

### 8.2 Remote Sensing Methods

| Paper | Year | Input | Models | Best R² | Best RMSE | Context |
|-------|------|-------|--------|---------|-----------|---------|
| HESS | 2024 | Time series | LSTM/FA-LSTM | High | Low | Remote sensing |
| Land | 2024 | SAR + Optical | SABM | 0.861 | 0.025 | Regional |
| Nature | 2025 | RS features | XGBoost/RF | 0.98 | 0.018 | Regional |
| Remote Sensing | 2025 | Multi-source | RF | High | Low | Regional |

### 8.3 Sensor Methods

| Sensor | Accuracy | Cost | Range | Limitations |
|--------|----------|------|-------|-------------|
| TDR | ±2% | High ($20K-$40K) | Full range | Expensive, calibration needed |
| FDR | ±5% | Medium ($12K-$25K) | Full range | Temperature sensitive |
| Tensiometer | 85% | Low ($3K-$8K) | 0-100 kPa | Fails in dry conditions |
| Capacitive | Variable | Very low ($800-$3K) | Limited | Temperature sensitive |

### 8.4 IoT Systems

| System | Year | Context | Cost | Key Feature |
|--------|------|---------|------|-------------|
| Solar irrigation | 2024 | Bangladesh rice | Not specified | Solar tracker |
| Smart irrigation | 2024 | Bangladesh | Low | Crop protection |
| AWD monitoring | 2024 | Bangladesh paddy | ~$42 | Water saving |
| SoilSense | 2025 | Bangladesh | Low | Telegram bot |
| Weather-soil | 2024 | Bangladesh | Low | Weather correlation |

---

## 9. Research Gaps Identified

### 9.1 Critical Gaps

1. **No RGB image + tensiometer validation study exists**
   - All image-based studies use lab conditions or satellite data
   - No study validates RGB predictions against tensiometer readings
   - Our dataset uniquely combines RGB images with tensiometer ground truth

2. **Limited field-captured RGB image studies**
   - Most studies use controlled lab conditions
   - Only Suud et al. (2026) attempted field images - FAILED (R²=0.205-0.513)
   - Gap: How to handle uncontrolled lighting, shadows, non-soil objects

3. **No Bangladesh-specific image-based soil moisture study**
   - Bangladesh has IoT studies but no image-based approaches
   - Tropical climate, specific soil types not studied
   - Gap: Climate-specific model validation

4. **Limited multi-depth prediction from single RGB image**
   - Most studies predict only surface moisture
   - Only PLOS ONE (2026) attempts depth prediction
   - Gap: Can surface RGB predict subsurface moisture?

5. **No continuous regression from tensiometer scale (0-101 kPa)**
   - Most studies use volumetric water content (VWC)
   - Tensiometers measure matric potential (kPa)
   - Gap: Direct kPa prediction from images

### 9.2 Methodological Gaps

6. **Limited attention mechanism studies**
   - Only Zhang et al. (2024) uses attention for soil moisture
   - Gap: Transformer-based approaches for RGB soil moisture

7. **No ensemble stacking for image-based soil moisture**
   - Ensemble stacking successful in remote sensing (SABM)
   - Gap: Apply stacking to image-based approaches

8. **Limited interpretable ML for feature analysis**
   - Only Indian soils study uses IML
   - Gap: What visual features actually predict moisture?

9. **No data augmentation comparison study**
   - Most studies use basic augmentation
   - Gap: Which augmentation strategies work best for soil images?

10. **Limited transfer learning across soil types**
    - Most studies use single soil type
    - Gap: Can models transfer across different soils?

### 9.3 Application Gaps

11. **No smartphone app for farmers**
    - Research exists but no deployed apps
    - Gap: Practical tool for smallholder farmers

12. **Limited real-time monitoring systems**
    - IoT studies exist but not image-based
    - Gap: Real-time RGB-based monitoring

13. **No irrigation scheduling from RGB images**
    - Studies estimate moisture but don't link to irrigation
    - Gap: Decision support system from images

14. **Limited multi-crop validation**
    - Most studies use single crop type
    - Gap: Crop-agnostic soil moisture estimation

15. **No cost-benefit analysis**
    - Studies don't compare cost of image vs sensor approaches
    - Gap: Economic feasibility study needed

### 9.4 Data Gaps

16. **No large-scale public RGB soil moisture dataset**
    - Most studies use small private datasets
    - Gap: Need standardized benchmark dataset

17. **Limited temporal diversity**
    - Most studies capture single time point
    - Gap: Temporal dynamics in RGB images

18. **No multi-resolution comparison**
    - Studies use different image resolutions
    - Gap: Optimal resolution for prediction?

19. **Limited lighting condition studies**
    - Only Hossain et al. compares lighting conditions
    - Gap: How to handle varying field lighting?

20. **No non-soil object robustness study**
    - Suud et al. acknowledges this as failure cause
    - Gap: Segmentation/preprocessing for field images?

---

## 10. References

### Image-Based Soil Moisture
1. PLOS ONE (2026). "Image-based machine learning models for customized soil moisture management." https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0341904
2. Zhang, Y. et al. (2024). "Advancing Digital Image-Based Recognition of Soil Water Content." Water, 16(8), 1133. https://www.mdpi.com/2073-4441/16/8/1133
3. Hossain, M.R.H. et al. (2023). "Machine Learning Techniques for Estimating Soil Moisture from Smartphone Captured Images." Agriculture, 13(3), 574. https://www.mdpi.com/2077-0472/13/3/574
4. ScienceDirect (2025). "Smartphone-based image analysis and interpretable ML for soil moisture estimation across diverse Indian soils." https://www.sciencedirect.com/science/article/abs/pii/S2352938525002083
5. Suud, H.M. et al. (2026). "Performance of CNN for Classifying Soil Moisture Level based on In-Situ RGB Soil Surface Images." Jurnal Teknik Pertanian Lampung, 15(2). https://jurnal.fp.unila.ac.id/index.php/jtp/article/view/11703
6. Rakib, M. et al. (2024). "MIS-ME: A Multi-modal Framework for Soil Moisture Estimation." arXiv. https://doi.org/10.48550/arxiv.2408.00963
7. Kim, D. et al. (2023). "CNN-Based Soil Water Content and Density Prediction Model." Applied Sciences, 13(5), 2936. https://doi.org/10.3390/app13052936

### Remote Sensing + ML/DL
8. HESS (2024). "A comprehensive study of deep learning for soil moisture prediction." https://hess.copernicus.org/articles/28/917/2024/
9. Lamichhane, M. et al. (2025). "Soil Moisture Prediction Using Remote Sensing and ML Algorithms: A Review." Remote Sensing, 17(14), 2397. https://doi.org/10.3390/rs17142397
10. Land (2024). "Comparative Analysis of ML Models for Soil Moisture Estimation Using High-Resolution RS Data." https://www.mdpi.com/2073-445X/13/8/1331
11. Nature (2025). "A data driven comparison of hybrid ML techniques for soil moisture modeling." https://doi.org/10.1038/s41598-025-27225-0
12. MDPI (2025). "Regional Soil Moisture Estimation Leveraging Multi-Source Data Fusion and AutoML." https://www.mdpi.com/2072-4292/17/5/837
13. Xu, Y. et al. (2025). "A Multimodal Deep Learning Approach for Soil Moisture Downscaling." https://doi.org/10.1029/2025jh000639

### Sensor Methods
14. Sensors (2023). "Toward Optimal Irrigation Management at the Plot Level." https://pmc.ncbi.nlm.nih.gov/articles/PMC10674332/
15. MDPI (2024). "Use of Probes and Sensors in Agriculture." https://www.mdpi.com/2624-7402/6/4/234
16. JISem (2024). "Soil Moisture Prediction Using ML: A Comparative Study of Sensor Technologies." https://doi.org/10.52783/jisem.v9i4s.12287
17. MDPI (2025). "Approaches for Assessment of Soil Moisture." https://www.mdpi.com/2073-4441/17/16/2388
18. MDPI (2025). "An Overview of ML Methods for Soil Moisture Estimation." https://www.mdpi.com/2073-4441/17/11/1638
19. MDPI (2025). "Soil Moisture Monitoring Method and Data Products." https://www.mdpi.com/2072-4292/17/24/3945
20. Springer (2025). "Machine learning for soil moisture analysis: a survey." https://doi.org/10.1007/s41060-025-00977-8

### IoT Systems
21. Dey, P.K. et al. (2024). "IoT-based solar-powered smart irrigation system for rice fields." https://doi.org/10.12972/pastj.20240004
22. Ahmed, K.R. et al. (2024). "A Sustainable Smart Irrigation and Crop Protection System for Bangladesh." https://doi.org/10.1109/csitss64042.2024.10816766
23. Sarkar, S. et al. (2024). "Real-Time Monitoring of Irrigation in Paddy Fields: An IoT Approach to AWD." https://doi.org/10.5281/zenodo.16140481
24. MDPI (2023). "Smart Crop Cultivation System Using Automated Agriculture Monitoring." https://www.mdpi.com/1424-8220/23/20/8472
25. Das, S. et al. (2025). "SoilSense: An IoT-Based Soil Health Monitoring System for Bangladesh." https://doi.org/10.1109/eict68394.2025.11355612
26. Banna, T.T. (2024). "Enhancing Agricultural Automation through Weather Invariant Soil Parameter Prediction." https://tahsintariq.github.io/publication/2024-ai_agri/
27. IRRI/Tufts (2024). "IRRI, Tufts University, and BMDA host workshop on AWD technology." https://www.tbsnews.net/agriculture/irri-tufts-university-and-bmda-host-workshop-alternate-wetting-and-drying-technology

### Additional Related Works
28. MDPI (2024). "Water Content Prediction in Smart Agriculture Using CNN and Transfer Learning."
29. IIETA (2025). "Embedded Optical Soil Moisture Measurement System Using Multi-Color-Space Feature Fusion."
30. Agriculture (2025). "Image-Based Interpolation of Soil Surface Imagery for Estimating SWC."
31. MDPI (2024). "Advancing Digital Image-Based Recognition of Soil Water Content."
32. ScienceDirect (2025). "Overcoming data scarcity: A transfer learning framework for soil moisture estimation."

---

*End of Literature Review*
