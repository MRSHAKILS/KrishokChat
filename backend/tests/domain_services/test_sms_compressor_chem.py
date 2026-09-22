"""Chemical-name slot in SMSCompressor.compress_from_qa_result."""
from app.domain.contracts import QAResult
from app.domain.enums import SafetyCategory, VerificationConfidence
from app.domain.sms_compressor import SMSCompressor


def _sms(answer, monkeypatch, on=True):
    monkeypatch.setenv("SMS_CHEM_SLOT", "1" if on else "0")
    qa = QAResult(query="q", category=SafetyCategory.SAFE_AGRI, answer=answer,
                  confidence=VerificationConfidence.VERIFIED)
    return SMSCompressor.compress_from_qa_result(qa, institution="DAE")


ANS = "পাতা মোড়ানো পোকা দমনে Cartap ব্যবহার করুন। মাত্রা: 1 ml/L পানি। ৭ দিন পর আবার দিন।"


def test_chemical_prepended_when_dose_sentence_lacks_it(monkeypatch):
    out = _sms(ANS, monkeypatch)
    assert "Cartap" in out and "1 ml/L" in out and len(out) <= 160


def test_flag_off_keeps_old_behaviour(monkeypatch):
    assert "Cartap: " not in _sms(ANS, monkeypatch, on=False)


def test_not_duplicated_when_dose_sentence_names_it(monkeypatch):
    out = _sms("Mancozeb ২ গ্রাম প্রতি লিটার পানিতে মিশিয়ে স্প্রে করুন।", monkeypatch)
    assert out.count("Mancozeb") == 1


def test_never_invents_a_chemical(monkeypatch):
    out = _sms("সমস্যা হলে মাত্রা: 2 g/L পানিতে মিশিয়ে দিন।", monkeypatch)
    assert ":" in out and "2 g/L" in out
    for name in ("Cartap", "Mancozeb", "ইমিডাক্লোপ্রিড"):
        assert name not in out
