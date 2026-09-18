#!/usr/bin/env python3
"""N03b: offline re-verification of stored live answers, all 4 mutation types (EACL Final).

The main N03 run's chemical_swap inserted lowercase English names that the
claim detector (capital-sensitive _EN_CHEM_RE) cannot see, so 0/12 measured
the mutation, not the verifier. This pass redoes ALL FOUR types offline ($0)
on the stored live answers (all <=1478 chars, complete) with case-preserved
chemical replacement, refetching source contents by id from the frozen nodes.

Outputs: experiments/results/n03b_alltypes_<date>.json (+ .jsonl).
"""
from __future__ import annotations

import json
import os
import random
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
WORKSPACE_ROOT = HERE.parents[5]
sys.path.insert(0, str(WORKSPACE_ROOT / "backend"))
sys.path.insert(0, str(WORKSPACE_ROOT / "paper" / "EACL Demo" / "experiments" / "shared"))

import _qa_harness as H  # noqa: E402
from app.application.verifier import HardenedDosageVerifier  # noqa: E402
from app.core.config import Settings  # noqa: E402
from app.domain.contracts import RetrievedSource  # noqa: E402
from app.infrastructure.verification.dosage_claims import extract_claims  # noqa: E402
from app.infrastructure.verification.normalization import normalize_chemical  # noqa: E402
from app.infrastructure.verification.dose_reference import load_dose_reference  # noqa: E402

OUT_DIR = WORKSPACE_ROOT / "paper" / "EACL Final" / "experiments" / "results"
REC_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else OUT_DIR / "n03_catchrate_20260917.jsonl"
OUT_PREFIX = sys.argv[2] if len(sys.argv) > 2 else "n03b_alltypes"
NODES_PATH = WORKSPACE_ROOT / "backend" / "ml_assets" / "rag_index" / "processed" / "knowledge_nodes_clean.jsonl"
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
    text = "%g" % value
    if any(c in "০১২৩৪৫৬৭৮৯" for c in template):
        text = text.translate(EN_DIGITS_BACK)
    if "," in template and "." in text:
        text = text.replace(".", ",")
    return text


def match_case(replacement: str, template: str) -> str:
    """Shape the replacement like the original token (Title/lower/upper)."""
    if template[:1].isupper() and template[1:2].islower():
        return replacement[:1].upper() + replacement[1:].lower()
    if template.isupper():
        return replacement.upper()
    return replacement.lower()


