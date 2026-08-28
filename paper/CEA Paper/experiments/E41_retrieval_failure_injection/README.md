# Retrieval Failure Injection + Verifier Rescue

**Experiment ID:** E41
**RQ:** RQ2
**Tier:** 1
**Status:** planned
**Venue:** CEA journal (NOT EACL Demo)

## Summary

Injects 5 retrieval failure modes (wrong record, conflicting, cross-document misbinding, adversarial injection) and measures CUAR per mode for B0/B1/B3/B5/B6.

## Methods

5 failure modes x 200 queries = 1,000 cases

## Key Claim

BAA does not need retrieval to be perfect to remain safe.

## Files

- Spec: `experiments/specs/E41_retrieval_failure_injection.spec.yaml`
- Runner: `experiments/scripts/E41_retrieval_failure_injection/` (to be implemented)
- Results: `experiments/results/E41_retrieval_failure_injection/` (frozen after run)
- Paper: This directory — freeze outputs here after acceptance

## Implementation Priority

See `experiments/specs/E41_retrieval_failure_injection.spec.yaml` for full design, metrics, acceptance gates, and implementation notes.

## Acceptance Protocol

Follow `experiments/ACCEPTANCE_PROTOCOL.md`:
1. Run script
2. Verify outputs
3. Real-application check
4. Freeze YAML
5. Update registry.yaml
