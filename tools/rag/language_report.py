"""Analyze language distribution in cleaned knowledge nodes."""
import json
from pathlib import Path

nodes_path = Path(__file__).resolve().parent.parent / "processed" / "knowledge_nodes_clean.jsonl"

nodes = []
with open(nodes_path, "r", encoding="utf-8") as f:
    for line in f:
        nodes.append(json.loads(line))

total = len(nodes)
has_bn = 0
has_en = 0
both = 0
neither = 0
bn_only = 0
en_only = 0

bn_chars_total = 0
en_chars_total = 0

en_only_nodes = []

for n in nodes:
    bn = n.get("content_bn", "").strip()
    en = n.get("content_en", "").strip()
    has_bn_bool = len(bn) > 10
    has_en_bool = len(en) > 10

    if has_bn_bool:
        has_bn += 1
        bn_chars_total += len(bn)
    if has_en_bool:
        has_en += 1
        en_chars_total += len(en)
    if has_bn_bool and has_en_bool:
        both += 1
    if not has_bn_bool and not has_en_bool:
        neither += 1
    if has_bn_bool and not has_en_bool:
        bn_only += 1
    if not has_bn_bool and has_en_bool:
        en_only += 1
        en_only_nodes.append(n)

print("=" * 60)
print("KNOWLEDGE NODES LANGUAGE REPORT")
print("=" * 60)
print(f"Total nodes: {total}")
print()
print(f"Has Bengali content (>10 chars):  {has_bn:5d}  ({has_bn/total*100:.1f}%)")
print(f"Has English content (>10 chars):  {has_en:5d}  ({has_en/total*100:.1f}%)")
print(f"Has BOTH languages:               {both:5d}  ({both/total*100:.1f}%)")
print(f"Bengali ONLY (no English):        {bn_only:5d}  ({bn_only/total*100:.1f}%)")
print(f"English ONLY (no Bengali):        {en_only:5d}  ({en_only/total*100:.1f}%)")
print(f"NEITHER (empty):                  {neither:5d}  ({neither/total*100:.1f}%)")
print()
print(f"Total Bengali characters: {bn_chars_total:,}")
print(f"Total English characters: {en_chars_total:,}")
print(f"Bengali/English ratio: {bn_chars_total/max(en_chars_total,1):.2f}x")
print()
print(f"Nodes needing translation (English only): {en_only}")
print()
print("SAMPLE NODES NEEDING TRANSLATION:")
for n in en_only_nodes[:15]:
    title = n.get("title_en", "")[:80]
    en_preview = n.get("content_en", "")[:120]
    print(f"  [{n['id']}] {title}")
    print(f"      EN: {en_preview}...")
    print()
