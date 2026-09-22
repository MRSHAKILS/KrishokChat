#!/usr/bin/env python3
"""KrishokChat E2E Test Runner Forwarder.

Forwards directly to tests/e2e/run_e2e.py while maintaining backward-compatibility.
"""

import sys
from pathlib import Path

# Add e2e folder and execute e2e runner
e2e_runner = Path(__file__).parent / "e2e" / "run_e2e.py"
if __name__ == "__main__":
    with open(e2e_runner, "r", encoding="utf-8") as f:
        code = compile(f.read(), str(e2e_runner), "exec")
        # Set __file__ to the target runner so CORPUS_PATH resolves correctly
        globs = {"__file__": str(e2e_runner), "__name__": "__main__"}
        exec(code, globs)
