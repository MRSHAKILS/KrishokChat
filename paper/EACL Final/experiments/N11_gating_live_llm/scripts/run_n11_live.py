#!/usr/bin/env python3
"""G5 live-vs-deterministic gating head-to-head on 200 REAL farmer queries.

Same 200 labeled rows as N01b (sheet), same frozen code, but the pipeline runs
the PRODUCTION live path (SafetyClassifier intent LLM + grounded generation,
both via OpenRouter gemini-2.5-flash-lite, temp/caps from server Settings).
Comparison target: N01b deterministic records on identical rows.

Money rules: pre-flight first; per-record fsync; abort after >20 consecutive
API errors; provider usage tokens recorded per row where exposed.

Outputs: experiments/results/n11_live_gating_<date>.json (+ .jsonl records).
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
WORKSPACE_ROOT = HERE.parents[5]
sys.path.insert(0, str(WORKSPACE_ROOT / "backend"))
sys.path.insert(0, str(WORKSPACE_ROOT / "paper" / "EACL Demo" / "experiments" / "shared"))

import _qa_harness as H  # noqa: E402

OUT_DIR = WORKSPACE_ROOT / "paper" / "EACL Final" / "experiments" / "results"
SHEET_PATH = OUT_DIR / "crop_slot_labeling_sheet_200.json"
N01B_PATH = OUT_DIR / "n01b_records_20260917.jsonl"


def append_jsonl(path: Path, record: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = OUT_DIR / f"n11_live_gating_{stamp}.json"
    rec_path = OUT_DIR / f"n11_live_gating_{stamp}.jsonl"
    if rec_path.exists():
        rec_path.unlink()

    from app.api.extras import SMSAdvisoryRequest  # noqa: F401  (import check only)
    from app.application.container import build_container
    from app.application.qa_pipeline import QAInput
    from app.core.config import Settings

    key = None
    for p in (WORKSPACE_ROOT / ".env", WORKSPACE_ROOT / "backend" / ".env"):
        try:
            for line in open(p, encoding="utf-8"):
                if line.strip().startswith("OPENROUTER_API_KEY"):
                    key = line.split("=", 1)[1].strip().strip("'").strip('"')
        except OSError:
            pass
    if not key:
        print("FAIL: no key (run preflight first)")
        return 1
    import subprocess as _sp
    _pre = _sp.run([sys.executable, str(WORKSPACE_ROOT / "paper" / "EACL Final" / "experiments" / "preflight.py")],
                   capture_output=True, text=True)
    if _pre.returncode != 0:
        print("FAIL: pre-flight authorization failed; aborting.")
        print(_pre.stdout[-500:] if _pre.stdout else "")
        return 1
    os.environ["OPENROUTER_API_KEY"] = key
    settings = Settings(openrouter_api_key=key)
    container = build_container(settings)
    live_config = {"model": settings.openrouter_model,
                   "temperature": settings.llm_temperature,
                   "max_output_tokens": settings.llm_max_output_tokens}

    sheet = json.loads(SHEET_PATH.read_text(encoding="utf-8"))
    det = {}
    for line in open(N01B_PATH, encoding="utf-8"):
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        det[r.get("id")] = r

    async def run_all():
        out, errs = [], 0
        # Per-record durability (fix: past runs buffered the live loop).
        if rec_path.exists():
            rec_path.unlink()
        for idx, row in enumerate(sheet):
            t0 = time.perf_counter()
            try:
                res = await container.qa.run(QAInput(query=row["query"]))
                latency_ms = round((time.perf_counter() - t0) * 1000, 1)
                rec = {"id": row["id"], "ok": True,
                       "tier": res.resolution_tier.value,
                       "category": res.category.value,
                       "confidence": res.confidence.value,
                       "halted": len(res.sources) == 0,
                       "n_sources": len(res.sources),
                       "answer_preview": (res.answer or "")[:120],
                       "latency_ms": latency_ms}
                out.append(rec)
                append_jsonl(rec_path, rec)
                errs = 0
            except Exception as e:  # noqa: BLE001 - record, gate on consecutive errors
                rec = {"id": row["id"], "ok": False,
                       "error": type(e).__name__ + ": " + str(e)[:150]}
                out.append(rec)
                append_jsonl(rec_path, rec)
                errs += 1
                if errs > 20:
                    print("ABORT: >20 consecutive API errors")
                    raise SystemExit(2)
            if (idx + 1) % 25 == 0:
                print(f"[{idx + 1}/{len(sheet)}] done", flush=True)
        return out

    recs = asyncio.run(run_all())

    ok = [r for r in recs if r.get("ok")]
    halt = sum(1 for r in ok if r["halted"])
    agree = sum(1 for r in ok if det.get(r["id"], {}).get("gated_halted") == r["halted"])
    lat = sorted(r["latency_ms"] for r in ok)
    p50 = lat[len(lat) // 2] if lat else None
    p95 = lat[int(len(lat) * 0.95)] if lat else None
    results = {
        "benchmark_name": "EACL_N11_LIVE_GATING_HEADTOHEAD",
        "execution_status": "DONE_REAL",
        "provenance": H.provenance(HERE, inputs={"sheet": SHEET_PATH}),
        "live_config": live_config,
        "design": {"n": len(sheet), "comparator": "N01b deterministic records, identical rows+code"},
        "live": {"n_ok": len(ok), "n_fail": len(recs) - len(ok),
                 "halt_rate": round(halt / len(ok), 4) if ok else None,
                 "halt_agreement_with_deterministic": round(agree / len(ok), 4) if ok else None,
                 "latency_p50_ms": p50, "latency_p95_ms": p95},
    }
    tmp = out_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(out_path)
    print(json.dumps(results["live"], indent=2))
    print(f"[OK] wrote {out_path} + {rec_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
