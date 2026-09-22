"""Boundary tests for the token-start Bengali crop matcher (45-crop gazetteer).

Matching rules under test: single-word aliases match at the START of a
whitespace-delimited token (Bengali vowel signs defeat regex \\b, so plain
substring matching would fire inside unrelated words such as rice "ধান"
inside "সমাধান" = solution); 2-character names (আম/জাম/আতা) and jute match
by exact token equality with explicit inflected forms; the generic collective
শাকসবজি never matches; multi-word aliases match by substring.
"""
from app.domain.intent import _match_crop_alias
from app.domain.query_extractor import QueryExtractor


def test_samadhan_alone_matches_no_crop():
    assert _match_crop_alias("সমাধান চাই") is None
    assert _match_crop_alias("গাছের সমাধান কী?") is None
    assert _match_crop_alias("লেবু গাছে সমাধান কী?") == "lemon"
    assert QueryExtractor.extract("লেবু গাছে সমাধান কী?").crop == "lemon"
    assert QueryExtractor.extract("তরমুজ গাছের সমাধান চাই").crop == "watermelon"


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


def test_short_names_match_exact_tokens_only():
    # আম (mango) must not fire on the pronouns আমার/আমাকে/আমি.
    assert _match_crop_alias("আমের পোকা") == "mango"
    assert _match_crop_alias("আমার গাছে পোকা") is None
    assert _match_crop_alias("আমি কৃষক") is None
    # জাম (jamun) must not fire on জামা (shirt).
    assert _match_crop_alias("Amar jam gacer") == "jamun"


def test_collision_prone_aliases_stay_quiet():
    # Patnitola (place) is not jute; symptom-yellow is not turmeric.
    assert _match_crop_alias("Patnitola, Naogaon") is None
    assert _match_crop_alias("পাটের জমি") == "jute"
    assert _match_crop_alias("গাছ হলুদ হয়ে গেছে") is None
    assert _match_crop_alias("হলুদগাছে পোকা") == "turmeric"
    # Paper S1: "holud dag" is yellow spots, and the production extractor
    # must agree with the gazetteer.
    paper = "Patay holud dag hoyeche, ki bish dibo?"
    assert _match_crop_alias(paper.lower()) is None
    assert QueryExtractor.extract(paper).crop is None
    assert _match_crop_alias("holud gach e poka") == "turmeric"
    assert _match_crop_alias("শীতকালীন শাকসবজি চাষ") is None


def test_expanded_taxonomy_spot_checks():
    assert QueryExtractor.extract("সরিষা ক্ষেতে জাব পোকা").crop == "mustard"
    assert QueryExtractor.extract("নারকেল গাছে পোকা").crop == "coconut"
    assert QueryExtractor.extract("পেঁপে গাছের পাতা কুকড়ে যাচ্ছে").crop == "papaya"
    assert _match_crop_alias("angor geser pata") == "grape"
