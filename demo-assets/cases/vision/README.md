# Vision Case Cards

All checked-in artifacts are `task: classify` — **no bounding boxes ever**.
Route: `POST /api/detect` (multipart `file`, optional `crop_hint`).

| # | Case | Input | Expected behavior | Determinism |
|---|------|-------|-------------------|-------------|
| 1 | Rice leaf blast (hint=rice) | `images/rice/leaf_blast.jpg` | diagnosis or not-recognized-by-confidence; `detection_mode=classification`, `boxes=[]` | DET (ONNX/YOLO in-process) |
| 2 | Rice brown spot (hint=rice) | `images/rice/brown_spot.jpg` | same as above | DET |
| 3 | Rice healthy leaf (hint=rice) | `images/rice/healthy_leaf.jpg` | healthy or not-recognized | DET |
| 4 | Potato late blight (hint=potato) | `images/potato/late_blight.jpg` | diagnosis or not-recognized | DET |
| 5 | Invalid image | `expected/invalid-image.txt` | HTTP 400; no model invoked | DET |
| 6 | Unsupported crop (tomato) | `images/tomato/late_blight.jpg` | explicit no-disease-model boundary; never a tomato diagnosis | DET |
| 7 | Crop classifier only | any photo, no crop_hint | crop classification into Brassica/Corn/GourdGuava/Potato/Solanacea/Wheat; routing to the matching disease model when it exists | DET |

Registered disease models: `brassica`, `corn`, `potato`, `rice`, `wheat`.
`Solanacea` (tomato family) has **no disease model** — the UI offers no tomato
hint and the backend answers the boundary explicitly.

Evidence: `backend/ml_assets/vision/verification_report.json` +
`test_images/test_matrix_results.json` (437-row matrix).
Screenshot fallback: `screenshots/04_detect_diagnosis.png`.