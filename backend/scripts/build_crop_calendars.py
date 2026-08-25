"""P2 offline builder: merge curated + corpus-extracted crop calendars.

Deterministic (sorted output, no timestamps) so the committed artifact is
reviewable diff-by-diff. Extensibility contract:

- Researchers add crops by editing ``curated_calendars_v1.json`` (each stage
  carries ``source`` + ``grounding``) and re-running this script. No code
  changes are ever needed to widen crop coverage.
- The corpus extractor scans Bengali content for harvest/maturity windows
  ("বপন/রোপণের N থেকে M দিন ... সংগ্রহ/পরিপক্ব") against each crop's aliases.
  Hits (a) sharpen the crop's final stage (end_das = max window day, source =
  the corpus citation, grounding = corpus-extracted) and (b) are recorded in
  the artifact's ``evidence`` list. Crops seen in the corpus but NOT curated
  land in ``pending_crops`` — visible TODOs, never silently dropped.

    uv run python scripts/build_crop_calendars.py [--curated PATH] [--corpus PATH] [--output PATH] [--print]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

DEFAULTS = {
    "curated": Path(__file__).resolve().parents[1] / "ml_assets" / "agronomy" / "curated_calendars_v1.json",
    "corpus": Path(__file__).resolve().parents[1] / "ml_assets" / "rag_index" / "processed" / "knowledge_nodes_clean.jsonl",
    "output": Path(__file__).resolve().parents[1] / "ml_assets" / "agronomy" / "crop_calendars_v1.json",
}

_BN_DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")

# "বপন/রোপণের ৮০ থেকে ৯০ দিন পর ... সংগ্রহ/পরিপক্ব" (also "৮০-৯০ দিন")
_WINDOW_RE = re.compile(
    r"(?:বপন|রোপণ)[^\n।]{0,40}?(\d+)\s*(?:থেকে|\-|–|—)\s*(\d+)\s*দিন[^\n।]{0,60}?(সংগ্রহ|পরিপক্ব|কাটা|পাকা)",
)

# Common Bengali crop words beyond the curated set. A harvest window binding
# to one of these lands in pending_crops (honest TODO) instead of stealing a
# curated crop's slot — garlic's 140-160 day window must not become rice's.
EXTRA_CROP_WORDS: dict[str, list[str]] = {
    "garlic": ["রসুন"], "onion": ["পেঁয়াজ"], "wheat": ["গম"], "maize": ["ভুট্টা"],
    "chilli": ["মরিচ"], "tomato": ["টমেটো"], "brinjal": ["বেগুন"],
    "mustard": ["সরিষা"], "jute": ["পাট"], "sugarcane": ["আখ"],
}


def _word_positions(text: str, alias: str) -> list[int]:
    """Positions of alias NOT glued inside a longer Bengali word.

    Bengali has no word boundaries, but a Bengali letter immediately BEFORE
    the alias means it is a substring (ধান ⊂ প্রধান). Right-side suffixes
    (ধানের, ধানক্ষেত) are legitimate inflections and stay valid.
    """
    return [m.start() for m in re.finditer(rf"(?<![\u0980-\u09FF]){re.escape(alias)}", text)]


def _norm(text: str) -> str:
    return unicodedata.normalize("NFKC", text).translate(_BN_DIGITS)


def extract_harvest_windows(corpus_path: Path, aliases_by_crop: dict[str, list[str]]) -> list[dict]:
    """Scan corpus BN content for per-crop harvest windows with citations."""
    hits: list[dict] = []
    seen: set[tuple[str, int, int, str]] = set()
    with open(corpus_path, encoding="utf-8") as fh:
        for line in fh:
            node = json.loads(line)
            citation = str(node.get("citation") or node.get("source_document") or "")[:140]
            text = _norm(node.get("content_bn") or "")
            if not text:
                continue
            present: list[tuple[str, int]] = []
            vocab = {**{k: list(v) for k, v in aliases_by_crop.items()}, **EXTRA_CROP_WORDS}
            for key, words in vocab.items():
                for word in words:
                    for pos in _word_positions(text, word):
                        present.append((key, pos))
            if not present:
                continue
            for match in _WINDOW_RE.finditer(text):
                lo, hi = int(match.group(1)), int(match.group(2))
                if not (0 < lo < hi <= 400):
                    continue
                # Bind the crop whose word occurrence sits nearest the match
                # AND within a bounded window (node-level co-occurrence lets
                # a crop mentioned elsewhere steal another crop's line).
                near = [(key, pos) for key, pos in present if abs(pos - match.start()) <= 200]
                if not near:
                    continue
                key, _pos = min(near, key=lambda kp: abs(kp[1] - match.start()))
                dedup = (key, lo, hi, citation)
                if dedup in seen:
                    continue
                seen.add(dedup)
                snippet = " ".join(text[max(0, match.start() - 60) : match.end() + 30].split())[:170]
                hits.append(
                    {
                        "crop": key,
                        "min_das": lo,
                        "max_das": hi,
                        "citation": citation,
                        "snippet": snippet,
                    }
                )
    hits.sort(key=lambda h: (h["crop"], h["max_das"], h["citation"]))
    return hits


def build(calendars: dict, windows: list[dict]) -> dict:
    """Merge corpus windows into the curated crops; collect pending crops."""
    curated_crops = {crop["key"]: crop for crop in calendars.get("crops", [])}
    evidence: list[dict] = []
    pending: dict[str, list[dict]] = {}

    for win in windows:
        crop = curated_crops.get(win["crop"])
        if crop is None:
            win = {**win, "status": "pending-curation"}
            evidence.append(win)
            pending.setdefault(win["crop"], []).append(win)
            continue
        stages = crop.get("stages") or []
        if not stages:
            continue
        final = stages[-1]
        curated_end = int(final.get("end_das") or 0)
        # Divergence guard: a corpus window far outside the curated range is
        # recorded for human review but never applied — it is more likely a
        # misbinding or a different variety/practice than better data.
        if curated_end and win["max_das"] > curated_end * 1.5:
            evidence.append({**win, "status": "divergent-not-applied"})
            continue
        evidence.append({**win, "status": "applied"})
        # Corpus evidence wins over the curated approximation for maturity.
        final["end_das"] = max(curated_end, win["max_das"])
        final["source"] = win["citation"] or final.get("source", "")
        final["grounding"] = "corpus-extracted"
        final["corpus_window_das"] = [win["min_das"], win["max_das"]]

    output_crops = sorted(curated_crops.values(), key=lambda c: c["key"])
    return {
        "version": 1,
        "generator": "backend/scripts/build_crop_calendars.py",
        "notes": (
            "Data-driven crop-stage calendars. Sources: curated seed "
            "(curated_calendars_v1.json, human-editable) merged with "
            "corpus-extracted harvest windows. grounding=curated-approximation "
            "entries must be shown as approximate in user-facing UI."
        ),
        "evidence": sorted(evidence, key=lambda e: (e["crop"], e["max_das"], e["citation"], e["snippet"])),
        "pending_crops": {key: wins for key, wins in sorted(pending.items())},
        "crops": output_crops,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--curated", type=Path, default=DEFAULTS["curated"])
    parser.add_argument("--corpus", type=Path, default=DEFAULTS["corpus"])
    parser.add_argument("--output", type=Path, default=DEFAULTS["output"])
    parser.add_argument("--print", action="store_true")
    args = parser.parse_args()

    with open(args.curated, encoding="utf-8") as fh:
        calendars = json.load(fh)
    aliases = {
        crop["key"]: list(crop.get("aliases_bn") or []) + list(crop.get("aliases_en") or [])
        for crop in calendars.get("crops", [])
    }
    # Aliases of crops NOT yet curated still get recorded as pending when seen.
    windows = extract_harvest_windows(args.corpus, aliases)
    artifact = build(calendars, windows)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(artifact, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    print(f"crops: {[c['key'] for c in artifact['crops']]}")
    print(f"corpus windows merged: {len(artifact['evidence'])}; pending (un-curated) crops: {list(artifact['pending_crops'])}")
    print(f"wrote {args.output}")
    if args.print:
        for e in artifact["evidence"]:
            print(f"  [{e['crop']}] {e['min_das']}-{e['max_das']} DAS | {e['snippet'][:120]} | {e['citation'][:60]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
