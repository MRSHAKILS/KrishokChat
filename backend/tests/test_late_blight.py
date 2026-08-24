"""PR1 tests: potato late-blight weather-risk rule, snapshot loader, admin route.

Locks:
- the rule's tiering (high/watch/low) on trailing consecutive favourable days,
  with unordered input, seasonality boundaries, and the no-dose advisory draft;
- the loader's fail-open contract (missing/broken file -> None; malformed rows
  skipped; sample flag preserved) against both synthetic and committed files;
- the admin route's fail-closed authz (401 anonymous) and payload shape
  (available/sample/risk-ordered districts with composer prefills; a missing
  snapshot yields ``available: false``, never a 500).
"""

from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from fastapi.testclient import TestClient

from app.application.admin import AdminService
from app.application.auth import AuthService
from app.core.config import Settings
from app.domain.late_blight import DailyWeather, draft_advisory, evaluate_district
from app.infrastructure.auth.jwks import SupabaseJWKSVerifier
from app.infrastructure.weather.snapshot import load_weather_snapshot
from app.main import create_app

PROJECT_ROOT = Path(__file__).resolve().parents[1]
COMMITTED_SNAPSHOT = PROJECT_ROOT / "ml_assets" / "weather" / "late_blight_snapshot.json"


def _days(*specs: tuple[str, float, float]) -> list[DailyWeather]:
    return [DailyWeather(date=d, tmin_c=t, rh_pct=h) for d, t, h in specs]


class RuleTests(unittest.TestCase):
    def test_two_trailing_favourable_days_is_high(self) -> None:
        days = _days(
            ("2026-01-13", 8.0, 70.0),
            ("2026-01-14", 11.0, 88.0),
            ("2026-01-15", 12.0, 90.0),
        )
        result = evaluate_district("X", days)
        self.assertEqual(result.risk, "high")
        self.assertEqual(result.favourable_days, 2)

    def test_single_favourable_day_is_watch(self) -> None:
        days = _days(
            ("2026-01-14", 9.0, 80.0),
            ("2026-01-15", 11.0, 88.0),
        )
        self.assertEqual(evaluate_district("X", days).risk, "watch")

    def test_none_favourable_is_low(self) -> None:
        days = _days(("2026-01-14", 9.0, 80.0), ("2026-01-15", 9.5, 84.0))
        self.assertEqual(evaluate_district("X", days).risk, "low")

    def test_favourable_run_broken_by_cold_day_is_low(self) -> None:
        # Early-month favourable days do not count: only the run ending at the
        # LATEST date matters.
        days = _days(
            ("2026-01-13", 12.0, 92.0),
            ("2026-01-14", 12.0, 92.0),
            ("2026-01-15", 8.0, 70.0),
        )
        self.assertEqual(evaluate_district("X", days).risk, "low")

    def test_rows_are_sorted_by_date(self) -> None:
        days = _days(
            ("2026-01-15", 11.0, 88.0),
            ("2026-01-14", 11.5, 90.0),
            ("2026-01-13", 9.0, 80.0),
        )
        result = evaluate_district("X", days)
        self.assertEqual(result.risk, "high")
        self.assertEqual(result.latest_date, "2026-01-15")

    def test_empty_district_is_none(self) -> None:
        self.assertIsNone(evaluate_district("X", []))

    def test_thresholds_are_inclusive(self) -> None:
        days = _days(
            ("2026-01-14", 10.0, 85.0),
            ("2026-01-15", 10.0, 85.0),
        )
        self.assertEqual(evaluate_district("X", days).risk, "high")

    def test_seasonality_boundaries(self) -> None:
        from app.domain.late_blight import _in_season

        self.assertTrue(_in_season("2026-01-16"))
        self.assertTrue(_in_season("2026-11-01"))
        self.assertTrue(_in_season("2026-03-15"))
        self.assertFalse(_in_season("2026-03-16"))
        self.assertFalse(_in_season("2026-10-31"))
        self.assertFalse(_in_season("2026-07-15"))
        self.assertFalse(_in_season("not-a-date"))


class DraftTests(unittest.TestCase):
    def _risk(self, risk: str):
        return evaluate_district("Bogura", _days(("2026-01-14", 11.0, 88.0), ("2026-01-15", 12.0, 90.0))) if risk == "high" else None

    def test_draft_contents(self) -> None:
        result = self._risk("high")
        draft = draft_advisory(result, sample=True)
        self.assertEqual(draft["kind"], "disease_alert")
        self.assertEqual(draft["severity"], "urgent")
        self.assertEqual(draft["crop"], "আলু")
        self.assertIn("Bogura", draft["title_bn"])
        self.assertIn("উচ্চ", draft["title_bn"])
        # Grounding + escalation present; no numeric dose may appear.
        self.assertIn("CABI", draft["body_bn"])
        self.assertIn("১৬১২৩", draft["body_bn"])
        self.assertIn("নমুনা", draft["body_bn"])

    def test_non_sample_draft_has_no_sample_marker(self) -> None:
        draft = draft_advisory(self._risk("high"), sample=False)
        self.assertNotIn("নমুনা", draft["body_bn"])

    def test_watch_maps_to_warning(self) -> None:
        result = evaluate_district("Y", _days(("2026-01-14", 9.0, 80.0), ("2026-01-15", 11.0, 88.0)))
        self.assertEqual(draft_advisory(result)["severity"], "warning")


