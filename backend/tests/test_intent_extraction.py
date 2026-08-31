"""R5 — Intent extraction and merged safety+intent tests.

Locks all R5 invariants:
  1. keyword_intent unit table.
  2. SafetyDecision carries intent on safe_agri, None on terminal.
  3. Precheck hit (0 LLM) → intent is None.
  4. Malformed/absent LLM intent block → never changes category.
  5. Classifier outage → intent is None.
  6. Legacy shim reads decision.intent, not a second classify_json call.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.domain.intent import Intent, keyword_intent
from app.domain.enums import SafetyCategory


# ---------------------------------------------------------------------------
# 1. keyword_intent unit table
# ---------------------------------------------------------------------------


class TestKeywordIntent:
    def test_treatment_bengali(self) -> None:
        i = keyword_intent("আলুর প্রতিকার কী?")
        assert i is not None and i.kind == "treatment" and i.source == "keyword"

    def test_treatment_english(self) -> None:
        i = keyword_intent("what treatment for late blight?")
        assert i is not None and i.kind == "treatment"

    def test_treatment_spray(self) -> None:
        i = keyword_intent("কীভাবে স্প্রে করব?")
        assert i is not None and i.kind == "treatment"

    def test_prevention_bengali(self) -> None:
        i = keyword_intent("রোগ প্রতিরোধ করব কীভাবে?")
        assert i is not None and i.kind == "prevention"

    def test_prevention_english(self) -> None:
        i = keyword_intent("how to prevent fungal disease?")
        assert i is not None and i.kind == "prevention"

    def test_fertilizer_bengali(self) -> None:
        i = keyword_intent("ইউরিয়া সার কতটুকু দিতে হবে?")
        assert i is not None and i.kind == "fertilizer"

    def test_fertilizer_english(self) -> None:
        i = keyword_intent("how much npk fertilizer for rice?")
        assert i is not None and i.kind == "fertilizer"

    def test_no_match_returns_none(self) -> None:
        i = keyword_intent("আলুর দাম কত?")
        assert i is None

    def test_treatment_beats_prevention(self) -> None:
        """Treatment keywords are checked before prevention."""
        i = keyword_intent("প্রতিকার এবং প্রতিরোধ")
        assert i is not None and i.kind == "treatment"

    def test_empty_query(self) -> None:
        assert keyword_intent("") is None

    def test_intent_source_is_keyword(self) -> None:
        i = keyword_intent("ওষুধ কী?")
        assert i is not None and i.source == "keyword"


# ---------------------------------------------------------------------------
# 2. Intent dataclass
# ---------------------------------------------------------------------------


def test_intent_defaults() -> None:
    i = Intent()
    assert i.kind is None
    assert i.crop is None
    assert i.source == "none"


def test_intent_frozen() -> None:
    i = Intent(kind="treatment")
    with pytest.raises(Exception):
        i.kind = "fertilizer"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# 3+4. SafetyClassifier returns correct Intent in various LLM scenarios
# ---------------------------------------------------------------------------


def _make_classifier(llm_response: dict) -> "SafetyClassifier":
    from app.application.safety import SafetyClassifier

    client = MagicMock()
    client.classify_json = AsyncMock(return_value=llm_response)
    return SafetyClassifier(client)


from app.domain.contracts import QueryContext


@pytest.mark.asyncio
async def test_safe_agri_with_llm_intent_block() -> None:
    """LLM returns an intent block → SafetyDecision.intent is populated."""
    from app.application.safety import SafetyClassifier

    clf = _make_classifier({
        "category": "safe_agri",
        "confidence": 0.95,
        "reason": "normal agri",
        "matched_rules": [],
        "requires_escalation": False,
        "intent": {
            "kind": "treatment",
            "crop": "potato",
            "problem": "late_blight",
            "stage": None,
            "upazila": None,
        },
    })
    decision = await clf.classify("আলুর মড়ক রোগের ওষুধ?", QueryContext())
    assert decision.category is SafetyCategory.SAFE_AGRI
    assert decision.intent is not None
    assert decision.intent.kind == "treatment"
    assert decision.intent.crop == "potato"
    assert decision.intent.problem == "late_blight"


@pytest.mark.asyncio
async def test_keyword_wins_over_llm_intent() -> None:
    """Keyword resolves kind; LLM block enriches slots only."""
    clf = _make_classifier({
        "category": "safe_agri",
        "confidence": 0.9,
        "reason": "ok",
        "matched_rules": [],
        "requires_escalation": False,
        "intent": {
            "kind": "general_info",  # LLM guessed wrong; keyword should win
            "crop": "rice",
            "problem": None,
            "stage": None,
            "upazila": None,
        },
    })
    decision = await clf.classify("চিকিৎসা কী করব?", QueryContext())
    assert decision.intent is not None
    # Keyword matched "চিকিৎসা" → treatment; LLM's "general_info" is ignored.
    assert decision.intent.kind == "treatment"
    assert decision.intent.source == "keyword"
    assert decision.intent.crop == "rice"  # enriched from LLM


@pytest.mark.asyncio
async def test_safe_agri_missing_intent_block() -> None:
    """Absent intent block → degrades to general_info, not an error."""
    clf = _make_classifier({
        "category": "safe_agri",
        "confidence": 0.8,
        "reason": "ok",
        "matched_rules": [],
        "requires_escalation": False,
        # no "intent" key at all
    })
    decision = await clf.classify("আলুর দাম কত?", QueryContext())
    assert decision.category is SafetyCategory.SAFE_AGRI
    assert decision.intent is not None
    assert decision.intent.kind == "general_info"


@pytest.mark.asyncio
async def test_safe_agri_null_intent_block() -> None:
    """Explicit null intent → degrades gracefully."""
    clf = _make_classifier({
        "category": "safe_agri",
        "confidence": 0.8,
        "reason": "ok",
        "matched_rules": [],
        "requires_escalation": False,
        "intent": None,
    })
    decision = await clf.classify("ধানের রোগ কী?", QueryContext())
    assert decision.intent is not None
    assert decision.intent.kind == "general_info"


@pytest.mark.asyncio
async def test_terminal_decision_intent_is_none() -> None:
    """Off-topic / banned → intent is None."""
    clf = _make_classifier({
        "category": "off_topic",
        "confidence": 0.99,
        "reason": "not agriculture",
        "matched_rules": [],
        "requires_escalation": False,
    })
    decision = await clf.classify("who won the world cup?", QueryContext())
    assert decision.category is SafetyCategory.OFF_TOPIC
    assert decision.intent is None


@pytest.mark.asyncio
async def test_malformed_intent_kind_ignored() -> None:
    """An invalid intent kind from the LLM must not crash or change category."""
    clf = _make_classifier({
        "category": "safe_agri",
        "confidence": 0.9,
        "reason": "ok",
        "matched_rules": [],
        "requires_escalation": False,
        "intent": {"kind": "INVALID_KIND", "crop": None, "problem": None, "stage": None, "upazila": None},
    })
    decision = await clf.classify("ধানের পোকা?", QueryContext())
    assert decision.category is SafetyCategory.SAFE_AGRI
    # Invalid kind → falls back to "none" source with general_info
    assert decision.intent is not None
    assert decision.intent.kind == "general_info"


# ---------------------------------------------------------------------------
# 3. Precheck hit → intent is None, 0 LLM calls (LLM client never called)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_precheck_hit_intent_is_none() -> None:
    """A deterministic precheck match returns intent=None without any LLM call."""
    from app.application.safety import SafetyClassifier

    client = MagicMock()
    client.classify_json = AsyncMock(side_effect=AssertionError("LLM must not be called on precheck hit"))
    clf = SafetyClassifier(client)

    # "furadan" matches the banned_active:carbofuran precheck rule
    decision = await clf.classify("furadan দিতে হবে?", QueryContext())
    assert decision.intent is None
    # Verify LLM was not called
    client.classify_json.assert_not_called()


# ---------------------------------------------------------------------------
# 5. Classifier outage → intent is None
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_outage_intent_is_none() -> None:
    from app.application.safety import SafetyClassifier

    client = MagicMock()
    client.classify_json = AsyncMock(side_effect=RuntimeError("network error"))
    clf = SafetyClassifier(client)

    decision = await clf.classify("আলুর রোগ?", QueryContext())
    assert decision.category is SafetyCategory.LOW_CONFIDENCE
    assert decision.classifier_outage is True
    assert decision.intent is None


# ---------------------------------------------------------------------------
# 6. Legacy shim reads decision.intent — no second classify_json call
# ---------------------------------------------------------------------------


def test_legacy_shim_uses_decision_intent() -> None:
    """Verify the legacy shim reads decision.intent — not a second classify_json call.

    We run classify_intent in a background thread so asyncio.run() inside the
    shim doesn't conflict with pytest-asyncio's event loop.
    """
    import threading
    from unittest.mock import patch
    from app.domain.intent import Intent

    mock_decision = MagicMock()
    mock_decision.category = MagicMock()
    mock_decision.category.value = "safe_agri"
    mock_decision.terminal = False
    mock_decision.confidence = 0.9
    mock_decision.reason = "ok"
    mock_decision.response = None
    mock_decision.intent = Intent(kind="treatment", source="keyword")

    mock_classifier_instance = MagicMock()
    mock_classifier_instance.classify = AsyncMock(return_value=mock_decision)

    result_box: list[dict] = []
    error_box: list[Exception] = []

    def run_in_thread() -> None:
        with patch("app.services.advisory.intent_classifier.SafetyClassifier", return_value=mock_classifier_instance):
            with patch("app.services.advisory.intent_classifier.create_llm_client", return_value=MagicMock()):
                import importlib
                from app.services.advisory import intent_classifier
                importlib.reload(intent_classifier)
                try:
                    result_box.append(intent_classifier.classify_intent("আলুর প্রতিকার?"))
                except Exception as exc:
                    error_box.append(exc)

    t = threading.Thread(target=run_in_thread, daemon=True)
    t.start()
    t.join(timeout=10)
    assert not error_box, f"classify_intent raised: {error_box[0]}"
    assert result_box, "classify_intent returned no result"
    assert result_box[0]["intent"] == "treatment"


# ---------------------------------------------------------------------------
# 7. Slot Disambiguation & Clarification Intercept Tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_ambiguous_treatment_query_triggers_clarification_slots() -> None:
    """When a treatment/disease query has no crop, intent marks is_ambiguous=True with clarification prompt."""
    clf = _make_classifier({
        "category": "safe_agri",
        "confidence": 0.95,
        "reason": "disease symptom query without crop",
        "matched_rules": [],
        "requires_escalation": False,
        "intent": {
            "kind": "treatment",
            "crop": None,
            "problem": "leaf_spot",
            "plant_part": "leaf",
            "problem_type": "disease",
            "is_ambiguous": True,
            "clarification_question_bn": "কোন ফসলের পাতায় লালচে দাগ হয়েছে বলবেন কি?",
            "suggested_crops": ["potato", "rice", "tomato"],
        },
    })
    decision = await clf.classify("পাতায় লালচে দাগ হয়েছে প্রতিকার কী?", QueryContext())
    assert decision.intent is not None
    assert decision.intent.crop is None
    assert decision.intent.plant_part == "leaf"
    assert decision.intent.is_ambiguous is True
    assert "কোন ফসলের" in (decision.intent.clarification_question_bn or "")
    assert "rice" in decision.intent.suggested_crops


@pytest.mark.asyncio
async def test_pipeline_clarification_intercept_skips_retrieval() -> None:
    """Pipeline intercepts ambiguous crop-less queries, returning clarification with 0 retrieval calls."""
    from app.application.generation import GroundedAnswerGenerator
    from app.application.qa_pipeline import QAInput, QAPipeline
    from app.application.safety import SafetyClassifier
    from app.domain.contracts import RetrievedSource
    from app.domain.enums import PipelineStage, ResolutionTier, StageStatus
    from app.infrastructure.verification.dosage import DosageVerifier

    llm = MagicMock()
    llm.classify_json = AsyncMock(return_value={
        "category": "safe_agri",
        "confidence": 0.95,
        "reason": "treatment without crop",
        "matched_rules": [],
        "requires_escalation": False,
        "intent": {
            "kind": "treatment",
            "crop": None,
            "problem": "leaf_spot",
            "plant_part": "leaf",
            "problem_type": "disease",
            "is_ambiguous": True,
            "clarification_question_bn": "কোন ফসলের পাতায় সমস্যা হয়েছে?",
        },
    })
    llm.generate = AsyncMock(side_effect=AssertionError("Generation must not run on clarification turn"))

    retriever = MagicMock()
    retriever.retrieve = MagicMock(side_effect=AssertionError("Retrieval must not run on clarification turn"))

    audit = MagicMock()
    sessions = MagicMock()
    sessions.get.return_value = []

    pipeline = QAPipeline(
        safety=SafetyClassifier(llm),
        retriever=retriever,
        generator=GroundedAnswerGenerator(llm),
        verifier=DosageVerifier(),
        audit=audit,
        sessions=sessions,
    )

    result = await pipeline.run(QAInput(query="পাতায় দাগ হয়েছে কী দেব?"))
    assert result.resolution_tier is ResolutionTier.INTERACTIVE_CLARIFICATION
    assert "কোন ফসলের" in result.answer
    assert result.sources == ()
    retriever.retrieve.assert_not_called()
    llm.generate.assert_not_called()

    # Check trace has RETRIEVAL/GENERATION as SKIP
    stages_skipped = [
        event.stage for event in result.trace if event.status is StageStatus.SKIP
    ]
    assert PipelineStage.RETRIEVAL in stages_skipped
    assert PipelineStage.GENERATION in stages_skipped


def test_cross_modal_conflict_detection_unit() -> None:
    from app.domain.intent import detect_cross_modal_conflict

    # Case 1: Image = Potato, Text = Begun (Conflict)
    conflict, img_c, txt_c, prompt = detect_cross_modal_conflict("potato", "আমার বেগুন গাছে পোকা লেগেছে")
    assert conflict is True
    assert img_c == "potato"
    assert txt_c == "brinjal"
    assert "আলু" in prompt
    assert "বেগুন" in prompt

    # Case 2: Image = Rice, Text = Dhan (Agreement - No conflict)
    conflict, img_c, txt_c, prompt = detect_cross_modal_conflict("rice", "ধানের ব্লাস্ট রোগের সমাধান কী?")
    assert conflict is False
    assert prompt is None

    # Case 3: No image provided (No conflict)
    conflict, img_c, txt_c, prompt = detect_cross_modal_conflict(None, "টমেটো পচা রোধ করব কীভাবে?")
    assert conflict is False


@pytest.mark.asyncio
async def test_pipeline_intercepts_cross_modal_contradiction() -> None:
    from app.application.generation import GroundedAnswerGenerator
    from app.application.safety import SafetyClassifier
    from app.application.verifier import HardenedDosageVerifier
    from app.application.qa_pipeline import QAInput, QAPipeline
    from app.domain.contracts import QueryContext
    from app.domain.enums import PipelineStage, ResolutionTier, StageStatus

    llm = MagicMock()
    llm.classify_json = AsyncMock(return_value={
        "category": "safe_agri",
        "confidence": 0.95,
        "reason": "safe question",
        "matched_rules": [],
        "requires_escalation": False,
        "intent": {
            "kind": "treatment",
            "crop": "brinjal",
            "problem": "pest",
            "is_ambiguous": False,
        },
    })
    llm.generate = AsyncMock(side_effect=AssertionError("Generation must not run on cross-modal contradiction"))

    retriever = MagicMock()
    retriever.retrieve = MagicMock(side_effect=AssertionError("Retrieval must not run on cross-modal contradiction"))

    pipeline = QAPipeline(
        safety=SafetyClassifier(llm),
        retriever=retriever,
        generator=GroundedAnswerGenerator(llm),
        verifier=HardenedDosageVerifier(),
        audit=MagicMock(),
        sessions=MagicMock(),
    )

    # User uploaded Potato image, but typed "বেগুন"
    result = await pipeline.run(QAInput(query="আমার বেগুন গাছে কী স্প্রে করব?", crop="potato"))
    assert result.resolution_tier is ResolutionTier.INTERACTIVE_CLARIFICATION
    assert "আলু" in result.answer
    assert "বেগুন" in result.answer
    assert result.sources == ()
    retriever.retrieve.assert_not_called()
    llm.generate.assert_not_called()


def test_regional_dialect_and_banglish_intent_extraction() -> None:
    # Sylheti dialect treatment query
    i_syl = keyword_intent("পাতা পুইড়া যাইতাছে কী করমু?")
    assert i_syl is not None
    assert i_syl.kind == "treatment"
    assert i_syl.plant_part == "leaf"
    assert i_syl.is_ambiguous is True  # missing crop slot

    # Chittagonian dialect crop + pest
    i_ctg = keyword_intent("বাইঙ্গন গাছে পোঁকা দমন করমু কেমনে?")
    assert i_ctg is not None
    assert i_ctg.kind == "treatment"
    assert i_ctg.crop == "brinjal"
    assert i_ctg.is_ambiguous is False

    # Banglish query
    i_banglish = keyword_intent("begun e poka lagse ki spray korbo?")
    assert i_banglish is not None
    assert i_banglish.kind == "treatment"
    assert i_banglish.crop == "brinjal"
    assert i_banglish.is_ambiguous is False

    # Northern / Rajshahi dialect
    i_north = keyword_intent("হামার আলুর পাতাত পোকা ধরছে কি করমু?")
    assert i_north is not None
    assert i_north.kind == "treatment"
    assert i_north.crop == "potato"
    assert i_north.plant_part == "leaf"

