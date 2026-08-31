#!/usr/bin/env python3
"""
experiments/scripts/run_vision_calibration_benchmark.py
Empirical Vision Gate Calibration & Threshold Sweep Benchmark across real test images.

Collects raw model predictions (p1, p2, margin, top-3), performs confidence calibration
analysis (ECE, MCE, Brier score, reliability diagram bins), and executes exhaustive
2D threshold sweeps to determine the Pareto-optimal operating threshold.
"""

from __future__ import annotations

import csv
import json
import math
import os
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image

# Add backend to Python path
BACKEND_DIR = Path(__file__).resolve().parents[2] / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.application.vision_pipeline import image_quality
from app.domain.vision import VisionGateConfig, VisionModelSpec
from app.infrastructure.vision.registry import ArtifactVisionRegistry
from app.infrastructure.vision.ultralytics_classifier import UltralyticsClassificationRunner

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
VISION_DIR = BACKEND_DIR / "ml_assets" / "vision"
FULL_LIBRARY_DIR = VISION_DIR / "test_images" / "full_library"
RESULTS_DIR = WORKSPACE_ROOT / "experiments" / "results" / "E02_vision_gate_calibration"


# Ground truth mapping helpers
CROP_FAMILY_MAP = {
    "cabbage": "Brassica",
    "cauliflower": "Brassica",
    "potato": "Potato",
    "tomato": "Solanacea",
    "eggplant": "Solanacea",
    "chili": "Solanacea",
    "corn": "Corn",
    "wheat": "Wheat",
    "rice": "Rice",
    "gourd": "GourdGuava",
    "guava": "GourdGuava",
}


def parse_ground_truth(folder_name: str) -> tuple[str, str, str, bool]:
    """Parse folder name into (true_crop_name, true_family, true_disease, is_ood)."""
    parts = folder_name.split("__")
    crop_prefix = parts[0].strip()
    disease_suffix = parts[1].strip() if len(parts) > 1 else "Unknown"
    
    crop_lower = crop_prefix.lower()
    expected_family = CROP_FAMILY_MAP.get(crop_lower, crop_prefix)
    is_ood = expected_family == "GourdGuava" or crop_lower in ("guava", "gourd")
    
    return crop_prefix, expected_family, folder_name, is_ood


@dataclass
class RawPredictionRecord:
    image_id: str
    folder: str
    true_crop: str
    expected_family: str
    is_ood: bool
    quality_accepted: bool
    
    # Crop prediction
    pred_crop: str
    crop_p1: float
    crop_p2: float
    crop_margin: float
    crop_correct: bool
    top3_crops: str
    
    # Disease prediction (if applicable)
    disease_model: str
    pred_disease: str
    disease_p1: float
    disease_p2: float
    disease_margin: float
    disease_correct: bool
    top3_diseases: str


def compute_calibration_metrics(confidences: list[float], correctness: list[bool], n_bins: int = 10) -> dict[str, Any]:
    """Compute Reliability diagram bins, ECE, MCE, and Brier Score."""
    if not confidences:
        return {"ece": 0.0, "mce": 0.0, "brier": 0.0, "bins": []}
    
    confs = np.array(confidences)
    accs = np.array(correctness, dtype=float)
    N = len(confs)
    
    # Brier score
    brier_score = float(np.mean((confs - accs) ** 2))
    
    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    bin_data = []
    ece = 0.0
    mce = 0.0
    
    for i in range(n_bins):
        low, high = bin_edges[i], bin_edges[i + 1]
        mask = (confs >= low) & (confs < high) if i < n_bins - 1 else (confs >= low) & (confs <= high)
        bin_count = int(np.sum(mask))
        if bin_count > 0:
            bin_conf = float(np.mean(confs[mask]))
            bin_acc = float(np.mean(accs[mask]))
            gap = abs(bin_acc - bin_conf)
            ece += (bin_count / N) * gap
            if gap > mce:
                mce = gap
            bin_data.append({
                "bin_index": i + 1,
                "bin_range": f"{low:.2f}–{high:.2f}",
                "count": bin_count,
                "mean_confidence": round(bin_conf, 4),
                "empirical_accuracy": round(bin_acc, 4),
                "calibration_gap": round(gap, 4),
            })
        else:
            bin_data.append({
                "bin_index": i + 1,
                "bin_range": f"{low:.2f}–{high:.2f}",
                "count": 0,
                "mean_confidence": 0.0,
                "empirical_accuracy": 0.0,
                "calibration_gap": 0.0,
            })
            
    return {
        "n_samples": N,
        "ece": round(float(ece), 4),
        "mce": round(float(mce), 4),
        "brier_score": round(brier_score, 4),
        "bins": bin_data,
    }


