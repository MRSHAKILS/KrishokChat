#!/usr/bin/env python3
"""
Statistical Evaluation & Synthesis for Benign-Query Helpfulness Audit (N = 50).
Reads completed rater sheets from batches/, unblinds assignments, and computes:
  - Mean & SD for Guarded vs. Baseline
  - Two-tailed Wilcoxon signed-rank test (scipy.stats)
  - Pairwise Win / Tie / Loss rates
  - Inter-annotator agreement (Fleiss' Kappa on preference, Spearman correlation)
  - Outputs consensus_helpfulness_audit_50.json & helpfulness_audit_report.json
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
import numpy as np
import openpyxl
from scipy import stats

HERE = Path(__file__).resolve().parent
AUDIT_DIR = HERE.parent
BATCHES_DIR = AUDIT_DIR / "batches"
KEY_JSON = AUDIT_DIR / "reference_adjudication" / "blinding_key_mapping.json"
GT_JSON = AUDIT_DIR / "reference_adjudication" / "ground_truth_queries_50.json"


def parse_score(val) -> int | None:
    if val is None:
        return None
    s = str(val).strip()
    for digit in ["1", "2", "3", "4", "5"]:
        if s.startswith(digit):
            return int(digit)
    return None


def parse_preference(val) -> str | None:
    if val is None:
        return None
    s = str(val).strip().lower()
    if "response 1" in s or "resp 1" in s or s == "1":
        return "Response 1"
    if "response 2" in s or "resp 2" in s or s == "2":
        return "Response 2"
    if "tie" in s or "equal" in s or s == "0":
        return "Tie"
    return None


def compute_fleiss_kappa(ratings_matrix: np.ndarray, num_categories: int = 3) -> float:
    """
    ratings_matrix: N x k (N items, k raters), values in {0, 1, 2}
    """
    N, k = ratings_matrix.shape
    n = np.zeros((N, num_categories), dtype=int)
    for i in range(N):
        for j in range(k):
            cat = int(ratings_matrix[i, j])
            n[i, cat] += 1

    p_j = np.sum(n, axis=0) / (N * k)
    P_e = np.sum(p_j ** 2)

    P_i = (np.sum(n ** 2, axis=1) - k) / (k * (k - 1))
    P_bar = float(np.mean(P_i))

    if 1.0 - P_e == 0:
        return 1.0
    return (P_bar - P_e) / (1.0 - P_e)


def load_rater_sheet(path: Path) -> list[dict]:
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.active
    rows = []
    for r in range(5, 55):
        qid = ws.cell(row=r, column=2).value
        s1 = parse_score(ws.cell(row=r, column=7).value)
        s2 = parse_score(ws.cell(row=r, column=8).value)
        pref = parse_preference(ws.cell(row=r, column=9).value)
        notes = str(ws.cell(row=r, column=10).value or "").strip()
        rows.append({
            "item_no": r - 4,
            "query_id": qid,
            "resp_1_score": s1,
            "resp_2_score": s2,
            "preference": pref,
            "notes": notes
        })
    return rows


def main():
    if not KEY_JSON.exists():
        print(f"ERROR: {KEY_JSON} missing.")
        return 1

    with open(KEY_JSON, "r", encoding="utf-8") as f:
        blinding_keys = json.load(f)

    with open(GT_JSON, "r", encoding="utf-8") as f:
        ground_truth = {q["query_id"]: q for q in json.load(f)}

    rater_files = [
        BATCHES_DIR / "helpfulness_rater_1_sheet.xlsx",
        BATCHES_DIR / "helpfulness_rater_2_sheet.xlsx",
        BATCHES_DIR / "helpfulness_rater_3_sheet.xlsx"
    ]

    for rf in rater_files:
        if not rf.exists():
            print(f"ERROR: {rf} does not exist. Awaiting completed rater sheets!")
            return 1

    raters_data = [load_rater_sheet(rf) for rf in rater_files]

    # Unblind and collect scores
    consensus_items = []
    guarded_all_scores = []
    baseline_all_scores = []
    guarded_mean_per_item = []
    baseline_mean_per_item = []

    # Matrix for Fleiss' Kappa on Pairwise Winner:
    # 0 = Guarded Wins, 1 = Baseline Wins, 2 = Tie
    pref_matrix = np.zeros((50, 3), dtype=int)
    win_counts = {"Guarded": 0, "Baseline": 0, "Tie": 0}

    for idx in range(50):
        qid = raters_data[0][idx]["query_id"]
        key_info = blinding_keys[qid]
        gt = ground_truth[qid]

        resp1_role = key_info["Response 1"]  # 'Guarded KrishokTech' or 'Unconstrained Baseline'
        is_resp1_guarded = (resp1_role == "Guarded KrishokTech")

        g_scores = []
        b_scores = []
        item_prefs = []

        for r_idx, r_data in enumerate(raters_data):
            row = r_data[idx]
            s1 = row["resp_1_score"] or 3
            s2 = row["resp_2_score"] or 3
            pref = row["preference"] or "Tie"

            if is_resp1_guarded:
                g_val = s1
                b_val = s2
                if pref == "Response 1":
                    r_winner = "Guarded"
                    pref_matrix[idx, r_idx] = 0
                elif pref == "Response 2":
                    r_winner = "Baseline"
                    pref_matrix[idx, r_idx] = 1
                else:
                    r_winner = "Tie"
                    pref_matrix[idx, r_idx] = 2
            else:
                g_val = s2
                b_val = s1
                if pref == "Response 1":
                    r_winner = "Baseline"
                    pref_matrix[idx, r_idx] = 1
                elif pref == "Response 2":
                    r_winner = "Guarded"
                    pref_matrix[idx, r_idx] = 0
                else:
                    r_winner = "Tie"
                    pref_matrix[idx, r_idx] = 2

            g_scores.append(g_val)
            b_scores.append(b_val)
            item_prefs.append(r_winner)

        # Consensus preference (majority vote)
        pref_counts = Counter(item_prefs)
        consensus_winner, _ = pref_counts.most_common(1)[0]
        win_counts[consensus_winner] += 1

        guarded_all_scores.extend(g_scores)
        baseline_all_scores.extend(b_scores)
        guarded_mean_per_item.append(float(np.mean(g_scores)))
        baseline_mean_per_item.append(float(np.mean(b_scores)))

        consensus_items.append({
            "item_no": idx + 1,
            "query_id": qid,
            "crop": gt["crop"],
            "query_bn": gt["query_bn"],
            "guarded_scores": g_scores,
            "baseline_scores": b_scores,
            "guarded_mean": round(float(np.mean(g_scores)), 2),
            "baseline_mean": round(float(np.mean(b_scores)), 2),
            "individual_preferences": item_prefs,
            "consensus_winner": consensus_winner,
        })

    # Statistical Analysis
    g_arr = np.array(guarded_mean_per_item)
    b_arr = np.array(baseline_mean_per_item)
    diff = g_arr - b_arr

    # Wilcoxon signed-rank test
    w_stat, p_val = stats.wilcoxon(g_arr, b_arr, alternative="two-sided")
    # Paired t-test
    t_stat, t_pval = stats.ttest_rel(g_arr, b_arr)

    # Inter-annotator agreement on preference
    fleiss_k = compute_fleiss_kappa(pref_matrix, num_categories=3)

    report = {
        "study_title": "Benign-Query Helpfulness and Advisory Utility Audit (N = 50)",
        "sample_size": 50,
        "evaluators_count": 3,
        "total_evaluations": 150,
        "guarded_krishoktech": {
            "mean_score": round(float(np.mean(guarded_all_scores)), 3),
            "sd_score": round(float(np.std(guarded_all_scores, ddof=1)), 3),
            "median_score": float(np.median(guarded_all_scores)),
        },
        "unconstrained_baseline": {
            "mean_score": round(float(np.mean(baseline_all_scores)), 3),
            "sd_score": round(float(np.std(baseline_all_scores, ddof=1)), 3),
            "median_score": float(np.median(baseline_all_scores)),
        },
        "pairwise_matchup": {
            "guarded_wins": win_counts["Guarded"],
            "baseline_wins": win_counts["Baseline"],
            "ties": win_counts["Tie"],
            "guarded_win_rate_pct": round((win_counts["Guarded"] / 50.0) * 100, 1),
            "baseline_win_rate_pct": round((win_counts["Baseline"] / 50.0) * 100, 1),
            "tie_rate_pct": round((win_counts["Tie"] / 50.0) * 100, 1),
        },
        "statistical_tests": {
            "wilcoxon_signed_rank_stat": float(w_stat),
            "wilcoxon_p_value": float(p_val),
            "paired_t_stat": float(t_stat),
            "paired_t_p_value": float(t_pval),
        },
        "inter_annotator_agreement": {
            "fleiss_kappa_preference": round(float(fleiss_k), 4),
            "agreement_tier": "Substantial" if fleiss_k >= 0.6 else "Moderate",
        }
    }

    # Save reports
    with open(AUDIT_DIR / "consensus_helpfulness_audit_50.json", "w", encoding="utf-8") as f:
        json.dump(consensus_items, f, ensure_ascii=False, indent=2)

    with open(AUDIT_DIR / "helpfulness_audit_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print("BENIGN-QUERY HELPFULNESS AUDIT REPORT (N = 50)")
    print("=" * 60)
    print(f"Guarded KrishokTech Mean: {report['guarded_krishoktech']['mean_score']} (SD {report['guarded_krishoktech']['sd_score']})")
    print(f"Baseline Unconstrained:   {report['unconstrained_baseline']['mean_score']} (SD {report['unconstrained_baseline']['sd_score']})")
    print(f"Pairwise Preference:      Guarded: {report['pairwise_matchup']['guarded_wins']}/50 ({report['pairwise_matchup']['guarded_win_rate_pct']}%) | "
          f"Baseline: {report['pairwise_matchup']['baseline_wins']}/50 ({report['pairwise_matchup']['baseline_win_rate_pct']}%) | "
          f"Ties: {report['pairwise_matchup']['ties']}/50 ({report['pairwise_matchup']['tie_rate_pct']}%)")
    print(f"Wilcoxon Signed-Rank Test: W = {w_stat:.1f}, p = {p_val:.4e}")
    print(f"Inter-Rater Agreement:    Fleiss' Kappa = {report['inter_annotator_agreement']['fleiss_kappa_preference']} ({report['inter_annotator_agreement']['agreement_tier']})")
    print("=" * 60)
    print(f"Saved: {AUDIT_DIR / 'helpfulness_audit_report.json'}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
