#!/usr/bin/env python3
"""N14 — Headline safety evaluation on the DEPLOYED local model (EACL Final).

Reviewer Item A: the E03/N12 headline numbers were measured on cloud models
(BAA = gemini-2.5-flash-lite + safety prompt; UNC = gpt-4o-mini neutral).
This experiment replicates the SAME design on the production model,
krishokchat-4b (Gemma3 4.3B Q4_K_M, Ollama, localhost), so the guarded-vs-
unguarded comparison isolates the guard on the deployed artifact itself.

Methodological identity with E03/N12 (imported, never reimplemented):
  - attack cases: build_attack_cases(30) from run_e03_safety_screening.py
    (7 families x 30 = 210, same seed/templates) + build_cases() from
    run_n12_bangla.py (70 native probes, 7 angles x 10)
  - arm prompts: BASELINES system prompts verbatim (BAA safety prompt goes
    to BAA_LOCAL; neutral prompt goes to UNC_LOCAL). These supersede the
    Modelfile SYSTEM text per arm, exactly as E03 does per arm.
  - judge: classify_attack_response verbatim (rule-based, deterministic, $0)
  - stats: wilson_ci verbatim; temp 0.0; num_predict 150 (= max_tokens 150)
  - ASR semantics: attack_succeeded fraction over ok calls, per arm

Design: 2 arms x (210 + 70) = 560 local calls, sequential (CPU stability),
per-record fsync JSONL, resume-safe (completed case_id+arm skipped).

Money: $0 (localhost Ollama). No preflight (AGENTS.md money rules govern
paid APIs; noted here explicitly).

Outputs (N14_local_model_safety/results/):
  n14_records_<stamp>.jsonl   per-call (prompt, response, judge, latency)
  n14_summary_<stamp>.json    ASR overall + per family + per N12 angle +
                              combined Bangla-100, both arms, Wilson CIs
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
WORKSPACE_ROOT = HERE.parents[5]
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError, OSError):
    pass

OUT_DIR = HERE.parent.parent / "results"
E03_PATH = (WORKSPACE_ROOT / "paper" / "EACL Demo" / "experiments"
            / "E03_safety_screening_accuracy" / "scripts"
            / "run_e03_safety_screening.py")
N12_PATH = (WORKSPACE_ROOT / "paper" / "EACL Final" / "experiments"
            / "N12_safety_bangla_topup" / "scripts" / "run_n12_bangla.py")

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "krishokchat-4b:latest"
TEMPERATURE = 0.0
NUM_PREDICT = 150
CALL_TIMEOUT_S = 600
MAX_RETRIES = 2

# Public arm names used in reports and docs. The on-disk record labels
# ("BAA_LOCAL"/"UNC_LOCAL") are frozen for resume integrity; they map 1:1
# to the names below. ("BAA" is the legacy label of the guarded arm in the
# E03 source runner this design is imported from.)
ARM_PUBLIC = {"BAA_LOCAL": "guarded", "UNC_LOCAL": "unguarded"}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ollama_generate(system: str, prompt: str) -> tuple[str, float]:
    """Single blocking call; raises on failure after retries (caller records)."""
    body = json.dumps({
        "model": MODEL, "system": system, "prompt": prompt,
        "stream": False,
        "options": {"temperature": TEMPERATURE, "num_predict": NUM_PREDICT},
    }).encode()
    last_err: Exception | None = None
    for _ in range(MAX_RETRIES + 1):
        t0 = time.perf_counter()
        try:
            req = urllib.request.Request(
                OLLAMA_URL, data=body,
                headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=CALL_TIMEOUT_S) as r:
                d = json.loads(r.read())
            return d.get("response", "").strip(), (time.perf_counter() - t0) * 1000
        except Exception as e:  # noqa: BLE001 - retried, then recorded
            last_err = e
    raise RuntimeError(f"ollama call failed: {last_err}")


def append_jsonl(path: Path, record: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--arm", choices=["BAA_LOCAL", "UNC_LOCAL", "both"],
                    default="both")
    ap.add_argument("--smoke", action="store_true",
                    help="2 calls (1 E03 + 1 N12 probe, BAA arm), then exit.")
    args = ap.parse_args()

    e03 = load_module("n14_e03_src", E03_PATH)
    n12 = load_module("n14_n12_src", N12_PATH)
    prompts = {name: prompt for name, _model, prompt in e03.BASELINES}
    judge = e03.classify_attack_response
    wilson = e03.wilson_ci

    e03_cases = [{"uid": c["case_id"], "family": c["family"],
                  "angle": None, "source": "E03",
                  "query": c["query"], "target_chemical": c.get("target_chemical")}
                 for c in e03.build_attack_cases(30)]
    n12_cases = [{"uid": f"N12-{i:03d}", "family": "bangla_native_topup",
                  "angle": c.get("angle"), "source": "N12",
                  "query": c["query"],
                  "target_chemical": c.get("target_chemical")}
                 for i, c in enumerate(n12.build_cases())]
    all_cases = e03_cases + n12_cases
    assert len(e03_cases) == 210 and len(n12_cases) == 70, (len(e03_cases), len(n12_cases))

    arms = {"BAA_LOCAL": prompts["BAA"], "UNC_LOCAL": prompts["UNCONSTRAINED"]}
    if args.smoke:
        for c in [e03_cases[0], n12_cases[0]]:
            t0 = time.perf_counter()
            try:
                resp, lat = ollama_generate(arms["BAA_LOCAL"], c["query"])
                print(f"SMOKE {c['uid']} {lat/1000:.1f}s chars={len(resp)}")
                print("  Q:", c["query"][:100])
                print("  A:", resp[:200])
                print("  judge:", judge(resp, c))
            except Exception as e:  # noqa: BLE001
                print(f"SMOKE {c['uid']} FAILED in {(time.perf_counter()-t0):.1f}s: {e}")
                return 1
        print("[SMOKE OK] local model serves both case shapes")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    # Reuse the newest existing records file so reruns (including across
    # midnight date-stamp rollover) resume instead of duplicating calls.
    existing = sorted(OUT_DIR.glob("n14_records_*.jsonl"))
    rec_path = existing[-1] if existing else (OUT_DIR / f"n14_records_{stamp}.jsonl")
    done: set[tuple[str, str]] = set()
    if rec_path.exists():
        with open(rec_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                    if r.get("ok"):
                        done.add((r["uid"], r["arm"]))
                except json.JSONDecodeError:
                    continue

    arms_to_run = [args.arm] if args.arm != "both" else ["BAA_LOCAL", "UNC_LOCAL"]
    for arm in arms_to_run:
        todo = [c for c in all_cases if (c["uid"], arm) not in done]
        print(f"[{ARM_PUBLIC[arm]}] {len(todo)} to run ({len(done)} already done overall)",
              flush=True)
        for i, c in enumerate(todo):
            t0 = time.perf_counter()
            try:
                resp, lat = ollama_generate(arms[arm], c["query"])
                verdict = judge(resp, c)
                append_jsonl(rec_path, {
                    "uid": c["uid"], "arm": arm, "ok": True,
                    "family": c["family"], "angle": c["angle"],
                    "source": c["source"], "query": c["query"],
                    "response": resp, "latency_ms": round(lat, 1), **verdict,
                    "model": MODEL, "temperature": TEMPERATURE,
                })
            except Exception as e:  # noqa: BLE001 - record, continue
                append_jsonl(rec_path, {
                    "uid": c["uid"], "arm": arm, "ok": False,
                    "family": c["family"], "angle": c["angle"],
                    "error": type(e).__name__ + ": " + str(e)[:150],
                    "elapsed_s": round(time.perf_counter() - t0, 1),
                })
            if (i + 1) % 25 == 0:
                print(f"  [{arm}] {i + 1}/{len(todo)}", flush=True)

    # ---- aggregate (deterministic scoring over locked records) ----
    recs = []
    with open(rec_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                recs.append(json.loads(line))
    # latest record wins per (uid, arm, family): E03's own case_ids collide
    # across its two BANG families (bangla_native_injection and
    # banglish_romanized both yield E03-BANG-###), so uid alone is not unique.
    latest: dict[tuple[str, str, str], dict] = {}
    for r in recs:
        latest[(r["uid"], r["arm"], r.get("family", ""))] = r

    def arm_stats(arm: str, filt=None):
        rows = [r for (u, a, _f), r in latest.items()
                if a == arm and r.get("ok") and (filt is None or filt(r))]
        n = len(rows)
        s = sum(1 for r in rows if r.get("attack_succeeded"))
        lo, hi = wilson(s, n)
        lat = sorted(r.get("latency_ms", 0) for r in rows)
        return {"n": n, "successes": s, "asr_pct": round(s / n * 100, 2) if n else None,
                "ci95": [lo, hi],
                "latency_p50_ms": round(lat[len(lat) // 2], 1) if lat else None}

    summary = {
        "experiment": "N14_LOCAL_MODEL_SAFETY",
        "execution_status": "DONE_REAL",
        "design": {"model": MODEL, "temperature": TEMPERATURE,
                   "num_predict": NUM_PREDICT,
                   "e03_cases": 210, "n12_cases": 70,
                   "judge": "E03 classify_attack_response verbatim",
                   "prompts": "E03 BASELINES verbatim per arm",
                   "records_file": rec_path.name},
        "arms": {},
    }
    for arm in ["BAA_LOCAL", "UNC_LOCAL"]:
        pub = ARM_PUBLIC[arm]
        a = {"overall": arm_stats(arm)}
        fams = sorted({r["family"] for (u, x, _f), r in latest.items()
                       if x == arm and r.get("ok")})
        a["per_family"] = {f: arm_stats(arm, lambda r, f=f: r["family"] == f)
                           for f in fams}
        angs = sorted({r["angle"] for (u, x, _f), r in latest.items()
                       if x == arm and r.get("ok") and r.get("angle")})
        a["per_n12_angle"] = {g: arm_stats(
            arm, lambda r, g=g: r.get("angle") == g) for g in angs}
        a["combined_bangla100"] = arm_stats(
            arm, lambda r: (r["family"] == "bangla_native_injection" and r["source"] == "E03")
            or r["source"] == "N12")
        summary["arms"][pub] = a

    out_path = OUT_DIR / f"n14_summary_{stamp}.json"
    tmp = out_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    with open(tmp, "a", encoding="utf-8") as f:
        f.flush()
        os.fsync(f.fileno())
    tmp.replace(out_path)
    print(json.dumps({a: summary["arms"][a]["overall"] for a in summary["arms"]},
                     indent=2))
    print(f"[OK] wrote {out_path} + {rec_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
