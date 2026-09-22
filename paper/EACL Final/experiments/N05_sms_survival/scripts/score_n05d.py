#!/usr/bin/env python3
"""N05d: SMS compressor with chemical-name slot vs frozen N05c arms (offline, no LLM calls).

Same 100 paired advisories and the SAME frozen dose/chemical detectors as N05c
(imported from score_n05c.py). Arms:
  naive, llm (stored N05c outputs), compressor_v1 (SMS_CHEM_SLOT=0), compressor_v2 (SMS_CHEM_SLOT=1).
Extra metrics: dose+chemical in the same SMS, and SMS segments
(UCS-2: 1 if <=70 chars else ceil(len/67); GSM-7 text: 1 if <=160 else ceil(len/153)).
Output: results/n05d_summary_<date>.json and n05d_records_<date>.jsonl
"""
from __future__ import annotations

import importlib.util
import json
import math
import os
import re
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
spec = importlib.util.spec_from_file_location("n05c", HERE.parent / "score_n05c.py")
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)  # sets sys.path to backend

from app.domain.contracts import QAResult  # noqa: E402
from app.domain.enums import SafetyCategory, VerificationConfidence  # noqa: E402
from app.domain.sms_compressor import SMSCompressor  # noqa: E402

GSM7 = re.compile(r"^[A-Za-z0-9 @£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞÆæßÉ!\"#¤%&'()*+,\-./:;<=>?¡ÄÖÑÜ§¿äöñüà^{}\\\[~\]|€]*$")


def segments(text: str) -> int:
    if GSM7.match(text or ""):
        return 1 if len(text) <= 160 else math.ceil(len(text) / 153)
    return 1 if len(text) <= 70 else math.ceil(len(text) / 67)


def flags(sms: str, gold: str, is_llm=False):
    if is_llm:
        new = C.chem_tokens(sms) - C.chem_tokens(gold)
        chem = bool(new or (C.chem_tokens(sms) & C.chem_tokens(gold)))
    else:
        chem = bool(C.chem_tokens(sms))
    dose = bool(C.DOSE_RE.search(sms))
    return {"len_ok": len(sms) <= 160, "dose": dose, "chem": chem, "both": dose and chem,
            "segments": segments(sms), "len": len(sms)}


def compress(gold, q, on: bool):
    os.environ["SMS_CHEM_SLOT"] = "1" if on else "0"
    qa = QAResult(query=q, category=SafetyCategory.SAFE_AGRI, answer=gold,
                  confidence=VerificationConfidence.VERIFIED)
    return SMSCompressor.compress_from_qa_result(qa, institution="DAE")


def stats(fl, gold_chem_n):
    n = len(fl)
    s = C.arm_stats(fl)
    both = sum(f["both"] for f in fl)
    s.update({"dose_and_chem": both, "dose_and_chem_ci95": C.wilson(both, n),
              "chem_of_gold_with_chem": f"{sum(f['chem'] for f in fl if f['_gold_chem'])}/{gold_chem_n}",
              "segments_mean": round(sum(f["segments"] for f in fl) / n, 2),
              "segments_dist": {k: sum(1 for f in fl if f["segments"] == k) for k in sorted({f["segments"] for f in fl})},
              "len_mean": round(sum(f["len"] for f in fl) / n, 1)})
    return s


def main():
    man = json.load(open(C.OUT_DIR / "n05c_sample_100.json", encoding="utf-8"))
    llm = {}
    for line in open(max(C.OUT_DIR.glob("n05c_records_*.jsonl")), encoding="utf-8"):
        if line.strip():
            r = json.loads(line); llm[r["row_id"]] = r
    arms = {k: [] for k in ("naive", "llm", "compressor_v1", "compressor_v2")}
    recs, hallu_v2 = [], 0
    for rec in man["records"]:
        rid, gold, q = rec["row_id"], rec["gold_answer"] or "", rec["question"]
        lr = llm.get(rid)
        if not lr or not lr.get("ok"):
            continue
        gc = bool(C.chem_tokens(gold))
        avail = 160 - len(C.NAIVE_PREFIX) - len(C.NAIVE_SUFFIX)
        out = {"naive": f"{C.NAIVE_PREFIX}{gold[:avail].strip()}{C.NAIVE_SUFFIX}"[:160],
               "llm": lr["llm_sms"] or "",
               "compressor_v1": compress(gold, q, False),
               "compressor_v2": compress(gold, q, True)}
        for k, sms in out.items():
            f = flags(sms, gold, is_llm=(k == "llm")); f["_gold_chem"] = gc
            arms[k].append(f)
        if (C.dose_pairs(out["compressor_v2"]) - C.dose_pairs(gold)) or (C.chem_tokens(out["compressor_v2"]) - C.chem_tokens(gold)):
            hallu_v2 += 1
        recs.append({"row_id": rid, **out})
    gold_chem_n = sum(1 for f in arms["naive"] if f["_gold_chem"])
    summary = {"experiment": "N05d_sms_chem_slot", "model_calls": 0, "n": len(recs),
               "gold_with_chem": gold_chem_n,
               "arms": {k: stats(v, gold_chem_n) for k, v in arms.items()},
               "compressor_v2_invented_dose_or_chem": hallu_v2,
               "notes": "Frozen N05c detectors. Segments: UCS-2 for Bengali text (70 single / 67 per part)."}
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    (C.OUT_DIR / f"n05d_summary_{stamp}.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(C.OUT_DIR / f"n05d_records_{stamp}.jsonl", "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
