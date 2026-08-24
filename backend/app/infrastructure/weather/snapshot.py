"""PR1: loader for the operator-maintained late-blight weather snapshot.

The snapshot is a JSON file on disk (never fetched at request time —
AGENTS.md rule 2). Schema::

    {
      "is_sample": true,                // shipped placeholder — MUST be
                                        // replaced with real BMD/BAMIS data
      "source_note": "...",             // provenance line for the admin UI
      "districts": {
        "Bogura": [
          {"date": "2026-01-15", "tmin_c": 11.5, "rh_pct": 88, "rain_mm": 4.2},
          ...                            // any number of daily rows
        ],
        ...
      }
    }

A missing or invalid file returns ``None`` — callers surface a clear
"no snapshot" state instead of failing.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from app.domain.late_blight import DailyWeather

logger = logging.getLogger("krishokchat.weather")


class WeatherSnapshot:
    def __init__(
        self,
        districts: dict[str, list[DailyWeather]],
        *,
        is_sample: bool,
        source_note: str,
    ) -> None:
        self.districts = districts
        self.is_sample = is_sample
        self.source_note = source_note

    @property
    def latest_date(self) -> str:
        return max(
            (rows[-1].date for rows in self.districts.values() if rows),
            default="",
        )


def load_weather_snapshot(path: str | Path) -> WeatherSnapshot | None:
    try:
        with open(path, encoding="utf-8") as fh:
            payload = json.load(fh)
    except FileNotFoundError:
        logger.warning("weather snapshot not found at %s — late-blight risk unavailable", path)
        return None
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("weather snapshot unreadable at %s (%s) — late-blight risk unavailable", path, exc)
        return None

    districts: dict[str, list[DailyWeather]] = {}
    for district, rows in (payload.get("districts") or {}).items():
        parsed: list[DailyWeather] = []
        for row in rows or []:
            try:
                parsed.append(
                    DailyWeather(
                        date=str(row["date"]),
                        tmin_c=float(row["tmin_c"]),
                        rh_pct=float(row["rh_pct"]),
                        rain_mm=float(row.get("rain_mm", 0.0)),
                    )
                )
            except (KeyError, TypeError, ValueError):
                continue  # skip malformed rows, keep the rest
        if parsed:
            parsed.sort(key=lambda d: d.date)
            districts[str(district)] = parsed
    if not districts:
        logger.warning("weather snapshot at %s carried no usable district rows", path)
        return None
    return WeatherSnapshot(
        districts,
        is_sample=bool(payload.get("is_sample", False)),
        source_note=str(payload.get("source_note", ""))[:200],
    )
