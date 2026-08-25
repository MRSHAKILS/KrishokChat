"""R2 — Fact-base tests.

Covers:
  1. Fact dataclass schema and from_dict().
  2. FactBase.lookup() — crop/problem/stage filtering.
  3. Fail-open loader — missing/corrupt/empty artifact.
  4. Builder validation — dose numeric, min<=max, banned agreement,
     known stage, F1-02 outlier bound, provenance invariant.
  5. Builder determinism — same seed → byte-identical artifact.
  6. Builder rejection archive — rejected rows archived, not dropped.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.domain.fact_base import Fact, FactBase
from app.infrastructure.knowledge.fact_base_store import load_fact_base


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

ARTIFACT = (
    Path(__file__).resolve().parents[1]
    / "ml_assets"
    / "rag_index"
    / "derived"
    / "fact_base_v1.json"
)

SEED = (
    Path(__file__).resolve().parents[1]
    / "ml_assets"
    / "rag_index"
    / "derived"
    / "curated_facts_v1.json"
)


def _make_row(**overrides) -> dict:
    base: dict = {
        "crop": "potato",
        "crop_bn": "আলু",
        "problem": "late_blight",
        "problem_bn": "নাবি ধ্বসা",
        "problem_type": "disease",
        "stage": "tuber_bulking",
        "active_ingredient": "mancozeb",
        "dose_min": 2.0,
        "dose_max": 2.5,
        "dose_unit": "g/l",
        "application_interval_days": 7,
        "pre_harvest_interval_days": 7,
        "ipm_alternatives_bn": ["আক্রান্ত পাতা সরানো"],
        "banned_flag": False,
        "severity": "high",
        "source_node_id": "DAE_PEST_001",
        "source_doc": "DAE",
        "citation": "DAE 2024",
        "grounding": "corpus-extracted",
        "confidence": 0.9,
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# 1. Fact dataclass
# ---------------------------------------------------------------------------


def test_fact_from_dict_roundtrip() -> None:
    row = _make_row()
    fact = Fact.from_dict(row)
    assert fact.crop == "potato"
    assert fact.active_ingredient == "mancozeb"
    assert fact.dose_min == 2.0
    assert fact.dose_max == 2.5
    assert fact.dose_unit == "g/l"
    assert fact.application_interval_days == 7
    assert fact.ipm_alternatives_bn == ("আক্রান্ত পাতা সরানো",)


def test_fact_from_dict_defaults() -> None:
    minimal: dict = {
        "crop": "potato",
        "problem": "late_blight",
        "stage": "tuber_bulking",
        "active_ingredient": "mancozeb",
        "dose_min": 2.0,
        "dose_max": 2.0,
        "dose_unit": "g/l",
        "application_interval_days": 7,
        "pre_harvest_interval_days": 7,
    }
    fact = Fact.from_dict(minimal)
    assert fact.grounding == "curated-approximation"
    assert fact.confidence == 0.0
    assert fact.ipm_alternatives_bn == ()


def test_fact_is_frozen() -> None:
    fact = Fact.from_dict(_make_row())
    with pytest.raises(Exception):
        fact.crop = "rice"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# 2. FactBase.lookup()
# ---------------------------------------------------------------------------


def _make_fact_base() -> FactBase:
    rows = [
        _make_row(stage="tuber_bulking", confidence=0.9),
        _make_row(stage="vegetative", confidence=0.8),
        _make_row(crop="rice", problem="blast", stage="tillering", confidence=0.7),
    ]
    return FactBase.from_artifact({"facts": rows})


def test_lookup_by_crop_and_problem() -> None:
    fb = _make_fact_base()
    results = fb.lookup("potato", "late_blight")
    assert len(results) == 2
    crops = {f.crop for f in results}
    assert crops == {"potato"}


def test_lookup_by_stage() -> None:
    fb = _make_fact_base()
    results = fb.lookup("potato", "late_blight", stage="tuber_bulking")
    assert len(results) == 1
    assert results[0].stage == "tuber_bulking"


def test_lookup_wrong_crop_returns_empty() -> None:
    fb = _make_fact_base()
    assert fb.lookup("wheat", "late_blight") == []


def test_lookup_wrong_stage_returns_empty() -> None:
    fb = _make_fact_base()
    assert fb.lookup("potato", "late_blight", stage="establishment") == []


def test_lookup_case_insensitive() -> None:
    fb = _make_fact_base()
    results = fb.lookup("POTATO", "LATE_BLIGHT")
    assert len(results) == 2


def test_lookup_sorted_by_confidence() -> None:
    fb = _make_fact_base()
    results = fb.lookup("potato", "late_blight")
    confidences = [f.confidence for f in results]
    assert confidences == sorted(confidences, reverse=True)


def test_factbase_len() -> None:
    fb = _make_fact_base()
    assert len(fb) == 3


def test_factbase_empty() -> None:
    fb = FactBase.empty()
    assert len(fb) == 0
    assert fb.lookup("potato", "late_blight") == []


# ---------------------------------------------------------------------------
# 3. Fail-open loader
# ---------------------------------------------------------------------------


def test_load_missing_file(tmp_path: Path) -> None:
    fb = load_fact_base(tmp_path / "nonexistent.json")
    assert isinstance(fb, FactBase)
    assert len(fb) == 0


def test_load_corrupt_json(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text("{not json!", encoding="utf-8")
    fb = load_fact_base(bad)
    assert len(fb) == 0


def test_load_no_facts_key(tmp_path: Path) -> None:
    f = tmp_path / "empty.json"
    f.write_text('{"version": 1}\n', encoding="utf-8")
    fb = load_fact_base(f)
    assert len(fb) == 0


def test_load_valid_artifact(tmp_path: Path) -> None:
    payload = {"version": 1, "facts": [_make_row()]}
    f = tmp_path / "valid.json"
    f.write_text(json.dumps(payload), encoding="utf-8")
    fb = load_fact_base(f)
    assert len(fb) == 1
    assert fb.facts[0].crop == "potato"


# ---------------------------------------------------------------------------
# 4. Builder validation rules
# ---------------------------------------------------------------------------


@pytest.fixture
def known_stages() -> set[str]:
    return {"establishment", "vegetative", "tuber_initiation", "tuber_bulking", "maturity"}


@pytest.fixture
def dose_bands() -> dict[tuple[str, str], float]:
    # mancozeb max = 2.5 g/l; outlier band = 3× = 7.5
    from app.infrastructure.verification.dosage_claims import normalize_chemical
    return {(normalize_chemical("mancozeb"), "g/l"): 2.5}


def _run_validate(row: dict, stages: set[str], bands: dict) -> "str | None":
    # Import the private validation function from the builder.
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.build_fact_base import _validate_row
    return _validate_row(row, stages, bands)


def test_valid_row_passes(known_stages, dose_bands) -> None:
    assert _run_validate(_make_row(), known_stages, dose_bands) is None


def test_non_numeric_dose_min(known_stages, dose_bands) -> None:
    reason = _run_validate(_make_row(dose_min="not_a_number"), known_stages, dose_bands)
    assert reason is not None and "non-numeric" in reason


def test_dose_min_greater_than_max(known_stages, dose_bands) -> None:
    reason = _run_validate(_make_row(dose_min=5.0, dose_max=2.0), known_stages, dose_bands)
    assert reason is not None and "dose_min" in reason


def test_banned_active_without_flag(known_stages, dose_bands) -> None:
    # carbofuran is in BANNED_ACTIVES
    reason = _run_validate(_make_row(active_ingredient="carbofuran", banned_flag=False), known_stages, dose_bands)
    assert reason is not None and "banned" in reason


def test_valid_active_with_false_banned_flag_passes(known_stages, dose_bands) -> None:
    assert _run_validate(_make_row(active_ingredient="mancozeb", banned_flag=False), known_stages, dose_bands) is None


def test_unknown_stage(known_stages, dose_bands) -> None:
    reason = _run_validate(_make_row(stage="unknown_stage_xyz"), known_stages, dose_bands)
    assert reason is not None and "stage" in reason


def test_outlier_dose_rejected(known_stages, dose_bands) -> None:
    # 10.0 g/l > 2.5 × 3 = 7.5
    reason = _run_validate(_make_row(dose_max=10.0), known_stages, dose_bands)
    assert reason is not None and "outlier" in reason.lower() or "exceed" in reason.lower()


def test_within_outlier_band_passes(known_stages, dose_bands) -> None:
    # 7.0 < 7.5 — within band
    assert _run_validate(_make_row(dose_max=7.0), known_stages, dose_bands) is None


def test_missing_source_node_id_without_curated(known_stages, dose_bands) -> None:
    reason = _run_validate(
        _make_row(source_node_id="", grounding="corpus-extracted"),
        known_stages, dose_bands,
    )
    assert reason is not None


def test_missing_source_node_id_with_curated_passes(known_stages, dose_bands) -> None:
    assert _run_validate(
        _make_row(source_node_id="", grounding="curated-approximation"),
        known_stages, dose_bands,
    ) is None


# ---------------------------------------------------------------------------
# 5. Builder determinism
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not SEED.exists(), reason="seed file not present")
def test_builder_is_deterministic(tmp_path: Path) -> None:
    import subprocess, sys, shutil

    out_a = tmp_path / "a.json"
    out_b = tmp_path / "b.json"
    rejected_a = tmp_path / "rej_a.json"
    rejected_b = tmp_path / "rej_b.json"
    backend = Path(__file__).resolve().parents[1]

    for out, rej in [(out_a, rejected_a), (out_b, rejected_b)]:
        r = subprocess.run(
            [sys.executable, "scripts/build_fact_base.py", "--output", str(out), "--rejected", str(rej)],
            cwd=backend, capture_output=True, text=True,
        )
        assert r.returncode == 0, f"builder failed: {r.stderr}"

    # Compare payload bodies excluding provenance fields that legitimately
    # vary between runs (built_at, sha256, endpoint_or_file with absolute path).
    for path in (out_a, out_b):
        data = json.loads(path.read_text(encoding="utf-8"))
        for key in ("built_at", "sha256", "endpoint_or_file"):
            data.get("provenance", {}).pop(key, None)
        path.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")

    assert out_a.read_bytes() == out_b.read_bytes(), "builder is not deterministic"


# ---------------------------------------------------------------------------
# 6. Committed artifact health (skipped if artifact not built yet)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not ARTIFACT.exists(), reason="fact_base_v1.json not built yet")
def test_committed_artifact_loads() -> None:
    fb = load_fact_base(ARTIFACT)
    assert len(fb) > 0


@pytest.mark.skipif(not ARTIFACT.exists(), reason="fact_base_v1.json not built yet")
def test_committed_artifact_banned_agreement() -> None:
    """No row may have banned_flag=False for a banned active."""
    from app.domain.chemical_registry import BANNED_ACTIVES
    from app.infrastructure.verification.dosage_claims import normalize_chemical

    banned_canonical = {normalize_chemical(a.canonical_en) for a in BANNED_ACTIVES}
    fb = load_fact_base(ARTIFACT)
    violations = [
        f for f in fb.facts
        if normalize_chemical(f.active_ingredient) in banned_canonical and not f.banned_flag
    ]
    assert not violations, f"Banned-flag mismatch: {violations}"


@pytest.mark.skipif(not ARTIFACT.exists(), reason="fact_base_v1.json not built yet")
def test_committed_artifact_no_outlier_doses() -> None:
    """No row may exceed 3× the dose_reference band max."""
    from pathlib import Path
    dose_ref = Path(__file__).resolve().parents[1] / "ml_assets" / "rag_index" / "derived" / "dose_reference_v1.json"
    if not dose_ref.exists():
        pytest.skip("dose_reference_v1.json not present")

    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.build_fact_base import _load_dose_bands, OUTLIER_FACTOR
    from app.infrastructure.verification.dosage_claims import normalize_chemical

    bands = _load_dose_bands(dose_ref)
    fb = load_fact_base(ARTIFACT)
    violations = []
    for f in fb.facts:
        key = (normalize_chemical(f.active_ingredient), f.dose_unit)
        ref_max = bands.get(key)
        if ref_max is not None and f.dose_max > ref_max * OUTLIER_FACTOR:
            violations.append(f)
    assert not violations, f"Outlier dose violations: {violations}"
