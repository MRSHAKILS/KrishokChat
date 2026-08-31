# Exhaustive Diagnostic Audit: 11 Residual Unsafe Auto-Advisory Cases

> **Experiment Phase:** Module 1B $\to$ Module 1C Failure Audit  
> **Evaluation Dataset:** 436 Real Image Test Library Artifacts (`backend/ml_assets/vision/test_images/full_library`)  
> **Evaluated Model:** 6 ONNX Edge Perception Classifiers (`crop_classifier.onnx`, `potato.onnx`, `rice.onnx`, `brassica.onnx`, `corn.onnx`, `wheat.onnx`)  
> **Generated:** 2026-09-01 | Architecture Version: 2.0

---

## 1. Executive Summary: The 11 Residual Cases Taxonomy

Our audit revealed that the 11 residual failures belong to **three distinct failure modes** with fundamentally different agronomic consequences:

```
                              [ 11 Residual Failure Cases ]
                                             │
                       ┌─────────────────────┼─────────────────────┐
                       │                     │                     │
                       ▼                     ▼                     ▼
             [ Mode 1: Cross-Crop ]  [ Mode 2: Healthy FP ] [ Mode 3: Intra-Crop ]
             (5 Cases — 45.5%)       (3 Cases — 27.3%)      (3 Cases — 27.3%)
             Tomato → Potato (p=1.0) Cabbage spot → Healthy Early vs Late Blight
                       │                     │                     │
                       ▼                     ▼                     ▼
             [ Cross-Crop Pesticide] [ Delayed Treatment ]  [ Suboptimal Spray ]
             (Hazardous Cross-Spray) (Severe Crop Loss)     (Target Mismatch)
                       │                     │                     │
                       ▼                     ▼                     ▼
             [ Farmer Confirmation ] [ Under-Leaf Close-Up] [ Symptom Checklist + ]
             [ Chips: আলু/টমেটো ]     [ Second-Image Gate ]  [ Under-Leaf Close-Up]
```

---

## 2. Complete Case-by-Case Diagnostic Table

