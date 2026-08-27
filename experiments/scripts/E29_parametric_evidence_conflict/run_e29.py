#!/usr/bin/env python3
"""
experiments/scripts/E29_parametric_evidence_conflict/run_e29.py
Canonical runner script for Layer E29 under experiments/scripts/.
"""

import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
CEA_E29_SCRIPT = WORKSPACE_ROOT / "paper" / "CEA Paper" / "experiments" / "E29_parametric_evidence_conflict" / "scripts" / "run_e29_parametric_eval.py"

if __name__ == "__main__":
    import subprocess
    sys.exit(subprocess.call([sys.executable, str(CEA_E29_SCRIPT)]))
