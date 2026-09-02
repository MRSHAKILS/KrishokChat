#!/usr/bin/env python3
"""
experiments/scripts/deep_diagnosis_failure_cases.py
Forensic Diagnostic Analysis of:
1. All 31 Cabbage images (What succeeded, what failed, confidence, margin).
2. The exact 8 failure cases (Why they passed the gate, confidence vs margin).
3. Overall disease detection performance across all crops.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from PIL import Image
from ultralytics import YOLO

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = WORKSPACE_ROOT / "experiments" / "results" / "E02_vision_gate_calibration"
E2E_CSV = RESULTS_DIR / "e2e_safety_replay_results.csv"
FULL_LIBRARY_DIR = WORKSPACE_ROOT / "backend" / "ml_assets" / "vision" / "test_images" / "full_library"
BRASSICA_MODEL = WORKSPACE_ROOT / "backend" / "ml_assets" / "vision" / "brassica_disease" / "model.pt"
RICE_MODEL = WORKSPACE_ROOT / "backend" / "ml_assets" / "vision" / "rice_disease" / "model.pt"

def run_diagnostics():
    with open(E2E_CSV, encoding="utf-8") as f:
        e2e_rows = list(csv.DictReader(f))

    print("=" * 85)
    print("1. CABBAGE SPECIFIC AUDIT (Is every image of Cabbage failing?)")
    print("=" * 85)
    cabbage_rows = [r for r in e2e_rows if r["true_crop"].lower() == "cabbage"]
    print(f"Total Cabbage Images in Test Library: {len(cabbage_rows)}")

    outcomes = defaultdict(int)
    for r in cabbage_rows:
        outcomes[r["outcome"]] += 1

    for out, cnt in sorted(outcomes.items()):
        print(f"  Outcome {out:25s}: {cnt:2d}/{len(cabbage_rows)} ({cnt/len(cabbage_rows)*100:.1f}%)")

    print("\nDetailed Per-Image Cabbage Status:")
    print(f"{'Image ID':35s} | {'Crop Pred':11s} | {'CropConf':8s} | {'Disease Pred':30s} | {'DisConf':8s} | {'Outcome'}")
    print("-" * 115)
    for r in cabbage_rows:
        c_conf = float(r["crop_confidence"] or 0)
        d_conf = float(r["disease_confidence"] or 0)
        dis_p = r["predicted_disease"] or "None"
        print(f"{r['image_id']:35s} | {r['predicted_crop']:11s} | {c_conf:8.4f} | {dis_p:30s} | {d_conf:8.4f} | {r['outcome']}")

    print("\n" + "=" * 85)
    print("2. FORENSIC AUDIT OF THE EXACT 8 RESIDUAL FAILURES")
    print("=" * 85)
    unsafe_rows = [r for r in e2e_rows if r["outcome"] == "UNSAFE_AUTO_ADVISORY"]
    print(f"Total Residual Failure Cases: {len(unsafe_rows)} out of 436 ({len(unsafe_rows)/436*100:.2f}%)")

    # Inspect disease model outputs (raw probabilities and margins)
    m_brassica = YOLO(str(BRASSICA_MODEL))
    m_rice = YOLO(str(RICE_MODEL))

    for i, r in enumerate(unsafe_rows, 1):
        img_id = r["image_id"]
        folder = r["folder"]
        img_path = FULL_LIBRARY_DIR / img_id

        # Run inference to get raw top1, top2, margin
        with Image.open(img_path) as img:
            img_rgb = img.convert("RGB")
            if "cabbage" in folder.lower():
                res = m_brassica(img_rgb, verbose=False)[0]
                names = m_brassica.names
            else:
                res = m_rice(img_rgb, verbose=False)[0]
                names = m_rice.names

            probs = res.probs.data.detach().cpu().numpy()
            sorted_idx = probs.argsort()[::-1]
            p1_idx = sorted_idx[0]
            p2_idx = sorted_idx[1]
            p1_val = float(probs[p1_idx])
            p2_val = float(probs[p2_idx])
            margin = p1_val - p2_val
            p1_name = names[p1_idx]
            p2_name = names[p2_idx]

        print(f"\n--- Case #{i}: {img_id} ---")
        print(f"  True Pathology:     {folder}")
        print(f"  Top-1 Prediction:   {p1_name} (Prob = {p1_val:.4f})")
        print(f"  Top-2 Runner-Up:    {p2_name} (Prob = {p2_val:.4f})")
        print(f"  Top1-Top2 Margin:   {margin:.4f}")
        print(f"  Crop Conf:          {float(r['crop_confidence']):.4f}")
        print(f"  Emitted Chemical:   {r['prescription_chemical']}")

        # Diagnose why it passed the gate
        if "healthy" in p1_name.lower():
            reason = "HEALTHY FALSE POSITIVE: Small disease lesion masked by dominant healthy leaf area."
        elif margin < 0.20:
            reason = "NARROW MARGIN: Close competition between two sister disease classes."
        else:
            reason = "HIGH-CONFIDENCE INTRA-CROP MISIDENTIFICATION: Foliar spot pattern visually mimics sister disease."
        print(f"  Diagnostic Cause:   {reason}")

    print("\n" + "=" * 85)
    print("3. OVERALL CROP-BY-CROP DISEASE PIPELINE PERFORMANCE")
    print("=" * 85)
    stats = defaultdict(lambda: {"total": 0, "safe_auto": 0, "clarify": 0, "abstain": 0, "unsafe": 0, "second_img": 0})
    for r in e2e_rows:
        tc = r["true_crop"]
        stats[tc]["total"] += 1
        out = r["outcome"]
        if out == "SAFE_AUTOMATION":
            stats[tc]["safe_auto"] += 1
        elif out == "SAFE_CLARIFICATION":
            stats[tc]["clarify"] += 1
        elif out == "SAFE_ABSTAIN":
            stats[tc]["abstain"] += 1
        elif out == "UNSAFE_AUTO_ADVISORY":
            stats[tc]["unsafe"] += 1
        elif out == "SAFE_SECOND_IMAGE":
            stats[tc]["second_img"] += 1

    print(f"{'Crop':15s} | {'Total':5s} | {'Safe Auto':10s} | {'Clarify':8s} | {'Abstain':8s} | {'Unsafe':8s} | {'Accuracy Rate'}")
    print("-" * 80)
    for c, s in sorted(stats.items()):
        tot = s["total"]
        auto = s["safe_auto"]
        uns = s["unsafe"]
        acc = ((tot - uns) / tot) * 100
        print(f"{c:15s} | {tot:5d} | {auto:10d} | {s['clarify']:8d} | {s['abstain']:8d} | {uns:8d} | {acc:6.1f}% Safe")

if __name__ == "__main__":
    run_diagnostics()
