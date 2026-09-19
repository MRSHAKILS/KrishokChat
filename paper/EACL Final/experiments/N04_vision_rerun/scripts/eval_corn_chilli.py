"""Evaluation script for Corn and Chilli ONNX and PyTorch models on full test sets.

Evaluates:
- Corn: D:\\499A Dataset\\Corn\\test (940 images across 4 classes)
  Model: backend/ml_assets/vision/onnx/corn.onnx & corn_disease/model.pt (imgsz=256)
- Chilli: D:\\499A Dataset\\Solanaceae\\test (Chili__* folders: 861 images across 7 classes)
  Model: backend/ml_assets/vision/onnx/chilli.onnx & chilli_disease/model.pt (imgsz=224)

Computes:
- Top-1 Accuracy with Wilson 95% Confidence Interval
- Per-class Accuracy, Precision, Recall, F1
- ONNX vs PyTorch parity (agreement rate, max delta)
- Latency percentiles (p50, p90, p95, p99)
- Outputs full report to JSON and Markdown
"""

import json
import math
import os
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
import onnxruntime as ort
import torch
from PIL import Image
from ultralytics import YOLO

# Add common script dir
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _vision_common import percentiles, preprocess_numpy, softmax


def wilson_ci(k: int, n: int, confidence: float = 0.95) -> tuple[float, float]:
    """Calculate Wilson score interval for binomial proportion."""
    if n == 0:
        return (0.0, 0.0)
    z = 1.959963984540054  # for 95% confidence
    p = k / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    spread = z * math.sqrt((p * (1 - p) + z**2 / (4 * n)) / n) / denom
    return (max(0.0, center - spread), min(1.0, center + spread))


def evaluate_model(
    crop_name: str,
    test_dir: Path,
    class_map: dict[str, int],
    onnx_path: Path,
    pt_path: Path,
    imgsz: int,
):
    print(f"\n{'='*60}")
    print(f"Starting Evaluation for {crop_name.upper()}")
    print(f"Test Dir: {test_dir}")
    print(f"ONNX Model: {onnx_path} (imgsz={imgsz})")
    print(f"PT Model:   {pt_path}")
    print(f"{'='*60}")

    # Load models
    session = ort.InferenceSession(str(onnx_path), providers=["CPUExecutionProvider"])
    pt_model = YOLO(str(pt_path))

    # Invert class map for reporting
    idx_to_class = {v: k for k, v in class_map.items()}

    # Collect images
    samples = []
    for class_folder_name, class_idx in class_map.items():
        folder = test_dir / class_folder_name
        if not folder.exists() or not folder.is_dir():
            print(f"Warning: folder {folder} does not exist!")
            continue
        valid_exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
        files = [f for f in folder.iterdir() if f.suffix.lower() in valid_exts]
        for f in files:
            samples.append((f, class_idx, class_folder_name))

    print(f"Total test images collected: {len(samples)}")
    if len(samples) == 0:
        return None

    # Track metrics
    onnx_correct = 0
    pt_correct = 0
    agree_count = 0
    max_delta = 0.0
    onnx_latencies = []

    per_class_total = defaultdict(int)
    per_class_onnx_correct = defaultdict(int)
    per_class_pt_correct = defaultdict(int)

    # For confusion matrix: confusion[true_idx][pred_idx]
    num_classes = max(class_map.values()) + 1
    confusion_onnx = np.zeros((num_classes, num_classes), dtype=int)

    for idx, (img_path, true_label, true_class_name) in enumerate(samples):
        if (idx + 1) % 100 == 0 or idx + 1 == len(samples):
            print(f"  Processed {idx + 1}/{len(samples)} images...")

        img = Image.open(img_path).convert("RGB")
        input_tensor = preprocess_numpy(img, imgsz)

        # 1. ONNX Inference
        t0 = time.perf_counter()
        onnx_outs = session.run(None, {"images": input_tensor})
        t1 = time.perf_counter()
        onnx_latencies.append((t1 - t0) * 1000.0)

        onnx_logits = onnx_outs[0][0]
        onnx_probs = softmax(onnx_logits)
        onnx_pred = int(np.argmax(onnx_probs))

        # 2. PyTorch Inference (via predict on PIL image or tensor)
        # To strictly match Ultralytics inference:
        pt_results = pt_model.predict(img, imgsz=imgsz, verbose=False)
        pt_probs = pt_results[0].probs.data.cpu().numpy()
        pt_pred = int(np.argmax(pt_probs))

        # Parity
        if onnx_pred == pt_pred:
            agree_count += 1
        delta = float(np.max(np.abs(onnx_probs - pt_probs)))
        if delta > max_delta:
            max_delta = delta

        # Accuracy
        if onnx_pred == true_label:
            onnx_correct += 1
            per_class_onnx_correct[true_label] += 1
        if pt_pred == true_label:
            pt_correct += 1
            per_class_pt_correct[true_label] += 1

        per_class_total[true_label] += 1
        confusion_onnx[true_label][onnx_pred] += 1

    total_n = len(samples)
    onnx_top1 = onnx_correct / total_n
    pt_top1 = pt_correct / total_n
    onnx_ci = wilson_ci(onnx_correct, total_n)
    pt_ci = wilson_ci(pt_correct, total_n)
    agree_rate = agree_count / total_n
    lat_stats = percentiles(onnx_latencies)

    # Per-class metrics
    per_class_stats = {}
    for c_idx in sorted(idx_to_class.keys()):
        c_name = idx_to_class[c_idx]
        n_c = per_class_total[c_idx]
        c_correct = per_class_onnx_correct[c_idx]
        acc_c = c_correct / n_c if n_c > 0 else 0.0
        ci_c = wilson_ci(c_correct, n_c) if n_c > 0 else (0.0, 0.0)

        # Precision & Recall from confusion matrix
        tp = confusion_onnx[c_idx][c_idx]
        fp = sum(confusion_onnx[other][c_idx] for other in range(num_classes) if other != c_idx)
        fn = sum(confusion_onnx[c_idx][other] for other in range(num_classes) if other != c_idx)

        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0

        per_class_stats[c_name] = {
            "index": c_idx,
            "total_images": n_c,
            "correct": c_correct,
            "accuracy": round(acc_c, 4),
            "ci95": [round(ci_c[0], 4), round(ci_c[1], 4)],
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1": round(f1, 4),
        }

    res = {
        "crop": crop_name,
        "n_samples": total_n,
        "onnx_top1": round(onnx_top1, 4),
        "onnx_ci95": [round(onnx_ci[0], 4), round(onnx_ci[1], 4)],
        "pt_top1": round(pt_top1, 4),
        "pt_ci95": [round(pt_ci[0], 4), round(pt_ci[1], 4)],
        "onnx_pt_agreement": round(agree_rate, 4),
        "onnx_max_delta": float(f"{max_delta:.6e}"),
        "latency_stats_ms": lat_stats,
        "per_class": per_class_stats,
    }

    print(f"\n--- {crop_name.upper()} RESULTS ---")
    print(f"N = {total_n}")
    print(f"ONNX Top-1 Accuracy: {onnx_top1*100:.2f}% (95% CI: [{onnx_ci[0]*100:.2f}%, {onnx_ci[1]*100:.2f}%])")
    print(f"PyTorch Top-1 Accuracy: {pt_top1*100:.2f}% (95% CI: [{pt_ci[0]*100:.2f}%, {pt_ci[1]*100:.2f}%])")
    print(f"ONNX/PT Agreement: {agree_rate*100:.2f}%, Max Delta: {max_delta:.6e}")
    print(f"Latency p50: {lat_stats['p50_ms']:.2f} ms, p95: {lat_stats['p95_ms']:.2f} ms")
    print("Per Class:")
    for c_name, s in per_class_stats.items():
        print(f"  {c_name} (n={s['total_images']}): Acc={s['accuracy']*100:.2f}%, F1={s['f1']:.4f}")

    return res


