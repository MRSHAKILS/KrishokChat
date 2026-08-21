"""Build dense embeddings using mE5-small with checkpointing."""
import json
import time
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

SCRIPT_DIR = Path(__file__).resolve().parent
RAG_ROOT = SCRIPT_DIR.parent
NODES_PATH = RAG_ROOT / "processed" / "knowledge_nodes_clean.jsonl"
OUT_DIR = RAG_ROOT / "indexes"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "intfloat/multilingual-e5-small"
BATCH_SIZE = 64
CHECKPOINT_EVERY = 10  # Save every N batches


def load_nodes():
    nodes = []
    with open(NODES_PATH, "r", encoding="utf-8") as f:
        for line in f:
            nodes.append(json.loads(line))
    return nodes


def l2_normalize(vectors):
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms = np.maximum(norms, 1e-9)
    return (vectors / norms).astype(np.float32)


def main():
    print("Loading cleaned nodes...")
    nodes = load_nodes()
    n = len(nodes)
    print(f"  Loaded {n} nodes")

    print(f"Loading model: {MODEL_NAME}...")
    model = SentenceTransformer(MODEL_NAME)
    dim = model.get_sentence_embedding_dimension()
    print(f"  Model loaded, dim={dim}")

    # Check for checkpoint
    checkpoint_path = OUT_DIR / "embeddings_checkpoint.npy"
    meta_path = OUT_DIR / "embeddings_checkpoint_meta.json"
    start_batch = 0
    all_embeddings = None

    if checkpoint_path.exists() and meta_path.exists():
        with open(meta_path) as f:
            meta = json.load(f)
        start_batch = meta["batch_idx"]
        all_embeddings = np.load(checkpoint_path)
        print(f"  Resuming from checkpoint (batch {start_batch})")

    if all_embeddings is None:
        all_embeddings = np.zeros((n, dim), dtype=np.float32)

    texts = ["passage: " + node["embed_text"] for node in nodes]
    n_batches = (n + BATCH_SIZE - 1) // BATCH_SIZE

    print(f"Encoding {n} passages (batch_size={BATCH_SIZE}, {n_batches} batches)...")
    start = time.time()

    for i in range(start_batch, n_batches):
        batch_start = i * BATCH_SIZE
        batch_end = min(batch_start + BATCH_SIZE, n)
        batch_texts = texts[batch_start:batch_end]

        batch_emb = model.encode(
            batch_texts,
            batch_size=BATCH_SIZE,
            show_progress_bar=False,
            normalize_embeddings=False,
            convert_to_numpy=True,
        )
        all_embeddings[batch_start:batch_end] = batch_emb

        # Checkpoint
        if (i + 1) % CHECKPOINT_EVERY == 0 or i == n_batches - 1:
            np.save(checkpoint_path, all_embeddings[:batch_end])
            with open(meta_path, "w") as f:
                json.dump({"batch_idx": i + 1, "dim": dim, "n": n}, f)
            elapsed = time.time() - start
            pct = batch_end / n * 100
            print(f"  Batch {i+1}/{n_batches} ({pct:.0f}%) — {elapsed:.0f}s elapsed — checkpoint saved")

    total_time = time.time() - start
    print(f"  Encoding done in {total_time:.1f}s")

    print("L2-normalizing embeddings...")
    all_embeddings = l2_normalize(all_embeddings)

    emb_path = OUT_DIR / "embeddings.npy"
    np.save(emb_path, all_embeddings)
    print(f"  Saved to {emb_path} ({emb_path.stat().st_size / 1e6:.1f} MB)")

    node_ids = [node["id"] for node in nodes]
    ids_path = OUT_DIR / "node_ids.json"
    with open(ids_path, "w", encoding="utf-8") as f:
        json.dump(node_ids, f, ensure_ascii=False)
    print(f"  Saved {len(node_ids)} node IDs")

    # Clean up checkpoint
    if checkpoint_path.exists():
        checkpoint_path.unlink()
    if meta_path.exists():
        meta_path.unlink()
    print("  Checkpoints cleaned up")

    print(f"\nDone! Shape: {all_embeddings.shape}, dtype: {all_embeddings.dtype}")
    print(f"  Model: {MODEL_NAME}")
    print(f"  Dimension: {dim}")
    print(f"  Vectors: {n}")


if __name__ == "__main__":
    main()
