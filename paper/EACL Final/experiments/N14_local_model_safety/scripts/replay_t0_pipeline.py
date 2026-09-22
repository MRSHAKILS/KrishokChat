#!/usr/bin/env python3
"""N14b: pipeline ASR on the deployed model = T0 precheck + guarded prompt (replay).

Replays the frozen N14 guarded-arm responses. A prompt counts as a pipeline
success only if the guarded response succeeded (N14 judge) AND the deterministic
T0 precheck does not match it; a T0 match ends the turn before any model call
(see app/application/safety.py, SafetyClassifier.classify). No model is called.

Also checks T0 false blocks on 200 real farmer queries and 15 benign Banglish queries.
Output: N14_local_model_safety/results/n14b_t0_pipeline_replay.json
"""
from __future__ import annotations

import collections
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[5]
EXP = HERE.parents[2]
sys.path.insert(0, str(ROOT / "backend"))
from app.domain.safety_policy import precheck  # noqa: E402

RECORDS = EXP / "N14_local_model_safety/results/n14_records_20260919.jsonl"
FARMER = EXP / "human_annotation_gate_200/consensus_gold_200.json"
BANGLISH = EXP / "banglish_phonetic_red_teaming_100/data/banglish_red_team_100.json"
OUT = EXP / "N14_local_model_safety/results/n14b_t0_pipeline_replay.json"
BN = {"bangla_native_injection", "bangla_native_topup"}


def wilson(k, n, z=1.95996):  # same as N01
    if n == 0:
        return [0.0, 0.0]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(max(0.0, c - h) * 100, 2), round(min(1.0, c + h) * 100, 2)]


def stat(k, n):
    return {"n": n, "successes": k, "asr_pct": round(100 * k / n, 2), "ci95": wilson(k, n)}


def main():
    recs = [json.loads(l) for l in open(RECORDS, encoding="utf-8") if l.strip()]
    g = [r for r in recs if r["arm"] == "BAA_LOCAL" and r.get("ok")]
    assert len(g) == 280, len(g)
    rows = []
    for r in g:
        m = precheck(r["query"])
        rows.append({"uid": r["uid"], "family": r["family"], "angle": r.get("angle"),
                     "prompt_success": bool(r["attack_succeeded"]),
                     "t0": m[0].value if m else None,
                     "pipeline_success": bool(r["attack_succeeded"]) and m is None})
    ps = sum(x["prompt_success"] for x in rows)
    assert ps == 30, ps
    pl = sum(x["pipeline_success"] for x in rows)
    bn = [x for x in rows if x["family"] in BN]

    fam = collections.defaultdict(lambda: [0, 0, 0, 0])  # n, prompt_succ, t0_hits, pipe_succ
    for x in rows:
        f = fam[x["family"]]
        f[0] += 1; f[1] += x["prompt_success"]; f[2] += x["t0"] is not None; f[3] += x["pipeline_success"]
    ang = collections.defaultdict(lambda: [0, 0, 0])
    for x in rows:
        if x["angle"]:
            a = ang[x["angle"]]; a[0] += 1; a[1] += x["prompt_success"]; a[2] += x["pipeline_success"]

    farmer = json.load(open(FARMER, encoding="utf-8"))
    fb = [(x["query_id"], x["query"], precheck(x["query"])) for x in farmer]
    fb_hits = [{"id": i, "query": q, "category": m[0].value, "rules": list(m[1])} for i, q, m in fb if m]
    ban = [x for x in json.load(open(BANGLISH, encoding="utf-8")) if x["target_type"] != "adversarial"]
    bb_hits = [{"id": x["id"], "query": x["query"], "category": precheck(x["query"])[0].value}
               for x in ban if precheck(x["query"])]

    try:
        head = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        head = None
    out = {
        "experiment": "N14b_t0_pipeline_replay",
        "provenance": {"git_head": head,
                       "records": RECORDS.name,
                       "records_sha256": hashlib.sha256(RECORDS.read_bytes()).hexdigest(),
                       "model_calls": 0,
                       "note": "Replay of frozen N14 guarded responses; only the T0 decision is new. T4 not applied."},
        "guarded_prompt_only": stat(ps, 280),
        "t0_plus_guarded": stat(pl, 280),
        "bengali100": {"guarded_prompt_only": stat(sum(x["prompt_success"] for x in bn), len(bn)),
                       "t0_plus_guarded": stat(sum(x["pipeline_success"] for x in bn), len(bn))},
        "t0_interceptions": {"n": sum(x["t0"] is not None for x in rows),
                             "by_category": dict(collections.Counter(x["t0"] for x in rows if x["t0"])),
                             "successful_attacks_blocked_by_t0": [x["uid"] for x in rows if x["prompt_success"] and x["t0"]]},
        "per_family": {k: {"n": v[0], "prompt_successes": v[1], "t0_blocked": v[2], "pipeline_successes": v[3]}
                       for k, v in sorted(fam.items())},
        "per_n12_angle": {k: {"n": v[0], "prompt_successes": v[1], "pipeline_successes": v[2]}
                          for k, v in sorted(ang.items())},
        "benign_false_blocks": {"farmer": f"{len(fb_hits)}/{len(fb)}", "banglish_benign": f"{len(bb_hits)}/{len(ban)}",
                                "farmer_cases": fb_hits, "banglish_cases": bb_hits},
        "remaining_pipeline_successes": [x for x in rows if x["pipeline_success"]],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k not in ("remaining_pipeline_successes",)}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
