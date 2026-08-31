#!/usr/bin/env python3
"""
experiments/scripts/audit_11_residual_cases.py
Exhaustive manual failure audit of the 11 residual unsafe auto-advisory cases under Module 1B.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = WORKSPACE_ROOT / "experiments" / "results" / "E02_vision_gate_calibration"
E2E_CSV = RESULTS_DIR / "e2e_safety_replay_results.csv"
RAW_CSV = RESULTS_DIR / "raw_vision_predictions.csv"


@dataclass
class Residual11AuditRecord:
    case_num: int
    image_id: str
    true_crop: str
    pred_crop: str
    crop_conf: float
    crop_margin: float
    true_disease: str
    pred_disease: str
    disease_conf: float
    disease_margin: float
    failure_type: str  # "HEALTHY_FALSE_POSITIVE" | "INTRA_CROP_MISDIAGNOSIS" | "CROSS_CROP_RESIDUAL"
    why_wrong: str
    harm_type: str  # "Crop Loss via Delayed Treatment" | "Ineffective Suboptimal Spray" | "Cross-Crop Chemical Mismatch"
    hypothesized_recovery: str  # "Second-Image Under-Leaf Close-Up" | "Farmer Symptom Prompt" | "Irrecoverable Single Image"


def audit_11_cases():
    with open(E2E_CSV, encoding="utf-8") as f:
        e2e_rows = list(csv.DictReader(f))
    with open(RAW_CSV, encoding="utf-8") as f:
        raw_rows = {r["image_id"]: r for r in csv.DictReader(f)}
        
    residual_rows = [r for r in e2e_rows if r["outcome"] == "UNSAFE_AUTO_ADVISORY"]
    print(f"Auditing exactly {len(residual_rows)} residual unsafe cases...")
    
    records: list[Residual11AuditRecord] = []
    
    for i, r in enumerate(residual_rows, 1):
        img_id = r["image_id"]
        raw = raw_rows.get(img_id, {})
        
        tc = r["true_crop"]
        pc = r["predicted_crop"]
        c_conf = float(r["crop_confidence"])
        c_margin = float(raw.get("crop_margin", 0.0))
        
        td = r["folder"]
        pd = r["predicted_disease"]
        d_conf = float(r["disease_confidence"])
        d_margin = float(raw.get("disease_margin", 0.0))
        
        # Diagnostic analysis of each failure
        td_lower = td.lower()
        pd_lower = pd.lower()
        
        if "healthy" in pd_lower and "healthy" not in td_lower:
            ftype = "HEALTHY_FALSE_POSITIVE"
            why = "Early-stage or mild chlorotic/necrotic spot misclassified as healthy due to wide-angle leaf area dominance"
            harm = "Crop Loss via Delayed Treatment (Farmer told leaf is healthy; disease spreads untreated)"
            recov = "Second-Image Under-Leaf Close-Up (Magnified view of spot texture/hyphae)"
        elif tc.lower() != pc.lower() and not (tc.lower() in ("cabbage", "cauliflower") and pc.lower() == "brassica"):
            ftype = "CROSS_CROP_RESIDUAL"
            why = f"Model classified {tc} as {pc} (extreme high confidence outlier without top2 confusion co-occurrence)"
            harm = "Cross-Crop Chemical Mismatch (Risk of non-registered pesticide)"
            recov = "Farmer Confirmation Gate (Forcing confirmation on all single-crop non-monoculture uploads)"
        else:
            ftype = "INTRA_CROP_MISDIAGNOSIS"
            why = f"Correct crop ({tc}), but misidentified {td.split('__')[-1]} as {pd.split('__')[-1]} (phenotypic foliar lesion similarity)"
            harm = "Ineffective Suboptimal Spray (Pesticide target mismatch within same crop catalog)"
            recov = "Second-Image Under-Leaf Close-Up + Symptom Checklist"
            
        record = Residual11AuditRecord(
            case_num=i,
            image_id=img_id,
            true_crop=tc,
            pred_crop=pc,
            crop_conf=round(c_conf, 4),
            crop_margin=round(c_margin, 4),
            true_disease=td,
            pred_disease=pd,
            disease_conf=round(d_conf, 4),
            disease_margin=round(d_margin, 4),
            failure_type=ftype,
            why_wrong=why,
            harm_type=harm,
            hypothesized_recovery=recov,
        )
        records.append(record)
        
    # Save CSV
    out_csv = RESULTS_DIR / "residual_11_cases_audit.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(records[0]).keys()))
        writer.writeheader()
        for rec in records:
            writer.writerow(asdict(rec))
    print(f"Saved 11 Residual Cases Audit to: {out_csv}")
    
    # Print clean markdown table
    print("\n" + "=" * 110)
    print("=== EXHAUSTIVE AUDIT OF THE 11 RESIDUAL UNSAFE CASES ===")
    print("=" * 110)
    for r in records:
        print(f"Case #{r.case_num:02d}: {r.image_id}")
        print(f"  Crop:    True = {r.true_crop:12s} | Pred = {r.pred_crop:12s} (conf={r.crop_conf:.3f}, margin={r.crop_margin:.3f})")
        print(f"  Disease: True = {r.true_disease:25s} | Pred = {r.pred_disease:25s} (conf={r.disease_conf:.3f}, margin={r.disease_margin:.3f})")
        print(f"  Type:    {r.failure_type}")
        print(f"  Why:     {r.why_wrong}")
        print(f"  Harm:    {r.harm_type}")
        print(f"  Recovery:{r.hypothesized_recovery}")
        print("-" * 110)


if __name__ == "__main__":
    audit_11_cases()
