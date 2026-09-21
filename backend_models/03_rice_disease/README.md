# Rice Pathology Classifier (`rice_disease`)

## 1. Overview
The **Rice Pathology Classifier** is dedicated to major rice (*Oryza sativa*) diseases affecting staple grain production in South Asia, including Bacterial Leaf Blight, Rice Blast, and Sheath Blight.

## 2. Model Specifications
- **Architecture**: YOLO26 Classification (`YOLO26-cls`)
- **Weights File (PyTorch)**: `rice_disease.pt` (~19.9 MB)
- **Edge Deployment (ONNX)**: `rice_disease.onnx` (~39.6 MB)
- **Input Resolution**: 224 × 224 RGB
- **Number of Classes**: 10
- **Agronomic Metadata**: `disease_details.json` (symptoms, thresholds, and treatments)

## 3. Class Index Mapping (`class_names.json`)
| Index | Class Label | Disease Name (English) | Disease Name (Bangla) |
|:---:|:---|:---|:---|
| 0 | `Others` | Other Foliage / OOD | অন্যান্য / অনির্ধারিত |
| 1 | `Rice__Bacterial_Leaf_Blight` | Bacterial Leaf Blight (*Xanthomonas oryzae*) | ব্যাক্টেরিয়াজনিত পাতা পোড়া |
| 2 | `Rice__Brown_Spot` | Brown Spot (*Bipolaris oryzae*) | বাদামী দাগ রোগ |
| 3 | `Rice__Healthy_Leaf` | Healthy Leaf | সুস্থ পাতা |
| 4 | `Rice__Leaf_Blast` | Leaf Blast (*Magnaporthe oryzae*) | পাতা ব্লাস্ট রোগ |
| 5 | `Rice__Leaf_Scald` | Leaf Scald (*Microdochium oryzae*) | পাতা ঝলসানো রোগ |
| 6 | `Rice__Narrow_Brown_Leaf_Spot` | Narrow Brown Leaf Spot (*Cercospora janseana*) | সরু বাদামী দাগ রোগ |
| 7 | `Rice__Neck_Blast` | Neck Blast (*Magnaporthe oryzae*) | শীষ ব্লাস্ট রোগ |
| 8 | `Rice__Sheath_Blight` | Sheath Blight (*Rhizoctonia solani*) | খোল পোড়া রোগ |
| 9 | `Rice__Sheath_Rot` | Sheath Rot (*Sarocladium oryzae*) | খোল পচা রোগ |

## 4. Quickstart Inference

```python
from ultralytics import YOLO

# 1. Load YOLO26 model
model = YOLO("rice_disease.pt")

# 2. Run inference
results = model.predict("rice_sample.jpg", imgsz=224, verbose=False)[0]
top_idx = results.probs.top1
top_conf = float(results.probs.top1conf)
label = model.names[top_idx]

print(f"Prediction: {label} ({top_conf:.2%})")
```
