#!/usr/bin/env python3
"""
KrishokChat E2E Paper-Claim Test Runner
========================================
Reads tests/e2e_queries.json and fires each test case against a running
backend (default: http://127.0.0.1:8000).

Usage:
    cd backend
    python tests/run_e2e.py                          # Gemini model (default)
    python tests/run_e2e.py --group T0               # run only T0 group
    python tests/run_e2e.py --group T1 T3 T4         # run multiple groups
    RUN_LOCAL_MODEL=1 python tests/run_e2e.py        # also run local-model tests
    python tests/run_e2e.py --base-url http://...    # custom backend URL
    python tests/run_e2e.py --timeout 60             # custom per-request timeout

Environment variables:
    RUN_LOCAL_MODEL=1   Enable T9 local-model tests (needs Ollama + krishokchat-4b)
    KRISHOKCHAT_BASE_URL  Override backend base URL

Exit code: 0 if all tests pass (or pass rate >= threshold), 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

# ── UTF-8 stdout (Windows fix) ────────────────────────────────────────────────
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]

try:
    import httpx
except ImportError:
    print("ERROR: httpx not installed. Run: pip install httpx")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
CORPUS_PATH = Path(__file__).parent / "e2e_queries.json"
DEFAULT_BASE_URL = os.environ.get("KRISHOKCHAT_BASE_URL", "http://127.0.0.1:8000")
RUN_LOCAL_MODEL = os.environ.get("RUN_LOCAL_MODEL", "0") == "1"

PASS = "[PASS]"
FAIL = "[FAIL]"
SKIP = "[SKIP]"
WARN = "[WARN]"

# ANSI colours (disabled on Windows CI if not supported)
GREEN  = "\033[92m" if os.name != "nt" or os.environ.get("FORCE_COLOR") else ""
RED    = "\033[91m" if os.name != "nt" or os.environ.get("FORCE_COLOR") else ""
YELLOW = "\033[93m" if os.name != "nt" or os.environ.get("FORCE_COLOR") else ""
CYAN   = "\033[96m" if os.name != "nt" or os.environ.get("FORCE_COLOR") else ""
RESET  = "\033[0m"  if os.name != "nt" or os.environ.get("FORCE_COLOR") else ""

try:
    import colorama; colorama.init()  # noqa: E402, E501
    GREEN = "\033[92m"; RED = "\033[91m"; YELLOW = "\033[93m"
    CYAN = "\033[96m"; RESET = "\033[0m"
except ImportError:
    pass


def clr(color: str, text: str) -> str:
    return f"{color}{text}{RESET}"


def load_corpus() -> dict:
    with CORPUS_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def validate_response(body: dict, expected: dict) -> tuple[bool, list[str]]:
    """Return (passed, list_of_failures)."""
    failures: list[str] = []

    # category check
    if "category" in expected:
        got = body.get("category", "")
        if got != expected["category"]:
            failures.append(f"category: expected '{expected['category']}', got '{got}'")

    # resolution_tier exact
    if "resolution_tier" in expected:
        got = body.get("resolution_tier", "")
        if got != expected["resolution_tier"]:
            failures.append(f"resolution_tier: expected '{expected['resolution_tier']}', got '{got}'")

    # resolution_tier any of
    if "resolution_tier_any" in expected:
        got = body.get("resolution_tier", "")
        if got not in expected["resolution_tier_any"]:
            failures.append(
                f"resolution_tier: expected one of {expected['resolution_tier_any']}, got '{got}'"
            )

    # answer must not be empty
    if expected.get("answer_not_empty"):
        ans = body.get("answer", "")
        if not ans or len(ans.strip()) < 5:
            failures.append(f"answer_not_empty: answer is empty or too short ({ans!r})")

    # answer must contain all listed strings
    if "answer_contains" in expected:
        ans = body.get("answer", "")
        for needle in expected["answer_contains"]:
            # Handle Bengali digit equivalents (e.g. 16123 / ১৬১২৩)
            if needle == "16123" and ("16123" in ans or "১৬১২৩" in ans):
                continue
            if needle not in ans:
                failures.append(f"answer_contains: '{needle}' not found in answer")

    # answer must contain at least one of listed strings
    if "answer_contains_any" in expected:
        ans = body.get("answer", "")
        if not any(needle in ans for needle in expected["answer_contains_any"]):
            failures.append(
                f"answer_contains_any: none of {expected['answer_contains_any']} found in answer"
            )

    # sources count min
    if "sources_count_min" in expected:
        cnt = len(body.get("sources", []))
        if cnt < expected["sources_count_min"]:
            failures.append(f"sources_count_min: got {cnt}, expected >= {expected['sources_count_min']}")

    # sources count max
    if "sources_count_max" in expected:
        cnt = len(body.get("sources", []))
        if cnt > expected["sources_count_max"]:
            failures.append(f"sources_count_max: got {cnt}, expected <= {expected['sources_count_max']}")

    # quick_reply_chips minimum count
    if "quick_reply_chips_min" in expected:
        chips = body.get("quick_reply_chips", [])
        if len(chips) < expected["quick_reply_chips_min"]:
            failures.append(
                f"quick_reply_chips_min: got {len(chips)} chips, expected >= {expected['quick_reply_chips_min']}"
            )

    # response_contains_keys (for GET endpoint tests, body IS the response dict)
    if "response_contains_keys" in expected:
        for key in expected["response_contains_keys"]:
            if key not in body:
                failures.append(f"response_contains_keys: key '{key}' missing from response")

    return len(failures) == 0, failures


def run_test(
    client: httpx.Client,
    test: dict,
    timeout: float = 45.0,
) -> tuple[str, list[str], dict, float]:
    """
    Returns (status, failures, response_body, elapsed_ms).
    status: 'pass' | 'fail' | 'skip' | 'error'
    """
    expected = test.get("expected", {})
    model_override = test.get("model")

    # Skip local-model tests unless enabled
    if model_override == "krishokchat-4b" and not RUN_LOCAL_MODEL:
        return "skip", [], {}, 0.0

    if model_override == "krishokchat-4b":
        timeout = max(timeout, 180.0)

    method = test.get("method", "POST").upper()
    endpoint = test.get("endpoint", "/api/qa")

    t0 = time.perf_counter()
    try:
        if method == "GET":
            resp = client.get(endpoint, timeout=timeout)
        else:
            payload: dict[str, Any] = {"query": test["query"]}
            if "history" in test:
                payload["history"] = test["history"]
            if model_override:
                payload["model"] = model_override

            resp = client.post(endpoint, json=payload, timeout=timeout)

        elapsed = (time.perf_counter() - t0) * 1000

        # status code check
        expected_code = expected.get("status_code", 200)
        if resp.status_code != expected_code:
            return "fail", [
                f"HTTP {resp.status_code} != expected {expected_code}"
            ], {}, elapsed

        body = resp.json()

    except httpx.ConnectError as exc:
        return "error", [f"ConnectError: {exc}"], {}, 0.0
    except httpx.TimeoutException as exc:
        return "error", [f"Timeout: {exc}"], {}, timeout * 1000
    except Exception as exc:  # noqa: BLE001
        return "error", [f"Exception: {exc}"], {}, 0.0

    passed, failures = validate_response(body, expected)
    return ("pass" if passed else "fail"), failures, body, elapsed


def print_result(
    test: dict,
    status: str,
    failures: list[str],
    body: dict,
    elapsed: float,
    verbose: bool = False,
) -> None:
    tid = test.get("id", "?")
    label = test.get("label", "")
    query_preview = (test.get("query") or "")[:60]

    if status == "pass":
        icon = clr(GREEN, PASS)
    elif status == "fail":
        icon = clr(RED, FAIL)
    elif status == "skip":
        icon = clr(YELLOW, SKIP)
    else:
        icon = clr(RED, "[ERR]")

    tier = body.get("resolution_tier", "—")
    cat  = body.get("category", "—")
    chips_count = len(body.get("quick_reply_chips", []))
    src_count   = len(body.get("sources", []))

    print(f"  {icon} [{tid}] {label}")
    if verbose or status in ("fail", "error"):
        print(f"         query   : {query_preview!r}")
        if status not in ("skip",):
            print(f"         tier    : {tier}   cat: {cat}   chips: {chips_count}   srcs: {src_count}   {elapsed:.0f}ms")
        for f in failures:
            print(f"         {clr(RED, 'FAIL')} {f}")
        if verbose and body.get("answer"):
            ans_preview = body["answer"][:120].replace("\n", " ")
            print(f"         answer  : {ans_preview!r}")
    else:
        if status not in ("skip",):
            print(f"         tier={tier} cat={cat} chips={chips_count} srcs={src_count} {elapsed:.0f}ms")


def run_all(args: argparse.Namespace) -> int:
    corpus = load_corpus()
    groups = corpus.get("test_groups", [])

    # Filter groups if requested
    group_filter = set(args.group) if args.group else None

    global RUN_LOCAL_MODEL
    if getattr(args, "local", False):
        RUN_LOCAL_MODEL = True

    base_url = args.base_url or DEFAULT_BASE_URL

    # Health check
    print(f"\n{clr(CYAN, '=== KrishokChat E2E Paper-Claim Tests ===')} ")
    print(f"Backend : {base_url}")
    print(f"Local   : {'enabled' if RUN_LOCAL_MODEL else 'disabled (pass --local or set RUN_LOCAL_MODEL=1)'}")
    if group_filter:
        print(f"Groups  : {', '.join(sorted(group_filter))}")
    print()

    with httpx.Client(base_url=base_url, timeout=args.timeout) as client:
        # Quick health-check first
        try:
            r = client.get("/health", timeout=5.0)
            if r.status_code != 200:
                print(clr(RED, f"FATAL: /health returned {r.status_code}. Is the backend running?"))
                return 1
            print(clr(GREEN, "✓ Backend is healthy\n"))
        except httpx.ConnectError:
            print(clr(RED, f"FATAL: Cannot connect to {base_url}. Start the backend first."))
            print("  Run: cd backend && uvicorn main:app --reload")
            return 1

        total = passed = failed = skipped = errors = 0
        group_results: dict[str, dict] = {}

        for group_def in groups:
            gname = group_def.get("group", "?")

            # Group-level filter: match if any of the user-supplied tokens appear in gname
            if group_filter:
                matched = any(tok.upper() in gname.upper() for tok in group_filter)
                if not matched:
                    continue

            claim = group_def.get("paper_claim", "")
            print(f"{clr(CYAN, gname)}")
            if claim:
                print(f"  {clr(YELLOW, 'Claim:')} {claim}")

            g_pass = g_fail = g_skip = g_err = 0

            for test in group_def.get("tests", []):
                status, failures, body, elapsed = run_test(
                    client, test, timeout=args.timeout
                )
                print_result(test, status, failures, body, elapsed, verbose=args.verbose)

                total += 1
                if status == "pass":
                    passed += 1; g_pass += 1
                elif status == "fail":
                    failed += 1; g_fail += 1
                elif status == "skip":
                    skipped += 1; g_skip += 1
                else:
                    errors += 1; g_err += 1

            summary_parts = [f"pass={g_pass}", f"fail={g_fail}"]
            if g_skip: summary_parts.append(f"skip={g_skip}")
            if g_err: summary_parts.append(f"err={g_err}")
            print(f"  {'—'*50}")
            print(f"  Group summary: {', '.join(summary_parts)}\n")

            group_results[gname] = {"pass": g_pass, "fail": g_fail, "skip": g_skip, "err": g_err}

    # Final summary
    print(clr(CYAN, "=" * 55))
    print(f"  Total   : {total}")
    print(f"  {clr(GREEN, 'Passed')}  : {passed}")
    print(f"  {clr(RED, 'Failed')}  : {failed + errors}")
    print(f"  {clr(YELLOW, 'Skipped')} : {skipped}")
    pass_rate = (passed / max(total - skipped, 1)) * 100
    print(f"  Pass rate: {pass_rate:.1f}%")
    print(clr(CYAN, "=" * 55))

    if failed + errors == 0:
        print(clr(GREEN, "\n✓ ALL TESTS PASSED\n"))
        return 0
    else:
        print(clr(RED, f"\n✗ {failed + errors} test(s) FAILED\n"))
        return 1


def main() -> None:
    parser = argparse.ArgumentParser(
        description="KrishokChat E2E paper-claim test runner"
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="Backend base URL (default: http://127.0.0.1:8000)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=45.0,
        help="Per-request timeout in seconds (default: 45)",
    )
    parser.add_argument(
        "--group",
        nargs="+",
        help="Run only groups matching these prefix tokens (e.g. T0 T1 T3)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print answer previews for all tests",
    )
    parser.add_argument(
        "--local",
        action="store_true",
        help="Enable local model tests (T9 group with krishokchat-4b via Ollama)",
    )
    args = parser.parse_args()
    sys.exit(run_all(args))


if __name__ == "__main__":
    main()
