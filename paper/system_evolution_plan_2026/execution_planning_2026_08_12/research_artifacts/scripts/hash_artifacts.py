#!/usr/bin/env python3
"""T09 hash tool — SHA-256 manifest for research artifacts.

Usage:
  python hash_artifacts.py <path> [<path> ...] -o manifest.json [--jsonl-line-count]

Accepts files and directories (recursive). Emits a JSON manifest:
  {"files": { "<relative path>": {"sha256": "...", "size_bytes": N, "lines": N|null} },
   "generated_at_utc": "...", "tool": "hash_artifacts.py v1"}

Deterministic: paths sorted, no mtimes. UTF-8 output.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def line_count(path: Path) -> int | None:
    if path.suffix.lower() not in (".jsonl", ".ndjson", ".csv", ".tsv"):
        return None
    n = 0
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for _ in f:
            n += 1
    return n


def collect(root: Path, items: list[Path]) -> list[Path]:
    out = []
    for p in items:
        if p.is_dir():
            out.extend(sorted(q for q in p.rglob("*") if q.is_file()))
        elif p.is_file():
            out.append(p)
    return sorted(out, key=lambda q: q.relative_to(root).as_posix())


def main() -> int:
    ap = argparse.ArgumentParser(description="SHA-256 manifest tool (T09).")
    ap.add_argument("paths", nargs="+", type=Path, help="files and/or directories")
    ap.add_argument("-o", "--out", type=Path, required=True, help="output manifest path")
    ap.add_argument("--root", type=Path, default=Path.cwd(), help="base for relative paths")
    ap.add_argument("--jsonl-line-count", action="store_true", help="include line counts for .jsonl/.csv")
    args = ap.parse_args()

    files = collect(args.root, args.paths)
    if not files:
        print("error: no files matched", file=sys.stderr)
        return 2

    manifest = {"files": {}, "generated_at_utc": datetime.now(timezone.utc).isoformat(),
                "tool": "hash_artifacts.py v1"}
    for p in files:
        rel = p.relative_to(args.root).as_posix()
        entry = {"sha256": sha256_file(p), "size_bytes": p.stat().st_size}
        if args.jsonl_line_count:
            entry["lines"] = line_count(p)
        manifest["files"][rel] = entry
        print(f"{rel}\t{entry['sha256']}\t{entry['size_bytes']}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"\nmanifest written: {args.out}  ({len(files)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
