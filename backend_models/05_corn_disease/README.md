# Corn / Maize Pathology Classifier (`corn_disease`)

## 1. Overview
The **Corn Pathology Classifier** provides automated diagnostic classification for Maize / Corn (*Zea mays*), identifying critical foliar fungal diseases.

## 2. Model Specifications
- **Architecture**: YOLO26 Classification (`YOLO26-cls`)
- **Weights File (PyTorch)**: `corn_disease.pt` (~10.5 MB)
- **Edge Deployment (ONNX)**: `corn_disease.onnx` (~20.8 MB)
- **Input Resolution**: 224 × 224 RGB
- **Number of Classes**: 4
- **Agronomic Metadata**: `disease_details.json`

## 3. Class Index Mapping (`class_names.json`)
| Index | Class Label | Disease Name (English) | Pathogen |
|:---:|:---|:---|:---|
| 0 | `Common_Rust` | Common Rust | *Puccinia sorghi* |
| 1 | `Gray_Leaf_Spot` | Gray Leaf Spot | *Cercospora zeae-maydis* |
| 2 | `Healthy` | Healthy Leaf | N/A |
| 3 | `Northern_Leaf_Blight` | Northern Corn Leaf Blight | *Exserohilum turcicum* |

## 4. Quickstart Inference

```python
from ultralytics import YOLO

model = YOLO("corn_disease.pt")
results = model.predict("corn_sample.jpg", imgsz=224, verbose=False)[0]

top_idx = results.probs.top1
top_conf = float(results.probs.top1conf)
label = model.names[top_idx]

print(f"Prediction: {label} ({top_conf:.2%})")
```
