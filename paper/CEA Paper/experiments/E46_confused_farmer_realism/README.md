# Confused Farmer Realism Benchmark

**Experiment ID:** E46
**RQ:** RQ1, RQ4
**Tier:** 2
**Status:** planned
**Venue:** CEA journal (NOT EACL Demo)

## Summary

Tests ACR and UCR on 800 imperfect queries across 8 corruption types: contradiction, missing info, wrong unit, stage mismatch, dialect, Banglish, false certainty, adversarial.

## Methods

8 types x 100 cases = 800 cases, evaluated by B0/B1/B4/B6

## Key Claim

BAA converts epistemic gaps to safe clarification rather than dangerous completion.

## Files

- Spec: `experiments/specs/E46_confused_farmer_realism.spec.yaml`
- Runner: `experiments/scripts/E46_confused_farmer_realism/` (to be implemented)
- Results: `experiments/results/E46_confused_farmer_realism/` (frozen after run)
- Paper: This directory — freeze outputs here after acceptance

## Implementation Priority

See `experiments/specs/E46_confused_farmer_realism.spec.yaml` for full design, metrics, acceptance gates, and implementation notes.

## Acceptance Protocol

Follow `experiments/ACCEPTANCE_PROTOCOL.md`:
1. Run script
2. Verify outputs
3. Real-application check
4. Freeze YAML
5. Update registry.yaml
