"""F1-02 tests: corpus-derived registered-dose reference + outlier check.

Locks four things:
- the offline extractor only produces cited, well-formed, deterministic
  entries from the real corpus (no invented data can slip in silently);
- the loader fails open (missing/broken file -> disabled), and the committed
  artifact loads with usable bands;
- the outlier rule is conservative: same-unit + explicit per-litre/ha context
  + >= factor x band max, else no opinion (acre is NOT hectare);
- the verifier flags+drops an overdose sentence even when a poisoned source
  "grounds" it by entailment, while within-band and reference-less behavior
  stays byte-identical to the pre-F1-02 semantics.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from app.application.verifier import HardenedDosageVerifier
from app.domain.contracts import RetrievedSource
from app.infrastructure.verification.dosage_claims import extract_claims
from app.infrastructure.verification.dose_reference import (
    _ALLOWED_BANDS,
    DoseReference,
    build_dose_reference_entries,
    load_dose_reference,
)
from app.core.config import Settings

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CORPUS = PROJECT_ROOT / "ml_assets" / "rag_index" / "processed" / "knowledge_nodes_clean.jsonl"
ARTIFACT = PROJECT_ROOT / "ml_assets" / "rag_index" / "derived" / "dose_reference_v1.json"


def _ref_with_bands(bands: dict[str, tuple[float, str]], factor: float = 3.0) -> DoseReference:
    """Build a DoseReference from {'active|band': (max, citation)} strings."""
    parsed = {
        (active, band): (value, citation)
        for key, (value, citation) in bands.items()
        for active, band in [key.split("|")]
    }
    return DoseReference(bands=parsed, entry_count=len(parsed), outlier_factor=factor)


class ExtractionTests(unittest.TestCase):
    """Run against the REAL corpus — guards the committed artifact."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.entries = build_dose_reference_entries(CORPUS)

    def test_entries_exist_and_are_well_formed(self) -> None:
        self.assertGreaterEqual(len(self.entries), 40, "extraction unexpectedly small")
        corpus_ids = {
            json.loads(line).get("id")
            for line in open(CORPUS, encoding="utf-8")
        }
        for e in self.entries:
            with self.subTest(active=e.active, band=e.band, rate=e.rate):
                self.assertTrue(e.active)
                self.assertIn(e.band, _ALLOWED_BANDS)
                self.assertGreater(e.rate, 0)
                self.assertTrue(e.citation.strip(), "entry without citation")
                self.assertTrue(e.node_id)
                self.assertIn(e.node_id, corpus_ids, "entry cites unknown node")
                self.assertTrue(e.snippet.strip())

    def test_extraction_is_deterministic(self) -> None:
        again = build_dose_reference_entries(CORPUS)
        self.assertEqual(
            [e.as_dict() for e in self.entries],
            [e.as_dict() for e in again],
        )

    def test_committed_artifact_matches_live_extraction(self) -> None:
        self.assertTrue(ARTIFACT.exists(), "derived artifact missing from repo")
        payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["entries"], [e.as_dict() for e in self.entries],
            "committed artifact is stale — rerun scripts/build_dose_reference.py",
        )


