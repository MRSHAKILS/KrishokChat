# Soil Case Cards

Route: `GET /api/soil/dataset` (info) and `POST /api/soil/analyze` (locked).
The **dataset is released** (real field photos, Pabna); the **regression
predictor stays `in_development`** — the analyzer is locked by design.

| # | Case | Input | Expected behavior |
|---|------|-------|-------------------|
| 1 | Dataset overview | `GET /api/soil/dataset` | 722 images, 0.0–21.5 kPa, 46 series, split 472/119/131, `model_status=in_development` |
| 2 | Dry sample (Doash) | `images/soil/P0001_Doash_8.0kpa.jpg` | analyzer-locked response; no fabricated kPa prediction |
| 3 | Wet sample (Atel) | `images/soil/P0406_Atel_16.5kpa.jpg` | analyzer-locked response |
| 4 | Split integrity | dataset files | train/val/test counts match 472/119/131 |

Screenshot fallback: `screenshots/05_soil_moisture.png`.