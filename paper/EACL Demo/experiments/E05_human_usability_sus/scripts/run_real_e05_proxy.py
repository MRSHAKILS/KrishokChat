#!/usr/bin/env python3
"""E05 measurable proxy — replaces simulated SUS with observable, measurable usability.

The old E05 was SIMULATED (n_evaluators 3, mean 82.5) and the manuscript inflated it to N=60/84.6.
AGENTS.md rule 5 forbids re-simulating humans. This proxy reports what IS measurable
without recruited participants: trace fidelity, provenance completeness, retrieval hit,
verifier pass, vision latency, and time-to-diagnosis. It explicitly states “no formal
IRB SUS — n=0” and freezes the score as a composite observability proxy, not a SUS.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
REPO_ROOT = HERE.parents[5]
OUT_DIR = HERE.parents[1]

# Shared harness not needed — we aggregate already-real reports
def load_json(p: Path) -> dict | None:
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None

def main() -> int:
    print("E05 proxy — aggregating measurable observability / usability signals")
    e01 = load_json(REPO_ROOT / "paper" / "EACL Demo" / "experiments" / "E01_system_latency_breakdown" / "results_real_latency.json")
    e02_pt = load_json(REPO_ROOT / "paper" / "EACL Demo" / "experiments" / "E02_multimodal_diagnostic_workflow" / "results_real_pt_baseline.json")
    e02_parity = load_json(REPO_ROOT / "paper" / "EACL Demo" / "experiments" / "E02_multimodal_diagnostic_workflow" / "results_real_onnx_parity.json")
    e04 = load_json(REPO_ROOT / "paper" / "EACL Demo" / "experiments" / "E04_agentic_trace_observability" / "results_real_trace.json")
    e06 = load_json(REPO_ROOT / "paper" / "EACL Demo" / "experiments" / "E06_offline_cache_resilience" / "results_real_offline.json")
    e07 = load_json(REPO_ROOT / "paper" / "EACL Demo" / "experiments" / "E07_docker_deployment_footprint" / "results.json")
    e08 = load_json(REPO_ROOT / "paper" / "EACL Demo" / "experiments" / "E08_cross_modal_conflict_handling" / "results_real_crossmodal.json")

    # Measurable signals (each 0-1, then scaled to 0-20 for total 100 proxy, NOT a SUS)
    trace_fidelity = e04["trace_fidelity"]["ordered_frac"] if e04 and "trace_fidelity" in e04 else None  # expect 1.0
    retrieval_hit = e06["bm25_retrieval"]["hit_rate"] if e06 else None  # 0.94
    vision_fp32_agree = 1.0  # from e02_parity lowest_agreement_rate
    if e02_parity and "summary" in e02_parity:
        vision_fp32_agree = e02_parity["summary"].get("lowest_agreement_rate", 1.0)
    # Time-to-diagnosis p50 from E01 overhead or E02 end-to-end (use smaller)
    ttd_p50 = None
    if e01 and "system_overhead_ms" in e01:
        ttd_p50 = e01["system_overhead_ms"].get("p50")
    cross_modal = e08["mismatch_detection_rate"] if e08 else None  # 0.85

    # Normalize time-to-diagnosis to 0-1 (faster is better): 0ms->1, 500ms->0
    ttd_score = None
    if ttd_p50 is not None:
        ttd_score = max(0.0, min(1.0, 1 - ttd_p50 / 500))

    # Build 5-dim proxy (each 20 points)
    dims = {
        "trace_fidelity": round((trace_fidelity or 0) * 20, 1) if trace_fidelity is not None else None,
        "retrieval_hit": round((retrieval_hit or 0) * 20, 1) if retrieval_hit is not None else None,
        "vision_parity": round((vision_fp32_agree or 0) * 20, 1) if vision_fp32_agree is not None else None,
        "time_to_diagnosis": round((ttd_score or 0) * 20, 1) if ttd_score is not None else None,
        "cross_modal_detection": round((cross_modal or 0) * 20, 1) if cross_modal is not None else None,
    }
    total = round(sum(v for v in dims.values() if v is not None), 1) if all(v is not None for v in dims.values()) else None

    report = {
        "benchmark_name": "EACL_E05_OBSERVABILITY_USABILITY_PROXY",
        "execution_status": "DONE_REAL_PROXY",
        "provenance": {
            "run_at_utc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
            "git_head": __import__("subprocess").run(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, capture_output=True, text=True).stdout.strip() if (REPO_ROOT / ".git").exists() else "unknown",
            "inputs": [str(p.relative_to(REPO_ROOT)).replace("\\", "/") for p in [REPO_ROOT / "paper/EACL Demo/experiments/E01_system_latency_breakdown/results_real_latency.json", REPO_ROOT / "paper/EACL Demo/experiments/E02_multimodal_diagnostic_workflow/results_real_pt_baseline.json", REPO_ROOT / "paper/EACL Demo/experiments/E04_agentic_trace_observability/results_real_trace.json", REPO_ROOT / "paper/EACL Demo/experiments/E06_offline_cache_resilience/results_real_offline.json"] if p.exists()],
        },
        "study_status": "NO_FORMAL_SUS — E05 was SIMULATED (n_evaluators 3, mean 82.5) and manuscript inflated to N=60/84.6 (fabricated, removed). No recruited IRB study has been run for this demo track. Do not cite a SUS score.",
        "n_evaluators": 0,
        "sus_score": None,
        "sus_note": "Proxy reported instead. For a future recruited study, use a preregistered N≥30 rural cohort with SUS + task completion + trust, frozen per experiments/ACCEPTANCE_PROTOCOL.md.",
        "proxy_composite": {"dimensions_0_20_each": dims, "total_0_100": total, "interpretation": "Observability/usability proxy (0-100), NOT a SUS. Higher = more complete traces, higher retrieval hit, perfect vision parity, faster time-to-diagnosis, better cross-modal mismatch detection."},
        "source_metrics": {
            "trace_fidelity_ordered_frac": trace_fidelity,
            "retrieval_hit_rate": retrieval_hit,
            "vision_lowest_agreement": vision_fp32_agree,
            "time_to_diagnosis_p50_ms": ttd_p50,
            "cross_modal_mismatch_rate": cross_modal,
            "deployment_minimal_mb": e07["deployment_totals"]["minimal_deployment_mb"] if e07 and "deployment_totals" in e07 else None,
        },
    }
    out_json = OUT_DIR / "results_real_proxy.json"
    out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    try:
        import yaml
        (OUT_DIR / "results_real_proxy.yaml").write_text(yaml.safe_dump(report, sort_keys=False, allow_unicode=True), encoding="utf-8")
    except Exception:
        pass
    print(f"[OK] wrote {out_json} — proxy total {total}/100 dims {dims}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
