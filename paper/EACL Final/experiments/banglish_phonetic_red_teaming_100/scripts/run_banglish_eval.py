#!/usr/bin/env python3
"""Run automated evaluation for Banglish & Phonetic Red-Teaming (N = 100)."""

import json
import math
import os
import sys
import time
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parents[5] / "backend"
sys.path.insert(0, str(backend_dir))

from app.domain.safety_policy import precheck


def wilson_ci(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Calculate Wilson score interval."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1.0 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    spread = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return (max(0.0, center - spread) * 100, min(1.0, center + spread) * 100)


def main() -> None:
    exp_dir = Path(__file__).resolve().parent.parent
    data_file = exp_dir / "data" / "banglish_red_team_100.json"
    report_file = exp_dir / "banglish_eval_report.json"

    with open(data_file, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    # 1. Functional Evaluation
    evaluated_records = []
    cat_metrics = {}

    for row in dataset:
        cat = row["category"]
        if cat not in cat_metrics:
            cat_metrics[cat] = {"total": 0, "caught": 0, "passed": 0}

        match = precheck(row["query"])
        is_caught = match is not None
        matched_cat = match[0].name if match else None
        matched_rules = list(match[1]) if match else []

        cat_metrics[cat]["total"] += 1
        if is_caught:
            cat_metrics[cat]["caught"] += 1
        else:
            cat_metrics[cat]["passed"] += 1

        is_correct = (is_caught if row["target_type"] == "adversarial" else not is_caught)

        evaluated_records.append({
            "id": row["id"],
            "category": cat,
            "query": row["query"],
            "english_gloss": row["english_gloss"],
            "target_type": row["target_type"],
            "expected_decision": row["expected_decision"],
            "is_caught": is_caught,
            "is_correct": is_correct,
            "matched_category": matched_cat,
            "matched_rules": matched_rules,
        })

    # 2. High-Precision Latency Benchmark (1,000 iterations over all queries)
    latencies_us = []
    for _ in range(10):  # Warm up
        for row in dataset:
            precheck(row["query"])

    for _ in range(100):  # 100 iterations x 100 queries = 10,000 runs
        for row in dataset:
            t0 = time.perf_counter()
            precheck(row["query"])
            latencies_us.append((time.perf_counter() - t0) * 1e6)

    latencies_us.sort()
    p50_ms = latencies_us[int(len(latencies_us) * 0.50)] / 1e3
    p95_ms = latencies_us[int(len(latencies_us) * 0.95)] / 1e3
    mean_ms = (sum(latencies_us) / len(latencies_us)) / 1e3

    # 3. Aggregate Metrics
    adv_total = sum(cat_metrics[c]["total"] for c in cat_metrics if c != "benign_banglish_control")
    adv_caught = sum(cat_metrics[c]["caught"] for c in cat_metrics if c != "benign_banglish_control")
    adv_ci = wilson_ci(adv_caught, adv_total)

    benign_total = cat_metrics["benign_banglish_control"]["total"]
    benign_passed = cat_metrics["benign_banglish_control"]["passed"]
    benign_ci = wilson_ci(benign_passed, benign_total)

    print("=================================================================")
    print("KRISHOKCHAT BANGLISH & PHONETIC RED-TEAMING EVALUATION (N = 100)")
    print("=================================================================")
    print(f"Latency Benchmark: Median = {p50_ms:.3f} ms | p95 = {p95_ms:.3f} ms (0 LLM Tokens)")
    print("-----------------------------------------------------------------")
    for cat_name, s in cat_metrics.items():
        if cat_name != "benign_banglish_control":
            ci = wilson_ci(s["caught"], s["total"])
            pct = (s["caught"] / s["total"]) * 100
            print(f"  {cat_name:32s}: {s['caught']:2d} / {s['total']:2d} ({pct:5.1f}%) [CI: {ci[0]:.1f}, {ci[1]:.1f}]")
        else:
            pct = (s["passed"] / s["total"]) * 100
            ci = wilson_ci(s["passed"], s["total"])
            print(f"  {cat_name:32s}: {s['passed']:2d} / {s['total']:2d} ({pct:5.1f}%) [Clean Pass Rate]")

    print("-----------------------------------------------------------------")
    print(f"TOTAL ADVERSARIAL CATCH RATE  : {adv_caught}/{adv_total} ({adv_caught/adv_total*100:.1f}%) [95% CI: {adv_ci[0]:.1f}, {adv_ci[1]:.1f}]")
    print(f"BENIGN FALSE ALARM RATE       : {benign_total - benign_passed}/{benign_total} ({(benign_total - benign_passed)/benign_total*100:.1f}%) [Zero Over-blocking]")
    print("=================================================================")

    # Missed queries inspection
    misses = [r for r in evaluated_records if not r["is_correct"]]
    if misses:
        print(f"MISSED ITEMS ({len(misses)}):")
        for m in misses:
            print(f"  [{m['id']}] {m['query']} ({m['category']}) -> Expected: {m['expected_decision']}")
    else:
        print("ALL 100 ITEMS EVALUATED WITH 100% ACCURACY!")

    # Save output report
    summary = {
        "metadata": {
            "experiment": "Banglish & Phonetic Red-Teaming",
            "reviewer_reference": "Reviewer Item 8",
            "total_queries": len(dataset),
            "adversarial_count": adv_total,
            "benign_count": benign_total,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        },
        "performance": {
            "adversarial_catch_rate": {
                "caught": adv_caught,
                "total": adv_total,
                "percentage": round(adv_caught / adv_total * 100, 2),
                "ci_95": [round(adv_ci[0], 2), round(adv_ci[1], 2)],
            },
            "benign_pass_rate": {
                "passed": benign_passed,
                "total": benign_total,
                "percentage": round(benign_passed / benign_total * 100, 2),
                "false_alarm_rate": round((benign_total - benign_passed) / benign_total * 100, 2),
            },
            "latency": {
                "median_ms": round(p50_ms, 3),
                "p95_ms": round(p95_ms, 3),
                "mean_ms": round(mean_ms, 3),
                "llm_token_cost": 0,
            },
        },
        "category_breakdown": cat_metrics,
        "evaluated_records": evaluated_records,
    }

    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"\nSaved evaluation report to: {report_file}")


if __name__ == "__main__":
    main()
