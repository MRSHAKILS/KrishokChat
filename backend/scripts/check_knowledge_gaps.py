"""Check knowledge gaps and prepare generation tasks."""
import json
import pathlib
import sys

sys.path.insert(0, r"D:\KrishokChat Advisory System\backend")
from app.services.advisory._extractors import load_all_crop_classes, HEALTHY, get_disease_details, load_rag_nodes, get_rag_node

ROOT = pathlib.Path(r"D:\KrishokChat Advisory System\backend")
MAP_FILE = ROOT / "ml_assets/advisory/disease_knowledge_map.json"

mapping = json.loads(MAP_FILE.read_text(encoding="utf-8"))
nodes = load_rag_nodes()


def main():
    needs_generation = []
    for cls, info in mapping.items():
        if info["category"] != "B":
            continue
        has_rag = len(info["rag_node_ids"]) > 0
        has_details = info["has_disease_details"]

        details = get_disease_details(info["crop"], info["disease_name"])
        rag_node = get_rag_node(info["rag_node_ids"][0], nodes) if has_rag else None

        needs_generation.append({
            "class": cls,
            "crop": info["crop"],
            "disease": info["disease_name"],
            "has_rag": has_rag,
            "has_details": has_details,
            "needs": "rag_node" if not has_rag else ("details" if not has_details else "enrich"),
            "details_content": details,
            "rag_content": rag_node,
        })

    print(f"Category B diseases needing generation: {len(needs_generation)}")
    for item in needs_generation:
        has_desc = bool(item["details_content"] and item["details_content"].get("description_bn"))
        has_sol = bool(item["details_content"] and item["details_content"].get("solution_bn"))
        rag_has_content = bool(item["rag_content"] and item["rag_content"].get("content_en"))
        print(
            f"  {item['class']:40s} crop={item['crop']:10s} "
            f"rag={item['has_rag']} details={item['has_details']} "
            f"desc={has_desc} sol={has_sol} rag_content={rag_has_content} "
            f"-> {item['needs']}"
        )

    OUT = ROOT / "ml_assets/advisory/generation_tasks.json"
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(needs_generation, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nSaved generation tasks to {OUT}")
    return needs_generation


if __name__ == "__main__":
    main()
