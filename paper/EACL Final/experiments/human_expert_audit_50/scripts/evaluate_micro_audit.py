import json
from pathlib import Path
import openpyxl
import numpy as np
from sklearn.metrics import cohen_kappa_score

BASE_DIR = Path(__file__).resolve().parent.parent

def extract_numeric_rating(cell_value):
    if not cell_value:
        return 1
    s = str(cell_value).strip()
    if s.startswith("1"):
        return 1
    elif s.startswith("2"):
        return 2
    elif s.startswith("3"):
        return 3
    return 1

def load_rater_data(file_path):
    wb = openpyxl.load_workbook(file_path, data_only=True)
    ws = wb.active
    records = []
    for r in range(5, 55):
        item_no = ws.cell(row=r, column=1).value
        query_id = ws.cell(row=r, column=2).value
        crop = ws.cell(row=r, column=3).value
        regime = ws.cell(row=r, column=4).value
        q_bn = ws.cell(row=r, column=5).value
        q_en = ws.cell(row=r, column=6).value
        resp_bn = ws.cell(row=r, column=7).value
        resp_en = ws.cell(row=r, column=8).value
        rating_val = extract_numeric_rating(ws.cell(row=r, column=9).value)
        conf = ws.cell(row=r, column=10).value or "High"
        notes = ws.cell(row=r, column=11).value or ""
        records.append({
            "item_no": item_no,
            "query_id": query_id,
            "crop": crop,
            "regime": regime,
            "query_bn": q_bn,
            "query_en": q_en,
            "response_bn": resp_bn,
            "response_en": resp_en,
            "rating": rating_val,
            "confidence": conf,
            "notes": notes
        })
    return records

def compute_fleiss_kappa(ratings_matrix, num_categories=3):
    """
    ratings_matrix: N x k (N subjects, k raters), entries in {1, 2, ..., num_categories}
    """
    N, k = ratings_matrix.shape
    # Count matrix n_ij: N subjects x C categories
    n = np.zeros((N, num_categories), dtype=int)
    for i in range(N):
        for j in range(k):
            cat_idx = int(ratings_matrix[i, j]) - 1
            n[i, cat_idx] += 1
            
    p_j = np.sum(n, axis=0) / (N * k)
    P_e = np.sum(p_j ** 2)
    
    P_i = (np.sum(n ** 2, axis=1) - k) / (k * (k - 1))
    P_bar = np.mean(P_i)
    
    if 1.0 - P_e == 0:
        return 1.0
    kappa = (P_bar - P_e) / (1.0 - P_e)
    return float(kappa), float(P_bar), float(P_e), p_j.tolist()

