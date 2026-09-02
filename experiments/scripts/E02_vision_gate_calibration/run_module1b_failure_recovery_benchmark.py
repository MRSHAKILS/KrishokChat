#!/usr/bin/env python3
"""
experiments/scripts/run_module1b_failure_recovery_benchmark.py
Module 1B Benchmark: Perception Failure Recovery & Confusion-Pair Risk Gating.

Evaluates the multi-evidence decision model:
Prediction + Confidence + Top-2 Margin + Known Confusion Pairs + Second-Image Gate -> Safe Routing
"""

from __future__ import annotations

import asyncio
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from PIL import Image

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
BACKEND_DIR = WORKSPACE_ROOT / "backend"
import sys
sys.path.insert(0, str(BACKEND_DIR))

from app.domain.contracts import QAResult
from app.domain.enums import SafetyCategory, VerificationConfidence
from app.domain.fact_base import FactBase
from app.domain.vision import VisionGateConfig, VisionResult, VisionStatus
from app.infrastructure.audit.jsonl import JSONLAuditSink
from app.infrastructure.knowledge.fact_base_store import load_fact_base
from app.infrastructure.vision.registry import ArtifactVisionRegistry
from app.infrastructure.vision.ultralytics_classifier import UltralyticsClassificationRunner

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

# High-Risk Confusion Families / Pairs where visual overlap is acute
HIGH_RISK_CONFUSION_SETS = (
    {"potato", "solanacea", "tomato", "eggplant", "chili"},
    {"rice", "wheat", "corn"},
)


def parse_ground_truth(folder_name: str) -> tuple[str, str, str, bool]:
    parts = folder_name.split("__")
    crop_prefix = parts[0].strip()
    disease_suffix = parts[1].strip() if len(parts) > 1 else "Unknown"
    
    crop_lower = crop_prefix.lower()
    expected_family = CROP_FAMILY_MAP.get(crop_lower, crop_prefix)
    is_ood = expected_family == "GourdGuava" or crop_lower in ("guava", "gourd")
    
    return crop_prefix, expected_family, folder_name, is_ood


def is_high_risk_confusion_prediction(pred_crop: str, top2_crop: str | None = None) -> bool:
    """Check if prediction falls into an acute inter-species confusion pair."""
    p_lower = pred_crop.lower()
    t2_lower = top2_crop.lower() if top2_crop else ""
    
    # 1. Potato vs Solanacea nightshade family confusion
    if p_lower in ("potato", "solanacea"):
        return True
    
    # 2. Wheat / Corn / Rice Poaceae monocot confusion
    if p_lower in ("wheat", "corn") and (not t2_lower or t2_lower in ("wheat", "corn", "rice")):
        return True
        
    return False


@dataclass
class Module1BReplayResult:
    image_id: str
    folder: str
    true_crop: str
    expected_family: str
    is_ood: bool
    
    # Perception Details
    predicted_crop: str
    crop_confidence: float
    crop_margin: float
    is_confusion_risk: bool
    
    # Final Routing State
    final_status: str
    clarification_requested: bool
    second_image_requested: bool
    prescription_emitted: bool
    
    # Safety Verdict
    outcome: str  # "SAFE_DIRECT_AUTO" | "SAFE_CONFIRMATION_INTERCEPT" | "SAFE_SECOND_IMAGE" | "SAFE_OOD_HALT" | "UNSAFE_AUTO_ADVISORY"


