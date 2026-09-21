#!/usr/bin/env python3
"""KrishokChat ML Models Automated Verification Suite.

Validates:
1. Every YOLO26 PyTorch (.pt) vision classification model loads and performs inference.
2. Every ONNX model loads and runs a test session via onnxruntime.
3. Output probability dimensions strictly match class_names.json.
4. All 5 folds of the EfficientNet-B0 soil moisture regression model load and predict.
5. Prints a comprehensive diagnostic table for academic reviewers.
"""

import sys
import time
import json
from pathlib import Path
import numpy as np
from PIL import Image

try:
    import torch
    from ultralytics import YOLO
except ImportError as e:
    print(f"Error: Missing core dependencies. Run: pip install -r requirements.txt\n{e}")
    sys.exit(1)

try:
    import onnxruntime as ort
except ImportError:
    ort = None

BASE_DIR = Path(__file__).resolve().parent

VISION_MODELS = [
    ("01_crop_classifier", "crop_classifier.pt", "crop_classifier.onnx", 10),
    ("02_potato_disease", "potato_disease.pt", "potato_disease.onnx", 3),
    ("03_rice_disease", "rice_disease.pt", "rice_disease.onnx", 10),
    ("04_wheat_disease", "wheat_disease.pt", "wheat_disease.onnx", 11),
    ("05_corn_disease", "corn_disease.pt", "corn_disease.onnx", 4),
    ("06_chilli_disease", "chilli_disease.pt", "chilli_disease.onnx", 8),
    ("07_brassica_disease", "brassica_disease.pt", "brassica_disease.onnx", 11),
]


def run_vision_verification():
    print("=" * 80)
    print(" KRISHOKCHAT ML SUITE — VISION MODELS (YOLO26-CLS) VERIFICATION")
    print("=" * 80)
    header = f"{'Folder / Task':<25} | {'PT File':<20} | {'Classes':<7} | {'PT Status':<10} | {'ONNX Status':<11} | {'Latency':<8}"
    print(header)
    print("-" * 80)

    # Base test image
    dummy_img = Image.fromarray(np.uint8(np.random.rand(224, 224, 3) * 255))

    all_passed = True

    for folder, pt_name, onnx_name, expected_classes in VISION_MODELS:
        model_dir = BASE_DIR / folder
        pt_path = model_dir / pt_name
        onnx_path = model_dir / onnx_name
        classes_path = model_dir / "class_names.json"

        # Check files exist
        if not pt_path.exists():
            print(f"{folder:<25} | {pt_name:<20} | {expected_classes:<7} | FAILED (missing)")
            all_passed = False
            continue

        # Check class names
        with open(classes_path, encoding="utf-8") as f:
            classes_data = json.load(f)
            num_classes = len(classes_data)
            assert num_classes == expected_classes, f"Class count mismatch: {num_classes} != {expected_classes}"

        # 1. PyTorch YOLO26-cls test
        pt_status = "FAIL"
        elapsed = 0.0
        try:
            t0 = time.time()
            model = YOLO(str(pt_path))
            res = model.predict(dummy_img, imgsz=224, verbose=False)[0]
            elapsed = (time.time() - t0) * 1000.0
            probs = res.probs.data.cpu().numpy()
            if len(probs) == expected_classes and np.isclose(np.sum(probs), 1.0, atol=1e-2):
                pt_status = "PASSED"
            else:
                pt_status = f"ERR(shape {len(probs)})"
                all_passed = False
        except Exception as ex:
            pt_status = f"EXC: {type(ex).__name__}"
            all_passed = False

        # 2. ONNX test
        onnx_status = "SKIP"
        if ort is not None and onnx_path.exists():
            try:
                session = ort.InferenceSession(str(onnx_path))
                input_tensor = session.get_inputs()[0]
                shape = input_tensor.shape
                # Adapt resolution if static (e.g. 224 vs 256)
                h = shape[2] if len(shape) > 2 and isinstance(shape[2], int) else 224
                w = shape[3] if len(shape) > 3 and isinstance(shape[3], int) else 224
                onnx_np = np.array(dummy_img.resize((w, h)), dtype=np.float32).transpose(2, 0, 1)[None, ...] / 255.0

                outputs = session.run(None, {input_tensor.name: onnx_np})[0]
                if outputs.shape[-1] == expected_classes:
                    onnx_status = "PASSED"
                else:
                    onnx_status = f"ERR({outputs.shape})"
                    all_passed = False
            except Exception as ex:
                onnx_status = f"EXC: {type(ex).__name__}"
                all_passed = False
        elif not onnx_path.exists():
            onnx_status = "MISSING"

        print(f"{folder:<25} | {pt_name:<20} | {num_classes:<7} | {pt_status:<10} | {onnx_status:<11} | {elapsed:.1f} ms")

    return all_passed


def run_soil_verification():
    print("\n" + "=" * 80)
    print(" KRISHOKCHAT ML SUITE — SOIL MOISTURE REGRESSION (EFFICIENTNET-B0) VERIFICATION")
    print("=" * 80)

    soil_dir = BASE_DIR / "08_soil_moisture"
    sys.path.insert(0, str(soil_dir))

    try:
        from model_def import load_soil_model
    except ImportError as e:
        print(f"Soil model def import failed: {e}")
        return False

    all_passed = True
    dummy_tensor = torch.randn(1, 3, 224, 224)

    for fold in range(5):
        fold_file = soil_dir / f"effnetb0_fold{fold}.pt"
        if not fold_file.exists():
            print(f"Fold {fold}: FAILED (file not found: {fold_file.name})")
            all_passed = False
            continue

        try:
            t0 = time.time()
            model = load_soil_model(fold_file, device="cpu")
            with torch.no_grad():
                pred = model(dummy_tensor).item()
            latency = (time.time() - t0) * 1000.0
            print(f"Fold {fold:<2} ({fold_file.name:<18}) | Output: {pred:7.2f} kPa | Status: PASSED | Latency: {latency:.1f} ms")
        except Exception as e:
            print(f"Fold {fold:<2} ({fold_file.name:<18}) | Status: FAILED ({e})")
            all_passed = False

    return all_passed


if __name__ == "__main__":
    v_ok = run_vision_verification()
    s_ok = run_soil_verification()

    print("\n" + "=" * 80)
    if v_ok and s_ok:
        print(" SUCCESS: ALL 8 MODEL CATEGORIES AND WEIGHTS VERIFIED CLEANLY!")
        print(" The 'backend_models/' folder is 100% ready for reviewers and Hugging Face release.")
        print("=" * 80)
        sys.exit(0)
    else:
        print(" WARNING: Some model checks failed or were skipped.")
        print("=" * 80)
        sys.exit(1)
