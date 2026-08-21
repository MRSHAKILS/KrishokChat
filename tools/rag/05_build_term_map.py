"""05 — Build a corpus-derived Bengali→English term map for query expansion.

No external dictionary, no fabricated pairs: every term comes from the actual
knowledge corpus's own bilingual titles (title_bn -> title_en). This is the
honest expansion base for P3 until the researcher's 110-word dialect map
(dataset_release/safety/phase4_dialect_map.json) is restored; when it exists,
the runtime expander merges it too (see infrastructure/retrieval/expansion.py).
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
RAG_ROOT = SCRIPT_DIR.parent
NODES_PATH = RAG_ROOT / "processed" / "knowledge_nodes_clean.jsonl"
OUT_PATH = RAG_ROOT / "indexes" / "term_map.json"

BENGALI_RE = re.compile(r"[\u0980-\u09FF]")
EN_ALIAS_RE = re.compile(r"^[A-Za-z0-9\s,;:()/&.'’\-]+$")  # pure English/Latin titles


def main() -> None:
    nodes: list[dict] = []
    with NODES_PATH.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                nodes.append(json.loads(line))

    pairs: list[dict[str, str]] = []
    seen: set[str] = set()
    for node in nodes:
        bn = (node.get("title_bn") or "").strip()
        en = (node.get("title_en") or "").strip()
        if not bn or not en:
            continue
        if not BENGALI_RE.search(bn) or len(bn) > 60 or len(en) > 80:
            continue
        # Require a real English rendering (drop titles that are Bengali-only
        # or transcription-only like "BARI Sarisha-14").
        if not EN_ALIAS_RE.search(en):
            continue
        key = bn.lower()
        if key in seen:
            continue
        seen.add(key)
        pairs.append({"bn": bn, "en": en})

    # Longest-first so expansion matches the most specific term first.
    pairs.sort(key=lambda p: len(p["bn"]), reverse=True)

    payload = {
        "version": 1,
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "corpus bilingual titles (knowledge_nodes_clean.jsonl)",
        "count": len(pairs),
        "map": pairs,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(payload, ensure_ascii=False, indent=1)
    OUT_PATH.write_text(raw, encoding="utf-8")
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()

    print(f"nodes scanned : {len(nodes)}")
    print(f"term pairs    : {len(pairs)}")
    print(f"output        : {OUT_PATH}")
    print(f"sha256        : {digest}")
    print("--- samples ---")
    for p in pairs[:8]:
        print(f"  {p['bn']} => {p['en']}")


if __name__ == "__main__":
    main()