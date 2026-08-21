"""
Node Refinement Pipeline using Gemini 3.1 Flash Lite.

Two parallel workers, round-robin key rotation.
One node per Gemini call. Checkpoint saved after EVERY node (append mode).
Resumable: skips already-refined node IDs.

Usage:
    python scripts/03_refine_nodes_gemini.py --keys "key1,key2"
    python scripts/03_refine_nodes_gemini.py --keys-file ../../../.env
"""
import argparse
import json
import os
import sys
import time
import threading
from pathlib import Path
from datetime import datetime

import httpx

SCRIPT_DIR = Path(__file__).resolve().parent
RAG_ROOT = SCRIPT_DIR.parent
NODES_PATH = RAG_ROOT / "processed" / "knowledge_nodes_clean.jsonl"
SOURCE_MD_DIR = RAG_ROOT / "source_md"
CHECKPOINT_PATH = RAG_ROOT / "processed" / "knowledge_nodes_refined.jsonl"
LOG_PATH = RAG_ROOT / "logs" / "refinement_log.json"

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent"
MODEL_NAME = "gemini-3.1-flash-lite"

# Thread lock for file writing
file_lock = threading.Lock()


def load_api_keys(args):
    """Load API keys from args, env file, or environment."""
    keys = []

    if args.keys:
        keys = [k.strip() for k in args.keys.split(",") if k.strip()]
    elif args.keys_file:
        with open(args.keys_file) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("GEMINI_API_KEY"):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    # Remove inline comments
                    if " #" in val:
                        val = val.split(" #")[0].strip()
                    if val:
                        keys.append(val)
                elif line.startswith("GEMINI_API_KEYS"):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if " #" in val:
                        val = val.split(" #")[0].strip()
                    keys.extend([k.strip() for k in val.split(",") if k.strip()])

    if not keys:
        for key, val in os.environ.items():
            if key.startswith("GEMINI_API_KEY") and val:
                v = val.strip()
                if " #" in v:
                    v = v.split(" #")[0].strip()
                if v:
                    keys.append(v)

    if not keys:
        print("ERROR: No Gemini API keys found!")
        sys.exit(1)

    # Deduplicate
    keys = list(dict.fromkeys(keys))
    print(f"Loaded {len(keys)} API key(s)")
    return keys


