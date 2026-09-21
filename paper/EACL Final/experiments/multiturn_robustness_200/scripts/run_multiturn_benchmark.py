"""Execution runner for the N=200 Multi-Turn Conversational Robustness Benchmark.

Adheres strictly to AGENTS.md Section 0 & 0.1 Directives:
- Authorized Model: google/gemini-2.5-flash-lite via OpenRouter (OPENROUTER_API_KEY)
- Pre-flight authorization check (1-token test aborts if 401/403)
- Durable disk sync (zero memory buffering, os.fsync() under lock)
- Consecutive error circuit breaker (>20 consecutive errors aborts)
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import time
from typing import Any
from dotenv import load_dotenv

# Ensure UTF-8 output on Windows
sys.stdout.reconfigure(encoding="utf-8")

# Add backend to Python path
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../backend"))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.domain.safety_policy import precheck, canned_response
from app.domain.intent import keyword_intent, _match_crop_alias, CROP_NAMES_BN
from app.domain.working_memory import AgriculturalWorkingMemory
from app.infrastructure.llm.openai_compatible import OpenAICompatibleClient
from app.application.rewrite import ConversationalQueryRewriter
from app.domain.enums import SafetyCategory

load_dotenv()

DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/multiturn_benchmark_200.json"))
RESULTS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../results/multiturn_results_200.jsonl"))

FILE_LOCK = asyncio.Lock()
CONSECUTIVE_ERRORS = 0
MAX_CONSECUTIVE_ERRORS = 20

# Known disease list for slot recognition
DISEASE_KEYWORDS = [
    "ব্লাস্ট রোগ", "খোলপোড়া রোগ", "মাজরা পোকা", "বাদামি দাগ", "ব্লাস্ট",
    "লেট ব্লাইট", "নাবী ধসা", "আগাম ধসা", "কাটুই পোকা", "মোজাইক ভাইরাস", "ধসা",
    "জাবপোকা", "অল্টারনারিয়া ব্লাইট", "সাদা মরিচা", "এফিড",
    "পাতা কোঁকড়ানো রোগ", "অ্যানথ্রাকনোজ", "ফল পচা", "থ্রিপস পোকা", "পাতা কোঁকড়া",
    "ফল আর্মিওয়ার্ম", "পাতা ঝলসানো রোগ", "কান্ড পচা", "আর্মিওয়ার্ম",
    "গম ব্লাস্ট", "পাতার মরিচা রোগ", "আলগা চিটা রোগ", "মরিচা রোগ",
    "ডগা ও ফল ছিদ্রকারী পোকা", "ঢলে পড়া রোগ", "ছোট পাতা রোগ", "ছিদ্রকারী পোকা",
    "আর্লি ব্লাইট", "ব্যাকটেরিয়াল উইল্ট", "সাদা মাছি", "হলুদ ছোপ"
]

def preflight_auth_check(api_key: str | None) -> None:
    """Pre-flight 1-token authorization test per AGENTS.md Section 0.1."""
    import httpx
    print("[Pre-flight] Verifying OpenRouter API Key for google/gemini-2.5-flash-lite...")
    if not api_key:
        print("[FATAL] OPENROUTER_API_KEY is not set!")
        sys.exit(1)
    try:
        resp = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "google/gemini-2.5-flash-lite",
                "messages": [{"role": "user", "content": "ping"}],
                "max_tokens": 1,
            },
            timeout=10.0,
        )
        if resp.status_code in (401, 403):
            print(f"[FATAL] Pre-flight auth failed with HTTP {resp.status_code}: {resp.text}")
            sys.exit(1)
        resp.raise_for_status()
        print(f"[Pre-flight] Authorization confirmed (HTTP {resp.status_code}). Proceeding.")
    except Exception as exc:
        print(f"[FATAL] Pre-flight network/auth error: {exc}")
        sys.exit(1)


async def durable_write_record(record: dict[str, Any], file_handle) -> None:
    """Atomic immediate durable disk sync under lock."""
    async with FILE_LOCK:
        line = json.dumps(record, ensure_ascii=False) + "\n"
        file_handle.write(line)
        file_handle.flush()
        os.fsync(file_handle.fileno())


async def process_dialogue(
    dial: dict[str, Any],
    rewriter: ConversationalQueryRewriter,
    file_handle,
) -> list[dict[str, Any]]:
    global CONSECUTIVE_ERRORS
    dial_id = dial["dialogue_id"]
    regime = dial["regime"]
    turns = dial["turns"]

    wm = AgriculturalWorkingMemory()
    history: list[dict[str, str]] = []
    dial_results = []

    for turn in turns:
        t_start = time.perf_counter()
        turn_idx = turn["turn_index"]
        user_utterance = turn["user_utterance"]

        # Step 1: Tier 0 Deterministic Precheck
        safety_match = precheck(user_utterance)
        if safety_match:
            cat, rules = safety_match
            lat_ms = (time.perf_counter() - t_start) * 1000
            rec = {
                "dialogue_id": dial_id,
                "regime": regime,
                "turn_index": turn_idx,
                "user_utterance": user_utterance,
                "expected_crop": turn.get("expected_crop"),
                "resolved_crop": None,
                "expected_gate_action": turn.get("expected_gate_action"),
                "actual_gate_action": "block_and_refer",
                "is_topic_shift_expected": turn.get("is_topic_shift", False),
                "is_topic_shift_actual": False,
                "prior_crop": wm.crop,
                "safety_status": "blocked",
                "safety_category": cat.value,
                "matched_rules": list(rules),
                "banned_substance_intercepted": (cat == SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL),
                "rewritten_query": None,
                "working_memory": wm.to_dict(),
                "latency_ms": round(lat_ms, 2),
                "rewrite_latency_ms": 0.0,
            }
            await durable_write_record(rec, file_handle)
            dial_results.append(rec)
            history.append({"role": "user", "content": user_utterance})
            history.append({"role": "assistant", "content": canned_response(cat)})
            continue

        # Step 2: NLU Slot Extraction & Ambiguity Detection
        kw = keyword_intent(user_utterance)
        extracted_crop = _match_crop_alias(user_utterance.lower())

        extracted_disease = None
        for d in DISEASE_KEYWORDS:
            if d in user_utterance:
                extracted_disease = d
                break

        # Check clarification condition (ambiguous query with no crop in query AND no prior crop in memory)
        is_ambiguous = (extracted_crop is None and wm.crop is None and kw is not None and kw.is_ambiguous)

        if is_ambiguous:
            lat_ms = (time.perf_counter() - t_start) * 1000
            prompt_bn = kw.clarification_question_bn if kw else "কোন ফসলের সমস্যা হয়েছে বলবেন কি?"
            rec = {
                "dialogue_id": dial_id,
                "regime": regime,
                "turn_index": turn_idx,
                "user_utterance": user_utterance,
                "expected_crop": turn.get("expected_crop"),
                "resolved_crop": None,
                "expected_gate_action": turn.get("expected_gate_action"),
                "actual_gate_action": "halt_ask",
                "is_topic_shift_expected": turn.get("is_topic_shift", False),
                "is_topic_shift_actual": False,
                "prior_crop": wm.crop,
                "safety_status": "safe",
                "safety_category": "safe_agri",
                "matched_rules": [],
                "banned_substance_intercepted": False,
                "rewritten_query": None,
                "working_memory": wm.to_dict(),
                "latency_ms": round(lat_ms, 2),
                "rewrite_latency_ms": 0.0,
            }
            await durable_write_record(rec, file_handle)
            dial_results.append(rec)
            history.append({"role": "user", "content": user_utterance})
            history.append({"role": "assistant", "content": prompt_bn})
            continue

        # Step 3: Working Memory State Transitions & Topic Shift Handling
        prior_crop = wm.crop
        prior_disease = wm.disease_candidate or wm.symptom
        is_topic_shift = bool(extracted_crop and prior_crop and extracted_crop.lower() != prior_crop.lower())

        wm = wm.merge(
            crop=extracted_crop,
            disease_candidate=extracted_disease,
            symptom=kw.plant_part if kw else None,
        )
        resolved_crop = wm.crop

        # Step 4: Conversational Query Rewriting (if follow-up with deixis)
        rewritten_query = None
        rw_latency_ms = 0.0
        if rewriter.should_rewrite(user_utterance, history):
            rw_start = time.perf_counter()
            try:
                rewritten_query = await rewriter.rewrite(user_utterance, history)
                CONSECUTIVE_ERRORS = 0
            except Exception as e:
                CONSECUTIVE_ERRORS += 1
                print(f"[WARN] Rewrite error on {dial_id} turn {turn_idx}: {e}")
                if CONSECUTIVE_ERRORS > MAX_CONSECUTIVE_ERRORS:
                    print("[FATAL] Exceeded consecutive error threshold! Pausing pipeline.")
                    sys.exit(1)
                rewritten_query = user_utterance
            rw_latency_ms = (time.perf_counter() - rw_start) * 1000

        lat_ms = (time.perf_counter() - t_start) * 1000

        rec = {
            "dialogue_id": dial_id,
            "regime": regime,
            "turn_index": turn_idx,
            "user_utterance": user_utterance,
            "expected_crop": turn.get("expected_crop"),
            "resolved_crop": resolved_crop,
            "expected_gate_action": turn.get("expected_gate_action"),
            "actual_gate_action": "proceed",
            "is_topic_shift_expected": turn.get("is_topic_shift", False),
            "is_topic_shift_actual": is_topic_shift,
            "prior_crop": prior_crop,
            "flushed_prior_disease": prior_disease if is_topic_shift else None,
            "safety_status": "safe",
            "safety_category": "safe_agri",
            "matched_rules": [],
            "banned_substance_intercepted": False,
            "rewritten_query": rewritten_query,
            "working_memory": wm.to_dict(),
            "latency_ms": round(lat_ms, 2),
            "rewrite_latency_ms": round(rw_latency_ms, 2),
        }

        await durable_write_record(rec, file_handle)
        dial_results.append(rec)
        history.append({"role": "user", "content": user_utterance})
        ctx = wm.as_context_line() or "সাধারণ কৃষি"
        history.append({"role": "assistant", "content": f"পরামর্শ ({ctx}): প্রয়োজনীয় যত্ন ও অনুমোদিত স্প্রে করুন।"})

    return dial_results


async def main():
    print("=================================================================")
    print("KrishokTech Multi-Turn Robustness Benchmark Runner (N=200)")
    print("=================================================================")

    api_key = os.getenv("OPENROUTER_API_KEY")
    preflight_auth_check(api_key)

    client = OpenAICompatibleClient(
        base_url="https://openrouter.ai/api/v1",
        model="google/gemini-2.5-flash-lite",
        api_key=api_key,
        max_output_tokens=150,
        temperature=0.0,
    )
    rewriter = ConversationalQueryRewriter(llm=client)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        benchmark_suite = json.load(f)

    print(f"Loaded {len(benchmark_suite)} dialogues from {DATA_FILE}.")
    total_turns = sum(len(d["turns"]) for d in benchmark_suite)
    print(f"Total turns to execute: {total_turns}")

    # Prepare results directory and file
    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
    # Check for existing checkpoint to resume if needed
    existing_ids = set()
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r", encoding="utf-8") as rf:
            for line in rf:
                if line.strip():
                    try:
                        row = json.loads(line)
                        existing_ids.add(row["dialogue_id"])
                    except Exception:
                        pass
        print(f"Found existing results: {len(existing_ids)} dialogues already logged.")

    # Concurrency gate: 5 parallel workers
    semaphore = asyncio.Semaphore(5)

    with open(RESULTS_FILE, "a", encoding="utf-8") as out_f:
        async def sem_worker(dial):
            async with semaphore:
                return await process_dialogue(dial, rewriter, out_f)

        tasks = []
        for dial in benchmark_suite:
            if dial["dialogue_id"] in existing_ids:
                continue
            tasks.append(sem_worker(dial))

        if not tasks:
            print("All dialogues already executed! Nothing to do.")
            return

        print(f"Launching {len(tasks)} dialogues across 5 concurrent coroutines...")
        t0 = time.perf_counter()
        completed = 0

        # Execute in batches of 20 with progress report
        batch_size = 20
        for i in range(0, len(tasks), batch_size):
            chunk = tasks[i : i + batch_size]
            await asyncio.gather(*chunk)
            completed += len(chunk)
            elapsed = time.perf_counter() - t0
            print(f"Progress: [{completed}/{len(tasks)}] dialogues ({round(completed/len(tasks)*100, 1)}%) in {round(elapsed, 1)}s")

    total_time = time.perf_counter() - t0
    print(f"\n[DONE] Successfully executed all dialogues in {round(total_time, 2)}s.")
    print(f"Results durably saved to: {RESULTS_FILE}")


if __name__ == "__main__":
    asyncio.run(main())
