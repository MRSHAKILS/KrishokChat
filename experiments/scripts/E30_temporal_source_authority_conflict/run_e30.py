#!/usr/bin/env python3
"""
experiments/scripts/E30_temporal_source_authority_conflict/run_e30.py
Canonical runner script for Layer E30 under experiments/scripts/.
"""

import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
CEA_E30_SCRIPT = WORKSPACE_ROOT / "paper" / "CEA Paper" / "experiments" / "E30_temporal_source_authority_conflict" / "scripts" / "run_e30_temporal_eval.py"

if __name__ == "__main__":
    import subprocess
    sys.exit(subprocess.call([sys.executable, str(CEA_E30_SCRIPT)]))
