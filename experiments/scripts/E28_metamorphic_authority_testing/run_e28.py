#!/usr/bin/env python3
"""
experiments/scripts/E28_metamorphic_authority_testing/run_e28.py
Canonical runner script for Layer E28 under experiments/scripts/.
"""

import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
CEA_E28_SCRIPT = WORKSPACE_ROOT / "paper" / "CEA Paper" / "experiments" / "E28_metamorphic_authority_testing" / "scripts" / "run_e28_metamorphic_eval.py"

if __name__ == "__main__":
    import subprocess
    sys.exit(subprocess.call([sys.executable, str(CEA_E28_SCRIPT)]))
