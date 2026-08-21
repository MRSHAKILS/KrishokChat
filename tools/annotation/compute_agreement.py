"""Stage A3/A4 gate tool: inter-annotator agreement for two annotators.

AUTHORITY RULE (fixed 2026-08-22): the gate number is Krippendorff's nominal
alpha computed ONLY by the maintained `krippendorff` reference package. This
script implements no alpha math itself. Run through uv's ephemeral environment
so nothing is installed permanently:

    uv run --with krippendorff python tools/annotation/compute_agreement.py \
        --a research_artifacts/annotations/labels/pilot_annotator_A.jsonl \
        --b research_artifacts/annotations/labels/pilot_annotator_B.jsonl

ORIENTATION CONTRACT (cost us an afternoon — do not regress):
the package expects reliability_data shaped (M raters, N units) — one ROW per
annotator. Passing per-unit pairs [[a_1,b_1],[a_2,b_2],...] silently transposes
the matrix: perfect agreement scores -0.5 and every number is garbage. The
selftest pins both orientations of the worked example so this cannot return.

Without the package the tool still reports percent agreement and Scott's pi,
but those are INFORMATIONAL ONLY and can never pass the protocol gate
(annotation protocol v1 requires alpha >= 0.70 computed by the reference
implementation). Use --allow-fallback only for dry-run sanity checks.

Exit codes: 0 gate PASS, 1 gate FAIL, 2 reference package unavailable.

Selftest:
    uv run --with krippendorff python tools/annotation/compute_agreement.py --selftest
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

# Recorded from krippendorff 0.8.2 on 2026-08-22, CORRECT orientation,
# A=[x,x,y,y], B=[x,y,x,x]. Independently confirmed by hand coincidence
# matrix: D_o = 3/4, D_e = 15/28, alpha = 1 - (3/4)/(15/28) = -2/5 exactly.
# Note alpha != Scott's pi (-0.6 here); the two coefficients are different.
WORKED_SET_ALPHA = -0.40000000000000013
# Same data transposed to units-x-raters — kept as an orientation tripwire.
WORKED_SET_TRANSPOSED = -0.08888888888888889


def read_labels(path: Path, label_field: str) -> dict[str, str]:
    labels: dict[str, str] = {}
    with open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            item_id = row.get("item_id")
            value = row.get(label_field)
            if item_id is None or value is None:
                raise SystemExit(f"{path}:{lineno}: missing item_id or '{label_field}'")
            labels[str(item_id)] = str(value)
    return labels


def scotts_pi_informational(a: list[str], b: list[str]) -> float:
    """Scott's pi, INFORMATIONAL ONLY — not the protocol metric.

    Hand-checkable: A=[x,x,y,y], B=[x,y,x,x]:
    P_o=0.25; pooled marginals x=5/8, y=3/8; P_e=34/64;
    pi=(0.25-0.53125)/(1-0.53125)=-0.6 exactly."""
    n = len(a)
    if n <= 1:
        return 1.0
    p_o = sum(1 for x, y in zip(a, b) if x == y) / n
    pooled = Counter(a) + Counter(b)
    total = sum(pooled.values())
    p_e = sum((c / total) ** 2 for c in pooled.values())
    if p_e == 1.0:
        return 1.0
    return (p_o - p_e) / (1.0 - p_e)


def encode(a: list[str], b: list[str]) -> tuple[dict[str, int], list[int], list[int]]:
    vocabulary: dict[str, int] = {}
    for v in [*a, *b]:
        vocabulary.setdefault(v, len(vocabulary))
    return vocabulary, [vocabulary[v] for v in a], [vocabulary[v] for v in b]


def reference_alpha(a: list[str], b: list[str]) -> float | None:
    """Krippendorff nominal alpha via the reference package, else None.

    Builds (M raters, N units) rows — one row PER ANNOTATOR — per the
    package contract. See ORIENTATION CONTRACT in the module docstring.
    """
    try:
        import krippendorff  # type: ignore
    except ImportError:
        return None
    _vocab, enc_a, enc_b = encode(a, b)
    return float(krippendorff.alpha(reliability_data=[enc_a, enc_b], level_of_measurement="nominal"))


def report(labels_a: dict[str, str], labels_b: dict[str, str], gate: float, allow_fallback: bool) -> int:
    only_a = sorted(set(labels_a) - set(labels_b))
    only_b = sorted(set(labels_b) - set(labels_a))
    shared = sorted(set(labels_a) & set(labels_b))
    va = [labels_a[i] for i in shared]
    vb = [labels_b[i] for i in shared]
    agree = sum(1 for x, y in zip(va, vb) if x == y)

    print(f"shared items: {len(shared)}")
    if only_a:
        print(f"items only in A: {only_a}")
    if only_b:
        print(f"items only in B: {only_b}")
    print(f"percent agreement: {agree}/{len(shared)} = {agree / max(len(shared), 1):.4f}")
    print(f"scott's pi (informational only): {scotts_pi_informational(va, vb):.4f}")

    alpha = reference_alpha(va, vb)
    if alpha is None:
        print("krippendorff reference package NOT available.")
        print("Gate decisions require it. Rerun inside uv's ephemeral env:")
        print("  uv run --with krippendorff python tools/annotation/compute_agreement.py ...")
        if allow_fallback:
            proxy = scotts_pi_informational(va, vb)
            verdict = "PASS" if proxy >= gate else "FAIL"
            print(f"FALLBACK (--allow-fallback): gating on scott's pi {proxy:.4f} >= {gate}: {verdict}")
            print("WARNING: fallback number is NOT the protocol metric.")
            return 0 if proxy >= gate else 1
        return 2

    try:
        from importlib.metadata import version as _pkg_version

        pkg_version = _pkg_version("krippendorff")
    except Exception:
        pkg_version = "unknown"
    print(f"krippendorff reference alpha: {alpha:.4f} (package version {pkg_version})")

    confusions: Counter[tuple[str, str]] = Counter(zip(va, vb))
    disagreements = {(x, y): c for (x, y), c in confusions.items() if x != y}
    if disagreements:
        print("confusion counts (A_label -> B_label):")
        for (x, y), count in sorted(disagreements.items(), key=lambda kv: -kv[1]):
            print(f"  {x} -> {y}: {count}")
    verdict = "PASS" if alpha >= gate else "FAIL"
    print(f"gate (reference alpha >= {gate}): {verdict}")
    return 0 if alpha >= gate else 1


def selftest() -> int:
    # Informational pi keeps its hand-verifiable value regardless of package.
    assert abs(scotts_pi_informational(["x", "x", "y", "y"], ["x", "y", "x", "x"]) + 0.6) < 1e-12

    ref = reference_alpha(["x", "y"], ["x", "y"])
    if ref is None:
        print("krippendorff package absent; ran informational-pi checks only")
        print("selftest OK (limited)")
        return 0

    perfect = reference_alpha(["x", "y"], ["x", "y"])
    assert perfect == 1.0, f"perfect agreement must give alpha 1.0, got {perfect}"

    worked = reference_alpha(["x", "x", "y", "y"], ["x", "y", "x", "x"])
    assert abs(worked - WORKED_SET_ALPHA) < 1e-9, (
        f"correctly-oriented worked set drifted: {worked} vs {WORKED_SET_ALPHA}"
    )

    # Orientation tripwire: the SAME data fed units-first must reproduce the
    # historical wrong answer, proving we would notice another transpose.
    try:
        import krippendorff  # type: ignore

        _v, ea, eb = encode(["x", "x", "y", "y"], ["x", "y", "x", "x"])
        transposed = float(
            krippendorff.alpha(reliability_data=list(zip(ea, eb)), level_of_measurement="nominal")
        )
        assert abs(transposed - WORKED_SET_TRANSPOSED) < 1e-9, (
            f"transposed regression changed: {transposed} vs {WORKED_SET_TRANSPOSED}"
        )
    except ImportError:
        pass

    print(f"selftest OK: perfect={perfect}, worked={worked:.10f}, transposed-tripwire pinned")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--a", type=Path, help="annotator A labels (JSONL)")
    parser.add_argument("--b", type=Path, help="annotator B labels (JSONL)")
    parser.add_argument("--label-field", default="label")
    parser.add_argument("--gate", type=float, default=0.70)
    parser.add_argument("--allow-fallback", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if not args.a or not args.b:
        parser.error("--a and --b are required unless --selftest")
    return report(read_labels(args.a, args.label_field), read_labels(args.b, args.label_field), args.gate, args.allow_fallback)


if __name__ == "__main__":
    sys.exit(main())
