#!/usr/bin/env python3
"""KrishokChat ML Suite — Standalone Inference Runner for Academic Reviewers.

Usage:
    # 1. Automatic Crop Identification
    python run_inference.py --crop crop --image sample_images/crop_sample.jpg

    # 2. Crop-specific Pathology Diagnosis
    python run_inference.py --crop potato --image sample_images/potato_sample.jpg
    python run_inference.py --crop rice --image sample_images/rice_sample.jpg
    python run_inference.py --crop wheat --image sample_images/wheat_sample.jpg
    python run_inference.py --crop corn --image sample_images/corn_sample.jpg
    python run_inference.py --crop chilli --image sample_images/chilli_sample.jpg
    python run_inference.py --crop brassica --image sample_images/brassica_sample.jpg

    # 3. Soil Moisture Tension (kPa) Prediction
    python run_inference.py --task soil --image sample_images/crop_sample.jpg
"""

import argparse
import json
import sys
from pathlib import Path
from PIL import Image
import numpy as np

try:
    import torch
    from ultralytics import YOLO
except ImportError as e:
    print(f"Error: Required libraries missing. Run: pip install -r requirements.txt\n{e}")
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent

CROP_MAP = {
    "crop": ("01_crop_classifier", "crop_classifier.pt"),
    "intake": ("01_crop_classifier", "crop_classifier.pt"),
    "potato": ("02_potato_disease", "potato_disease.pt"),
    "rice": ("03_rice_disease", "rice_disease.pt"),
    "wheat": ("04_wheat_disease", "wheat_disease.pt"),
    "corn": ("05_corn_disease", "corn_disease.pt"),
    "maize": ("05_corn_disease", "corn_disease.pt"),
    "chilli": ("06_chilli_disease", "chilli_disease.pt"),
    "chili": ("06_chilli_disease", "chilli_disease.pt"),
    "brassica": ("07_brassica_disease", "brassica_disease.pt"),
    "cabbage": ("07_brassica_disease", "brassica_disease.pt"),
    "cauliflower": ("07_brassica_disease", "brassica_disease.pt"),
}


def run_vision(crop: str, image_path: Path, topk: int = 3):
    folder, model_file = CROP_MAP[crop.lower()]
    model_path = BASE_DIR / folder / model_file
    classes_path = BASE_DIR / folder / "class_names.json"
    details_path = BASE_DIR / folder / "disease_details.json"

    print(f"Loading YOLO26 model: {model_path.relative_to(BASE_DIR)} ...")
    model = YOLO(str(model_path))

    with open(classes_path, encoding="utf-8") as f:
        classes = json.load(f)
        if isinstance(classes, dict):
            class_names = [classes[str(i)] for i in range(len(classes))]
        else:
            class_names = list(classes)

    print(f"Processing image: {image_path.name} ...")
    img = Image.open(image_path).convert("RGB")
    results = model.predict(img, imgsz=224, verbose=False)[0]

    probs = results.probs.data.cpu().numpy()
    top_indices = np.argsort(probs)[::-1][:topk]

    print("\n" + "=" * 60)
    print(f" DIAGNOSTIC RESULTS ({crop.upper()} - YOLO26)")
    print("=" * 60)
    for rank, idx in enumerate(top_indices, 1):
        c_name = class_names[idx] if idx < len(class_names) else str(idx)
        conf = float(probs[idx])
        print(f" {rank}. {c_name:<35} | Confidence: {conf:6.2%}")
    print("-" * 60)

    # Print agronomic advice if disease details exist
    if details_path.exists():
        top_label = class_names[top_indices[0]]
        try:
            with open(details_path, encoding="utf-8") as f:
                details = json.load(f)
            # Find matching advice section
            advice_found = False
            for sec_key, sec_val in details.items():
                if isinstance(sec_val, dict) and "classes" in sec_val:
                    for entry in sec_val["classes"]:
                        if entry.get("name") == top_label or top_label.endswith(entry.get("name", "___")):
                            print("\nAGRONOMIC MANAGEMENT ADVICE:")
                            if "bangla_name" in entry:
                                print(f" • রোগ (বাংলা): {entry['bangla_name']}")
                            if "symptoms" in entry:
                                print(f" • Symptoms: {entry['symptoms']}")
                            if "organic_control" in entry:
                                print(f" • জৈব প্রতিকার: {entry['organic_control']}")
                            if "chemical_control" in entry:
                                print(f" • রাসায়নিক নিয়ন্ত্রণ: {entry['chemical_control']}")
                            advice_found = True
                            break
                if advice_found:
                    break
        except Exception:
            pass


def run_soil(image_path: Path):
    soil_dir = BASE_DIR / "08_soil_moisture"
    sys.path.insert(0, str(soil_dir))
    from model_def import load_soil_model
    import torchvision.transforms as T

    transform = T.Compose([
        T.Resize((224, 224)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    img = Image.open(image_path).convert("RGB")
    tensor = transform(img).unsqueeze(0)

    print("Running 5-Fold EfficientNet-B0 Ensemble for Soil Moisture Tension ...")
    preds = []
    for fold in range(5):
        m = load_soil_model(soil_dir / f"effnetb0_fold{fold}.pt", device="cpu")
        with torch.no_grad():
            val = m(tensor).item()
            preds.append(val)
            print(f" • Fold {fold}: {val:6.2f} kPa")

    mean_kpa = sum(preds) / len(preds)
    print("-" * 60)
    print(f" ENSEMBLE PREDICTED SOIL TENSION: {mean_kpa:6.2f} kPa")

    # Status
    if mean_kpa < 10.0:
        status = "Field Capacity / High Moisture (No irrigation needed)"
    elif mean_kpa < 30.0:
        status = "Optimal Moisture for Vegetative Growth"
    elif mean_kpa < 50.0:
        status = "Moderate Drying (Plan irrigation in 24-48 hrs)"
    else:
        status = "Moisture Deficit (Irrigate immediately)"
    print(f" STATUS: {status}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="KrishokChat ML Standalone Inference CLI")
    parser.add_argument("--crop", type=str, choices=list(CROP_MAP.keys()), help="Target crop or 'crop' for intake classifier")
    parser.add_argument("--task", type=str, choices=["vision", "soil"], default="vision", help="ML Task")
    parser.add_argument("--image", type=str, required=True, help="Path to input RGB image")
    parser.add_argument("--topk", type=int, default=3, help="Top-K classes to display")
    args = parser.parse_args()

    img_path = Path(args.image)
    if not img_path.exists():
        print(f"Error: Image not found: {img_path}")
        sys.exit(1)

    if args.task == "soil":
        run_soil(img_path)
    else:
        if not args.crop:
            print("Error: Specify --crop <crop_name> (e.g. potato, rice, wheat, corn, chilli, brassica, crop)")
            sys.exit(1)
        run_vision(args.crop, img_path, args.topk)


if __name__ == "__main__":
    main()
