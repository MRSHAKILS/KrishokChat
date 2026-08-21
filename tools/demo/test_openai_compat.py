import urllib.request, json, sys, time
sys.stdout.reconfigure(encoding='utf-8')

data = json.dumps({
    "model": "krishokchat-4b",
    "messages": [{"role": "user", "content": "ধান গাছে ব্লাস্ট রোগ কি?"}],
    "max_tokens": 80
}).encode('utf-8')
req = urllib.request.Request(
    "http://127.0.0.1:11434/v1/chat/completions",
    data=data,
    headers={"Content-Type": "application/json", "Authorization": "Bearer ollama"},
    method="POST"
)
t0 = time.time()
try:
    with urllib.request.urlopen(req, timeout=120) as r:
        result = json.load(r)
    elapsed = time.time() - t0
    content = result.get('choices', [{}])[0].get('message', {}).get('content', '?')
    print(f"OK in {elapsed:.1f}s: {content[:200]}")
except Exception as e:
    print(f"ERROR: {e}")
