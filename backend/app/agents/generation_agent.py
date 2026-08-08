"""Generation Agent — grounded answer from retrieved sources."""
from __future__ import annotations


def generate_answer(query: str, sources: list[dict]) -> dict:
    if not sources:
        return {
            "answer": "দুঃখিত, আপনার প্রশ্নের উত্তর দেওয়ার মতো পর্যাপ্ত তথ্য খুঁজে পাওয়া যায়নি।",
            "used_source_ids": [],
            "confidence": "low_confidence",
            "note": "LLM unavailable — no relevant sources found.",
        }

    parts = []
    used = []
    for s in sources[:3]:
        text = s.get("content_bn") or s.get("content_en") or ""
        title = s.get("title_bn") or s.get("title_en") or s.get("category", "")
        if text:
            parts.append(f"{title}: {text[:400]}")
            used.append(s["id"])

    context = "\n\n".join(parts)
    first_title = (sources[0].get("title_bn") or sources[0].get("title_en") or "").strip()

    answer = (
        f"প্রাসঙ্গিক তথ্য:\n{context}\n\n"
        "⚠️ লোকাল LLM সংযুক্ত নেই — উত্তরটি শুধুমাত্র সংগৃহীত তথ্য থেকে নেওয়া হয়েছে। "
        "সঠিক মাত্রা জানতে কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২৩।"
    )
    return {
        "answer": answer,
        "used_source_ids": used,
        "confidence": "verified" if len(sources) >= 3 else "low_confidence",
        "note": "LLM unavailable — answer extracted from retrieved sources. Verify dosages with expert or 16123.",
    }
