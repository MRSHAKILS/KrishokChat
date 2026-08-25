"""P2: generic, data-driven crop-stage calculator (pure domain).

Operates on the artifact dict produced by ``scripts/build_crop_calendars.py``
(see ``ml_assets/agronomy/crop_calendars_v1.json``). No crop is hardcoded:
supported crops, stage windows, advisory hints, and grounding badges all come
from the data — adding a crop means editing the curated JSON and rebuilding,
never touching this module.

Deterministic: given (artifact, crop, sowing date, today) the result is fixed.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class StageResult:
    crop_key: str
    crop_name_bn: str
    stage_key: str
    stage_name_bn: str
    das: int  # days after sowing
    start_das: int
    end_das: int
    advisory_bn: str
    grounding: str
    source: str
    season_note_bn: str

    @property
    def is_approximate(self) -> bool:
        return self.grounding != "corpus-extracted"

    @property
    def farmer_context_bn(self) -> str:
        """One-line context for the QA pipeline / UI cards."""
        return (
            f"ফসল: {self.crop_name_bn} · বর্তমান পর্যায়: {self.stage_name_bn} "
            f"(বপন/রোপণের {self.das} তম দিন) · পর্যায়-নির্দেশনা: {self.advisory_bn}"
        )


def _parse_date(value: str) -> date | None:
    try:
        return date.fromisoformat(str(value)[:10])
    except (ValueError, TypeError):
        return None


class CropCalendarLibrary:
    """Parsed view over the crop-calendars artifact."""

    def __init__(self, artifact: dict) -> None:
        self.version = int(artifact.get("version", 1))
        self._crops: dict[str, dict] = {
            str(crop.get("key")): crop for crop in artifact.get("crops", []) if crop.get("key")
        }
        self._by_alias: dict[str, str] = {}
        for key, crop in self._crops.items():
            self._by_alias[key.lower()] = key
            for alias in list(crop.get("aliases_bn") or []) + list(crop.get("aliases_en") or []):
                self._by_alias[str(alias).lower()] = key
        self.pending_crops = dict(artifact.get("pending_crops") or {})

    @property
    def supported_crops(self) -> list[dict[str, str]]:
        """Crop list for UI selectors (stable order by key)."""
        return [
            {"key": key, "name_bn": crop.get("name_bn", key)}
            for key, crop in sorted(self._crops.items())
        ]

    def resolve_crop(self, value: str | None) -> str | None:
        if not value:
            return None
        return self._by_alias.get(str(value).strip().lower())

    def compute_stage(
        self, crop: str, sowing_date: str | date, today: str | date | None = None
    ) -> StageResult | None:
        """Current stage for a crop + sowing date; None when unresolvable."""
        crop_key = self.resolve_crop(crop)
        if crop_key is None:
            return None
        sown = sowing_date if isinstance(sowing_date, date) else _parse_date(sowing_date)
        now = today if isinstance(today, date) or today is None else _parse_date(today)
        if sown is None or (now is not None and now < sown):
            return None
        das = ((now or date.today()) - sown).days
        crop_data = self._crops[crop_key]
        stages = sorted(crop_data.get("stages") or [], key=lambda s: int(s.get("start_das", 0)))
        stage = next((s for s in stages if int(s.get("start_das", 0)) <= das < int(s.get("end_das", 0))), None)
        if stage is None:
            # Past the final window: report the final stage (harvest-ready).
            if stages and das >= int(stages[-1].get("start_das", 0)):
                stage = stages[-1]
            else:
                return None
        return StageResult(
            crop_key=crop_key,
            crop_name_bn=str(crop_data.get("name_bn", crop_key)),
            stage_key=str(stage.get("key", "")),
            stage_name_bn=str(stage.get("name_bn", "")),
            das=das,
            start_das=int(stage.get("start_das", 0)),
            end_das=int(stage.get("end_das", 0)),
            advisory_bn=str(stage.get("advisory_bn", "")),
            grounding=str(stage.get("grounding", "")),
            source=str(stage.get("source", "")),
            season_note_bn=str(crop_data.get("season_note_bn", "")),
        )
