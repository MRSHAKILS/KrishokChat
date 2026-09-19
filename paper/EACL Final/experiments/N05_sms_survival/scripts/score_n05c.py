#!/usr/bin/env python3
"""Score N05c — LLM-summarizer vs naive truncation vs deterministic compressor.

Deterministic and FREE ($0): reads the frozen sample manifest +
per-record LLM outputs, recomputes all three arms with the SAME frozen
detectors, and writes the aggregate summary atomically.

Arms (same 100 advisories, paired):
  naive       hard truncation with DAE prefix + helpline suffix (same
              prefix/suffix method as evaluate_sms_survival_84.py)
  llm         stored Gemini-Flash-Lite summaries from run_n05c_llm_summarizer.py
  compressor  deterministic 11-slot SMSCompressor from the gold answer
              (E15 Arm A; QAResult wiring identical to evaluate_sms_survival_84.py)

Metrics per arm: n, length<=160 rate, dose-pattern survival, chemical
survival. LLM-only extras: hallucinated dose pairs and hallucinated
chemicals, where "hallucinated" = a dose (number+unit) or chemical token
present in the summary but absent from the SOURCE advisory (Bengali digits
normalized, bn<->en unit synonyms unified first, so genuine translations
are not counted as hallucinations).

Rates carry Wilson 95% CIs. No pooling across arms; paired by row_id.

Outputs (N05_sms_survival/results/):
  n05c_summary_<stamp>.json
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
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

# Frozen dose definition, mirrored from run_n05_sms.analyze_dose_chemical.
DOSE_RE = re.compile(
    r"[0-9০-৯]+(?:[.,][0-9০-৯]+)?\s*(?:ml|mg|\bg\b|kg|\bl\b|liter|litre|"
    r"মিলি|গ্রাম|লিটার|কেজি|ইসি|ডব্লিউপি|EC|WP|SC|SL|শতক|বিঘা|একর)",
    re.IGNORECASE,
)
# Frozen chemical lexicon, mirrored from evaluate_sms_survival_84.py.
CHEMICALS = (
    "Carbendazim", "Mancozeb", "Imidacloprid", "Cypermethrin", "Chlorpyrifos",
    "Deltamethrin", "Dimethoate", "Fipronil", "Malathion", "Propiconazole",
    "Spinosad", "Tebuconazole", "Cartap", "Carbofuran", "CARBENDAZIM", "MANCOZEB",
    "কার্বেন্ডাজিম", "ম্যানকোজেব", "ইমিডাক্লোপ্রিড", "সাইপারমেথ্রিন",
    "ইউরিয়া", "ইউরিয়া", "পটাশ", "টিএসপি", "ডিএপি", "জিংক", "বোরন",
    "ক্লোরপাইরিফস", "ট্রাইসাইক্লাজল", "ফিপ্রোনিল",
)

# Naive arm: same prefix/suffix framing as evaluate_sms_survival_84.py.
NAIVE_PREFIX = "DAE পরামর্শ: "
NAIVE_SUFFIX = " | হেল্প: ১৬১২৩"

BN_DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")
UNIT_NORM = {
    "মিলি": "ml", "ml": "ml",
    "গ্রাম": "g", "g": "g", "mg": "mg",
    "লিটার": "l", "liter": "l", "litre": "l", "l": "l",
    "কেজি": "kg", "kg": "kg",
    "ইসি": "ec", "ec": "ec",
    "ডব্লিউপি": "wp", "wp": "wp",
    "sc": "sc", "sl": "sl",
    "শতক": "shotok", "বিঘা": "bigha", "একর": "acre",
}
PAIR_RE = re.compile(
    r"([0-9০-৯]+(?:[.,][0-9০-৯]+)?)\s*(ml|mg|\bg\b|kg|\bl\b|liter|litre|"
    r"মিলি|গ্রাম|লিটার|কেজি|ইসি|ডব্লিউপি|EC|WP|SC|SL|শতক|বিঘা|একর)",
    re.IGNORECASE,
)


def dose_pairs(text: str) -> set[tuple[str, str]]:
    """Normalized (number, unit) dose commitments in a text."""
    out: set[tuple[str, str]] = set()
    for m in PAIR_RE.finditer(text or ""):
        num = m.group(1).translate(BN_DIGITS).replace(",", ".")
        unit = UNIT_NORM.get(m.group(2).lower(), m.group(2).lower())
        out.add((num, unit))
    return out


def chem_tokens(text: str) -> set[str]:
    """Chemical lexicon hits (substring match, same as frozen detector).

    One normalization: the lexicon carries two spellings of urea
    (ইউরিয়া / ইউরিয়া). They are unified before matching so a spelling
    variant is never counted as a "new" chemical (autopsy: farmer_q_392).
    """
    t = (text or "").replace("ইউরিয়া", "ইউরিয়া")
    return {c for c in CHEMICALS if c in t}


def wilson(k: int, n: int, z: float = 1.96) -> list[float]:
    if n == 0:
        return [0.0, 0.0]
    p = k / n
    d = 1.0 + z * z / n
    c = p + z * z / (2.0 * n)
    m = z * math.sqrt(p * (1.0 - p) / n + z * z / (4.0 * n * n))
    return [round(max(0.0, (c - m) / d), 4), round(min(1.0, (c + m) / d), 4)]


def arm_stats(flags: list[dict]) -> dict:
    n = len(flags)
    len_ok = sum(1 for f in flags if f["len_ok"])
    dose = sum(1 for f in flags if f["dose"])
    chem = sum(1 for f in flags if f["chem"])
    return {
        "n": n,
        "len_ok": len_ok,
        "len_ok_rate": round(len_ok / n, 4) if n else 0.0,
        "len_ok_ci95": wilson(len_ok, n),
        "dose_survived": dose,
        "dose_rate": round(dose / n, 4) if n else 0.0,
        "dose_ci95": wilson(dose, n),
        "chem_survived": chem,
        "chem_rate": round(chem / n, 4) if n else 0.0,
        "chem_ci95": wilson(chem, n),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--manifest", default=str(OUT_DIR / "n05c_sample_100.json"))
    ap.add_argument("--records", default=None,
                    help="default: newest n05c_records_*.jsonl in results/")
    args = ap.parse_args()

    manifest = json.loads(open(args.manifest, encoding="utf-8").read())
    rec_path = Path(args.records) if args.records else max(
        OUT_DIR.glob("n05c_records_*.jsonl"))
    llm_by_row = {}
    with open(rec_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                r = json.loads(line)
                llm_by_row[r["row_id"]] = r

    from app.domain.contracts import QAResult
    from app.domain.enums import SafetyCategory, VerificationConfidence
    from app.domain.sms_compressor import SMSCompressor

    naive_flags, llm_flags, comp_flags = [], [], []
    hallu_dose_recs, hallu_dose_pairs = 0, 0
    hallu_chem_recs = 0
    skipped = 0
    for rec in manifest["records"]:
        row_id = rec["row_id"]
        gold = rec["gold_answer"] or ""
        lr = llm_by_row.get(row_id)
        if not lr or not lr.get("ok"):
            skipped += 1
            continue

        # Arm 1 — naive truncation (prefix/suffix method, frozen).
        avail = 160 - len(NAIVE_PREFIX) - len(NAIVE_SUFFIX)
        naive_sms = f"{NAIVE_PREFIX}{gold[:avail].strip()}{NAIVE_SUFFIX}"[:160]
        naive_flags.append({
            "len_ok": len(naive_sms) <= 160,
            "dose": bool(DOSE_RE.search(naive_sms)),
            "chem": bool(chem_tokens(naive_sms)),
        })

        # Arm 2 — LLM summary (stored output).
        summary = lr["llm_sms"] or ""
        new_pairs = dose_pairs(summary) - dose_pairs(gold)
        new_chems = chem_tokens(summary) - chem_tokens(gold)
        if new_pairs:
            hallu_dose_recs += 1
            hallu_dose_pairs += len(new_pairs)
        if new_chems:
            hallu_chem_recs += 1
        llm_flags.append({
            "len_ok": len(summary) <= 160,
            "dose": bool(DOSE_RE.search(summary)),
            "chem": bool(new_chems or (chem_tokens(summary) & chem_tokens(gold))),
        })

        # Arm 3 — deterministic 11-slot compressor from the gold answer.
        qa_res = QAResult(
            query=rec["question"],
            category=SafetyCategory.SAFE_AGRI,
            answer=gold,
            confidence=VerificationConfidence.VERIFIED,
        )
        comp_sms = SMSCompressor.compress_from_qa_result(
            qa_res, institution="DAE")
        comp_flags.append({
            "len_ok": len(comp_sms) <= 160,
            "dose": bool(DOSE_RE.search(comp_sms)),
            "chem": bool(chem_tokens(comp_sms)),
        })

    summary = {
        "arm": "N05c_LLM_SUMMARIZER_BASELINE",
        "execution_status": "DONE_DETERMINISTIC_SCORING",
        "design": {
            "n_scored": len(llm_flags),
            "n_skipped_failed_llm": skipped,
            "seed": manifest["seed"],
            "pool_n": manifest["eligibility"]["pool_n"],
            "live_config": manifest["live_config"],
        },
        "files": {
            "manifest": Path(args.manifest).name,
            "records": rec_path.name,
        },
        "arms": {
            "naive_truncation": arm_stats(naive_flags),
            "llm_summarizer": {
                **arm_stats(llm_flags),
                "records_with_hallucinated_dose": hallu_dose_recs,
                "hallucinated_dose_pairs_total": hallu_dose_pairs,
                "records_with_hallucinated_chem": hallu_chem_recs,
            },
            "deterministic_compressor": arm_stats(comp_flags),
        },
        "notes": (
            "Same 100 advisories, paired by row_id; same frozen dose/chemical "
            "detectors for all arms. Hallucinated = dose pair or chemical in "
            "the summary absent from the source advisory (bn digits normalized, "
            "bn<->en units unified). Length claim is characters, never segments."
        ),
    }

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = OUT_DIR / f"n05c_summary_{stamp}.json"
    tmp = out_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    with open(tmp, "a", encoding="utf-8") as f:
        f.flush()
        os.fsync(f.fileno())
    tmp.replace(out_path)

    print(json.dumps(summary["arms"], indent=2, ensure_ascii=False))
    print(f"[OK] wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
