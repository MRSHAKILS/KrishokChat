"""Test QA pipeline directly."""
import asyncio
import sys
sys.path.insert(0, r"D:\KrishokChat Advisory System\backend")

from app.agents.safety_agent import classify_query
from app.agents.retrieval_agent import retrieve
from app.agents.generation_agent import generate_answer


async def main():
    query = "আলুর দেরি ব্লাইট রোগের প্রতিকার কি?"
    print(f"Query: {query}")

    # Safety
    safety = classify_query(query)
    print(f"Safety: {safety['category']}")

    # Retrieval
    sources = retrieve(query, top_k=10)
    print(f"Sources: {len(sources)}")
    for s in sources[:5]:
        print(f"  {s['id'][:40]:40s} score={s['score']:.2f} title={s.get('title_en','')[:40]}")

    # Generation
    gen = generate_answer(query, sources)
    print(f"Answer: {gen['answer'][:300]}")
    print(f"Confidence: {gen['confidence']}")


asyncio.run(main())
