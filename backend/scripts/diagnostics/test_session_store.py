"""Test session store."""
import sys
sys.path.insert(0, r"D:\KrishokChat Advisory System\backend")
from app.services.advisory.session_store import session_store

s1 = "test-session-1"
session_store.append(s1, "user", "আলুর রোগ কী?")
session_store.append(s1, "assistant", "আলুরের দেরি ব্লাইট...")
session_store.append(s1, "user", "মাত্রা কত?")
h = session_store.get(s1)
print(f"History len: {len(h)}")
for m in h:
    print(f"  {m['role']}: {m['content'][:40]}")
session_store.clear(s1)
print(f"After clear: {len(session_store.get(s1))}")
print("OK")
