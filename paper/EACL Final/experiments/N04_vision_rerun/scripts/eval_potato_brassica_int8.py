"""Evaluation script for Potato and Brassica FP32 vs INT8 ONNX models on full test sets.

Evaluates:
- Potato: D:\\499A Dataset\\Potato\\test (1,170 images across 3 classes)
  FP32: backend/ml_assets/vision/onnx/potato.onnx (imgsz=224)
  INT8: backend/ml_assets/vision/onnx_int8/potato_int8.onnx (imgsz=224)
- Brassica: D:\\499A Dataset\\Brassica\\test (443 images across 11 classes)
  FP32: backend/ml_assets/vision/onnx/brassica.onnx (imgsz=256)
  INT8: backend/ml_assets/vision/onnx_int8/brassica_int8.onnx (imgsz=256)

Computes:
- Top-1 Accuracy (FP32 and INT8) with Wilson 95% Confidence Intervals
- Accuracy drop in percentage points (Gate: <= 2.0 pp drop)
- FP32 vs INT8 Agreement Rate
- Two-sided exact binomial McNemar test
- Latency percentiles (FP32 vs INT8)
- Per-class metrics
"""

import json
import math
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
import onnxruntime as ort
from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _vision_common import percentiles, preprocess_numpy, softmax


def wilson_ci(k: int, n: int, confidence: float = 0.95) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    z = 1.959963984540054
    p = k / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    spread = z * math.sqrt((p * (1 - p) + z**2 / (4 * n)) / n) / denom
    return (max(0.0, center - spread), min(1.0, center + spread))


def mcnemar_exact(only_a: int, only_b: int) -> dict:
    n = only_a + only_b
    if n == 0:
        return {"discordant_pairs": 0, "p_value": 1.0, "interpretation": "identical predictions; no discordance"}
    larger = max(only_a, only_b)
    tail = sum(math.comb(n, k) for k in range(larger, n + 1)) * (0.5**n)
    p_value = min(1.0, 2.0 * tail)
    return {
        "discordant_pairs": n,
        "only_fp32_correct": only_a,
        "only_int8_correct": only_b,
        "p_value": round(p_value, 6),
        "test": "two-sided exact binomial McNemar (paired)",
        "statistically_significant": p_value < 0.05,
    }


def evaluate_int8_pair(
    crop_name: str,
    test_dir: Path,
    class_map: dict[str, int],
    fp32_path: Path,
    int8_path: Path,
    imgsz: int,
):
    print(f"\n{'='*65}")
    print(f"Starting FP32 vs INT8 Evaluation for {crop_name.upper()}")
    print(f"Test Dir:  {test_dir}")
    print(f"FP32 ONNX: {fp32_path} (imgsz={imgsz})")
    print(f"INT8 ONNX: {int8_path} (imgsz={imgsz})")
    print(f"{'='*65}")

    sess_fp32 = ort.InferenceSession(str(fp32_path), providers=["CPUExecutionProvider"])
    sess_int8 = ort.InferenceSession(str(int8_path), providers=["CPUExecutionProvider"])

    input_name_fp32 = sess_fp32.get_inputs()[0].name
    input_name_int8 = sess_int8.get_inputs()[0].name
    idx_to_class = {v: k for k, v in class_map.items()}

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

    fp32_correct = 0
    int8_correct = 0
    agree_count = 0
    only_fp32 = 0
    only_int8 = 0
    max_delta = 0.0

    fp32_latencies = []
    int8_latencies = []

    per_class_total = defaultdict(int)
    per_class_fp32_correct = defaultdict(int)
    per_class_int8_correct = defaultdict(int)

    for idx, (img_path, true_label, true_class_name) in enumerate(samples):
        if (idx + 1) % 200 == 0 or idx + 1 == len(samples):
            print(f"  Processed {idx + 1}/{len(samples)} images...")

        img = Image.open(img_path).convert("RGB")
        input_tensor = preprocess_numpy(img, imgsz)

        # FP32 inference
        t0 = time.perf_counter()
        out_fp32 = sess_fp32.run(None, {input_name_fp32: input_tensor})
        t1 = time.perf_counter()
        fp32_latencies.append((t1 - t0) * 1000.0)

        probs_fp32 = softmax(out_fp32[0][0])
        pred_fp32 = int(np.argmax(probs_fp32))

        # INT8 inference
        t0 = time.perf_counter()
        out_int8 = sess_int8.run(None, {input_name_int8: input_tensor})
        t1 = time.perf_counter()
        int8_latencies.append((t1 - t0) * 1000.0)

        probs_int8 = softmax(out_int8[0][0])
        pred_int8 = int(np.argmax(probs_int8))

        # Agreement & delta
        if pred_fp32 == pred_int8:
            agree_count += 1
        delta = float(np.max(np.abs(probs_fp32 - probs_int8)))
        if delta > max_delta:
            max_delta = delta

        # Accuracy
        fp32_hit = (pred_fp32 == true_label)
        int8_hit = (pred_int8 == true_label)

        if fp32_hit:
            fp32_correct += 1
            per_class_fp32_correct[true_label] += 1
        if int8_hit:
            int8_correct += 1
            per_class_int8_correct[true_label] += 1

        if fp32_hit and not int8_hit:
            only_fp32 += 1
        elif int8_hit and not fp32_hit:
            only_int8 += 1

        per_class_total[true_label] += 1

    total_n = len(samples)
    fp32_top1 = fp32_correct / total_n
    int8_top1 = int8_correct / total_n
    drop_pp = (fp32_top1 - int8_top1) * 100.0

    fp32_ci = wilson_ci(fp32_correct, total_n)
    int8_ci = wilson_ci(int8_correct, total_n)
    agree_rate = agree_count / total_n

    mcnemar = mcnemar_exact(only_fp32, only_int8)
    fp32_lat_stats = percentiles(fp32_latencies)
    int8_lat_stats = percentiles(int8_latencies)

    # Gate check: drop <= 2.0pp, n >= 100
    gate_passed = (drop_pp <= 2.0) and (total_n >= 100)

    per_class_stats = {}
    for c_idx in sorted(idx_to_class.keys()):
        c_name = idx_to_class[c_idx]
        n_c = per_class_total[c_idx]
        c_fp32 = per_class_fp32_correct[c_idx]
        c_int8 = per_class_int8_correct[c_idx]
        per_class_stats[c_name] = {
            "index": c_idx,
            "total_images": n_c,
            "fp32_correct": c_fp32,
            "fp32_accuracy": round(c_fp32 / n_c, 4) if n_c > 0 else 0.0,
            "int8_correct": c_int8,
            "int8_accuracy": round(c_int8 / n_c, 4) if n_c > 0 else 0.0,
        }

    res = {
        "crop": crop_name,
        "n_samples": total_n,
        "fp32_top1": round(fp32_top1, 4),
        "fp32_ci95": [round(fp32_ci[0], 4), round(fp32_ci[1], 4)],
        "int8_top1": round(int8_top1, 4),
        "int8_ci95": [round(int8_ci[0], 4), round(int8_ci[1], 4)],
        "drop_pp": round(drop_pp, 4),
        "agreement_rate": round(agree_rate, 4),
        "max_delta": float(f"{max_delta:.6e}"),
        "gate_passed_2pp": gate_passed,
        "reportable": total_n >= 100,
        "mcnemar": mcnemar,
        "fp32_latency_ms": fp32_lat_stats,
        "int8_latency_ms": int8_lat_stats,
        "per_class": per_class_stats,
    }

    print(f"\n--- {crop_name.upper()} INT8 RESULTS ---")
    print(f"N = {total_n} (Reportable: {total_n >= 100})")
    print(f"FP32 Top-1: {fp32_top1*100:.2f}% (95% CI: [{fp32_ci[0]*100:.2f}%, {fp32_ci[1]*100:.2f}%])")
    print(f"INT8 Top-1: {int8_top1*100:.2f}% (95% CI: [{int8_ci[0]*100:.2f}%, {int8_ci[1]*100:.2f}%])")
    print(f"Drop: {drop_pp:.2f} pp (Gate <= 2.0pp: {'PASSED' if gate_passed else 'REJECTED'})")
    print(f"Agreement Rate: {agree_rate*100:.2f}%, Max Delta: {max_delta:.6e}")
    print(f"McNemar p-value: {mcnemar['p_value']}")
    print(f"Latency FP32 p50: {fp32_lat_stats['p50_ms']:.2f} ms | INT8 p50: {int8_lat_stats['p50_ms']:.2f} ms")

    return res


