#!/usr/bin/env python3
"""
experiments/scripts/E27_independent_expert_benchmark/run_e27.py
Canonical runner script for Layer E27 under experiments/scripts/.
"""

import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
CEA_E27_SCRIPT = WORKSPACE_ROOT / "paper" / "CEA Paper" / "experiments" / "E27_independent_expert_benchmark" / "scripts" / "run_e27_benchmark_eval.py"

if __name__ == "__main__":
    import subprocess
    sys.exit(subprocess.call([sys.executable, str(CEA_E27_SCRIPT)]))
