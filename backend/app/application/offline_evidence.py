"""Keyless evidence lane: verbatim, non-chemical sentences from crop-fenced retrieval.

Used only when the safety classifier is unreachable and OFFLINE_EVIDENCE_ENABLED is
true. Nothing is generated: sentences are copied from retrieved source passages.
A sentence is withheld when it carries a dose, an amount, a known chemical or an
application instruction, so the lane can describe a problem but never prescribe a
product or a quantity. Anything uncertain is dropped, never kept.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from app.domain.contracts import RetrievedSource
from app.domain.crop_scope import _ALIASES as _CROP_ALIAS_TABLE
from app.infrastructure.verification.dosage_claims import extract_claims

MAX_SOURCES = 3
MAX_SENTENCES_PER_SOURCE = 2
MIN_CHARS = 25
MAX_CHARS = 240

# Application and quantity language that signals an instruction rather than a description.
# Matched case-insensitively as substrings; over-matching only withholds more text.
_WITHHOLD_TERMS = (
    "স্প্রে", "spray", "প্রয়োগ", "ডোজ", "dose", "মাত্রা", "ছিটান", "ছিটিয়ে", "মিশিয়ে",
    "মিশ্রণ", "%", "ppm", "শতাংশ", "প্রতি লিটার", "প্রতি বিঘা", "প্রতি হেক্টর", "প্রতি শতক",
    "বিঘা প্রতি", "হেক্টর প্রতি", "একর প্রতি", "লিটার পানি", "পানিতে", "রাসায়নিক",
    "কেমিক্যাল", "chemical", "pesticide", "fungicide", "insecticide", "herbicide",
    # Imperative and use language: the lane describes a problem, it does not instruct.
    "করুন", "করবেন", "করতে হবে", "দিন", "নিন", "ব্যবহার", "ব্যবহৃত", "ছিটা", "মেশা", "মাখিয়ে",
)

# Any digit (ASCII or Bengali). A bare figure is not safe to show without its table:
# units can be glued to the next word and escape the amount parser.
_DIGIT_RE = re.compile(r"[0-9০-৯]")

def _norm(text: str) -> str:
    """NFC. Bengali য় exists as U+09DF and as U+09AF U+09BC; the corpus mixes both."""
    return unicodedata.normalize("NFC", text)


_WITHHOLD_TERMS = tuple(_norm(t).lower() for t in _WITHHOLD_TERMS)

BOUNDARY_BN = (
    "সঠিক মাত্রা নিশ্চিত না হয়ে কোনো রাসায়নিক কীটনাশক প্রয়োগ করবেন না। "
    "মাঠ পরিদর্শনের পর নির্দিষ্ট ওষুধের জন্য স্থানীয় উপ-সহকারী কৃষি কর্মকর্তা (SAAO) বা "
    "কৃষি কল সেন্টারে (১৬১২৩) যোগাযোগ করুন।"
)

HEADER_BN = "আপনার প্রশ্নের শব্দের সাথে মিল থাকা নথি-অংশ (এআই দিয়ে তৈরি নয়; নিশ্চিত উত্তর নয়):"


_WORD_RE = re.compile(r"[ঀ-৿A-Za-z]{3,}")
_TRAILING_SIGNS = "ািীুূৃেৈোৌ্ংঃঁয়র"
MIN_STEM = 3

def _stem(word: str) -> str:
    """Strip up to two trailing vowel signs or inflection marks."""
    w = word.lower()
    for _ in range(2):
        if len(w) > MIN_STEM and w[-1] in _TRAILING_SIGNS:
            w = w[:-1]
    return w


# Question and filler words: they say nothing about which problem the farmer has and
# would let any passage "match" a question. Matched on the stem, so inflections are covered.
_GENERIC_WORDS = (
    "কেন", "কোন", "কোনো", "কোনও", "কিভাবে", "কীভাবে", "কিসের", "কখন", "কত", "কতটুকু", "কিছু",
    "করব", "করতে", "করছি", "করা", "করে", "করুন", "কারণ", "হচ্ছে", "হয়েছে", "হয়নি", "হবে", "হলো",
    "যাচ্ছে", "যায়", "আছে", "নাই", "নেই", "আমার", "আমি", "আপনার", "এখন", "এখনো", "এই", "এটা", "এটি",
    "উচিত", "সমস্যা", "সমাধান", "উপায়", "প্রতিকার", "পরামর্শ", "জানতে", "চাই", "বলুন", "দয়া", "দিন",
    "গাছ", "গাছে", "জমি", "জমিতে", "ক্ষেত", "ক্ষেতে", "ফসল", "চাষ", "রোগ", "পোকা", "সার", "ঔষধ", "ওষুধ",
    "স্প্রে", "সব", "খুব", "বেশি", "ভালো", "দেখা", "লাগছে", "ধরছে", "পাতা", "পাতায়", "ফলন", "সময়",
    "আর", "বা", "না", "তো", "মতো", "জন্য", "থেকে", "পরে", "আগে",
)
_GENERIC = frozenset(_stem(_norm(w)) for w in _GENERIC_WORDS)


def _is_crop_word(word: str) -> bool:
    low = word.lower()
    return any(low.startswith(alias) for alias, _crop in _CROP_ALIAS_TABLE)


def specific_terms(query: str) -> list[str]:
    """Stems of the query words that name a symptom or problem.

    Crop names, question words and filler are removed: a crop word is present in every
    crop-fenced passage by construction, and a filler word matches any prose.
    """
    out: list[str] = []
    for word in _WORD_RE.findall(_norm(query or "")):
        stem = _stem(word)
        if len(stem) < MIN_STEM or _is_crop_word(word):
            continue
        if stem in _GENERIC or any(len(g) >= 4 and stem.startswith(g) for g in _GENERIC):
            continue
        if stem not in out:
            out.append(stem)
    return out


def _shares_term(sentence: str, stems: list[str]) -> bool:
    words = [w.lower() for w in _WORD_RE.findall(sentence)]
    return any(w.startswith(stem) for stem in stems for w in words)


@dataclass(frozen=True)
class EvidenceExcerpt:
    text: str
    source_id: str
    title: str


def _is_clean(sentence: str, *, has_dosage: bool, chemicals: tuple[str, ...], failures: tuple[str, ...]) -> bool:
    if has_dosage or chemicals or failures:
        return False
    if not (MIN_CHARS <= len(sentence) <= MAX_CHARS):
        return False
    if _DIGIT_RE.search(sentence):
        return False
    low = sentence.lower()
    if any(term in low for term in _WITHHOLD_TERMS):
        return False
    # Imperative verbs end in -ুন (করুন, রাখুন, থাকুন, ফেলুন): the lane describes, never instructs.
    return not any(w.endswith("ুন") for w in re.findall(r"[ঀ-৿]+", low) if len(w) >= 3)


def clean_sentences(text: str) -> list[str]:
    """Return the sentences of ``text`` that carry no dose, chemical or instruction."""
    kept: list[str] = []
    for claim in extract_claims(_norm(text or "")):
        sentence = claim.sentence.strip()
        if _is_clean(sentence, has_dosage=claim.has_dosage, chemicals=claim.chemicals, failures=claim.parse_failures):
            kept.append(sentence)
    return kept


def select_excerpts(sources: list[RetrievedSource], terms: list[str]) -> list[EvidenceExcerpt]:
    """Pick up to MAX_SOURCES sources, each contributing clean sentences that share a rare
    word with the question. No shared word means no excerpt: topical overlap with the
    crop alone is not enough."""
    if not terms:
        return []
    excerpts: list[EvidenceExcerpt] = []
    used_sources = 0
    for source in sources:
        if used_sources >= MAX_SOURCES:
            break
        text = source.content_bn or source.content_en or ""
        sentences = [t for t in clean_sentences(text) if _shares_term(t, terms)][:MAX_SENTENCES_PER_SOURCE]
        if not sentences:
            continue
        title = source.title_bn or source.title_en or source.source or source.id
        for sentence in sentences:
            excerpts.append(EvidenceExcerpt(text=sentence, source_id=source.id, title=title))
        used_sources += 1
    return excerpts


def render_answer(excerpts: list[EvidenceExcerpt]) -> str:
    lines = [HEADER_BN, ""]
    lines.extend(f"• {e.text}  [{e.title}]" for e in excerpts)
    lines.extend(["", BOUNDARY_BN])
    return "\n".join(lines)
