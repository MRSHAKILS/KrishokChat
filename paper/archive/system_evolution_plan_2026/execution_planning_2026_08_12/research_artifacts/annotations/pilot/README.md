# T08 Annotation Pilot — Run Kit

**Status:** SCAFFOLDED (items + schema + forms ready). **Blocked on human experts** —
labeling, adjudication, and agreement will run at the END of the project per plan
decision. Do NOT run confirmatory evaluations before pilot agreement clears.

**Authority:** `execution_planning_2026_08_12/11_FINAL_IMPLEMENTATION_SPEC.md` row T08;
labeling rules: `annotations/guidelines/T07_label_manual_v1.md`,
`T07_protocol_v1.md`, `T07_risk_taxonomy_v1.md`; label output schema:
`../datasets/frozen/T07_claim_schema_v1.json`.

## What exists now (regenerated only through the tools below)

| File | Description |
|---|---|
| `T08_pilot_item_schema_v1.json` | JSON Schema for pilot items (validated). |
| `T08_pilot_items_v1.jsonl` | 24 self-contained items (query + answer + evidence passage), DEV pool only, 5 strata, seeded 20260813. |
| `../../scripts/sample_pilot_items.py` | Regenerates the items deterministically (never touches TEST). |

## Pilot items at a glance

- **Pool:** DEVELOPMENT only (`split_pool != "test"` enforced by the sampler).
  Train is used only as a fallback; the current run needed no fallback (24/24 dev).
- **Strata:** disease+chem 6 · pest+chem 6 · fertilizer+chem 6 · non-chem 4 · other 2.
- **Evidence:** each item embeds the first 4000 chars of its source passage with the
  source SHA-256, so labeling is self-contained.

## Roles (when humans are available)

1. **Annotator A** and **Annotator B** — independent domain experts (native Bengali
   comprehension required; agriculture/disease/pest expertise preferred).
2. **Lead adjudicator (third expert)** — resolves disagreements; writes the
   adjudication decision with lineage.

## Run order (T08 when unpaused)

1. Both annotators label **each item** independently, per the label manual, producing
   one label file per annotator over *all 24 items*:
   - `annotations/adjudicated/T08_labels_annotatorA_v1.jsonl`
   - `annotations/adjudicated/T08_labels_annotatorB_v1.jsonl`
   Each label object conforms to `T07_claim_schema_v1` and adds
   `annotator_id`, `label_timestamp_utc`, `guideline_version` (raw labels preserved,
   never replaced by consensus).
2. **Adjudication:** lead expert fills
   `annotations/adjudicated/T08_adjudication_v1.jsonl` — one entry per disagreement:
   `item_id`, `claim_id`, `annotator_a_label`, `annotator_b_label`, `decision`,
   `rationale`, `adjudicator_id`, `timestamp_utc`.
3. Compute agreement (Krippendorff alpha or approved kappa, per
   `manifests/T07_endpoints_margins_multiplicity_latency_v1.md`) — T10 deliverable.
4. **Gate:** pilot agreement must meet the frozen threshold (alpha ≥ 0.70 on the
   development target). The pilot must validate every relation type, missing-value
   state, conflict marker, and safety criterion (label manual §pilot). At most **ONE**
   guideline revision is allowed; if the gate still fails, STOP and re-plan
   (per spec T08 row).

## Never do

- Do NOT draw pilot items from the TEST split.
- Do NOT change labels based on a later test run.
- Do NOT replace raw labels with consensus only — keep both.
- Do NOT edit `T08_pilot_items_v1.jsonl` by hand; regenerate via
  `sample_pilot_items.py` and re-hash.

## Regeneration

```powershell
$env:PYTHONIOENCODING='utf-8'
python research_artifacts/scripts/sample_pilot_items.py
```

Deterministic given the T09 split files and fixed seed (20260813). After any
regeneration, update the hash manifest
(`manifests/T09_artifact_hashes_v1.json`) via
`research_artifacts/scripts/hash_artifacts.py`.