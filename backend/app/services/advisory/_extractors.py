"""Shared extractors for advisory workflow."""
import json
import pathlib

HEALTHY = {"healthy", "healthyleaf", "healthy_leaf", "healthy leaf"}


def is_healthy(cls: str) -> bool:
    c = cls.lower().replace("_", "").replace(" ", "").replace("-", "")
    return c in {"healthy", "healthyleaf"}


def extract_disease_name(cls: str) -> str:
    s = cls.split("__")[-1] if "__" in cls else cls
    return s.replace("_", " ").strip()


def load_all_crop_classes():
    VISION = pathlib.Path(r"D:\KrishokChat Advisory System\backend\ml_assets\vision")
    CROP_MODELS = {
        "Rice": VISION / "rice_disease",
        "Wheat": VISION / "wheat_disease",
        "Potato": VISION / "potato_disease",
        "Brassica": VISION / "brassica_disease",
        "Corn": VISION / "corn_disease",
    }
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


def get_disease_details(crop, disease_name):
    """Get disease details content from nested disease_details.json."""
    VISION = pathlib.Path(r"D:\KrishokChat Advisory System\backend\ml_assets\vision")
    CROP_MODELS = {
        "Rice": VISION / "rice_disease",
        "Wheat": VISION / "wheat_disease",
        "Potato": VISION / "potato_disease",
        "Brassica": VISION / "brassica_disease",
        "Corn": VISION / "corn_disease",
    }
    model_dir = CROP_MODELS.get(crop)
    if not model_dir:
        return None
    dd_file = model_dir / "disease_details.json"
    if not dd_file.exists():
        return None
    details = json.loads(dd_file.read_text(encoding="utf-8"))
    for lib_key, lib_val in details.items():
        if isinstance(lib_val, dict) and "classes" in lib_val:
            for cls_entry in lib_val["classes"]:
                cls_name = cls_entry.get("class_name", "")
                norm = cls_name.lower().split("(")[0].strip().replace(" ", "").replace("_", "")
                dname_norm = disease_name.lower().replace(" ", "").replace("_", "")
                if norm == dname_norm:
                    return cls_entry
    return None


def load_rag_nodes():
    NODES_FILE = pathlib.Path(r"D:\KrishokChat Advisory System\backend\ml_assets\rag_index\processed\knowledge_nodes_clean.jsonl")
    nodes = []
    with open(NODES_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                nodes.append(json.loads(line))
    return nodes


def get_rag_node(node_id, nodes):
    for n in nodes:
        if n["id"] == node_id:
            return n
    return None
