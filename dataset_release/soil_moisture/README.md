# Bangladesh Soil Moisture Field Dataset (RGB → kPa)

**First field-collected RGB soil-moisture dataset for Bangladesh.**
722 tensiometer-labeled soil photos (0.0–21.5 kPa), 6 USDA-equivalent soil
texture classes, 3 land types, 14 crops, 8 growth stages — collected over a
3-day field campaign (May 29–31, 2026) in **Pabna District**.

| Stat | Value |
|---|---|
| Images | ৭২২ (722) |
| Resolution | 720×1280 portrait JPEG (mixed orientations, all valid) |
| Ground truth | Field tensiometer log (`TraceData.xlsx`), kPa |
| kPa range | 0.0 – 21.5 kPa (50 unique values) |
| kPa bins | 0–10: 100 · 10–20: 506 · 20–22: 116 |
| Soil types | 6 (see map below) |
| Land types | High: 289 · Medium: 308 · Low: 117 |
| Crops | 14 (Rich 119, No crop 107, Jute 96, Grass 81, Mango 77, …) |
| Growth stages | 8 (Mature 280, Seedling 100, Pre-harvest 79, …) |
| Measurement series | 46 (largest 83, 15 singletons) |
| Split | Train 472 / Val 119 / Test 131 — **series-stratified, leakage-checked** |
| Metadata matched | 714/722 from field log (98.9%) · 8 inferred by nearest-neighbor (1.1%) |
| Corrections | 106 kPa corrections (Δ>0.5), 12 missing IDs filled, 4 duplicate IDs resolved |
| Contamination | 2 images flagged & excluded from training (P0029, P0166) |

## Soil Type Map (Bengali transliteration → USDA)

| Key | USDA class | Count |
|---|---|---|
| `Doash` | Loam | 180 |
| `Atel` | Clay | 156 |
| `Bele_Doash` | Sandy Loam | 143 |
| `Atel_Doash` | Clay Loam | 126 |
| `Poli` | Silt | 85 |
| `Bele` | Sandy | 32 |

## Files

| File | Purpose |
|---|---|
| `image_manifest.csv` | **FROZEN canonical manifest** — 722 rows × 16 cols (single source of truth) |
| `split_assignment.csv` | **FROZEN** series-stratified train/val/test (472/119/131) |
| `dataset_summary.json` | Summary statistics (types, bins, splits) |
| `anomalies.json` | Active anomalies: contamination, viewpoint, inferred metadata |
| `series_map.json` | 46 series definitions (kPa per series, id ranges) |
| `exif_metadata.json` | Camera metadata, lighting window evidence |
| `reports/PHASE0_AUDIT_REPORT.md` | Full integrity audit (corrections, dedup, leakage check) |
| `reports/preprocessing_report.md` | Canonical pipeline documentation (steps 0a–2e) |
| `model_status.json` | **Honest model benchmark table** — all models `in_development` |
| `thumbnails/` + `preview_grid.jpg` | 12 stratified samples + contact sheet (UI display copy) |

## Split Integrity

Split is performed **at the series level** (a measurement series = one plot/tensiometer
setup over time). Images from the same series never appear in both train and test,
eliminating temporal autocorrelation leakage. Validation: exact 472/119/131 with zero
series overlap.

## Known Limitations

- **3-day window** (May 29–31, 2026) — single site, single season.
- **No capture timestamps** in the field log; `rain_date/rain_time` refer to the last
  rainfall, not the photo time.
- **Tensiometer range ceiling ~21.5 kPa** — wetter/drier extremes not represented.
- **Bele (Sandy) is underrepresented** (32 images).
- **8 images** have inferred (not logged) metadata — flagged in `anomalies.json`.
- Landscape images are intentionally shot horizontally — **do not auto-rotate**
  (see `orientation_note` in `anomalies.json`).

## Model Status

**The dataset is the released asset. The regression model is NOT.**

All trained models currently underperform the mean predictor (negative R²).
See `model_status.json` for the frozen benchmark table. The KrishokTech UI
ships the analyzer **locked** ("মডেল উন্নয়নে") until a validated artifact exists
(target: positive R² on held-out series).

## Citation & License

TODO: add citation line and license after researcher confirmation.
Preferred citation format (placeholders):

```
Khan, R. et al. (2026). Bangladesh Soil Moisture Field Dataset (RGB→kPa).
Pabna District field campaign, May 29–31 2026.
```

## Access

- This folder ships inside the KrishokTech repository (`dataset_release/soil_moisture/`).
- Display copy for the UI: `frontend/public/assets/soil_samples/` (12 thumbnails + grid).
- Hugging Face upload: TODO (follows `RaiyanKhaan/krishokChat` pattern).
- Regenerate UI assets: `python scripts/build_soil_release.py` (idempotent).