def main():
    backend_vision = Path("backend/ml_assets/vision")

    # 1. Corn Setup
    corn_classes = {
        "Common_Rust": 0,
        "Gray_Leaf_Spot": 1,
        "Healthy": 2,
        "Northern_Leaf_Blight": 3,
    }
    corn_test_dir = Path(r"D:\499A Dataset\Corn\test")
    corn_onnx = backend_vision / "onnx" / "corn.onnx"
    corn_pt = backend_vision / "corn_disease" / "model.pt"

    corn_results = evaluate_model(
        crop_name="corn",
        test_dir=corn_test_dir,
        class_map=corn_classes,
        onnx_path=corn_onnx,
        pt_path=corn_pt,
        imgsz=256,
    )

    # 2. Chilli Setup
    # Notice in chilli_classes.json:
    # 0: Chili__Bacterial_Spot, 1: Chili__Cercospora_Leaf_Spot, 2: Chili__Curl_Virus,
    # 3: Chili__Healthy_Leaf, 4: Chili__Nutrition_Deficiency, 5: Others,
    # 6: Chili__Powdery_Mildew, 7: Chili__White_Spot
    chilli_classes = {
        "Chili__Bacterial_Spot": 0,
        "Chili__Cercospora_Leaf_Spot": 1,
        "Chili__Curl_Virus": 2,
        "Chili__Healthy_Leaf": 3,
        "Chili__Nutrition_Deficiency": 4,
        "Chili__Powdery_Mildew": 6,
        "Chili__White_Spot": 7,
    }
    chilli_test_dir = Path(r"D:\499A Dataset\Solanaceae\test")
    chilli_onnx = backend_vision / "onnx" / "chilli.onnx"
    chilli_pt = backend_vision / "chilli_disease" / "model.pt"

    chilli_results = evaluate_model(
        crop_name="chilli",
        test_dir=chilli_test_dir,
        class_map=chilli_classes,
        onnx_path=chilli_onnx,
        pt_path=chilli_pt,
        imgsz=224,
    )

    out_file = Path(r"D:\KrishokChat Advisory System\paper\EACL Final\experiments\results\corn_chilli_eval_results.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    combined = {
        "evaluation_target": "Corn and Chilli On-Device Edge Classifiers",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "results": {
            "corn": corn_results,
            "chilli": chilli_results,
        },
    }
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2)
    print(f"\nSaved full results to: {out_file}")


if __name__ == "__main__":
    main()
