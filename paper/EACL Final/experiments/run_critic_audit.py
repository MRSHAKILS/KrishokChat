import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
WORKSPACE_ROOT = Path(r"D:\KrishokChat Advisory System")

EXP_DIR = WORKSPACE_ROOT / "paper" / "EACL Final" / "experiments"
RESULTS_DIR = EXP_DIR / "results"

# Only N-track experiments (EACL Final new ones)
N_TRACK_SPECS = sorted(EXP_DIR.glob("N*/spec.yaml"))
GT_FILE = EXP_DIR / "ground_truth.yaml"


def load_yaml(path: Path):
    import yaml
    return yaml.safe_load(open(path, encoding="utf-8"))


def check_experiment(spec_path: Path) -> dict:
    spec = load_yaml(spec_path)
    exp_id = spec.get("id", "UNKNOWN")
    status = spec.get("status", "UNKNOWN")
    
    locked_results = spec_path.parent / "results.json"
    has_locked = locked_results.exists()
    
    # Check for any jsonl with this experiment ID
    jsonl_files = list(RESULTS_DIR.glob(f"*{exp_id.lower()}*"))
    has_jsonl = len(jsonl_files) > 0
    
    required = ["id", "title", "question", "status", "beats", "lane", "locked"]
    missing = [f for f in required if f not in spec]
    
    locked = spec.get("locked", {})
    has_key = "key" in locked
    
    return {
        "id": exp_id,
        "status": status,
        "has_locked_results": has_locked,
        "has_jsonl": has_jsonl,
        "missing_fields": missing,
        "has_key_metrics": has_key,
        "spec_path": str(spec_path.relative_to(WORKSPACE_ROOT)),
    }


def main() -> int:
    print("=" * 70)
    print("CRITIC AUDIT BATCH REPORT - EACL Final Track (N-track only)")
    print(f"Generated: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)
    
    gt = load_yaml(GT_FILE)
    gt_exps = gt.get("experiments", {})
    
    results = []
    for spec_path in N_TRACK_SPECS:
        r = check_experiment(spec_path)
        results.append(r)
    
    print(f"\nTotal N-track spec.yaml files: {len(results)}")
    print(f"Ground truth N-track experiments: {len([k for k in gt_exps if k.startswith('N')])}")
    
    from collections import Counter
    status_counts = Counter(r["status"] for r in results)
    print(f"\nStatus breakdown:")
    for s, c in sorted(status_counts.items()):
        print(f"  {s}: {c}")
    
    issues = []
    for r in results:
        if r["missing_fields"]:
            issues.append(f"{r['id']}: missing fields {r['missing_fields']}")
        if not r["has_locked_results"]:
            issues.append(f"{r['id']}: NO locked results.json")
        if not r["has_jsonl"]:
            issues.append(f"{r['id']}: NO results.jsonl in results dir")
        if not r["has_key_metrics"]:
            issues.append(f"{r['id']}: NO key metrics in locked section")
    
    spec_ids = {r["id"] for r in results}
    gt_ids = {k for k in gt_exps if k.startswith('N')}
    in_spec_not_gt = spec_ids - gt_ids
    in_gt_not_spec = gt_ids - spec_ids
    if in_spec_not_gt:
        issues.append(f"In spec but not ground_truth: {in_spec_not_gt}")
    if in_gt_not_spec:
        issues.append(f"In ground_truth but not spec: {in_gt_not_spec}")
    
    print(f"\nIssues found: {len(issues)}")
    for issue in issues:
        print(f"  - {issue}")
    
    if not issues:
        print("\nALL CHECKS PASSED - Ready for paper submission")
    else:
        print(f"\n{len(issues)} issues need attention")
    
    print("\n" + "=" * 70)
    print("DETAILED N-TRACK EXPERIMENT STATUS")
    print("=" * 70)
    print(f"{'ID':<25} {'Status':<35} {'Locked':<7} {'JSONL':<6} {'Key':<4} {'Issues'}")
    print("-" * 70)
    for r in sorted(results, key=lambda x: x["id"]):
        issues_str = "; ".join([
            f"missing:{len(r['missing_fields'])}" if r["missing_fields"] else "",
            "no-locked" if not r["has_locked_results"] else "",
            "no-jsonl" if not r["has_jsonl"] else "",
            "no-key" if not r["has_key_metrics"] else "",
        ]).strip("; ")
        print(f"{r['id']:<25} {r['status']:<35} {'OK' if r['has_locked_results'] else 'MISSING':<7} {'OK' if r['has_jsonl'] else 'MISSING':<6} {'OK' if r['has_key_metrics'] else 'MISSING':<4} {issues_str}")
    
    report = {
        "audit_name": "EACL_FINAL_CRITIC_AUDIT_NTRACK",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_experiments": len(results),
        "status_breakdown": dict(status_counts),
        "issues": issues,
        "experiments": results,
        "ground_truth_count": len(gt_ids),
        "spec_count": len(spec_ids),
        "all_good": len(issues) == 0,
    }
    
    out_path = EXP_DIR / f"critic_audit_report_n_track_{datetime.now(timezone.utc).strftime('%Y%m%d')}.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\n[OK] Report written to {out_path}")
    
    return 0 if len(issues) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())