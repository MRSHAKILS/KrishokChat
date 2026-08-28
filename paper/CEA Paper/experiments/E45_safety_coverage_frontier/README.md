# Safety-CUAR Frontier (Coverage@CUAR<=X%)

**Experiment ID:** E45
**RQ:** RQ3
**Tier:** 2
**Status:** planned
**Venue:** CEA journal (NOT EACL Demo)

## Summary

Sweeps threshold theta across E04 precomputed corpus to produce a Pareto frontier of Coverage vs CUAR. No new API calls needed.

## Methods

101 threshold values on 20,112-case E04 corpus. Runtime < 5 min.

## Key Claim

Policymakers can select CUAR budget and read coverage implications.

## Files

- Spec: `experiments/specs/E45_safety_coverage_frontier.spec.yaml`
- Runner: `experiments/scripts/E45_safety_coverage_frontier/` (to be implemented)
- Results: `experiments/results/E45_safety_coverage_frontier/` (frozen after run)
- Paper: This directory — freeze outputs here after acceptance

## Implementation Priority

See `experiments/specs/E45_safety_coverage_frontier.spec.yaml` for full design, metrics, acceptance gates, and implementation notes.

## Acceptance Protocol

Follow `experiments/ACCEPTANCE_PROTOCOL.md`:
1. Run script
2. Verify outputs
3. Real-application check
4. Freeze YAML
5. Update registry.yaml
