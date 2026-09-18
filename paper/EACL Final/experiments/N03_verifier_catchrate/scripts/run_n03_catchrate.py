#!/usr/bin/env python3
"""N03-lite verifier catch-rate on mutated REAL answers (EACL Final).

Items: 71 dose_reference entries (real actives + registered rates + citations).
Per item: live T3 generation (production container, OpenRouter) of a Bengali
dosage question -> keep answers with >=1 dosage claim (refused/no-claim items
are EXCLUDED with reason, counted, never silently dropped).
Mutations per kept answer (lite, 4 types): dose_x2, dose_div2, unit_swap,
chemical_swap. Verifier (production-identical incl. dose reference) judges
clean + mutated answers against the retrieved sources.

Catch = >=1 unsupported verdict (strict) + mutated-sentence flagged (precise).
FP = unsupported verdict on a clean answer (sample-reviewed to separate
verifier error from generation hallucination).

Money rules: pre-flight auth first (preflight.py); per-record fsync; abort
after >20 consecutive API errors; generation token caps from server Settings.

Outputs (experiments/results/): n03_catchrate_<date>.json (+ .jsonl records).
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
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
DOSE_REF = WORKSPACE_ROOT / "backend" / "ml_assets" / "rag_index" / "derived" / "dose_reference_v1.json"

BN_DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")
EN_DIGITS_BACK = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
NUM_RE = re.compile(r"(?P<num>[০-৯0-9]+(?:[.,][০-৯0-9]+)?)\s*(?P<unit>ml|mg|\bg\b|kg|\bl\b|liter|litre|মিলি|গ্রাম|লিটার|কেজি|ইসি|ডব্লিউপি|EC|WP|SC|SL|শতক|বিঘা|একর)",
                    re.IGNORECASE)
UNIT_SWAP = {"ml": "g", "g": "ml", "l": "kg", "kg": "l", "মিলি": "গ্রাম", "গ্রাম": "মিলি",
             "লিটার": "কেজি", "কেজি": "লিটার", "EC": "WP", "WP": "EC", "ইসি": "ডব্লিউপি", "ডব্লিউপি": "ইসি"}


def to_float(num: str) -> float:
    return float(num.translate(BN_DIGITS).replace(",", "."))


def fmt_like(value: float, template: str) -> str:
    text = ("%g" % value)
    if any(c in "০১২৩৪৫৬৭৮৯" for c in template):
        text = text.translate(EN_DIGITS_BACK)
    if "," in template and "." in text:
        text = text.replace(".", ",")
    return text


def append_jsonl(path: Path, record: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def mutate(answer: str, entry: dict, all_actives: list[str], claims) -> dict[str, str]:
    """Return {mutation_type: mutated_answer} for applicable types.

    Dose/unit swaps target the first numeric dose mention. Chemical swap targets
    the chemical inside the first GROUNDED dose-bearing claim (not the
    elicitation active, which often sits in a no-dosage sentence) — fix
    2026-09-17b after v1 swapped a no-dosage sentence and measured nothing.
    """
    from app.infrastructure.verification.dosage_claims import extract_claims as _ex
    out: dict[str, str] = {}
    m = NUM_RE.search(answer)
    if m:
        val = to_float(m.group("num"))
        unit = m.group("unit")
        out["dose_x2"] = answer.replace(m.group("num"), fmt_like(val * 2, m.group("num")), 1)
        out["dose_div2"] = answer.replace(m.group("num"), fmt_like(val / 2, m.group("num")), 1)
        swap = UNIT_SWAP.get(unit) or UNIT_SWAP.get(unit.lower(), None)
        if swap:
            out["unit_swap"] = re.sub(re.escape(unit), swap, answer, count=1)
    dosed = [c for c in (claims if claims is not None else _ex(answer)) if c.has_dosage]
    target = None
    for c in dosed:
        chems = list(getattr(c, "chemicals", []) or [])
        if chems:
            target = (c.sentence, chems[0])
            break
    if target is None and dosed:
        return out
    if target:
        sent, chem = target
        alts = [a for a in all_actives if a.lower() not in sent.lower()]
        if alts:
            import random as _r
            alt = _r.Random(42).choice(alts)
            out["chemical_swap"] = answer.replace(chem, alt, 1)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-items", type=int, default=71)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = OUT_DIR / f"n03_catchrate_{stamp}.json"
    rec_path = OUT_DIR / f"n03_catchrate_{stamp}.jsonl"
    if rec_path.exists():
        rec_path.unlink()

    from app.core.config import Settings
    from app.application.container import build_container
    from app.application.qa_pipeline import QAInput
    from app.application.verifier import HardenedDosageVerifier
    from app.infrastructure.verification.dose_reference import load_dose_reference
    from app.infrastructure.verification.dosage_claims import extract_claims

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
    os.environ["OPENROUTER_API_KEY"] = key
    settings = Settings(openrouter_api_key=key)
    container = build_container(settings)
    verifier = HardenedDosageVerifier(
        dose_reference=load_dose_reference(settings.dose_reference_resolved_path,
                                           settings.dose_outlier_factor))
    prov_extra = {"model": settings.openrouter_model,
                  "max_output_tokens": settings.llm_max_output_tokens,
                  "temperature": settings.llm_temperature}

    entries = json.load(open(DOSE_REF, encoding="utf-8"))["entries"][:args.max_items]
    all_actives = sorted({e["active"] for e in entries})

    # Resolve a question crop per entry from its source node (title/section,
    # then snippet scan). Entries with no determinable crop are asked cropless
    # (expect clarification) and counted separately. Cropless elicitation is
    # what produced 0 dose claims in the first attempt (41 refusals + 27
    # clarifications on 71 entries) — documented, not hidden.
    from app.domain.intent import _CROP_ALIASES
    TOK_RE = re.compile(r"[\w\u0980-\u09FF]+")

    def node_crops(node: dict) -> set[str]:
        out: set[str] = set()
        for field in ("title_en", "title_bn", "section_title"):
            text = str(node.get(field) or "")
            low = text.lower()
            toks = set(TOK_RE.findall(low))
            for crop, als in _CROP_ALIASES.items():
                for a in als:
                    a = str(a).strip().lower()
                    if not a:
                        continue
                    if (" " in a and a in low) or (" " not in a and a in toks):
                        out.add(crop)
                        break
        return out

    nodes: dict[str, dict] = {}
    try:
        with open(WORKSPACE_ROOT / "backend" / "ml_assets" / "rag_index" / "processed" / "knowledge_nodes_clean.jsonl", encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if r.get("id"):
                    nodes[r["id"]] = r
    except OSError:
        pass

    from app.domain.intent import CROP_NAMES_BN

    def elicitation(entry: dict) -> tuple[str, str | None, str]:
        node = nodes.get(entry.get("node_id", ""), {})
        crops = node_crops(node)
        if len(crops) == 1:
            crop = next(iter(crops))
            return (f"{CROP_NAMES_BN.get(crop, crop)} গাছে {entry['active']} এর অনুমোদিত প্রয়োগমাত্রা কত?",
                    crop, "node_title_section")
        snippet = str(entry.get("snippet") or "")
        slow = snippet.lower()
        stoks = set(TOK_RE.findall(slow))
        for crop, als in _CROP_ALIASES.items():
            for a in als:
                a = str(a).strip().lower()
                if not a:
                    continue
                if (" " in a and a in slow) or (" " not in a and a in stoks):
                    return (f"{CROP_NAMES_BN.get(crop, crop)} গাছে {entry['active']} এর অনুমোদিত প্রয়োগমাত্রা কত?",
                            crop, "node_snippet_scan")
                    break
        return (f"{entry['active']} এর অনুমোদিত প্রয়োগমাত্রা কত?", None, "cropless")

    consec_err = 0

    async def gen_one(entry: dict):
        nonlocal consec_err
        q, qcrop, qsrc = elicitation(entry)
        t0 = time.perf_counter()
        try:
            res = await container.qa.run(QAInput(query=q))
            consec_err = 0
        except Exception as e:  # noqa: BLE001
            consec_err += 1
            if consec_err > 20:
                print("ABORT: >20 consecutive API errors")
                raise SystemExit(2)
            return {"active": entry["active"], "ok": False,
                    "error": type(e).__name__ + ": " + str(e)[:150]}
        latency_ms = round((time.perf_counter() - t0) * 1000, 1)
        claims = extract_claims(res.answer or "")
        dosed = [c for c in claims if c.has_dosage]
        return {"active": entry["active"], "ok": True, "query": q,
                "qcrop": qcrop, "qsrc": qsrc,
                "tier": res.resolution_tier.value, "confidence": res.confidence.value,
                "n_sources": len(res.sources),
                "source_ids": [s.id for s in res.sources],
                "answer": res.answer or "", "latency_ms": latency_ms,
                "n_claims": len(claims), "n_dosed": len(dosed),
                "_sources": list(res.sources), "_entry": entry}

    async def run_all():
        out = []
        for i, e in enumerate(entries):
            out.append(await gen_one(e))
            if (i + 1) % 10 == 0:
                print(f"[{i + 1}/{len(entries)}] generated", flush=True)
        return out

    produced = asyncio.run(run_all())

    # verify clean + mutated
    results_items = []
    for p in produced:
        if not p.get("ok"):
            append_jsonl(rec_path, {**p, "stage": "generation_failed"})
            results_items.append(p)
            continue
        claims = extract_claims(p["answer"])
        dosed = [c for c in claims if c.has_dosage]
        if not dosed:
            append_jsonl(rec_path, {k: v for k, v in p.items() if not k.startswith("_")}
                         | {"stage": "excluded_no_dose_claim",
                            "reason": f"tier={p['tier']} conf={p['confidence']} claims={len(claims)}"})
            results_items.append({"active": p["active"], "stage": "excluded_no_dose_claim"})
            continue
        clean = verifier.verify(p["answer"], p["_sources"])
        row: dict = {"active": p["active"], "stage": "scored",
                     "tier": p["tier"], "confidence": p["confidence"],
                     "n_sources": p["n_sources"], "latency_ms": p["latency_ms"],
                     "clean": {"checked": clean.checked_count, "grounded": clean.grounded_count,
                               "unsupported": clean.unsupported_count,
                               "fp": clean.unsupported_count > 0,
                               "verdicts": [{"text": v.text[:160], "verdict": v.verdict,
                                             "reason": (v.reason or "")[:160]} for v in clean.claims]}}
        muts = mutate(p["answer"], p["_entry"], all_actives, extract_claims(p["answer"]))
        row["mutations_applied"] = sorted(muts.keys())
        row["mutations"] = {}
        for mtype, mtext in muts.items():
            v = verifier.verify(mtext, p["_sources"])
            mut_sentence = mtext  # full mutated answer stored separately on catch
            row["mutations"][mtype] = {
                "unsupported": v.unsupported_count,
                "caught_strict": v.unsupported_count > 0,
                "verdicts": [{"text": x.text[:160], "verdict": x.verdict} for x in v.claims],
            }
        row["mutated_texts"] = {k: v[:2000] for k, v in muts.items()}
        row["clean_answer"] = p["answer"][:2000]
        row["source_ids"] = p["source_ids"]
        append_jsonl(rec_path, row)
        results_items.append(row)

    scored = [r for r in results_items if r.get("stage") == "scored"]
    per_type: dict[str, dict] = {}
    for mtype in ("dose_x2", "dose_div2", "unit_swap", "chemical_swap"):
        aplic = [r for r in scored if mtype in r.get("mutations", {})]
        caught = sum(1 for r in aplic if r["mutations"][mtype]["caught_strict"])
        per_type[mtype] = {"n": len(aplic), "caught": caught,
                           "rate": round(caught / len(aplic), 4) if aplic else None}
    fp_n = sum(1 for r in scored if r["clean"]["fp"])
    results = {
        "benchmark_name": "EACL_N03_VERIFIER_CATCHRATE_LITE",
        "execution_status": "DONE_REAL",
        "provenance": H.provenance(HERE, inputs={"dose_reference": DOSE_REF}),
        "live_config": prov_extra,
        "design": {"n_entries": len(entries), "arms": ["clean"] + ["mut:" + t for t in per_type],
                   "elicitation": "crop-paired (node title/section, else snippet scan, else cropless): '{crop_bn} গাছে {active} এর অনুমোদিত প্রয়োগমাত্রা কত?' (disclosed uniform template)",
                   "elicitation_note": "v1 cropless elicitation yielded 0 dose claims (41 refusals incl. banned actives + 27 clarifications); v2 pairs each entry with its source-node crop so generation can ground"},
        "flow": {"generated_ok": sum(1 for r in produced if r.get("ok")),
                 "excluded_no_dose_claim": sum(1 for r in results_items if r.get("stage") == "excluded_no_dose_claim"),
                 "generation_failed": sum(1 for r in results_items if r.get("stage") == "generation_failed"),
                 "scored": len(scored)},
        "clean_fp": {"n": len(scored), "flagged": fp_n,
                     "rate": round(fp_n / len(scored), 4) if scored else None,
                     "note": "flagged clean answers need sample review (verifier error vs generation hallucination)"},
        "catch_rate_strict": per_type,
    }
    tmp = out_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(out_path)
    print(json.dumps({"flow": results["flow"], "fp": results["clean_fp"],
                      "catch": {k: v for k, v in per_type.items()}}, indent=2, ensure_ascii=False)[:1500])
    print(f"[OK] wrote {out_path} + {rec_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
