"""Find Category C diseases (no KB, no details)."""
import json, pathlib, sys
sys.path.insert(0, r"D:\KrishokChat Advisory System\backend")
from app.services.advisory._extractors import load_all_crop_classes, HEALTHY, get_disease_details

ROOT = pathlib.Path(r"D:\KrishokChat Advisory System\backend")
MAP_FILE = ROOT / "ml_assets/advisory/disease_knowledge_map.json"
mapping = json.loads(MAP_FILE.read_text(encoding="utf-8"))

print("=== Category C (no KB, no details) ===")
for cls, info in mapping.items():
    if info["category"] == "C":
        print(f"  {cls:40s} crop={info['crop']:10s} disease={info['disease_name']}")

print("\n=== Category B with details but no KB ===")
for cls, info in mapping.items():
    if info["category"] == "B" and info["has_disease_details"] and len(info["rag_node_ids"]) == 0:
        print(f"  {cls:40s} crop={info['crop']:10s} disease={info['disease_name']}")

print("\n=== Category B with KB but no details ===")
for cls, info in mapping.items():
    if info["category"] == "B" and not info["has_disease_details"] and len(info["rag_node_ids"]) > 0:
        print(f"  {cls:40s} crop={info['crop']:10s} disease={info['disease_name']}")
