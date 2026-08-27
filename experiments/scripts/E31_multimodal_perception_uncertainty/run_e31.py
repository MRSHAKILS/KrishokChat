#!/usr/bin/env python3
"""
experiments/scripts/E31_multimodal_perception_uncertainty/run_e31.py
Canonical runner script for Layer E31 under experiments/scripts/.
"""

import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
CEA_E31_SCRIPT = WORKSPACE_ROOT / "paper" / "CEA Paper" / "experiments" / "E31_multimodal_perception_uncertainty" / "scripts" / "run_e31_multimodal_eval.py"

if __name__ == "__main__":
    import subprocess
    sys.exit(subprocess.call([sys.executable, str(CEA_E31_SCRIPT)]))
