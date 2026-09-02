"""Debug retrieval for potato late blight."""
import sys
sys.path.insert(0, r"D:\KrishokChat Advisory System\backend")
from app.agents.retrieval_agent import retrieve

queries = [
    "potato late blight treatment",
    "আলুর দেরি ব্লাইট",
    "late blight potato",
]

for q in queries:
    print(f"\n=== Query: {q} ===")
    tokens = q.lower().split()
    print(f"  Tokens: {tokens}")
    sources = retrieve(q, top_k=5)
    for s in sources:
        print(f"  {s['score']:.1f} {s['id'][:40]:40s} {s.get('title_en','')[:50]}")
