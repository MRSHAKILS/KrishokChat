"""Vision Orchestration Service.

Implements the agentic workflow:
  User uploads image → Crop Classifier → Disease Detector → Disease Details

Follows the 4-stage pipeline from AGENTS.md §4.
"""
from __future__ import annotations

import io
import json
from pathlib import Path

import numpy as np
from fastapi import APIRouter, File, UploadFile, HTTPException
from PIL import Image
from pydantic import BaseModel
from ultralytics import YOLO

from app.core.config import settings

router = APIRouter()

# --- Model Registry ---
VISION_DIR = Path(settings.ml_assets_dir) / "vision"

CROP_CLASSIFIER_PATH = VISION_DIR / "crop_classifier" / "model.pt"
DISEASE_MODEL_PATHS = {
    "rice": VISION_DIR / "rice_disease" / "model.pt",
    "wheat": VISION_DIR / "wheat_disease" / "model.pt",
    "corn": VISION_DIR / "corn_disease" / "model.pt",
    "potato": VISION_DIR / "potato_disease" / "model.pt",
    "brassica": VISION_DIR / "brassica_disease" / "model.pt",
}

# Crop class name → disease model key (lowercase matching).
# The crop classifier has no dedicated class for Rice (Bangladesh's #1 crop):
# rice images consistently classify as "Wheat". Wheat is therefore an
# ambiguous catch-all bucket: it can be real wheat OR rice, so BOTH the wheat
# and rice disease models run and the higher-confidence result wins.
# Solanacea/GourdGuava have no dedicated model → nearest family.
CROP_TO_MODEL = {
    "rice": "rice",
    "wheat": "wheat",
    "corn": "corn",
    "potato": "potato",
    "brassica": "brassica",
    "gourdguava": "brassica", # no dedicated model → nearest family
    "solanacea": "potato",    # no dedicated model → nearest family
}

# Ambiguous catch-all crops: run every candidate model, pick the winner by
# top-1 confidence. Wheat == possibly rice (classifier blind spot).
AMBIGUOUS_CROP_CANDIDATES = {
    "wheat": ["wheat", "rice"],
}

# Lazy-loaded models
_crop_classifier = None
_disease_models: dict[str, YOLO] = {}


def get_crop_classifier() -> YOLO:
    """Lazy-load crop classifier."""
    global _crop_classifier
    if _crop_classifier is None:
        if not CROP_CLASSIFIER_PATH.exists():
            raise HTTPException(500, "Crop classifier model not found")
        _crop_classifier = YOLO(str(CROP_CLASSIFIER_PATH))
    return _crop_classifier


def get_disease_model(crop_key: str) -> YOLO:
    """Lazy-load disease model for a specific crop."""
    if crop_key not in _disease_models:
        model_path = DISEASE_MODEL_PATHS.get(crop_key)
        if not model_path or not model_path.exists():
            raise HTTPException(500, f"Disease model not found for {crop_key}")
        _disease_models[crop_key] = YOLO(str(model_path))
    return _disease_models[crop_key]


