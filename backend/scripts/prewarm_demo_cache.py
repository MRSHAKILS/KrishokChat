"""Offline prewarm of the demo answer cache (B1).

Runs the REAL pipeline over the curated demo questions from
`demo-assets/qa-demo-questions.md` and stores the verified safe answers in
`demo-assets/cached_responses.json` (the same file the server reads when
DEMO_MODE=true). After prewarming, the demo's curated questions replay from
disk: instant (~ms), zero LLM cost, fully offline-capable.

Honesty:
- Terminal questions (banned / self-harm / off-topic / prompt injection) are
  run but never cached — the safety lane always re-evaluates them live.
- The prewarm writes its audit rows to a throwaway temp file, never the live
  `safety_audit.jsonl`, so demo metrics are not polluted by build runs.
- Nothing is fabricated: every cached payload is a real pipeline output with
  its real sources, trace, and verifier stamps.

Usage (from `backend/`):
    uv run python scripts/prewarm_demo_cache.py
"""

from __future__ import annotations

import asyncio
import re
import sys
import tempfile
import time
from pathlib import Path

# Make `app` importable when run as `uv run python scripts/prewarm_demo_cache.py`
# from the backend/ directory (script dir, not cwd, is on sys.path by default).
BACKEND_ROOT = Path(__file__).resolve().parent.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.application.container import build_container
from app.application.qa_pipeline import QAInput
from app.core.config import Settings
from app.infrastructure.cache.demo import DemoAnswerCache, qa_result_to_dict

QUESTIONS_MD = Path(__file__).resolve().parent.parent.parent / "demo-assets" / "qa-demo-questions.md"


def extract_questions(md_text: str) -> list[str]:
    """Pull the backticked demo questions from the markdown tables."""
    rows = re.findall(r"^\|\s*\d+\s*\|\s*`([^`]+)`", md_text, flags=re.MULTILINE)
    return [row.strip() for row in rows]


async def main() -> None:
    if not QUESTIONS_MD.exists():
        print(f"ERROR: demo questions file not found: {QUESTIONS_MD}")
        sys.exit(1)

    questions = extract_questions(QUESTIONS_MD.read_text(encoding="utf-8"))
    if not questions:
        print("ERROR: no questions extracted from qa-demo-questions.md")
        sys.exit(1)
    print(f"Prewarming demo answer cache with {len(questions)} curated questions...\n")

    # Throwaway audit log: prewarm runs must not pollute the demo metrics panel.
    tmp_dir = tempfile.mkdtemp(prefix="krishokchat_prewarm_")
    settings = Settings(audit_log_path=str(Path(tmp_dir) / "prewarm_audit.jsonl"))
    cache = DemoAnswerCache(
        settings.resolved_demo_cache_path,
        max_entries=settings.demo_cache_max_entries,
    )
    container = build_container(settings)

    cached = 0
    for index, question in enumerate(questions, start=1):
        started = time.monotonic()
        result = await container.qa.run(QAInput(query=question))
        elapsed = time.monotonic() - started

        key = cache.key_for(question)
        qualifies = result.category.value == "safe_agri" and result.error is None
        if qualifies:
            cache.put(key, qa_result_to_dict(result))
            cached += 1
        status = "CACHED" if qualifies else "not-cached"
        print(f"  [{index}] {status:11s} {result.category.value:28s} {elapsed:5.1f}s  {question[:48]}")
        if result.error:
            print(f"         error: {result.error[:160]}")

    print(
        f"\nDone: {cached}/{len(questions)} cached. Cache file: {cache.path} "
        f"({len(cache)} entries)."
    )
    if cached == 0:
        print("NOTE: nothing was cached — check the OpenRouter key / LLM reachability.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())