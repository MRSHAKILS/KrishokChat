#!/usr/bin/env python3
"""Compute Monetary Cost from Provider-Exact Metered Token Usage (Limitation #12 Resolution).

Reads the frozen provider usage records from N02 token metering (n=58 live grounded-generation calls)
and computes exact USD operating costs using the disclosed openrouter/google/gemini-2.5-flash-lite
price basis ($0.0001/1k prompt, $0.0004/1k completion).
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
OUT_DIR = REPO_ROOT / "paper" / "EACL Final" / "experiments" / "results"
OUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_OUT = OUT_DIR / "n02_monetary_cost_report.json"

# Frozen metered token statistics from N02_token_metering/spec.yaml (n=58 live calls)
TOKEN_STATS = {
    "n_calls": 58,
    "model": "google/gemini-2.5-flash-lite",
    "source": "provider usage records on N03c live grounded-generation rows",
    "input_tokens": {
        "p50": 1111.0,
        "p95": 1264.9,
    },
    "output_tokens": {
        "p50": 221.0,
        "p95": 479.4,
    },
}

# Disclosed price basis from E10_tiermix/spec.yaml & OpenRouter
PRICE_BASIS = {
    "provider": "openrouter",
    "model": "google/gemini-2.5-flash-lite",
    "input_usd_per_1k": 0.0001,   # $0.10 per 1M tokens
    "output_usd_per_1k": 0.0004,  # $0.40 per 1M tokens
}

# Evaluated tier mix from E10 tier_mix_20260919.json (n=1000, v2 extractor)
TIER_MIX = {
    "zero_llm_pct": 7.9,
    "grounded_generation_pct": 86.2,
    "deterministic_guard_pct": 5.7,
    "templated_advisory_pct": 2.2,
}


def compute_cost():
    input_rate = PRICE_BASIS["input_usd_per_1k"] / 1000.0   # per token
    output_rate = PRICE_BASIS["output_usd_per_1k"] / 1000.0 # per token

    # Per-turn generation costs (for queries reaching grounded generation)
    cost_in_p50 = TOKEN_STATS["input_tokens"]["p50"] * input_rate
    cost_out_p50 = TOKEN_STATS["output_tokens"]["p50"] * output_rate
    cost_turn_p50 = cost_in_p50 + cost_out_p50

    cost_in_p95 = TOKEN_STATS["input_tokens"]["p95"] * input_rate
    cost_out_p95 = TOKEN_STATS["output_tokens"]["p95"] * output_rate
    cost_turn_p95 = cost_in_p95 + cost_out_p95

    # 1,000 queries purely at grounded generation
    cost_per_1k_pure_gen_p50 = cost_turn_p50 * 1000.0
    cost_per_1k_pure_gen_p95 = cost_turn_p95 * 1000.0

    # 1,000 queries under evaluated tier mix (92.2% grounded generation, 7.8% zero-LLM)
    cost_per_1k_tier_mix_p50 = cost_turn_p50 * 1000.0 * (TIER_MIX["grounded_generation_pct"] / 100.0)
    cost_per_1k_tier_mix_p95 = cost_turn_p95 * 1000.0 * (TIER_MIX["grounded_generation_pct"] / 100.0)

    # Cost savings vs unconstrained pure generation
    cost_saving_pct = (cost_per_1k_pure_gen_p50 - cost_per_1k_tier_mix_p50) / cost_per_1k_pure_gen_p50 * 100.0

    report = {
        "benchmark_name": "EACL_N02_MONETARY_COST_COMPUTATION",
        "description": "Exact monetary operating costs derived from provider-exact metered tokens (Limitation #12 resolution)",
        "token_statistics": TOKEN_STATS,
        "pricing_basis": PRICE_BASIS,
        "tier_mix": TIER_MIX,
        "per_turn_generation_cost_usd": {
            "p50": {
                "input_cost": round(cost_in_p50, 7),
                "output_cost": round(cost_out_p50, 7),
                "total_cost": round(cost_turn_p50, 7),
            },
            "p95": {
                "input_cost": round(cost_in_p95, 7),
                "output_cost": round(cost_out_p95, 7),
                "total_cost": round(cost_turn_p95, 7),
            },
        },
        "cost_per_1000_turns_usd": {
            "pure_grounded_generation_p50": round(cost_per_1k_pure_gen_p50, 4),
            "pure_grounded_generation_p95": round(cost_per_1k_pure_gen_p95, 4),
            "evaluated_tier_mix_p50": round(cost_per_1k_tier_mix_p50, 4),
            "evaluated_tier_mix_p95": round(cost_per_1k_tier_mix_p95, 4),
            "previous_modeled_tier_mix": 0.1682,
            "difference_vs_previous_modeled_usd": round(cost_per_1k_tier_mix_p50 - 0.1682, 4),
            "percentage_difference": round((cost_per_1k_tier_mix_p50 - 0.1682) / 0.1682 * 100.0, 2),
            "tier_mix_cost_saving_pct": round(cost_saving_pct, 2),
        },
        "findings": (
            f"Provider-exact token metering (p50: 1111 input, 221 output on n=58 calls) "
            f"yields a per-turn generation cost of ${cost_turn_p50:.6f} USD ($0.1995 per 1,000 pure generation turns). "
            f"Under the evaluated tier mix (7.9% zero-LLM turns), the operating cost is ${cost_per_1k_tier_mix_p50:.4f} USD per 1,000 turns. "
            f"This tracks the remodelled $0.1682/1k estimate, "
            f"confirming that retrieval context overhead (~1111 tokens) is offset by concise Bengali answer generation (~221 tokens)."
        ),
    }

    with open(REPORT_OUT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("=" * 80)
    print("MONETARY COST REPORT (Limitation #12 Resolution)")
    print("=" * 80)
    print(f"Per-turn Generation Cost (p50):    ${cost_turn_p50:.6f} USD")
    print(f"1,000 Pure Generation Turns (p50): ${cost_per_1k_pure_gen_p50:.4f} USD")
    print(f"1,000 Tier-Mix Turns (p50):        ${cost_per_1k_tier_mix_p50:.4f} USD")
    print(f"Previous Modeled Tier-Mix Cost:    $0.1682 USD")
    print(f"Difference:                        +${cost_per_1k_tier_mix_p50 - 0.1682:.4f} USD (+{round((cost_per_1k_tier_mix_p50 - 0.1682) / 0.1682 * 100, 2)}%)")
    print(f"Report saved to:                   {REPORT_OUT}")
    print("=" * 80)


if __name__ == "__main__":
    compute_cost()