def append_jsonl(path: Path, record: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def main() -> int:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = OUT_DIR / f"{OUT_PREFIX}_{stamp}.json"
    rec_path = OUT_DIR / f"{OUT_PREFIX}_{stamp}.jsonl"
    if rec_path.exists():
        rec_path.unlink()

    settings = Settings()
    verifier = HardenedDosageVerifier(
        dose_reference=load_dose_reference(settings.dose_reference_resolved_path,
                                           settings.dose_outlier_factor))
    nodes: dict[str, dict] = {}
    with open(NODES_PATH, encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("id"):
                nodes[r["id"]] = r
    actives = sorted({e["active"] for e in
                      json.load(open(DOSE_REF, encoding="utf-8"))["entries"]})

    def to_source(node: dict) -> RetrievedSource:
        return RetrievedSource(
            id=str(node.get("id", "")), score=0.0,
            title_en=str(node.get("title_en", "")), title_bn=str(node.get("title_bn", "")),
            content_en=str(node.get("content_en", "")), content_bn=str(node.get("content_bn", "")),
            source=str(node.get("source_document", "")), citation=str(node.get("citation", "")),
            metadata={"section_title": node.get("section_title", "")})

    recs = [json.loads(l) for l in open(REC_PATH, encoding="utf-8")]
    scored = [r for r in recs if r.get("stage") == "scored"]
    per_type: dict[str, dict[str, int]] = {}
    fp = 0
    for r in scored:
        sources = [to_source(nodes[i]) for i in r.get("source_ids", []) if i in nodes]
        clean = verifier.verify(r["clean_answer"], sources)
        if clean.unsupported_count > 0:
            fp += 1
        claims = extract_claims(r["clean_answer"])
        # Anchor target: first GROUNDED dose-bearing claim (clean verdicts just
        # computed above). Mutations apply INSIDE its sentence span only.
        target = None
        for c, v in zip(claims, clean.claims):
            if c.has_dosage and v.verdict == "grounded":
                target = c
                break
        muts: dict[str, str] = {}
        mut_sents: dict[str, str] = {}
        invalid: list[str] = []
        # Rate-context gate (fix 2026-09-17d): formulation codes (4G/20EC/57EC)
        # are product labels, not dosage claims. Only sentences with application-
        # rate context (প্রতি/per//L//ha/হেক্টর/শতক/পানিতে/হারে) are valid targets.
        if target is not None and not re.search(
                r"প্রতি|per\b|/ ?[Ll]|/ ?ha|হেক্টর|শতক|পানিতে|হারে",
                r["clean_answer"][target.start:target.end]):
            invalid.append("all:no-rate-context")
            target = None
        if target is not None:
            sent = r["clean_answer"][target.start:target.end]
            sent_claims = [c for c in extract_claims(sent) if c.has_dosage]
            base_amounts = [(a, u) for c in sent_claims for (a, u) in list(c.amounts) + list(c.fractions)]

            def valid(mtext: str) -> bool:
                """Mutated sentence must still parse as a dose claim AND differ."""
                if mtext[target.start:target.end] == sent:
                    return False
                try:
                    post = extract_claims(mtext[target.start:target.end])
                except Exception:  # noqa: BLE001 - unparseable mutation
                    return False
                return any(c.has_dosage for c in post)

            if base_amounts:
                value, unit = base_amounts[0]
                # Surface anchor (fix 2026-09-17d): the parsed value ("%g" ASCII)
                # never matches Bengali-digit surface tokens, producing silent
                # no-op "mutations" the verifier correctly passed. Find the surface
                # token in the span whose parsed value equals the claim value.
                anchor = None
                for tok in re.findall(r"[০-৯0-9]+(?:[.,][০-৯0-9]+)?", sent):
                    try:
                        if abs(to_float(tok) - value) < 1e-9:
                            anchor = tok
                            break
                    except ValueError:
                        continue
                if anchor is None:
                    invalid.append("numeric:no-surface-anchor")
                else:
                    cand = sent.replace(anchor, fmt_like(value * 2, anchor), 1)
                    if valid(r["clean_answer"][:target.start] + cand + r["clean_answer"][target.end:]):
                        muts["dose_x2"] = r["clean_answer"][:target.start] + cand + r["clean_answer"][target.end:]
                        mut_sents["dose_x2"] = cand
                    else:
                        invalid.append("dose_x2:unparseable")
                    cand = sent.replace(anchor, fmt_like(value / 2, anchor), 1)
                    if valid(r["clean_answer"][:target.start] + cand + r["clean_answer"][target.end:]):
                        muts["dose_div2"] = r["clean_answer"][:target.start] + cand + r["clean_answer"][target.end:]
                        mut_sents["dose_div2"] = cand
                    else:
                        invalid.append("dose_div2:unparseable")
                # Surface unit token (same fix): the CLAIM's own unit surface form,
                # not the longest UNIT_SWAP key in the sentence (which hit
                # denominator nouns like লিটার while the dose unit মিলি survived
                # → silent no-op, fix 2026-09-17e).
                surf_unit = None
                for tok in re.findall(r"[\w\u0980-\u09FF]+", sent):
                    try:
                        from app.infrastructure.verification.dosage_claims import (
                            _UNIT_ALIASES as _UA)
                        canon = _UA.get(tok.lower(), tok.lower())
                    except Exception:  # noqa: BLE001
                        canon = tok.lower()
                    if canon == unit.lower():
                        surf_unit = tok
                        break
                if surf_unit and UNIT_SWAP.get(surf_unit):
                    cand = sent.replace(surf_unit, UNIT_SWAP[surf_unit], 1)
                    if valid(r["clean_answer"][:target.start] + cand + r["clean_answer"][target.end:]):
                        muts["unit_swap"] = r["clean_answer"][:target.start] + cand + r["clean_answer"][target.end:]
                        mut_sents["unit_swap"] = cand
                    else:
                        invalid.append("unit_swap:unparseable")
                else:
                    invalid.append("unit_swap:no-surface-unit")
            chems = list(getattr(target, "chemicals", []) or [])
            # Prefer specific chemicals over generic words (সার/কীটনাশক/ওষুধ):
            # generics recur across sentences and never fully swap (2026-09-17e).
            GENERIC = {"সার", "কীটনাশক", "ওষুধ", "ঔষধ", "পোকা", "রোগ", "সার,"}
            specific = [c for c in chems if c not in GENERIC]
            chem_key = (specific or chems)[0] if (specific or chems) else None
            if chem_key:
                alts = [a for a in actives if a.lower() not in sent.lower()]
                if alts:
                    alt = random.Random(42).choice(alts)
                    new_sent = sent
                    # Replace ALL occurrences (fix 2026-09-17e): single replace
                    # left repeated chemical tokens grounding the claim.
                    for _ in range(20):
                        replaced = False
                        for tok in re.findall(r"[\w\u0980-\u09FF]+(?:[-/][\w\u0980-\u09FF]+)*", new_sent):
                            try:
                                same = normalize_chemical(tok) == chem_key
                            except Exception:  # noqa: BLE001 - unknown token shape, skip
                                same = False
                            if same:
                                new_sent = new_sent.replace(tok, match_case(alt, tok), 1)
                                replaced = True
                                break
                        if not replaced:
                            break
                    if new_sent != sent and valid(
                            r["clean_answer"][:target.start] + new_sent + r["clean_answer"][target.end:]):
                        muts["chemical_swap"] = (
                            r["clean_answer"][:target.start] + new_sent
                            + r["clean_answer"][target.end:])
                        mut_sents["chemical_swap"] = new_sent
                    else:
                        invalid.append("chemical_swap:unparseable-or-unchanged")
        row: dict = {"active": r["active"],
                     "clean_fp": clean.unsupported_count > 0,
                     "target_sentence": (r["clean_answer"][target.start:target.end]
                                         if target is not None else None),
                     "invalid_mutations": invalid,
                     "mutations_applied": sorted(muts.keys()), "mutations": {}}
        for mtype, mtext in muts.items():
            v = verifier.verify(mtext, sources)
            # precise: is the MUTATED sentence itself flagged? (uses the recorded
            # mutated sentence, not the clean span — earlier code compared the
            # clean text and undercounted.)
            flagged_texts = [x.text for x in v.claims if x.verdict == "unsupported"]
            mut_sent = mut_sents.get(mtype, "")
            precise = any(mut_sent.strip() == ft.strip() or
                          (len(mut_sent.strip()) > 40 and mut_sent.strip()[:40] in ft)
                          for ft in flagged_texts) if mut_sent else False
            row["mutations"][mtype] = {
                "unsupported": v.unsupported_count,
                "caught_strict": v.unsupported_count > 0,
                "caught_precise": precise,
                "mut_text": mtext[:600],
                "flagged_texts": flagged_texts[:3],
            }
            per_type.setdefault(mtype, {"n": 0, "caught": 0, "caught_precise_n": 0})
            per_type[mtype]["n"] += 1
            if v.unsupported_count > 0:
                per_type[mtype]["caught"] += 1
            if precise:
                per_type[mtype]["caught_precise_n"] += 1
        append_jsonl(rec_path, row)

    summary = {k: {"n": v["n"], "caught": v["caught"],
                   "rate": round(v["caught"] / v["n"], 4) if v["n"] else None,
                   "caught_precise": v.get("caught_precise_n", 0),
                   "precise_rate": round(v.get("caught_precise_n", 0) / v["n"], 4) if v["n"] else None}
               for k, v in sorted(per_type.items())}
    results = {
        "benchmark_name": "EACL_N03B_ALLTYPES_OFFLINE_REVERIFY",
        "execution_status": "DONE_REAL",
        "provenance": H.provenance(HERE, inputs={"records": REC_PATH, "nodes": NODES_PATH}),
        "design": {"n_answers": len(scored),
                   "method": "stored live answers re-verified offline; case-preserved chemical replacement; all 4 types",
                   "verifier": "production-identical (dose reference loaded)"},
        "clean_fp": {"n": len(scored), "flagged": fp,
                     "rate": round(fp / len(scored), 4) if scored else None},
        "catch_rate_strict": summary,
    }
    tmp = out_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(out_path)
    print(json.dumps(summary, indent=2), "| fp:", results["clean_fp"])
    print(f"[OK] wrote {out_path} + {rec_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
