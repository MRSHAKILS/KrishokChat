"""Verify merged knowledge nodes."""
import pickle
import pathlib

ROOT = pathlib.Path(r"D:\KrishokChat Advisory System\backend")
INDEX_FILE = ROOT / "ml_assets/rag_index/indexes/bm25_index.pkl"
MAP_FILE = ROOT / "ml_assets/advisory/disease_knowledge_map.json"

with open(INDEX_FILE, "rb") as f:
    data = pickle.load(f)
print(f"Total nodes: {len(data['nodes'])}")

check_ids = [
    "GEN_WHEAT_BlackPoint",
    "GEN_RICE_Healthy_Leaf",
    "GEN_BRASSICA_Cabbage_Healthy_Leaf",
]
for nid in check_ids:
    found = [n for n in data["nodes"] if n["id"] == nid]
    if found:
        n = found[0]
        has_treatment = bool(n.get("treatment_summary_bn"))
        print(f"  {nid}: treatment={has_treatment} tags={n.get('tags', [])[:3]}")
    else:
        print(f"  {nid}: NOT FOUND")

# Check Category counts
import json
mapping = json.loads(MAP_FILE.read_text(encoding="utf-8"))
cats = {"A": 0, "B": 0, "C": 0}
for info in mapping.values():
    cats[info["category"]] += 1
print(f"\nCategory counts: {cats}")