def load_nodes():
    """Load all knowledge nodes."""
    nodes = []
    with open(NODES_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                nodes.append(json.loads(line))
    return nodes


def load_completed_ids():
    """Load successfully-refined node IDs from checkpoint (skip errors)."""
    completed = set()
    if CHECKPOINT_PATH.exists():
        with open(CHECKPOINT_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        node = json.loads(line)
                        # Only count as completed if it has content_bn (success)
                        if node.get("content_bn") and not node.get("error"):
                            completed.add(node.get("id", ""))
                    except json.JSONDecodeError:
                        pass
    return completed


def find_source_md(node):
    """Try to find the source MD file for a node."""
    publisher = node.get("publisher", "").strip()
    title = node.get("title_en", "").strip()

    if not publisher or not SOURCE_MD_DIR.exists():
        return None

    # Try to find in publisher folder
    pub_dir = SOURCE_MD_DIR / publisher
    if not pub_dir.exists():
        return None

    # Search for files matching section_title or title
    section = node.get("section_title", "").strip()

    # Try matching by section_title in filename
    for md_file in pub_dir.rglob("*.md"):
        fname = md_file.stem.lower()
        if section and section.lower()[:40] in fname:
            return md_file
        if title and title.lower()[:40] in fname:
            return md_file

    return None


def build_prompt(node, source_md_content=None):
    """Build the refinement prompt for a single node."""
    section_context = ""
    if source_md_content:
        # Truncate to ~4000 chars to keep prompt manageable
        truncated = source_md_content[:4000]
        if len(source_md_content) > 4000:
            truncated += "\n... [truncated]"
        section_context = f"\n### মূল উৎস দলিল (Source Markdown):\n{truncated}\n"

    # Build structured data string
    structured = node.get("structured", {})
    structured_str = json.dumps(structured, ensure_ascii=False, indent=2) if structured else "{}"

    prompt = f"""আপনি একজন বাংলাদেশের কৃষি সম্প্রসারণ অফিসার। আপনার কাজ হলো নিচে দেওয়া তথ্য থেকে একটি সম্পূর্ণ, সুসংগঠিত, কৃষক-বান্ধব জ্ঞান নোড তৈরি করা।

## মূল নিয়ম
1. সব তথ্য কৃষি বিজ্ঞানসম্মত ও সঠিক হতে হবে
2. রাসায়নিক নাম, মাত্রা (dosage), একক ইত্যাদি যথাযথভাবে সংরক্ষণ করুন — এগুলো পরিবর্তন করবেন না
3. ভাষা সহজ, প্রাঞ্জল, কৃষকের বোঝার মতো করে লিখুন
4. ইংরেজি প্রযুক্তিগত শব্দের পাশাপাশি বাংলা পরিভাষা ব্যবহার করুন
5. কোনো নতুন চিকিৎসা বা পরামর্শ তৈরি করবেন না — শুধু যা আছে তাকে সুন্দরভাবে সাজান
6. ছোট কন্টেন্টকে প্রসারিত করুন — বিস্তারিত ব্যাখ্যা দিন, উদাহরণ দিন, প্রয়োজনে ধাপে ধাপে নির্দেশনা দিন
7. কন্টেন্ট অন্তত ১৫০ শব্দের হতে হবে
{section_context}
### বর্তমান নোড ডেটা:
- ক্যাটাগরি: {node.get('category', 'N/A')}
- শিরোনাম (EN): {node.get('title_en', '')}
- বিষয়বস্তু (BN): {node.get('content_bn', '')[:500]}
- সারসংক্ষেপ: {node.get('summary', '')}
- ট্যাগ: {node.get('tags', [])}
- উৎস: {node.get('source_document', '')}
- প্রকাশক: {node.get('publisher', '')}
- ধারণাগত ডেটা: {structured_str[:500]}

## আউটপুট ফরমাট (JSON উত্তর দিন, কোনো অতিরিক্ত টেক্সট ছাড়া):

{{
  "id": "{node.get('id', '')}",
  "category": "{node.get('category', '')}",
  "title_bn": "বাংলা শিরোনাম (সংক্ষিপ্ত, অর্থপূর্ণ)",
  "title_en": "{node.get('title_en', '')}",
  "summary": "১-২ লাইনের সারসংক্ষেপ",
  "natural_intro_bn": "কৃষকের কাছে উপযোগী ভাষায় ভূমিকা (২-৩ বাক্য)",
  "content_bn": "বিস্তারিত বিষয়বস্তু — সুসংগঠিত, পয়েন্টযুক্ত, পড়াতে সহজ",
  "content_en": "Detailed content in English — well-organized, structured",
  "key_points": ["পয়েন্ট ১", "পয়েন্ট ২"],
  "tags": ["ট্যাগ১", "ট্যাগ২"],
  "safety_notes": "সতর্কতা (যদি থাকে, না থাকলে empty string)",
  "source_document": "{node.get('source_document', '')}",
  "publisher": "{node.get('publisher', '')}"
}}"""
    return prompt


def call_gemini(prompt, api_key, max_retries=3):
    """Call Gemini API with retry logic."""
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 4096,
            "topP": 0.9,
        },
    }

    for attempt in range(max_retries):
        try:
            url = f"{GEMINI_URL}?key={api_key}"
            resp = httpx.post(url, headers=headers, json=payload, timeout=120)

            if resp.status_code == 429:
                return None, "rate_limit"
            if resp.status_code in (401, 403):
                return None, "auth_error"
            if resp.status_code != 200:
                return None, f"http_{resp.status_code}"

            data = resp.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]

            # Clean up markdown code block if present
            text = text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

            return text, "success"

        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 * (attempt + 1))
                continue
            return None, f"error: {str(e)[:100]}"

    return None, "max_retries"


def save_checkpoint(node_data, log_data):
    """Thread-safe checkpoint save (append mode)."""
    with file_lock:
        # Append refined node
        with open(CHECKPOINT_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(node_data, ensure_ascii=False) + "\n")
            f.flush()

        # Append log
        log_path = LOG_PATH
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_data, ensure_ascii=False) + "\n")
            f.flush()


