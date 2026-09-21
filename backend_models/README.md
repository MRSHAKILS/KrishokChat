---
license: apache-2.0
tags:
- agriculture
- plant-pathology
- crop-disease
- computer-vision
- yolo26
- efficientnet
- soil-moisture
- bangladesh
- multimodal
datasets:
- agricultural-vision
metrics:
- accuracy
- rmse
library_name: ultralytics
pipeline_tag: image-classification
---

# KrishokChat: Agricultural Vision & Soil Intelligence Model Suite

This repository contains the complete, production-ready suite of machine learning models developed for the **KrishokChat Advisory System**. These models are packaged into self-contained, folderized directories to enable academic reviewers, agronomists, and developers to reproduce and run our full diagnostic pipeline locally without requiring expensive cloud GPU servers.

---

## 1. Architectural Overview

The KrishokChat perception and diagnostic stack uses a multi-tier decoupled architecture:
1. **Tier 1: Crop Species Identification** — A `YOLO26-cls` model identifying 10 major crop families in Bangladesh to eliminate cross-crop pesticide misbinding hazard.
2. **Tier 2: Specialized Crop Pathology Diagnosis** — Six per-crop dedicated `YOLO26-cls` models diagnosing foliar fungal, bacterial, viral, and physiological diseases.
3. **Tier 3: Soil Moisture Matric Tension Estimation** — A 5-fold cross-validated `EfficientNet-B0` regression model predicting continuous soil suction pressure ($\text{kPa}$) directly from field images for precision irrigation guidance.

```
                   [ Farmer Field Leaf Image ]
                               │
                               ▼
                   [ 01_crop_classifier ] (YOLO26-cls)
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
     [ 02_potato_disease ]  [ 03_rice_disease ]  [ 04_wheat_disease ] ...
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ▼
               [ Diagnosis + Bangla Treatment Advice ]
```

---

## 2. Model Catalog & Checkpoint Manifest

Every PyTorch weight (`.pt`) is named distinctively with zero ambiguity. Corresponding optimized `ONNX` weights are included for cross-platform edge deployment.

| # | Directory | PyTorch Weight (`.pt`) | Edge ONNX (`.onnx`) | Architecture | Classes / Output | Target Crop / Task |
|:---:|:---|:---|:---|:---:|:---:|:---|
| **1** | `01_crop_classifier` | `crop_classifier.pt` (10.5 MB) | `crop_classifier.onnx` (20.8 MB) | YOLO26-cls | 10 classes | Multi-crop species classification |
| **2** | `02_potato_disease` | `potato_disease.pt` (10.5 MB) | `potato_disease.onnx` (20.8 MB) | YOLO26-cls | 3 classes | Potato (*Solanum tuberosum*) |
| **3** | `03_rice_disease` | `rice_disease.pt` (19.9 MB) | `rice_disease.onnx` (39.6 MB) | YOLO26-cls | 10 classes | Rice (*Oryza sativa*) |
| **4** | `04_wheat_disease` | `wheat_disease.pt` (9.0 MB) | `wheat_disease.onnx` (5.9 MB) | YOLO26-cls | 11 classes | Wheat (*Triticum aestivum*) |
| **5** | `05_corn_disease` | `corn_disease.pt` (10.5 MB) | `corn_disease.onnx` (20.8 MB) | YOLO26-cls | 4 classes | Corn / Maize (*Zea mays*) |
| **6** | `06_chilli_disease` | `chilli_disease.pt` (3.1 MB) | `chilli_disease.onnx` (5.9 MB) | YOLO26-cls | 8 classes | Chilli (*Capsicum annuum*) |
| **7** | `07_brassica_disease` | `brassica_disease.pt` (10.5 MB) | `brassica_disease.onnx` (20.8 MB) | YOLO26-cls | 11 classes | Cabbage & Cauliflower (*Brassica spp.*) |
| **8** | `08_soil_moisture` | `effnetb0_fold[0-4].pt` (81 MB) | N/A (PyTorch state_dict) | EfficientNet-B0 | 1 continuous (kPa) | Soil matric tension estimation |

---

## 3. Directory Layout

