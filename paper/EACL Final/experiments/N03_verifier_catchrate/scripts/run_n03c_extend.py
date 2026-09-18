#!/usr/bin/env python3
"""N03c extension generation: more live dosage answers + usage capture (EACL Final).

Set B: 39 farmer dosage-seeking queries (regex filter, deterministic by row_id).
Paraphrases: 71 dose_reference entries x 2 new phrasings (P2 rate-first, P3
safety-framed), crop-paired via source-node crop resolution (same method as
run_n03_catchrate elicitation).
Live container (OpenRouter gemini-2.5-flash-lite); per-call usage captured from
generation + safety lanes when exposed (last_usage contract); per-record fsync;
abort after >20 consecutive API errors.

Outputs: experiments/results/n03c_extend_<date>.json (+ .jsonl records).
Verify with: run_n03b_chemswap.py <records> n03c_verify
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
FARMER_PATH = WORKSPACE_ROOT / "backend" / "ml_assets" / "rag_index" / "eval" / "farmer_benchmark_1000.jsonl"
DOSE_REF = WORKSPACE_ROOT / "backend" / "ml_assets" / "rag_index" / "derived" / "dose_reference_v1.json"
NODES_PATH = WORKSPACE_ROOT / "backend" / "ml_assets" / "rag_index" / "processed" / "knowledge_nodes_clean.jsonl"

DOSE_Q_RE = re.compile(
    r"Carbendazim|Mancozeb|Imidacloprid|Cypermethrin|Chlorpyrifos|Deltamethrin|"
    r"Dimethoate|Fipronil|Malathion|Propiconazole|Spinosad|Tebuconazole|Cartap|"
    r"Carbofuran|Mohon|Ridomil|Bavistin|Dithane|Sevin|Decis|Karate|Actara|Tilt|"
    r"মিলি|গ্রাম|লিটার|মাত্রা|ডোজ|ইউরিয়া|ইউরিয়া|পটাশ|টিএসপি|ডিএপি|জিংক|বোরন|"
    r"\bml\b|\bEC\b|\bWP\b|\bSL\b|dose|ppm", re.IGNORECASE)
TOK_RE = re.compile(r"[\w\u0980-\u09FF]+")


def append_jsonl(path: Path, record: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def main() -> int:
    pre = subprocess.run([sys.executable, str(WORKSPACE_ROOT / "paper" / "EACL Final"
                                              / "experiments" / "preflight.py")],
                         capture_output=True, text=True)
    if pre.returncode != 0:
        print("FAIL: pre-flight authorization failed; aborting.")
        print(pre.stdout[-500:] if pre.stdout else "")
        return 1

    from app.application.container import build_container
    from app.application.qa_pipeline import QAInput
    from app.core.config import Settings
    from app.domain.intent import _CROP_ALIASES, CROP_NAMES_BN
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
    live_config = {"model": settings.openrouter_model,
                   "temperature": settings.llm_temperature,
                   "max_output_tokens": settings.llm_max_output_tokens}

    def lane_usage():
        """Best-effort provider usage from known lane attributes.

        STALE-READ RULE (fix): only generation-tier rows with sources actually
        called generate(); all other tiers must record None, never the prior
        row's values. Callers pass tier/sources context via lane_usage_for().
        """
        return _lane_usage_impl()

    def _lane_usage_impl():
        out = {}
        try:
            gen = getattr(getattr(container, "qa", None), "generator", None)
            client = getattr(gen, "client", None)
            if getattr(client, "last_usage", None):
                out["generation"] = dict(client.last_usage)
        except (AttributeError, TypeError, ValueError):
            pass
        try:
            safety = getattr(getattr(container, "qa", None), "safety", None)
            for attr in ("intent_llm", "client", "llm"):
                client = getattr(safety, attr, None)
                if getattr(client, "last_usage", None):
                    out["safety"] = dict(client.last_usage)
                    break
        except (AttributeError, TypeError, ValueError):
            pass
        return out

    # --- elicitation sets ---
    farmer = [json.loads(l) for l in open(FARMER_PATH, encoding="utf-8")]
    set_b = sorted([r for r in farmer if DOSE_Q_RE.search(r.get("question", ""))],
                   key=lambda r: r.get("row_id", ""))
    entries = json.load(open(DOSE_REF, encoding="utf-8"))["entries"]
    nodes = {}
    with open(NODES_PATH, encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("id"):
                nodes[r["id"]] = r

    def node_crop(entry):
        node = nodes.get(entry.get("node_id", ""), {})
        for field in ("title_en", "title_bn", "section_title"):
            low = str(node.get(field) or "").lower()
            toks = set(TOK_RE.findall(low))
            for crop, als in _CROP_ALIASES.items():
                for a in als:
                    a = str(a).strip().lower()
                    if not a:
                        continue
                    if (" " in a and a in low) or (" " not in a and a in toks):
                        return crop
        return None

    elicitations = []
    for r in set_b:
        elicitations.append({"kind": "farmer_dosage", "qid": r.get("row_id"),
                             "query": r["question"]})
    for e in entries:
        crop = node_crop(e)
        bn = CROP_NAMES_BN.get(crop, crop) if crop else None
        base = f"{bn} গাছে " if bn else ""
        elicitations.append({"kind": "para_rate", "qid": e["active"] + "|" + e.get("node_id", "") + "|P2",
                             "query": f"{base}{e['active']} কতটুকু হারে স্প্রে করতে হবে?",
                             "active": e["active"]})
        elicitations.append({"kind": "para_safety", "qid": e["active"] + "|" + e.get("node_id", "") + "|P3",
                             "query": f"{base}{e['active']} ব্যবহার কি নিরাপদ? সঠিক মাত্রা কত?",
                             "active": e["active"]})
    # Dedupe identical question texts (same active+crop across entries):
    # one live call per unique query; covered entry ids recorded.
    uniq, seen_q = [], set()
    for item in elicitations:
        if item["query"] in seen_q:
            continue
        seen_q.add(item["query"])
        uniq.append(item)
    elicitations = uniq

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = OUT_DIR / f"n03c_extend_{stamp}.json"
    rec_path = OUT_DIR / f"n03c_extend_{stamp}.jsonl"
    # Resume: skip queries already recorded (keyed by query TEXT — qids
    # collided across same-active entries in earlier runs). Per-record fsync
    # makes reruns safe.
    done_q = set()
    if rec_path.exists():
        with open(rec_path, encoding="utf-8") as f:
            for line in f:
                try:
                    done_q.add(json.loads(line).get("query"))
                except json.JSONDecodeError:
                    continue
        if done_q:
            print(f"resuming: {len(done_q)} queries already recorded, skipping")

    def reset_usage():
        """Clear lane usage before each query so a recorded value can only be
        fresh (fix: stale prior-row values previously persisted on rows that
        made no generation call)."""
        try:
            gen = getattr(getattr(container, "qa", None), "generator", None)
            client = getattr(gen, "client", None)
            if hasattr(client, "last_usage"):
                client.last_usage = None
        except (AttributeError, TypeError, ValueError):
            pass

    async def run_all():
        out, errs = [], 0
        for idx, item in enumerate(elicitations):
            if item["query"] in done_q:
                continue
            reset_usage()
            t0 = time.perf_counter()
            try:
                res = await container.qa.run(QAInput(query=item["query"]))
                latency_ms = round((time.perf_counter() - t0) * 1000, 1)
                claims = extract_claims(res.answer or "")
                rec = {"qid": item["qid"], "kind": item["kind"], "ok": True,
                       "query": item["query"],
                       "tier": res.resolution_tier.value,
                       "confidence": res.confidence.value,
                       "n_sources": len(res.sources),
                       "source_ids": [s.id for s in res.sources],
                       "answer": res.answer or "", "latency_ms": latency_ms,
                       "usage": lane_usage(),
                       "n_claims": len(claims),
                       "n_dosed": sum(1 for c in claims if c.has_dosage)}
                errs = 0
            except Exception as e:  # noqa: BLE001
                rec = {"qid": item["qid"], "kind": item["kind"], "ok": False,
                       "query": item["query"],
                       "error": type(e).__name__ + ": " + str(e)[:150]}
                errs += 1
                if errs > 20:
                    print("ABORT: >20 consecutive API errors")
                    raise SystemExit(2)
            out.append(rec)
            append_jsonl(rec_path, rec)
            if (idx + 1) % 25 == 0:
                print(f"[{idx + 1}/{len(elicitations)}] done", flush=True)
        return out

    produced = asyncio.run(run_all())
    # Summarize the FULL records file (includes resumed rows), not just this run.
    all_recs = []
    with open(rec_path, encoding="utf-8") as f:
        for line in f:
            try:
                all_recs.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    seen = {}
    for r in all_recs:
        seen[r.get("qid")] = r
    full = list(seen.values())
    ok = [r for r in full if r.get("ok")]
    dosed = [r for r in ok if r.get("n_dosed", 0) > 0]
    used = [r for r in ok if r.get("usage")]
    # Adapter: dose-bearing rows in the n03_catchrate record schema so the
    # frozen verify battery (run_n03b_chemswap.py <records> <prefix>) runs
    # unchanged on the extension set.
    adapted_path = OUT_DIR / f"n03c_scored_{stamp}.jsonl"
    if adapted_path.exists():
        adapted_path.unlink()
    for r in dosed:
        append_jsonl(adapted_path, {
            "stage": "scored", "active": r.get("qid", "farmer"),
            "query": r["query"], "tier": r["tier"], "confidence": r["confidence"],
            "n_sources": r["n_sources"], "source_ids": r["source_ids"],
            "answer": r["answer"]})
    results = {
        "benchmark_name": "EACL_N03C_EXTENSION_GENERATION",
        "execution_status": "DONE_REAL",
        "provenance": H.provenance(HERE, inputs={
            "farmer": FARMER_PATH, "dose_reference": DOSE_REF, "nodes": NODES_PATH}),
        "live_config": live_config,
        "design": {"n_elicitations": len(elicitations),
                   "farmer_dosage": len([e for e in elicitations if e["kind"] == "farmer_dosage"]),
                   "paraphrases": len([e for e in elicitations if e["kind"] != "farmer_dosage"])},
        "flow": {"ok": len(ok), "failed": len(full) - len(ok),
                 "with_dose_claims": len(dosed),
                 "with_usage": len(used)},
    }
    tmp = out_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(out_path)
    print(json.dumps(results["flow"], indent=2))
    print(f"[OK] wrote {out_path} + {rec_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