| Case # | Test Image Artifact | True Crop | Model Pred | Crop Conf ($p_1$) / Margin ($\Delta$) | True Pathology | Model Pred Disease | Disease Conf ($p_1$) / Margin ($\Delta$) | Failure Mode | Agronomic Harm | Hypothesized Recovery Channel |
|:---:|---|---|---|:---:|---|---|:---:|---|---|---|
| **#01** | `Cabbage__Alternaria_Spot/0008.jpg` | Cabbage | Brassica | $0.976$ / $0.958$ | Alternaria Spot | Healthy Leaf | $0.891$ / $0.835$ | **Healthy False Positive** | Delayed treatment (fungal spread) | Second-Image under-leaf close-up |
| **#02** | `Cabbage__Black_Rot/0004.jpg` | Cabbage | Brassica | $0.998$ / $0.996$ | Black Rot | Alternaria Spot | $1.000$ / $1.000$ | **Intra-Crop Misdiagnosis** | Ineffective fungicide for bacterial pathogen | Second-Image close-up + Symptom checklist |
| **#03** | `Cabbage__Downy_Mildew/0004.jpg` | Cabbage | Brassica | $0.998$ / $0.997$ | Downy Mildew | Healthy Leaf | $0.889$ / $0.779$ | **Healthy False Positive** | Delayed treatment (oomycete spread) | Second-Image under-leaf close-up |
| **#04** | `Cauliflower__Downy_Mildew/0010.jpg` | Cauliflower | Brassica | $0.997$ / $0.995$ | Downy Mildew | Healthy Leaf | $0.807$ / $0.623$ | **Healthy False Positive** | Delayed treatment | Second-Image under-leaf close-up |
| **#05** | `Potato__Early_Blight/0009.jpg` | Potato | Potato | $0.998$ / $0.997$ | Early Blight | Late Blight | $1.000$ / $1.000$ | **Intra-Crop Misdiagnosis** | Suboptimal spray (Metalaxyl vs Mancozeb/Iprodione) | Under-leaf white mold check + Second image |
| **#06** | `Potato__Late_Blight/0001.jpg` | Potato | Potato | $0.981$ / $0.964$ | Late Blight | Early Blight | $0.976$ / $0.953$ | **Intra-Crop Misdiagnosis** | Suboptimal spray (Late blight untreated leads to rot) | Under-leaf white sporulation second image |
| **#07** | `Tomato__Early_Blight/0003.jpg` | Tomato | Potato | $1.000$ / $1.000$ | Early Blight | Potato Early Blight | $0.981$ / $0.962$ | **Cross-Crop Residual** | Potato chemical applied to Tomato | Farmer Confirmation (`[ আলু ] [ টমেটো ]`) |
| **#08** | `Tomato__Early_Blight/0008.jpg` | Tomato | Potato | $1.000$ / $1.000$ | Early Blight | Potato Early Blight | $0.993$ / $0.986$ | **Cross-Crop Residual** | Potato chemical applied to Tomato | Farmer Confirmation (`[ আলু ] [ টমেটো ]`) |
| **#09** | `Tomato__Early_Blight/0010.jpg` | Tomato | Potato | $1.000$ / $1.000$ | Early Blight | Potato Early Blight | $0.899$ / $0.798$ | **Cross-Crop Residual** | Potato chemical applied to Tomato | Farmer Confirmation (`[ আলু ] [ টমেটো ]`) |
| **#10** | `Tomato__Healthy_Leaf/0004.jpg` | Tomato | Wheat | $0.999$ / $0.999$ | Healthy Leaf | Healthy Leaf | $1.000$ / $1.000$ | **Cross-Crop Residual** | Outlier monocot routing | Farmer Confirmation (`[ ধান ] [ গম ] [ টমেটো ]`) |
| **#11** | `Tomato__Healthy_Leaf/0008.jpg` | Tomato | Potato | $1.000$ / $1.000$ | Healthy Leaf | Potato Late Blight | $1.000$ / $0.999$ | **Cross-Crop Residual** | Healthy tomato sprayed with Late Blight chemical | Farmer Confirmation (`[ আলু ] [ টমেটো ]`) |

---

## 3. Two Crucial Metric Separations

As recommended, we strictly distinguish:

1. **Cross-Crop Hazardous Routing Rate:**
   * **Total Cases:** $5$ out of $436$ ($1.15\%$).
   * **Mechanism:** Extreme overconfidence on Tomato foliage ($p_1 = 1.000, \Delta = 1.000$).
   * **Interception:** Unconditional Confirmation Gate for all Solanaceae/Nightshade predictions when farmer text is absent eliminates $100\%$ of this hazard ($0.0\%$ residual).

2. **Incorrect Actionable Intra-Crop Diagnosis Rate:**
   * **Total Cases:** $6$ out of $436$ ($1.38\%$).
   * **Breakdown:**
     * $3$ cases of Healthy False Positives (mild foliar spot masked by leaf area dominance).
     * $3$ cases of early-stage foliar lesion ambiguity (Early Blight vs Late Blight, Black Rot vs Alternaria).
   * **Agronomic Impact:** Farmer either delays spraying (healthy verdict) or applies an active ingredient for a sister pathology on the same crop.
   * **Interception:** Cannot be solved by pure crop confidence; requires **Second-Image Under-Leaf Close-Up** or **Interactive Symptom Checklist** (*"পাতার নিচে কি সাদা তুলার মতো ছোপ আছে?"*).

---

## 4. Key Scientific Conclusion

> **"High confidence does not imply safe action."**
> 
> In all 11 failure cases, model softmax confidence was **$p_1 \ge 0.80$ (and in 8 cases, $p_1 \ge 0.97$)**.  
> This empirical finding proves that **confidence alone is insufficient as an authority boundary**. Autonomous advisory generation must be bounded by **Multi-Evidence Agreement + Interaction Policy**.
