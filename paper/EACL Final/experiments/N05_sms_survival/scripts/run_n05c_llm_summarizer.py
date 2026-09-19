#!/usr/bin/env python3
"""N05c — LLM-summarizer SMS baseline (EACL Final).

Reviewer-driven STRONG baseline for the deterministic 11-slot SMS compressor:
an actual LLM (the paper's frozen cloud benchmark model) summarizes long,
dose-carrying advisories under a 160-character budget — replacing naive hard
truncation (`text[:160]`) as the comparison point.

Design (locked):
  - Sample: n=100 advisories from farmer_benchmark_1000.jsonl with
    len(gold_answer) > 160 AND a dose pattern, seed 42.
  - One LLM arm only: google/gemini-2.5-flash-lite via OpenRouter,
    temperature 0.2, max_output_tokens 500 (AGENTS.md cloud cap).
  - Prompt is the reviewer's wording verbatim + a fairness clause
    ("output only the SMS text, no preamble") so the LLM is not
    handicapped the way truncation was.

Money rules (AGENTS.md s0.1): in-runner preflight authorization via
experiments/preflight.py; per-record fsync to JSONL; abort after >20
consecutive API errors; no in-memory result buffering for records.

Outputs (N05_sms_survival/results/):
  n05c_sample_100.json         — frozen sample manifest (row_ids + texts)
  n05c_records_<stamp>.jsonl   — per-record LLM outputs (fsync'd)

Scoring is separate and free: score_n05c.py recomputes naive +
compressor + LLM arms deterministically from the manifest + records.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import random
import re
import subprocess as sp
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
WORKSPACE_ROOT = HERE.parents[5]
try:  # Windows consoles default to cp1252, which cannot print Bengali.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError, OSError):
    pass
sys.path.insert(0, str(WORKSPACE_ROOT / "backend"))

OUT_DIR = HERE.parent.parent / "results"
FARMER_PATH = (
    WORKSPACE_ROOT / "backend" / "ml_assets" / "rag_index" / "eval"
    / "farmer_benchmark_1000.jsonl"
)
PREFLIGHT = WORKSPACE_ROOT / "paper" / "EACL Final" / "experiments" / "preflight.py"

# Frozen dose definition, mirrored from run_n05_sms.analyze_dose_chemical
# (digit(s) adjacent to a unit token, per the verifier's dosage-claim notion).
DOSE_RE = re.compile(
    r"[0-9০-৯]+(?:[.,][0-9০-৯]+)?\s*(?:ml|mg|\bg\b|kg|\bl\b|liter|litre|"
    r"মিলি|গ্রাম|লিটার|কেজি|ইসি|ডব্লিউপি|EC|WP|SC|SL|শতক|বিঘা|একর)",
    re.IGNORECASE,
)

# Reviewer's prompt verbatim + fairness clause (no preamble, so the LLM is
# not penalized for conversational framing the way truncation was).
PROMPT_TEMPLATE = (
    "Summarize this agricultural advisory for SMS. Keep it under 160 "
    "characters. Do not lose the dosage or chemical name. "
    "Output only the SMS text, no preamble.\n\nAdvisory:\n{advisory}"
)

DEFAULT_MODEL = "google/gemini-2.5-flash-lite"
DEFAULT_TEMPERATURE = 0.2
DEFAULT_MAX_TOKENS = 500  # AGENTS.md s0.1 cloud cap for grounded advisory
DEFAULT_N = 100
DEFAULT_SEED = 42
MIN_GOLD_LEN = 161  # strictly over the 160-char SMS ceiling


def append_jsonl(path: Path, record: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def eligible_pool() -> list[dict]:
    """All advisories that NEED summarization and carry a dose to preserve."""
    pool = []
    with open(FARMER_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            gold = r.get("gold_answer", "") or ""
            if len(gold) >= MIN_GOLD_LEN and DOSE_RE.search(gold):
                pool.append(r)
    return pool


def build_prompt(gold_answer: str) -> str:
    return PROMPT_TEMPLATE.format(advisory=gold_answer)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--n", type=int, default=DEFAULT_N)
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    ap.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
    ap.add_argument("--smoke", action="store_true",
                    help="AGENTS.md Step B: print full prompts for first 2 "
                         "sampled rows, then exit without spending.")
    ap.add_argument("--sample-only", action="store_true",
                    help="write the frozen sample manifest only, no API calls.")
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pool = eligible_pool()
    if len(pool) < args.n:
        print(f"N05c FAIL: pool={len(pool)} < n={args.n}")
        return 1
    sample = random.Random(args.seed).sample(pool, args.n)

    manifest = {
        "arm": "N05c_LLM_SUMMARIZER_BASELINE",
        "n": args.n,
        "seed": args.seed,
        "eligibility": {
            "min_gold_len": MIN_GOLD_LEN,
            "requires_dose_pattern": True,
            "pool_n": len(pool),
            "source": str(FARMER_PATH.relative_to(WORKSPACE_ROOT)),
        },
        "prompt_template": PROMPT_TEMPLATE,
        "live_config": {
            "model": args.model,
            "temperature": args.temperature,
            "max_output_tokens": args.max_tokens,
            "base_url": "https://openrouter.ai/api/v1",
        },
        "records": [
            {"row_id": r.get("row_id"), "question": r.get("question"),
             "gold_answer": r.get("gold_answer", "")}
            for r in sample
        ],
    }

    if args.smoke:
        for rec in manifest["records"][:2]:
            print("=" * 70)
            print(f"row_id={rec['row_id']} gold_len={len(rec['gold_answer'])}")
            print("-" * 70)
            print(build_prompt(rec["gold_answer"]))
        print("=" * 70)
        print(f"[SMOKE OK] pool={len(pool)} sample={args.n} "
              f"(no API calls made)")
        return 0

    manifest_path = OUT_DIR / "n05c_sample_100.json"
    tmp_manifest = manifest_path.with_suffix(".tmp")
    tmp_manifest.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    with open(tmp_manifest, "a", encoding="utf-8") as f:
        f.flush()
        os.fsync(f.fileno())
    tmp_manifest.replace(manifest_path)
    print(f"[OK] manifest: {manifest_path} (pool={len(pool)}, n={args.n})")
    if args.sample_only:
        return 0

    # ---- Money gate: preflight authorization is blocking (AGENTS.md s0.1) ----
    pre = sp.run([sys.executable, str(PREFLIGHT)],
                 capture_output=True, text=True)
    if pre.returncode != 0:
        print("N05c FAIL: pre-flight authorization failed; aborting.")
        print((pre.stdout or "")[-500:])
        return 1
    key = None
    for p in (WORKSPACE_ROOT / ".env", WORKSPACE_ROOT / "backend" / ".env"):
        try:
            for line in open(p, encoding="utf-8"):
                if line.strip().startswith("OPENROUTER_API_KEY"):
                    key = line.split("=", 1)[1].strip().strip("'").strip('"')
        except OSError:
            pass
    if not key:
        print("N05c FAIL: no OPENROUTER_API_KEY (run preflight first)")
        return 1

    from app.infrastructure.llm.openai_compatible import OpenAICompatibleClient

    client = OpenAICompatibleClient(
        base_url="https://openrouter.ai/api/v1",
        model=args.model,
        api_key=key,
        timeout=30.0,
        temperature=args.temperature,
        max_output_tokens=args.max_tokens,
        max_retries=3,
    )

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    rec_path = OUT_DIR / f"n05c_records_{stamp}.jsonl"
    if rec_path.exists():
        rec_path.unlink()

    async def _run() -> tuple[int, int]:
        ok_count, errs = 0, 0
        for rec in manifest["records"]:
            prompt = build_prompt(rec["gold_answer"])
            t0 = time.perf_counter()
            try:
                sms = await client.generate(prompt)
                append_jsonl(rec_path, {
                    "row_id": rec["row_id"],
                    "ok": True,
                    "llm_sms": sms,
                    "llm_len": len(sms),
                    "exceeds_160": len(sms) > 160,
                    "latency_ms": round((time.perf_counter() - t0) * 1000, 1),
                    "usage": client.last_usage,
                    "model": args.model,
                    "temperature": args.temperature,
                })
                ok_count += 1
                errs = 0
            except Exception as e:  # noqa: BLE001 - record, don't stop
                append_jsonl(rec_path, {
                    "row_id": rec["row_id"],
                    "ok": False,
                    "error": type(e).__name__ + ": " + str(e)[:150],
                })
                errs += 1
                if errs > 20:
                    print("ABORT: >20 consecutive API errors (money rule)")
                    raise SystemExit(2)
            if (ok_count % 20) == 0:
                print(f"  ... {ok_count}/{args.n} ok", flush=True)
        return ok_count, args.n - ok_count

    ok_count, fail_count = asyncio.run(_run())
    print(f"[OK] records: {rec_path} ({ok_count} ok, {fail_count} failed)")
    print("Next: python score_n05c.py  (deterministic, $0)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
