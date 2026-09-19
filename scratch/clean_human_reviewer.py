import os
import re
import shutil
from pathlib import Path

target_dir = Path("paper/EACL Final/experiments/human_reviewer")

for p in (target_dir / "scripts").glob("*.py"):
    with open(p, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = r'BASE_DIR\s*=\s*r?["\'].*?human_reviewer["\']'
    if re.search(pattern, content):
        content = re.sub(pattern, 'from pathlib import Path\nBASE_DIR = str(Path(__file__).resolve().parent.parent)', content)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {p.name}")

dup = target_dir / "multi_reviewer_evaluation_report.json"
if dup.exists():
    dup.unlink()
    print("Removed duplicate report.")

pycache = target_dir / "scripts" / "__pycache__"
if pycache.exists():
    shutil.rmtree(pycache)
    print("Removed pycache.")

print("Done cleaning human_reviewer directory.")
