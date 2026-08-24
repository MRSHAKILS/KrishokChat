"""PR1: potato late-blight weather-risk rule + advisory draft (pure domain).

Risk rule — a documented approximation of the classic Smith period, evaluated
on DAILY AGGREGATES an operator snapshot can carry (the ≥90% RH for ≥11 h
criterion needs hourly data most bulletins don't publish):

- a day is *favourable* when ``tmin_c >= 10.0`` AND ``rh_pct >= 85``
  (mean-RH proxy for the humidity criterion);
- risk tier from the run of consecutive favourable days ending at the
  snapshot's latest date: >=2 → ``high``, 1 → ``watch``, 0 → ``low``.

Seasonality: Bangladesh's main potato season is ~1 Nov – 15 Mar; ``in_season``
is derived from the snapshot's own latest date (deterministic — no wall clock),
so an out-of-season "high" is reported but flagged for the admin to judge.

The drafted advisory cites the corpus grounding (CABI late-blight nodes: the
disease is severe in cold+humid weather) and deliberately contains NO fungicide
dose — dose advice flows through the grounded QA pipeline (F1-02) or 16123.
"""

from __future__ import annotations

from dataclasses import dataclass

TMIN_THRESHOLD_C = 10.0
RH_THRESHOLD_PCT = 85.0
HIGH_DAYS = 2

# Main potato season window (month, day) inclusive.
SEASON_START = (11, 1)
SEASON_END = (3, 15)

RISK_LABELS_BN = {"high": "উচ্চ", "watch": "সতর্ক", "low": "কম"}


@dataclass(frozen=True)
class DailyWeather:
    date: str  # ISO date, e.g. "2026-01-15"
    tmin_c: float
    rh_pct: float
    rain_mm: float = 0.0


@dataclass(frozen=True)
class DistrictRisk:
    district: str
    risk: str  # "high" | "watch" | "low"
    favourable_days: int
    latest_date: str
    in_season: bool
    detail: tuple[DailyWeather, ...]  # the rows evaluated (latest N)


def _is_favourable(day: DailyWeather) -> bool:
    return day.tmin_c >= TMIN_THRESHOLD_C and day.rh_pct >= RH_THRESHOLD_PCT


def _in_season(iso_date: str) -> bool:
    try:
        year, month, day = (int(part) for part in iso_date.split("-")[:3])
    except (ValueError, AttributeError):
        return False
    if not (1 <= month <= 12 and 1 <= day <= 31 and year > 1900):
        return False
    if (month, day) >= SEASON_START or (month, day) <= SEASON_END:
        return True
    return False


def evaluate_district(district: str, days: list[DailyWeather]) -> DistrictRisk | None:
    """Risk for one district from its daily rows (any order; sorted by date)."""
    rows = sorted(days, key=lambda d: d.date)
    if not rows:
        return None
    latest = rows[-1]
    favourable = 0
    for day in reversed(rows):
        if _is_favourable(day):
            favourable += 1
        else:
            break
    if favourable >= HIGH_DAYS:
        risk = "high"
    elif favourable == 1:
        risk = "watch"
    else:
        risk = "low"
    return DistrictRisk(
        district=district,
        risk=risk,
        favourable_days=favourable,
        latest_date=latest.date,
        in_season=_in_season(latest.date),
        detail=tuple(rows[-7:]),
    )


def draft_advisory(result: DistrictRisk, sample: bool = False) -> dict[str, str]:
    """Composer prefill for the announcements lane (admin reviews + edits)."""
    label = RISK_LABELS_BN.get(result.risk, result.risk)
    title = f"আলুর লেট ব্লাইট ঝুঁকি: {result.district} জেলা ({label})"
    window = ", ".join(f"{d.date}: সর্বনিম্ন {d.tmin_c:g}°সে, আর্দ্রতা {d.rh_pct:g}%" for d in result.detail[-2:])
    body = (
        f"আবহাওয়া উপাত্ত অনুযায়ী গত {result.favourable_days} দিন ধরে {result.district} জেলায় "
        f"লেট ব্লাইট-অনুকূল পরিস্থিতি বিরাজ করছে ({window})। "
        "ঠাণ্ডা ও আর্দ্র আবহাওয়ায় লেট ব্লাইট মারাত্মক রূপ নিতে পারে (তথ্যসূত্র: CABI Potato Disease Manuals)। "
        "আলু ক্ষেত প্রতিদিন পরীক্ষা করুন; পাতায় জলসিক্ত কালচে দাগ দেখা দিলে দ্রুত ব্যবস্থা নিন। "
        "প্রতিরোধমূলক ছত্রাকনাশকের অনুমোদিত মাত্রা জানতে এই অ্যাপে জিজ্ঞাসা করুন বা কৃষক কল সেন্টারে কল করুন: ১৬১২৩।"
    )
    if not result.in_season:
        body += " (উল্লেখ্য: এখন মূল আলু মৌসুমের বাইরে — প্রয়োজনে এলাকার কৃষি কর্মকর্তার সঙ্গে যাচাই করুন।)"
    if sample:
        body += " (উপাত্ত নমুনা — প্রকাশের আগে প্রকৃত আবহাওয়া উপাত্ত বসিয়ে নিন।)"
    severity = "urgent" if result.risk == "high" else "warning" if result.risk == "watch" else "info"
    return {"title_bn": title, "body_bn": body, "kind": "disease_alert", "severity": severity, "crop": "আলু"}
