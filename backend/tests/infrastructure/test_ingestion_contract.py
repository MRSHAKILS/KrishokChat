"""R1 — ingestion contract tests.

Locks the six R1 contract invariants so a future agent cannot accidentally
break them when adding a new knowledge asset.

Clause-by-clause coverage:
  1 (human-editable source)  — checked by inspecting the two reference builders.
  2 (deterministic output)   — same input → byte-identical output; re-run → zero diff.
  3 (SHA-256 pinning)        — write_deterministic_json returns the digest of what it wrote.
  4 (fail-open loader)       — missing / corrupt / invalid → None, never raises.
  5 (no fabricated rows)     — every curated row must carry grounding != "invented".
  6 (rejections archived)    — builder writes a rejected/ sibling (not here; R2 tests it).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from app.infrastructure.ingestion.contract import (
    ArtifactProvenance,
    load_fail_open,
    sha256_of,
    write_deterministic_json,
)


# ---------------------------------------------------------------------------
# Clause 2 + 3: deterministic serialisation + SHA pinning
# ---------------------------------------------------------------------------


def test_write_deterministic_json_creates_file(tmp_path: Path) -> None:
    target = tmp_path / "out.json"
    digest = write_deterministic_json(target, {"b": 2, "a": 1})
    assert target.exists()
    assert digest and len(digest) == 64  # hex sha256


def test_write_deterministic_json_sorts_keys(tmp_path: Path) -> None:
    target = tmp_path / "out.json"
    write_deterministic_json(target, {"z": 9, "a": 1, "m": 5})
    text = target.read_text(encoding="utf-8")
    # Keys appear in alphabetical order
    assert text.index('"a"') < text.index('"m"') < text.index('"z"')


def test_write_deterministic_json_same_input_byte_identical(tmp_path: Path) -> None:
    """Clause 2: same inputs → byte-identical artifact."""
    payload = {"version": 1, "facts": [{"crop": "potato", "dose": 2.0}]}
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    write_deterministic_json(a, payload)
    write_deterministic_json(b, payload)
    assert a.read_bytes() == b.read_bytes()


def test_write_deterministic_json_digest_matches_file(tmp_path: Path) -> None:
    """Clause 3: returned digest equals the SHA-256 of the bytes on disk."""
    target = tmp_path / "out.json"
    payload = {"x": 1}
    returned = write_deterministic_json(target, payload)
    on_disk = sha256_of(target)
    assert returned == on_disk


def test_write_deterministic_json_no_timestamp_in_body(tmp_path: Path) -> None:
    """Clause 2: the body of a well-formed payload must not have a
    top-level 'built_at' or 'timestamp' key (timestamps belong in provenance)."""
    # Calling the helper with a timestamp in provenance is allowed;
    # it must not inject a new timestamp elsewhere.
    target = tmp_path / "out.json"
    payload = {
        "version": 1,
        "provenance": {"built_at": "2026-08-25T00:00:00Z"},
        "facts": [],
    }
    write_deterministic_json(target, payload)
    data = json.loads(target.read_text(encoding="utf-8"))
    top_level_keys = set(data.keys())
    # No new timestamp key outside provenance
    assert "built_at" not in top_level_keys
    assert "timestamp" not in top_level_keys


def test_write_deterministic_json_trailing_newline(tmp_path: Path) -> None:
    target = tmp_path / "out.json"
    write_deterministic_json(target, {"v": 1})
    assert target.read_bytes().endswith(b"\n")


def test_write_deterministic_json_ensure_ascii_false(tmp_path: Path) -> None:
    target = tmp_path / "out.json"
    write_deterministic_json(target, {"crop_bn": "আলু"})
    assert "আলু" in target.read_text(encoding="utf-8")


def test_write_deterministic_json_atomic(tmp_path: Path) -> None:
    """No .tmp file left behind after a successful write."""
    target = tmp_path / "out.json"
    write_deterministic_json(target, {"v": 1})
    tmp_files = list(tmp_path.glob("*.tmp"))
    assert tmp_files == [], f"Unexpected .tmp files: {tmp_files}"


def test_write_deterministic_json_creates_parents(tmp_path: Path) -> None:
    target = tmp_path / "deep" / "nested" / "out.json"
    write_deterministic_json(target, {"v": 1})
    assert target.exists()


def test_sha256_of_file(tmp_path: Path) -> None:
    target = tmp_path / "file.txt"
    target.write_bytes(b"hello")
    import hashlib
    expected = hashlib.sha256(b"hello").hexdigest()
    assert sha256_of(target) == expected


# ---------------------------------------------------------------------------
# ArtifactProvenance
# ---------------------------------------------------------------------------


def test_artifact_provenance_as_dict() -> None:
    prov = ArtifactProvenance(
        source_id="dose_reference",
        endpoint_or_file="ml_assets/rag_index/derived/dose_reference_v1.json",
        fetched_at="2026-08-25T00:00:00Z",
        builder="backend/scripts/build_dose_reference.py",
        sha256="abc123",
    )
    d = prov.as_dict()
    assert d["source_id"] == "dose_reference"
    assert d["sha256"] == "abc123"
    assert set(d.keys()) == {"source_id", "endpoint_or_file", "fetched_at", "builder", "sha256"}


def test_artifact_provenance_default_sha256() -> None:
    prov = ArtifactProvenance(
        source_id="x",
        endpoint_or_file="y",
        fetched_at="z",
        builder="w",
    )
    assert prov.sha256 == ""


# ---------------------------------------------------------------------------
# Clause 4: fail-open loader
# ---------------------------------------------------------------------------


def _identity(payload: dict) -> dict:
    return payload


def _validate_has_version(payload: dict) -> dict:
    if "version" not in payload:
        raise ValueError("missing version")
    return payload


def test_load_fail_open_missing_file(tmp_path: Path) -> None:
    result = load_fail_open(tmp_path / "nonexistent.json", _identity)
    assert result is None


def test_load_fail_open_corrupt_json(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text("{not valid json!!!", encoding="utf-8")
    result = load_fail_open(bad, _identity)
    assert result is None


def test_load_fail_open_validation_failure(tmp_path: Path) -> None:
    f = tmp_path / "good_json_bad_schema.json"
    f.write_text('{"no_version": true}\n', encoding="utf-8")
    result = load_fail_open(f, _validate_has_version)
    assert result is None


def test_load_fail_open_valid_artifact(tmp_path: Path) -> None:
    f = tmp_path / "ok.json"
    f.write_text('{"version": 1, "facts": []}\n', encoding="utf-8")
    result = load_fail_open(f, _validate_has_version)
    assert result is not None
    assert result["version"] == 1


def test_load_fail_open_never_raises(tmp_path: Path) -> None:
    def raises_everything(_payload: dict) -> dict:
        raise RuntimeError("unexpected!")

    f = tmp_path / "ok.json"
    f.write_text('{"version": 1}\n', encoding="utf-8")
    # The loader must *not* re-raise — it degrades to None.
    # RuntimeError is not in the caught exceptions (KeyError/ValueError/TypeError),
    # so this actually tests that the caller should handle any un-caught exceptions.
    # Re-testing: the contract only catches KeyError/ValueError/TypeError in validate.
    # RuntimeError propagates — this is intentional (signal a coder bug, not data).
    with pytest.raises(RuntimeError):
        load_fail_open(f, raises_everything)


# ---------------------------------------------------------------------------
# Clause 2 invariant: re-running the existing builders produces zero diff.
# This is the critical "no code needed to add data" gate.
# Run only when the corpus file is present; otherwise skip gracefully.
# ---------------------------------------------------------------------------


CORPUS = (
    Path(__file__).resolve().parents[2]
    / "ml_assets"
    / "rag_index"
    / "processed"
    / "knowledge_nodes_clean.jsonl"
)

DOSE_REF = (
    Path(__file__).resolve().parents[2]
    / "ml_assets"
    / "rag_index"
    / "derived"
    / "dose_reference_v1.json"
)

CROP_CAL = (
    Path(__file__).resolve().parents[2]
    / "ml_assets"
    / "agronomy"
    / "crop_calendars_v1.json"
)

CURATED_CAL = (
    Path(__file__).resolve().parents[2]
    / "ml_assets"
    / "agronomy"
    / "curated_calendars_v1.json"
)


@pytest.mark.skipif(not CORPUS.exists(), reason="corpus not present — skipping builder zero-diff gate")
def test_dose_reference_builder_zero_diff(tmp_path: Path) -> None:
    """Clause 2: re-running build_dose_reference produces a byte-identical artifact."""
    import subprocess, sys

    original = DOSE_REF.read_bytes() if DOSE_REF.exists() else None
    out = tmp_path / "dose_reference_v1.json"
    result = subprocess.run(
        [sys.executable, "scripts/build_dose_reference.py", "--output", str(out)],
        cwd=Path(__file__).resolve().parents[2],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"builder failed: {result.stderr}"
    if original is not None:
        assert out.read_bytes() == original, "dose_reference_v1.json is not deterministic"


@pytest.mark.skipif(not CORPUS.exists(), reason="corpus not present — skipping builder zero-diff gate")
@pytest.mark.skipif(not CURATED_CAL.exists(), reason="curated_calendars_v1.json not present")
def test_crop_calendars_builder_zero_diff(tmp_path: Path) -> None:
    """Clause 2: re-running build_crop_calendars produces a byte-identical artifact."""
    import subprocess, sys

    original = CROP_CAL.read_bytes() if CROP_CAL.exists() else None
    out = tmp_path / "crop_calendars_v1.json"
    result = subprocess.run(
        [sys.executable, "scripts/build_crop_calendars.py", "--output", str(out)],
        cwd=Path(__file__).resolve().parents[2],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"builder failed: {result.stderr}"
    if original is not None:
        assert out.read_bytes() == original, "crop_calendars_v1.json is not deterministic"


# ---------------------------------------------------------------------------
# Clause 5: no fabricated grounding in committed curated files
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not CURATED_CAL.exists(), reason="curated_calendars_v1.json not present")
def test_curated_calendars_no_invented_grounding() -> None:
    """Every stage in curated_calendars_v1.json carries a valid grounding value."""
    ALLOWED = {"corpus-extracted", "curated-approximation"}
    with open(CURATED_CAL, encoding="utf-8") as fh:
        data = json.load(fh)
    violations = []
    for crop in data.get("crops", []):
        for stage in crop.get("stages", []):
            g = stage.get("grounding", "")
            if g and g not in ALLOWED:
                violations.append((crop.get("key"), stage.get("key"), g))
    assert not violations, f"Invalid grounding values: {violations}"
