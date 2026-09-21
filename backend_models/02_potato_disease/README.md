# Potato Pathology Classifier (`potato_disease`)

## 1. Overview
The **Potato Pathology Classifier** provides localized disease detection for potato crops (*Solanum tuberosum*), specializing in distinguishing between destructive Early Blight (*Alternaria solani*), Late Blight (*Phytophthora infestans*), and healthy foliage.

## 2. Model Specifications
- **Architecture**: YOLO26 Classification (`YOLO26-cls`)
- **Weights File (PyTorch)**: `potato_disease.pt` (~10.5 MB)
- **Edge Deployment (ONNX)**: `potato_disease.onnx` (~20.8 MB)
- **Input Resolution**: 224 × 224 RGB
- **Number of Classes**: 3
- **Agronomic Metadata**: `disease_details.json` (bilingual Bangla/English symptoms, chemical fungicides, and organic controls)

## 3. Class Index Mapping (`class_names.json`)
| Index | Class Label | Disease Name (English) | Disease Name (Bangla) |
|:---:|:---|:---|:---|
| 0 | `Potato__Early_Blight` | Early Blight (*Alternaria solani*) | আগাম ধসা রোগ |
| 1 | `Potato__Healthy_Leaf` | Healthy Leaf | সুস্থ পাতা |
| 2 | `Potato__Late_Blight` | Late Blight (*Phytophthora infestans*) | নাবি ধসা রোগ |

## 4. Quickstart Inference

### Python (PyTorch via Ultralytics)
```python
from ultralytics import YOLO
import json

# Load YOLO26 model and disease details
model = YOLO("potato_disease.pt")
details = json.load(open("disease_details.json", encoding="utf-8"))

results = model.predict("potato_sample.jpg", imgsz=224, verbose=False)[0]
top_idx = results.probs.top1
top_conf = float(results.probs.top1conf)
label = model.names[top_idx]

print(f"Prediction: {label} ({top_conf:.2%})")
```

### Python (ONNX Runtime)
```python
import onnxruntime as ort
import numpy as np
from PIL import Image

session = ort.InferenceSession("potato_disease.onnx")
img = Image.open("potato_sample.jpg").convert("RGB").resize((224, 224))
x = np.array(img, dtype=np.float32).transpose(2, 0, 1)[None, ...] / 255.0

outputs = session.run(None, {session.get_inputs()[0].name: x})[0]
pred_idx = int(np.argmax(outputs[0]))
print(f"Predicted Class Index: {pred_idx}")
```
