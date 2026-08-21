"""Show 3 random node examples from treatment and general categories."""
import json
import random
from pathlib import Path

random.seed(42)

nodes_path = Path(__file__).resolve().parent.parent / "processed" / "knowledge_nodes_clean.jsonl"

nodes = []
with open(nodes_path, "r", encoding="utf-8") as f:
    for line in f:
        nodes.append(json.loads(line))

# Filter by category
treatment = [n for n in nodes if n.get("category") == "treatment"]
general = [n for n in nodes if n.get("category") == "general"]
disease = [n for n in nodes if n.get("category") == "disease"]
pest = [n for n in nodes if n.get("category") == "pest"]

print(f"Category counts: treatment={len(treatment)}, general={len(general)}, disease={len(disease)}, pest={len(pest)}")
print()

# Pick random from each
samples = []
if treatment:
    samples.append(("TREATMENT", random.choice(treatment)))
if general:
    samples.append(("GENERAL", random.choice(general)))
if disease:
    samples.append(("DISEASE", random.choice(disease)))
if pest:
    samples.append(("PEST", random.choice(pest)))

# Add one more random
samples.append(("RANDOM", random.choice(nodes)))

for label, node in samples:
    print("=" * 70)
    print(f"[{label}] {node['id']}")
    print(f"Category: {node.get('category', 'N/A')}")
    print(f"Publisher: {node.get('publisher', 'N/A')}")
    print()
    print(f"title_bn: {node.get('title_bn', '(empty)')[:100]}")
    print(f"title_en: {node.get('title_en', '(empty)')[:100]}")
    print()
    print(f"summary: {node.get('summary', '(empty)')[:200]}")
    print()
    content_bn = node.get("content_bn", "")
    print(f"content_bn ({len(content_bn)} chars):")
    print(content_bn[:400])
    print()
    content_en = node.get("content_en", "")
    print(f"content_en ({len(content_en)} chars):")
    print(content_en[:300] if content_en else "(empty)")
    print()
    print(f"tags: {node.get('tags', [])}")
    print(f"source: {node.get('source_document', 'N/A')}")
    print()
