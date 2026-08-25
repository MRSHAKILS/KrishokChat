"""R2 offline builder: build the fact-base artifact from corpus + curated seed.

Deterministic — same inputs yield a byte-identical artifact (sorted keys,
no timestamps in the payload body; provenance dates live in ``provenance``).

Run once after a corpus or seed rebuild:

    uv run python scripts/build_fact_base.py [--print] [--output PATH] [--seed PATH]

Build-time validation (the safety guarantee — R2 spec §Build-time validation):
  - dose_min / dose_max must be numeric, and min <= max.
  - active must NOT be in chemical_registry.BANNED_ACTIVES unless banned_flag=true.
  - stage must be a known key in crop_calendars_v1.json.
  - dose must not exceed the F1-02 outlier band (>= 3× reference max).
  - source_node_id must be non-empty OR grounding must be "curated-approximation".

Rejections are written to ``ml_assets/rag_index/derived/rejected/`` (R1 clause 6).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.domain.chemical_registry import BANNED_ACTIVES
from app.infrastructure.ingestion.contract import (
    ArtifactProvenance,
    write_deterministic_json,
)
from app.infrastructure.verification.dosage_claims import normalize_chemical

# Banned canonical active-ingredient names (all lowercase, normalised).
_BANNED_CANONICAL: frozenset[str] = frozenset(
    normalize_chemical(a.canonical_en)
    for a in BANNED_ACTIVES
)

DEFAULT_SEED = (
    Path(__file__).resolve().parents[1]
    / "ml_assets"
    / "rag_index"
    / "derived"
    / "curated_facts_v1.json"
)
DEFAULT_OUTPUT = (
    Path(__file__).resolve().parents[1]
    / "ml_assets"
    / "rag_index"
    / "derived"
    / "fact_base_v1.json"
)
DEFAULT_REJECTED = (
    Path(__file__).resolve().parents[1]
    / "ml_assets"
    / "rag_index"
    / "derived"
    / "rejected"
    / "fact_base_v1.rejected.json"
)
DEFAULT_CALENDARS = (
    Path(__file__).resolve().parents[1]
    / "ml_assets"
    / "agronomy"
    / "crop_calendars_v1.json"
)
DEFAULT_DOSE_REF = (
    Path(__file__).resolve().parents[1]
    / "ml_assets"
    / "rag_index"
    / "derived"
    / "dose_reference_v1.json"
)

OUTLIER_FACTOR = 3.0  # same as dose_reference.py


def _load_known_stages(calendars_path: Path) -> set[str]:
    """Return all stage keys from crop_calendars_v1.json."""
    try:
        with open(calendars_path, encoding="utf-8") as fh:
            cal = json.load(fh)
        stages: set[str] = set()
        for crop in cal.get("crops", []):
            for stage in crop.get("stages", []):
                key = stage.get("key")
                if key:
                    stages.add(str(key))
        return stages
    except (OSError, json.JSONDecodeError):
        return set()


def _load_dose_bands(dose_ref_path: Path) -> dict[tuple[str, str], float]:
    """Return (active_normalised, band) -> max_rate from dose_reference_v1.json."""
    try:
        with open(dose_ref_path, encoding="utf-8") as fh:
            dr = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {}
    bands: dict[tuple[str, str], float] = {}
    for entry in dr.get("entries", []):
        active = normalize_chemical(str(entry.get("active", "")))
        band = str(entry.get("band", ""))
        try:
            rate = float(entry["rate"])
        except (KeyError, TypeError, ValueError):
            continue
        key = (active, band)
        bands[key] = max(bands.get(key, 0.0), rate)
    return bands


def _validate_row(
    row: dict,
    known_stages: set[str],
    dose_bands: dict[tuple[str, str], float],
) -> str | None:
    """Return a rejection reason string, or None if the row is valid."""
    active = str(row.get("active_ingredient", ""))
    dose_min = row.get("dose_min")
    dose_max = row.get("dose_max")
    dose_unit = str(row.get("dose_unit", ""))
    stage = str(row.get("stage", ""))
    banned_flag = bool(row.get("banned_flag", False))
    grounding = str(row.get("grounding", ""))
    source_node_id = str(row.get("source_node_id", ""))

    # Dose fields must be numeric.
    try:
        dmin = float(dose_min)
        dmax = float(dose_max)
    except (TypeError, ValueError):
        return "dose_min or dose_max is non-numeric"

    if dmin > dmax:
        return f"dose_min ({dmin}) > dose_max ({dmax})"
    if dmin < 0 or dmax < 0:
        return "negative dose value"

    # Banned cross-check.
    active_norm = normalize_chemical(active)
    is_banned = active_norm in _BANNED_CANONICAL
    if is_banned and not banned_flag:
        return f"active '{active}' is banned but banned_flag=false"
    if not is_banned and banned_flag:
        return f"active '{active}' has banned_flag=true but is not in registry"

    # Stage must be a known calendar key.
    if known_stages and stage not in known_stages:
        return f"stage '{stage}' not in crop_calendars_v1.json known stages"

    # F1-02 outlier band: dose_max must not exceed 3× reference max.
    # Unit mapping: g/l -> "g/l", ml/l -> "ml/l", etc.
    band_key = (active_norm, dose_unit)
    ref_max = dose_bands.get(band_key)
    if ref_max is not None and dmax > ref_max * OUTLIER_FACTOR:
        return (
            f"dose_max ({dmax} {dose_unit}) exceeds {OUTLIER_FACTOR}× reference max "
            f"({ref_max} {dose_unit}) for {active}"
        )

    # Provenance: non-empty source_node_id OR curated-approximation.
    if not source_node_id and grounding != "curated-approximation":
        return "source_node_id is empty and grounding is not curated-approximation"

    return None  # valid


def build(
    seed_path: Path,
    calendars_path: Path,
    dose_ref_path: Path,
) -> tuple[list[dict], list[dict]]:
    """Return (validated_facts, rejected_facts)."""
    with open(seed_path, encoding="utf-8") as fh:
        seed = json.load(fh)

    known_stages = _load_known_stages(calendars_path)
    dose_bands = _load_dose_bands(dose_ref_path)

    valid: list[dict] = []
    rejected: list[dict] = []

    for row in seed.get("facts", []):
        reason = _validate_row(row, known_stages, dose_bands)
        if reason:
            rejected.append({**row, "_rejection_reason": reason})
        else:
            # Clean copy: remove any _rejection_reason leftover from a previous run.
            clean = {k: v for k, v in row.items() if not k.startswith("_")}
            valid.append(clean)

    # Sort deterministically by (crop, problem, stage, active_ingredient).
    valid.sort(key=lambda r: (r.get("crop", ""), r.get("problem", ""), r.get("stage", ""), r.get("active_ingredient", "")))
    rejected.sort(key=lambda r: (r.get("crop", ""), r.get("problem", ""), r.get("stage", "")))
    return valid, rejected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=Path, default=DEFAULT_SEED)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--rejected", type=Path, default=DEFAULT_REJECTED)
    parser.add_argument("--calendars", type=Path, default=DEFAULT_CALENDARS)
    parser.add_argument("--dose-ref", type=Path, default=DEFAULT_DOSE_REF)
    parser.add_argument("--print", action="store_true", dest="do_print")
    args = parser.parse_args()

    valid, rejected = build(args.seed, args.calendars, args.dose_ref)

    built_at = datetime.now(tz=timezone.utc).isoformat(timespec="seconds")
    payload: dict = {
        "version": 1,
        "provenance": ArtifactProvenance(
            source_id="curated_facts_v1.json",
            endpoint_or_file=str(args.seed.relative_to(Path(__file__).resolve().parents[1])),
            fetched_at=built_at,
            builder="backend/scripts/build_fact_base.py",
        ).as_dict(),
        "notes": (
            "Structured fact rows for the T1/T2 resolver (R4). "
            "Scope v1: potato late blight only. "
            "Every corpus-extracted row carries a source_node_id; "
            "curated-approximation rows carry grounding='curated-approximation'. "
            "No row was invented."
        ),
        "facts": valid,
    }

    # Write the artifact — the SHA-256 is recorded after writing.
    digest = write_deterministic_json(args.output, payload)

    # Update the provenance.sha256 in place and rewrite.
    payload["provenance"]["sha256"] = digest
    digest = write_deterministic_json(args.output, payload)

    # Write the rejection archive (R1 clause 6) — even if empty (honest).
    rejected_payload = {
        "version": 1,
        "built_at": built_at,
        "notes": "Rows rejected from curated_facts_v1.json during build. Each carries _rejection_reason.",
        "rejected": rejected,
    }
    write_deterministic_json(args.rejected, rejected_payload)

    print(f"wrote {len(valid)} facts -> {args.output}  (sha256: {digest[:16]}…)")
    print(f"rejected: {len(rejected)} rows -> {args.rejected}")
    by_crop: dict[str, int] = {}
    for r in valid:
        by_crop[r.get("crop", "?")] = by_crop.get(r.get("crop", "?"), 0) + 1
    for crop, count in sorted(by_crop.items()):
        print(f"  {crop}: {count} facts")
    if args.do_print:
        for r in valid:
            print(f"  [{r['crop']}/{r['problem']}/{r['stage']}] {r['active_ingredient']} {r['dose_min']}-{r['dose_max']} {r['dose_unit']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
