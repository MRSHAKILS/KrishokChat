"""
Build or load the FAISS retrieval index for the knowledge base.

Usage:
    python scripts/build_rag_index.py \
        --input backend/ml_assets/rag_index/knowledge_nodes.json \
        --output backend/ml_assets/rag_index/

Prerequisites:
    - knowledge_nodes.json placed in backend/ml_assets/rag_index/
    - JSON schema: array of objects with fields:
        id, crop_bn, crop_en, disease_bn, problem_type, question, answer,
        treatment, dosage, safety_warnings, legal_status, source, expert_verified
    - faiss-cpu, sentence-transformers installed
"""

import argparse
import json
from pathlib import Path


def build_index(corpus_path: Path, output_dir: Path):
    """Build FAISS index from knowledge nodes JSON."""
    from sentence_transformers import SentenceTransformer
    import faiss
    import numpy as np

    print(f"Loading corpus from {corpus_path}...")
    with open(corpus_path, "r", encoding="utf-8") as f:
        nodes = json.load(f)

    print(f"Loaded {len(nodes)} knowledge nodes")

    texts = []
    for node in nodes:
        parts = []
        if node.get("question"):
            parts.append(node["question"])
        if node.get("answer"):
            parts.append(node["answer"])
        if node.get("crop_bn"):
            parts.append(node["crop_bn"])
        if node.get("disease_bn"):
            parts.append(node["disease_bn"])
        texts.append(" ".join(parts))

    print("Encoding with sentence-transformers...")
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)

    dimension = embeddings.shape[1]
    print(f"Embedding dimension: {dimension}")

    print("Building FAISS index...")
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings.astype("float32"))

    output_dir.mkdir(parents=True, exist_ok=True)

    index_path = output_dir / "knowledge.faiss"
    faiss.write_index(index, str(index_path))
    print(f"Index saved: {index_path}")

    metadata_path = output_dir / "metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(nodes, f, ensure_ascii=False, indent=2)
    print(f"Metadata saved: {metadata_path}")

    print(f"\nDone! Index contains {index.ntotal} vectors")


def main():
    parser = argparse.ArgumentParser(description="Build FAISS RAG index")
    parser.add_argument("--input", type=Path, required=True, help="Path to knowledge_nodes.json")
    parser.add_argument("--output", type=Path, required=True, help="Output directory for index files")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Input file not found: {args.input}")
        print("Place your knowledge_nodes.json file there first.")
        return

    build_index(args.input, args.output)


if __name__ == "__main__":
    main()
