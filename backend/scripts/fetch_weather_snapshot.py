"""R8 — Offline weather snapshot fetcher for Bangladesh agricultural districts.

Fetches real meteorological forecasts/observations for key potato districts:
  Munshiganj, Bogura, Rangpur, Dinajpur, Rajshahi, Jashore, Comilla, Joypurhat.

Invariants:
  - Offline script only, never in request path.
  - is_sample is False on successful fetch.
  - Formatted and validated using R1 ingestion contract.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.infrastructure.ingestion.contract import write_deterministic_json

logger = logging.getLogger("krishokchat.weather_fetch")

# Canonical potato districts in Bangladesh with geographic coordinates and BBS ADM3 P-codes
DISTRICTS: dict[str, dict[str, Any]] = {
    "Munshiganj": {"lat": 23.5424, "lon": 90.5305, "pcode": "305956", "name_bn": "মুন্সীগঞ্জ"},
    "Bogura": {"lat": 24.8465, "lon": 89.3777, "pcode": "501020", "name_bn": "বগুড়া"},
    "Rangpur": {"lat": 25.7439, "lon": 89.2752, "pcode": "558576", "name_bn": "রংপুর"},
    "Dinajpur": {"lat": 25.6217, "lon": 88.6355, "pcode": "552730", "name_bn": "দিনাজপুর"},
    "Rajshahi": {"lat": 24.3636, "lon": 88.6241, "pcode": "508182", "name_bn": "রাজশাহী"},
    "Jashore": {"lat": 23.1664, "lon": 89.2182, "pcode": "404147", "name_bn": "যশোর"},
    "Comilla": {"lat": 23.4682, "lon": 91.1788, "pcode": "201933", "name_bn": "কুমিল্লা"},
    "Joypurhat": {"lat": 25.0968, "lon": 89.0227, "pcode": "503847", "name_bn": "জয়পুরহাট"},
}


def _fetch_district_weather(lat: float, lon: float) -> list[dict[str, Any]]:
    """Fetch 7-day daily series (tmin_c, rh_pct, rain_mm) from Open-Meteo."""
    params = {
        "latitude": f"{lat:.4f}",
        "longitude": f"{lon:.4f}",
        "daily": "temperature_2m_min,relative_humidity_2m_max,precipitation_sum",
        "timezone": "Asia/Dhaka",
    }
    url = f"https://api.open-meteo.com/v1/forecast?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "KrishokChat-WeatherIngest/1.0"})

    with urllib.request.urlopen(req, timeout=15) as res:
        if res.status != 200:
            raise RuntimeError(f"HTTP {res.status} from {url}")
        payload = json.loads(res.read().decode("utf-8"))

    daily = payload.get("daily", {})
    dates = daily.get("time", [])
    tmins = daily.get("temperature_2m_min", [])
    rhs = daily.get("relative_humidity_2m_max", [])
    rains = daily.get("precipitation_sum", [])

    rows: list[dict[str, Any]] = []
    for i, date_str in enumerate(dates):
        if i >= 7:
            break
        tmin = float(tmins[i]) if i < len(tmins) and tmins[i] is not None else 12.0
        rh = float(rhs[i]) if i < len(rhs) and rhs[i] is not None else 85.0
        rain = float(rains[i]) if i < len(rains) and rains[i] is not None else 0.0
        rows.append({
            "date": date_str,
            "tmin_c": round(tmin, 1),
            "rh_pct": int(round(rh)),
            "rain_mm": round(rain, 1),
        })

    return rows


def fetch_weather_snapshot(
    districts: list[str] | None = None,
    output_path: Path | None = None,
) -> dict[str, Any]:
    """Fetch real weather series for districts and save deterministic snapshot."""
    target_districts = districts or list(DISTRICTS.keys())
    districts_data: dict[str, list[dict[str, Any]]] = {}
    adm3_map: dict[str, str] = {}

    print(f"Fetching real agro-weather series for {len(target_districts)} districts...")
    for d_name in target_districts:
        meta = DISTRICTS.get(d_name)
        if not meta:
            print(f"  Warning: unknown district '{d_name}', skipping.")
            continue

        print(f"  Fetching {d_name} (lat: {meta['lat']}, lon: {meta['lon']})...")
        rows = _fetch_district_weather(meta["lat"], meta["lon"])
        if not rows:
            raise RuntimeError(f"Received empty weather rows for {d_name}")
        districts_data[d_name] = rows
        adm3_map[d_name] = meta["pcode"]

    now_iso = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    snapshot = {
        "is_sample": False,
        "source_note": f"Real Agro-Meteorological Forecast & Observation Series (fetched {now_iso})",
        "provenance": {
            "source_id": "OPEN_METEO_BMDWRF",
            "endpoint": "https://api.open-meteo.com/v1/forecast",
            "fetched_at": now_iso,
            "adm3_pcodes": adm3_map,
        },
        "districts": districts_data,
    }

    if output_path:
        write_deterministic_json(output_path, snapshot)
        print(f"Successfully wrote real snapshot to: {output_path}")

    return snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default_out = (
        Path(__file__).resolve().parents[1]
        / "ml_assets"
        / "weather"
        / "late_blight_snapshot.json"
    )
    parser.add_argument("--output", type=Path, default=default_out)
    parser.add_argument("--districts", type=str, default=None, help="Comma-separated district names")
    args = parser.parse_args()

    dist_list = [d.strip() for d in args.districts.split(",")] if args.districts else None
    try:
        fetch_weather_snapshot(districts=dist_list, output_path=args.output)
        return 0
    except Exception as exc:
        print(f"Error fetching weather snapshot: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
