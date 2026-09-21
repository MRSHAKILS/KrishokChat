# Chilli / Pepper Pathology Classifier (`chilli_disease`)

## 1. Overview
The **Chilli Pathology Classifier** diagnoses viral, bacterial, fungal, and physiological conditions in chili pepper plants (*Capsicum annuum*), addressing major yield threats in Bangladesh.

## 2. Model Specifications
- **Architecture**: YOLO26 Classification (`YOLO26-cls`)
- **Weights File (PyTorch)**: `chilli_disease.pt` (~3.1 MB)
- **Edge Deployment (ONNX)**: `chilli_disease.onnx` (~5.9 MB)
- **Input Resolution**: 224 × 224 RGB
- **Number of Classes**: 8
- **Agronomic Metadata**: `disease_details.json`

## 3. Class Index Mapping (`class_names.json`)
| Index | Class Label | Condition Name (English) | Disease Category |
|:---:|:---|:---|:---|
| 0 | `Chili__Bacterial_Spot` | Bacterial Spot (*Xanthomonas campestris*) | Bacterial |
| 1 | `Chili__Cercospora_Leaf_Spot` | Cercospora Leaf Spot / Frogeye | Fungal |
| 2 | `Chili__Curl_Virus` | Chilli Leaf Curl Virus | Viral (Whitefly vector) |
| 3 | `Chili__Healthy_Leaf` | Healthy Leaf | Healthy |
| 4 | `Chili__Late_Blight` | Late Blight / Phytophthora | Oomycete |
| 5 | `Chili__Nutrition_Deficiency` | Nutrient Deficiency (N/P/K/Fe) | Physiological |
| 6 | `Chili__White_Fly` | Whitefly Infestation (*Bemisia tabaci*) | Entomological |
| 7 | `Chili__Yellow_Virus` | Chilli Yellow Mosaic Virus | Viral |

## 4. Quickstart Inference

```python
from ultralytics import YOLO

model = YOLO("chilli_disease.pt")
results = model.predict("chilli_sample.jpg", imgsz=224, verbose=False)[0]

top_idx = results.probs.top1
top_conf = float(results.probs.top1conf)
label = model.names[top_idx]

print(f"Prediction: {label} ({top_conf:.2%})")
```