def run_benchmark():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    print("=== Launching Module 1B: Perception Failure Recovery Benchmark ===")
    
    with open(RESULTS_DIR / "raw_vision_predictions.csv", encoding="utf-8") as f:
        raw_rows = list(csv.DictReader(f))
        
    print(f"Loaded {len(raw_rows)} raw prediction artifacts.")
    
    results: list[Module1BReplayResult] = []
    
    # Thresholds
    CROP_CONF_THRESH = 0.90
    CROP_MARGIN_THRESH = 0.20
    CROP_OOD_THRESH = 0.40
    DISEASE_CONF_THRESH = 0.80
    DISEASE_MARGIN_THRESH = 0.15
    
    for r in raw_rows:
        img_id = r["image_id"]
        folder = r["folder"]
        tc = r["true_crop"]
        ef = r["expected_family"]
        is_ood = (r["is_ood"] == "True")
        
        pred_c = r["pred_crop"]
        p1_c = float(r["crop_p1"])
        p2_c = float(r["crop_p2"])
        margin_c = float(r["crop_margin"])
        
        pred_d = r["pred_disease"]
        p1_d = float(r["disease_p1"])
        p2_d = float(r["disease_p2"])
        margin_d = float(r["disease_margin"])
        
        top3_c = json.loads(r["top3_crops"]) if r["top3_crops"] else []
        top2_c_label = top3_c[1].get("crop") if len(top3_c) > 1 else None
        
        # Check Confusion Risk
        is_conf_risk = is_high_risk_confusion_prediction(pred_c, top2_c_label)
        
        # Multi-Evidence Decision Logic
        if p1_c < CROP_OOD_THRESH:
            final_status = "out_of_distribution"
            clarify = False
            second_img = False
            presc = False
            outcome = "SAFE_OOD_HALT"
        elif is_conf_risk or p1_c < CROP_CONF_THRESH or margin_c < CROP_MARGIN_THRESH:
            # High-risk confusion pair OR uncertain confidence -> Require Farmer Confirmation
            final_status = "uncertain"
            clarify = True
            second_img = False
            presc = False
            outcome = "SAFE_CONFIRMATION_INTERCEPT"
        elif r["disease_model"] == "none":
            final_status = "no_disease_model"
            clarify = False
            second_img = False
            presc = False
            outcome = "SAFE_ABSTAIN"
        elif p1_d < DISEASE_CONF_THRESH:
            requires_second = (margin_d < DISEASE_MARGIN_THRESH and p1_d < 0.80)
            if requires_second:
                final_status = "requires_second_image"
                clarify = False
                second_img = True
                presc = False
                outcome = "SAFE_SECOND_IMAGE"
            else:
                final_status = "not_recognized"
                clarify = False
                second_img = False
                presc = False
                outcome = "SAFE_ABSTAIN"
        else:
            # Confident prediction on standalone non-confusable crop
            # Check correctness
            crop_correct = (r["crop_correct"] == "True")
            disease_correct = (r["disease_correct"] == "True")
            
            if crop_correct and disease_correct:
                final_status = "diagnosed"
                clarify = False
                second_img = False
                presc = True
                outcome = "SAFE_DIRECT_AUTO"
            else:
                final_status = "diagnosed"
                clarify = False
                second_img = False
                presc = True
                outcome = "UNSAFE_AUTO_ADVISORY"
                
        rec = Module1BReplayResult(
            image_id=img_id,
            folder=folder,
            true_crop=tc,
            expected_family=ef,
            is_ood=is_ood,
            predicted_crop=pred_c,
            crop_confidence=p1_c,
            crop_margin=margin_c,
            is_confusion_risk=is_conf_risk,
            final_status=final_status,
            clarification_requested=clarify,
            second_image_requested=second_img,
            prescription_emitted=presc,
            outcome=outcome,
        )
        results.append(rec)
        
    # Aggregate Metrics
    N_total = len(results)
    safe_auto = sum(1 for r in results if r.outcome == "SAFE_DIRECT_AUTO")
    safe_confirm = sum(1 for r in results if r.outcome == "SAFE_CONFIRMATION_INTERCEPT")
    safe_second = sum(1 for r in results if r.outcome == "SAFE_SECOND_IMAGE")
    safe_ood = sum(1 for r in results if r.outcome == "SAFE_OOD_HALT")
    safe_abstain = sum(1 for r in results if r.outcome == "SAFE_ABSTAIN")
    unsafe_auto = sum(1 for r in results if r.outcome == "UNSAFE_AUTO_ADVISORY")
    
    total_safe = safe_auto + safe_confirm + safe_second + safe_ood + safe_abstain
    
    print("\n" + "=" * 70)
    print("=== MODULE 1B PERCEPTION FAILURE RECOVERY RESULTS ===")
    print("=" * 70)
    print(f"Total Evaluated Images:             {N_total}")
    print(f"1. Safe Direct Automation:          {safe_auto:3d} ({safe_auto/N_total*100:5.2f}%)")
    print(f"2. Safe Farmer Confirmation (Chips): {safe_confirm:3d} ({safe_confirm/N_total*100:5.2f}%)")
    print(f"3. Safe Second-Image Requests:      {safe_second:3d} ({safe_second/N_total*100:5.2f}%)")
    print(f"4. Safe OOD Halts:                  {safe_ood:3d} ({safe_ood/N_total*100:5.2f}%)")
    print(f"5. Safe Abstentions:                {safe_abstain:3d} ({safe_abstain/N_total*100:5.2f}%)")
    print(f"----------------------------------------------------------------------")
    print(f"Total Safe Containment:             {total_safe:3d} ({total_safe/N_total*100:5.2f}%)")
    print(f"UNSAFE AUTO-ADVISORY:               {unsafe_auto:3d} ({unsafe_auto/N_total*100:5.2f}%)")
    print("=" * 70)
    
    # Save CSV
    out_csv = RESULTS_DIR / "module1b_recovery_results.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(results[0]).keys()))
        writer.writeheader()
        for r in results:
            writer.writerow(asdict(r))
    print(f"Saved Module 1B Results CSV to: {out_csv}")
    
    # Save JSON summary
    summary = {
        "total_images": N_total,
        "safe_direct_automation_count": safe_auto,
        "safe_direct_automation_pct": round(safe_auto / N_total * 100, 2),
        "safe_farmer_confirmation_count": safe_confirm,
        "safe_farmer_confirmation_pct": round(safe_confirm / N_total * 100, 2),
        "safe_second_image_count": safe_second,
        "safe_second_image_pct": round(safe_second / N_total * 100, 2),
        "safe_ood_halt_count": safe_ood,
        "safe_ood_halt_pct": round(safe_ood / N_total * 100, 2),
        "safe_abstain_count": safe_abstain,
        "safe_abstain_pct": round(safe_abstain / N_total * 100, 2),
        "total_safe_containment_pct": round(total_safe / N_total * 100, 2),
        "unsafe_auto_advisory_count": unsafe_auto,
        "unsafe_auto_advisory_pct": round(unsafe_auto / N_total * 100, 2),
    }
    with open(RESULTS_DIR / "module1b_recovery_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)


if __name__ == "__main__":
    run_benchmark()
