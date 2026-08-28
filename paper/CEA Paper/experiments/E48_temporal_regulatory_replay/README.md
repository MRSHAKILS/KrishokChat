# Temporal Regulatory Replay

**Experiment ID:** E48
**RQ:** RQ2
**Tier:** 3
**Status:** planned
**Venue:** CEA journal (NOT EACL Demo)

## Summary

Replays 200 queries against 4 temporal knowledge-base snapshots (2022-2025) for 10 synthetic chemicals evolving from APPROVED to BANNED. Tests temporal consistency.

## Methods

10 chemicals x 4 periods x 5 queries = 200 evaluation points

## Key Claim

BAA is temporally consistent; CUAR == 0% for BANNED period.

## Files

- Spec: `experiments/specs/E48_temporal_regulatory_replay.spec.yaml`
- Runner: `experiments/scripts/E48_temporal_regulatory_replay/` (to be implemented)
- Results: `experiments/results/E48_temporal_regulatory_replay/` (frozen after run)
- Paper: This directory — freeze outputs here after acceptance

## Implementation Priority

See `experiments/specs/E48_temporal_regulatory_replay.spec.yaml` for full design, metrics, acceptance gates, and implementation notes.

## Acceptance Protocol

Follow `experiments/ACCEPTANCE_PROTOCOL.md`:
1. Run script
2. Verify outputs
3. Real-application check
4. Freeze YAML
5. Update registry.yaml
