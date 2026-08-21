"""Clean and normalize AgriTrust knowledge nodes for the RAG index.

Reads  : ml_assets/rag_index/raw/knowledge_nodes.json
Writes : ml_assets/rag_index/processed/knowledge_nodes_clean.jsonl

Runnable from any working directory (paths resolved from __file__).
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

from bnunicodenormalizer import Normalizer

SCRIPT_DIR = Path(__file__).resolve().parent
RAG_ROOT = SCRIPT_DIR.parent
RAW_PATH = RAG_ROOT / "raw" / "knowledge_nodes.json"
OUT_DIR = RAG_ROOT / "processed"
OUT_PATH = OUT_DIR / "knowledge_nodes_clean.jsonl"

BENGALI_RE = re.compile(r"[\u0980-\u09FF]")
WS_RE = re.compile(r"\s+")

_normalizer = Normalizer()


def collapse_ws(text: str) -> str:
    return WS_RE.sub(" ", text).strip()


def as_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return collapse_ws(value)
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, (list, tuple)):
        return collapse_ws(" ".join(as_text(v) for v in value))
    return collapse_ws(str(value))


def as_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        item = collapse_ws(value)
        return [item] if item else []
    if isinstance(value, (list, tuple)):
        out = []
        for v in value:
            item = as_text(v)
            if item:
                out.append(item)
        return out
    return [as_text(value)]


def normalize_bengali(text: str) -> str:
    """Apply bnunicodenormalizer word-wise.

    The library normalizes a single word at a time and returns
    {'normalized': None} for tokens with no Bengali content, so
    non-Bengali tokens are passed through unchanged.
    """
    if not text:
        return ""
    text = unicodedata.normalize("NFC", text)
    if not BENGALI_RE.search(text):
        return collapse_ws(text)

    out = []
    for token in text.split(" "):
        if not token:
            continue
        if not BENGALI_RE.search(token):
            out.append(token)
            continue
        try:
            result = _normalizer(token)
        except Exception:
            out.append(token)
            continue
        normalized = result.get("normalized") if isinstance(result, dict) else None
        out.append(normalized if normalized else token)
    return collapse_ws(" ".join(out))


def join_nonempty(*parts: str) -> str:
    return collapse_ws(" ".join(p for p in parts if p))


def build_record(node: dict, index: int) -> dict:
    node_id = as_text(node.get("node_id")) or as_text(node.get("id"))
    if not node_id:
        node_id = f"node_{index:05d}"

    category = as_text(node.get("category"))
    title_bn = normalize_bengali(as_text(node.get("title_bn")))
    title_en = as_text(node.get("title_en"))
    content_bn = normalize_bengali(as_text(node.get("content_bn")))
    content_en = as_text(node.get("content_en"))

    raw_summary = as_text(node.get("summary"))
    summary = normalize_bengali(raw_summary) if BENGALI_RE.search(raw_summary) else raw_summary

    tags = [normalize_bengali(t) if BENGALI_RE.search(t) else t for t in as_list(node.get("tags"))]

    source_document = as_text(node.get("source_document"))
    publisher = as_text(node.get("publisher"))
    citation = as_text(node.get("citation"))
    section_title = as_text(node.get("section_title"))
    if BENGALI_RE.search(section_title):
        section_title = normalize_bengali(section_title)

    tags_text = " ".join(tags)

    # Field weighting for BM25: titles and category repeated x2.
    bm25_text = join_nonempty(
        title_bn,
        title_bn,
        title_en,
        title_en,
        content_bn,
        content_en,
        summary,
        category,
        category,
        tags_text,
    )

    embed_text = join_nonempty(title_bn, title_en, content_bn, content_en, summary)

    return {
        "id": node_id,
        "category": category,
        "title_bn": title_bn,
        "title_en": title_en,
        "content_bn": content_bn,
        "content_en": content_en,
        "summary": summary,
        "tags": tags,
        "source_document": source_document,
        "publisher": publisher,
        "citation": citation,
        "section_title": section_title,
        "bm25_text": bm25_text,
        "embed_text": embed_text,
    }


def main() -> int:
    if not RAW_PATH.exists():
        print(f"ERROR: raw file not found: {RAW_PATH}", file=sys.stderr)
        return 1

    with RAW_PATH.open("r", encoding="utf-8") as fh:
        nodes = json.load(fh)

    if not isinstance(nodes, list):
        print(f"ERROR: expected a JSON array, got {type(nodes).__name__}", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    total = 0
    empty_content_bn = 0
    empty_content_en = 0
    empty_both = 0
    empty_embed = 0
    seen_ids: set[str] = set()
    duplicate_ids = 0

    with OUT_PATH.open("w", encoding="utf-8", newline="\n") as out:
        for index, node in enumerate(nodes):
            if not isinstance(node, dict):
                print(f"WARN: skipping non-object at index {index}", file=sys.stderr)
                continue

            record = build_record(node, index)

            if record["id"] in seen_ids:
                duplicate_ids += 1
            seen_ids.add(record["id"])

            if not record["content_bn"]:
                empty_content_bn += 1
            if not record["content_en"]:
                empty_content_en += 1
            if not record["content_bn"] and not record["content_en"]:
                empty_both += 1
            if not record["embed_text"]:
                empty_embed += 1

            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            total += 1

    print("=" * 52)
    print("Clean + normalize complete")
    print("=" * 52)
    print(f"Input                : {RAW_PATH}")
    print(f"Output               : {OUT_PATH}")
    print(f"Total nodes          : {total}")
    print(f"Empty content_bn     : {empty_content_bn}")
    print(f"Empty content_en     : {empty_content_en}")
    print(f"Empty both contents  : {empty_both}")
    print(f"Empty embed_text     : {empty_embed}")
    print(f"Unique ids           : {len(seen_ids)}")
    print(f"Duplicate ids        : {duplicate_ids}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
