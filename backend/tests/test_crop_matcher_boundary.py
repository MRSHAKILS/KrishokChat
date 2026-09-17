"""Regression tests for the token-start Bengali crop matcher (fix 2026-09-17).

Root cause: rice alias "ধান" fired inside the unrelated word "সমাধান"
(solution) because Bengali vowel signs defeat regex \\b boundaries.
Each such false positive set has_crop=true and suppressed safety clarification.

v2 additions: leading-punctuation strip ("(ধানের)" matches); লঙ্কা/লংকা
recognized as chilli (farmer_q_593).
Documented residual (NOT asserted fixed): tokens merely STARTING with an
alias (e.g. place name ধানসিড়ি, compound আলুপটল) still match.
"""
from app.domain.intent import _match_crop_alias
from app.domain.query_extractor import QueryExtractor


def test_samadhan_alone_matches_no_crop():
    assert _match_crop_alias("সমাধান চাই") is None
    assert _match_crop_alias("লেবু গাছে সমাধান কী?") is None
    assert QueryExtractor.extract("লেবু গাছে সমাধান কী?").crop is None
    assert QueryExtractor.extract("তরমুজ গাছের সমাধান চাই").crop is None


def test_true_crops_still_match():
    assert _match_crop_alias("ধানের ব্লাস্ট") == "rice"
    assert _match_crop_alias("আলুর দাগ") == "potato"
    assert _match_crop_alias("মরিচের পোকা") == "chilli"
    assert _match_crop_alias("বেগুনের ডগা") == "brinjal"
    assert _match_crop_alias("লঙ্কা গাছে পোকা") == "chilli"
    assert QueryExtractor.extract("ধানের ব্লাস্ট রোগের সমাধান কী?").crop == "rice"
    assert QueryExtractor.extract("আলুর নাভি ধসা").crop == "potato"


def test_leading_punctuation_matches():
    assert _match_crop_alias("(ধানের) পাতায় দাগ?") == "rice"


def test_pipeline_path_punctuation_matches():
    # The pipeline consumes QueryExtractor, not _match_crop_alias: the strip
    # must work on the production path (regression: strip was dead code here).
    assert QueryExtractor.extract("(ধানের) পাতায় দাগ?").crop == "rice"


def test_retrieval_bridge_has_no_samadhan_rice():
    # build_retrieval_query must not inject the "rice" bridge from সমাধান.
    from app.application.query_builder import build_retrieval_query
    from app.domain.contracts import QueryContext

    ctx = QueryContext()
    q_with = build_retrieval_query("লঙ্কা গাছে সমাধান আছে?", ctx, "safe_agri")
    assert " rice" not in (" " + q_with + " ").replace("  ", " ")
    q_rice = build_retrieval_query("ধানের ব্লাস্ট", ctx, "safe_agri")
    assert "rice" in q_rice


def test_romanized_forms_hold():
    assert _match_crop_alias("dhaner jomi") == "rice"
    assert _match_crop_alias("begun e poka") == "brinjal"
    assert _match_crop_alias("moris gas") == "chilli"
