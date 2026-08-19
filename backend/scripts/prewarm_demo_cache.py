"""Prewarm / regenerate the demo answer cache (B1).

Runs the curated demo questions through the live QA pipeline and persists
verified safe_agri answers with corpus-aware keys, so the demo cache hits
at runtime. Regenerating after a corpus rebuild or a demo-question change
is one command.

Usage (from the backend directory):
    uv run python scripts/prewarm_demo_cache.py
        # regenerate plain-lane entries from the questions already in the cache
    uv run python scripts/prewarm_demo_cache.py --file qs.txt
        # also (re)build every line in qs.txt (one question per line)
    uv run python scripts/prewarm_demo_cache.py --model krishokchat-4b
        # rebuild the local-model lane (llama-server must be up on 11435)

Behaviour:
    * Plain-lane entries (crop="", disease="") are regenerated with uniform
      corpus-aware keys; legacy duplicate key formats for the same query are
      removed so the cache stays clean.
    * CROP-lane entries (detect-flow follow-ups) are left untouched — reproduce
      them by running the detect page.
    * gemini / krishokchat-4b model-lane entries are left untouched unless
      --model is given.
    * Any question that now classifies as a terminal category is purged across
      every lane: a refusal must never leave a cached answer behind.

Requirements: backend/.env with a working LLM provider key (or a reachable
local llama-server for --model), DEMO_MODE=true.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from app.application.container import build_container  # noqa: E402
from app.application.qa_pipeline import QAInput  # noqa: E402
from app.core.config import Settings  # noqa: E402

CACHE_PATH = BACKEND_DIR.parent / "demo-assets" / "cached_responses.json"
TERMINAL = {"banned_or_restricted_chemical", "self_harm_or_poisoning_risk", "off_topic", "prompt_injection", "low_confidence"}


def load_cache() -> dict:
    if not CACHE_PATH.exists():
        return {}
    return json.loads(CACHE_PATH.read_text(encoding="utf-8"))


def plain_lane_queries(data: dict) -> list[str]:
    """Unique plain-lane (crop="", disease="") queries across key formats."""
    queries: list[str] = []
    seen: set[str] = set()
    for key, payload in data.items():
        parts = key.split("|")
        if len(parts) >= 5 and parts[0] == "" and parts[1] == "":
            q = payload.get("query", "")
            if q and q not in seen:
                seen.add(q)
                queries.append(q)
    return queries


async def purge_terminal_lanes(container, queries: list[str]) -> list[str]:
    """Delete every cached entry whose live classification is terminal."""
    purged: list[str] = []
    for q in queries:
        try:
            result = await container.qa.run(QAInput(query=q))
        except Exception as exc:
            print(f"    [classify-error] {q[:48]}: {exc}")
            continue
        if result.category.value in TERMINAL:
            for key in [k for k, v in container.qa.answer_cache._items.items() if v.get("query", "") == q]:
                container.qa.answer_cache.delete(key)
                purged.append(f"{q[:40]} -> {result.category.value}")
    return purged


async def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=str, default=None, help="txt file with one question per line")
    parser.add_argument("--model", type=str, default=None, help="lane model selector (e.g. krishokchat-4b)")
    args = parser.parse_args()

    data = load_cache()
    queries = plain_lane_queries(data)
    if args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"file not found: {path}", file=sys.stderr)
            return 2
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and line not in queries:
                queries.append(line)

    if not queries:
        print("no questions to regenerate", file=sys.stderr)
        return 1

    settings = Settings(demo_mode=True)
    container = build_container(settings)
    cache = container.qa.answer_cache

    # 1) Purge terminal-classified questions across every lane (fail-safe).
    purged = await purge_terminal_lanes(container, queries)
    for p in purged:
        print(f"[purged ] {p}")

    # 2) Drop stale plain-lane keys (any format) for the queries we will rebuild,
    #    so legacy duplicate formats collapse into one uniform key each.
    model_sel = args.model
    for key in list(cache._items.keys()):
        parts = key.split("|")
        if len(parts) >= 5 and parts[0] == "" and parts[1] == "":
            q = cache._items[key].get("query", "")
            lane_model = parts[2] or None
            if q in queries and (model_sel is None or lane_model == model_sel):
                cache.delete(key)

    # 3) Regenerate.
    target = [(q, model_sel) for q in queries] if model_sel else [(q, None) for q in queries]
    cached = 0
    for query, model in target:
        result = await container.qa.run(QAInput(query=query, model=model))
        ok = result.category.value == "safe_agri" and result.error is None
        if ok:
            cached += 1
        print(f"[{'cached' if ok else 'NOT-CACHED':11s}] {result.category.value:24s} {query[:44]}")
        if result.error:
            print(f"    error: {result.error[:120]}")

    print(f"\ndone — {cached}/{len(target)} cached; {CACHE_PATH} now has {len(cache._items)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))