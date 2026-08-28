# Model-Substitution Safety Invariance

**Experiment ID:** E40
**RQ:** RQ2
**Tier:** 1
**Status:** planned
**Venue:** CEA journal (NOT EACL Demo)

## Summary

Tests whether CUAR remains invariant when the Tier-3 LLM is swapped across 5 models. Reuses E27 100-case benchmark. No new data generation needed.

## Methods

5 LLMs x 100 E27 cases = 500 evaluations via OpenRouter

## Key Claim

CUAR is model-agnostic; authority is architectural.

## Files

- Spec: `experiments/specs/E40_model_substitution_safety_invariance.spec.yaml`
- Runner: `experiments/scripts/E40_model_substitution_safety_invariance/` (to be implemented)
- Results: `experiments/results/E40_model_substitution_safety_invariance/` (frozen after run)
- Paper: This directory — freeze outputs here after acceptance

## Implementation Priority

See `experiments/specs/E40_model_substitution_safety_invariance.spec.yaml` for full design, metrics, acceptance gates, and implementation notes.

## Acceptance Protocol

Follow `experiments/ACCEPTANCE_PROTOCOL.md`:
1. Run script
2. Verify outputs
3. Real-application check
4. Freeze YAML
5. Update registry.yaml
