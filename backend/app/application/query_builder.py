from __future__ import annotations

from app.domain.contracts import QueryContext


BNGLISH_TERMS = {
    "আলুর": "potato", "আলু": "potato", "আলুত": "potato", "ধান": "rice", "ধানর": "rice", "গম": "wheat", "ভুট্টা": "corn",
    "ফুলকপি": "cauliflower", "বাঁধাকপি": "cabbage", "টমেটো": "tomato", "মরিচ": "chilli", "মরিস": "chilli",
    "বেগুন": "brinjal", "বাইঙ্গন": "brinjal", "begun": "brinjal",
    "লেট ব্লাইট": "late blight", "নাবি ধসা": "late blight", "নাবি ধ্বসা": "late blight", "দেরি ব্লাইট": "late blight",
    "আর্লি ব্লাইট": "early blight", "আগাম ধসা": "early blight", "মড়ক": "late blight", "মড়ক": "late blight",
    "খোলপোড়া": "sheath blight", "ব্লাস্ট": "blast", "রাস্ট": "rust", "মরিচা": "leaf rust",
    "পুইড়া": "blight burn", "পইড়া": "blight burn", "কুকড়ে": "leaf curl", "কুকড়াইয়া": "leaf curl",
    "পচা": "rot", "পচি": "rot", "পোকা": "pest", "পোঁকা": "pest", "পোকায়": "pest",
    "প্রতিকার": "treatment", "রোগ": "disease", "বীজ": "seed", "সার": "fertilizer",
    "কৃষি": "agriculture", "ফসল": "crop", "নির্ণয়": "diagnosis",
}


def build_retrieval_query(query: str, context: QueryContext, category: str) -> str:
    terms = [query]
    lowered = query.lower()
    # Token-start matching (fix 2026-09-17): plain substring matching injected
    # false bridge terms because Bengali vowel signs defeat \b (e.g. "ধান"→rice
    # fired inside "সমাধান"=solution). Single-word keys must open a token;
    # multi-word keys (contain a space) keep substring matching. Residual risk:
    # tokens merely starting with a key (place names); other substring keyword
    # lists (follow-up/fertilizer/symptom) are unchanged and noted as residual.
    tokens = lowered.split()
    for bengali, english in BNGLISH_TERMS.items():
        key = bengali.strip().lower()
        if not key:
            continue
        if " " in key:
            hit = key in lowered
        else:
            hit = any(tok == key or tok.startswith(key) for tok in tokens)
        if hit:
            terms.append(english)
    if context.crop:
        terms.append(context.crop.replace("__", " ").replace("_", " ").lower())
    if context.disease:
        terms.append(context.disease.replace("__", " ").replace("_", " ").lower())
    terms.append(category)
    return " ".join(dict.fromkeys(term.strip() for term in terms if term.strip()))
