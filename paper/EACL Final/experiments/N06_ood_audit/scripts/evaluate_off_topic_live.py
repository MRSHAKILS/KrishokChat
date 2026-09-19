#!/usr/bin/env python3
"""Evaluate 30 Off-Topic Queries through Live Production NLU (SafetyClassifier with google/gemini-2.5-flash-lite).

Resolves Limitation #17:
Measures the true off-topic refusal rate of the production LLM classification branch
(Tier 1 NLU) on the 30 out-of-domain queries from E09/N06 that were unrefused by the
Tier-0 deterministic precheck (which only checks for emergency/banned pesticides).
"""

from __future__ import annotations

import asyncio
import json
import math
import os
import sys
import threading
import time
from pathlib import Path

import dotenv
import requests

dotenv.load_dotenv()
sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parents[5]
BACKEND_DIR = REPO_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.application.safety import SafetyClassifier
from app.domain.contracts import QueryContext
from app.domain.enums import SafetyCategory
from app.infrastructure.llm.openai_compatible import OpenAICompatibleClient

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_KEY:
    print("[ERROR] Missing OPENROUTER_API_KEY in environment.")
    sys.exit(1)

MODEL_ID = "google/gemini-2.5-flash-lite"
MAX_OUTPUT_TOKENS = 180

RESULTS_DIR = REPO_ROOT / "paper" / "EACL Final" / "experiments" / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
JSONL_OUT = RESULTS_DIR / "n06_off_topic_live_results.jsonl"
SUMMARY_OUT = RESULTS_DIR / "n06_off_topic_live_summary.json"


def preflight_check(api_key: str) -> None:
    """Pre-flight key authorization check (Rule 0.1)."""
    print(f"[PRE-FLIGHT] Testing 1-token authorization on OpenRouter for {MODEL_ID}...")
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "model": MODEL_ID,
        "messages": [{"role": "user", "content": "test"}],
        "max_tokens": 1,
    }
    try:
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10,
        )
        if resp.status_code in (401, 403):
            print(f"[FATAL] Key unauthorized (HTTP {resp.status_code}): {resp.text}")
            sys.exit(1)
        resp.raise_for_status()
        print("[PRE-FLIGHT] Authorization check PASSED (HTTP 200).")
    except Exception as e:
        print(f"[FATAL] Pre-flight check failed: {e}")
        sys.exit(1)


def wilson_interval(successes: int, total: int, confidence: float = 0.95) -> tuple[float, float]:
    """Calculate Wilson score interval."""
    if total == 0:
        return 0.0, 0.0
    z = 1.95996  # 95%
    p = successes / total
    denom = 1 + z**2 / total
    centre = (p + z**2 / (2 * total)) / denom
    spread = z * math.sqrt(p * (1 - p) / total + z**2 / (4 * total**2)) / denom
    return max(0.0, centre - spread), min(1.0, centre + spread)