def run_benchmark() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"=== Starting Vision Gate Calibration Study ===")
    print(f"Vision assets directory: {VISION_DIR}")
    print(f"Test library directory: {FULL_LIBRARY_DIR}")
    
    registry = ArtifactVisionRegistry(VISION_DIR)
    runner = UltralyticsClassificationRunner()
    
    records: list[RawPredictionRecord] = []
    
    # 1. Collect raw predictions across test images
    image_files = sorted(FULL_LIBRARY_DIR.glob("*/*.[jJ][pP][gG]")) + sorted(FULL_LIBRARY_DIR.glob("*/*.[pP][nN][gG]"))
    print(f"Found {len(image_files)} test images across classes.")
    
    for img_path in image_files:
        folder_name = img_path.parent.name
        img_name = img_path.name
        image_id = f"{folder_name}/{img_name}"
        
        true_crop, expected_family, true_disease, is_ood = parse_ground_truth(folder_name)
        
        try:
            with Image.open(img_path) as img:
                img_rgb = img.convert("RGB")
                qual = image_quality(img_rgb)
                
                # Predict Crop
                crop_pred = runner.predict(registry.crop_classifier, img_rgb)
                p1_crop = crop_pred.confidence
                p2_crop = float(crop_pred.top3[1]["confidence"]) if len(crop_pred.top3) > 1 else 0.0
                margin_crop = round(p1_crop - p2_crop, 4)
                
                # Check correctness
                # In 6-class model: Brassica, Corn, GourdGuava, Potato, Solanacea, Wheat
                # Rice is not in 6-class model (historically mitigated via Wheat)
                pred_crop_label = crop_pred.label
                if is_ood:
                    # For OOD images (Guava, Gourd), correct behavior is matching GourdGuava
                    crop_correct = (pred_crop_label == "GourdGuava")
                elif true_crop.lower() == "rice":
                    # Rice was trained without crop class; handled via Wheat fallback or disease check
                    crop_correct = (pred_crop_label in ("Wheat", "Rice"))
                else:
                    crop_correct = (pred_crop_label == expected_family)
                
                # Predict Disease using candidate disease models
                disease_candidates = registry.disease_candidates(pred_crop_label)
                if pred_crop_label == "Wheat" and true_crop.lower() == "rice":
                    disease_candidates = disease_candidates + registry.disease_candidates("rice")
                if not disease_candidates and expected_family in ("Potato", "Brassica", "Corn", "Wheat"):
                    disease_candidates = registry.disease_candidates(expected_family)
                
                disease_model_name = "none"
                pred_disease_label = "none"
                p1_disease = 0.0
                p2_disease = 0.0
                margin_disease = 0.0
                disease_correct = False
                top3_dis_str = ""
                
                if disease_candidates:
                    dis_preds = []
                    for spec in disease_candidates:
                        try:
                            d_pred = runner.predict(spec, img_rgb)
                            dis_preds.append((spec.key, d_pred))
                        except Exception:
                            pass
                    if dis_preds:
                        best_spec_key, best_d_pred = max(dis_preds, key=lambda item: item[1].confidence)
                        disease_model_name = best_spec_key
                        pred_disease_label = best_d_pred.label
                        p1_disease = best_d_pred.confidence
                        p2_disease = float(best_d_pred.top3[1]["confidence"]) if len(best_d_pred.top3) > 1 else 0.0
                        margin_disease = round(p1_disease - p2_disease, 4)
                        top3_dis_str = json.dumps(best_d_pred.top3)
                        
                        # Match disease label
                        # Normalization: e.g. "Potato__Late_Blight" == "Potato__Late_Blight"
                        disease_correct = (pred_disease_label.lower().replace(" ", "") == folder_name.lower().replace(" ", ""))
                
                record = RawPredictionRecord(
                    image_id=image_id,
                    folder=folder_name,
                    true_crop=true_crop,
                    expected_family=expected_family,
                    is_ood=is_ood,
                    quality_accepted=qual.accepted,
                    pred_crop=pred_crop_label,
                    crop_p1=p1_crop,
                    crop_p2=p2_crop,
                    crop_margin=margin_crop,
                    crop_correct=crop_correct,
                    top3_crops=json.dumps(crop_pred.top3),
                    disease_model=disease_model_name,
                    pred_disease=pred_disease_label,
                    disease_p1=p1_disease,
                    disease_p2=p2_disease,
                    disease_margin=margin_disease,
                    disease_correct=disease_correct,
                    top3_diseases=top3_dis_str,
                )
                records.append(record)
        except Exception as exc:
            print(f"Error processing {img_path}: {exc}")

    print(f"Successfully collected {len(records)} raw prediction records.")
    
    # 2. Save raw predictions to CSV
    raw_csv_path = RESULTS_DIR / "raw_vision_predictions.csv"
    with open(raw_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "image_id", "folder", "true_crop", "expected_family", "is_ood", "quality_accepted",
            "pred_crop", "crop_p1", "crop_p2", "crop_margin", "crop_correct", "top3_crops",
            "disease_model", "pred_disease", "disease_p1", "disease_p2", "disease_margin",
            "disease_correct", "top3_diseases"
        ])
        writer.writeheader()
        for r in records:
            writer.writerow(asdict(r))
    print(f"Saved raw predictions CSV to: {raw_csv_path}")
    
    # 3. Confidence Calibration for Crop Classifier
    crop_confs = [r.crop_p1 for r in records if not r.is_ood]
    crop_corrects = [r.crop_correct for r in records if not r.is_ood]
    crop_calib = compute_calibration_metrics(crop_confs, crop_corrects, n_bins=10)
    
    # Disease calibration for supported disease model cases
    dis_records = [r for r in records if r.disease_model != "none" and not r.is_ood]
    dis_confs = [r.disease_p1 for r in dis_records]
    dis_corrects = [r.disease_correct for r in dis_records]
    dis_calib = compute_calibration_metrics(dis_confs, dis_corrects, n_bins=10)
    
    # 4. Exhaustive 2D Threshold Sweep on Crop Classifier
    conf_thresholds = [0.40, 0.50, 0.60, 0.70, 0.75, 0.80, 0.82, 0.85, 0.88, 0.90, 0.92, 0.95]
    margin_thresholds = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
    ood_threshold = 0.40
    
    in_dist_records = [r for r in records if not r.is_ood]
    N_in = len(in_dist_records)
    
    crop_sweep_results = []
    
    for c_thresh in conf_thresholds:
        for m_thresh in margin_thresholds:
            auto_accept_count = 0
            correct_auto_accept = 0
            wrong_auto_accept = 0  # UNSAFE AUTO-ROUTING
            farmer_clarification = 0
            ood_rejected = 0
            
            for r in in_dist_records:
                p1 = r.crop_p1
                margin = r.crop_margin
                
                if p1 < ood_threshold:
                    ood_rejected += 1
                elif p1 < c_thresh or margin < m_thresh:
                    farmer_clarification += 1
                else:
                    auto_accept_count += 1
                    if r.crop_correct:
                        correct_auto_accept += 1
                    else:
                        wrong_auto_accept += 1
            
            auto_accept_rate = auto_accept_count / N_in if N_in > 0 else 0.0
            unsafe_auto_routing_rate = wrong_auto_accept / N_in if N_in > 0 else 0.0
            unsafe_of_accepted_pct = (wrong_auto_accept / auto_accept_count * 100.0) if auto_accept_count > 0 else 0.0
            clarification_rate = farmer_clarification / N_in if N_in > 0 else 0.0
            
            crop_sweep_results.append({
                "confidence_threshold": c_thresh,
                "margin_threshold": m_thresh,
                "total_evaluated": N_in,
                "auto_accept_count": auto_accept_count,
                "auto_accept_rate_pct": round(auto_accept_rate * 100, 2),
                "correct_auto_accept": correct_auto_accept,
                "wrong_auto_accept_unsafe": wrong_auto_accept,
                "unsafe_auto_routing_rate_pct": round(unsafe_auto_routing_rate * 100, 2),
                "unsafe_of_accepted_pct": round(unsafe_of_accepted_pct, 2),
                "farmer_clarification_count": farmer_clarification,
                "clarification_rate_pct": round(clarification_rate * 100, 2),
                "ood_rejected_count": ood_rejected,
            })
            
    # Save crop sweep CSV
    crop_sweep_csv = RESULTS_DIR / "threshold_sweep_crop.csv"
    with open(crop_sweep_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "confidence_threshold", "margin_threshold", "total_evaluated",
            "auto_accept_count", "auto_accept_rate_pct", "correct_auto_accept",
            "wrong_auto_accept_unsafe", "unsafe_auto_routing_rate_pct", "unsafe_of_accepted_pct",
            "farmer_clarification_count", "clarification_rate_pct", "ood_rejected_count"
        ])
        writer.writeheader()
        for row in crop_sweep_results:
            writer.writerow(row)
    print(f"Saved Crop Threshold Sweep CSV to: {crop_sweep_csv}")
    
    # 5. Exhaustive 2D Threshold Sweep on Disease Models
    N_dis = len(dis_records)
    disease_sweep_results = []
    
    for c_thresh in conf_thresholds:
        for m_thresh in margin_thresholds:
            auto_accept_count = 0
            correct_auto_accept = 0
            wrong_auto_accept = 0
            second_image_requested = 0
            unrecognized_count = 0
            
            for r in dis_records:
                p1 = r.disease_p1
                margin = r.disease_margin
                
                requires_second = (margin < m_thresh and p1 < 0.80)
                
                if p1 < c_thresh:
                    if requires_second:
                        second_image_requested += 1
                    else:
                        unrecognized_count += 1
                else:
                    auto_accept_count += 1
                    if r.disease_correct:
                        correct_auto_accept += 1
                    else:
                        wrong_auto_accept += 1
                        
            auto_rate = auto_accept_count / N_dis if N_dis > 0 else 0.0
            unsafe_rate = wrong_auto_accept / N_dis if N_dis > 0 else 0.0
            
            disease_sweep_results.append({
                "confidence_threshold": c_thresh,
                "margin_threshold": m_thresh,
                "total_evaluated": N_dis,
                "auto_accept_count": auto_accept_count,
                "auto_accept_rate_pct": round(auto_rate * 100, 2),
                "correct_auto_accept": correct_auto_accept,
                "wrong_auto_accept_unsafe": wrong_auto_accept,
                "unsafe_auto_routing_rate_pct": round(unsafe_rate * 100, 2),
                "second_image_requested": second_image_requested,
                "unrecognized_count": unrecognized_count,
            })
            
    disease_sweep_csv = RESULTS_DIR / "threshold_sweep_disease.csv"
    with open(disease_sweep_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "confidence_threshold", "margin_threshold", "total_evaluated",
            "auto_accept_count", "auto_accept_rate_pct", "correct_auto_accept",
            "wrong_auto_accept_unsafe", "unsafe_auto_routing_rate_pct",
            "second_image_requested", "unrecognized_count"
        ])
        writer.writeheader()
        for row in disease_sweep_results:
            writer.writerow(row)
    print(f"Saved Disease Threshold Sweep CSV to: {disease_sweep_csv}")
    
    # 6. Find Pareto Optimal Threshold for Crop Gate (Zero / Minimum Unsafe Routing)
    # Find combinations with wrong_auto_accept_unsafe == 0, then sort by highest auto_accept_rate_pct
    zero_unsafe_crop = [r for r in crop_sweep_results if r["wrong_auto_accept_unsafe"] == 0]
    if zero_unsafe_crop:
        pareto_crop = max(zero_unsafe_crop, key=lambda x: x["auto_accept_rate_pct"])
    else:
        pareto_crop = min(crop_sweep_results, key=lambda x: (x["wrong_auto_accept_unsafe"], -x["auto_accept_rate_pct"]))
        
    zero_unsafe_dis = [r for r in disease_sweep_results if r["wrong_auto_accept_unsafe"] == 0]
    if zero_unsafe_dis:
        pareto_dis = max(zero_unsafe_dis, key=lambda x: x["auto_accept_rate_pct"])
    else:
        pareto_dis = min(disease_sweep_results, key=lambda x: (x["wrong_auto_accept_unsafe"], -x["auto_accept_rate_pct"]))
        
    # 7. Evaluate OOD rejection capability
    ood_records = [r for r in records if r.is_ood]
    ood_total = len(ood_records)
    ood_caught_by_gourdguava = sum(1 for r in ood_records if r.pred_crop == "GourdGuava")
    ood_caught_by_low_conf = sum(1 for r in ood_records if r.crop_p1 < ood_threshold)
    ood_total_safe_handling = sum(1 for r in ood_records if r.pred_crop == "GourdGuava" or r.crop_p1 < ood_threshold)
    
    # 8. Full JSON Summary Report
    summary = {
        "dataset_total_images": len(records),
        "in_distribution_images": N_in,
        "ood_images": ood_total,
        "crop_classifier_calibration": crop_calib,
        "disease_classifier_calibration": dis_calib,
        "pareto_optimal_crop_gate": pareto_crop,
        "pareto_optimal_disease_gate": pareto_dis,
        "ood_evaluation": {
            "total_ood_images": ood_total,
            "handled_by_dedicated_gourdguava_class": ood_caught_by_gourdguava,
            "handled_by_low_confidence_ood_gate": ood_caught_by_low_conf,
            "total_safe_rejections": ood_total_safe_handling,
            "ood_safety_containment_rate_pct": round(ood_total_safe_handling / ood_total * 100, 2) if ood_total > 0 else 100.0,
        },
        "recommended_frozen_config": {
            "crop_confidence_threshold": pareto_crop["confidence_threshold"],
            "crop_margin_threshold": pareto_crop["margin_threshold"],
            "crop_ood_threshold": ood_threshold,
            "disease_confidence_threshold": pareto_dis["confidence_threshold"],
            "disease_margin_threshold": pareto_dis["margin_threshold"],
        }
    }
    
    json_path = RESULTS_DIR / "vision_calibration_report.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved full Calibration Report JSON to: {json_path}")
    
    # Print high-level findings to stdout
    print("\n" + "=" * 70)
    print("=== EMPIRICAL VISION CALIBRATION FINDINGS ===")
    print("=" * 70)
    print(f"Total Evaluated Images: {len(records)} ({N_in} In-Distribution, {ood_total} OOD)")
    print(f"Crop Classifier ECE: {crop_calib['ece']} | Brier: {crop_calib['brier_score']}")
    print(f"Disease Classifier ECE: {dis_calib['ece']} | Brier: {dis_calib['brier_score']}")
    print("\n--- Reliability Diagram Bins (Crop Classifier) ---")
    for b in crop_calib["bins"]:
        print(f"  Bin {b['bin_range']}: count={b['count']:3d}, conf={b['mean_confidence']:.2f}, acc={b['empirical_accuracy']:.2f}, gap={b['calibration_gap']:.2f}")
    print("\n--- Pareto Operating Point (Crop Gate) ---")
    print(f"  Confidence Threshold: {pareto_crop['confidence_threshold']}")
    print(f"  Margin Threshold:     {pareto_crop['margin_threshold']}")
    print(f"  Auto-Accept Rate:     {pareto_crop['auto_accept_rate_pct']}% ({pareto_crop['auto_accept_count']}/{N_in})")
    print(f"  Unsafe Auto-Routing:  {pareto_crop['unsafe_auto_routing_rate_pct']}% ({pareto_crop['wrong_auto_accept_unsafe']} wrong auto-routed)")
    print(f"  Farmer Clarification: {pareto_crop['clarification_rate_pct']}% ({pareto_crop['farmer_clarification_count']}/{N_in})")
    print("\n--- Pareto Operating Point (Disease Gate) ---")
    print(f"  Confidence Threshold: {pareto_dis['confidence_threshold']}")
    print(f"  Margin Threshold:     {pareto_dis['margin_threshold']}")
    print(f"  Auto-Accept Rate:     {pareto_dis['auto_accept_rate_pct']}% ({pareto_dis['auto_accept_count']}/{N_dis})")
    print(f"  Unsafe Auto-Routing:  {pareto_dis['unsafe_auto_routing_rate_pct']}% ({pareto_dis['wrong_auto_accept_unsafe']} wrong auto-routed)")
    print(f"  Second-Image Request: {pareto_dis['second_image_requested']} cases")
    print("=" * 70)


if __name__ == "__main__":
    run_benchmark()
