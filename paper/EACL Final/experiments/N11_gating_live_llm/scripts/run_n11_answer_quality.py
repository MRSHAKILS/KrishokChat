#!/usr/bin/env python3
"""N11 Answer-Quality Review: 60 live-pass/det-halt rows.

Reviews the 60 queries where live LLM produced a grounded answer but
deterministic gate halted (interactive clarification). Evaluates whether
the live answers are correct, helpful, and safe.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
WORKSPACE_ROOT = HERE.parents[5]
sys.path.insert(0, str(WORKSPACE_ROOT / "backend"))
sys.path.insert(0, str(WORKSPACE_ROOT / "paper" / "EACL Demo" / "experiments" / "shared"))

import _qa_harness as H  # noqa: E402

LIVE_PATH = WORKSPACE_ROOT / "paper" / "EACL Final" / "experiments" / "results" / "n11_live_gating_20260917.jsonl"
DET_PATH = WORKSPACE_ROOT / "paper" / "EACL Final" / "experiments" / "results" / "n01b_records_20260917.jsonl"
OUT_DIR = WORKSPACE_ROOT / "paper" / "EACL Final" / "experiments" / "results"


def load_jsonl(path: Path):
    return [json.loads(l) for l in open(path, encoding="utf-8")]


def evaluate_answer_quality(query: str, answer: str, true_crop: str | None) -> dict:
    """Heuristic quality evaluation for Bengali agricultural answers."""
    if not answer or len(answer.strip()) < 10:
        return {"quality": "empty_or_too_short", "score": 0}
    
    # Check for disease/pest name mention (English or Bengali patterns)
    disease_indicators = [
        "disease", "symptom", "treatment", "spray", "fungicide", "pesticide",
        "bacterial", "fungal", "viral", "blight", "rot", "spot", "wilt", "mildew",
        "rog", "pata", "kora", "bhuri", "dala", "ulta", "mora", "sankramon",  # Bengali romanized
        " ओइडियम", "pectobacterium", "alternaria", "sigatoka", "anthracnose"  # Common pathogens
    ]
    has_disease = any(w in answer.lower() for w in disease_indicators)
    
    # Check for crop mention (if true_crop known)
    crop_mentioned = true_crop and true_crop.lower() in answer.lower() if true_crop else True
    
    # Check for actionable advice (English + Bengali romanized)
    action_indicators = [
        "apply", "spray", "use", "treat", "control", "manage", "prevent", 
        "remove", "destroy", "rotate", "resistant",
        "chara", "dala", "bebohar", "niron", "rokhha", "niyontron",  # Bengali romanized
        "প্রয়োগ", "ছাড়া", "ব্যবহার", "নিরোধ", "রক্ষা", "নিযন্ত্রণ"  # Bengali script
    ]
    has_action = any(w in answer.lower() for w in action_indicators)
    
    # Check for Bangla content (target language)
    has_bangla = any('\u0980' <= c <= '\u09FF' for c in answer)
    
    # Check for structured response (bullet points, numbered lists)
    has_structure = any(c in answer for c in ["*", "•", "১", "২", "৩", "৪", "৫"])
    
    score = 0
    if has_disease: score += 2
    if crop_mentioned: score += 1
    if has_action: score += 2
    if has_bangla: score += 1
    if has_structure: score += 1
    
    if score >= 5:
        quality = "high"
    elif score >= 3:
        quality = "medium"
    else:
        quality = "low"
    
    return {"quality": quality, "score": score, "has_disease": has_disease, 
            "crop_mentioned": crop_mentioned, "has_action": has_action, 
            "has_bangla": has_bangla, "has_structure": has_structure}


def main() -> int:
    import argparse as _ap
    _par = _ap.ArgumentParser()
    _par.add_argument("--det-path", default=str(DET_PATH))
    _det_path = Path(_par.parse_args().det_path)
    live = {r['id']: r for r in load_jsonl(LIVE_PATH)}
    det = {r['id']: r for r in load_jsonl(_det_path)}
    
    rows_to_review = []
    for id_ in det:
        if id_ in live:
            lh = live[id_].get('halted')
            dh = det[id_].get('gated_halted')
            if lh == False and dh == True:
                rows_to_review.append((id_, live[id_], det[id_]))
    
    print(f"Reviewing {len(rows_to_review)} live-pass/det-halt rows...")
    
    results = []
    quality_counts = {"high": 0, "medium": 0, "low": 0, "empty_or_too_short": 0}
    
    for id_, l, d in rows_to_review:
        query = l.get('query', '')
        answer = l.get('answer_preview', '')
        true_crop = d.get('true_crop')
        
        eval_result = evaluate_answer_quality(query, answer, true_crop)
        quality_counts[eval_result["quality"]] = quality_counts.get(eval_result["quality"], 0) + 1
        
        results.append({
            "id": id_,
            "query": query,
            "true_crop": true_crop,
            "live_tier": l.get("tier"),
            "live_answer": answer,
            "det_tier": d.get("gated_tier"),
            "det_reason": d.get("gated_tier"),
            "quality": eval_result
        })
    
    # Write review output
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = OUT_DIR / f"n11_answer_quality_review_{stamp}.json"
    rec_path = OUT_DIR / f"n11_answer_quality_review_{stamp}.jsonl"
    
    # JSON summary
    summary = {
        "benchmark_name": "EACL_N11_ANSWER_QUALITY_REVIEW",
        "execution_status": "DONE_REAL",
        "provenance": H.provenance(HERE, inputs={"live": LIVE_PATH, "det": DET_PATH}),
        "design": {"n": len(rows_to_review), "method": "heuristic evaluation (Bangla presence, disease mention, actionability, crop mention)"},
        "quality_distribution": quality_counts,
        "high_quality_rate": quality_counts["high"] / len(rows_to_review) if rows_to_review else 0,
        "medium_or_above_rate": (quality_counts["high"] + quality_counts["medium"]) / len(rows_to_review) if rows_to_review else 0,
        "note": "Heuristic only — human/Agent review recommended for paper claims. This is Appendix-grade evidence.",
        "results": results
    }
    
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    
    # JSONL records
    with open(rec_path, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            f.flush()
    
    print(f"Quality distribution: {quality_counts}")
    print(f"High quality: {quality_counts['high']}/{len(rows_to_review)} ({quality_counts['high']/len(rows_to_review)*100:.1f}%)")
    print(f"Medium+: {(quality_counts['high']+quality_counts['medium'])/len(rows_to_review)*100:.1f}%")
    print(f"[OK] wrote {out_path} + {rec_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())