async def main():
    preflight_check(OPENROUTER_KEY)

    # 1. Load 30 off-topic queries from e09_stratified_evaluation_400.json
    e09_file = REPO_ROOT / "paper" / "EACL Demo" / "experiments" / "E09_slot_disambiguation_gating" / "e09_stratified_evaluation_400.json"
    with open(e09_file, "r", encoding="utf-8") as f:
        e09_data = json.load(f)

    # Filter out prompt injections; keep the 30 off-topic queries
    off_topic_items = [
        d for d in e09_data
        if d.get("category") == "out_of_scope_and_injection"
        and "OVERRIDE" not in d.get("query", "")
        and "HACKED" not in d.get("query", "")
    ]

    print(f"[SETUP] Loaded {len(off_topic_items)} off-topic evaluation queries from {e09_file.name}.")
    assert len(off_topic_items) == 30, f"Expected exactly 30 off-topic queries, got {len(off_topic_items)}"

    # 2. Setup LLM client and SafetyClassifier
    client = OpenAICompatibleClient(
        base_url="https://openrouter.ai/api/v1",
        model=MODEL_ID,
        api_key=OPENROUTER_KEY,
        timeout=30.0,
        temperature=0.0,
        max_output_tokens=MAX_OUTPUT_TOKENS,
    )
    classifier = SafetyClassifier(client)

    # Clear previous results file
    if JSONL_OUT.exists():
        JSONL_OUT.unlink()

    file_lock = threading.Lock()
    results = []

    print(f"[EVAL] Evaluating 30 queries through SafetyClassifier ({MODEL_ID})...\n")

    for idx, item in enumerate(off_topic_items, 1):
        query = item["query"]
        case_id = item["id"]
        context = QueryContext()

        t0 = time.perf_counter()
        decision = await classifier.classify(query, context)
        latency_ms = (time.perf_counter() - t0) * 1000

        is_refusal = decision.category in (SafetyCategory.OFF_TOPIC, SafetyCategory.LOW_CONFIDENCE, SafetyCategory.PROMPT_INJECTION)
        is_off_topic = decision.category == SafetyCategory.OFF_TOPIC

        rec = {
            "id": case_id,
            "query": query,
            "category": decision.category.value,
            "is_refusal": is_refusal,
            "is_off_topic": is_off_topic,
            "reason": decision.reason,
            "confidence": decision.confidence,
            "response": decision.response,
            "latency_ms": round(latency_ms, 2),
        }
        results.append(rec)

        # Immediate durable disk sync (Rule 0.1)
        with file_lock:
            with open(JSONL_OUT, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
                os.fsync(f.fileno())

        print(f"[{idx:02d}/30] ID: {case_id} | Cat: {decision.category.value:<12} | Refusal: {str(is_refusal):<5} | Latency: {latency_ms:.1f}ms | Query: {query}")

    # 3. Compute aggregate statistics
    n_total = len(results)
    n_refused = sum(1 for r in results if r["is_refusal"])
    n_off_topic = sum(1 for r in results if r["is_off_topic"])
    n_safe_agri = sum(1 for r in results if r["category"] == "safe_agri")
    
    ci_low, ci_high = wilson_interval(n_refused, n_total)
    ot_ci_low, ot_ci_high = wilson_interval(n_off_topic, n_total)

    summary = {
        "benchmark_name": "EACL_N06_OFF_TOPIC_LIVE_EVALUATION",
        "model": MODEL_ID,
        "n_queries": n_total,
        "refused_count": n_refused,
        "refusal_rate": round(n_refused / n_total, 4),
        "refusal_rate_pct": round(n_refused / n_total * 100, 2),
        "refusal_wilson_95_ci": [round(ci_low * 100, 2), round(ci_high * 100, 2)],
        "off_topic_exact_count": n_off_topic,
        "off_topic_exact_rate": round(n_off_topic / n_total, 4),
        "off_topic_exact_ci": [round(ot_ci_low * 100, 2), round(ot_ci_high * 100, 2)],
        "safe_agri_fallthrough_count": n_safe_agri,
        "category_breakdown": {
            cat: sum(1 for r in results if r["category"] == cat)
            for cat in set(r["category"] for r in results)
        },
        "query_performance_by_probe": {},
    }

    # Group by distinct probe query
    unique_queries = {}
    for r in results:
        q = r["query"]
        if q not in unique_queries:
            unique_queries[q] = []
        unique_queries[q].append(r)

    for q, rows in unique_queries.items():
        summary["query_performance_by_probe"][q] = {
            "count": len(rows),
            "refused": sum(1 for r in rows if r["is_refusal"]),
            "category": rows[0]["category"],
            "reason": rows[0]["reason"],
        }

    with open(SUMMARY_OUT, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print("EVALUATION SUMMARY")
    print("=" * 80)
    print(f"Total Queries:        {n_total}")
    print(f"Total Refused:        {n_refused} / {n_total} ({summary['refusal_rate_pct']}%) [95% CI: {summary['refusal_wilson_95_ci']}]")
    print(f"Exact Off-Topic:      {n_off_topic} / {n_total} ({round(n_off_topic/n_total*100, 2)}%)")
    print(f"Safe Agri (Weather):  {n_safe_agri} / {n_total} ({round(n_safe_agri/n_total*100, 2)}%)")
    print(f"Breakdown:            {summary['category_breakdown']}")
    print(f"Saved to:             {JSONL_OUT}")
    print(f"Summary to:           {SUMMARY_OUT}")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
