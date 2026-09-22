"""P0-4: bootstrap startup-check tests.

run_bootstrap_checks is advisory: it must never raise, must never block app
startup, and must surface actionable warnings (provider key absent in live
mode, missing asset folders) while staying silent on healthy configs.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from app.core.bootstrap_checks import run_bootstrap_checks
from app.core.config import Settings


class BootstrapChecksTests(unittest.TestCase):
    def test_healthy_defaults_produce_no_warnings(self) -> None:
        warnings = run_bootstrap_checks(Settings())
        self.assertEqual(warnings, [])

    def test_missing_provider_key_warns_only_outside_demo_mode(self) -> None:
        config = Settings(demo_mode=False, openrouter_api_key=None, gemini_api_key=None)
        warnings = run_bootstrap_checks(config)
        self.assertTrue(
            any("no LLM provider key" in w for w in warnings),
            f"expected provider-key warning, got {warnings}",
        )

    def test_demo_mode_without_key_stays_silent(self) -> None:
        config = Settings(demo_mode=True, openrouter_api_key=None, gemini_api_key=None)
        warnings = run_bootstrap_checks(config)
        self.assertEqual(warnings, [])

    def test_missing_asset_folders_warn(self) -> None:
        tmp = tempfile.mkdtemp()
        config = Settings(
            ml_assets_dir=str(Path(tmp) / "no-ml-assets"),
            soil_release_dir=str(Path(tmp) / "no-soil-release"),
        )
        warnings = run_bootstrap_checks(config)
        self.assertTrue(any("ml_assets_dir missing" in w for w in warnings))
        self.assertTrue(any("soil release folder missing" in w for w in warnings))

    def test_never_raises_on_odd_inputs(self) -> None:
        """Advisory by design: odd settings produce warnings, not exceptions."""
        config = Settings(
            ml_assets_dir="",  # empty path is invalid-ish but must not crash
            readiness_strict=True,
            environment="production",
        )
        try:
            warnings = run_bootstrap_checks(config)
        except Exception as exc:  # noqa: BLE001 - this test exists to catch this
            self.fail(f"run_bootstrap_checks raised: {exc}")
        self.assertIsInstance(warnings, list)


if __name__ == "__main__":
    unittest.main()