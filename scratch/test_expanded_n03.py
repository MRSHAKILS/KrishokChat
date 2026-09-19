#!/usr/bin/env python3
"""Expanded N03 dosage verifier benchmark on 250+ authentic answers.

Combines:
1. Live generated answers from OpenRouter/gemini-2.5-flash-lite with retrieved sources.
2. Authentic BARI/BRRI/DAE research handbook advisory answers grounded in official knowledge nodes.

Evaluates:
- Clean FP rate
- 4 mutation types: dose_x2, dose_div2, unit_swap, chemical_swap
- Strict catch rate + precise sentence catch rate
- Wilson 95% confidence intervals
"""
import json
import os
import random
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE_ROOT = Path("d:/KrishokChat Advisory System")
sys.path.insert(0, str(WORKSPACE_ROOT / "backend"))

from app.application.verifier import HardenedDosageVerifier
from app.core.config import Settings
from app.domain.contracts import RetrievedSource
from app.infrastructure.verification.dosage_claims import extract_claims, _UNIT_ALIASES
from app.infrastructure.verification.normalization import normalize_chemical
from app.infrastructure.verification.dose_reference import load_dose_reference

OUT_DIR = WORKSPACE_ROOT / "paper" / "EACL Final" / "experiments" / "results"
NODES_PATH = WORKSPACE_ROOT / "backend" / "ml_assets" / "rag_index" / "processed" / "knowledge_nodes_clean.jsonl"
DOSE_REF = WORKSPACE_ROOT / "backend" / "ml_assets" / "rag_index" / "derived" / "dose_reference_v1.json"

BN_DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")
EN_DIGITS_BACK = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
NUM_RE = re.compile(r"(?P<num>[০-৯0-9]+(?:[.,][০-৯0-9]+)?)\s*(?P<unit>ml|mg|\bg\b|kg|\bl\b|liter|litre|মিলি|গ্রাম|লিটার|কেজি|ইসি|ডব্লিউপি|EC|WP|SC|SL|শতক|বিঘা|একর)", re.IGNORECASE)
UNIT_SWAP = {
    "ml": "g", "g": "ml", "l": "kg", "kg": "l",
    "মিলি": "গ্রাম", "গ্রাম": "মিলি", "লিটার": "কেজি", "কেজি": "লিটার",
    "EC": "WP", "WP": "EC", "ইসি": "ডব্লিউপি", "ডব্লিউপি": "ইসি"
}

def to_float(num: str) -> float:
    return float(num.translate(BN_DIGITS).replace(",", "."))

def fmt_like(value: float, template: str) -> str:
    text = "%g" % value
    if any(c in "০১২৩৪৫৬৭৮৯" for c in template):
        text = text.translate(EN_DIGITS_BACK)
    if "," in template and "." in text:
        text = text.replace(".", ",")
    return text

def match_case(replacement: str, template: str) -> str:
    if template[:1].isupper() and template[1:2].islower():
        return replacement[:1].upper() + replacement[1:].lower()
    if template.isupper():
        return replacement.upper()
    return replacement.lower()

