import pytest
from app.domain.contracts import QAResult
from app.domain.enums import SafetyCategory, VerificationConfidence
from app.domain.fact_base import Fact
from app.domain.sms_compressor import SMSCompressor


def test_compress_from_slots_en():
    sms = SMSCompressor.compress_from_slots(
        crop="potato",
        pest="late_blight",
        active="mancozeb",
        formulation="80 WP",
        dose_min=2.0,
        dose_max=2.5,
        unit="g/l",
        vol="1L",
        tau=7,
        phi=14,
        helpline="16123",
        institution="DAE",
        lang="en",
    )
    assert len(sms) <= 160
    assert "potato" in sms.lower()
    assert "late blight" in sms.lower()
    assert "mancozeb" in sms.lower()
    assert "80 WP" in sms
    assert "2-2.5g/l/1L" in sms
    assert "7d" in sms
    assert "14d" in sms
    assert "16123" in sms


def test_compress_from_slots_bn():
    sms = SMSCompressor.compress_from_slots(
        crop="আলু",
        pest="নাবি ধসা",
        active="ম্যানকোজেব",
        formulation="৮০ ডব্লিউপি",
        dose_min=2.0,
        dose_max=2.5,
        unit="গ্রাম/লিটার",
        vol="১ লিটার",
        tau=7,
        phi=14,
        helpline="১৬১২৩",
        institution="DAE",
        lang="bn",
    )
    assert len(sms) <= 160
    assert "আলু" in sms
    assert "ম্যানকোজেব" in sms
    assert "২-২.৫" in sms or "2-2.5" in sms
    assert "১৬১২৩" in sms


def test_compress_from_fact():
    fact = Fact(
        crop="rice",
        crop_bn="ধান",
        problem="blast",
        problem_bn="ব্লাস্ট রোগ",
        problem_type="disease",
        stage="tillering",
        active_ingredient="tricyclazole",
        dose_min=0.75,
        dose_max=0.75,
        dose_unit="g/l",
        application_interval_days=10,
        pre_harvest_interval_days=21,
    )
    sms = SMSCompressor.compress_from_fact(fact, institution="BRRI", lang="bn")
    assert len(sms) <= 160
    assert "BRRI পরামর্শ:" in sms
    assert "ধান" in sms
    assert "ব্লাস্ট" in sms
    assert "tricyclazole" in sms
    assert "0.75" in sms
    assert "10" in sms
    assert "21" in sms
    assert "১৬১২৩" in sms


def test_compress_from_qa_result_referral_on_blocked():
    qa_res = QAResult(
        query="বিষাক্ত কীটনাশক দিয়ে আত্মহত্যা করতে চাই",
        category=SafetyCategory.SELF_HARM_OR_POISONING_RISK,
        answer="সাহায্যের জন্য ১৬১২৩ নম্বরে কল করুন।",
        confidence=VerificationConfidence.BLOCKED,
    )
    sms = SMSCompressor.compress_from_qa_result(qa_res)
    assert len(sms) <= 160
    assert "১৬১২৩" in sms
    assert "কল সেন্টারে সরাসরি ডায়াল করুন" in sms


def test_compress_from_qa_result_referral_on_unverified_flags():
    qa_res = QAResult(
        query="বেগুনের পোকা দমনে কি দেব?",
        category=SafetyCategory.SAFE_AGRI,
        answer="সাইপারমেথ্রিন ১০ মিলি প্রতি লিটারে দিন।",
        confidence=VerificationConfidence.FLAGGED_UNVERIFIED,
        verifier_flags=("Unverified dosage claim: 10 ml",),
    )
    sms = SMSCompressor.compress_from_qa_result(qa_res)
    assert len(sms) <= 160
    assert "১৬১২৩" in sms
    # Unsupported dosage must not leak into SMS
    assert "সাইপারমেথ্রিন" not in sms
    assert "10 ml" not in sms


def test_compress_from_qa_result_preserves_dosage_over_preamble():
    long_answer = (
        "কৃষক ভাই, আপনার ধানে মাজরা পোকার আক্রমণ দেখা দিলে প্রথমে খেত নিয়মিত পরিদর্শন করুন এবং ডিমের গাদা সংগ্রহ করে নষ্ট করুন। "
        "আক্রমণ বেশি হলে প্রতি লিটার পানিতে ০.৫ মিলি ক্লোরপাইরিফস ২০ ইসি মিশিয়ে স্প্রে করুন। "
        "স্প্রে করার সময় মুখে মাস্ক পরুন এবং সাবান দিয়ে হাত ধুয়ে নিন।"
    )
    qa_res = QAResult(
        query="ধানে মাজরা পোকা হয়েছে কি করব?",
        category=SafetyCategory.SAFE_AGRI,
        answer=long_answer,
        confidence=VerificationConfidence.VERIFIED,
    )
    sms = SMSCompressor.compress_from_qa_result(qa_res, institution="DAE")
    assert len(sms) <= 160
    assert "DAE পরামর্শ:" in sms
    assert "১৬১২৩" in sms
    # Crucial: Dosage MUST survive
    assert "০.৫ মিলি" in sms or "0.5" in sms
    assert "ক্লোরপাইরিফস" in sms
