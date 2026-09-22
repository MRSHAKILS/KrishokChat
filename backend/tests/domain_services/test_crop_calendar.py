"""P2 tests: data-driven crop-stage calculator, fail-open loader, extensibility.

Locks:
- deterministic stage computation given (artifact, crop, sowing, today):
  boundary handling, past-final clamp, alias resolution, pre-sowing None;
- the loader's fail-open contract (missing/broken/empty file -> None);
- the extensibility contract: a dummy crop added to a COPY of the curated
  file is picked up by both the builder and the calculator with NO code
  changes (adding a crop = data edit + rebuild only);
- the committed artifact loads and exposes the seeded crops.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from app.domain.crop_calendar import CropCalendarLibrary
from app.infrastructure.agronomy.calendar_store import load_crop_calendars

PROJECT_ROOT = Path(__file__).resolve().parents[2]
COMMITTED_ARTIFACT = PROJECT_ROOT / "ml_assets" / "agronomy" / "crop_calendars_v1.json"
CURATED_SEED = PROJECT_ROOT / "ml_assets" / "agronomy" / "curated_calendars_v1.json"


def _artifact(crops: list[dict]) -> dict:
    return {"version": 1, "crops": crops}


_POTATO = {
    "key": "potato",
    "name_bn": "আলু",
    "aliases_bn": ["আলু"],
    "aliases_en": ["potato"],
    "season_note_bn": "নভেম্বর–মার্চ",
    "stages": [
        {"key": "establishment", "name_bn": "চারা", "start_das": 0, "end_das": 20,
         "advisory_bn": "আর্দ্রতা", "source": "curated", "grounding": "curated-approximation"},
        {"key": "bulking", "name_bn": "কন্দ স্ফীতি", "start_das": 20, "end_das": 75,
         "advisory_bn": "সেচ", "source": "curated", "grounding": "curated-approximation"},
        {"key": "maturity", "name_bn": "সংগ্রহ", "start_das": 75, "end_das": 90,
         "advisory_bn": "সংগ্রহ করুন", "source": "BARC", "grounding": "corpus-extracted"},
    ],
}


class CalculatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.lib = CropCalendarLibrary(_artifact([_POTATO]))

    def test_stage_at_start_boundary_is_that_stage(self) -> None:
        # das == start_das falls in the stage; das == end_das rolls to next.
        r = self.lib.compute_stage("potato", "2026-01-01", "2026-01-01")
        self.assertIsNotNone(r)
        self.assertEqual(r.stage_key, "establishment")
        self.assertEqual(r.das, 0)

    def test_mid_window_stage(self) -> None:
        sowing = date(2026, 1, 1)
        today = sowing + timedelta(days=40)
        r = self.lib.compute_stage("potato", sowing, today)
        self.assertEqual(r.stage_key, "bulking")
        self.assertEqual(r.das, 40)
        self.assertTrue(r.is_approximate)  # curated-approximation

    def test_end_boundary_rolls_to_next_stage(self) -> None:
        sowing = date(2026, 1, 1)
        r = self.lib.compute_stage("potato", sowing, sowing + timedelta(days=20))
        self.assertEqual(r.stage_key, "bulking")

    def test_past_final_window_clamps_to_final_stage(self) -> None:
        sowing = date(2026, 1, 1)
        r = self.lib.compute_stage("potato", sowing, sowing + timedelta(days=200))
        self.assertEqual(r.stage_key, "maturity")
        self.assertFalse(r.is_approximate)  # corpus-extracted final

    def test_pre_sowing_returns_none(self) -> None:
        r = self.lib.compute_stage("potato", "2026-01-10", "2026-01-01")
        self.assertIsNone(r)

    def test_alias_resolution_bn_and_en(self) -> None:
        self.assertEqual(self.lib.resolve_crop("আলু"), "potato")
        self.assertEqual(self.lib.resolve_crop("POTATO"), "potato")
        self.assertIsNone(self.lib.resolve_crop("wheat"))

    def test_unknown_crop_returns_none(self) -> None:
        self.assertIsNone(self.lib.compute_stage("wheat", "2026-01-01", "2026-03-01"))

    def test_farmer_context_line_shape(self) -> None:
        r = self.lib.compute_stage("potato", "2026-01-01", "2026-02-10")
        self.assertIn("ফসল: আলু", r.farmer_context_bn)
        self.assertIn("বর্তমান পর্যায়", r.farmer_context_bn)

    def test_supported_crops_sorted(self) -> None:
        lib = CropCalendarLibrary(_artifact([_POTATO, {**_POTATO, "key": "rice", "name_bn": "ধান"}]))
        keys = [c["key"] for c in lib.supported_crops]
        self.assertEqual(keys, ["potato", "rice"])


class LoaderFailOpenTests(unittest.TestCase):
    def test_missing_file_returns_none(self) -> None:
        self.assertIsNone(load_crop_calendars(Path(tempfile.mkdtemp()) / "nope.json"))

    def test_broken_json_returns_none(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh:
            fh.write("{not json")
        self.assertIsNone(load_crop_calendars(fh.name))

    def test_empty_crops_returns_none(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh:
            json.dump({"version": 1, "crops": []}, fh)
        self.assertIsNone(load_crop_calendars(fh.name))

    def test_committed_artifact_loads_with_potato(self) -> None:
        lib = load_crop_calendars(COMMITTED_ARTIFACT)
        self.assertIsNotNone(lib)
        self.assertIsNotNone(lib.resolve_crop("potato"))
        r = lib.compute_stage("potato", "2026-01-01", "2026-02-25")
        self.assertIsNotNone(r)
        self.assertEqual(r.crop_key, "potato")


class ExtensibilityTests(unittest.TestCase):
    """Adding a crop = edit curated JSON + rebuild; NO code changes."""

    def test_dummy_crop_flows_through_builder_and_calculator(self) -> None:
        # Build a curated COPY with an extra dummy crop, run the real builder
        # against an empty corpus, and confirm the artifact + calculator both
        # pick it up without any Python change.
        from scripts.build_crop_calendars import build, extract_harvest_windows

        with open(CURATED_SEED, encoding="utf-8") as fh:
            curated = json.load(fh)
        dummy = {
            "key": "mango", "name_bn": "আম", "aliases_bn": ["আম"], "aliases_en": ["mango"],
            "season_note_bn": "গ্রীষ্ম", "sowing_term_bn": "রোপণ",
            "stages": [
                {"key": "veg", "name_bn": "বৃদ্ধি", "start_das": 0, "end_das": 60,
                 "advisory_bn": "পরিচর্যা", "source": "curated", "grounding": "curated-approximation"},
                {"key": "harvest", "name_bn": "সংগ্রহ", "start_das": 60, "end_das": 120,
                 "advisory_bn": "সংগ্রহ", "source": "curated", "grounding": "curated-approximation"},
            ],
        }
        curated["crops"].append(dummy)

        # Empty corpus file -> no windows; builder still merges curated crops.
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as corpus_fh:
            corpus_fh.write("")
        aliases = {c["key"]: list(c.get("aliases_bn") or []) + list(c.get("aliases_en") or []) for c in curated["crops"]}
        windows = extract_harvest_windows(Path(corpus_fh.name), aliases)
        artifact = build(curated, windows)

        keys = [c["key"] for c in artifact["crops"]]
        self.assertIn("mango", keys)

        lib = CropCalendarLibrary(artifact)
        r = lib.compute_stage("mango", "2026-01-01", "2026-02-20")  # das=50 -> veg
        self.assertIsNotNone(r)
        self.assertEqual(r.crop_key, "mango")
        self.assertEqual(r.stage_key, "veg")


if __name__ == "__main__":
    unittest.main()
