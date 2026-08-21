"""Quick count of refined nodes."""
import json
from pathlib import Path

refined_path = Path(r"D:\KrishokChat Advisory System\backend\ml_assets\rag_index\processed\knowledge_nodes_refined.jsonl")
log_path = Path(r"D:\KrishokChat Advisory System\backend\ml_assets\rag_index\logs\refinement_log.json")

success = 0
errors = 0
total = 0
with open(refined_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        total += 1
        try:
            n = json.loads(line)
            if n.get("error"):
                errors += 1
            else:
                success += 1
        except:
            pass

print(f"Total in file: {total}")
print(f"Success: {success}")
print(f"Error: {errors}")
print(f"Remaining: {2120 - success}")

# Log breakdown
if log_path.exists():
    statuses = {}
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                j = json.loads(line)
                s = j.get("status", "unknown")
                statuses[s] = statuses.get(s, 0) + 1
            except:
                pass
    print(f"\nLog breakdown:")
    for s, c in sorted(statuses.items(), key=lambda x: -x[1]):
        print(f"  {s}: {c}")
