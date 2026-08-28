# Knowledge-Base Incompleteness + Monotone Safe Degradation

**Experiment ID:** E44
**RQ:** RQ3
**Tier:** 2
**Status:** planned
**Venue:** CEA journal (NOT EACL Demo)

## Summary

Progressively deletes 5-50% of authoritative records. Shows coverage degrades monotonically while CUAR stays near-zero — quantifies the qualitative Section 16 claim.

## Methods

7 deletion levels x 5 seeds x 1,000 queries = 35,000 cases

## Key Claim

Evidence incompleteness converts to abstention, not dangerous advice.

## Files

- Spec: `experiments/specs/E44_knowledge_base_incompleteness.spec.yaml`
- Runner: `experiments/scripts/E44_knowledge_base_incompleteness/` (to be implemented)
- Results: `experiments/results/E44_knowledge_base_incompleteness/` (frozen after run)
- Paper: This directory — freeze outputs here after acceptance

## Implementation Priority

See `experiments/specs/E44_knowledge_base_incompleteness.spec.yaml` for full design, metrics, acceptance gates, and implementation notes.

## Acceptance Protocol

Follow `experiments/ACCEPTANCE_PROTOCOL.md`:
1. Run script
2. Verify outputs
3. Real-application check
4. Freeze YAML
5. Update registry.yaml
