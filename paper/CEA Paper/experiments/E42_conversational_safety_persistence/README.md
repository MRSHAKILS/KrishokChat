# Multi-Turn Conversational Safety Persistence

**Experiment ID:** E42
**RQ:** RQ1, RQ4
**Tier:** 1
**Status:** planned
**Venue:** CEA journal (NOT EACL Demo)

## Summary

Tests whether BAA maintains safety-critical slot values under 8 adversarial conversational pressure types across 200 multi-turn dialogue sequences.

## Methods

8 turn types x 25 scenarios x 5 turns = 1,000 adversarial turns

## Key Claim

CSP (Conversational Safety Persistence) for B6 >= 0.92 vs B0 <= 0.60

## Files

- Spec: `experiments/specs/E42_conversational_safety_persistence.spec.yaml`
- Runner: `experiments/scripts/E42_conversational_safety_persistence/` (to be implemented)
- Results: `experiments/results/E42_conversational_safety_persistence/` (frozen after run)
- Paper: This directory — freeze outputs here after acceptance

## Implementation Priority

See `experiments/specs/E42_conversational_safety_persistence.spec.yaml` for full design, metrics, acceptance gates, and implementation notes.

## Acceptance Protocol

Follow `experiments/ACCEPTANCE_PROTOCOL.md`:
1. Run script
2. Verify outputs
3. Real-application check
4. Freeze YAML
5. Update registry.yaml
