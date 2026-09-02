#!/usr/bin/env python3
"""
experiments/scripts/verify_crops_classifier_s.py
Deep technical verification and empirical testing of the 10-Class Crop Classifier in:
backend/ml_assets/updated retrain/crops_classifier/s/
and inspecting the notebook yolo26-cls-fine-tuning-on-a-cleaned-10-class-crop.ipynb.
"""

from __future__ import annotations

import csv
import json
import time
from pathlib import Path
from collections import defaultdict
from PIL import Image
import torch
from ultralytics import YOLO

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
BASE_RETRAIN_DIR = WORKSPACE_ROOT / "backend" / "ml_assets" / "updated retrain"
CROPS_S_DIR = BASE_RETRAIN_DIR / "crops_classifier" / "s"
CROPS_M_DIR = BASE_RETRAIN_DIR / "crops_classifier" / "m"
NOTEBOOK_PATH = BASE_RETRAIN_DIR / "yolo26-cls-fine-tuning-on-a-cleaned-10-class-crop.ipynb"
FULL_LIBRARY_DIR = WORKSPACE_ROOT / "backend" / "ml_assets" / "vision" / "test_images" / "full_library"
RESULTS_DIR = WORKSPACE_ROOT / "experiments" / "results" / "E02_vision_gate_calibration"

def parse_notebook():
    print("=" * 80)
    print("1. PARSING NOTEBOOK CONTENT & TRAINING METRICS")
    print("=" * 80)
    if not NOTEBOOK_PATH.exists():
        print(f"Notebook not found at: {NOTEBOOK_PATH}")
        return

    with open(NOTEBOOK_PATH, encoding="utf-8") as f:
        nb = json.load(f)

    print(f"Notebook loaded: {NOTEBOOK_PATH.name} ({len(nb.get('cells', []))} cells)")

    # Search for markdown tables, text summaries, and code outputs
    for i, cell in enumerate(nb.get("cells", [])):
        cell_type = cell.get("cell_type")
        source = "".join(cell.get("source", []))
        
        # Look for accuracy tables or key summaries
        if "accuracy" in source.lower() or "class" in source.lower() or "confusion" in source.lower() or "result" in source.lower():
            if cell_type == "markdown" and ("table" in source.lower() or "|" in source or "metrics" in source.lower()):
                print(f"\n--- [Cell {i} Markdown] ---")
                print(source[:1500])
            elif cell_type == "code":
                outputs = cell.get("outputs", [])
                for out in outputs:
                    if "text" in out:
                        text_out = "".join(out["text"])
                        if "accuracy" in text_out.lower() or "top1" in text_out.lower() or "precision" in text_out.lower() or "classes" in text_out.lower():
                            print(f"\n--- [Cell {i} Code Output] ---")
                            print(text_out[:1500])

