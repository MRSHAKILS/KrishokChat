# Wheat Pathology Classifier (`wheat_disease`)

## 1. Overview
The **Wheat Pathology Classifier** diagnoses foliar and spike infections in wheat (*Triticum aestivum*), covering critical pathogens such as Wheat Blast (*Magnaporthe oryzae Triticum* pathotype) and Rusts (*Puccinia spp.*).

## 2. Model Specifications
- **Architecture**: YOLO26 Classification (`YOLO26-cls`)
- **Weights File (PyTorch)**: `wheat_disease.pt` (~9.0 MB)
- **Edge Deployment (ONNX)**: `wheat_disease.onnx` (~5.9 MB)
- **Input Resolution**: 224 × 224 RGB
- **Number of Classes**: 11
- **Metadata**: `disease_details.json`, `metadata.json`

## 3. Class Index Mapping (`class_names.json`)
| Index | Class Label | Disease Name (English) | Pathogen |
|:---:|:---|:---|:---|
| 0 | `BlackPoint` | Black Point | *Bipolaris sorokiniana* / *Alternaria* |
| 1 | `Blast` | Wheat Blast | *Magnaporthe oryzae* pv. *triticum* |
| 2 | `FusariumFootRot` | Fusarium Foot Rot | *Fusarium spp.* |
| 3 | `Healthy` | Healthy Leaf | N/A |
| 4 | `LeafBlight` | Leaf Blight | *Bipolaris sorokiniana* |
| 5 | `LeafRust` | Leaf Rust / Brown Rust | *Puccinia triticina* |
| 6 | `LooseSmut` | Loose Smut | *Ustilago tritici* |
| 7 | `PowderyMildew` | Powdery Mildew | *Blumeria graminis* |
| 8 | `SpotBlotch` | Spot Blotch | *Bipolaris sorokiniana* |
| 9 | `StripeRust` | Stripe Rust / Yellow Rust | *Puccinia striiformis* |
| 10 | `TanSpot` | Tan Spot | *Pyrenophora tritici-repentis* |

## 4. Quickstart Inference

```python
from ultralytics import YOLO

model = YOLO("wheat_disease.pt")
results = model.predict("wheat_sample.jpg", imgsz=224, verbose=False)[0]

top_idx = results.probs.top1
top_conf = float(results.probs.top1conf)
label = model.names[top_idx]

print(f"Prediction: {label} ({top_conf:.2%})")
```
