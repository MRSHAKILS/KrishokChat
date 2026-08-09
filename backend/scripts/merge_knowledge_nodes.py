"""Merge generated knowledge nodes into RAG index with UTF-8 encoding."""
import json
import pathlib
import pickle
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

ROOT = pathlib.Path(r"D:\KrishokChat Advisory System\backend")
INPUT_DIR = pathlib.Path(r"C:\Users\raiya\Downloads\files_extracted")
NODES_FILE = ROOT / "ml_assets/rag_index/processed/knowledge_nodes_clean.jsonl"
INDEX_FILE = ROOT / "ml_assets/rag_index/indexes/bm25_index.pkl"
MAP_FILE = ROOT / "ml_assets/advisory/disease_knowledge_map.json"

def validate_node(node, filename):
    """Validate and fix a knowledge node."""
    required = ["id", "category", "title_bn", "title_en", "content_bn", "content_en",
                "summary", "tags", "source_document", "treatment_summary_bn",
                "prevention_bn", "bm25_text", "embed_text"]
    for field in required:
        if field not in node or not node[field]:
            print(f"  WARN: {filename} missing field: {field}")
            node[field] = node.get(field, f"TODO: {field}")

    # Ensure tags is a list
    if isinstance(node["tags"], str):
        node["tags"] = [t.strip() for t in node["tags"].split(",")]

    # Ensure bm25_text includes key terms
    if "bm25_text" in node and not node["bm25_text"].strip():
        node["bm25_text"] = f"{node.get('title_bn','')} {node.get('title_en','')} {node.get('summary','')} {' '.join(node.get('tags',[]))}"

    node["generated"] = True
    return node


def main():
    # Find all JSON files
    json_files = list(INPUT_DIR.glob("*.json"))
    print(f"Found {len(json_files)} JSON files")

    # Load existing node IDs
    existing_ids = set()
    if NODES_FILE.exists():
        with open(NODES_FILE, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    node = json.loads(line)
                    existing_ids.add(node["id"])
    print(f"Existing nodes: {len(existing_ids)}")

    # Process new nodes
    new_nodes = []
    for jf in sorted(json_files):
        print(f"\nProcessing: {jf.name}")
        with open(jf, encoding="utf-8") as f:
            node = json.load(f)

        if node["id"] in existing_ids:
            print(f"  SKIP (already exists): {node['id']}")
            continue

        node = validate_node(node, jf.name)
        new_nodes.append(node)
        print(f"  OK: {node['id']} ({node.get('title_en','')})")

    # Append to nodes file
    with open(NODES_FILE, "a", encoding="utf-8") as f:
        for node in new_nodes:
            f.write(json.dumps(node, ensure_ascii=False) + "\n")

    print(f"\nAdded {len(new_nodes)} new nodes")

    # Rebuild BM25 index
    print("Rebuilding BM25 index...")
    try:
        from rank_bm25 import BM25Okapi
        nodes = []
        with open(NODES_FILE, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    nodes.append(json.loads(line))

        corpus = [n.get("bm25_text", "") for n in nodes]
        tokenized = [doc.lower().split() for doc in corpus]
        bm25 = BM25Okapi(tokenized)

        index_data = {
            "bm25": bm25,
            "nodes": nodes,
            "corpus": corpus,
            "ids": [n["id"] for n in nodes],
        }
        with open(INDEX_FILE, "wb") as f:
            pickle.dump(index_data, f)
        print(f"BM25 rebuilt: {len(nodes)} documents")
    except ImportError:
        print("rank_bm25 not installed, skipping BM25 rebuild")

    # Update disease knowledge map
    print("Updating disease knowledge map...")
    mapping = json.loads(MAP_FILE.read_text(encoding="utf-8"))
    updated = 0
    for node in new_nodes:
        # Find matching disease class
        for cls, info in mapping.items():
            disease_norm = info["disease_name"].lower().replace(" ", "_").replace("-", "_")
            node_id_lower = node["id"].lower()
            if disease_norm in node_id_lower or info["crop"].lower() in node_id_lower:
                if not info["rag_node_ids"]:
                    info["rag_node_ids"].append(node["id"])
                    info["category"] = "A" if info["has_disease_details"] else "B"
                    updated += 1
                    print(f"  Updated: {cls} -> {info['category']}")
                break

    with open(MAP_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f"Updated {updated} mappings")

    print("\nDone!")


if __name__ == "__main__":
    main()
