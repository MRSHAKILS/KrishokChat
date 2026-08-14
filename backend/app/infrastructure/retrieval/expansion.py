"""Query expansion for retrieval (P3).

Expands Bengali colloquial terms to English terms the BM25 (English corpus)
and dense (BGE-M3) channels can match. The base map is corpus-derived
(indexes/term_map.json from 05_build_term_map.py). When the researcher's
110-word dialect map (dataset_release/safety/phase4_dialect_map.json) is
restored, it is merged automatically — its absence degrades nothing.
"""
from __future__ import annotations

import json
from pathlib import Path

DEFAULT_MAX_TERMS = 8
DEFAULT_MAX_LEN = 512


class QueryExpander:
    def __init__(self, term_map_path: Path, dialect_map_path: Path | None = None) -> None:
        self.term_map_path = term_map_path
        self.dialect_map_path = dialect_map_path
        self._terms: list[tuple[str, str]] = []  # (bn, en), longest bn first
        self._loaded = False

    def _load(self) -> list[tuple[str, str]]:
        if self._loaded:
            return self._terms
        pairs: list[tuple[str, str]] = []
        if self.term_map_path.exists():
            try:
                data = json.loads(self.term_map_path.read_text(encoding="utf-8"))
                entries = data.get("map", data) if isinstance(data, dict) else data
                for entry in entries:
                    if isinstance(entry, dict):
                        bn = entry.get("bn") or entry.get("dialect") or ""
                        en = entry.get("en") or entry.get("standard") or ""
                    elif isinstance(entry, (list, tuple)) and len(entry) == 2:
                        bn, en = entry
                    else:
                        continue
                    if bn and en:
                        pairs.append((str(bn).strip(), str(en).strip()))
            except (OSError, json.JSONDecodeError, ValueError):
                pairs = []
        if self.dialect_map_path and self.dialect_map_path.exists():
            try:
                data = json.loads(self.dialect_map_path.read_text(encoding="utf-8"))
                entries = data.get("map", data) if isinstance(data, dict) else data
                if isinstance(entries, dict):  # {"dialect_term": "standard_term"}
                    entries = [{"bn": k, "en": v} for k, v in entries.items()]
                for entry in entries:
                    if not isinstance(entry, dict):
                        continue
                    bn = entry.get("bn") or entry.get("dialect") or ""
                    en = entry.get("en") or entry.get("standard") or ""
                    if bn and en:
                        pairs.append((str(bn).strip(), str(en).strip()))
            except (OSError, json.JSONDecodeError, ValueError):
                pass
        # Longest-first so the most specific term wins substring matching.
        pairs.sort(key=lambda p: len(p[0]), reverse=True)
        self._terms = pairs
        self._loaded = True
        return self._terms

    def expand(self, query: str, *, max_terms: int = DEFAULT_MAX_TERMS, max_len: int = DEFAULT_MAX_LEN) -> tuple[str, list[str]]:
        """Return (expanded_query, matched_terms) where matched_terms are
        "বাংলা→English" strings for the trace."""
        terms = self._load()
        if not terms:
            return query, []
        lowered = query.lower()
        matched: list[str] = []
        additions: list[str] = []
        for bn, en in terms:
            if len(matched) >= max_terms:
                break
            if bn.lower() in lowered and bn not in additions:
                matched.append(f"{bn}→{en}")
                additions.append(en)
        if not additions:
            return query, []
        expanded = query
        for en in additions:
            if len(expanded) >= max_len:
                break
            expanded = f"{expanded} {en}"
        return expanded, matched