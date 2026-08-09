# Vision Workflow — Paper and Demo Claims

This file prevents the demo narrative from drifting beyond the verified artifacts.

## Defensible claim today

> KrishokChat implements a modular, safety-aware multimodal crop-disease advisory
> workflow for Bengali agricultural support. An image is quality-checked, classified into
> a crop, routed to a crop-specific disease classification model, matched to Bengali
> disease knowledge, and passed through the same grounded retrieval/generation/verifier
> path used by text advice.

## Do not claim today

- Do not call the current response “object detection” in the paper or demo narration.
- Do not display or describe bounding boxes, lesion localization, mAP, or IoU for the
  current artifacts.
- Do not say that every crop has a disease model. `GourdGuava` and `Solanacea` currently
  have no mapped disease model in the registry.
- Do not describe confidence values as calibrated probabilities without a calibration
  evaluation.
- Do not claim all treatment advice is verified merely because a disease was classified.
  The advisory response has its own retrieval and verifier confidence.

## Demo sequence

1. Upload a clear leaf image.
2. Show the intake/quality gate.
3. Show crop classification confidence.
4. Show routing to the specialized crop model.
5. Show disease classification and Bengali disease details.
6. Show the advisory trace: safety → retrieval → generation → verification.
7. Show treatment confidence and any verifier warning.
8. If the image is dark, too small, low-detail, low-confidence, healthy, or unsupported,
   show the explicit honest-failure state instead of forcing a diagnosis.

## Metrics to add only when measured

Use `TODO` placeholders until the source evaluation artifacts provide the values:

- crop classifier top-1/top-3 accuracy;
- per-disease classification accuracy/F1;
- confidence threshold coverage and rejection rate;
- disease-details matching coverage;
- advisory retrieval grounding rate;
- dosage interception rate;
- end-to-end latency by stage;
- human review of unsafe or flagged advice.
