"""Analyze refined nodes quality."""
import json
from pathlib import Path

refined_path = Path(r"D:\KrishokChat Advisory System\backend\ml_assets\rag_index\processed\knowledge_nodes_refined.jsonl")

nodes = []
with open(refined_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            try:
                nodes.append(json.loads(line))
            except:
                pass

success = [n for n in nodes if not n.get("error")]
errors = [n for n in nodes if n.get("error")]

print(f"Total records: {len(nodes)}")
print(f"Success: {len(success)}")
print(f"Error: {len(errors)}")
print()

# Quality of successful nodes
title_bn_filled = sum(1 for n in success if n.get("title_bn", "").strip())
content_bn_filled = sum(1 for n in success if n.get("content_bn", "").strip())
key_points_filled = sum(1 for n in success if n.get("key_points"))
tags_filled = sum(1 for n in success if n.get("tags"))
safety_filled = sum(1 for n in success if n.get("safety_notes", "").strip())

print("Field completion (successful nodes):")
print(f"  title_bn: {title_bn_filled}/{len(success)} ({title_bn_filled/len(success)*100:.0f}%)")
print(f"  content_bn: {content_bn_filled}/{len(success)} ({content_bn_filled/len(success)*100:.0f}%)")
print(f"  key_points: {key_points_filled}/{len(success)} ({key_points_filled/len(success)*100:.0f}%)")
print(f"  tags: {tags_filled}/{len(success)} ({tags_filled/len(success)*100:.0f}%)")
print(f"  safety_notes: {safety_filled}/{len(success)} ({safety_filled/len(success)*100:.0f}%)")
print()

# Content length distribution
lengths = [len(n.get("content_bn", "")) for n in success]
import statistics
print(f"Content BN length: min={min(lengths)}, max={max(lengths)}, avg={statistics.mean(lengths):.0f}, median={statistics.median(lengths):.0f}")
print()

# Show 3 examples
print("=" * 60)
print("SAMPLE REFINED NODES")
print("=" * 60)
for n in success[-3:]:
    print(f"ID: {n['id']}")
    print(f"title_bn: {n.get('title_bn', '')[:80]}")
    print(f"content_bn ({len(n.get('content_bn', ''))} chars): {n.get('content_bn', '')[:200]}...")
    print(f"key_points: {n.get('key_points', [])}")
    print()
