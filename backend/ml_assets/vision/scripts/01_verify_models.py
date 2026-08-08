"""
Vision Model Verification Script.
Loads each model, extracts REAL class names from weights, runs predictions on test images.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from ultralytics import YOLO

VISION_DIR = Path(__file__).resolve().parent.parent
TEST_DIR = VISION_DIR / "test_images"

MODELS = {
    "crop_classifier": {
        "path": VISION_DIR / "crop_classifier" / "model.pt",
        "test_dir": TEST_DIR / "crop_classifier",
    },
    "rice_disease": {
        "path": VISION_DIR / "rice_disease" / "model.pt",
        "test_dir": TEST_DIR / "rice_disease",
    },
    "wheat_disease": {
        "path": VISION_DIR / "wheat_disease" / "model.pt",
        "test_dir": TEST_DIR / "wheat_disease",
    },
    "corn_disease": {
        "path": VISION_DIR / "corn_disease" / "model.pt",
        "test_dir": TEST_DIR / "corn_disease",
    },
    "potato_disease": {
        "path": VISION_DIR / "potato_disease" / "model.pt",
        "test_dir": TEST_DIR / "potato_disease",
    },
    "brassica_disease": {
        "path": VISION_DIR / "brassica_disease" / "model.pt",
        "test_dir": TEST_DIR / "brassica_disease",
    },
}


def verify_model(name, config):
    """Load model, extract class names, run predictions."""
    print(f"\n{'='*60}")
    print(f"VERIFYING: {name}")
    print(f"{'='*60}")

    model_path = config["path"]
    test_dir = config["test_dir"]

    # Check model file exists
    if not model_path.exists():
        print(f"  ❌ Model file not found: {model_path}")
        return None

    size_mb = model_path.stat().st_size / 1e6
    print(f"  Model file: {model_path.name} ({size_mb:.2f} MB)")

    # Load model
    try:
        model = YOLO(str(model_path))
        print(f"  ✅ Model loaded successfully")
    except Exception as e:
        print(f"  ❌ Failed to load model: {e}")
        return None

    # Extract REAL class names from weights
    names = model.names
    print(f"  Classes ({len(names)}): {list(names.values())}")

    # Save class names to JSON
    class_names_path = model_path.parent / "class_names.json"
    with open(class_names_path, "w", encoding="utf-8") as f:
        json.dump(names, f, ensure_ascii=False, indent=2)
    print(f"  ✅ Class names saved to: {class_names_path.name}")

    # Check if it's a classifier or detector
    task = getattr(model, "task", "unknown")
    print(f"  Task type: {task}")

    # Run predictions on test images
    if not test_dir.exists() or not any(test_dir.iterdir()):
        print(f"  ⚠️  No test images found in {test_dir.name}")
        return {"name": name, "classes": list(names.values()), "task": task, "predictions": []}

    images = list(test_dir.glob("*.jpg")) + list(test_dir.glob("*.png")) + list(test_dir.glob("*.jpeg"))
    print(f"  Test images found: {len(images)}")

    predictions = []
    for img_path in images[:5]:  # Max 5 images
        try:
            result = model(str(img_path), verbose=False)[0]

            # Classification: use .probs
            if hasattr(result, "probs") and result.probs is not None:
                probs = result.probs.data.cpu().numpy()
                top_idx = int(np.argmax(probs))
                top_conf = float(probs[top_idx])
                pred_class = names[top_idx]
                pred = {
                    "image": img_path.name,
                    "predicted_class": pred_class,
                    "confidence": round(top_conf, 4),
                    "top3": [
                        {"class": names[i], "conf": round(float(probs[i]), 4)}
                        for i in np.argsort(probs)[-3:][::-1]
                    ],
                }
                predictions.append(pred)
                print(f"    📷 {img_path.name}: {pred_class} ({top_conf:.1%})")

            # Detection: use .boxes
            elif hasattr(result, "boxes") and result.boxes is not None and len(result.boxes) > 0:
                boxes = result.boxes
                pred = {
                    "image": img_path.name,
                    "detections": len(boxes),
                    "boxes": [],
                }
                for i in range(len(boxes)):
                    cls_idx = int(boxes.cls[i])
                    conf = float(boxes.conf[i])
                    pred["boxes"].append({
                        "class": names[cls_idx],
                        "confidence": round(conf, 4),
                    })
                predictions.append(pred)
                print(f"    📷 {img_path.name}: {len(boxes)} detections")

            else:
                print(f"    📷 {img_path.name}: No predictions (unknown result type)")
                predictions.append({"image": img_path.name, "predictions": "none"})

        except Exception as e:
            print(f"    ❌ {img_path.name}: Prediction failed — {e}")
            predictions.append({"image": img_path.name, "error": str(e)})

    return {
        "name": name,
        "classes": list(names.values()),
        "task": task,
        "model_size_mb": round(size_mb, 2),
        "predictions": predictions,
    }


def main():
    print("=" * 60)
    print("VISION MODEL VERIFICATION")
    print("=" * 60)

    results = {}
    for name, config in MODELS.items():
        result = verify_model(name, config)
        if result:
            results[name] = result

    # Summary
    print(f"\n{'='*60}")
    print("VERIFICATION SUMMARY")
    print(f"{'='*60}")

    for name, r in results.items():
        n_classes = len(r["classes"])
        n_preds = len(r.get("predictions", []))
        task = r.get("task", "?")
        size = r.get("model_size_mb", "?")
        print(f"  {name:>20}: {n_classes:2d} classes, {n_preds} predictions, task={task}, {size}MB")

    # Save full results
    report_path = VISION_DIR / "verification_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nFull report saved to: {report_path}")

    # Check for wheat-disease issue
    if "wheat_disease" in results and "crop_classifier" in results:
        wheat_classes = results["wheat_disease"]["classes"]
        crop_classes = results["crop_classifier"]["classes"]
        if wheat_classes == crop_classes:
            print(f"\n  ⚠️  WHEAT DISEASE model is IDENTICAL to CROP CLASSIFIER!")
            print(f"      This is a placeholder — real wheat disease model needed.")


if __name__ == "__main__":
    main()
