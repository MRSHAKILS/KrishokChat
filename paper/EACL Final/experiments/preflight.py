"""Pre-flight 1-token auth test (AGENTS.md 0.1). Aborts (exit 1) on 401/403."""
import os
import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

KEY = None
for path in ("D:/KrishokChat Advisory System/.env",
             "D:/KrishokChat Advisory System/backend/.env"):
    try:
        for line in open(path, encoding="utf-8"):
            if line.strip().startswith("OPENROUTER_API_KEY"):
                KEY = line.split("=", 1)[1].strip().strip("'").strip('"')
    except OSError:
        pass

if not KEY:
    print("PRE-FLIGHT FAIL: no OPENROUTER_API_KEY found")
    raise SystemExit(1)

import httpx

# Retry transient transport errors (flaky network resets observed); 401/403
# and unexpected statuses abort immediately — never retried.
r = None
for attempt in range(3):
    try:
        r = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": "Bearer " + KEY,
                     "HTTP-Referer": "krishokchat-preflight",
                     "X-Title": "krishokchat-preflight"},
            json={"model": "google/gemini-2.5-flash-lite",
                  "messages": [{"role": "user", "content": "ping"}],
                  "max_tokens": 1, "temperature": 0},
            timeout=30)
        break
    except Exception as e:
        print(f"PRE-FLIGHT transient error (attempt {attempt + 1}/3):",
              type(e).__name__, str(e)[:100])
        time.sleep(5)
else:
    print("PRE-FLIGHT FAIL: transport failed after retries")
    raise SystemExit(1)

print("HTTP:", r.status_code)
if r.status_code in (401, 403):
    print("PRE-FLIGHT FAIL: unauthorized/forbidden - ABORTING per money rules")
    raise SystemExit(1)
if r.status_code == 200:
    try:
        usage = r.json().get("usage", {})
    except Exception:
        usage = {}
    print("PRE-FLIGHT PASS: key authorized. usage:", usage)
    raise SystemExit(0)
print("PRE-FLIGHT FAIL: unexpected status", r.status_code, r.text[:200])
raise SystemExit(1)
