# Crop Intake Classifier (`crop_classifier`)

## 1. Overview
The **Crop Intake Classifier** acts as Tier-1 in the multi-crop diagnostic pipeline. When a farmer submits a leaf image, this model identifies the crop species among 10 common agricultural crops in Bangladesh. Once the crop is identified, the pipeline dynamically routes the image to the corresponding specialized pathology classifier.

## 2. Model Specifications
- **Architecture**: YOLO26 Classification (`YOLO26-cls`)
- **Weights File (PyTorch)**: `crop_classifier.pt` (~10.5 MB)
- **Edge Deployment (ONNX)**: `crop_classifier.onnx` (~20.8 MB)
- **Input Resolution**: 224 × 224 RGB
- **Number of Classes**: 10
- **Normalization**: Standard RGB normalization [0, 1]

## 3. Class Index Mapping (`class_names.json`)
| Index | Crop Name (English) | Bangla Name | Routing Target |
|:---:|:---|:---|:---|
| 0 | Cabbage | বাঁধাকপি | `07_brassica_disease` |
| 1 | Cauliflower | ফুলকপি | `07_brassica_disease` |
| 2 | Chili | মরিচ | `06_chilli_disease` |
| 3 | Eggplant | বেগুন | General Advisory |
| 4 | Gourd | লাউ / মিষ্টি কুমড়া | General Advisory |
| 5 | Guava | পেয়ারা | General Advisory |
| 6 | Others | অন্যান্য / অচেনা ফসল | Out-of-Distribution Rejection |
| 7 | Potato | আলু | `02_potato_disease` |
| 8 | Rice | ধান | `03_rice_disease` |
| 9 | Tomato | টমেটো | Solanaceae Advisory |

## 4. Quickstart Inference

### Python (PyTorch via Ultralytics)
```python
from ultralytics import YOLO
from PIL import Image

# 1. Load model
model = YOLO("crop_classifier.pt")

# 2. Run inference
results = model.predict("sample.jpg", imgsz=224, verbose=False)[0]

# 3. Extract top prediction
top_idx = results.probs.top1
top_conf = float(results.probs.top1conf)
crop_name = model.names[top_idx]

print(f"Predicted Crop: {crop_name} (Confidence: {top_conf:.2%})")
```

### Python (ONNX Runtime)
```python
import onnxruntime as ort
import numpy as np
from PIL import Image

session = ort.InferenceSession("crop_classifier.onnx")
img = Image.open("sample.jpg").convert("RGB").resize((224, 224))
x = np.array(img, dtype=np.float32).transpose(2, 0, 1)[None, ...] / 255.0

outputs = session.run(None, {session.get_inputs()[0].name: x})[0]
predicted_idx = int(np.argmax(outputs[0]))
print(f"Predicted Class Index: {predicted_idx}")
```
