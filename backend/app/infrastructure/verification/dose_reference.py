"""F1-02: corpus-derived registered-dose reference + gross-outlier check.

Two concerns live here:

1. **Offline extraction** (``build_dose_reference_entries`` + the thin CLI
   ``scripts/build_dose_reference.py``): scan the RAG corpus for sentences that
   pair a known pesticide active (canonical EN, Bengali transliteration, or an
   attested trade name) with a numeric spray/field rate (``ml/l``, ``g/l``,
   ``g/ha``, ``kg/ha``). Every entry carries the corpus node id, citation, and
   the matched snippet — nothing is invented (AGENTS.md §2.5). Output is
   deterministic (sorted, no timestamps) so the committed artifact is
   reviewable diff-by-diff.

2. **Runtime check** (``DoseReference``): the verifier consults the loaded
   reference and flags a dosage claim ONLY when all of these hold —
   the claim names a chemical that maps to a referenced active, the claim
   sentence carries a per-litre (or per-hectare) context, the claim's unit
   matches the band's numerator exactly, and the value exceeds the band max by
   ``outlier_factor`` (default 3×). No context / no band / different unit /
   unknown chemical → no flag (fail-open to the entailment-only behavior).

Bengali digits are normalized; acre (একর) is deliberately NOT treated as a
hectare context (1 acre ≈ 0.40 ha, too close to the 3× factor to mix).
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

from app.infrastructure.verification.dosage_claims import (
    DosageClaim,
    normalize_chemical,
)

# ---------------------------------------------------------------------------
# Shared vocabulary
# ---------------------------------------------------------------------------

_BN_DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")

# Canonical actives -> surface aliases (all lowercase; every alias must be
# attested in the corpus — see F1-02 completion log for the frequency audit).
ACTIVE_ALIASES: dict[str, tuple[str, ...]] = {
    "carbendazim": ("carbendazim", "কার্বেন্ডাজিম"),
    "mancozeb": ("mancozeb", "ম্যানকোজেব"),
    "cypermethrin": ("cypermethrin", "সাইপারমেথ্রিন"),
    "chlorpyrifos": ("chlorpyrifos", "ক্লোরপাইরিফস", "ক্লোরোপাইরিফস", "dursban"),
    "imidacloprid": ("imidacloprid", "imidachlorpid", "ইমিডাক্লোপ্রিড", "admire", "imitaf"),
    "carbofuran": ("carbofuran", "কার্বোফুরান", "furadan"),
    "thiamethoxam": ("thiamethoxam", "থায়ামেথক্সাম", "virtako"),
    "acetamiprid": ("acetamiprid", "এসিটামিপ্রিড"),
    "emamectin": ("emamectin", "ইমামেক্টিন"),
    "spinosad": ("spinosad", "স্পাইনোসাড", "tracer"),
    "abamectin": ("abamectin", "অ্যাবামেক্টিন"),
    "deltamethrin": ("deltamethrin", "ডেল্টামেথ্রিন"),
    "propiconazole": ("propiconazole", "প্রোপিকোনাজল"),
    "tebuconazole": ("tebuconazole", "টেবুকোনাজল"),
    "azoxystrobin": ("azoxystrobin", "অ্যাজোক্সিস্ট্রোবিন"),
    "tricyclazole": ("tricyclazole", "ট্রাইসাইক্লাজল"),
    "cartap": ("cartap", "কারটাপ"),
    "fipronil": ("fipronil", "ফিপ্রোনিল"),
    "dimethoate": ("dimethoate", "ডাইমেথোয়েট"),
    "malathion": ("malathion", "ম্যালাথিয়ন"),
    "lambda-cyhalothrin": ("lambda-cyhalothrin", "lambda cyhalothrin", "karate"),
}

# alias (normalized) -> canonical active, built once.
_ALIAS_TO_ACTIVE: dict[str, str] = {
    normalize_chemical(alias): active
    for active, aliases in ACTIVE_ALIASES.items()
    for alias in aliases
}

_ALLOWED_BANDS = ("ml/l", "g/l", "g/ha", "kg/ha")

_NUM = r"(\d+(?:[.,]\d+)?)"
# English compound rates: "0.25 ml/litre", "1 ml/l of water", "1.5 kg a.i/ha",
# "2 g per litre", "625 g/ha".
_RATE_EN = re.compile(
    rf"{_NUM}\s*(ml|g|gm|gram|kg)\s*(?:a\.?i\.?\s*/\s*)?(?:/|per\s+)\s*(l(?![a-z])|litre|liter|ha(?![a-z])|hectare)",
    re.IGNORECASE,
)
# Bengali compound rates: "১ মিলি/লিটার", "২ গ্রাম/হেক্টর".
_RATE_BN = re.compile(
    rf"{_NUM}\s*(মিলি|গ্রাম|কেজি)\s*/\s*(লিটার|হেক্টর)",
)
# Bengali prose form: "প্রতি লিটার পানিতে ২ মিলি", "প্রতি হেক্টরে ১ কেজি".
_RATE_BN_PROSE = re.compile(
    r"প্রতি\s*(লিটার|হেক্টর)[^\d০-৯]{" r"0,30}?" rf"{_NUM}\s*(মিলি|গ্রাম|কেজি)",
)

_UNIT_CANON = {
    "ml": "ml", "g": "g", "gm": "g", "gram": "g", "kg": "kg",
    "মিলি": "ml", "গ্রাম": "g", "কেজি": "kg",
}
_DENOM_CANON = {
    "l": "l", "litre": "l", "liter": "l", "ha": "ha", "hectare": "ha",
    "লিটার": "l", "হেক্টর": "ha",
}

# Claim-sentence context signals (the denominator must be explicit — a bare
# "5 ml" in a mixing instruction is not comparable to a per-litre band).
_LITRE_CONTEXT = re.compile(
    r"প্রতি\s*লিটার|লিটার\s*পানি|মিলি/লিটার|গ্রাম/লিটার|per\s+litre|per\s+liter|/l(?![a-z])|ml/l|g/l",
    re.IGNORECASE,
)
_HA_CONTEXT = re.compile(
    r"প্রতি\s*হেক্টর|কেজি/হেক্টর|গ্রাম/হেক্টর|per\s+hectare|/ha(?![a-z])|a\.?i\.?/ha",
    re.IGNORECASE,
)


def _ascii_digits(text: str) -> str:
    return unicodedata.normalize("NFKC", text).translate(_BN_DIGITS)


def _value(raw: str) -> float:
    return float(raw.replace(",", "."))


# ---------------------------------------------------------------------------
# Offline extraction
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DoseReferenceEntry:
    active: str
    surface: str  # the alias that appeared next to the rate
    rate: float
    band: str  # one of _ALLOWED_BANDS
    node_id: str
    citation: str
    snippet: str

    def as_dict(self) -> dict[str, object]:
        return {
            "active": self.active,
            "surface": self.surface,
            "rate": self.rate,
            "band": self.band,
            "node_id": self.node_id,
            "citation": self.citation,
            "snippet": self.snippet,
        }


def _iter_rate_matches(text: str):
    """Yield (value, band, match) for every rate pattern in the text."""
    for m in _RATE_EN.finditer(text):
        num, unit, denom = m.group(1), m.group(2).lower(), m.group(3).lower()
        yield _value(num), f"{_UNIT_CANON[unit]}/{_DENOM_CANON[denom]}", m
    for m in _RATE_BN.finditer(text):
        num, unit, denom = m.group(1), m.group(2), m.group(3)
        yield _value(num), f"{_UNIT_CANON[unit]}/{_DENOM_CANON[denom]}", m
    for m in _RATE_BN_PROSE.finditer(text):
        num, unit = m.group(2), m.group(3)
        denom = m.group(1)
        yield _value(num), f"{_UNIT_CANON[unit]}/{_DENOM_CANON[denom]}", m


def build_dose_reference_entries(corpus_path: str | Path) -> list[DoseReferenceEntry]:
    """Extract (active, rate, citation) entries from the corpus JSONL.

    A rate binds to an active only when the alias occurs within ±120 characters
    of the rate in the same content field — node-level co-occurrence alone lets
    unrelated seed-rate numbers steal a chemical mentioned elsewhere in the node.
    """
    entries: list[DoseReferenceEntry] = []
    seen: set[tuple[str, str, float, str]] = set()
    with open(corpus_path, encoding="utf-8") as fh:
        for line in fh:
            node = json.loads(line)
            node_id = str(node.get("id", ""))
            citation = str(node.get("citation") or node.get("source_document") or "")[:140]
            for key in ("content_en", "content_bn"):
                text = node.get(key) or ""
                if not text:
                    continue
                normalized = _ascii_digits(text)
                lowered = normalized.lower()
                # Pre-compute alias positions once per field.
                positions: list[tuple[int, str]] = []
                for alias, active in _ALIAS_TO_ACTIVE.items():
                    if not alias:
                        continue
                    start = lowered.find(alias)
                    while start != -1:
                        positions.append((start, active))
                        start = lowered.find(alias, start + 1)
                for value, band, match in _iter_rate_matches(normalized):
                    if band not in _ALLOWED_BANDS:
                        continue
                    near = [
                        (pos, active)
                        for pos, active in positions
                        if abs(pos - match.start()) <= 120
                    ]
                    if not near:
                        continue
                    # Bind the closest alias occurrence.
                    pos, active = min(near, key=lambda pa: abs(pa[0] - match.start()))
                    # Cover BOTH the alias and the rate — in table-style text
                    # the alias can trail the rate by >100 chars, and a
                    # one-sided window would slice to an empty span.
                    lo = max(0, min(pos, match.start()) - 60)
                    hi = max(match.end(), pos + 30) + 40
                    span = normalized[lo:hi]
                    snippet = " ".join(span.split())[:170]
                    key4 = (active, band, value, node_id)
                    if key4 in seen:
                        continue
                    seen.add(key4)
                    surface_raw = lowered[pos : pos + 40].split()[0] if lowered[pos : pos + 40] else active
                    entries.append(
                        DoseReferenceEntry(
                            active=active,
                            surface=surface_raw,
                            rate=value,
                            band=band,
                            node_id=node_id,
                            citation=citation,
                            snippet=snippet,
                        )
                    )
    entries.sort(key=lambda e: (e.active, e.band, e.rate, e.node_id, e.snippet))
    return entries


# ---------------------------------------------------------------------------
# Runtime reference
# ---------------------------------------------------------------------------


@dataclass
class DoseReference:
    """Loaded reference: per (active, band) max rate + provenance for flags."""

    bands: dict[tuple[str, str], tuple[float, str]] = field(default_factory=dict)
    # (active, band) -> (max_rate, citation of the max-rate entry)
    entry_count: int = 0
    outlier_factor: float = 3.0

    @classmethod
    def disabled(cls) -> "DoseReference":
        return cls()

    @property
    def enabled(self) -> bool:
        return bool(self.bands)

    def outlier_details(self, claim: DosageClaim) -> list[str]:
        """Gross-outlier descriptions for one claim (empty = no opinion)."""
        if not self.bands or not claim.has_dosage:
            return []
        actives = {
            _ALIAS_TO_ACTIVE.get(chemical, chemical)
            for chemical in claim.chemicals
        } & set(a for a, _band in self.bands)
        if not actives:
            return []
        sentence = _ascii_digits(claim.sentence)
        litre_ctx = bool(_LITRE_CONTEXT.search(sentence))
        ha_ctx = bool(_HA_CONTEXT.search(sentence))
        details: list[str] = []
        for value, unit in claim.amounts:
            for active in sorted(actives):
                if unit in ("ml", "g") and litre_ctx:
                    band_key = (active, f"{unit}/l")
                elif unit in ("kg", "g") and ha_ctx:
                    band_key = (active, f"{unit}/ha")
                else:
                    continue
                hit = self.bands.get(band_key)
                if hit is None:
                    continue
                max_rate, citation = hit
                if value > max_rate * self.outlier_factor:
                    details.append(
                        f"{active} {value:g} {unit} vs referenced max "
                        f"{max_rate:g} {band_key[1]} ({citation or 'BARC corpus'})"
                    )
        return details


def load_dose_reference(
    path: str | Path, outlier_factor: float = 3.0
) -> DoseReference:
    """Load a dose-reference JSON; a missing/broken file disables the check."""
    import logging

    logger = logging.getLogger("krishokchat.dose_reference")
    try:
        with open(path, encoding="utf-8") as fh:
            payload = json.load(fh)
    except FileNotFoundError:
        logger.warning("dose reference not found at %s — outlier check disabled", path)
        return DoseReference.disabled()
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("dose reference unreadable at %s (%s) — outlier check disabled", path, exc)
        return DoseReference.disabled()

    bands: dict[tuple[str, str], tuple[float, str]] = {}
    for entry in payload.get("entries", []):
        active = normalize_chemical(str(entry.get("active", "")))
        band = str(entry.get("band", ""))
        if not active or band not in _ALLOWED_BANDS:
            continue
        try:
            rate = float(entry.get("rate"))
        except (TypeError, ValueError):
            continue
        citation = str(entry.get("citation", ""))[:140]
        key = (active, band)
        current = bands.get(key)
        if current is None or rate > current[0]:
            bands[key] = (rate, citation)
    if not bands:
        logger.warning("dose reference at %s carried no usable entries — check disabled", path)
        return DoseReference.disabled()
    return DoseReference(bands=bands, entry_count=len(payload.get("entries", [])), outlier_factor=outlier_factor)