def worker(worker_id, keys, nodes_queue, stats):
    """Worker thread: processes nodes with strict per-key rate limiting.

    Rate limit: ~10 RPM per key = 1 call per 6 seconds (safe).
    Each key tracks its own cooldown. If no key is available, WAIT.
    On rate limit: add heavy cooldown to that key and WAIT.
    """
    num_keys = len(keys)
    # Track when each key will be available (absolute timestamp)
    key_available_at = [0.0] * num_keys
    key_idx = 0
    BASE_COOLDOWN = 6.0  # seconds between calls per key (safe for 10 RPM)
    RATE_LIMIT_PENALTY = 30.0  # extra seconds when rate limited
    CONSECUTIVE_RL_THRESHOLD = 5  # after this many consecutive RLs, global wait
    consecutive_rl = 0

    while True:
        with file_lock:
            if not nodes_queue:
                break
            node = nodes_queue.pop(0)
            idx = stats["processed"] + 1
            stats["processed"] += 1

        node_id = node.get("id", "")
        print(f"[Worker {worker_id}] [{idx}/{stats['total']}] Refining: {node_id}")

        # Find source MD
        source_md = find_source_md(node)
        md_content = None
        if source_md:
            try:
                md_content = source_md.read_text(encoding="utf-8")
            except Exception:
                pass

        # Build prompt
        prompt = build_prompt(node, md_content)

        # --- Rate-limited key selection ---
        now = time.time()
        selected_idx = -1
        for _ in range(num_keys):
            ki = key_idx % num_keys
            key_idx += 1
            if now >= key_available_at[ki]:
                selected_idx = ki
                break

        # If no key available, wait for the soonest one + small buffer
        if selected_idx == -1:
            soonest = min(range(num_keys), key=lambda i: key_available_at[i])
            wait_time = key_available_at[soonest] - now + 1.0
            if wait_time > 0:
                print(f"[Worker {worker_id}] Waiting {wait_time:.1f}s for key {soonest}...")
                time.sleep(wait_time)
            selected_idx = soonest
            now = time.time()

        # If too many consecutive rate limits, do a global cooldown
        if consecutive_rl >= CONSECUTIVE_RL_THRESHOLD:
            print(f"[Worker {worker_id}] {consecutive_rl} consecutive rate limits — global 30s cooldown...")
            time.sleep(30)
            consecutive_rl = 0
            # Reset all keys
            now = time.time()
            for i in range(num_keys):
                key_available_at[i] = now

        selected_key = keys[selected_idx]

        # Call Gemini
        result, status = call_gemini(prompt, selected_key)

        # Update key cooldown
        if status == "success":
            key_available_at[selected_idx] = time.time() + BASE_COOLDOWN
            consecutive_rl = 0  # reset on success
        elif status == "rate_limit":
            key_available_at[selected_idx] = time.time() + BASE_COOLDOWN + RATE_LIMIT_PENALTY
            consecutive_rl += 1
            print(f"[Worker {worker_id}] Key {selected_idx} rate limited, +{RATE_LIMIT_PENALTY:.0f}s cooldown")
        else:
            key_available_at[selected_idx] = time.time() + BASE_COOLDOWN

        if status == "auth_error":
            print(f"[Worker {worker_id}] AUTH ERROR — aborting!")
            with file_lock:
                stats["auth_error"] = True
            return

        if status == "rate_limit":
            # DON'T save — node will be retried next run
            print(f"[Worker {worker_id}] RATE LIMITED — skipping")
            with file_lock:
                stats["rate_limited"] += 1
            continue

        if result is None:
            print(f"[Worker {worker_id}] FAILED: {node_id} ({status})")
            with file_lock:
                stats["failed"] += 1
            save_checkpoint(
                {"id": node_id, "error": True, "status": status},
                {"node_id": node_id, "status": "failed", "error": status, "timestamp": datetime.now().isoformat()},
            )
            continue

        # Parse JSON result
        try:
            refined = json.loads(result)
            refined["id"] = node_id
            save_checkpoint(
                refined,
                {"node_id": node_id, "status": "success", "timestamp": datetime.now().isoformat()},
            )
            with file_lock:
                stats["success"] += 1
            print(f"[Worker {worker_id}] ✓ Success: {node_id}")
        except json.JSONDecodeError as e:
            print(f"[Worker {worker_id}] JSON parse error: {e}")
            with file_lock:
                stats["parse_errors"] += 1
            save_checkpoint(
                {"id": node_id, "error": True, "raw_result": result[:500]},
                {"node_id": node_id, "status": "parse_error", "timestamp": datetime.now().isoformat()},
            )


def main():
    parser = argparse.ArgumentParser(description="Refine knowledge nodes using Gemini")
    parser.add_argument("--keys", help="Comma-separated Gemini API keys")
    parser.add_argument("--keys-file", help="Path to .env file with GEMINI_API_KEY")
    parser.add_argument("--workers", type=int, default=2, help="Number of parallel workers")
    args = parser.parse_args()

    # Load keys
    all_keys = load_api_keys(args)
    if len(all_keys) < 2:
        print("WARNING: Only 1 key provided, both workers will share it")

    # Split keys between workers (round-robin)
    keys_a = all_keys[::2]  # Even indices
    keys_b = all_keys[1::2]  # Odd indices
    if not keys_b:
        keys_b = keys_a

    print(f"Worker A keys: {len(keys_a)}, Worker B keys: {len(keys_b)}")

    # Load nodes
    nodes = load_nodes()
    print(f"Loaded {len(nodes)} nodes")

    # Check completed
    completed = load_completed_ids()
    print(f"Already refined: {len(completed)}")

    # Queue remaining
    queue = [n for n in nodes if n.get("id", "") not in completed]
    remaining = len(queue)
    print(f"Remaining to refine: {remaining}")

    if remaining == 0:
        print("All nodes already refined!")
        return

    # Stats
    stats = {
        "total": remaining,
        "processed": 0,
        "success": 0,
        "failed": 0,
        "parse_errors": 0,
        "rate_limited": 0,
        "auth_error": False,
    }

    # Launch workers
    threads = []
    worker_keys = [keys_a, keys_b]
    for i in range(min(args.workers, 2)):
        t = threading.Thread(
            target=worker,
            args=(i, worker_keys[i], queue, stats),
            daemon=True,
        )
        threads.append(t)
        t.start()

    # Wait
    for t in threads:
        t.join()

    # Report
    print("\n" + "=" * 60)
    print("REFINEMENT COMPLETE")
    print("=" * 60)
    print(f"Total processed: {stats['processed']}")
    print(f"Success: {stats['success']}")
    print(f"Failed: {stats['failed']}")
    print(f"Rate limited (will retry): {stats['rate_limited']}")
    print(f"Parse errors: {stats['parse_errors']}")
    print(f"Checkpoint saved to: {CHECKPOINT_PATH}")
    print(f"Log saved to: {LOG_PATH}")


if __name__ == "__main__":
    main()
