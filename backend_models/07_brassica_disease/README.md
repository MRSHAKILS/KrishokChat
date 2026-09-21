# Brassica / Crucifer Pathology Classifier (`brassica_disease`)

## 1. Overview
The **Brassica Pathology Classifier** provides dual-crop diagnostic coverage for Cabbage (*Brassica oleracea var. capitata*) and Cauliflower (*Brassica oleracea var. botrytis*), diagnosing major fungal and bacterial diseases.

## 2. Model Specifications
- **Architecture**: YOLO26 Classification (`YOLO26-cls`)
- **Weights File (PyTorch)**: `brassica_disease.pt` (~10.5 MB)
- **Edge Deployment (ONNX)**: `brassica_disease.onnx` (~20.8 MB)
- **Input Resolution**: 224 × 224 RGB
- **Number of Classes**: 11
- **Agronomic Metadata**: `disease_details.json`

## 3. Class Index Mapping (`class_names.json`)
| Index | Class Label | Crop | Condition |
|:---:|:---|:---|:---|
| 0 | `Cabbage__Alternaria_Spot` | Cabbage | Alternaria Leaf Spot |
| 1 | `Cabbage__Black_Rot` | Cabbage | Black Rot (*Xanthomonas campestris*) |
| 2 | `Cabbage__Downy_Mildew` | Cabbage | Downy Mildew (*Peronospora parasitica*) |
| 3 | `Cabbage__Healthy_Leaf` | Cabbage | Healthy Leaf |
| 4 | `Cabbage__Soft_Rot` | Cabbage | Bacterial Soft Rot (*Pectobacterium*) |
| 5 | `Cauliflower__Alternaria_Spot` | Cauliflower | Alternaria Leaf Spot |
| 6 | `Cauliflower__Black_Rot` | Cauliflower | Black Rot (*Xanthomonas campestris*) |
| 7 | `Cauliflower__Downy_Mildew` | Cauliflower | Downy Mildew |
| 8 | `Cauliflower__Healthy_Leaf` | Cauliflower | Healthy Leaf |
| 9 | `Cauliflower__Soft_Rot` | Cauliflower | Bacterial Soft Rot |
| 10 | `Others` | Brassica | Other / Out-of-Distribution |

## 4. Quickstart Inference

```python
from ultralytics import YOLO

model = YOLO("brassica_disease.pt")
results = model.predict("brassica_sample.jpg", imgsz=224, verbose=False)[0]

top_idx = results.probs.top1
top_conf = float(results.probs.top1conf)
label = model.names[top_idx]

print(f"Prediction: {label} ({top_conf:.2%})")
```
