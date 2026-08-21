"""
Master Preprocessing Runner
============================
Runs all Step 0 scripts in sequence.

Usage (from dataset/scripts/):
    python run_preprocessing.py

Or from project root:
    python dataset/scripts/run_preprocessing.py
"""

import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

STEPS = [
    ("Step 0a: Parse & Validate", "preprocess_step0.py"),
    ("Step 0b: Normalize Filenames", "normalize_filenames_step0b.py"),
    ("Step 0c: Extract EXIF", "extract_exif_step0c.py"),
    ("Step 0d: Plan Train/Val/Test Split", "split_planner_step0d.py"),
]


def main():
    print("SOIL MOISTURE DETECTION - PREPROCESSING PIPELINE")
    print("=" * 60)

    for name, script in STEPS:
        print(f"\n{'=' * 60}")
        print(f"  RUNNING: {name}")
        print(f"{'=' * 60}\n")

        script_path = SCRIPT_DIR / script
        if not script_path.exists():
            print(f"  ERROR: {script_path} not found!")
            sys.exit(1)

        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(SCRIPT_DIR),
            capture_output=False,
        )
        if result.returncode != 0:
            print(f"\n  FAILED: {name}")
            sys.exit(1)
        print(f"\n  DONE: {name}")

    print(f"\n{'=' * 60}")
    print(f"  ALL STEPS COMPLETED")
    print(f"{'=' * 60}")
    print(f"  Dataset ready at: {SCRIPT_DIR.parent}")


if __name__ == "__main__":
    main()
