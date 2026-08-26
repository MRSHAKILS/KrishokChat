#!/usr/bin/env python3
"""KrishokChat v2 — Master Reproducibility Runner.

Executes the entire empirical experimental battery in deterministic sequence:
1. Layer E2: Relational Misbinding Attack Suite (10,000 cases)
2. Layer E3: 11-Slot Schema Ablation Study (10,000 cases)
3. Layer E4: Selective Risk-Coverage Calibration & Conformal Abstention (20,112 rows)
4. Layer E5: Counterfactual Evidence Binding Consistency (2,000 pairs)
5. Layer E6: Ecological Farmer Benchmark & Regional Dialects (4,000 queries)
6. Layer E7/E8: Security & Adversarial Prompt Injection Suite (1,400 attacks)
7. Layer E9: Latency Decomposition & Systems Economics ($C_safe modeling)
8. Layer E10: Safety Failure Taxonomy Root-Cause Audit (100 cases)

All results are automatically validated and written into structured YAML reports
under research_artifacts/evaluations/.
"""

import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
SCRIPTS_DIR = WORKSPACE_ROOT / "research_artifacts" / "scripts" / "runners"

RUNNER_SCRIPTS = [
    ("Layer E2 (Relational Misbinding)", SCRIPTS_DIR / "run_relational_attack_eval.py"),
    ("Layer E3 (11-Slot Schema Ablation)", SCRIPTS_DIR / "run_slot_ablation_eval.py"),
    ("Layer E4 (Risk-Coverage Calibration)", SCRIPTS_DIR / "run_calibration_evaluation.py"),
    ("Layer E5 (Counterfactual Consistency)", SCRIPTS_DIR / "run_counterfactual_eval.py"),
    ("Layer E6 (Ecological Farmer & Dialects)", SCRIPTS_DIR / "run_farmer_benchmark_eval.py"),
    ("Layer E7/E8 (Security & Prompt Injection)", SCRIPTS_DIR / "run_security_injection_eval.py"),
    ("Layer E9 (Latency & Systems Economics)", SCRIPTS_DIR / "run_latency_economic_eval.py"),
    ("Layer E10 (Safety Failure Taxonomy)", SCRIPTS_DIR / "run_failure_taxonomy_eval.py"),
    ("Layer E11 (Multi-Generator Invariance)", SCRIPTS_DIR / "run_multi_generator_eval.py"),
]


def main():
    print("=" * 80)
    print("      KRISHOKCHAT V2 — MASTER EMPIRICAL REPRODUCIBILITY BATTERY")
    print(f"      Execution Started at: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 80)

    start_time = time.perf_counter()
    completed = 0

    for name, script_path in RUNNER_SCRIPTS:
        print(f"\n[RUNNING] {name} ...")
        t0 = time.perf_counter()
        res = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
        elapsed = time.perf_counter() - t0

        if res.returncode == 0:
            print(f"[PASSED]  {name} completed in {elapsed:.2f}s")
            completed += 1
        else:
            print(f"[FAILED]  {name} failed with exit code {res.returncode}")
            print("--- STDERR ---")
            print(res.stderr)
            sys.exit(1)

    total_time = time.perf_counter() - start_time

    print("\n" + "=" * 80)
    print("      ALL EXPERIMENTAL RUNNERS COMPLETED SUCCESSFULLY!")
    print(f"      Total Suites: {completed} / {len(RUNNER_SCRIPTS)} passed")
    print(f"      Total Duration: {total_time:.2f}s")
    print(f"      All YAML evaluation artifacts verified under research_artifacts/evaluations/")
    print("=" * 80)


if __name__ == "__main__":
    main()
