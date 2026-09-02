#!/usr/bin/env python3
"""
experiments/scripts/eval_retrained_models_on_test_library.py
Empirical Evaluation of the Retrained Models on the Full 436-Image Test Library.

Evaluates:
1. Unified 45-Class Agri-YOLO26s Model (agri_y26s_cls_35_epochs_updated/weights/best.pt)
2. Retrained Brassica Model (brassica_disease_exports/best.pt)
3. Retrained Potato Model (potato/best.pt)
"""

from __future__ import annotations

import csv
import json
import time
from collections import defaultdict
from pathlib import Path
from PIL import Image
from ultralytics import YOLO

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
BASE_RETRAIN_DIR = WORKSPACE_ROOT / "backend" / "ml_assets" / "updated retrain"
FULL_LIBRARY_DIR = WORKSPACE_ROOT / "backend" / "ml_assets" / "vision" / "test_images" / "full_library"
RESULTS_DIR = WORKSPACE_ROOT / "experiments" / "results" / "E02_vision_gate_calibration"

def run_evaluation():
    print("=" * 80)
    print("EMPIRICAL BENCHMARK: RETRAINED MODELS ON FULL TEST LIBRARY (436 IMAGES)")
    print("=" * 80)

    # Load 45-class unified model
    unified_pt = BASE_RETRAIN_DIR / "agri_y26s_cls_35_epochs_updated" / "weights" / "best.pt"
    print(f"Loading Unified 45-Class Model: {unified_pt}")
    m_unified = YOLO(str(unified_pt))

    # Load brassica & potato models
    brassica_pt = BASE_RETRAIN_DIR / "brassica_disease_exports" / "best.pt"
    m_brassica = YOLO(str(brassica_pt))
    potato_pt = BASE_RETRAIN_DIR / "potato" / "best.pt"
    m_potato = YOLO(str(potato_pt))

    image_files = sorted(FULL_LIBRARY_DIR.glob("*/*.[jJ][pP][gG]")) + sorted(FULL_LIBRARY_DIR.glob("*/*.[pP][nN][gG]"))
    print(f"Found {len(image_files)} test images across 45 classes in full library.")

    unified_records = []
    brassica_records = []
    potato_records = []

    t0 = time.time()
    for img_path in image_files:
        folder_name = img_path.parent.name
        img_name = img_path.name
        image_id = f"{folder_name}/{img_name}"

        with Image.open(img_path) as img:
            img_rgb = img.convert("RGB")

            # 1. Unified 45-Class Model Inference
            res_u = m_unified(img_rgb, verbose=False)[0]
            probs_u = res_u.probs.data.detach().cpu().numpy()
            top1_idx = int(probs_u.argmax())
            top1_conf = float(probs_u[top1_idx])
            sorted_indices = probs_u.argsort()[::-1]
            p2_conf = float(probs_u[sorted_indices[1]]) if len(sorted_indices) > 1 else 0.0
            margin_u = round(top1_conf - p2_conf, 4)
            pred_u = m_unified.names[top1_idx]

            # Check exact match with folder
            is_correct_u = (pred_u.lower().replace(" ", "") == folder_name.lower().replace(" ", ""))
            
            # Crop match (e.g. Tomato, Potato, Rice, Cabbage, Cauliflower, Chili, Eggplant, Gourd, Guava)
            true_crop = folder_name.split("__")[0]
            pred_crop = pred_u.split("__")[0]
            crop_correct_u = (true_crop.lower() == pred_crop.lower())

            unified_records.append({
                "image_id": image_id,
                "folder": folder_name,
                "true_crop": true_crop,
                "pred_crop": pred_crop,
                "crop_correct": crop_correct_u,
                "true_class": folder_name,
                "pred_class": pred_u,
                "exact_correct": is_correct_u,
                "top1_conf": round(top1_conf, 4),
                "top2_conf": round(p2_conf, 4),
                "margin": margin_u,
            })

            # 2. Specialized Brassica evaluation
            if true_crop.lower() in ("cabbage", "cauliflower"):
                res_b = m_brassica(img_rgb, verbose=False)[0]
                probs_b = res_b.probs.data.detach().cpu().numpy()
                b_idx = int(probs_b.argmax())
                b_conf = float(probs_b[b_idx])
                b_pred = m_brassica.names[b_idx]
                b_correct = (b_pred.lower().replace(" ", "") == folder_name.lower().replace(" ", ""))
                brassica_records.append({
                    "image_id": image_id,
                    "true_class": folder_name,
                    "pred_class": b_pred,
                    "correct": b_correct,
                    "conf": round(b_conf, 4),
                })

            # 3. Specialized Potato evaluation
            if true_crop.lower() == "potato":
                res_p = m_potato(img_rgb, verbose=False)[0]
                probs_p = res_p.probs.data.detach().cpu().numpy()
                p_idx = int(probs_p.argmax())
                p_conf = float(probs_p[p_idx])
                p_pred = m_potato.names[p_idx]
                p_correct = (p_pred.lower().replace(" ", "") == folder_name.lower().replace(" ", ""))
                potato_records.append({
                    "image_id": image_id,
                    "true_class": folder_name,
                    "pred_class": p_pred,
                    "correct": p_correct,
                    "conf": round(p_conf, 4),
                })

    elapsed = time.time() - t0
    print(f"\nInference completed in {elapsed:.2f}s ({elapsed/len(image_files)*1000:.2f} ms/image).")

    # Metrics for Unified Model
    N = len(unified_records)
    crop_acc = sum(1 for r in unified_records if r["crop_correct"]) / N * 100
    exact_acc = sum(1 for r in unified_records if r["exact_correct"]) / N * 100
    avg_conf = sum(r["top1_conf"] for r in unified_records) / N
    avg_margin = sum(r["margin"] for r in unified_records) / N

    print("\n" + "=" * 80)
    print("UNIFIED 45-CLASS RETRAINED MODEL BENCHMARK RESULTS")
    print("=" * 80)
    print(f"Total Evaluated Test Images:      {N}")
    print(f"1. Crop Identification Accuracy:  {sum(1 for r in unified_records if r['crop_correct'])}/{N} ({crop_acc:.2f}%)")
    print(f"2. Exact Disease Class Accuracy:  {sum(1 for r in unified_records if r['exact_correct'])}/{N} ({exact_acc:.2f}%)")
    print(f"3. Mean Top-1 Confidence:         {avg_conf:.4f}")
    print(f"4. Mean Top1-Top2 Margin:         {avg_margin:.4f}")

    # Crop breakdown for unified model
    crop_stats = defaultdict(lambda: {"total": 0, "crop_correct": 0, "exact_correct": 0})
    for r in unified_records:
        c = r["true_crop"]
        crop_stats[c]["total"] += 1
        if r["crop_correct"]:
            crop_stats[c]["crop_correct"] += 1
        if r["exact_correct"]:
            crop_stats[c]["exact_correct"] += 1

    print("\n--- Per-Crop Breakdown (Unified 45-Class Model) ---")
    print(f"{'Crop':15s} | {'Total':5s} | {'Crop Acc':10s} | {'Exact Disease Acc':18s}")
    print("-" * 60)
    for c, stat in sorted(crop_stats.items()):
        tot = stat["total"]
        c_acc = stat["crop_correct"] / tot * 100
        e_acc = stat["exact_correct"] / tot * 100
        print(f"{c:15s} | {tot:5d} | {c_acc:8.2f}% | {e_acc:15.2f}%")

    # Metrics for specialized models
    print("\n" + "=" * 80)
    print("SPECIALIZED RETRAINED MODELS RESULTS")
    print("=" * 80)
    if brassica_records:
        b_acc = sum(1 for r in brassica_records if r["correct"]) / len(brassica_records) * 100
        print(f"Brassica 11-Class Model: {sum(1 for r in brassica_records if r['correct'])}/{len(brassica_records)} ({b_acc:.2f}%)")
    if potato_records:
        p_acc = sum(1 for r in potato_records if r["correct"]) / len(potato_records) * 100
        print(f"Potato 3-Class Model:    {sum(1 for r in potato_records if r['correct'])}/{len(potato_records)} ({p_acc:.2f}%)")

    # Save results to CSV
    unified_csv = RESULTS_DIR / "retrained_unified_45_eval.csv"
    with open(unified_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(unified_records[0].keys()))
        writer.writeheader()
        for r in unified_records:
            writer.writerow(r)
    print(f"\nSaved detailed evaluation to: {unified_csv}")

if __name__ == "__main__":
    run_evaluation()