def main():
    backend_vision = Path("backend/ml_assets/vision")

    # 1. Potato
    potato_classes = {
        "Potato__Early_Blight": 0,
        "Potato__Healthy_Leaf": 1,
        "Potato__Late_Blight": 2,
    }
    potato_test_dir = Path(r"D:\499A Dataset\Potato\test")
    potato_fp32 = backend_vision / "onnx" / "potato.onnx"
    potato_int8 = backend_vision / "onnx_int8" / "potato_int8.onnx"

    potato_results = evaluate_int8_pair(
        crop_name="potato",
        test_dir=potato_test_dir,
        class_map=potato_classes,
        fp32_path=potato_fp32,
        int8_path=potato_int8,
        imgsz=224,
    )

    # 2. Brassica
    brassica_classes = {
        "Cabbage__Alternaria_Spot": 0,
        "Cabbage__Black_Rot": 1,
        "Cabbage__Downy_Mildew": 2,
        "Cabbage__Healthy_Leaf": 3,
        "Cauliflower__Alternaria_Disease": 4,
        "Cauliflower__Bacterial_Soft_Rot": 5,
        "Cauliflower__Bacterial_Spot": 6,
        "Cauliflower__Black_Spot": 7,
        "Cauliflower__Downy_Mildew": 8,
        "Cauliflower__Healthy": 9,
        "Cauliflower__Nutrient_Deficiency": 10,
    }
    brassica_test_dir = Path(r"D:\499A Dataset\Brassica\test")
    brassica_fp32 = backend_vision / "onnx" / "brassica.onnx"
    brassica_int8 = backend_vision / "onnx_int8" / "brassica_int8.onnx"

    brassica_results = evaluate_int8_pair(
        crop_name="brassica",
        test_dir=brassica_test_dir,
        class_map=brassica_classes,
        fp32_path=brassica_fp32,
        int8_path=brassica_int8,
        imgsz=256,
    )

    out_file = Path(r"D:\KrishokChat Advisory System\paper\EACL Final\experiments\results\potato_brassica_int8_results.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    combined = {
        "evaluation_target": "Potato and Brassica FP32 vs INT8 Full Test Set Evaluation",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "results": {
            "potato": potato_results,
            "brassica": brassica_results,
        },
    }
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2)
    print(f"\nSaved full INT8 results to: {out_file}")


if __name__ == "__main__":
    main()
