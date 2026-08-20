"""Debug the local model streaming - captures all SSE events with timestamps."""
import urllib.request, json, sys, time

sys.stdout.reconfigure(encoding='utf-8')

data = json.dumps({
    "query": "ধান গাছে ব্লাস্ট রোগের লক্ষণ কী",
    "model": "krishokchat-4b"
}, ensure_ascii=False).encode('utf-8')

req = urllib.request.Request(
    "http://127.0.0.1:8000/api/qa/stream",
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST"
)

print(f"[{time.strftime('%H:%M:%S')}] Sending request with model=krishokchat-4b ...")
t0 = time.time()

try:
    with urllib.request.urlopen(req, timeout=300) as r:
        print(f"[{time.strftime('%H:%M:%S')}] Connection established, reading SSE stream...")
        buf = ""
        decoder_buf = b""
        final_received = False
        
        while True:
            chunk = r.read(256)
            if not chunk:
                print(f"[{time.strftime('%H:%M:%S')}] Stream ended (EOF)")
                break
            
            decoder_buf += chunk
            try:
                text = decoder_buf.decode('utf-8')
                decoder_buf = b""
            except UnicodeDecodeError:
                continue
                
            buf += text
            lines = buf.split("\n")
            buf = lines.pop()
            
            for line in lines:
                t = line.strip()
                if not t:
                    continue
                elapsed = time.time() - t0
                if t.startswith(": keepalive"):
                    print(f"[+{elapsed:.1f}s] KEEPALIVE (pipeline still running...)")
                elif t.startswith("data:"):
                    try:
                        event = json.loads(t[5:].strip())
                        print(f"[+{elapsed:.1f}s] STAGE: {event.get('stage')} → {event.get('status')} | {event.get('detail','')[:60]}")
                    except:
                        print(f"[+{elapsed:.1f}s] RAW DATA: {t[:100]}")
                elif t.startswith("token:"):
                    try:
                        tok = json.loads(t[6:].strip())
                        print(f"[+{elapsed:.1f}s] TOKEN: {tok.get('text','')[:50]}")
                    except:
                        print(f"[+{elapsed:.1f}s] RAW TOKEN: {t[:100]}")
                elif t.startswith("final:"):
                    final_received = True
                    try:
                        final = json.loads(t[6:].strip())
                        print(f"\n[+{elapsed:.1f}s] ✅ FINAL RECEIVED!")
                        print(f"  Category: {final.get('category')}")
                        print(f"  Model: {final.get('model')}")
                        print(f"  Answer: {final.get('answer','')[:150]}")
                    except Exception as e:
                        print(f"[+{elapsed:.1f}s] ❌ FINAL PARSE ERROR: {e}")
                else:
                    print(f"[+{elapsed:.1f}s] UNKNOWN: {t[:100]}")
        
        if not final_received:
            print(f"\n❌ Stream ended WITHOUT final: event! Total time: {time.time()-t0:.1f}s")
        else:
            print(f"\n✅ Done in {time.time()-t0:.1f}s")

except Exception as e:
    print(f"\n❌ ERROR after {time.time()-t0:.1f}s: {type(e).__name__}: {e}")
