"""Quick count."""
import json
from pathlib import Path

refined_path = Path(r"D:\KrishokChat Advisory System\backend\ml_assets\rag_index\processed\knowledge_nodes_refined.jsonl")

total = 0
success = 0
with open(refined_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        total += 1
        try:
            n = json.loads(line)
            if n.get("content_bn") and not n.get("error"):
                success += 1
        except:
            pass

print(f"Total records: {total}")
print(f"Successful: {success}")
print(f"Remaining: {2120 - success}")
print(f"Progress: {success/2120*100:.1f}%")