```text
backend_models/
├── README.md                           # Main Model Card & Reviewer Documentation
├── requirements.txt                    # Minimal pip dependencies
├── verify_all_models.py                # Single-click automated diagnostic verification suite
├── run_inference.py                    # Multi-model CLI inference runner
├── upload_to_huggingface.py            # Hugging Face Hub upload automation script
│
├── 01_crop_classifier/                 # Intake Crop Classifier (10 classes)
│   ├── crop_classifier.pt
│   ├── crop_classifier.onnx
│   ├── class_names.json
│   └── README.md
│
├── 02_potato_disease/                  # Potato Pathology (Early Blight, Late Blight, Healthy)
│   ├── potato_disease.pt
│   ├── potato_disease.onnx
│   ├── class_names.json
│   ├── disease_details.json
│   └── README.md
│
├── 03_rice_disease/                    # Rice Pathology (Blast, BLB, Sheath Blight, etc.)
│   ├── rice_disease.pt
│   ├── rice_disease.onnx
│   ├── class_names.json
│   ├── disease_details.json
│   └── README.md
│
├── 04_wheat_disease/                   # Wheat Pathology (Rusts, Blast, Tan Spot, etc.)
│   ├── wheat_disease.pt
│   ├── wheat_disease.onnx
│   ├── class_names.json
│   ├── disease_details.json
│   ├── metadata.json
│   └── README.md
│
├── 05_corn_disease/                    # Corn Pathology (Rust, Leaf Spot, Blight)
│   ├── corn_disease.pt
│   ├── corn_disease.onnx
│   ├── class_names.json
│   ├── disease_details.json
│   └── README.md
│
├── 06_chilli_disease/                  # Chilli Pathology (Bacterial Spot, Curl Virus, etc.)
│   ├── chilli_disease.pt
│   ├── chilli_disease.onnx
│   ├── class_names.json
│   ├── disease_details.json
│   └── README.md
│
├── 07_brassica_disease/                # Crucifers (Cabbage / Cauliflower diseases)
│   ├── brassica_disease.pt
│   ├── brassica_disease.onnx
│   ├── class_names.json
│   ├── disease_details.json
│   └── README.md
│
├── 08_soil_moisture/                   # Soil Moisture Tensiometer Regression (5-fold ensemble)
│   ├── effnetb0_fold0.pt ... fold4.pt
│   ├── oof_predictions.csv
│   ├── pred_vs_actual.png
│   ├── model_def.py
│   └── README.md
│
└── sample_images/                      # Representative leaf images for zero-setup verification
    ├── crop_sample.jpg
    ├── potato_sample.jpg
    ├── rice_sample.jpg
    ├── wheat_sample.jpg
    ├── corn_sample.jpg
    ├── chilli_sample.jpg
    └── brassica_sample.jpg
```

---

## 4. Quickstart Guide for Academic Reviewers

### Step 1: Install Dependencies
```bash
cd backend_models
pip install -r requirements.txt
```

### Step 2: Automated Verification of All Models
Run the automated test runner to verify that every single model checkpoint loads into memory, performs forward inference, and verifies against class specifications:
```bash
python verify_all_models.py
```

### Step 3: Run Standalone Inferences

**Test Potato Disease Diagnosis:**
```bash
python run_inference.py --crop potato --image sample_images/potato_sample.jpg
```

**Test Rice Disease Diagnosis:**
```bash
python run_inference.py --crop rice --image sample_images/rice_sample.jpg
```

**Test Wheat Disease Diagnosis:**
```bash
python run_inference.py --crop wheat --image sample_images/wheat_sample.jpg
```

**Test Soil Moisture Regression:**
```bash
python run_inference.py --task soil --image sample_images/crop_sample.jpg
```

---

## 5. Python API Usage

### Vision Models (YOLO26)
```python
from ultralytics import YOLO

# Load any specialized YOLO26 pathology classifier
model = YOLO("02_potato_disease/potato_disease.pt")

# Predict on an RGB image
results = model.predict("sample_images/potato_sample.jpg", imgsz=224, verbose=False)[0]

top_class = model.names[results.probs.top1]
confidence = float(results.probs.top1conf)
print(f"Result: {top_class} ({confidence:.2%})")
```

### Soil Moisture Regression (5-Fold Ensemble)
```python
import sys
sys.path.insert(0, "08_soil_moisture")
from model_def import load_soil_model
import torch
import torchvision.transforms as T
from PIL import Image

transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

img = transform(Image.open("sample_images/crop_sample.jpg").convert("RGB")).unsqueeze(0)

# Ensemble average across 5 folds
predictions = []
for fold in range(5):
    m = load_soil_model(f"08_soil_moisture/effnetb0_fold{fold}.pt")
    with torch.no_grad():
        predictions.append(m(img).item())

mean_kpa = sum(predictions) / len(predictions)
print(f"Estimated Soil Matric Potential: {mean_kpa:.2f} kPa")
```

---

## 6. Uploading to Hugging Face Hub

To publish this suite to the official Hugging Face repository:
```bash
python upload_to_huggingface.py --token <YOUR_HF_TOKEN>
```
Target repository: `https://huggingface.co/RaiyanKhaan/KrishokTech-Models`

---

## 7. Citation
If you use these model weights or the KrishokChat pipeline in your research, please cite our paper:

```bibtex
@inproceedings{krishokchat2026,
  title={KrishokChat: A Grounded Multi-Modal Agricultural Advisory and Pathology Diagnostic System for Smallholder Farming},
  author={Reza, Raiyaan and Khaan, Raiyan and Collaborators},
  booktitle={Proceedings of the European Chapter of the Association for Computational Linguistics (EACL)},
  year={2026}
}
```
