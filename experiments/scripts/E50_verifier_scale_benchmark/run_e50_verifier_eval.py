#!/usr/bin/env python3
"""
E50 — Verifier Scale Benchmark: Evaluation
===========================================
Step 2 of 2: Run HardenedDosageVerifier against all 528 generated cases.

For each record:
  - source passage → RetrievedSource
  - generated_advisory_bn → answer
  - verifier.verify(answer, [source]) → verdict

Expected:
  - Mutations (T1–T5): confidence == FLAGGED_UNVERIFIED
  - Clean (T0):        confidence == VERIFIED

Outputs:
  experiments/results/E50_verifier_scale_benchmark/e50_results.yaml
  experiments/results/E50_verifier_scale_benchmark/e50_per_record.jsonl
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(WORKSPACE / "backend"))

from app.domain.contracts import RetrievedSource
from app.application.verifier import HardenedDosageVerifier
from app.infrastructure.verification.dose_reference import DoseReference

RESULTS_DIR = WORKSPACE / "experiments" / "results" / "E50_verifier_scale_benchmark"
GEN_FILES = [
    RESULTS_DIR / "generated_A.jsonl",
    RESULTS_DIR / "generated_B.jsonl",
    RESULTS_DIR / "generated_C.jsonl",
]
OUT_RECORDS = RESULTS_DIR / "e50_per_record.jsonl"
OUT_RESULTS = RESULTS_DIR / "e50_results.yaml"


def wilson_ci(k: int, n: int) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    z = 1.959963984540054
    p = k / n
    denom = 1.0 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    margin = z * math.sqrt((p * (1 - p) / n) + z**2 / (4 * n**2)) / denom
    return (round(max(0.0, center - margin) * 100, 2), round(min(100.0, center + margin) * 100, 2))


def load_all_records() -> list[dict]:
    records: list[dict] = []
    for gf in GEN_FILES:
        if not gf.exists():
            print(f"WARNING: {gf.name} not found — skipping (run generator first)")
            continue
        for line in gf.read_text(encoding="utf-8").splitlines():
            try:
                records.append(json.loads(line))
            except Exception:
                pass
    return records


def make_source(record: dict) -> RetrievedSource:
    return RetrievedSource(
        id=record["passage_id"],
        score=1.0,
        title_en=record.get("title_en", ""),
        title_bn="",
        content_en=record.get("content_en", ""),
        content_bn=record.get("content_bn", ""),
        source=record.get("source_document", ""),
        citation=record.get("citation", ""),
    )


def main() -> None:
    print("E50 Verifier Evaluation", flush=True)
    print("=" * 60)

    records = load_all_records()
    if not records:
        print("ERROR: No generated records found. Run generate_advisories.py --worker A/B/C first.")
        sys.exit(1)
    print(f"Loaded {len(records)} generated records")

    # Check for missing worker files
    mutation_types = {"T1_overdose", "T2_underdose", "T3_chem_swap", "T4_unit_error", "T5_phi_hallucination", "T0_clean"}
    found_types = {r["mutation_type"] for r in records}
    missing = mutation_types - found_types
    if missing:
        print(f"WARNING: Missing mutation types in data: {missing}")

    verifier = HardenedDosageVerifier(dose_reference=DoseReference.disabled())

    # Per-type counters: caught = verifier flagged it as unsupported (correct for mutations)
    counters: dict[str, dict[str, int]] = {
        t: {"n": 0, "caught": 0, "no_dosage_claim": 0, "verified": 0} for t in mutation_types
    }
    total_checked = 0
    errors = 0

    # Clear output file
    OUT_RECORDS.write_text("", encoding="utf-8")

    for i, record in enumerate(records):
        advisory = record.get("generated_advisory_bn", "").strip()
        mut_type = record.get("mutation_type", "unknown")
        passage_id = record.get("passage_id", "?")

        if not advisory:
            print(f"  [{i+1}] SKIP (empty advisory): {passage_id} {mut_type}")
            errors += 1
            continue

        source = make_source(record)

        try:
            result = verifier.verify(advisory, [source])
        except Exception as e:
            print(f"  [{i+1}] VERIFIER ERROR: {e} — {passage_id} {mut_type}")
            errors += 1
            continue

        confidence = result.confidence.value if hasattr(result.confidence, "value") else str(result.confidence)
        checked = result.checked_count
        unsupported = result.unsupported_count
        grounded = result.grounded_count

        # Determine outcome
        is_flagged = unsupported > 0  # verifier detected something wrong
        is_no_dosage = checked == 0   # verifier found no measurable dosage claim at all
        is_verified = grounded > 0 and unsupported == 0 and not is_no_dosage

        if mut_type in counters:
            counters[mut_type]["n"] += 1
            if is_flagged:
                counters[mut_type]["caught"] += 1
            elif is_no_dosage:
                counters[mut_type]["no_dosage_claim"] += 1
            else:
                counters[mut_type]["verified"] += 1

        total_checked += 1

        out_record = {
            "passage_id": passage_id,
            "mutation_type": mut_type,
            "confidence": confidence,
            "checked_count": checked,
            "unsupported_count": unsupported,
            "grounded_count": grounded,
            "is_flagged": is_flagged,
            "is_no_dosage": is_no_dosage,
            "advisory_snippet": advisory[:120],
        }

        with open(OUT_RECORDS, "a", encoding="utf-8") as f:
            f.write(json.dumps(out_record, ensure_ascii=False) + "\n")
            f.flush()

        if (i + 1) % 50 == 0:
            print(f"  Progress: {i+1}/{len(records)}", flush=True)

    print(f"\nEvaluation complete. Total: {total_checked}, Errors: {errors}")
    print()

    # ---------------------------------------------------------------------------
    # Compute catch rates and CIs
    # ---------------------------------------------------------------------------
    print("=" * 60)
    print("RESULTS")
    print("=" * 60)

    yaml_lines = [
        f"experiment: E50_verifier_scale_benchmark",
        f"timestamp: {datetime.now(timezone.utc).isoformat()}",
        f"total_records: {total_checked}",
        f"total_errors: {errors}",
        "",
        "mutation_catch_rates:",
    ]

    mutation_order = ["T1_overdose", "T2_underdose", "T3_chem_swap", "T4_unit_error", "T5_phi_hallucination"]
    total_mutation_n = 0
    total_mutation_caught = 0

    for mut in mutation_order:
        c = counters[mut]
        n, caught = c["n"], c["caught"]
        no_dos = c["no_dosage_claim"]
        # catch rate denominator: cases where verifier found a claim to check
        effective_n = n - no_dos
        catch_rate = caught / effective_n if effective_n > 0 else 0.0
        lo, hi = wilson_ci(caught, effective_n) if effective_n > 0 else (0.0, 0.0)
        total_mutation_n += effective_n
        total_mutation_caught += caught

        print(f"  {mut}: {caught}/{effective_n} caught ({catch_rate*100:.1f}%) CI=[{lo:.1f},{hi:.1f}] | no_dosage_claim={no_dos}")
        yaml_lines += [
            f"  {mut}:",
            f"    n_total: {n}",
            f"    n_effective: {effective_n}",
            f"    caught: {caught}",
            f"    no_dosage_claim: {no_dos}",
            f"    catch_rate: {round(catch_rate, 4)}",
            f"    catch_pct: {round(catch_rate * 100, 2)}",
            f"    wilson_ci_95: [{lo}, {hi}]",
        ]

    # Overall mutation catch rate
    overall_rate = total_mutation_caught / total_mutation_n if total_mutation_n > 0 else 0.0
    overall_lo, overall_hi = wilson_ci(total_mutation_caught, total_mutation_n)
    print()
    print(f"  OVERALL MUTATIONS: {total_mutation_caught}/{total_mutation_n} caught ({overall_rate*100:.1f}%) CI=[{overall_lo:.1f},{overall_hi:.1f}]")
    yaml_lines += [
        "",
        "overall_mutation_catch_rate:",
        f"  n_effective: {total_mutation_n}",
        f"  caught: {total_mutation_caught}",
        f"  catch_rate: {round(overall_rate, 4)}",
        f"  catch_pct: {round(overall_rate * 100, 2)}",
        f"  wilson_ci_95: [{overall_lo}, {overall_hi}]",
    ]

    # Clean control: false positive rate
    c0 = counters["T0_clean"]
    n0, fp = c0["n"], c0["caught"]
    no_dos0 = c0["no_dosage_claim"]
    effective_n0 = n0 - no_dos0
    fp_rate = fp / effective_n0 if effective_n0 > 0 else 0.0
    fp_lo, fp_hi = wilson_ci(fp, effective_n0) if effective_n0 > 0 else (0.0, 0.0)
    print()
    print(f"  T0_clean (False Positive Rate): {fp}/{effective_n0} falsely flagged ({fp_rate*100:.1f}%) CI=[{fp_lo:.1f},{fp_hi:.1f}] | no_dosage={no_dos0}")
    yaml_lines += [
        "",
        "clean_control_false_positive_rate:",
        f"  n_total: {n0}",
        f"  n_effective: {effective_n0}",
        f"  falsely_flagged: {fp}",
        f"  no_dosage_claim: {no_dos0}",
        f"  fp_rate: {round(fp_rate, 4)}",
        f"  fp_pct: {round(fp_rate * 100, 2)}",
        f"  wilson_ci_95: [{fp_lo}, {fp_hi}]",
    ]

    OUT_RESULTS.write_text("\n".join(yaml_lines) + "\n", encoding="utf-8")
    print(f"\nResults written to: {OUT_RESULTS}")
    print(f"Per-record log:     {OUT_RECORDS}")


if __name__ == "__main__":
    main()
