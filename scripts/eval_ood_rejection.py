"""Eval OOD rejection rate using the live backend ONNX/Ultralytics crop classifier.
Logs p1, p2, margin, gate decision (State C vs B vs A) for each OOD image.
Saves results to experiments/ood_test/ood_100/ood_eval_results.json / .csv
"""
from pathlib import Path
import csv, json
from PIL import Image
import sys
sys.path.insert(0, str(Path("D:/KrishokChat Advisory System/backend")))
from app.infrastructure.vision.ultralytics_classifier import UltralyticsClassificationRunner
from app.infrastructure.vision.registry import ArtifactVisionRegistry
from app.domain.vision import VisionGateConfig

VISION_DIR = Path("D:/KrishokChat Advisory System/backend/ml_assets/vision")
OOD_ROOT = Path("D:/KrishokChat Advisory System/experiments/ood_test/ood_100")
OUT_JSON = OOD_ROOT / "ood_eval_results.json"
OUT_CSV = OOD_ROOT / "ood_eval_results.csv"

gate = VisionGateConfig()  # defaults: crop_ood 0.40, crop_conf 0.90, margin 0.20
registry = ArtifactVisionRegistry(VISION_DIR)
runner = UltralyticsClassificationRunner()

print(f"Gate: ood={gate.crop_ood_threshold} conf={gate.crop_confidence_threshold} margin={gate.crop_margin_threshold}")
print(f"Crop classes: {registry.crop_classifier.class_names}")
print(f"Scanning {OOD_ROOT}")

records = []
for cat_dir in sorted(OOD_ROOT.iterdir()):
    if not cat_dir.is_dir():
        continue
    for img_path in sorted(cat_dir.glob("*.jpg")):
        img = Image.open(img_path).convert("RGB")
        pred = runner.predict(registry.crop_classifier, img)
        p1 = pred.confidence
        # runner stores under "class" not "crop" - VisionPipeline uses "crop"/"class" flexible lookup
        # unify
        top3 = pred.top3
        p2 = float(top3[1]["confidence"]) if len(top3) > 1 else 0.0
        margin = p1 - p2
        # tri-state gate logic copy
        if p1 < gate.crop_ood_threshold:
            gate_state = "C_OOD_REJECT"
            decision = "State C: prompt for re-capture (out_of_distribution)"
            is_ood_rejected = True
            is_misclassified_confident = False
        elif p1 < gate.crop_confidence_threshold or margin < gate.crop_margin_threshold:
            # also check confusion pair
            gate_state = "B_UNCERTAIN"
            decision = "State B: ask user to select crop chip"
            is_ood_rejected = False  # not fully rejected, but not confidently misclassified either
            is_misclassified_confident = False
        else:
            gate_state = "A_CONFIDENT"
            decision = f"State A: CONFIDENTLY misclassifies as {pred.label} ({p1:.3f})"
            is_ood_rejected = False
            is_misclassified_confident = True

        rec = {
            "category": cat_dir.name,
            "file": img_path.relative_to(OOD_ROOT).as_posix(),
            "true_ood_crop": cat_dir.name,
            "predicted_label": pred.label,
            "p1": p1,
            "p2": p2,
            "margin": round(margin,4),
            "top3": [{"label": t.get("class") or t.get("crop"), "conf": t.get("confidence")} for t in top3],
            "gate_state": gate_state,
            "decision": decision,
            "is_ood_rejected": is_ood_rejected,
            "is_misclassified_confident": is_misclassified_confident,
        }
        records.append(rec)
        print(f"{rec['category']:10s} {img_path.name:45s} -> {pred.label:12s} p1={p1:.3f} p2={p2:.3f} margin={margin:.3f} [{gate_state}]")

# summary
total = len(records)
n_c = sum(1 for r in records if r["gate_state"]=="C_OOD_REJECT")
n_b = sum(1 for r in records if r["gate_state"]=="B_UNCERTAIN")
n_a = sum(1 for r in records if r["gate_state"]=="A_CONFIDENT")
# OOD rejection rate as defined in paper: State C 100% ideal; State B is also safe (not confident misclassify)
safe = n_c + n_b
conf_mis = n_a

print("\n=== SUMMARY ===")
print(f"Total OOD images: {total}")
print(f"State C (OOD reject, p1<0.40): {n_c} ({n_c/total*100:.1f}%)")
print(f"State B (Uncertain, prompt chip): {n_b} ({n_b/total*100:.1f}%)")
print(f"State A (Confident but WRONG): {n_a} ({n_a/total*100:.1f}%)")
print(f"SAFE (C+B, not confidently misclassified): {safe} ({safe/total*100:.1f}%)")
print(f"HAZARD (confidently misclassified as supported crop): {conf_mis} ({conf_mis/total*100:.1f}%)")

# per-category breakdown
from collections import defaultdict
per_cat = defaultdict(list)
for r in records:
    per_cat[r["category"]].append(r)
print("\nPer-category:")
for cat in sorted(per_cat):
    lst = per_cat[cat]
    tc = sum(1 for r in lst if r["gate_state"]=="C_OOD_REJECT")
    tb = sum(1 for r in lst if r["gate_state"]=="B_UNCERTAIN")
    ta = sum(1 for r in lst if r["gate_state"]=="A_CONFIDENT")
    print(f" {cat:10s} n={len(lst):2d}  C={tc:2d} ({tc/len(lst)*100:4.1f}%)  B={tb:2d} ({tb/len(lst)*100:4.1f}%)  A={ta:2d} ({ta/len(lst)*100:4.1f}%) safe={tc+tb}/{len(lst)}")

# save
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump({"gate": {"crop_ood_threshold": gate.crop_ood_threshold, "crop_confidence_threshold": gate.crop_confidence_threshold, "crop_margin_threshold": gate.crop_margin_threshold}, "summary": {"total": total, "C": n_c, "B": n_b, "A": n_a, "safe": safe, "hazard": conf_mis}, "records": records}, f, indent=2, ensure_ascii=False)
print(f"\nSaved JSON: {OUT_JSON}")

with open(OUT_CSV, "w", newline="", encoding="utf-8") as cf:
    w = csv.DictWriter(cf, fieldnames=["category","file","true_ood_crop","predicted_label","p1","p2","margin","gate_state","is_ood_rejected","is_misclassified_confident"])
    w.writeheader()
    for r in records:
        w.writerow({k: r[k] for k in ["category","file","true_ood_crop","predicted_label","p1","p2","margin","gate_state","is_ood_rejected","is_misclassified_confident"]})
print(f"Saved CSV: {OUT_CSV}")