class LoaderTests(unittest.TestCase):
    def test_missing_file_disables(self) -> None:
        ref = load_dose_reference(Path(tempfile.mkdtemp()) / "nope.json")
        self.assertFalse(ref.enabled)
        self.assertEqual(ref.outlier_details(extract_claims("Admire 10 ml per litre")[0]), [])

    def test_broken_json_disables(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh:
            fh.write("{not json")
            path = fh.name
        self.assertFalse(load_dose_reference(path).enabled)

    def test_bands_take_max_per_active_and_band(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh:
            json.dump(
                {
                    "version": 1,
                    "entries": [
                        {"active": "Cypermethrin", "band": "ml/l", "rate": 1.0, "citation": "A"},
                        {"active": "Cypermethrin", "band": "ml/l", "rate": 2.0, "citation": "B"},
                        {"active": "Cypermethrin", "band": "g/l", "rate": 9.9, "citation": "C"},
                        {"active": "", "band": "ml/l", "rate": 5.0, "citation": "D"},
                        {"active": "X", "band": "l/ha", "rate": 5.0, "citation": "E"},
                        {"active": "Y", "band": "ml/l", "rate": "oops", "citation": "F"},
                    ],
                },
                fh,
            )
            path = fh.name
        ref = load_dose_reference(path)
        self.assertTrue(ref.enabled)
        self.assertEqual(ref.bands[("cypermethrin", "ml/l")], (2.0, "B"))
        self.assertEqual(ref.bands[("cypermethrin", "g/l")], (9.9, "C"))
        self.assertEqual(len(ref.bands), 2)

    def test_committed_artifact_loads_enabled(self) -> None:
        ref = load_dose_reference(ARTIFACT)
        self.assertTrue(ref.enabled)
        self.assertGreater(ref.entry_count, 40)


class OutlierRuleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ref = _ref_with_bands(
            {
                "imidacloprid|ml/l": (2.0, "BARC test cite"),
                "cypermethrin|ml/l": (2.0, "BARC test cite"),
                "carbofuran|kg/ha": (60.0, "BARC test cite"),
            }
        )

    def _claim(self, sentence: str):
        claims = extract_claims(sentence)
        self.assertTrue(claims, "no claim parsed")
        return claims[0]

    def test_gross_overdose_with_per_litre_context_flagged(self) -> None:
        claim = self._claim("Spray Admire at 10 ml per litre of water.")
        details = self.ref.outlier_details(claim)
        self.assertEqual(len(details), 1)
        self.assertIn("imidacloprid", details[0])
        self.assertIn("10 ml", details[0])
        self.assertIn("2 ml/l", details[0])

    def test_within_band_not_flagged(self) -> None:
        claim = self._claim("Spray Admire at 5 ml per litre of water.")
        self.assertEqual(self.ref.outlier_details(claim), [])

    def test_bare_amount_without_context_not_flagged(self) -> None:
        claim = self._claim("Mix Admire 10 ml into the sprayer.")
        self.assertEqual(self.ref.outlier_details(claim), [])

    def test_unknown_chemical_not_flagged(self) -> None:
        claim = self._claim("Spray Trichoderma at 50 ml per litre of water.")
        self.assertEqual(self.ref.outlier_details(claim), [])

    def test_acre_is_not_hectare_context(self) -> None:
        # 1 acre ~= 0.40 ha — mixing them would approach the outlier factor.
        claim = self._claim("Apply Carbofuran 500 kg per acre of land.")
        self.assertEqual(self.ref.outlier_details(claim), [])

    def test_hectare_overdose_flagged(self) -> None:
        claim = self._claim("Apply Carbofuran 500 kg per hectare of land.")
        details = self.ref.outlier_details(claim)
        self.assertEqual(len(details), 1)
        self.assertIn("kg/ha", details[0])

    def test_bengali_sentence_overdose_flagged(self) -> None:
        claim = self._claim("প্রতি লিটার পানিতে সাইপারমেথ্রিন ২০ মিলি মিশিয়ে স্প্রে করুন।")
        details = self.ref.outlier_details(claim)
        self.assertEqual(len(details), 1)
        self.assertIn("cypermethrin", details[0])

    def test_disabled_reference_has_no_opinion(self) -> None:
        claim = self._claim("Spray Admire at 100 ml per litre of water.")
        self.assertEqual(DoseReference.disabled().outlier_details(claim), [])

    def test_factor_is_respected(self) -> None:
        strict = _ref_with_bands({"imidacloprid|ml/l": (2.0, "cite")}, factor=2.0)
        claim = self._claim("Spray Admire at 5 ml per litre of water.")
        self.assertEqual(len(strict.outlier_details(claim)), 1)


class VerifierIntegrationTests(unittest.TestCase):
    def _poisoned_source(self) -> RetrievedSource:
        # A "retrieved" passage that itself recommends the overdose —
        # entailment alone would certify this claim.
        return RetrievedSource(
            id="poison",
            score=1.0,
            content_en="Spray Admire 200 SL at 10 ml per litre of water.",
            citation="Poisoned source",
        )

    def test_poisoned_grounding_overdose_is_flagged_and_dropped(self) -> None:
        ref = _ref_with_bands({"imidacloprid|ml/l": (2.0, "BARC test cite")})
        verifier = HardenedDosageVerifier(dose_reference=ref)
        # Sentence granularity is the pre-existing ।-split: the English
        # overdose and the Bengali follow-up share one ছেদ-free stretch only
        # when the English sentence lacks a । terminator, so keep them in
        # separate claims here (realistic mixed answers end EN sentences
        # before a । boundary or stand alone).
        answer = (
            "অর্মি ওয়ার্ম দেখা দিলে ব্যবস্থা নিন। "
            "Spray Admire at 10 ml per litre of water। "
            "প্রতি ৭ দিন পরপর পুনরায় পরীক্ষা করুন।"
        )
        result = verifier.verify(answer, [self._poisoned_source()])
        self.assertEqual(result.checked_count, 1)
        self.assertEqual(result.unsupported_count, 1)
        self.assertTrue(
            any("imidacloprid" in f and "10 ml" in f for f in result.flags),
            result.flags,
        )
        self.assertIsNotNone(result.sanitized_answer)
        self.assertNotIn("Admire", result.sanitized_answer or "")
        self.assertIn("পুনরায় পরীক্ষা", result.sanitized_answer or "")

    def test_within_band_grounded_stays_verified(self) -> None:
        ref = _ref_with_bands({"imidacloprid|ml/l": (2.0, "BARC test cite")})
        verifier = HardenedDosageVerifier(dose_reference=ref)
        result = verifier.verify(
            "Spray Admire at 2 ml per litre of water.",
            [RetrievedSource(
                id="ok", score=1.0,
                content_en="Spray Admire 200 SL at 2 ml per litre of water.",
                citation="BARC ok",
            )],
        )
        self.assertEqual(result.grounded_count, 1)
        self.assertEqual(result.unsupported_count, 0)
        self.assertIsNone(result.sanitized_answer)

    def test_default_verifier_matches_referenceless_semantics(self) -> None:
        # The default-constructed verifier must behave exactly like the
        # pre-F1-02 verifier: the poisoned overdose is grounded (entailment
        # only) — the outlier catch requires an explicit reference.
        answer = "Spray Admire at 10 ml per litre of water."
        default = HardenedDosageVerifier()
        with_disabled = HardenedDosageVerifier(dose_reference=DoseReference.disabled())
        self.assertEqual(default.verify(answer, [self._poisoned_source()]),
                         with_disabled.verify(answer, [self._poisoned_source()]))
        result = default.verify(answer, [self._poisoned_source()])
        self.assertEqual(result.grounded_count, 1)
        self.assertEqual(result.flags, ())


class ContainerConfigTests(unittest.TestCase):
    def test_settings_defaults(self) -> None:
        s = Settings(_env_file=None)
        self.assertEqual(s.dose_reference_path, "")
        self.assertEqual(s.dose_outlier_factor, 3.0)
        self.assertEqual(
            s.dose_reference_resolved_path.name, "dose_reference_v1.json"
        )


if __name__ == "__main__":
    unittest.main()
