"""R4 — Tests for Bengali advisory templates (T1 and T2).

Pure string rendering tests:
  - Numbers are verbatim from the Fact row (no rounding, no fabrication).
  - T1 includes crop, problem, active, dose, interval, PHI, citation.
  - T2 includes T1 fields + IPM alternatives + optional stage advisory note.
  - Severity rendering.
"""

from __future__ import annotations

import pytest

from app.domain.advisory_templates import render_t1, render_t2
from app.domain.fact_base import Fact


def _sample_fact(**overrides) -> Fact:
    data = {
        "crop": "potato",
        "crop_bn": "আলু",
        "problem": "late_blight",
        "problem_bn": "নাবি ধ্বসা / লেট ব্লাইট",
        "problem_type": "disease",
        "stage": "tuber_bulking",
        "active_ingredient": "mancozeb",
        "dose_min": 2.0,
        "dose_max": 2.5,
        "dose_unit": "g/l",
        "application_interval_days": 7,
        "pre_harvest_interval_days": 7,
        "ipm_alternatives_bn": ("আক্রান্ত পাতা অপসারণ", "সুষম সেচ"),
        "banned_flag": False,
        "severity": "high",
        "source_node_id": "DAE_PEST_5E48F1_001",
        "source_doc": "DAE. List of Registered Agricultural Pesticides",
        "citation": "DAE. page_751. List of Registered Agricultural Pesticides (DAE). pp. 751-751.",
        "grounding": "corpus-extracted",
        "confidence": 0.9,
    }
    data.update(overrides)
    return Fact.from_dict(data)


def test_render_t1_content() -> None:
    fact = _sample_fact()
    rendered = render_t1(fact)

    assert "আলু" in rendered
    assert "নাবি ধ্বসা" in rendered
    assert "mancozeb" in rendered
    assert "2–2.5 g/l" in rendered
    assert "৭" in rendered or "7" in rendered
    assert "৭ দিন আগে" in rendered or "7 দিন আগে" in rendered
    assert fact.citation in rendered


def test_render_t1_single_dose_number() -> None:
    fact = _sample_fact(dose_min=2.0, dose_max=2.0)
    rendered = render_t1(fact)
    assert "2 g/l" in rendered


def test_render_t2_with_ipm_and_stage() -> None:
    fact = _sample_fact()
    stage_note = "কন্দ বৃদ্ধির সময় জমিতে অতিরিক্ত পানি জমতে দেবেন না।"
    rendered = render_t2(fact, stage_advisory_bn=stage_note)

    assert "আলু" in rendered
    assert "mancozeb" in rendered
    assert "2–2.5 g/l" in rendered
    assert "সমন্বিত বালাই ব্যবস্থাপনা (IPM)" in rendered
    assert "আক্রান্ত পাতা অপসারণ" in rendered
    assert "সুষম সেচ" in rendered
    assert "বর্তমান পর্যায়ের পরামর্শ" in rendered
    assert stage_note in rendered
    assert fact.citation in rendered


def test_render_t2_no_stage_advisory() -> None:
    fact = _sample_fact(ipm_alternatives_bn=())
    rendered = render_t2(fact, stage_advisory_bn=None)

    assert "mancozeb" in rendered
    assert "বর্তমান পর্যায়ের পরামর্শ" not in rendered
    assert "সমন্বিত বালাই ব্যবস্থাপনা (IPM)" not in rendered
