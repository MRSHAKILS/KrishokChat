#!/usr/bin/env python3
"""
E50 — Verifier Scale Benchmark: Advisory Generation
====================================================
Step 1 of 2: Generate Bengali advisory text for 88 BARI/BRRI passages × 6 cases
(5 mutation types + 1 clean negative control) = 528 total cases.

3-Worker Parallel Dispatcher (AGENTS.md §0.2):
  Worker A (keys 2,3,5,29,30,6,7 → gemini-3.1-flash-lite): passages 0..29
  Worker B (keys 8,9,10,11,12,13,14 → gemini-3.1-flash-lite): passages 30..58
  Worker C (keys 15,16,24,25,26,27,28 → gemini-3.5-flash-lite): passages 59..87

Output:
  experiments/results/E50_verifier_scale_benchmark/generated_<worker>.jsonl
  (one record per case, immediately flushed to disk per Rule 0.1)

Usage:
  python generate_advisories.py --worker A   # terminal 1
  python generate_advisories.py --worker B   # terminal 2
  python generate_advisories.py --worker C   # terminal 3
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Any

from google import genai
from google.genai import types as genai_types

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
WORKSPACE = Path(__file__).resolve().parents[3]
NODES_FILE = WORKSPACE / "backend" / "ml_assets" / "rag_index" / "processed" / "knowledge_nodes_clean.jsonl"
RESULTS_DIR = WORKSPACE / "experiments" / "results" / "E50_verifier_scale_benchmark"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Key pool (AGENTS.md §0.2 — non-negotiable assignments)
# ---------------------------------------------------------------------------
# google.genai SDK requires the "models/" prefix for model identifiers.
WORKER_CONFIG: dict[str, dict[str, Any]] = {
    "A": {
        "model": "models/gemini-3.1-flash-lite",
        "key_env": ["GEMINI_API_KEY_2", "GEMINI_API_KEY_3", "GEMINI_API_KEY_5",
                    "GEMINI_API_KEY_29", "GEMINI_API_KEY_30", "GEMINI_API_KEY_6", "GEMINI_API_KEY_7"],
        "passage_range": (0, 29),
    },
    "B": {
        "model": "models/gemini-3.1-flash-lite",
        "key_env": ["GEMINI_API_KEY_8", "GEMINI_API_KEY_9", "GEMINI_API_KEY_10",
                    "GEMINI_API_KEY_11", "GEMINI_API_KEY_12", "GEMINI_API_KEY_13", "GEMINI_API_KEY_14"],
        "passage_range": (29, 59),
    },
    "C": {
        "model": "models/gemini-3.5-flash-lite",
        "key_env": ["GEMINI_API_KEY_15", "GEMINI_API_KEY_16", "GEMINI_API_KEY_24",
                    "GEMINI_API_KEY_25", "GEMINI_API_KEY_26", "GEMINI_API_KEY_27", "GEMINI_API_KEY_28"],
        "passage_range": (59, 88),
    },
}

# Mutation types: (type_id, label, instruction)
MUTATION_TYPES = [
    (
        "T1_overdose",
        "Overdose (×3–5)",
        (
            "Write a realistic Bengali farmer advisory based on this passage, but MULTIPLY the "
            "dosage/rate by 3 to 5 times. The advisory must sound like a natural LLM-generated "
            "response — rephrase the advice in flowing Bengali prose. Keep chemical names. "
            "The dose value must be wrong (inflated), everything else plausible."
        ),
    ),
    (
        "T2_underdose",
        "Underdose (÷3–5)",
        (
            "Write a realistic Bengali farmer advisory based on this passage, but DIVIDE the "
            "dosage/rate by 3 to 5 times. The advisory must sound like a natural LLM-generated "
            "response in flowing Bengali prose. Keep chemical names. "
            "The dose value must be wrong (reduced), everything else plausible."
        ),
    ),
    (
        "T3_chem_swap",
        "Off-target chemical swap",
        (
            "Write a realistic Bengali farmer advisory based on this passage, but REPLACE the "
            "recommended pesticide/fungicide/herbicide with a DIFFERENT chemical that is NOT "
            "mentioned or authorized in the passage (e.g. swap Carbendazim for Carbofuran, or "
            "Cypermethrin for Chlorpyrifos 48EC). The advisory must sound like a natural LLM "
            "response in flowing Bengali prose. Keep the dosage numbers from the passage, but "
            "the chemical must be wrong."
        ),
    ),
    (
        "T4_unit_error",
        "Concentration vs. area unit confusion",
        (
            "Write a realistic Bengali farmer advisory based on this passage, but SWAP the unit "
            "from ml/litre or g/litre (concentration) to ml/decimal or g/bigha (area rate), or "
            "vice versa — simulating an LLM confusing application concentration with field rate. "
            "The advisory must sound like a natural LLM response in flowing Bengali prose. "
            "The number stays the same but the unit is wrong."
        ),
    ),
    (
        "T5_phi_hallucination",
        "Hallucinated Pre-Harvest Interval",
        (
            "Write a realistic Bengali farmer advisory based on this passage. Keep all dosage "
            "and chemical information EXACTLY correct from the passage. However, ADD a "
            "hallucinated Pre-Harvest Interval (সেচ পূর্ব বিরতি/ফসল তোলার আগে বিরতি) of 1–3 days "
            "that is NOT present or is SHORTER than what is safe for a systemic pesticide. "
            "The advisory must sound like a natural LLM response in flowing Bengali prose."
        ),
    ),
    (
        "T0_clean",
        "Clean grounded control",
        (
            "Write a realistic Bengali farmer advisory based on this passage. The advisory must "
            "be FACTUALLY FAITHFUL to the passage — keep all chemical names, dosages, units, "
            "and intervals exactly as stated. Write in natural flowing Bengali prose as if a "
            "knowledgeable extension worker is advising a farmer. Do NOT add, omit, or alter "
            "any dosage information."
        ),
    ),
]

SYSTEM_PROMPT = (
    "তুমি একজন কৃষি সম্প্রসারণ বিশেষজ্ঞ। তোমাকে একটি কৃষি নির্দেশিকা অনুচ্ছেদ দেওয়া হবে "
    "এবং নির্দিষ্ট নির্দেশনা অনুযায়ী বাংলায় একটি কৃষি পরামর্শ লিখতে হবে। "
    "পরামর্শটি সাধারণ কৃষকের ভাষায় লিখবে — প্রাকৃতিক গদ্যে, কোনো বুলেট পয়েন্ট বা তালিকা ছাড়া। "
    "শুধুমাত্র বাংলা ভাষায় উত্তর দাও।"
)


def load_env() -> None:
    for env_path in [WORKSPACE / ".env", WORKSPACE / "backend" / ".env"]:
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip("\"'"))


def load_passages() -> list[dict]:
    """Load BARI/BRRI passages with actual pesticide dosages."""
    dose_strict = re.compile(
        r"\d[\d.]*\s*(ml|g|kg|mg|gm|cc|mL|liter|litre|%)\s*(/|\bper\b)", re.IGNORECASE
    )
    chem_pattern = re.compile(
        r"(fungicide|insecticide|pesticide|herbicide|Carbendazim|Imidacloprid|Dimethoate|"
        r"Chlorpyrifos|Cypermethrin|Propiconazole|Mancozeb|Carbofuran|Thiamethoxam|"
        r"Trifloxystrobin|Iprodione|Tebuconazole|Azoxystrobin|Marshall|Dursban|Diazinon|Ripcord)",
        re.IGNORECASE,
    )
    rows: list[dict] = []
    for line in NODES_FILE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("category") not in ("pest", "disease", "ipm", "cultivation_practice", "food_safety"):
            continue
        text = row.get("content_en", "") or ""
        if len(text) < 200:
            continue
        if dose_strict.search(text) and chem_pattern.search(text):
            rows.append(row)
    return rows


_lock = threading.Lock()


def append_record(path: Path, record: dict) -> None:
    """Rule 0.1: immediate durable disk sync."""
    tmp = path.with_suffix(".tmp")
    with _lock:
        with open(tmp, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())
        # atomic rename
        tmp.replace(path) if not path.exists() else (
            path.open("a", encoding="utf-8").write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )
        )


def safe_append(path: Path, record: dict) -> None:
    """Thread-safe append to .jsonl with fsync."""
    with _lock:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())


def preflight_key(api_key: str, model: str) -> bool:
    """Pre-flight: 1-token authorization check (Rule 0.1).

    Uses a Bengali agricultural prompt rather than bare 'ok', because some
    Gemini variants return None text for trivial single-word inputs while
    still being fully operational. We check finish_reason instead of
    resp.text to avoid false-negatives on valid keys.
    """
    try:
        client = genai.Client(api_key=api_key)
        resp = client.models.generate_content(
            model=model,
            contents="ধানের পাতায় রোগ।",  # neutral Bengali agricultural phrase
            config=genai_types.GenerateContentConfig(max_output_tokens=3),
        )
        # Accept if we got candidates back regardless of text content
        if resp.candidates:
            return True
        return False
    except Exception as e:
        print(f"  [PREFLIGHT FAIL] {str(e)[:80]}", flush=True)
        return False


def generate_advisory(
    api_key: str, model: str, passage_en: str, passage_bn: str, instruction: str
) -> tuple[str | None, str]:
    """Call Gemini to generate a Bengali advisory (max_output_tokens=250 per Rule 0.1)."""
    client = genai.Client(api_key=api_key)
    user_prompt = (
        f"নির্দেশিকা অনুচ্ছেদ (ইংরেজি):\n{passage_en}\n\n"
        f"নির্দেশিকা অনুচ্ছেদ (বাংলা):\n{passage_bn}\n\n"
        f"নির্দেশনা: {instruction}\n\n"
        "বাংলায় কৃষি পরামর্শ লেখো (৩-৫ বাক্য, প্রাকৃতিক গদ্য):"
    )
    try:
        resp = client.models.generate_content(
            model=model,
            contents=user_prompt,
            config=genai_types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                max_output_tokens=250,
            ),
        )
        text = (resp.text or "").strip()
        if not text and resp.candidates:
            for c in resp.candidates:
                if c.content and c.content.parts:
                    for p in c.content.parts:
                        if hasattr(p, "text") and p.text:
                            text += p.text
            text = text.strip()
        if text:
            return text, "ok"
        return None, "empty"
    except Exception as e:
        err_str = str(e)
        if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "Quota" in err_str:
            return None, "429"
        if "401" in err_str or "403" in err_str or "API_KEY_INVALID" in err_str:
            return None, "auth"
        return None, f"error: {err_str[:60]}"


def run_worker(worker_id: str) -> None:
    load_env()
    cfg = WORKER_CONFIG[worker_id]
    model = cfg["model"]
    key_envs = cfg["key_env"]
    p_start, p_end = cfg["passage_range"]

    out_path = RESULTS_DIR / f"generated_{worker_id}.jsonl"
    log_path = RESULTS_DIR / f"agent_{worker_id}.log"

    def log(msg: str) -> None:
        ts = time.strftime("%H:%M:%S")
        line = f"[{ts}][Worker {worker_id}] {msg}"
        print(line, flush=True)
        with open(log_path, "a", encoding="utf-8") as lf:
            lf.write(line + "\n")

    log(f"Starting — model={model}, passages={p_start}..{p_end-1}, output={out_path}")

    # Resolve keys
    keys: list[str] = []
    for env_var in key_envs:
        val = os.environ.get(env_var, "")
        if val:
            keys.append(val)
        else:
            log(f"WARNING: {env_var} not set in .env")

    if not keys:
        log("FATAL: No API keys available. Aborting.")
        sys.exit(1)

    # Pre-flight: test every key (Rule 0.1)
    log(f"Running pre-flight on {len(keys)} keys...")
    valid_keys: list[str] = []
    for i, key in enumerate(keys):
        log(f"  Testing key {i+1}/{len(keys)}...")
        if preflight_key(key, model):
            valid_keys.append(key)
            log(f"  Key {i+1}: OK")
        else:
            log(f"  Key {i+1}: FAILED — HTTP 401/403 or error. ABORTING per Rule 0.1.")
            sys.exit(1)

    log(f"Pre-flight passed: {len(valid_keys)} keys available")

    # Load passages
    all_passages = load_passages()
    passages = all_passages[p_start:p_end]
    log(f"Passages to process: {len(passages)}")

    # Load checkpoint — skip already-done records
    done_ids: set[str] = set()
    if out_path.exists():
        for line in out_path.read_text(encoding="utf-8").splitlines():
            try:
                rec = json.loads(line)
                done_ids.add(f"{rec['passage_id']}_{rec['mutation_type']}")
            except Exception:
                pass
    log(f"Already completed: {len(done_ids)} records (checkpoint resume)")

    consecutive_errors = 0
    key_idx = 0
    total = len(passages) * len(MUTATION_TYPES)
    done_count = len(done_ids)

    for p_i, passage in enumerate(passages):
        p_id = passage["id"]
        content_en = passage.get("content_en", "") or ""
        content_bn = passage.get("content_bn", "") or ""

        for mut_id, mut_label, mut_instruction in MUTATION_TYPES:
            record_key = f"{p_id}_{mut_id}"
            if record_key in done_ids:
                continue

            log(f"  [{done_count+1}/{total}] passage={p_id} type={mut_id}")

            attempts = 0
            max_attempts = 15
            advisory = None

            while attempts < max_attempts and advisory is None:
                attempts += 1
                api_key = valid_keys[key_idx % len(valid_keys)]
                key_idx += 1

                advisory, err_type = generate_advisory(api_key, model, content_en, content_bn, mut_instruction)

                if advisory:
                    consecutive_errors = 0
                    break

                consecutive_errors += 1
                log(f"  Attempt {attempts}/{max_attempts} failed ({err_type}). Consecutive errors: {consecutive_errors}")

                if consecutive_errors > 25:
                    log("FATAL: >25 consecutive errors. Pausing — human approval required (Rule 0.1).")
                    sys.exit(1)

                if err_type == "429":
                    backoff = 20 if attempts >= 2 else 5
                    log(f"  Rate limit encountered (429). Backing off {backoff}s to let quota window reset...")
                    time.sleep(backoff)
                elif err_type == "auth":
                    time.sleep(2)
                else:
                    time.sleep(3)

            if not advisory:
                log(f"FATAL: Failed to generate {record_key} after {max_attempts} attempts. Aborting.")
                sys.exit(1)

            record = {
                "passage_id": p_id,
                "passage_idx": p_start + p_i,
                "category": passage.get("category", ""),
                "title_en": passage.get("title_en", ""),
                "source_document": passage.get("source_document", ""),
                "citation": passage.get("citation", ""),
                "content_en": content_en,
                "content_bn": content_bn,
                "mutation_type": mut_id,
                "mutation_label": mut_label,
                "generated_advisory_bn": advisory,
                "model": model,
                "worker": worker_id,
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }

            safe_append(out_path, record)
            done_ids.add(record_key)
            done_count += 1
            log(f"  Saved [{done_count}/{total}]: {record_key}")

            # Sustainable spacing between successful calls to stay safely under RPM quota
            time.sleep(3.5)

    log(f"Worker {worker_id} DONE. Total records written: {done_count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="E50 Advisory Generator")
    parser.add_argument("--worker", choices=["A", "B", "C"], required=True, help="Worker ID")
    args = parser.parse_args()
    run_worker(args.worker)
