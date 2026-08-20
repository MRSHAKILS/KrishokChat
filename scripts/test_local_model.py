"""Quick test that the local KrishokChat-4B model responds via Ollama."""
import urllib.request, json, sys, time

sys.stdout.reconfigure(encoding='utf-8')

# Test 1: direct Ollama API
print("Test 1: Direct Ollama API (http://127.0.0.1:11434)")
try:
    data = json.dumps({
        "model": "krishokchat-4b",
        "prompt": "ধান গাছের পাতায় বাদামি দাগ দেখা দিলে কী করব?",
        "stream": False,
        "options": {"num_predict": 80}
    }).encode('utf-8')
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=120) as r:
        result = json.load(r)
    elapsed = time.time() - t0
    print(f"  OK - {elapsed:.1f}s")
    print(f"  Response: {result.get('response','')[:200]}")
except Exception as e:
    print(f"  ERROR: {e}")

# Test 2: via backend API with model=krishokchat-4b
print("\nTest 2: Backend /api/qa with model=krishokchat-4b")
try:
    data = json.dumps({
        "query": "ধান চাষে ইউরিয়া সারের পরিমাণ কতটুকু?",
        "model": "krishokchat-4b"
    }, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/qa",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=120) as r:
        result = json.load(r)
    elapsed = time.time() - t0
    print(f"  OK - {elapsed:.1f}s")
    print(f"  Category: {result.get('category')}")
    print(f"  Model: {result.get('model')}")
    print(f"  Answer (first 200 chars): {result.get('answer','')[:200]}")
except Exception as e:
    print(f"  ERROR: {e}")
