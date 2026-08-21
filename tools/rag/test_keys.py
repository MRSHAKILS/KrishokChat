"""Quick test: parse .env keys and verify."""
import sys
from pathlib import Path

# Read .env
env_path = Path(r"D:\KrishokChat Advisory System\.env")
keys = []
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("GEMINI_API_KEY") and not line.startswith("GEMINI_API_KEYS"):
            val = line.split("=", 1)[1].strip().strip('"').strip("'")
            if " #" in val:
                val = val.split(" #")[0].strip()
            if val:
                keys.append(val)

print(f"Parsed {len(keys)} keys")
for i, k in enumerate(keys[:5]):
    print(f"  [{i}] {k[:20]}...{k[-5:]}")
if len(keys) > 5:
    print(f"  ... and {len(keys)-5} more")

# Split for 2 workers round-robin
keys_a = keys[::2]
keys_b = keys[1::2]
print(f"\nWorker A: {len(keys_a)} keys")
print(f"Worker B: {len(keys_b)} keys")
print(f"\nTotal nodes to refine: ~1,570 (skipping ~550 already-good)")
print(f"Estimated time: ~30-40 min with 2 workers")
