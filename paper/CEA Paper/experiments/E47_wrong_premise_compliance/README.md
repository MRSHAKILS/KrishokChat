# Wrong-Premise Compliance Test

**Experiment ID:** E47
**RQ:** RQ1
**Tier:** 3
**Status:** planned
**Venue:** CEA journal (NOT EACL Demo)

## Summary

200 cases where farmers present plausible but incorrect diagnosis premises. Measures Premise Correction Rate (PCR) and Unsafe Compliance Rate (UCR).

## Methods

5 wrong-premise classes x 40 cases = 200 cases

## Key Claim

BAA challenges incorrect premises; B0 complies with wrong premises.

## Files

- Spec: `experiments/specs/E47_wrong_premise_compliance.spec.yaml`
- Runner: `experiments/scripts/E47_wrong_premise_compliance/` (to be implemented)
- Results: `experiments/results/E47_wrong_premise_compliance/` (frozen after run)
- Paper: This directory — freeze outputs here after acceptance

## Implementation Priority

See `experiments/specs/E47_wrong_premise_compliance.spec.yaml` for full design, metrics, acceptance gates, and implementation notes.

## Acceptance Protocol

Follow `experiments/ACCEPTANCE_PROTOCOL.md`:
1. Run script
2. Verify outputs
3. Real-application check
4. Freeze YAML
5. Update registry.yaml
