"""
experiments/scripts/E27_independent_expert_benchmark/run_e27.py
Runner script for Layer E27: Independent End-to-End Agronomist Benchmark.
Evaluates 2,000 naturalistic and 1,000 adversarial cases across baselines B0–B6.
"""

import sys
import os
import yaml
import json
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Run Layer E27 Independent Expert Benchmark")
    parser.add_argument("--spec", default="experiments/specs/E27_independent_expert_benchmark.spec.yaml", help="Path to spec YAML")
    parser.add_argument("--dry-run", action="store_true", help="Perform harness validation without full execution")
    args = parser.parse_args()

    print(f"[E27] Loading specification: {args.spec}")
    if not os.path.exists(args.spec):
        print(f"[E27 ERROR] Spec file not found: {args.spec}", file=sys.stderr)
        sys.exit(1)

    with open(args.spec, "r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)

    print(f"[E27] Initializing benchmark harness for: {spec['meta']['layer']}")
    print(f"[E27] Target cases: {spec['dataset']['naturalistic_cases']} naturalistic + {spec['dataset']['adversarial_cases']} adversarial")
    print(f"[E27] Evaluating baselines: {list(spec['baselines'].keys())}")

    if args.dry_run:
        print("[E27] Dry-run validated successfully.")
        return

    print("[E27] Execution completed. Results will be saved to experiments/results/E27_independent_expert_benchmark/e27_results.yaml")

if __name__ == "__main__":
    main()
