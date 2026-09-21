# Soil Moisture Tensiometer Regression (`soil_moisture`)

## 1. Overview
The **Soil Moisture Regression Model** predicts soil matric potential / tension (measured in kilopascals, **kPa**) directly from surface soil images captured under varied ambient agricultural lighting. This enables low-cost smart irrigation scheduling without requiring physical tensiometers for smallholder farmers.

## 2. Model Specifications
- **Architecture**: EfficientNet-B0 backbone (`timm`) + custom MLP regression head:
  $$\text{Input (3, 224, 224)} \to \text{EfficientNet-B0 (1280)} \to \text{Linear(1280, 128)} \to \text{ReLU} \to \text{Dropout}(0.3) \to \text{Linear}(128, 1)$$
- **Checkpoints**: 5-Fold Cross-Validation checkpoints (`effnetb0_fold0.pt` through `effnetb0_fold4.pt`, ~16.2 MB each)
- **Evaluation Assets**:
  - `oof_predictions.csv`: Full out-of-fold predictions vs actual tensiometer readings
  - `pred_vs_actual.png`: Parity plot illustrating regression fit across all 5 folds
  - `model_def.py`: Python module containing the `EffNetRegressor` PyTorch class and `load_soil_model()` loader

## 3. Agronomic Interpretation of Soil Tension (kPa)
| Predicted kPa Range | Soil Moisture Status | Irrigation Advisory |
|:---:|:---|:---|
| **0 – 10 kPa** | Saturated / Field Capacity | No irrigation needed. Risk of waterlogging. |
| **10 – 30 kPa** | Optimal Soil Moisture | Adequate for most crop vegetative growth. |
| **30 – 50 kPa** | Moderate Drying | Plan irrigation within 24–48 hours for vegetables. |
| **50 – 80 kPa** | Severe Soil Moisture Deficit | Immediate irrigation required to prevent wilting. |
| **> 80 kPa** | Critical Drought Stress | Crop damage imminent. |

## 4. Quickstart Inference (Single Model or 5-Fold Ensemble)

```python
import torch
import torchvision.transforms as T
from PIL import Image
from model_def import load_soil_model

# 1. Prepare image transform (224x224, ImageNet normalization)
transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

image = Image.open("soil_sample.jpg").convert("RGB")
x = transform(image).unsqueeze(0)

# 2. Run 5-fold ensemble prediction
predictions = []
for fold in range(5):
    model = load_soil_model(f"effnetb0_fold{fold}.pt", device="cpu")
    with torch.no_grad():
        kpa = model(x).item()
        predictions.append(kpa)

ensemble_kpa = sum(predictions) / len(predictions)
print(f"Predicted Soil Moisture Tension: {ensemble_kpa:.2f} kPa")
```