def wilson_ci(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    margin = (z / denom) * ((p * (1 - p) / n + z**2 / (4 * n**2)) ** 0.5)
    low = max(0.0, center - margin) * 100.0
    high = min(1.0, center + margin) * 100.0
    return (round(low, 1), round(high, 1))

def main():
    settings = Settings()
    verifier = HardenedDosageVerifier(
        dose_reference=load_dose_reference(settings.dose_reference_resolved_path, settings.dose_outlier_factor)
    )

    nodes = {}
    with open(NODES_PATH, encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
                if r.get("id"):
                    nodes[r["id"]] = r
            except json.JSONDecodeError:
                continue

    actives = sorted({e["active"] for e in json.load(open(DOSE_REF, encoding="utf-8"))["entries"]})

    def to_source(node: dict) -> RetrievedSource:
        return RetrievedSource(
            id=str(node.get("id", "")),
            score=0.0,
            title_en=str(node.get("title_en", "")),
            title_bn=str(node.get("title_bn", "")),
            content_en=str(node.get("content_en", "")),
            content_bn=str(node.get("content_bn", "")),
            source=str(node.get("source_document", "")),
            citation=str(node.get("citation", "")),
            metadata={"section_title": node.get("section_title", "")},
        )

    # Gather candidate answers
    candidates = []

    # 1. Live answers from r1
    r1_path = OUT_DIR / "n03_catchrate_20260917.jsonl"
    if r1_path.exists():
        for l in open(r1_path, encoding="utf-8"):
            r = json.loads(l)
            if r.get("stage") == "scored" and r.get("clean_answer"):
                candidates.append({
                    "id": f"live_r1_{len(candidates)}",
                    "source_type": "live_generation",
                    "answer": r["clean_answer"],
                    "source_ids": r.get("source_ids", []),
                    "active": r.get("active", "")
                })

    # 2. Live answers from r2
    r2_path = OUT_DIR / "n03c_extend_20260917.jsonl"
    if r2_path.exists():
        for l in open(r2_path, encoding="utf-8"):
            r = json.loads(l)
            if r.get("ok") and r.get("n_dosed", 0) > 0 and r.get("answer"):
                candidates.append({
                    "id": f"live_r2_{len(candidates)}",
                    "source_type": "live_generation",
                    "answer": r["answer"],
                    "source_ids": r.get("source_ids", []),
                    "active": r.get("qid", "")
                })

    # 3. Official BARI/BRRI/DAE handbook nodes with explicit rate-context dosage claims
    for nid, node in nodes.items():
        text = node.get("content_bn", "")
        claims = [c for c in extract_claims(text) if c.has_dosage and c.amounts]
        valid_claims = [c for c in claims if re.search(r"প্রতি|per\b|/ ?[Ll]|/ ?ha|হেক্টর|শতক|পানিতে|হারে", c.sentence)]
        if valid_claims:
            candidates.append({
                "id": f"handbook_{nid}",
                "source_type": "official_handbook",
                "answer": valid_claims[0].sentence,
                "source_ids": [nid],
                "active": valid_claims[0].chemicals[0] if valid_claims[0].chemicals else "dosage_rate"
            })

    print(f"Total raw candidates: {len(candidates)}")

    # Deduplicate by answer text
    seen_answers = set()
    deduped = []
    for c in candidates:
        ans_norm = " ".join(c["answer"].split())
        if ans_norm not in seen_answers:
            seen_answers.add(ans_norm)
            deduped.append(c)

    print(f"Total unique candidates: {len(deduped)}")

    # Limit to 250 high quality items for balance and speed
    eval_set = deduped[:250]
    print(f"Evaluating on {len(eval_set)} items...")

    per_type = {}
    clean_fp = 0
    scored_items = []

    for item in eval_set:
        sources = [to_source(nodes[i]) for i in item.get("source_ids", []) if i in nodes]
        clean = verifier.verify(item["answer"], sources)
        is_clean_fp = clean.unsupported_count > 0
        if is_clean_fp:
            clean_fp += 1

        claims = extract_claims(item["answer"])
        # Find first grounded dose-bearing claim
        target = None
        for c, v in zip(claims, clean.claims):
            if c.has_dosage and v.verdict == "grounded":
                target = c
                break

        muts = {}
        mut_sents = {}
        invalid = []

        if target is not None and not re.search(r"প্রতি|per\b|/ ?[Ll]|/ ?ha|হেক্টর|শতক|পানিতে|হারে", item["answer"][target.start:target.end]):
            invalid.append("no-rate-context")
            target = None

        if target is not None:
            sent = item["answer"][target.start:target.end]
            sent_claims = [c for c in extract_claims(sent) if c.has_dosage]
            base_amounts = [(a, u) for c in sent_claims for (a, u) in list(c.amounts) + list(c.fractions)]

            def valid(mtext: str) -> bool:
                if mtext[target.start:target.end] == sent:
                    return False
                try:
                    post = extract_claims(mtext[target.start:target.end])
                except Exception:
                    return False
                return any(c.has_dosage for c in post)

            if base_amounts:
                value, unit = base_amounts[0]
                anchor = None
                for tok in re.findall(r"[০-৯0-9]+(?:[.,][০-৯0-9]+)?", sent):
                    try:
                        if abs(to_float(tok) - value) < 1e-9:
                            anchor = tok
                            break
                    except ValueError:
                        continue

                if anchor:
                    # dose_x2
                    cand = sent.replace(anchor, fmt_like(value * 2, anchor), 1)
                    full = item["answer"][:target.start] + cand + item["answer"][target.end:]
                    if valid(full):
                        muts["dose_x2"] = full
                        mut_sents["dose_x2"] = cand

                    # dose_div2
                    cand = sent.replace(anchor, fmt_like(value / 2, anchor), 1)
                    full = item["answer"][:target.start] + cand + item["answer"][target.end:]
                    if valid(full):
                        muts["dose_div2"] = full
                        mut_sents["dose_div2"] = cand

                # unit_swap
                surf_unit = None
                for tok in re.findall(r"[\w\u0980-\u09FF]+", sent):
                    try:
                        canon = _UNIT_ALIASES.get(tok.lower(), tok.lower())
                    except Exception:
                        canon = tok.lower()
                    if canon == unit.lower():
                        surf_unit = tok
                        break

                if surf_unit and UNIT_SWAP.get(surf_unit):
                    cand = sent.replace(surf_unit, UNIT_SWAP[surf_unit], 1)
                    full = item["answer"][:target.start] + cand + item["answer"][target.end:]
                    if valid(full):
                        muts["unit_swap"] = full
                        mut_sents["unit_swap"] = cand

            # chemical_swap
            chems = list(getattr(target, "chemicals", []) or [])
            GENERIC = {"সার", "কীটনাশক", "ওষুধ", "ঔষধ", "পোকা", "রোগ", "সার,"}
            specific = [c for c in chems if c not in GENERIC]
            chem_key = (specific or chems)[0] if (specific or chems) else None
            if chem_key:
                alts = [a for a in actives if a.lower() not in sent.lower()]
                if alts:
                    alt = random.Random(42).choice(alts)
                    new_sent = sent
                    for _ in range(20):
                        replaced = False
                        for tok in re.findall(r"[\w\u0980-\u09FF]+(?:[-/][\w\u0980-\u09FF]+)*", new_sent):
                            try:
                                same = normalize_chemical(tok) == chem_key
                            except Exception:
                                same = False
                            if same:
                                new_sent = new_sent.replace(tok, match_case(alt, tok), 1)
                                replaced = True
                                break
                        if not replaced:
                            break
                    full = item["answer"][:target.start] + new_sent + item["answer"][target.end:]
                    if new_sent != sent and valid(full):
                        muts["chemical_swap"] = full
                        mut_sents["chemical_swap"] = new_sent

        row = {
            "id": item["id"],
            "source_type": item["source_type"],
            "clean_fp": is_clean_fp,
            "mutations_applied": sorted(muts.keys()),
            "mutations": {}
        }

        for mtype, mtext in muts.items():
            v = verifier.verify(mtext, sources)
            flagged_texts = [x.text for x in v.claims if x.verdict == "unsupported"]
            mut_sent = mut_sents.get(mtype, "")
            precise = any(mut_sent.strip() == ft.strip() or (len(mut_sent.strip()) > 40 and mut_sent.strip()[:40] in ft) for ft in flagged_texts) if mut_sent else False

            row["mutations"][mtype] = {
                "unsupported": v.unsupported_count,
                "caught_strict": v.unsupported_count > 0,
                "caught_precise": precise
            }

            per_type.setdefault(mtype, {"n": 0, "caught": 0, "precise": 0})
            per_type[mtype]["n"] += 1
            if v.unsupported_count > 0:
                per_type[mtype]["caught"] += 1
            if precise:
                per_type[mtype]["precise"] += 1

        scored_items.append(row)

    print("\n=== BENCHMARK RESULTS ===")
    print(f"Total Answers Evaluated: {len(eval_set)}")
    print(f"Clean False Positives: {clean_fp}/{len(eval_set)} ({clean_fp/len(eval_set)*100:.2f}%) CI: {wilson_ci(clean_fp, len(eval_set))}")

    summary = {}
    for mtype, stats in sorted(per_type.items()):
        ci = wilson_ci(stats["caught"], stats["n"])
        p_ci = wilson_ci(stats["precise"], stats["n"])
        rate = stats["caught"] / stats["n"] * 100
        p_rate = stats["precise"] / stats["n"] * 100
        summary[mtype] = {
            "n": stats["n"],
            "caught": stats["caught"],
            "rate_pct": round(rate, 2),
            "ci95": ci,
            "precise": stats["precise"],
            "precise_pct": round(p_rate, 2),
            "precise_ci95": p_ci
        }
        print(f"{mtype:15s}: n={stats['n']:3d} | caught={stats['caught']:3d} ({rate:5.1f}% CI: {ci}) | precise={stats['precise']:3d} ({p_rate:5.1f}% CI: {p_ci})")

if __name__ == "__main__":
    main()
