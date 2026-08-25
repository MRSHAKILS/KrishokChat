"""R9: Build offline fact packs and manifest for zero-signal client-side resolution.

Reads backend/ml_assets/rag_index/derived/fact_base_v1.json and
backend/ml_assets/agronomy/crop_calendars_v1.json to emit compact per-crop JSON
packs into frontend/public/packs/:
  - facts_potato_v1.json
  - facts_maize_v1.json
  - facts_rice_v1.json
  - manifest.json
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.infrastructure.ingestion.contract import sha256_of, write_deterministic_json

logger = logging.getLogger("krishokchat.pack_builder")

DEFAULT_FACT_BASE = (
    Path(__file__).resolve().parents[1]
    / "ml_assets"
    / "rag_index"
    / "derived"
    / "fact_base_v1.json"
)
DEFAULT_CALENDARS = (
    Path(__file__).resolve().parents[1]
    / "ml_assets"
    / "agronomy"
    / "crop_calendars_v1.json"
)
DEFAULT_OUTPUT_DIR = (
    Path(__file__).resolve().parents[2]
    / "frontend"
    / "public"
    / "packs"
)


def build_packs(
    fact_base_path: Path,
    calendars_path: Path,
    output_dir: Path,
) -> dict[str, Any]:
    """Generate per-crop fact packs and manifest."""
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(fact_base_path, encoding="utf-8") as fh:
        fb_data = json.load(fh)

    with open(calendars_path, encoding="utf-8") as fh:
        cal_data = json.load(fh)

    facts = fb_data.get("facts", [])
    fb_version = fb_data.get("version", 1)
    calendars_list = cal_data.get("calendars", [])
    calendars = {c["key"]: c for c in calendars_list if isinstance(c, dict) and "key" in c}

    # Group facts by crop
    crops: dict[str, list[dict[str, Any]]] = {}
    for fact in facts:
        crop_key = fact.get("crop", "").lower().strip()
        if not crop_key:
            continue
        crops.setdefault(crop_key, []).append(fact)

    now_iso = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    manifest_packs: list[dict[str, Any]] = []

    print(f"Building fact packs for {len(crops)} crops -> {output_dir}")

    for crop_name, crop_facts in sorted(crops.items()):
        pack_filename = f"facts_{crop_name}_v{fb_version}.json"
        pack_path = output_dir / pack_filename

        crop_calendar = calendars.get(crop_name, {})

        pack_payload = {
            "crop": crop_name,
            "pack_version": fb_version,
            "built_at": now_iso,
            "source": f"BARI/BRRI/DAE curated fact base v{fb_version}",
            "calendar": crop_calendar,
            "facts": crop_facts,
        }

        digest = write_deterministic_json(pack_path, pack_payload)
        size_bytes = pack_path.stat().st_size

        manifest_packs.append({
            "crop": crop_name,
            "version": fb_version,
            "filename": pack_filename,
            "path": f"/packs/{pack_filename}",
            "facts_count": len(crop_facts),
            "size_bytes": size_bytes,
            "sha256": digest,
            "built_at": now_iso,
        })
        print(f"  [{crop_name}] wrote {len(crop_facts)} facts -> {pack_filename} ({size_bytes} B, sha256: {digest[:12]}…)")

    # Build manifest
    manifest_payload = {
        "schema_version": 1,
        "updated_at": now_iso,
        "packs": manifest_packs,
    }
    manifest_path = output_dir / "manifest.json"
    manifest_digest = write_deterministic_json(manifest_path, manifest_payload)
    print(f"Wrote manifest -> manifest.json (sha256: {manifest_digest[:12]}…)")

    return manifest_payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fact-base", type=Path, default=DEFAULT_FACT_BASE)
    parser.add_argument("--calendars", type=Path, default=DEFAULT_CALENDARS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    try:
        build_packs(args.fact_base, args.calendars, args.output_dir)
        return 0
    except Exception as exc:
        print(f"Error building fact packs: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
