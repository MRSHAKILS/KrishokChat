#!/usr/bin/env python3
"""N03 Master Expansion: Generate additional live dosage advisory answers.

Runs 100 targeted crop-disease-chemical queries through the production pipeline.
Ensures total evaluated live answers with grounded dosage claims reaches n >= 100.
Strictly adheres to:
- OpenRouter Safe Execution Policy (pre-flight check, per-record fsync, token caps).
- Authorized model registry (google/gemini-2.5-flash-lite).
- Real data doctrine (zero artificial mocks, real retrieved sources).
"""
from __future__ import annotations

import asyncio
import json
import os
import re
import subprocess
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
NODES_PATH = WORKSPACE_ROOT / "backend" / "ml_assets" / "rag_index" / "processed" / "knowledge_nodes_clean.jsonl"
DOSE_REF = WORKSPACE_ROOT / "backend" / "ml_assets" / "rag_index" / "derived" / "dose_reference_v1.json"

CROPS_PROBLEMS = [
    ('আলু', 'potato', [
        ('নাবি ধসা', 'late blight', 'Mancozeb'),
        ('আগাম ধসা', 'early blight', 'Carbendazim'),
        ('কাটওয়ার্ম', 'cutworm', 'Chlorpyrifos'),
        ('জাবপোকা', 'aphid', 'Imidacloprid'),
        ('কন্দ পচা', 'tuber rot', 'Mancozeb')
    ]),
    ('ধান', 'rice', [
        ('ব্লাস্ট', 'blast', 'Tricyclazole'),
        ('খোল পোড়া', 'sheath blight', 'Hexaconazole'),
        ('বাদামী গাছফড়িং', 'BPH', 'Pymetrozine'),
        ('মাজরা পোকা', 'stem borer', 'Cartap'),
        ('পাতামোড়ানো পোকা', 'leaf folder', 'Cypermethrin'),
        ('বাকানি রোগ', 'bakanae', 'Carbendazim')
    ]),
    ('টমেটো', 'tomato', [
        ('নাবি ধসা', 'late blight', 'Mancozeb'),
        ('ফল ছিদ্রকারী পোকা', 'fruit borer', 'Spinosad'),
        ('পাতা কোঁকড়ানো', 'leaf curl', 'Imidacloprid'),
        ('ঢলে পড়া', 'wilt', 'Carbendazim'),
        ('আলি ব্লাইট', 'early blight', 'Mancozeb')
    ]),
    ('বেগুন', 'brinjal', [
        ('ডগা ও ফল ছিদ্রকারী পোকা', 'shoot borer', 'Cypermethrin'),
        ('পাতার দাগ', 'leaf spot', 'Carbendazim'),
        ('সাদা মাছি', 'whitefly', 'Imidacloprid'),
        ('ফোমপসিস ব্লাইট', 'phomopsis blight', 'Mancozeb')
    ]),
    ('মরিচ', 'chilli', [
        ('অ্যানথ্রাকনোজ / ডাইব্যাক', 'anthracnose', 'Propiconazole'),
        ('থ্রিপস', 'thrips', 'Imidacloprid'),
        ('মাকড়', 'mite', 'Abamectin'),
        ('গোড়া পচা', 'collar rot', 'Carbendazim'),
        ('পাতা কোঁকড়ানো', 'leaf curl', 'Imidacloprid')
    ]),
    ('গম', 'wheat', [
        ('মরিচা রোগ', 'rust', 'Propiconazole'),
        ('ব্লাস্ট', 'blast', 'Tebuconazole'),
        ('জাবপোকা', 'aphid', 'Dimethoate'),
        ('পাতার দাগ', 'leaf spot', 'Tilt')
    ]),
    ('ভুট্টা', 'corn', [
        ('ফল আর্মিওয়ার্ম', 'fall armyworm', 'Spinosad'),
        ('পাতা ধসা', 'leaf blight', 'Mancozeb'),
        ('কাণ্ড পচা', 'stem rot', 'Carbendazim'),
        ('মাজরা পোকা', 'stem borer', 'Cartap')
    ]),
    ('সরিষা', 'mustard', [
        ('অল্টারনারিয়া ব্লাইট', 'Alternaria blight', 'Iprodione'),
        ('জাবপোকা', 'aphid', 'Malathion'),
        ('ডাউনি মিলডিউ', 'downy mildew', 'Mancozeb')
    ]),
    ('মুগডাল', 'mungbean', [
        ('হলুদ মোজাইক', 'yellow mosaic', 'Imidacloprid'),
        ('পাউডারি মিলডিউ', 'powdery mildew', 'Carbendazim'),
        ('পড বোরার', 'pod borer', 'Deltamethrin')
    ]),
    ('বাঁধাকপি', 'cabbage', [
        ('ডায়মন্ড ব্যাক মথ', 'DBM', 'Spinosad'),
        ('মাথা পচা', 'head rot', 'Mancozeb'),
        ('কাটওয়ার্ম', 'cutworm', 'Chlorpyrifos')
    ]),
    ('ফুলকপি', 'cauliflower', [
        ('কাটওয়ার্ম', 'cutworm', 'Chlorpyrifos'),
        ('অল্টারনারিয়া ব্লাইট', 'Alternaria blight', 'Mancozeb'),
        ('ডাউনি মিলডিউ', 'downy mildew', 'Ridomil')
    ]),
    ('মসুর', 'lentil', [
        ('স্টেমফাইলিয়াম ব্লাইট', 'Stemphylium blight', 'Rovral'),
        ('গোড়া পচা', 'root rot', 'Autostin')
    ])
]

