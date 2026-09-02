"""Test retrieval augmentation."""
import sys
sys.path.insert(0, r"D:\KrishokChat Advisory System\backend")
from app.agents.retrieval_agent import retrieve

# Simulate augmented query with detected crop/disease
aug = "এই রোগের প্রতিকার কি? প্রতিকার treatment wheat leaf rust leaf rust"
srcs = retrieve(aug, top_k=5)
print("With augmentation:")
for s in srcs:
    print(f"  {s['score']:.1f} {s['id'][:40]:40s} {s.get('title_en','')[:50]}")

print("\nWithout augmentation:")
aug2 = "এই রোগের প্রতিকার কি?"
srcs2 = retrieve(aug2, top_k=5)
for s in srcs2:
    print(f"  {s['score']:.1f} {s['id'][:40]:40s} {s.get('title_en','')[:50]}")
