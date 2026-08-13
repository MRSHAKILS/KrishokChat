#!/usr/bin/env python3
"""T15 structured verifier runner — offline predictions on frozen splits.

Identical frame to the T12 lexical runner (same frozen splits, same evidence
mode: each record's own generating source passage) so T17 can compare the two
candidates directly on the identical (answer, evidence) pairs.

Verdicts carry the same confidence enum strings as the lexical baseline
(verified | flagged-unverified | low_confidence) plus per-claim structured
traces: relation, field trace, reasons, risk tier, evidence spans, parse failures.

The candidate is NEW research code under
backend/app/infrastructure/verification/{normalization,claim_parser,
relation_matcher,structured}.py; the runtime pipeline and dosage.py are NOT
modified or imported by the pipeline.

Usage:
  python research_artifacts/scripts/run_structured_verifier.py
Outputs (under research_artifacts/):
  runs/T15_structured_predictions_v1.jsonl
  runs/T15_failure_log_v1.jsonl
  manifests/T15_structured_run_manifest_v1.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
TOOL_VERSION = "run_structured_verifier.py v1"


def find_backend() -> Path | None:
    p = SCRIPT_DIR
    for _ in range(6):
        if (p / "backend" / "app" / "infrastructure" / "verification" / "dosage.py").exists():
            return p / "backend"
        p = p.parent
    return None


BACKEND = find_backend()
if BACKEND is None:
    print("error: backend/ not located from " + str(SCRIPT_DIR), file=sys.stderr)
    sys.exit(2)
sys.path.insert(0, str(BACKEND))

from app.domain.contracts import RetrievedSource  # noqa: E402
from app.infrastructure.verification.structured import StructuredVerifier  # noqa: E402

ARTIFACTS_ROOT = SCRIPT_DIR.parent
FROZEN_DIR = ARTIFACTS_ROOT / "datasets" / "frozen"
RUNS_DIR = ARTIFACTS_ROOT / "runs"
MANIFESTS_DIR = ARTIFACTS_ROOT / "manifests"
SPLIT_FILES = {
    "train": "T09_treatment_qa_train_v1.jsonl",
    "dev": "T09_treatment_qa_dev_v1.jsonl",
    "test": "T09_treatment_qa_test_v1.jsonl",
}
CANDIDATE_FILES = (
    "normalization.py", "claim_parser.py", "relation_matcher.py", "structured.py",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_head() -> tuple[str, bool]:
    try:
        root = SCRIPT_DIR.parent.parent.parent.parent.parent
        rev = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, cwd=root).strip()
        dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], text=True, cwd=root).strip())
        return rev, dirty
    except Exception:
        return "unknown", True


def load_jsonl(path: Path) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def read_passage(path: str | None) -> tuple[str | None, str, str | None, str | None]:
    if not path:
        return None, "missing", "no_source_md", "record has no source_md"
    p = Path(str(path))
    if not p.exists():
        return None, "missing", "missing_file", f"not found: {p}"
    try:
        return p.read_text(encoding="utf-8", errors="replace"), "attached", None, None
    except OSError as e:
        return None, "unreadable", type(e).__name__, str(e)


def main() -> int:
    ap = argparse.ArgumentParser(description="T15 structured verifier runner.")
    ap.add_argument("--frozen-dir", type=Path, default=FROZEN_DIR)
    ap.add_argument("--out-dir", type=Path, default=RUNS_DIR)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    verifier = StructuredVerifier()
    predictions: list[dict] = []
    failures: list[dict] = []
    cache: dict[str, str] = {}
    input_hashes: dict[str, str] = {}
    per_split_counts: dict[str, dict] = {}

    claim_dump: list[dict] = []  # per-claim structured traces (for T17 oracle/eval)

    for split, fname in SPLIT_FILES.items():
        split_path = args.frozen_dir / fname
        records = load_jsonl(split_path)
        input_hashes[fname] = sha256_file(split_path)
        counts = {"records": len(records), "verified": 0, "flagged_unverified": 0,
                  "low_confidence": 0, "claims": 0, "certifiable_claims": 0,
                  "attached": 0, "missing": 0}
        per_split_counts[split] = counts

        for idx, rec in enumerate(records):
            smd = rec.get("source_md")
            body, status, err_type, err_msg = (None, "missing", "no_source_md", "no source_md") if not smd else read_passage(str(smd))
            evidence_hash = None
            sources: list[RetrievedSource] = []
            if status == "attached":
                if str(smd) not in cache:
                    cache[str(smd)] = body
                content = cache[str(smd)]
                evidence_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
                sources = [RetrievedSource(id=str(rec.get("source_document") or "unknown"),
                                           score=0.0, content_bn=content)]
                counts["attached"] += 1
            else:
                counts["missing"] += 1
                failures.append({"split": split, "record_idx": idx, "t09_cell": rec.get("t09_group"),
                                 "source_md": str(smd or ""), "status": status,
                                 "error_type": err_type, "error": err_msg or ""})

            try:
                result = verifier.verify(rec.get("answer") or "", sources,
                                         source_ids=(rec.get("source_document") or "unknown",))
            except Exception:
                failures.append({"split": split, "record_idx": idx, "t09_cell": rec.get("t09_group"),
                                 "status": "exception", "error_type": "Exception",
                                 "error": traceback.format_exc(limit=5)})
                continue

            counts[result.confidence.replace("-", "_")] = counts.get(result.confidence.replace("-", "_"), 0) + 1
            counts["claims"] += len(result.claims)
            counts["certifiable_claims"] += sum(1 for c in result.claims if c.certifiable)

            predictions.append({
                "split": split, "record_idx": idx, "t09_cell": rec.get("t09_group"),
                "question": rec.get("question"), "answer": rec.get("answer"),
                "confidence": result.confidence,
                "flags": list(result.flags),
                "unverified_claims": list(result.unverified_claims),
                "claim_ids": [c.claim_id for c in result.claims],
                "parse_failures": list(result.parse_failures),
                "evidence_status": status,
                "evidence_hash": evidence_hash,
            })
            for c in result.claims:
                claim_dump.append({
                    "split": split, "record_idx": idx, "t09_cell": rec.get("t09_group"),
                    "claim_id": c.claim_id, "text": c.text, "relation": c.relation,
                    "certifiable": c.certifiable, "risk_tier": c.risk_tier,
                    "safety_critical": c.safety_critical, "reasons": list(c.reasons),
                    "field_trace": list(c.field_trace),
                    "evidence_spans": [{"source_id": s.source_id, "text": s.text,
                                        "start": s.start, "end": s.end}
                                       for s in c.evidence_spans],
                })

    run_id = f"T15-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}"
    pred_path = args.out_dir / "T15_structured_predictions_v1.jsonl"
    fail_path = args.out_dir / "T15_failure_log_v1.jsonl"
    claims_path = args.out_dir / "T15_structured_claims_v1.jsonl"
    with open(pred_path, "w", encoding="utf-8") as f:
        for p in predictions:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    with open(fail_path, "w", encoding="utf-8") as f:
        for p in failures:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    with open(claims_path, "w", encoding="utf-8") as f:
        for p in claim_dump:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")

    rev, dirty = git_head()
    ver_dir = BACKEND / "app" / "infrastructure" / "verification"
    code_hashes = {f: sha256_file(ver_dir / f) for f in CANDIDATE_FILES}
    code_hashes["runner"] = sha256_file(__file__)
    manifest = {
        "manifest_version": "1",
        "tool": TOOL_VERSION,
        "run_id": run_id,
        "task": "T15 structured verifier candidate",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "git": {"revision": rev, "dirty_tree": dirty},
        "inputs": {"splits": input_hashes,
                   "split_manifest": sha256_file(args.frozen_dir / "T09_split_manifest_v1.json")},
        "code_hashes": code_hashes,
        "method": ("StructuredVerifier.verify(answer, [RetrievedSource(content_bn=passage)]) "
                   "per frozen record; parser+normalizer+relation matcher+fail-closed policy; "
                   "candidate is dead code w.r.t. the runtime pipeline (dosage.py untouched)"),
        "evidence_mode": "record's generating source passage (source_md), full content; matches T12",
        "determinism": "deterministic; record order follows frozen split order",
        "seed": None, "thresholds": None,
        "per_split_counts": per_split_counts,
        "outputs": {
            "predictions": {"path": str(pred_path), "records": len(predictions), "sha256": sha256_file(pred_path)},
            "failure_log": {"path": str(fail_path), "records": len(failures), "sha256": sha256_file(fail_path)},
            "claims": {"path": str(claims_path), "records": len(claim_dump), "sha256": sha256_file(claims_path)},
        },
    }
    manifest_path = MANIFESTS_DIR / "T15_structured_run_manifest_v1.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"run_id: {run_id}  revision: {rev} dirty={dirty}")
    print(f"predictions: {len(predictions)}  failures: {len(failures)}  claims: {len(claim_dump)}")
    for split, c in per_split_counts.items():
        print(f"  {split}: records={c['records']} verified={c['verified']} flagged={c['flagged_unverified']} "
              f"low_conf={c['low_confidence']} claims={c['claims']} certifiable={c['certifiable_claims']} "
              f"evidence_attached={c['attached']} missing={c['missing']}")
    print(f"manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())