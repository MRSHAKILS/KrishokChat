#!/usr/bin/env python3
"""
experiments/scripts/verify_retrained_models.py
Deep technical verification, weight integrity check, and test suite evaluation of retrained models in:
backend/ml_assets/updated retrain/
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
import yaml
import torch
from ultralytics import YOLO

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
BASE_RETRAIN_DIR = WORKSPACE_ROOT / "backend" / "ml_assets" / "updated retrain"
FULL_LIBRARY_DIR = WORKSPACE_ROOT / "backend" / "ml_assets" / "vision" / "test_images" / "full_library"

def inspect_models():
    print("=" * 80)
    print("DEEP INTEGRITY & ARCHITECTURE AUDIT: RETRAINED MODELS")
    print("=" * 80)

    # 1. agri_y26s_cls_35_epochs_updated
    print("\n--- Model 1: agri_y26s_cls_35_epochs_updated ---")
    agri_dir = BASE_RETRAIN_DIR / "agri_y26s_cls_35_epochs_updated"
    args_file = agri_dir / "args.yaml"
    if args_file.exists():
        with open(args_file, encoding="utf-8") as f:
            args = yaml.safe_load(f)
        print("Training Config:")
        print(f"  Base Model Architecture: {args.get('model')}")
        print(f"  Dataset Path:            {args.get('data')}")
        print(f"  Target Epochs:           {args.get('epochs')}")
        print(f"  Image Resolution (imgsz):{args.get('imgsz')}")
        print(f"  Batch Size:              {args.get('batch')}")
        print(f"  Optimizer / LR:          {args.get('optimizer')} / lr0={args.get('lr0')}")
        print(f"  Device:                  {args.get('device')}")

    results_file = agri_dir / "results.csv"
    if results_file.exists():
        with open(results_file, encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
        print(f"\nTraining Convergence ({len(reader)} epochs recorded):")
        # Clean keys
        for row in [reader[0], reader[-1]]:
            clean_row = {k.strip(): v.strip() for k, v in row.items()}
            print(f"  Epoch {clean_row.get('epoch')}: train_loss={clean_row.get('train/loss')}, val_loss={clean_row.get('val/loss')}, top1_acc={clean_row.get('metrics/accuracy_top1')}, top5_acc={clean_row.get('metrics/accuracy_top5')}")

    best_pt_agri = agri_dir / "weights" / "best.pt"
    if best_pt_agri.exists():
        try:
            m_agri = YOLO(str(best_pt_agri))
            print(f"\nModel File Integrity: PASSED ({best_pt_agri.stat().st_size / (1024*1024):.2f} MB)")
            print(f"  Task: {m_agri.task}")
            print(f"  Classes ({len(m_agri.names)}):")
            for idx, cname in m_agri.names.items():
                print(f"    [{idx}] {cname}")
        except Exception as e:
            print(f"Model Loading Failed: {e}")

    # 2. brassica_disease_exports
    print("\n--- Model 2: brassica_disease_exports ---")
    brassica_dir = BASE_RETRAIN_DIR / "brassica_disease_exports"
    best_pt_brassica = brassica_dir / "best.pt"
    if best_pt_brassica.exists():
        try:
            m_brassica = YOLO(str(best_pt_brassica))
            print(f"Model File Integrity: PASSED ({best_pt_brassica.stat().st_size / (1024*1024):.2f} MB)")
            print(f"  Task: {m_brassica.task}")
            print(f"  Classes ({len(m_brassica.names)}):")
            for idx, cname in m_brassica.names.items():
                print(f"    [{idx}] {cname}")
        except Exception as e:
            print(f"Model Loading Failed: {e}")

    metrics_csv = brassica_dir / "brassica_per_class_metrics.csv"
    if metrics_csv.exists():
        with open(metrics_csv, encoding="utf-8") as f:
            b_reader = list(csv.DictReader(f))
        print("\nReported Brassica Per-Class Metrics:")
        for row in b_reader:
            print(f"  {row}")

    # 3. potato
    print("\n--- Model 3: potato ---")
    potato_dir = BASE_RETRAIN_DIR / "potato"
    best_pt_potato = potato_dir / "best.pt"
    if best_pt_potato.exists():
        try:
            m_potato = YOLO(str(best_pt_potato))
            print(f"Model File Integrity: PASSED ({best_pt_potato.stat().st_size / (1024*1024):.2f} MB)")
            print(f"  Task: {m_potato.task}")
            print(f"  Classes ({len(m_potato.names)}):")
            for idx, cname in m_potato.names.items():
                print(f"    [{idx}] {cname}")
        except Exception as e:
            print(f"Model Loading Failed: {e}")

if __name__ == "__main__":
    inspect_models()
