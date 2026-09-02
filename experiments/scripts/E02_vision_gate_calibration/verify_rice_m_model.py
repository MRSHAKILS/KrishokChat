#!/usr/bin/env python3
"""
experiments/scripts/verify_rice_m_model.py
Benchmark the newly retrained rice disease model (m/best.pt) vs the old model (model.pt)
across the 80 held-out field images and evaluate Tungro integration and calibrated thresholds.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from PIL import Image
from ultralytics import YOLO

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
OLD_MODEL = WORKSPACE_ROOT / "backend" / "ml_assets" / "vision" / "rice_disease" / "model.pt"
NEW_M_MODEL = WORKSPACE_ROOT / "backend" / "ml_assets" / "updated retrain" / "rice disease classfier" / "m" / "best.pt"
NEW_N_MODEL = WORKSPACE_ROOT / "backend" / "ml_assets" / "updated retrain" / "rice disease classfier" / "n" / "best.pt"
FULL_LIBRARY = WORKSPACE_ROOT / "backend" / "ml_assets" / "vision" / "test_images" / "full_library"

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    
    print("=" * 80)
    print("1. MODEL INSPECTION & ARCHITECTURE")
    print("=" * 80)
    old_m = YOLO(str(OLD_MODEL))
    new_m = YOLO(str(NEW_M_MODEL))
    new_n = YOLO(str(NEW_N_MODEL))
    
    print(f"Old Model ({OLD_MODEL.name}): {len(old_m.names)} classes")
    print("  Names:", old_m.names)
    print(f"\nNew M Model (YOLO26m-cls): {len(new_m.names)} classes")
    print("  Names:", new_m.names)
    print(f"\nNew N Model (YOLO26n-cls): {len(new_n.names)} classes")
    print("  Names:", new_n.names)
    
    print("\n" + "=" * 80)
    print("2. EVALUATION ON 80 REAL FIELD RICE TEST IMAGES")
    print("=" * 80)
    
    rice_folders = sorted([f for f in os.listdir(FULL_LIBRARY) if f.startswith("Rice__")])
    total = 0
    old_correct = 0
    new_m_correct = 0
    new_n_correct = 0
    
    results = []
    
    for folder in rice_folders:
        f_path = FULL_LIBRARY / folder
        for img_name in sorted(os.listdir(f_path)):
            if not img_name.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            total += 1
            img_path = f_path / img_name
            with Image.open(img_path) as im:
                rgb = im.convert("RGB")
                
                # Old
                r_old = old_m(rgb, verbose=False)[0]
                p_old = r_old.probs.data.cpu().numpy()
                pred_old = old_m.names[p_old.argmax()]
                conf_old = float(p_old.max())
                
                # New M
                r_m = new_m(rgb, verbose=False)[0]
                p_m = r_m.probs.data.cpu().numpy()
                pred_m = new_m.names[p_m.argmax()]
                conf_m = float(p_m.max())
                sort_m = p_m.argsort()[::-1]
                margin_m = float(p_m[sort_m[0]] - p_m[sort_m[1]])
                runner_m = new_m.names[sort_m[1]]
                runner_conf_m = float(p_m[sort_m[1]])
                
                # New N
                r_n = new_n(rgb, verbose=False)[0]
                p_n = r_n.probs.data.cpu().numpy()
                pred_n = new_n.names[p_n.argmax()]
                conf_n = float(p_n.max())
                sort_n = p_n.argsort()[::-1]
                margin_n = float(p_n[sort_n[0]] - p_n[sort_n[1]])
                
                ok_old = (pred_old.lower().replace(" ", "") == folder.lower().replace(" ", ""))
                ok_m = (pred_m.lower().replace(" ", "") == folder.lower().replace(" ", ""))
                ok_n = (pred_n.lower().replace(" ", "") == folder.lower().replace(" ", ""))
                
                if ok_old: old_correct += 1
                if ok_m: new_m_correct += 1
                if ok_n: new_n_correct += 1
                
                results.append({
                    "id": f"{folder}/{img_name}",
                    "true": folder,
                    "old_pred": pred_old,
                    "old_conf": conf_old,
                    "old_ok": ok_old,
                    "m_pred": pred_m,
                    "m_conf": conf_m,
                    "m_margin": margin_m,
                    "m_runner": runner_m,
                    "m_runner_conf": runner_conf_m,
                    "m_ok": ok_m,
                    "n_pred": pred_n,
                    "n_conf": conf_n,
                    "n_margin": margin_n,
                    "n_ok": ok_n,
                })
                
    print(f"Total Evaluated Rice Field Images: {total}")
    print(f"Old 8-Class Model Accuracy:        {old_correct}/{total} ({old_correct/total*100:.2f}%)")
    print(f"New 10-Class M Model Accuracy:     {new_m_correct}/{total} ({new_m_correct/total*100:.2f}%)")
    print(f"New 10-Class N Model Accuracy:     {new_n_correct}/{total} ({new_n_correct/total*100:.2f}%)")
    
    print("\n" + "=" * 80)
    print("3. DETAILED PER-DISEASE ACCURACY BREAKDOWN (M MODEL)")
    print("=" * 80)
    from collections import defaultdict
    per_disease = defaultdict(lambda: {"total": 0, "correct": 0, "wrong": []})
    for r in results:
        per_disease[r["true"]]["total"] += 1
        if r["m_ok"]:
            per_disease[r["true"]]["correct"] += 1
        else:
            per_disease[r["true"]]["wrong"].append(r)
            
    print(f"{'Pathology':32s} | {'Total':5s} | {'Correct':7s} | {'Accuracy':8s}")
    print("-" * 60)
    for dis, d in sorted(per_disease.items()):
        tot = d["total"]
        cor = d["correct"]
        acc = (cor / tot) * 100 if tot > 0 else 0
        print(f"{dis:32s} | {tot:5d} | {cor:7d} | {acc:6.1f}%")
        
    print("\n" + "=" * 80)
    print("4. FORENSIC AUDIT OF ALL M MODEL MISCLASSIFICATIONS")
    print("=" * 80)
    all_wrong_m = [r for r in results if not r["m_ok"]]
    print(f"Total Misclassifications in M model: {len(all_wrong_m)}")
    for i, w in enumerate(all_wrong_m, 1):
        print(f"\nError #{i}: {w['id']}")
        print(f"  True Pathology:   {w['true']}")
        print(f"  Predicted Disease: {w['m_pred']} (Confidence = {w['m_conf']:.4f})")
        print(f"  Runner-Up Disease: {w['m_runner']} (Confidence = {w['m_runner_conf']:.4f})")
        print(f"  Top1-Top2 Margin: {w['m_margin']:.4f}")
        # Check safety gate behavior:
        # Calibrated threshold for rice: conf >= 0.80, margin >= 0.15
        passes_gate = (w['m_conf'] >= 0.80 and w['m_margin'] >= 0.15)
        print(f"  Passes Gate (conf>=0.80, margin>=0.15)? {passes_gate}")
        if passes_gate:
            print("  -> Actionable Error if not caught by symptom/sourcing gate")
        else:
            print("  -> SAFELY INTERCEPTED by Gate! (Interactive chip or request clearer photo)")

if __name__ == "__main__":
    main()
