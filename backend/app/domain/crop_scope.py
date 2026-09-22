"""Post-retrieval crop filter (hard evidence fence).

Once a crop is bound, drop retrieved passages that mention only other crops.
Passages that mention no crop (soil, weather, general IPM) and passages that
mention the bound crop are kept. Crop mentions are found with the same alias
table the rest of the pipeline uses (`app.domain.intent._CROP_ALIASES`).

Disable with the environment variable RETRIEVAL_CROP_FILTER=0.
"""
from __future__ import annotations

import os
import re
from collections.abc import Iterable

from app.domain.contracts import RetrievedSource
from app.domain.intent import _CROP_ALIASES

_TOKEN_RE = re.compile(r"[\wঀ-৿]+")


def _alias_table() -> tuple[tuple[str, str], ...]:
    pairs: dict[str, str] = {}
    for crop, aliases in _CROP_ALIASES.items():
        for alias in aliases:
            alias = str(alias).strip().lower()
            if alias and alias not in pairs:
                pairs[alias] = crop
    return tuple(sorted(pairs.items(), key=lambda p: len(p[0]), reverse=True))


_ALIASES = _alias_table()
_CACHE: dict[str, frozenset[str]] = {}


def crop_filter_enabled() -> bool:
    return os.getenv("RETRIEVAL_CROP_FILTER", "1").strip() != "0"


def passage_crops(source: RetrievedSource) -> frozenset[str]:
    """Crops named anywhere in a passage's title, content, citation or metadata."""
    key = source.id
    cached = _CACHE.get(key) if key else None
    if cached is not None:
        return cached
    texts = [source.title_en, source.title_bn, source.source, source.citation,
             source.content_en, source.content_bn]
    meta = source.metadata or {}
    for field_name in ("section_title", "title_en", "title_bn", "category", "publisher"):
        value = meta.get(field_name, "")
        if isinstance(value, str) and value:
            texts.append(value)
    tags = meta.get("tags", [])
    if isinstance(tags, list):
        texts.extend(str(t) for t in tags if isinstance(t, str))
    blob = "\n".join(t for t in texts if t).lower()
    tokens = set(_TOKEN_RE.findall(blob))
    found = frozenset(
        crop for alias, crop in _ALIASES
        if (alias in blob if " " in alias else alias in tokens)
    )
    if key:
        _CACHE[key] = found
    return found


def filter_by_crop(
    sources: Iterable[RetrievedSource], crop: str | None, top_k: int
) -> tuple[list[RetrievedSource], int]:
    """Keep crop-neutral passages and passages naming `crop`; preserve order.

    Returns (kept[:top_k], number_removed). With no crop, returns the input unchanged.
    """
    sources = list(sources)
    if not crop or crop not in _CROP_ALIASES:
        # Unknown crop id: never filter, so an unmapped label cannot empty the evidence.
        return sources[:top_k], 0
    kept: list[RetrievedSource] = []
    removed = 0
    for source in sources:
        crops = passage_crops(source)
        if crops and crop not in crops:
            removed += 1
            continue
        kept.append(source)
    return kept[:top_k], removed
