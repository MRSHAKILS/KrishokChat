"""Test classify_query directly."""
import sys
sys.path.insert(0, r"D:\KrishokChat Advisory System\backend")
from app.agents.safety_agent import classify_query

queries = [
    "এই রোগের প্রতিকার কি?",
    "আলুর দেরি ব্লাইট রোগের প্রতিকার কি?",
    "wheat leaf rust treatment",
    "potato late blight",
]

# Test without context
print("=== Without context ===")
for q in queries:
    r = classify_query(q)
    print(f"Query: {q}")
    print(f"  Category: {r['category']}")

# Test with context
print("\n=== With context (Wheat / Leaf Rust) ===")
context_queries = [
    "এই রোগের প্রতিকার কি?",
    "কীভাবে দূর করব?",
    "ওষুধ কী?",
]
for q in context_queries:
    r = classify_query(q, "Wheat", "Leaf Rust")
    print(f"Query: {q}")
    print(f"  Category: {r['category']}")
