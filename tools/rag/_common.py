"""Shared paths and helpers for the RAG index pipeline."""
from __future__ import annotations

import json
import pathlib
import sys

RAG_ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW_DIR = RAG_ROOT / "raw"
PROCESSED_DIR = RAG_ROOT / "processed"
INDEX_DIR = RAG_ROOT / "indexes"
EVAL_DIR = RAG_ROOT / "eval"
RESULTS_DIR = EVAL_DIR / "results"
LOGS_DIR = RAG_ROOT / "logs"

CORPUS_JSONL = PROCESSED_DIR / "knowledge_nodes_clean.jsonl"
BM25_PKL = INDEX_DIR / "bm25_index.pkl"
BM25_CORPUS_TOK_PKL = INDEX_DIR / "bm25_corpus_tok.pkl"
EMBEDDINGS_NPY = INDEX_DIR / "embeddings.npy"
NODE_IDS_JSON = INDEX_DIR / "node_ids.json"
FAISS_INDEX = INDEX_DIR / "nodes.faiss"
MANIFEST = RAG_ROOT / "manifest.json"

EMBED_MODEL = "intfloat/multilingual-e5-base"
E5_QUERY_PREFIX = "query: "
E5_PASSAGE_PREFIX = "passage: "
BM25_K1 = 2.2
BM25_B = 0.4
RRF_K = 20
CANDIDATE_POOL_DEPTH = 50
FINAL_TOP_K = 5


def utf8_stdout() -> None:
    """Windows consoles default to cp1252 and choke on Bengali output."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def load_corpus() -> list[dict]:
    with CORPUS_JSONL.open(encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def write_json(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
