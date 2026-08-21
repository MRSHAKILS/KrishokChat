"""Count and show examples."""
import json
from pathlib import Path

refined_path = Path(r"D:\KrishokChat Advisory System\backend\ml_assets\rag_index\processed\knowledge_nodes_refined.jsonl")

nodes = []
with open(refined_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            n = json.loads(line)
            if n.get("content_bn") and not n.get("error"):
                nodes.append(n)
        except:
            pass

print(f"Successfully refined: {len(nodes)} / 2120 ({len(nodes)/2120*100:.1f}%)")
print(f"Remaining: {2120 - len(nodes)}")
print()

# Show 3 diverse examples
examples = []
# Pick from different categories
cats_seen = set()
for n in nodes:
    cat = n.get("category", "unknown")
    if cat not in cats_seen and len(examples) < 3:
        examples.append(n)
        cats_seen.add(cat)

# If not enough, add more
if len(examples) < 3:
    for n in nodes:
        if n not in examples:
            examples.append(n)
            if len(examples) >= 3:
                break

for i, n in enumerate(examples):
    print("=" * 70)
    print(f"EXAMPLE {i+1}: {n['id']}")
    print(f"Category: {n.get('category')} | Publisher: {n.get('publisher')}")
    print("=" * 70)
    print(f"title_bn: {n.get('title_bn', '')}")
    print(f"title_en: {n.get('title_en', '')}")
    print()
    print(f"summary: {n.get('summary', '')}")
    print()
    print(f"natural_intro_bn: {n.get('natural_intro_bn', '')}")
    print()
    content = n.get("content_bn", "")
    print(f"content_bn ({len(content)} chars):")
    print(content[:600])
    print("...")
    print()
    print(f"key_points: {n.get('key_points', [])}")
    print(f"tags: {n.get('tags', [])}")
    safety = n.get("safety_notes", "")
    if safety:
        print(f"safety_notes: {safety}")
    print()