def inspect_models():
    print("\n" + "=" * 80)
    print("2. WEIGHT INTEGRITY & ARCHITECTURE AUDIT: CROPS_CLASSIFIER/S")
    print("=" * 80)

    # Inspect results.csv in crops_classifier/s
    res_csv = CROPS_S_DIR / "results.csv"
    if res_csv.exists():
        with open(res_csv, encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        print(f"Training history in results.csv ({len(rows)} epochs recorded):")
        for r in [rows[0], rows[len(rows)//2], rows[-1]]:
            clean_r = {k.strip(): v.strip() for k, v in r.items()}
            print(f"  Epoch {clean_r.get('epoch')}: train_loss={clean_r.get('train/loss')}, val_loss={clean_r.get('val/loss')}, top1_acc={clean_r.get('metrics/accuracy_top1')}, top5_acc={clean_r.get('metrics/accuracy_top5')}")

    # Inspect best.pt (YOLO26s)
    pt_path = CROPS_S_DIR / "best.pt"
    if pt_path.exists():
        try:
            m_s = YOLO(str(pt_path))
            print(f"\nPyTorch Checkpoint: PASSED ({pt_path.stat().st_size / (1024*1024):.2f} MB)")
            print(f"  Task: {m_s.task}")
            print(f"  Classes ({len(m_s.names)}):")
            for idx, name in sorted(m_s.names.items()):
                print(f"    [{idx}] {name}")
        except Exception as e:
            print(f"PyTorch Load Failed: {e}")

    # Inspect best.onnx
    onnx_path = CROPS_S_DIR / "best.onnx"
    print(f"\nONNX Export: {onnx_path.name} (exists={onnx_path.exists()}, size={onnx_path.stat().st_size / (1024*1024):.2f} MB)")

    # Inspect best.tflite
    tflite_path = CROPS_S_DIR / "best.tflite"
    print(f"TFLite Export: {tflite_path.name} (exists={tflite_path.exists()}, size={tflite_path.stat().st_size / (1024*1024):.2f} MB)")

    # Inspect Medium Model (crops_classifier/m)
    m_pt_path = CROPS_M_DIR / "best.pt"
    if m_pt_path.exists():
        try:
            m_m = YOLO(str(m_pt_path))
            print(f"\nMedium Model (crops_classifier/m): PASSED ({m_pt_path.stat().st_size / (1024*1024):.2f} MB)")
            print(f"  Task: {m_m.task}")
            print(f"  Classes ({len(m_m.names)}): {m_m.names}")
        except Exception as e:
            print(f"Medium Model Load Failed: {e}")

def run_empirical_eval():
    print("\n" + "=" * 80)
    print("3. EMPIRICAL BENCHMARK ON 436 REAL TEST IMAGES")
    print("=" * 80)

    pt_path = CROPS_S_DIR / "best.pt"
    m = YOLO(str(pt_path))

    image_files = sorted(FULL_LIBRARY_DIR.glob("*/*.[jJ][pP][gG]")) + sorted(FULL_LIBRARY_DIR.glob("*/*.[pP][nN][gG]"))
    print(f"Evaluating {len(image_files)} real images from {FULL_LIBRARY_DIR.name}...")

    # Mapping from folder prefix to expected 10-crop class
    # Model classes: Cabbage, Cauliflower, Chili, Corn, Eggplant, Gourd, Guava, Potato, Rice, Tomato (or similar)
    model_classes_lower = {v.lower().replace(" ", ""): v for v in m.names.values()}
    print(f"Model Class Vocabulary: {list(m.names.values())}")

    records = []
    t0 = time.time()
    for img_path in image_files:
        folder_name = img_path.parent.name
        img_name = img_path.name
        image_id = f"{folder_name}/{img_name}"
        true_crop = folder_name.split("__")[0].strip()

        with Image.open(img_path) as img:
            img_rgb = img.convert("RGB")
            res = m(img_rgb, verbose=False)[0]
            probs = res.probs.data.detach().cpu().numpy()
            top1_idx = int(probs.argmax())
            top1_conf = float(probs[top1_idx])
            sorted_indices = probs.argsort()[::-1]
            p2_conf = float(probs[sorted_indices[1]]) if len(sorted_indices) > 1 else 0.0
            margin = round(top1_conf - p2_conf, 4)
            pred_class = m.names[top1_idx]

            # Check correctness
            # Direct match
            is_correct = (true_crop.lower() == pred_class.lower())

            records.append({
                "image_id": image_id,
                "folder": folder_name,
                "true_crop": true_crop,
                "pred_crop": pred_class,
                "is_correct": is_correct,
                "top1_conf": round(top1_conf, 4),
                "top2_conf": round(p2_conf, 4),
                "margin": margin,
            })

    elapsed = time.time() - t0
    N = len(records)
    acc = sum(1 for r in records if r["is_correct"]) / N * 100
    avg_conf = sum(r["top1_conf"] for r in records) / N
    avg_margin = sum(r["margin"] for r in records) / N

    print(f"\nInference finished in {elapsed:.2f}s ({elapsed/N*1000:.2f} ms/image).")
    print("\n" + "=" * 80)
    print("10-CLASS CROPS_CLASSIFIER/S TEST BENCHMARK RESULTS")
    print("=" * 80)
    print(f"Total Evaluated Test Images:      {N}")
    print(f"1. Overall Crop Accuracy:         {sum(1 for r in records if r['is_correct'])}/{N} ({acc:.2f}%)")
    print(f"2. Mean Top-1 Softmax Confidence: {avg_conf:.4f}")
    print(f"3. Mean Top1-Top2 Margin:         {avg_margin:.4f}")

    # Per-Crop Breakdown
    crop_stats = defaultdict(lambda: {"total": 0, "correct": 0, "errors": defaultdict(int)})
    for r in records:
        c = r["true_crop"]
        crop_stats[c]["total"] += 1
        if r["is_correct"]:
            crop_stats[c]["correct"] += 1
        else:
            crop_stats[c]["errors"][r["pred_crop"]] += 1

    print("\n--- Per-Crop Breakdown ---")
    print(f"{'Crop':15s} | {'Total':5s} | {'Correct':8s} | {'Accuracy':10s} | {'Confusion / Errors'}")
    print("-" * 80)
    for c, s in sorted(crop_stats.items()):
        tot = s["total"]
        cor = s["correct"]
        c_acc = (cor / tot) * 100
        err_str = ", ".join(f"{k}:{v}" for k, v in s["errors"].items()) if s["errors"] else "None (100% Perfect)"
        print(f"{c:15s} | {tot:5d} | {cor:8d} | {c_acc:8.2f}% | {err_str}")

    # Save CSV
    out_csv = RESULTS_DIR / "crops_classifier_s_436_eval.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        writer.writeheader()
        for r in records:
            writer.writerow(r)
    print(f"\nSaved evaluation log to: {out_csv}")

if __name__ == "__main__":
    parse_notebook()
    inspect_models()
    run_empirical_eval()