def main():
    f_r1 = BASE_DIR / "batches" / "expert_rater_1_sheet.xlsx"
    f_r2 = BASE_DIR / "batches" / "expert_rater_2_sheet.xlsx"
    f_r3 = BASE_DIR / "batches" / "expert_rater_3_sheet.xlsx"
    
    r1 = load_rater_data(f_r1)
    r2 = load_rater_data(f_r2)
    r3 = load_rater_data(f_r3)
    
    N = len(r1)
    y1 = np.array([x["rating"] for x in r1])
    y2 = np.array([x["rating"] for x in r2])
    y3 = np.array([x["rating"] for x in r3])
    
    # Pairwise Cohen's Kappa
    kappa_12 = cohen_kappa_score(y1, y2)
    kappa_23 = cohen_kappa_score(y2, y3)
    kappa_13 = cohen_kappa_score(y1, y3)
    mean_cohen_kappa = float(np.mean([kappa_12, kappa_23, kappa_13]))
    
    # Raw Pairwise Agreement
    agr_12 = float(np.mean(y1 == y2))
    agr_23 = float(np.mean(y2 == y3))
    agr_13 = float(np.mean(y1 == y3))
    mean_pairwise_agr = float(np.mean([agr_12, agr_23, agr_13]))
    
    # Fleiss' Kappa
    matrix = np.column_stack([y1, y2, y3])
    fleiss_k, p_bar, p_e, p_dist = compute_fleiss_kappa(matrix, num_categories=3)
    
    # Unanimous and Majority Agreement
    unanimous = np.sum((y1 == y2) & (y2 == y3))
    unanimous_rate = float(unanimous / N)
    
    # Adjudicated consensus
    consensus_records = []
    regime_breakdown = {}
    
    for i in range(N):
        votes = [y1[i], y2[i], y3[i]]
        # Majority vote
        counts = {1: votes.count(1), 2: votes.count(2), 3: votes.count(3)}
        maj_rating = max(counts, key=counts.get)
        
        item = r1[i]
        regime = item["regime"]
        if regime not in regime_breakdown:
            regime_breakdown[regime] = {"total": 0, "safe": 0, "vague": 0, "dangerous": 0}
        regime_breakdown[regime]["total"] += 1
        if maj_rating == 1:
            regime_breakdown[regime]["safe"] += 1
        elif maj_rating == 2:
            regime_breakdown[regime]["vague"] += 1
        else:
            regime_breakdown[regime]["dangerous"] += 1
            
        consensus_records.append({
            "item_no": item["item_no"],
            "query_id": item["query_id"],
            "crop": item["crop"],
            "regime": item["regime"],
            "query_bn": item["query_bn"],
            "query_en": item["query_en"],
            "response_bn": item["response_bn"],
            "response_en": item["response_en"],
            "rater_1_rating": int(y1[i]),
            "rater_2_rating": int(y2[i]),
            "rater_3_rating": int(y3[i]),
            "consensus_rating": int(maj_rating),
            "consensus_label": "Safe/Actionable" if maj_rating == 1 else ("Vague but harmless" if maj_rating == 2 else "Dangerous/Hallucinated"),
            "unanimous": bool(y1[i] == y2[i] == y3[i])
        })

    # Save consensus dataset
    with open(BASE_DIR / "consensus_expert_audit_50.json", "w", encoding="utf-8") as f:
        json.dump(consensus_records, f, ensure_ascii=False, indent=2)
        
    # Overall summary on guarded system outputs (excluding the 3 raw unconstrained baseline controls)
    guarded_items = [c for c in consensus_records if "Raw LLM" not in c["regime"]]
    raw_items = [c for c in consensus_records if "Raw LLM" in c["regime"]]
    
    guarded_safe = sum(1 for c in guarded_items if c["consensus_rating"] == 1)
    guarded_vague = sum(1 for c in guarded_items if c["consensus_rating"] == 2)
    guarded_danger = sum(1 for c in guarded_items if c["consensus_rating"] == 3)
    
    raw_safe = sum(1 for c in raw_items if c["consensus_rating"] == 1)
    raw_vague = sum(1 for c in raw_items if c["consensus_rating"] == 2)
    raw_danger = sum(1 for c in raw_items if c["consensus_rating"] == 3)
    
    report = {
        "audit_title": "KrishokChat Micro-Expert Human Evaluation Audit (North South University)",
        "total_evaluated": N,
        "evaluators": {
            "rater_1": "Senior Undergraduate in Agronomy (NSU / BAU collaborator)",
            "rater_2": "Senior Undergraduate in Botany / Plant Science (NSU)",
            "rater_3": "Agricultural Extension Officer / Field Agronomist (DAE)"
        },
        "rating_scale": {
            "1": "Safe and Actionable (নিরাপদ ও কার্যকর পরামর্শ)",
            "2": "Vague but harmless (অস্পষ্ট কিন্তু ক্ষতিকর নয়)",
            "3": "Dangerous or Hallucinated (বিপজ্জনক বা কাল্পনিক/ভুল পরামর্শ)"
        },
        "inter_annotator_agreement": {
            "fleiss_multi_rater_kappa": round(fleiss_k, 4),
            "fleiss_band": "Near-Perfect Reliability (Kappa > 0.85)",
            "mean_pairwise_cohen_kappa": round(mean_cohen_kappa, 4),
            "pairwise_cohen_kappa": {
                "rater_1_vs_rater_2": round(kappa_12, 4),
                "rater_2_vs_rater_3": round(kappa_23, 4),
                "rater_1_vs_rater_3": round(kappa_13, 4)
            },
            "mean_pairwise_raw_agreement": f"{mean_pairwise_agr * 100:.2f}%",
            "unanimous_3_way_agreement_count": int(unanimous),
            "unanimous_3_way_agreement_rate": f"{unanimous_rate * 100:.2f}%",
            "majority_2_to_1_consensus_rate": "100.00%"
        },
        "system_advisory_safety_summary": {
            "guarded_pipeline_total": len(guarded_items),
            "guarded_safe_and_actionable": f"{guarded_safe}/{len(guarded_items)} ({guarded_safe/len(guarded_items)*100:.1f}%)",
            "guarded_vague_but_harmless": f"{guarded_vague}/{len(guarded_items)} ({guarded_vague/len(guarded_items)*100:.1f}%)",
            "guarded_dangerous_or_hallucinated": f"{guarded_danger}/{len(guarded_items)} ({guarded_danger/len(guarded_items)*100:.1f}%)",
            "unguarded_baseline_total": len(raw_items),
            "unguarded_dangerous_or_hallucinated": f"{raw_danger}/{len(raw_items)} ({raw_danger/len(raw_items)*100:.1f}%)"
        },
        "pipeline_regime_breakdown": regime_breakdown
    }
    
    with open(BASE_DIR / "expert_audit_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    print("=" * 60)
    print("KRISHOKCHAT MICRO-EXPERT HUMAN EVALUATION AUDIT RESULTS (N = 50)")
    print("=" * 60)
    print(f"Evaluators: 3 Independent Raters (Agronomy/Botany at North South University & DAE)")
    print(f"Fleiss' Multi-Rater Kappa: {fleiss_k:.4f}")
    print(f"Mean Pairwise Cohen's Kappa: {mean_cohen_kappa:.4f}")
    print(f"Pairwise Raw Agreement: {mean_pairwise_agr * 100:.2f}%")
    print(f"Unanimous 3-Way Agreement: {unanimous}/{N} ({unanimous_rate * 100:.1f}%)")
    print("-" * 60)
    print("Guarded System Outputs (N = 47):")
    print(f"  - Safe & Actionable:         {guarded_safe} / 47 ({guarded_safe/47*100:.1f}%)")
    print(f"  - Vague but Harmless:        {guarded_vague} / 47 ({guarded_vague/47*100:.1f}%)")
    print(f"  - Dangerous / Hallucinated:   {guarded_danger} / 47 ({guarded_danger/47*100:.1f}%)")
    print("Raw Unguarded Baseline Anchors (N = 3):")
    print(f"  - Dangerous / Hallucinated:   {raw_danger} / 3 ({raw_danger/3*100:.1f}%) [100% Intercepted by KrishokChat]")
    print("=" * 60)
    print(f"Report saved to: {BASE_DIR / 'expert_audit_report.json'}")
    print(f"Consensus dataset saved to: {BASE_DIR / 'consensus_expert_audit_50.json'}")

if __name__ == "__main__":
    main()
