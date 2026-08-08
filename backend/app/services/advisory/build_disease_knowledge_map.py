"""Build disease_knowledge_map.json — maps YOLO-detectable diseases to RAG knowledge nodes."""
import json
import pathlib
import sys

ROOT = pathlib.Path(r"D:\KrishokChat Advisory System\backend")
NODES_FILE = ROOT / "ml_assets/rag_index/processed/knowledge_nodes_clean.jsonl"
VISION = ROOT / "ml_assets/vision"
OUT_FILE = ROOT / "ml_assets/advisory/disease_knowledge_map.json"

CROP_MODELS = {
    "Rice": VISION / "rice_disease",
    "Wheat": VISION / "wheat_disease",
    "Potato": VISION / "potato_disease",
    "Brassica": VISION / "brassica_disease",
    "Corn": VISION / "corn_disease",
}

HEALTHY = {"healthy", "healthyleaf", "healthy_leaf", "healthy leaf"}


def load_all_crop_classes() -> list[tuple[str, str]]:
    """Return list of (crop_name, class_name) from each crop model's class_names.json."""
    result = []
    for crop_name, model_dir in CROP_MODELS.items():
        cn = model_dir / "class_names.json"
        if not cn.exists():
            continue
        classes = json.loads(cn.read_text(encoding="utf-8"))
        if isinstance(classes, dict):
            classes = [classes[str(i)] for i in range(len(classes))]
        for cls in classes:
            result.append((crop_name, cls))
    return result


def is_healthy(cls: str) -> bool:
    c = cls.lower().replace("_", "").replace(" ", "").replace("-", "")
    return c in {"healthy", "healthyleaf"}


def extract_disease_name(cls: str) -> str:
    s = cls.split("__")[-1] if "__" in cls else cls
    return s.replace("_", " ").strip()


def make_variants(name: str) -> set[str]:
    n = name.lower()
    variants = {n, n + " disease"}
    for suf in [" disease", " blight", " rust", " spot", " rot", " mildew",
                " wilt", " scald", " blast", " point", " leaf spot", " leaf rust"]:
        if n.endswith(suf) and len(n) - len(suf) > 2:
            variants.add(n[: -len(suf)].strip())
    return variants


def main():
    # Load all nodes
    nodes = []
    with open(NODES_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                nodes.append(json.loads(line))

    # Index: crop keyword -> list of node ids (precomputed for speed)
    crop_to_nodes = {}
    for n in nodes:
        hay = (n.get("title_en", "") + " " +
               " ".join(n.get("tags", [])) + " " +
               n.get("bm25_text", "")).lower()
        for crop in ["Rice", "Wheat", "Potato", "Maize", "Corn", "Brassica",
                     "Cabbage", "Cauliflower", "Tomato"]:
            if crop.lower() in hay:
                crop_to_nodes.setdefault(crop, []).append(n)

    mapping = {}
    for crop_name, model_dir in CROP_MODELS.items():
        cn = model_dir / "class_names.json"
        dd_file = model_dir / "disease_details.json"
        classes = json.loads(cn.read_text(encoding="utf-8"))
        if isinstance(classes, dict):
            classes = [classes[str(i)] for i in range(len(classes))]
        details = json.loads(dd_file.read_text(encoding="utf-8")) if dd_file.exists() else {}
        detail_keys = list(details.keys()) if isinstance(details, dict) else []
        print(f"  {crop_name}: {len(classes)} classes, {len(detail_keys)} detail keys")

        for cls in classes:
            if is_healthy(cls):
                continue
            dname = extract_disease_name(cls)
            variants = make_variants(dname)

            # Search in crop-specific node subset + all disease nodes
            search_set = crop_to_nodes.get(crop_name, []) + crop_to_nodes.get("Maize" if crop_name == "Corn" else crop_name, [])
            # de-duplicate
            seen_ids = set()
            unique_nodes = []
            for n in search_set:
                if n["id"] not in seen_ids:
                    seen_ids.add(n["id"])
                    unique_nodes.append(n)
            # also include all disease category nodes as fallback
            for n in nodes:
                if n.get("category") == "disease" and n["id"] not in seen_ids:
                    seen_ids.add(n["id"])
                    unique_nodes.append(n)

            matched = []
            for node in unique_nodes:
                hay = (node.get("title_en", "") + " " +
                       " ".join(node.get("tags", [])) + " " +
                       node.get("bm25_text", "")).lower()
                if any(v in hay for v in variants):
                    matched.append(node["id"])

            has_details = False
            matched_detail_keys = []
            for dk in detail_keys:
                dklower = dk.lower()
                if any(v in dklower for v in variants) or dname.lower() in dklower:
                    has_details = True
                    matched_detail_keys.append(dk)

            if matched and has_details:
                completeness = "A"
            elif matched or has_details:
                completeness = "B"
            else:
                completeness = "C"

            mapping[cls] = {
                "crop": crop_name,
                "disease_name": dname,
                "category": completeness,
                "rag_node_ids": matched[:5],
                "has_disease_details": has_details,
                "matched_detail_keys": matched_detail_keys[:3],
            }

    # Report
    cat_counts = {"A": 0, "B": 0, "C": 0}
    for v in mapping.values():
        cat_counts[v["category"]] += 1
    print(f"Total disease classes mapped: {len(mapping)}")
    print(f"Category A (full info): {cat_counts['A']}")
    print(f"Category B (partial): {cat_counts['B']}")
    print(f"Category C (no info): {cat_counts['C']}")
    print()
    for cls, info in mapping.items():
        nodes_str = ", ".join(info["rag_node_ids"][:2]) if info["rag_node_ids"] else "NONE"
        print(f"[{info['category']}] {cls} ({info['disease_name']}) -> nodes: {nodes_str} | details: {info['has_disease_details']}")

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to {OUT_FILE}")


if __name__ == "__main__":
    main()
