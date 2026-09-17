#!/usr/bin/env python3
"""N05 SMS survival through the real endpoint (EACL Final).

OFFLINE part ($0): N>=300 real queries through POST-logic sms_advisory_endpoint
with the offline (stub) container. Checks: char_count<=160 (must be 100%),
referral-only text on blocked/low-confidence, tier/confidence recorded.
LIVE part (real API): --live N safe queries through the same endpoint with a
live container (build_container + OpenRouter key) for field-survival measurement.

Money rules: pre-flight auth required before --live (run preflight.py first);
per-record fsync; pause after >20 consecutive API errors; max tokens come from
server Settings caps.

Outputs (experiments/results/): n05_sms_<date>.json (+ _live variant).
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve()
WORKSPACE_ROOT = HERE.parents[5]
sys.path.insert(0, str(WORKSPACE_ROOT / "backend"))
sys.path.insert(0, str(WORKSPACE_ROOT / "paper" / "EACL Demo" / "experiments" / "shared"))

import _qa_harness as H  # noqa: E402

OUT_DIR = WORKSPACE_ROOT / "paper" / "EACL Final" / "experiments" / "results"
FARMER_PATH = WORKSPACE_ROOT / "backend" / "ml_assets" / "rag_index" / "eval" / "farmer_benchmark_1000.jsonl"
PRISM_PATH = WORKSPACE_ROOT / "research_artifacts" / "datasets" / "prism_benchmark" / "prism_benchmark_1000.jsonl"

GSM7 = set("@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞÆæßÉ !\"#¤%&'()*+,-./0123456789:;<=>?¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿abcdefghijklmnopqrstuvwxyzäöñüà")


def gsm_audit(text: str) -> dict:
    non_gsm = sorted({c for c in text if c not in GSM7})
    return {"len_chars": len(text), "non_gsm_count": len(non_gsm),
            "non_gsm_sample": "".join(non_gsm[:12]), "is_gsm7": not non_gsm}


def append_jsonl(path: Path, record: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def load_queries(n_safe: int, n_amb: int, n_risk: int, seed: int):
    rnd = random.Random(seed)
    farmer = [json.loads(l) for l in open(FARMER_PATH, encoding="utf-8")]
    prism = [json.loads(l) for l in open(PRISM_PATH, encoding="utf-8")]
    amb = [r["query"] for r in prism if r.get("category") == "F_underspecified"]
    risk_pool = ([r["query"] for r in prism if r.get("category") == "J_high_risk_treatment"])
    safe = rnd.sample([r["question"] for r in farmer], n_safe)
    return ([("safe", q) for q in safe] + [("ambiguous", q) for q in rnd.sample(amb, n_amb)]
            + [("high_risk", q) for q in rnd.sample(risk_pool, n_risk)])


async def run_offline(queries) -> list[dict]:
    from app.api.extras import SMSAdvisoryRequest, sms_advisory_endpoint
    pipeline, _, _, _ = H.build_offline_pipeline(audit=H.InMemoryAudit())
    container = SimpleNamespace(qa=pipeline)
    out = []
    for kind, q in queries:
        t0 = time.perf_counter()
        try:
            resp = await sms_advisory_endpoint(SMSAdvisoryRequest(query=q), container)
            out.append({"kind": kind, "query": q, "ok": True,
                        "sms_text": resp.sms_text, "char_count": resp.char_count,
                        "gsm_segments": resp.gsm_segments, "tier": resp.resolution_tier,
                        "confidence": resp.confidence, "institution": resp.institution,
                        "referral": resp.helpline_referral,
                        "audit": gsm_audit(resp.sms_text),
                        "latency_ms": round((time.perf_counter() - t0) * 1000, 1)})
        except Exception as e:  # noqa: BLE001 - record, don't stop
            out.append({"kind": kind, "query": q, "ok": False, "error": type(e).__name__ + ": " + str(e)[:150]})
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true", help="live container for field-survival subset")
    ap.add_argument("--live-n", type=int, default=100)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    tag = "live" if args.live else "offline"
    out_path = OUT_DIR / f"n05_sms_{tag}_{stamp}.json"
    rec_path = OUT_DIR / f"n05_sms_{tag}_{stamp}.jsonl"
    if rec_path.exists():
        rec_path.unlink()

    if args.live:
        from app.api.extras import SMSAdvisoryRequest, sms_advisory_endpoint
        from app.core.config import Settings
        from app.application.container import build_container
        import os as _os
        key = None
        for p in (WORKSPACE_ROOT / ".env", WORKSPACE_ROOT / "backend" / ".env"):
            try:
                for line in open(p, encoding="utf-8"):
                    if line.strip().startswith("OPENROUTER_API_KEY"):
                        key = line.split("=", 1)[1].strip().strip("'").strip('"')
            except OSError:
                pass
        if not key:
            print("LIVE FAIL: no key (run preflight first)");
            return 1
        _os.environ["OPENROUTER_API_KEY"] = key
        settings = Settings(openrouter_api_key=key)
        container = build_container(settings)
        farmer = [json.loads(l) for l in open(FARMER_PATH, encoding="utf-8")]
        queries = [("safe", r["question"]) for r in random.Random(args.seed).sample(farmer, args.live_n)]
        # run sequentially in async context below
        async def _run():
            global records
            recs, errs = [], 0
            for kind, q in queries:
                try:
                    resp = await sms_advisory_endpoint(SMSAdvisoryRequest(query=q), container)
                    recs.append({"kind": kind, "query": q, "ok": True,
                                 "sms_text": resp.sms_text, "char_count": resp.char_count,
                                 "tier": resp.resolution_tier, "confidence": resp.confidence,
                                 "institution": resp.institution, "audit": gsm_audit(resp.sms_text)})
                    errs = 0
                except Exception as e:  # noqa: BLE001
                    recs.append({"kind": kind, "query": q, "ok": False,
                                 "error": type(e).__name__ + ": " + str(e)[:150]})
                    errs += 1
                    if errs > 20:
                        print("ABORT: >20 consecutive API errors (money rule)");
                        raise SystemExit(2)
            return recs
        records = asyncio.run(_run())
    else:
        queries = load_queries(200, 50, 50, args.seed)
        records = asyncio.run(run_offline(queries))

    for r in records:
        append_jsonl(rec_path, r)

    ok = [r for r in records if r.get("ok")]
    viol = [r for r in ok if r.get("char_count", 0) > 160]
    blocked = [r for r in ok if r.get("confidence") in ("blocked", "low_confidence")]
    blocked_referral_ok = [r for r in blocked if "16123" in (r.get("sms_text") or "") or "১৬১২৩" in (r.get("sms_text") or "")]
    non_gsm = [r for r in ok if not r.get("audit", {}).get("is_gsm7", True)]
    results = {
        "benchmark_name": "EACL_N05_SMS_SURVIVAL",
        "execution_status": "DONE_REAL",
        "provenance": H.provenance(HERE, inputs={"farmer": FARMER_PATH, "prism": PRISM_PATH}),
        "mode": tag,
        "design": {"n": len(records), "seed": args.seed},
        "enforcement": {
            "n_ok": len(ok), "n_fail": len(records) - len(ok),
            "over_160": len(viol),
            "blocked_or_lowconf": len(blocked),
            "blocked_referral_only": len(blocked_referral_ok),
        },
        "encoding": {
            "non_gsm7_texts": len(non_gsm),
            "note": "Bengali script travels as UCS-2 on real gateways (70 chars/segment); length claim is characters, not GSM segments.",
        },
    }
    tmp = out_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(out_path)
    print(json.dumps(results["enforcement"], indent=2), "| non-gsm7:", len(non_gsm))
    print(f"[OK] wrote {out_path} + {rec_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
