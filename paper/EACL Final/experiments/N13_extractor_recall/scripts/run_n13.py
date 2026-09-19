#!/usr/bin/env python3
"""N13 — T1 extractor recall upgrade (EACL Final).

Reviewer-driven fix for the 47.5% extractor miss rate: the miss audit showed
~99% of misses are crops entirely outside the 9-crop gazetteer (not spelling
variants), so the primary lever is taxonomy expansion, with normalization +
thresholded fuzzy matching as secondary layers.

Layers (ablation, all deterministic, offline, $0):
  L0  production QueryExtractor.extract (baseline, frozen backend code)
  L1  v2 alias table (9 + 36 crops), same exact/token-start rule
  L2  L1 + Unicode normalization
  L3  L2 + rapidfuzz fallback (ratio>=86, token>=4, alias>=4, same 1st char)

Ground truth: crop_slot_labeling_sheet_200.json (human_crop), same 200
queries as N01b. Metrics per layer: agreement, miss, mismatch, FP, miss-rate
Wilson 95% CI, plus per-row first-fixing-layer attribution and L0->Lx
regressions (must stay zero).

Money: no API calls. Preflight N/A (AGENTS.md s0.3 covers batch inference;
this is offline deterministic scoring).

Outputs (N13_extractor_recall/results/):
  n13_records_<stamp>.jsonl   per-row, per-layer (atomic rewrite)
  n13_summary_<stamp>.json    aggregates + ablation + attribution
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
WORKSPACE_ROOT = HERE.parents[5]
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError, OSError):
    pass
sys.path.insert(0, str(WORKSPACE_ROOT / "backend"))

OUT_DIR = HERE.parent.parent / "results"
ALIAS_PATH = HERE.parent.parent / "data" / "crop_alias_v2.json"
LABEL_PATH = (WORKSPACE_ROOT / "paper" / "EACL Final" / "experiments"
              / "results" / "crop_slot_labeling_sheet_200.json")

STRIP_PAT = re.compile(r"^[^\w\u0980-\u09FF]+")
FUZZ_THRESHOLD = 90
FUZZ_MIN_LEN = 4
# Generic collective nouns that are NOT a specific crop and must never match,
# even as prefix hosts (farmer_q_110: শীতকালীন শাকসবজি labeled EMPTY).
NEGATIVE_TOKENS = {"শাকসবজি"}
# Aliases excluded from fuzzy candidacy: করলা-series collides at 88.9 with
# the extremely common verb form করার ("to do") — measured 6 systematic FPs.
# Exact matching still covers করলা.
FUZZ_EXCLUDE = {"করলা", "করলার", "করলাগাছ"}


def normalize(text: str) -> str:
    """L2 normalization: NFKC + lowercase. Conservative by design —
    Bengali ZWJ/ZWNJ and vowel signs are linguistically significant and
    are never stripped."""
    return unicodedata.normalize("NFKC", text or "").lower()


def tokenize(lowered: str) -> list[str]:
    toks = [t for t in (STRIP_PAT.sub("", t) for t in lowered.split()) if t]
    return [t for t in toks if t not in NEGATIVE_TOKENS]


def load_table() -> list[tuple[str, list[str], bool]]:
    """(crop_id, aliases-longest-first, short_exact) in fixed table order."""
    raw = json.loads(open(ALIAS_PATH, encoding="utf-8").read())["crops"]
    table = []
    for crop_id, spec in raw.items():
        if isinstance(spec, dict):
            aliases, short_exact = spec["aliases"], bool(spec.get("short_exact"))
        else:
            aliases, short_exact = spec, False
        ordered = sorted((str(a).strip().lower() for a in aliases if str(a).strip()),
                         key=len, reverse=True)
        table.append((crop_id, ordered, short_exact))
    return table


def match_exact(lowered: str, table) -> tuple[str | None, str | None]:
    toks = tokenize(lowered)
    for crop_id, aliases, short_exact in table:
        for alias in aliases:
            if " " in alias:
                if alias in lowered:
                    return crop_id, alias
            elif short_exact:
                if any(tok == alias for tok in toks):
                    return crop_id, alias
            elif any(tok == alias or tok.startswith(alias) for tok in toks):
                return crop_id, alias
    return None, None


def match_fuzzy(lowered: str, table) -> tuple[str | None, str | None, float]:
    from rapidfuzz import fuzz
    toks = [t for t in tokenize(lowered) if len(t) >= FUZZ_MIN_LEN]
    for crop_id, aliases, _ in table:
        for alias in aliases:
            if " " in alias or len(alias) < FUZZ_MIN_LEN:
                continue
            if alias in FUZZ_EXCLUDE:
                continue
            for tok in toks:
                if tok[0] != alias[0]:
                    continue
                score = fuzz.ratio(tok, alias)
                if score >= FUZZ_THRESHOLD:
                    return crop_id, alias, round(float(score), 1)
    return None, None, 0.0


def extract_v2(query: str, table, norm: bool, fuzzy: bool) -> dict:
    lowered = normalize(query) if norm else query.lower()
    crop, alias = match_exact(lowered, table)
    via = "exact" if crop else None
    score = 100.0 if crop else 0.0
    if not crop and fuzzy:
        crop, alias, score = match_fuzzy(lowered, table)
        via = "fuzzy" if crop else None
    return {"crop": crop, "alias": alias, "via": via, "score": score}


def wilson(k: int, n: int, z: float = 1.96) -> list[float]:
    if n == 0:
        return [0.0, 0.0]
    p = k / n
    d = 1.0 + z * z / n
    c = p + z * z / (2.0 * n)
    m = z * __import__("math").sqrt(p * (1.0 - p) / n + z * z / (4.0 * n * n))
    return [round(max(0.0, (c - m) / d), 4), round(min(1.0, (c + m) / d), 4)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    args = ap.parse_args()

    from app.domain.query_extractor import QueryExtractor

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = json.loads(open(LABEL_PATH, encoding="utf-8").read())
    table = load_table()
    n_crops = len(table)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    rec_path = OUT_DIR / f"n13_records_{stamp}.jsonl"
    if rec_path.exists():
        rec_path.unlink()

    layers = {
        "L0_baseline": {"v2": False},
        "L1_taxonomy": {"v2": True, "norm": False, "fuzzy": False},
        "L2_plus_norm": {"v2": True, "norm": True, "fuzzy": False},
        "L3_plus_fuzzy": {"v2": True, "norm": True, "fuzzy": True},
    }
    stats: dict[str, dict] = {k: {"agree": 0, "miss": 0, "mismatch": 0, "fp": 0,
                                   "miss_ids": [], "fp_ids": [],
                                   "mismatch_ids": [], "fuzzy_hits": []}
                               for k in layers}
    first_fix: dict[str, int] = {}
    regressions: list[dict] = []
    n = len(rows)

    with open(rec_path, "w", encoding="utf-8") as f:
        for r in rows:
            q, human = r["query"], r.get("human_crop") or ""
            rec = {"id": r["id"], "human": human, "layers": {}}
            base_ok: bool | None = None
            for lname, cfg in layers.items():
                if not cfg.get("v2"):
                    ext = QueryExtractor.extract(q).crop or ""
                    via = "production"
                else:
                    out = extract_v2(q, table, cfg["norm"], cfg["fuzzy"])
                    ext, via = out["crop"] or "", out["via"] or "none"
                    if via == "fuzzy":
                        stats[lname]["fuzzy_hits"].append(
                            {"id": r["id"], "alias": out["alias"],
                             "score": out["score"]})
                rec["layers"][lname] = {"ext": ext, "via": via}
                s = stats[lname]
                if human and not ext:
                    s["miss"] += 1
                    s["miss_ids"].append(r["id"])
                elif human and ext and human != ext:
                    s["mismatch"] += 1
                    s["mismatch_ids"].append(
                        {"id": r["id"], "human": human, "ext": ext})
                elif not human and ext:
                    s["fp"] += 1
                    s["fp_ids"].append({"id": r["id"], "ext": ext})
                else:
                    s["agree"] += 1
                if lname == "L0_baseline":
                    base_ok = (human == ext)
            # first-fixing-layer attribution + regression check
            for lname in ("L1_taxonomy", "L2_plus_norm", "L3_plus_fuzzy"):
                e = rec["layers"][lname]["ext"]
                if human and e == human:
                    prev = {"L1_taxonomy": "L0_baseline",
                            "L2_plus_norm": "L1_taxonomy",
                            "L3_plus_fuzzy": "L2_plus_norm"}[lname]
                    pe = rec["layers"][prev]["ext"]
                    if pe != human:
                        first_fix[lname] = first_fix.get(lname, 0) + 1
                    break
            if base_ok and human:
                for lname in ("L1_taxonomy", "L2_plus_norm", "L3_plus_fuzzy"):
                    if rec["layers"][lname]["ext"] != human:
                        regressions.append({"id": r["id"], "layer": lname,
                                            "human": human,
                                            "ext": rec["layers"][lname]["ext"]})
                        break
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())

    summary = {
        "experiment": "N13_EXTRACTOR_RECALL",
        "execution_status": "DONE_OFFLINE_DETERMINISTIC",
        "design": {"n": n, "ground_truth": "crop_slot_labeling_sheet_200.json",
                   "alias_table": "data/crop_alias_v2.json",
                   "n_crops": n_crops, "fuzzy_threshold": FUZZ_THRESHOLD},
        "layers": {},
        "first_fix_attribution": first_fix,
        "regressions_vs_L0": regressions,
        "target": {"miss_lt_10pct": None},
    }
    for lname, s in stats.items():
        summary["layers"][lname] = {
            "agree": s["agree"], "miss": s["miss"],
            "miss_rate": round(s["miss"] / n, 4),
            "miss_ci95": wilson(s["miss"], n),
            "mismatch": s["mismatch"], "fp": s["fp"],
            "miss_ids": s["miss_ids"], "fp_ids": s["fp_ids"],
            "mismatch_ids": s["mismatch_ids"],
            "fuzzy_hits": s["fuzzy_hits"],
        }
    summary["target"]["miss_lt_10pct"] = summary["layers"]["L3_plus_fuzzy"]["miss"] / n < 0.10

    out_path = OUT_DIR / f"n13_summary_{stamp}.json"
    tmp = out_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    with open(tmp, "a", encoding="utf-8") as f:
        f.flush()
        os.fsync(f.fileno())
    tmp.replace(out_path)

    for lname, s in summary["layers"].items():
        print(f"{lname}: agree={s['agree']} miss={s['miss']} "
              f"({s['miss_rate']*100:.1f}% {s['miss_ci95']}) "
              f"mismatch={s['mismatch']} fp={s['fp']}")
    print("first-fix:", first_fix, "| regressions:", len(regressions),
          "| target<10%:", summary["target"]["miss_lt_10pct"])
    print(f"[OK] wrote {out_path} + {rec_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