def load_class_names(model_dir: Path) -> dict:
    """Load class names from JSON."""
    names_path = model_dir / "class_names.json"
    if names_path.exists():
        with open(names_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def load_disease_details(crop_key: str) -> dict | None:
    """Load disease details knowledge base."""
    details_path = VISION_DIR / f"{crop_key}_disease" / "disease_details.json"
    if details_path.exists():
        with open(details_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def _detail_tokens(name: str) -> set[str]:
    """Extract meaningful English tokens from a class/disease name."""
    import re

    return {t for t in re.split(r"[^a-z0-9]+", name.lower()) if len(t) > 1}


def match_disease_details(disease_class: str, details: dict) -> dict | None:
    """Match a model class name (e.g. 'Potato__Early_Blight') against the
    disease_details knowledge base using token overlap.

    Class names in the knowledge base are human-written (e.g. 'Early Blight
    (আগাম ব্লাইট...)') so substring matching is unreliable; token-overlap
    against the disease-class core (last segment after '__') is robust.
    """
    # Core = last segment: 'Potato__Early_Blight' -> 'early blight'
    core = disease_class.split("__")[-1]
    core_tokens = _detail_tokens(core)
    if not core_tokens:
        return None

    best: dict | None = None
    best_score = 0.0
    for crop_data in details.values():
        for cls in crop_data.get("classes", []):
            cls_tokens = _detail_tokens(cls.get("class_name", ""))
            if not cls_tokens:
                continue
            overlap = len(core_tokens & cls_tokens) / len(core_tokens)
            if overlap >= 0.5 and overlap > best_score:
                best = cls
                best_score = overlap

    return best



def predict_classification(model: YOLO, image: Image.Image) -> dict:
    """Run classification and return top predictions."""
    results = model(image, verbose=False)[0]
    names = model.names

    if hasattr(results, "probs") and results.probs is not None:
        probs = results.probs.data.cpu().numpy()
        top_indices = np.argsort(probs)[::-1]
        return {
            "top_prediction": {
                "class": names[int(top_indices[0])],
                "confidence": round(float(probs[top_indices[0]]), 4),
            },
            "top3": [
                {
                    "class": names[int(idx)],
                    "confidence": round(float(probs[idx]), 4),
                }
                for idx in top_indices[:3]
            ],
            "all_probabilities": {
                names[i]: round(float(probs[i]), 4) for i in range(len(probs))
            },
        }

    return {"error": "Model did not return probabilities"}


# --- Response Schemas ---
class CropClassificationResponse(BaseModel):
    crop: str
    confidence: float
    top3: list[dict]
    has_disease_model: bool


class DiseaseDetectionResponse(BaseModel):
    crop: str
    crop_confidence: float
    disease: str
    disease_confidence: float
    disease_info: dict | None
    top3_diseases: list[dict]


# --- Endpoints ---
@router.post("/api/classify", response_model=CropClassificationResponse)
async def classify_crop(file: UploadFile = File(...)):
    """
    Stage 1: Classify the crop from an uploaded image.
    Returns the predicted crop and whether a disease model exists.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image")

    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    model = get_crop_classifier()
    pred = predict_classification(model, image)

    crop_class = pred["top_prediction"]["class"]
    crop_conf = pred["top_prediction"]["confidence"]
    crop_key = crop_class.lower()
    has_model = CROP_TO_MODEL.get(crop_key) is not None

    return CropClassificationResponse(
        crop=crop_class,
        confidence=crop_conf,
        top3=pred["top3"],
        has_disease_model=has_model,
    )


@router.post("/api/detect", response_model=DiseaseDetectionResponse)
async def detect_disease(file: UploadFile = File(...)):
    """
    Full pipeline: Crop classification → Disease detection → Disease details.
    Returns crop, disease, and treatment information.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image")

    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    # Stage 1: Classify crop
    crop_model = get_crop_classifier()
    crop_pred = predict_classification(crop_model, image)
    crop_class = crop_pred["top_prediction"]["class"]
    crop_conf = crop_pred["top_prediction"]["confidence"]
    crop_key = crop_class.lower()

    # Stage 2: Route to disease model (ambiguous crops run all candidates,
    # the highest-confidence result wins)
    candidate_keys = AMBIGUOUS_CROP_CANDIDATES.get(crop_key, [])
    if not candidate_keys:
        disease_model_key = CROP_TO_MODEL.get(crop_key)
        if not disease_model_key:
            return DiseaseDetectionResponse(
                crop=crop_class,
                crop_confidence=crop_conf,
                disease="No disease model available for this crop",
                disease_confidence=0.0,
                disease_info=None,
                top3_diseases=[],
            )
        candidate_keys = [disease_model_key]

    best: dict | None = None
    for candidate in candidate_keys:
        # Skip placeholder models
        warning_path = VISION_DIR / f"{candidate}_disease" / "PLACEHOLDER_WARNING.json"
        if warning_path.exists():
            continue

        try:
            disease_model = get_disease_model(candidate)
            disease_pred = predict_classification(disease_model, image)
            disease_class = disease_pred["top_prediction"]["class"]
            disease_conf = disease_pred["top_prediction"]["confidence"]

            # Stage 4: Lookup disease details (token-overlap match)
            details = load_disease_details(candidate)
            disease_info = match_disease_details(disease_class, details) if details else None

            candidate_result = {
                "disease_model_key": candidate,
                "disease": disease_class,
                "disease_confidence": disease_conf,
                "disease_info": disease_info,
                "top3_diseases": disease_pred["top3"],
            }
            if best is None or disease_conf > best["disease_confidence"]:
                best = candidate_result
        except HTTPException:
            continue

    if best is None:
        return DiseaseDetectionResponse(
            crop=crop_class,
            crop_confidence=crop_conf,
            disease="No disease model available for this crop",
            disease_confidence=0.0,
            disease_info=None,
            top3_diseases=[],
        )

    return DiseaseDetectionResponse(
        crop=crop_class,
        crop_confidence=crop_conf,
        disease=best["disease"],
        disease_confidence=best["disease_confidence"],
        disease_info=best["disease_info"],
        top3_diseases=best["top3_diseases"],
    )
