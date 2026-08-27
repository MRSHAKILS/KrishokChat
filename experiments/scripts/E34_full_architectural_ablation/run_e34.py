#!/usr/bin/env python3
"""
experiments/scripts/E34_full_architectural_ablation/run_e34.py
Canonical runner script for Layer E34 under experiments/scripts/.
"""

import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
CEA_E34_SCRIPT = WORKSPACE_ROOT / "paper" / "CEA Paper" / "experiments" / "E34_full_architectural_ablation" / "scripts" / "run_e34_ablation_eval.py"

if __name__ == "__main__":
    import subprocess
    sys.exit(subprocess.call([sys.executable, str(CEA_E34_SCRIPT)]))
