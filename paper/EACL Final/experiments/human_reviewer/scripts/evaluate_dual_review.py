import os
import glob
import json
import openpyxl
from collections import Counter

BASE_DIR = r"D:\KrishokChat Advisory System\paper\EACL Final\experiments\human_reviewer"
SEALED_REF = os.path.join(BASE_DIR, "reference_ground_truth", "reviewer_1_labels_sealed.json")
BATCHES_DIR = os.path.join(BASE_DIR, "batches")
MASTER_FILE = os.path.join(BASE_DIR, "master_blind_sheet_200.xlsx")

def compute_cohens_kappa(labels1, labels2):
    """Compute Cohen's kappa for two raters."""
    assert len(labels1) == len(labels2)
    n = len(labels1)
    if n == 0:
        return 0.0

    categories = list(set(labels1) | set(labels2))
    cat_to_idx = {c: i for i, c in enumerate(categories)}
    k = len(categories)

    matrix = [[0] * k for _ in range(k)]
    for l1, l2 in zip(labels1, labels2):
        matrix[cat_to_idx[l1]][cat_to_idx[l2]] += 1

    # Observed agreement
    po = sum(matrix[i][i] for i in range(k)) / n

    # Expected agreement
    r1_counts = [sum(matrix[i][j] for j in range(k)) for i in range(k)]
    r2_counts = [sum(matrix[j][i] for j in range(k)) for i in range(k)]
    pe = sum((r1_counts[i] * r2_counts[i]) for i in range(k)) / (n * n)

    if pe == 1.0:
        return 1.0
    return (po - pe) / (1.0 - pe)

def load_reviewer_2_annotations():
    """Load annotations from either master sheet or batch sheets."""
    annotations = {}

    # Check batch files
    batch_files = sorted(glob.glob(os.path.join(BATCHES_DIR, "*.xlsx")))
    for bf in batch_files:
        wb = openpyxl.load_workbook(bf, data_only=True)
        ws = wb.active
        for r in range(2, ws.max_row + 1):
            qid = ws.cell(row=r, column=2).value
            if not qid:
                continue
            crop_bn = ws.cell(row=r, column=5).value or ""
            crop_en = ws.cell(row=r, column=6).value or ""
            specified = ws.cell(row=r, column=7).value or ""
            intent = ws.cell(row=r, column=8).value or ""
            confidence = ws.cell(row=r, column=9).value or ""
            notes = ws.cell(row=r, column=10).value or ""

            # Check if annotated
            if crop_bn or crop_en or specified:
                annotations[str(qid).strip()] = {
                    "crop_bn": str(crop_bn).strip(),
                    "crop_en": str(crop_en).strip().lower(),
                    "is_specified": str(specified).strip().upper(),
                    "intent": str(intent).strip(),
                    "confidence": str(confidence).strip(),
                    "notes": str(notes).strip()
                }

    # Also check master sheet if batches were empty
    if len(annotations) < 200 and os.path.exists(MASTER_FILE):
        wb = openpyxl.load_workbook(MASTER_FILE, data_only=True)
        ws = wb["All 200 Queries"]
        for r in range(2, ws.max_row + 1):
            qid = ws.cell(row=r, column=2).value
            if not qid:
                continue
            crop_bn = ws.cell(row=r, column=5).value or ""
            crop_en = ws.cell(row=r, column=6).value or ""
            specified = ws.cell(row=r, column=7).value or ""
            intent = ws.cell(row=r, column=8).value or ""
            confidence = ws.cell(row=r, column=9).value or ""
            notes = ws.cell(row=r, column=10).value or ""

            if (crop_bn or crop_en or specified) and str(qid).strip() not in annotations:
                annotations[str(qid).strip()] = {
                    "crop_bn": str(crop_bn).strip(),
                    "crop_en": str(crop_en).strip().lower(),
                    "is_specified": str(specified).strip().upper(),
                    "intent": str(intent).strip(),
                    "confidence": str(confidence).strip(),
                    "notes": str(notes).strip()
                }

    return annotations

def main():
    print("=== DUAL-REVIEWER EVALUATION RUNNER ===")
    with open(SEALED_REF, "r", encoding="utf-8") as f:
        ref_data = json.load(f)

    r2_data = load_reviewer_2_annotations()
    print(f"Total reference queries: {len(ref_data)}")
    print(f"Total Reviewer 2 annotated queries: {len(r2_data)}")

    if len(r2_data) == 0:
        print("\n[NOTE] No annotations detected in batch Excel files yet.")
        print("Once the human annotator fills in the Excel files in 'batches/', re-run this script to:")
        print("  1. Compute raw percentage agreement on crop slots and binary ambiguity.")
        print("  2. Compute Cohen's Kappa inter-annotator reliability coefficient.")
        print("  3. Generate an autopsy list of discordant cases for consensus resolution.")
        print("  4. Re-benchmark the deterministic gate against the consensus dual-reviewer gold.")
        return

    # Compare aligned items
    aligned_items = []
    r1_binary = []
    r2_binary = []
    r1_crop = []
    r2_crop = []
    disagreements = []

    for item in ref_data:
        qid = str(item["id"]).strip()
        if qid not in r2_data:
            continue

        r1_c = str(item.get("reviewer_1_crop") or "").strip().lower()
        r1_spec = "NO" if r1_c in ["", "none", "null"] else "YES"

        r2 = r2_data[qid]
        r2_c = str(r2.get("crop_en") or "").strip().lower()
        r2_spec = r2.get("is_specified") or ("NO" if r2_c in ["", "none", "null"] else "YES")

        r1_binary.append(r1_spec)
        r2_binary.append(r2_spec)

        r1_crop.append(r1_c if r1_c else "NO_CROP")
        r2_crop.append(r2_c if r2_c else "NO_CROP")

        match_binary = (r1_spec == r2_spec)
        match_crop = (r1_c == r2_c)

        if not (match_binary and match_crop):
            disagreements.append({
                "query_id": qid,
                "query": item["query"],
                "r1_crop": r1_c,
                "r2_crop": r2_c,
                "r1_specified": r1_spec,
                "r2_specified": r2_spec,
                "r2_notes": r2.get("notes")
            })

    total_eval = len(r1_binary)
    bin_agree = sum(1 for a, b in zip(r1_binary, r2_binary) if a == b) / total_eval if total_eval else 0
    crop_agree = sum(1 for a, b in zip(r1_crop, r2_crop) if a == b) / total_eval if total_eval else 0

    kappa_bin = compute_cohens_kappa(r1_binary, r2_binary)
    kappa_crop = compute_cohens_kappa(r1_crop, r2_crop)

    print(f"\nEvaluated instances: {total_eval} / {len(ref_data)}")
    print(f"Binary Crop Presence Agreement: {bin_agree*100:.2f}% (Cohen's Kappa: {kappa_bin:.4f})")
    print(f"Exact Crop Category Agreement:  {crop_agree*100:.2f}% (Cohen's Kappa: {kappa_crop:.4f})")
    print(f"Discrepancies requiring consensus: {len(disagreements)}")

    # Save report
    report = {
        "n_evaluated": total_eval,
        "binary_agreement_rate": bin_agree,
        "binary_cohens_kappa": kappa_bin,
        "crop_exact_agreement_rate": crop_agree,
        "crop_cohens_kappa": kappa_crop,
        "n_disagreements": len(disagreements),
        "disagreements": disagreements
    }

    out_json = os.path.join(BASE_DIR, "dual_review_report.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Saved evaluation report to: {out_json}")

if __name__ == "__main__":
    main()
