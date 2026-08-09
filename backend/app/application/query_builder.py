from __future__ import annotations

from app.domain.contracts import QueryContext


BNGLISH_TERMS = {
    "আলুর": "potato", "আলু": "potato", "ধান": "rice", "গম": "wheat", "ভুট্টা": "corn",
    "ফুলকপি": "cauliflower", "বাঁধাকপি": "cabbage", "টমেটো": "tomato", "মরিচ": "chilli",
    "দেরি ব্লাইট": "late blight", "ব্লাস্ট": "blast", "রাস্ট": "rust", "মরিচা": "leaf rust",
    "প্রতিকার": "treatment", "রোগ": "disease", "বীজ": "seed", "সার": "fertilizer",
    "কৃষি": "agriculture", "ফসল": "crop", "নির্ণয়": "diagnosis",
}


def build_retrieval_query(query: str, context: QueryContext, category: str) -> str:
    terms = [query]
    lowered = query.lower()
    terms.extend(english for bengali, english in BNGLISH_TERMS.items() if bengali in lowered)
    if context.crop:
        terms.append(context.crop.replace("__", " ").replace("_", " ").lower())
    if context.disease:
        terms.append(context.disease.replace("__", " ").replace("_", " ").lower())
    terms.append(category)
    return " ".join(dict.fromkeys(term.strip() for term in terms if term.strip()))
