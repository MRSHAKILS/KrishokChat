#!/usr/bin/env python3
"""Fetch or verify KrishokTech model artifacts from Hugging Face.

    python backend/scripts/fetch_models.py --check        # compare local files, download nothing
    python backend/scripts/fetch_models.py vision         # restore missing/corrupt vision weights
    python backend/scripts/fetch_models.py llm            # krishokchat.f16.gguf (~1.3 GB)
    python backend/scripts/fetch_models.py all

Standard library only. Files are verified by size and, for LFS files, SHA-256 taken
from the Hugging Face tree API, and written via a .part file so an interrupted
download never leaves a truncated model in place.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

REPO = "RaiyanKhaan/KrishokTech-Models"
REVISION = "main"
ROOT = Path(__file__).resolve().parents[2]
ML_ASSETS = ROOT / "backend" / "ml_assets"

CROPS = {
    "01_crop_classifier": ("crop_classifier", "crop_classifier.pt", ("class_names.json",)),
    "02_potato_disease": ("potato_disease", "potato_disease.pt", ("class_names.json", "disease_details.json")),
    "03_rice_disease": ("rice_disease", "rice_disease.pt", ("class_names.json", "disease_details.json")),
    "04_wheat_disease": ("wheat_disease", "wheat_disease.pt", ("class_names.json", "disease_details.json", "metadata.json")),
    "05_corn_disease": ("corn_disease", "corn_disease.pt", ("class_names.json", "disease_details.json")),
    "06_chilli_disease": ("chilli_disease", "chilli_disease.pt", ("class_names.json", "disease_details.json")),
    "07_brassica_disease": ("brassica_disease", "brassica_disease.pt", ("class_names.json", "disease_details.json")),
}


def targets(group: str) -> dict[str, Path]:
    """Map remote path -> local path for a group ('vision' or 'llm')."""
    out: dict[str, Path] = {}
    if group == "vision":
        for remote_dir, (local_dir, weights, extras) in CROPS.items():
            base = ML_ASSETS / "vision" / local_dir
            out[f"{remote_dir}/{weights}"] = base / "model.pt"
            for name in extras:
                out[f"{remote_dir}/{name}"] = base / name
    elif group == "llm":
        out["krishokchat.f16.gguf"] = ML_ASSETS / "gemma" / "model.gguf"
    return out


def remote_index() -> dict[str, dict]:
    url = f"https://huggingface.co/api/models/{REPO}/tree/{REVISION}?recursive=true"
    with urllib.request.urlopen(url, timeout=60) as resp:
        return {e["path"]: e for e in json.load(resp) if e.get("type") == "file"}


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def status(local: Path, entry: dict) -> str:
    if not local.exists():
        return "missing"
    oid = (entry.get("lfs") or {}).get("oid")
    if oid is None:
        # Small text sidecars are plain git blobs. Compare git blob SHA-1 of the raw
        # file and of its LF-normalised form, since Windows checkouts rewrite
        # line endings.
        data = local.read_bytes()
        for candidate in (data, data.replace(b"\r\n", b"\n")):
            blob = hashlib.sha1(b"blob %d\0" % len(candidate) + candidate).hexdigest()
            if blob == entry["oid"]:
                return "ok"
        return "content-mismatch"
    if local.stat().st_size != entry["size"]:
        return "size-mismatch"
    return "ok" if sha256_of(local) == oid else "hash-mismatch"


def download(remote: str, local: Path, entry: dict) -> None:
    url = f"https://huggingface.co/{REPO}/resolve/{REVISION}/{remote}"
    local.parent.mkdir(parents=True, exist_ok=True)
    part = local.with_suffix(local.suffix + ".part")
    done = 0
    with urllib.request.urlopen(url, timeout=60) as resp, part.open("wb") as fh:
        while chunk := resp.read(1 << 20):
            fh.write(chunk)
            done += len(chunk)
            print(f"\r  {remote}: {done / 1e6:8.1f} / {entry['size'] / 1e6:.1f} MB", end="", flush=True)
    print()
    part.replace(local)
    if status(local, entry) != "ok":
        local.unlink(missing_ok=True)
        raise SystemExit(f"verification failed after download: {remote}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("group", nargs="?", choices=["vision", "llm", "all"], default="vision")
    parser.add_argument("--check", action="store_true", help="report status only, download nothing")
    args = parser.parse_args()

    index = remote_index()
    wanted: dict[str, Path] = {}
    for group in ("vision", "llm") if args.group == "all" else (args.group,):
        wanted.update(targets(group))

    bad = 0
    for remote, local in wanted.items():
        entry = index.get(remote)
        if entry is None:
            print(f"NOT-ON-HUB     {remote}")
            bad += 1
            continue
        state = status(local, entry)
        print(f"{state:<14} {remote} -> {local.relative_to(ROOT)}")
        if state != "ok":
            bad += 1
            if not args.check:
                download(remote, local, entry)
    if args.check:
        return 1 if bad else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
