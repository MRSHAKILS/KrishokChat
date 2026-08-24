"""BD-grounded banned/cancelled pesticide active-ingredient registry.

Source-attributed, curated data for the deterministic
``banned_or_restricted_chemical`` safety gate (see
``app.domain.safety_policy``). This module intentionally contains ONLY active
ingredients that are legally **cancelled / banned** for agricultural use in
Bangladesh — advising any of them is always wrong, so a bare mention can be
refused with near-zero over-block risk.

It deliberately does NOT list Highly Hazardous Pesticides (HHPs) that remain
legally *registered* (e.g. Chlorpyrifos, Abamectin). Blanket-refusing a
mention of a still-registered product would over-block legitimate advice and
misstate the law; nuanced HHP handling (misuse/overdose context + IPM
alternatives) belongs to a later verifier-side task, not this blunt gate.

Sources (snapshot, not live-fetched):
- DAE "List of Cancelled Pesticides in Bangladesh" (Plant Protection Wing).
- PPW বাতিলকৃত বালাইনাশক তালিকা — ppw.krishi.gov.bd/pesticide-list-expired.
- Import Policy Order controlled-items list (Heptachlor, DDT, Dicrotophos,
  Methyl Bromide, Chlordane, Dieldrin explicitly named as banned).
- Banglapedia "Insecticide": DDT restricted; Endrin prohibited since 1962;
  cyclodienes (Chlordane, Heptachlor, Aldrin, Dieldrin, Endrin) and
  BHC/Lindane withdrawn.
- The Pesticides Act 2018 / Pesticide Rules 1985 / Ordinance 1971 (legal base).

Design rules:
- English aliases are matched with word boundaries (``\b``).
- Bengali has no word boundaries, so every Bengali alias MUST be a distinctive
  transliteration that cannot be a substring of a common Bengali word.
- Each active carries a stable ``rule`` tag (e.g. ``banned_active:ddt``) so the
  audit trail records exactly which banned ingredient fired.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class BannedActive:
    """One legally-cancelled/banned active ingredient with its match aliases."""

    rule: str  # stable audit tag, e.g. "banned_active:ddt"
    canonical_en: str
    en_aliases: tuple[str, ...] = ()  # matched with \b word boundaries, case-insensitive
    bn_aliases: tuple[str, ...] = field(default=())  # distinctive Bengali transliterations
    source: str = ""


# Curated list. Kept conservative and well-attested; each entry is a definitively
# banned/cancelled agricultural active in Bangladesh.
BANNED_ACTIVES: tuple[BannedActive, ...] = (
    # --- Organochlorines / cyclodienes (banned; long-persistent, POP-listed) ---
    BannedActive(
        rule="banned_active:ddt",
        canonical_en="DDT",
        en_aliases=("ddt", "dichlorodiphenyltrichloroethane"),
        bn_aliases=("ডিডিটি",),
        source="Banglapedia; IPO controlled-items list",
    ),
    BannedActive(
        rule="banned_active:aldrin",
        canonical_en="Aldrin",
        en_aliases=("aldrin",),
        bn_aliases=("অলড্রিন", "অ্যালড্রিন"),
        source="Banglapedia; DAE cancelled list",
    ),
    BannedActive(
        rule="banned_active:dieldrin",
        canonical_en="Dieldrin",
        en_aliases=("dieldrin",),
        bn_aliases=("ডাইএলড্রিন", "ডিলড্রিন"),
        source="DAE cancelled list; IPO controlled-items list",
    ),
    BannedActive(
        rule="banned_active:endrin",
        canonical_en="Endrin",
        en_aliases=("endrin",),
        bn_aliases=("এনড্রিন",),
        source="Banglapedia (prohibited since 1962)",
    ),
    BannedActive(
        rule="banned_active:heptachlor",
        canonical_en="Heptachlor",
        en_aliases=("heptachlor", "heptachlore"),
        bn_aliases=("হেপ্টাক্লোর",),
        source="IPO controlled-items list; DAE cancelled list",
    ),
    BannedActive(
        rule="banned_active:chlordane",
        canonical_en="Chlordane",
        en_aliases=("chlordane", "chlorden"),
        bn_aliases=("ক্লোরডেন",),
        source="IPO controlled-items list; DAE cancelled list",
    ),
    BannedActive(
        rule="banned_active:bhc_lindane",
        canonical_en="BHC / Lindane",
        en_aliases=("lindane", "gamma bhc", "gamma-bhc"),
        bn_aliases=("লিন্ডেন",),
        source="Banglapedia (BHC/Lindane withdrawn)",
    ),
    BannedActive(
        rule="banned_active:endosulfan",
        canonical_en="Endosulfan",
        en_aliases=("endosulfan",),
        bn_aliases=("এনডোসালফান", "এন্ডোসালফান"),
        source="DAE banned list (retained from prior policy)",
    ),
    # --- Fumigants / others explicitly named as banned ---
    BannedActive(
        rule="banned_active:methyl_bromide",
        canonical_en="Methyl Bromide",
        en_aliases=("methyl bromide", "methylbromide", "methybron", "mebrom"),
        bn_aliases=("মিথাইল ব্রোমাইড",),
        source="IPO controlled-items list; DAE cancelled list",
    ),
    # --- Organophosphates / carbamates on the cancelled list ---
    BannedActive(
        rule="banned_active:methyl_parathion",
        canonical_en="Methyl parathion",
        en_aliases=("methyl parathion", "parathion"),
        bn_aliases=("প্যারাথিয়ন", "মিথাইল প্যারাথিয়ন"),
        source="DAE cancelled list (retained from prior policy)",
    ),
    BannedActive(
        rule="banned_active:carbofuran",
        canonical_en="Carbofuran",
        en_aliases=("carbofuran", "furadan", "curaterr"),
        bn_aliases=("কার্বোফুরান",),
        source="DAE cancelled list (Furadan/Curaterr cancelled)",
    ),
    BannedActive(
        rule="banned_active:dichlorvos",
        canonical_en="Dichlorvos (DDVP)",
        en_aliases=("dichlorvos", "ddvp", "vapona", "nogos"),
        bn_aliases=("ডাইক্লোরভস",),
        source="DAE cancelled list (Dichlorvos/DDVP/Vapona cancelled)",
    ),
    BannedActive(
        rule="banned_active:monocrotophos",
        canonical_en="Monocrotophos",
        en_aliases=("monocrotophos", "azodrin", "nuvacron", "monodrin"),
        bn_aliases=("মনোক্রোটোফস",),
        source="DAE cancelled list (Azodrin/Nuvacron/Monodrin cancelled)",
    ),
    # --- Herbicides under national policy action (retained flagship HHPs) ---
    BannedActive(
        rule="banned_active:paraquat",
        canonical_en="Paraquat",
        en_aliases=("paraquat",),
        bn_aliases=("প্যারাকোয়াট", "পরাকুয়াট"),
        source="DAE Dec-2024 no-new-registration decision (The Daily Star 2025-11-25)",
    ),
    BannedActive(
        rule="banned_active:glyphosate",
        canonical_en="Glyphosate",
        en_aliases=("glyphosate",),
        bn_aliases=("গ্লাইফোসেট",),
        source="DAE Dec-2024 no-new-registration decision (The Daily Star 2025-11-25)",
    ),
)


def _compile_en(active: BannedActive) -> re.Pattern[str] | None:
    if not active.en_aliases:
        return None
    alts = "|".join(re.escape(alias) for alias in active.en_aliases)
    return re.compile(rf"\b(?:{alts})\b", re.IGNORECASE)


def _compile_bn(active: BannedActive) -> re.Pattern[str] | None:
    if not active.bn_aliases:
        return None
    # Bengali has no word boundaries; rely on distinctive transliterations.
    alts = "|".join(re.escape(alias) for alias in active.bn_aliases)
    return re.compile(alts)


def compiled_banned_patterns() -> tuple[tuple[str, re.Pattern[str]], ...]:
    """Return ``(rule_name, pattern)`` entries for the safety precheck.

    English and Bengali aliases are emitted as separate entries (suffixed
    ``:en`` / ``:bn``) so ``matched_rules`` in the audit trail records both the
    banned active and the language surface that matched.
    """
    entries: list[tuple[str, re.Pattern[str]]] = []
    for active in BANNED_ACTIVES:
        en = _compile_en(active)
        if en is not None:
            entries.append((f"{active.rule}:en", en))
        bn = _compile_bn(active)
        if bn is not None:
            entries.append((f"{active.rule}:bn", bn))
    return tuple(entries)
