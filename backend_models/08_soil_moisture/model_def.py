"""KrishokChat Soil Moisture (kPa) Regression Model Architecture.

Architecture:
    EfficientNet-B0 backbone (ImageNet pre-trained) with custom multi-layer
    perceptron (MLP) regression head. Trained via 5-Fold Cross Validation.

Target:
    Soil water tension / pressure (kPa) measured via electronic tensiometer.
"""

from __future__ import annotations
from pathlib import Path
import torch
import torch.nn as nn

try:
    import timm
except ImportError:
    timm = None


class EffNetRegressor(nn.Module):
    """EfficientNet-B0 Regressor for Tensiometer Soil Moisture (kPa)."""

    def __init__(self, dropout: float = 0.3) -> None:
        super().__init__()
        if timm is None:
            raise ImportError(
                "The 'timm' package is required to instantiate EffNetRegressor. "
                "Install it via: pip install timm"
            )
        # num_classes=0 strips the classifier head and returns the 1280-dim pooled features
        self.backbone = timm.create_model("efficientnet_b0", pretrained=False, num_classes=0)
        n_features = self.backbone.num_features  # 1280

        self.head = nn.Sequential(
            nn.Linear(n_features, 128),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(128, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        feats = self.backbone(x)
        out = self.head(feats)
        return out.squeeze(1)


def load_soil_model(weights_path: str | Path, device: str = "cpu") -> EffNetRegressor:
    """Convenience factory to instantiate the model and load fold weights."""
    model = EffNetRegressor(dropout=0.0)
    state_dict = torch.load(str(weights_path), map_location=device)
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()
    return model
