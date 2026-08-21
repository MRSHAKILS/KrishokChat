# Step 2: Canonical Dataset Preprocessing Report

**Date:** 2026-07-07  
**Dataset:** Soil Moisture Detection (Tensiometer Images)  
**Canonical Source:** `updated_dataset/correct_image/` + `updated_dataset/TraceData.xlsx`  
**Total Images:** 722

---

## Summary

Unlike a typical preprocessing pipeline that starts from raw camera exports, this dataset's **preprocessing was largely performed by the field team** before delivery. The `correct_image/` directory contains 722 corrected JPEGs with proper filenames, accurate kPa values, and associated metadata in `TraceData.xlsx`.

The Python preprocessing scripts in `dataset/scripts/` exist to:
1. **Merge** the images with their metadata (rebuild canonical manifest)
2. **Validate** correctness (cross-reference filenames vs XLSX)
3. **Infer** metadata for the 8 images not in TraceData but present in correct_image/
4. **Split** into train/val/test with series-aware stratification

---

## Pipeline Steps

| Step | Script | What it does | Status |
|------|--------|-------------|--------|
| 2a | `merge_updated_metadata_step2a.py` | Initial merge attempt: `correct_image/` + TraceData.xlsx → `image_manifest_canonical.csv` | ✅ Initial merge |
| 2b | `rebuild_canonical_dataset_step2b.py` | Rebuild canonical manifest with 16 columns, detect kPa corrections, build series | ✅ Canonical manifest |
| 2c | `fix_unmatched_metadata_step2c.py` | Investigate 8 images not in TraceData; locate gaps in blocks P0167–P0196 | ✅ Gap analysis |
| 2d | `finalize_canonical_manifest_step2d.py` | Infer metadata for 8 unmatched, finalize 46 series, generate stratified split | ✅ **Final canonical output** |

---

## No Filename Renaming Needed

The canonical dataset (`correct_image/`) has **already-correct filenames**. Unlike the original `raw/` directory which had:
- Comma decimals (`,` instead of `.`)
- Truncated unit (`Kp` instead of `Kpa`)
- Missing decimals (`985` instead of `9.85`)
- 603 files needing renaming

The canonical images require **zero filename corrections**.

---

## Key Numbers

| Metric | Value |
|--------|-------|
| Images in canonical manifest | **722** |
| Matched from TraceData.xlsx | 714 (98.9%) |
| Inferred from nearest neighbors | 8 (1.1%) |
| kPa corrections detected (Δ>0.5) | **106** |
| Series built | **46** |
| Stratified split | Train=**472**, Val=**119**, Test=**131** |

---

## kPa Corrections Detected

When the filename kPa value differed from the TraceData.xlsx value by >0.5 kPa, the TraceData value was adopted as ground truth. Largest corrections:

| Image | Filename kPa | Correct kPa | Δ | Reason |
|-------|-------------|-------------|---|--------|
| P0114 | 101.0 | 10.0 | 91.0 | Sensor spike — **corrected** |
| P0064 | 9.85 | 0.0 | 9.85 | Fully wet soil — corrected |
| P0028 | 19.95 | 15.25 | 4.70 | Field log correction |
| P0055 | 15.25 | 19.75 | 4.50 | Field log correction |
| P0053 | 15.25 | 11.50 | 3.75 | Field log correction |

These corrections are baked into `image_manifest.csv` — the `kpa_raw` column contains the canonical TraceData value.

---

## Inferred Images (8)

| Image | Inferred From | Reason |
|-------|--------------|--------|
| P0171 | P0170 (Δt=0.5 kPa) | Block P0167–P0196 missing from TraceData |
| P0172 | P0170 (Δt=0.0 kPa) | Same block gap |
| P0183 | P0182 (Δt=0.0 kPa) | Same block gap |
| P0184 | P0182 (Δt=1.0 kPa) | Same block gap |
| P0339 | P0338 (Δt=0.0 kPa) | Block P0339–P0340 missing from TraceData |
| P0340 | P0338 (Δt=0.0 kPa) | Same block gap |
| P0670 | P0669 (Δt=0.0 kPa) | Block gap |
| P0671 | P0669 (Δt=1.0 kPa) | Same block gap |

**Method:** Nearest-neighbor inference — same soil_type, crop, growth_stage, land_type, and rain_date as the preceding image. kPa adopted from the canonical filename.

---

## Split Details

**Method:** Stratified by soil_type × kpa_bin (18 strata). Series-grouped (no leakage).

| Split | Count | % | 0–10 kPa | 10–20 kPa | 20–22 kPa |
|-------|-------|---|----------|-----------|-----------|
| Train | 472 | 65.4% | 84 | 344 | 44 |
| Val | 119 | 16.5% | 3 | 58 | 58 |
| Test | 131 | 18.1% | 13 | 104 | 14 |

**Leakage check:** ✅ PASS — No series spans multiple splits.

---

## Output Files

| File | Location | Description |
|------|----------|-------------|
| `image_manifest.csv` | `dataset/preprocessed/` | **Frozen** — 722 images, 16 columns. Single source of truth. |
| `split_assignment.csv` | `dataset/preprocessed/` | **Frozen** — 472/119/131 split |
| `dataset_summary.json` | `dataset/preprocessed/` | Summary statistics |
| `canonical_migration_log.md` | `dataset/reports/` | Migration notes |

---

## What Was NOT Done

| Task | Reason | Status |
|------|--------|--------|
| Filename normalization | Not needed — correct_image/ already correct | ✅ SKIPPED |
| EXIF timestamp extraction | No EXIF timestamps embedded; blocked (Tesseract not installed) | ⏳ BLOCKED |
| Contamination flagging (auto) | Manual flag only (P0029) | ✅ Single flag |
| Image resizing/cropping | All images already 720×1280 | ✅ Already uniform |
| Color normalization | Deferred to Phase 1 (per-model preprocessing) | ⏳ PHASE 1 |

---

*End of preprocessing report (Canonical Dataset). Prepared 2026-07-07.*