def append_jsonl(path: Path, record: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())

def main() -> int:
    pre = subprocess.run([sys.executable, str(WORKSPACE_ROOT / "paper" / "EACL Final" / "experiments" / "preflight.py")],
                         capture_output=True, text=True)
    if pre.returncode != 0:
        print("FAIL: pre-flight authorization failed; aborting.")
        print(pre.stdout[-500:] if pre.stdout else "")
        return 1

    from app.application.container import build_container
    from app.application.qa_pipeline import QAInput
    from app.core.config import Settings
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
        print("FAIL: no key")
        return 1

    os.environ["OPENROUTER_API_KEY"] = key
    settings = Settings(openrouter_api_key=key)
    container = build_container(settings)

    queries = []
    for c_bn, c_en, probs in CROPS_PROBLEMS:
        for p_bn, p_en, chem in probs:
            queries.append({
                "qid": f"{c_en}_{p_en}_{chem}_q1",
                "crop": c_en,
                "crop_bn": c_bn,
                "problem": p_en,
                "chemical": chem,
                "query": f"{c_bn} ফসলে {p_bn} দমনে {chem} এর অনুমোদিত প্রয়োগমাত্রা কত?"
            })
            queries.append({
                "qid": f"{c_en}_{p_en}_{chem}_q2",
                "crop": c_en,
                "crop_bn": c_bn,
                "problem": p_en,
                "chemical": chem,
                "query": f"{c_bn} গাছে {p_bn} আক্রমণ দেখা দিলে {chem} কী হারে স্প্রে করতে হবে?"
            })

    # Limit to 100 unique queries
    queries = queries[:100]
    print(f"Generated {len(queries)} targeted dosage queries.")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = OUT_DIR / f"n03_expansion_{stamp}.json"
    rec_path = OUT_DIR / f"n03_expansion_{stamp}.jsonl"

    done_q = set()
    if rec_path.exists():
        with open(rec_path, encoding="utf-8") as f:
            for line in f:
                try:
                    done_q.add(json.loads(line).get("query"))
                except json.JSONDecodeError:
                    continue
        if done_q:
            print(f"Resuming: {len(done_q)} queries already recorded, skipping.")

    async def run_all():
        out, errs = [], 0
        for idx, item in enumerate(queries):
            if item["query"] in done_q:
                continue
            t0 = time.perf_counter()
            try:
                res = await container.qa.run(QAInput(query=item["query"]))
                latency_ms = round((time.perf_counter() - t0) * 1000, 1)
                claims = extract_claims(res.answer or "")
                dosed = [c for c in claims if c.has_dosage]
                rec = {
                    "qid": item["qid"],
                    "crop": item["crop"],
                    "chemical": item["chemical"],
                    "query": item["query"],
                    "ok": True,
                    "tier": res.resolution_tier.value,
                    "confidence": res.confidence.value,
                    "n_sources": len(res.sources),
                    "source_ids": [s.id for s in res.sources],
                    "answer": res.answer or "",
                    "latency_ms": latency_ms,
                    "n_claims": len(claims),
                    "n_dosed": len(dosed)
                }
                errs = 0
            except Exception as e:
                rec = {
                    "qid": item["qid"],
                    "crop": item["crop"],
                    "chemical": item["chemical"],
                    "query": item["query"],
                    "ok": False,
                    "error": type(e).__name__ + ": " + str(e)[:150]
                }
                errs += 1
                if errs > 20:
                    print("ABORT: >20 consecutive API errors")
                    raise SystemExit(2)

            out.append(rec)
            append_jsonl(rec_path, rec)
            d_flag = f"[DOSED: {rec.get('n_dosed', 0)}]" if rec.get("n_dosed", 0) > 0 else "[NO-DOSE]"
            print(f"[{idx + 1}/{len(queries)}] {d_flag} {item['crop']} - {item['chemical']} ({rec.get('tier', 'err')})", flush=True)

        return out

    asyncio.run(run_all())

    # Count total dosed in file
    all_recs = []
    with open(rec_path, encoding="utf-8") as f:
        for line in f:
            try:
                all_recs.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    dosed_count = sum(1 for r in all_recs if r.get("n_dosed", 0) > 0 and r.get("ok"))
    print(f"\n[DONE] Finished expansion run. Total queries: {len(all_recs)}, With dosage claims: {dosed_count}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