class LoaderTests(unittest.TestCase):
    def test_missing_file_returns_none(self) -> None:
        self.assertIsNone(load_weather_snapshot(Path(tempfile.mkdtemp()) / "absent.json"))

    def test_broken_json_returns_none(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh:
            fh.write("{oops")
        self.assertIsNone(load_weather_snapshot(fh.name))

    def test_malformed_rows_skipped_valid_kept(self) -> None:
        payload = {
            "is_sample": False,
            "source_note": "test",
            "districts": {
                "A": [
                    {"date": "2026-01-14", "tmin_c": 11.0, "rh_pct": 88.0},
                    {"date": "2026-01-15", "tmin_c": "bad", "rh_pct": 90.0},
                    {"date": "2026-01-16", "tmin_c": 12.0, "rh_pct": 91.0},
                ],
                "B": [],
                "C": "not-a-list",
            },
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh:
            json.dump(payload, fh)
        snap = load_weather_snapshot(fh.name)
        self.assertIsNotNone(snap)
        self.assertEqual(list(snap.districts), ["A"])
        self.assertEqual(len(snap.districts["A"]), 2)
        self.assertFalse(snap.is_sample)

    def test_committed_sample_snapshot_loads(self) -> None:
        snap = load_weather_snapshot(COMMITTED_SNAPSHOT)
        self.assertIsNotNone(snap)
        self.assertTrue(snap.is_sample, "shipped snapshot must be marked is_sample")
        self.assertGreaterEqual(len(snap.districts), 8)
        self.assertTrue(snap.source_note.strip())


class AdminRouteTests(unittest.TestCase):
    def setUp(self) -> None:
        key = ec.generate_private_key(ec.SECP256R1())
        numbers = key.public_key().public_numbers()
        import base64

        self.jwk = {
            "kty": "EC", "crv": "P-256",
            "x": base64.urlsafe_b64encode(numbers.x.to_bytes(32, "big")).rstrip(b"=").decode(),
            "y": base64.urlsafe_b64encode(numbers.y.to_bytes(32, "big")).rstrip(b"=").decode(),
            "kid": "k1", "alg": "ES256", "use": "sig",
        }
        self.pem = key.private_bytes(
            serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()
        )
        self.admin_token = jwt.encode(
            {"sub": "admin-1", "email": "a@example.com", "aud": "authenticated"},
            self.pem, algorithm="ES256", headers={"kid": "k1"},
        )

    @contextmanager
    def _client(self, config: Settings | None = None):
        verifier = SupabaseJWKSVerifier("http://unused.invalid/jwks")
        verifier._fetch_jwks = lambda: {"keys": [self.jwk]}  # type: ignore[method-assign]

        from tests.test_admin_authz import FakeAdminStore

        app = create_app(config=config) if config else create_app()
        with TestClient(app) as client:
            from dataclasses import replace

            client.app.state.container = replace(
                client.app.state.container,
                auth=AuthService(verifier=verifier),
                admin=AdminService(store=FakeAdminStore()),
            )
            yield client

    def test_anonymous_gets_401(self) -> None:
        with self._client() as client:
            response = client.get("/api/admin/advisory/late-blight-risk")
            self.assertEqual(response.status_code, 401)

    def test_admin_gets_risk_payload_from_committed_sample(self) -> None:
        with self._client() as client:
            response = client.get(
                "/api/admin/advisory/late-blight-risk",
                headers={"Authorization": f"Bearer {self.admin_token}"},
            )
            self.assertEqual(response.status_code, 200)
            body = response.json()
            self.assertTrue(body["available"])
            self.assertTrue(body["sample"])
            risks = [d["risk"] for d in body["districts"]]
            # Risk-ordered: high first, low last; all three tiers present in
            # the committed sample so the demo shows the full range.
            self.assertEqual(risks, sorted(risks, key=lambda r: {"high": 0, "watch": 1, "low": 2}[r]))
            self.assertIn("high", risks)
            self.assertIn("watch", risks)
            self.assertIn("low", risks)
            first = body["districts"][0]
            self.assertIn("title_bn", first["draft"])
            self.assertIn("body_bn", first["draft"])
            self.assertEqual(first["draft"]["kind"], "disease_alert")

    def test_missing_snapshot_is_available_false_not_500(self) -> None:
        config = Settings(
            _env_file=None,
            audit_log_path=str(Path(tempfile.mkdtemp()) / "audit.jsonl"),
            weather_snapshot_path=str(Path(tempfile.mkdtemp()) / "nope.json"),
        )
        with self._client(config=config) as client:
            response = client.get(
                "/api/admin/advisory/late-blight-risk",
                headers={"Authorization": f"Bearer {self.admin_token}"},
            )
            self.assertEqual(response.status_code, 200)
            body = response.json()
            self.assertFalse(body["available"])
            self.assertEqual(body["districts"], [])


if __name__ == "__main__":
    unittest.main()
