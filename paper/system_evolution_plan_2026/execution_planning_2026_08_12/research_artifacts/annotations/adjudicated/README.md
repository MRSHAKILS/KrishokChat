# Adjudicated annotations (T10 output)

**Status:** EMPTY — awaiting expert annotation at the END of the project.

This directory receives the outputs of T08 (pilot) and T10 (expert gold):

| File (when created) | Content |
|---|---|
| `T08_labels_annotatorA_v1.jsonl` | Raw labels, annotator A, all 24 pilot items. |
| `T08_labels_annotatorB_v1.jsonl` | Raw labels, annotator B, all 24 pilot items. |
| `T08_adjudication_v1.jsonl` | Adjudicator decisions with lineage for every disagreement. |
| `T10_labels_annotatorA/B_v1.jsonl` | Raw labels for the full gold set. |
| `T10_adjudication_v1.jsonl` | Adjudicator decisions for the full gold set. |
| `T10_agreement_report_v1.md` | Krippendorff alpha / kappa, span/field/relation agreement, adjudication rate. |

Rules (T07 protocol §6, scoped AGENTS.md rule 6):
- Every label keeps `annotator_id`, `guideline_version`, `timestamp_utc`, raw label,
  confidence/notes where approved, and adjudication lineage.
- Raw labels are never replaced by consensus; both survive.
- No file here is ever regenerated from a later test-informed state.