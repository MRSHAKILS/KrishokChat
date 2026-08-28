# Combinatorial Contract Corruption Ladder

**Experiment ID:** E43
**RQ:** RQ2
**Tier:** 1
**Status:** planned
**Venue:** CEA journal (NOT EACL Demo)

## Summary

Extends E28 single-slot mutations to multi-slot combinatorial attack. Tests B5 vs B6 at 1-slot, 2-slot, 3-slot, 5-slot, and 11-slot simultaneous corruption. All deterministic.

## Methods

36,500 total mutation cases, no LLM API calls

## Key Claim

B6 false-certification rate == 0% at all mutation levels.

## Files

- Spec: `experiments/specs/E43_combinatorial_contract_corruption.spec.yaml`
- Runner: `experiments/scripts/E43_combinatorial_contract_corruption/` (to be implemented)
- Results: `experiments/results/E43_combinatorial_contract_corruption/` (frozen after run)
- Paper: This directory — freeze outputs here after acceptance

## Implementation Priority

See `experiments/specs/E43_combinatorial_contract_corruption.spec.yaml` for full design, metrics, acceptance gates, and implementation notes.

## Acceptance Protocol

Follow `experiments/ACCEPTANCE_PROTOCOL.md`:
1. Run script
2. Verify outputs
3. Real-application check
4. Freeze YAML
5. Update registry.yaml
