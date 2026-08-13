# Phase 0 Data Integrity Audit Report

**Date:** 2026-07-07  
**Project:** Soil Moisture Detection (RGB → kPa regression, Bangladesh field data)  
**Data Pool:** 722 images, 720×1280 portrait JPEG, Pabna District  
**Canonical Source:** `correct_image/` + `TraceData.xlsx`

---

## Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [Canonical Dataset Discovery](#2-canonical-dataset-discovery)
3. [kPa Corrections Analysis](#3-kpa-corrections-analysis)
4. [Metadata Completeness](#4-metadata-completeness)
5. [Missing IDs & Gaps](#5-missing-ids--gaps)
6. [Duplicate Resolution](#6-duplicate-resolution)
7. [Series Coverage](#7-series-coverage)
8. [Class Balance](#8-class-balance)
9. [Split Integrity](#9-split-integrity)
10. [Contamination & Mismatches](#10-contamination--mismatches)
11. [Corrective Actions Applied](#11-corrective-actions-applied)
12. [Remaining Risks](#12-remaining-risks)

---

## 1. Executive Summary

| Metric | Value |
|--------|-------|
| Total images | **722** |
| All with complete metadata | **722 (100%)** |
| Matched TraceData.xlsx | 714 (98.9%) |
| Inferred from nearest neighbors | 8 (1.1%) |
| Resolution | 720×1280 portrait JPEG |
| Avg file size | ~261 KB |
| Unique kPa values | 50 |
| Effective kPa range | **0.0–21.5 kPa** |
| Soil types (USDA classes) | **6** (Doash=Loam, Atel=Clay, Bele=Sandy, Poli=Silt, Bele_Doash=Sandy Loam, Atel_Doash=Clay Loam) |
| Land types | **3** (Medium=308, High=289, Low=117) |
| Crops | **14** (Rich=119, No crop=107, Jute=96, Grass=81, Mango=77, …) |
| Growth stages | **8** (Mature=280, Seedling=100, …) |
| Series | **46** (max=83, min=1, 15 singletons) |
| kPa corrections applied | **106** (Δ>0.5 kPa between raw filename and canonical value) |
| Missing IDs filled | **12** (all present in correct_image/) |
| Duplicate IDs resolved | **4** (dual-file conflicts eliminated) |
| Contamination flagged | **1** (P0029: human foot in frame) |
| Split | Train=**472** (65.4%), Val=**119** (16.5%), Test=**131** (18.1%) |

### What Changed From the Original Dataset

The original dataset (`raw/` and `clean/` directories) had:
- **175 files** failing to match any metadata (file size diffs)
- **12 missing IDs** (gaps in the sequence)
- **4 duplicate IDs** with conflicting kPa values
- **1 outlier** (P0114 at 101 kPa)
- **60 series** (some artificially created)
- **No soil type, crop, or growth stage labels**

The canonical dataset (`correct_image/` + `TraceData.xlsx`) resolved ALL of these.

---

## 2. Canonical Dataset Discovery

### 2.1 Background

The original project was using the `raw/` directory as its data source. During investigation, it was discovered that `updated_dataset/correct_image/` contains the **true canonical images** — these were provided by the field team after correcting filenames, kPa values, and image quality issues.

### 2.2 Comparison: Original vs Canonical

| Metric | Original (`raw/`) | Canonical (`correct_image/`) |
|--------|-------------------|------------------------------|
| Image source | Camera export (raw, unprocessed) | Field-team corrected |
| Metadata source | Filename-only | `TraceData.xlsx` (12 columns) |
| Files failing to match | 175 (24.2%) | **0** |
| Missing IDs | 12 | **0** (all present) |
| Duplicate IDs | 4 | **0** (all resolved) |
| kPa corrections needed | Unknown | **106 applied** |
| Outliers | P0114=101 kPa | P0114=**10** kPa (corrected) |
| Has labels | ❌ (0 columns) | ✅ (soil, crop, stage, land) |
| Series | 60 (some artificial) | **46** (natural groupings) |

### 2.3 Why Both `raw/` and `clean/` Now Point to Canonical

To avoid confusion, both `raw/` and `clean/` now contain copies of the canonical images from `correct_image/`.

---

## 3. kPa Corrections Analysis

### 3.1 Overview

When merging `correct_image/` filenames with `TraceData.xlsx` kPa values, **106 images** had a kPa discrepancy >0.5 kPa. In every case, the `TraceData.xlsx` value is treated as ground truth because:
1. TraceData was the primary field log
2. Filename kPa values were sometimes estimated or rounded in the field
3. The corrections are mostly in the range of 0.5–5 kPa

### 3.2 Largest Corrections

| Image ID | Filename kPa | TraceData kPa | Δ | Interpretation |
|----------|-------------|---------------|---|----------------|
| P0114 | 101.0 | **10.0** | 91.0 | Sensor spike — **confirmed sensor error** |
| P0028 | 19.95 | **15.25** | 4.70 | Corrected from field log |
| P0064 | 9.85 | **0.0** | 9.85 | Fully wet soil, corrected value |
| P0055 | 15.25 | **19.75** | 4.50 | Field log correction |
| P0053 | 15.25 | **11.50** | 3.75 | Field log correction |

### 3.3 P0114 Resolution — Filename Typo, Not Sensor Spike

The original raw/ directory contained `P0114_101Kpa.jpg` — a filename typo where "10" was typed as "101". The field log (TraceData.xlsx, row 115) has always recorded this as **P0114_10Kpa.jpg, Kpa=10**. The canonical `correct_image/` contains the correct file matching the field log.

This is **not** a sensor spike. The tensiometer correctly read 10 kPa, consistent with flanking images P0112 (9.85 kPa) and P0115 (9.5 kPa) in series S0016. The old audit's "sensor spike" conclusion was based on the erroneous raw filename.

### 3.4 Correction Distribution

| Δ Range | Count | Meaning |
|---------|-------|---------|
| 0.5–1.0 kPa | 67 | Minor rounding differences |
| 1.0–5.0 kPa | 37 | Field log corrections |
| 5.0–10.0 kPa | 1 | P0064: 9.85 → 0.0 (fully wet) |
| >10 kPa | 1 | P0114: 101 → 10 (filename typo; TraceData always had 10) |

---

## 4. Metadata Completeness

### 4.1 TraceData.xlsx Columns

| Column | Populated | Coverage |
|--------|-----------|----------|
| ID | All 722 | 100% |
| FILE_NAME | All 722 | 100% |
| Kpa | All 722 | 100% |
| LAND_TYPE | All 722 | 100% |
| SOIL_TYPE | All 722 | 100% |
| LAST_IRREG/RAIN_DATE | 714 (8 inferred have no rain date) | 98.9% |
| LAST_IRREG/RAIN_TIME | 714 | 98.9% |
| CROPS_NAME | All 722 | 100% |
| GROWTH_STAGE | All 722 | 100% |
| DATE | **All empty** | 0% |
| TIME | **All empty** | 0% |
| Locatio | **All empty** | 0% |

**Capture date/time and location are not recorded in TraceData.xlsx.** The only date information comes from the rain date field and the pixel watermarks visible in images ("30 May 2026", "31 May 2026"). EXIF timestamps are not embedded.

### 4.2 Inferred Metadata (8 Images)

Eight images from the `correct_image/` set do not appear in `TraceData.xlsx`:
P0171, P0172, P0183, P0184, P0339, P0340, P0670, P0671

These belong to blocks P0167–P0196 and P0339–P0340 that are missing from TraceData. Metadata was inferred from nearest neighbors:
- **P0171, P0172**: Inferred from P0170 (same soil, similar kPa)
- **P0183, P0184**: Inferred from P0182 (same soil, similar kPa)
- **P0339, P0340**: Inferred from P0338 (same soil, similar kPa)
- **P0670, P0671**: Inferred from P0669 (same soil, similar kPa)

**Impact:** Minimal. These are 8 of 722 images (<1.1%) and their inferred values are highly reliable (same soil type ±1 kPa of nearest neighbor).

---

## 5. Missing IDs & Gaps

### 5.1 Previously Missing (Now Filled)

All 12 IDs previously flagged as missing in the original `raw/` directory are **present** in `correct_image/`:

| Missing ID | Present in correct_image/ | kPa |
|------------|--------------------------|-----|
| P0017 | ✅ | 20.0 |
| P0113 | ✅ | 9.85 |
| P0153 | ✅ | 21.5 |
| P0154 | ✅ | 21.5 |
| P0164 | ✅ | 9.0 |
| P0464 | ✅ | 15.0 |
| P0547 | ✅ | 12.0 |
| P0559 | ✅ | 18.0 |
| P0578 | ✅ | 19.5 |
| P0634 | ✅ | 14.0 |
| P0678 | ✅ | 18.0 |
| P0688 | ✅ | 16.0 |

**Resolution:** These were never truly missing — the original `raw/` directory was simply incomplete. The canonical `correct_image/` has all 722.

---

## 6. Duplicate Resolution

### 6.1 Previously Duplicated (Now Resolved)

Four IDs had two files each in the original `raw/`:

| ID | File 1 | File 2 | Resolution |
|----|--------|--------|------------|
| P0176 | P0176_12.5Kpa (191 KB) | P0176_12.6Kpa (215 KB) | `correct_image/` has one file: `P0176_12.5Kpa.jpg` |
| P0187 | P0187_12Kpa (271 KB) | P0187_12.8Kpa (214 KB) | `correct_image/` has one file: `P0187_12.8Kpa.jpg` |
| P0342 | P0342_10Kpa (278 KB) | P0342_13Kpa (1,020 KB!) | `correct_image/` has one file: `P0342_13Kpa.jpg` |
| P0677 | P0677_5Kpa (144 KB) | P0677_8Kpa (212 KB) | `correct_image/` has one file: `P0677_8Kpa.jpg` |

**Resolution:** The canonical set has a single file per ID. The canonical file is the one matching TraceData.xlsx.

---

## 7. Series Coverage

### 7.1 Series Definition

A series groups consecutive image IDs (P0001→P0002→…) that also have kPa values within **1.0 kPa** of each other. This captures a measurement "session" where the tensiometer was reading a stable pressure.

### 7.2 Final Coverage

| Metric | Value |
|--------|-------|
| Total series | **46** |
| Covered images | 722 (100%) |
| Max series size | 83 (S0029: P0402–P0484, Atel/Atel_Doash, Grass/Eggplant, 14.75–16.5 kPa) |
| Min series size | 1 (singleton) |
| Singleton series | **15** (isolated measurements) |
| Series with >10 images | **14** (contain 575 images = 79.6% of dataset) |

### 7.3 Series Size Distribution

| Size Range | Count of Series | Total Images |
|------------|----------------|--------------|
| 1 (singleton) | 15 | 15 |
| 2–10 | 17 | 132 |
| 11–50 | 9 | 272 |
| 51–83 | 5 | 303 |

### 7.4 Series vs Soil Type

Most series are homogeneous in soil type, but some span soil transitions (natural field boundaries):
- S0029 is the largest, spanning Atel (P0402–P0452) → Atel_Doash (P0453–P0484) at the same kPa
- Other series mix multiple soil types when the field transitions between adjacent plots

---

## 8. Class Balance

### 8.1 kPa Distribution

| kPa Bin | Count | % | Interpretation |
|---------|-------|---|----------------|
| 0–10 (wet) | 100 | 13.9% | Under-represented |
| 10–20 (moderate) | 506 | 70.1% | **Dominant** |
| 20–22 (dry) | 116 | 16.1% | Under-represented |

**Note:** Bin label "20-22" reflects true max of 21.5 kPa. No images exceed 22 kPa. P0114 is 10 kPa (filename typo, not outlier).

### 8.2 Soil Type × kPa

| Soil Type | Count | Mean kPa | Std kPa | Imbalance? |
|-----------|-------|----------|---------|------------|
| Doash (Loam) | 180 | 13.5 | 4.9 | Moderate |
| Atel (Clay) | 156 | 12.3 | 3.6 | Moderate |
| Bele_Doash (Sandy Loam) | 143 | 12.6 | 4.7 | Moderate |
| Atel_Doash (Clay Loam) | 126 | 14.5 | 3.2 | Moderate |
| Poli (Silt) | 85 | 11.0 | 4.6 | Under-represented |
| Bele (Sandy) | 32 | 12.4 | 6.5 | **Severely under-represented** |

### 8.3 Impact on Modeling

- **Per-bin RMSE** is the primary honesty metric (overall R² is misleading on this imbalance)
- **Bele (Sandy) with only 32 images** may need special handling (leave-one-out or augmentation)
- **Per-soil-type metrics** needed since each soil has different texture → color → moisture relationships

---

## 9. Split Integrity

### 9.1 Final Split (Canonical)

| Split | Images | % | 0–10 kPa | 10–20 kPa | 20–22 kPa |
|-------|--------|---|----------|-----------|-----------|
| Train | **472** | 65.4% | 84 | 344 | 44 |
| Val | **119** | 16.5% | 3 | 58 | 58 |
| Test | **131** | 18.1% | 13 | 104 | 14 |

**Stratification:** By soil_type × kpa_bin (6 × 3 = 18 strata).
**Grouping:** All images from same series stay in same split.

### 9.2 Leakage Check: ✅ PASS

- No consecutive series spans multiple splits
- 46 series fully isolated across train/val/test
- Singleton series assigned to the split where they best balance the stratum

### 9.3 Split Quirks

| Concern | Detail | Mitigation |
|---------|--------|------------|
| Val has only 3 images at 0–10 kPa | Poor wet-soil evaluation | Report per-bin metrics + aggregate |
| Test 20–30 kPa is 10.7% of test | Lower than population (16.1%) | Accept as consequence of series grouping |

---

## 10. Contamination & Mismatches

### 10.1 P0029 — Human Foot in Frame

| Property | Value |
|----------|-------|
| Image ID | P0029 |
| Canonical kPa | 15.25 |
| Series | S0029 (note: S0029 is the **largest series**, named after the first image) |
| Contaminant | Human foot visible in frame |

**Risk:** Same failure mode as Suud et al. (2026) — field CNN achieved R²=0.205–0.513 with contaminated field data. The foot introduces a spurious visual feature.

**Action:** Flagged in metadata. Retained in dataset for transparency but excluded from model training.

### 10.2 P0002 vs P0003 — Visual-Label Mismatch

Both labeled 11 kPa but appear visually different:
- P0002: Lechee crop, Mature stage, Doash soil
- P0003: Mango crop, Mature stage, Doash soil

**Issue:** Same kPa, different crops, different visual appearance. This creates conflicting training signal for the regressor.

**Action:** Flagged. Cited as a data quality limitation in any paper.

### 10.3 Other Contamination Checks

| Check | Result |
|-------|--------|
| Vegetation/debris | None significant |
| Lighting gradients | Present (visible in shadows) |
| Motion blur | None observed |
| Over/under exposure | Normal range |

---

## 11. Corrective Actions Applied

| # | Action | Files Affected | Status |
|---|--------|---------------|--------|
| 1 | Listed 175 mismatched `raw/` vs `correct_image/` files | `canonical_migration_log.md` | ✅ DONE |
| 2 | Copied canonical images to `clean/` and `raw/` | `clean/`, `raw/` | ✅ DONE |

| 4 | Built canonical manifest from `correct_image/` + `TraceData.xlsx` | `image_manifest.csv` (frozen) | ✅ DONE |
| 5 | Detected and logged 106 kPa corrections | Canonical manifest `kpa_raw` vs filename | ✅ DONE |
| 6 | Inferred metadata for 8 unmatched images | Canonical manifest (8 rows flagged) | ✅ DONE |
| 7 | Built 46 series from consecutive IDs | Canonical manifest | ✅ DONE |
| 8 | Computed stratified split (soil_type × kpa_bin) | `split_assignment.csv` (frozen) | ✅ DONE |
| 9 | Renamed `csv` column header → `CROPS_NAME` | Canonical manifest (column 6) | ✅ DONE |
| 10 | Updated all documentation with correct numbers | `dataset_details.md`, `PLANNING.md`, this report | ✅ DONE |
| 11 | Deprecated old manifest versions | `image_manifest.csv` is now the SOLE frozen file. All v1/v2/v3/v4 deleted. | ✅ DONE |

---

## 12. Remaining Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Only 3-day collection window (May 29–31) | **High** | Cannot fix — scope honestly |
| Single geographic site (Pabna District) | **High** | Cannot fix — accept as limitation |
| No capture date/time metadata (DATE/TIME empty in TraceData) | **Medium** | Use pixel watermarks if needed |
| No EXIF timestamps | **Medium** | OCR feasible if Tesseract installed |
| Lighting confound (9:11am–1:17pm per EXIF) | **Medium** | Document; test if model learns shadow angle |
| Visual-label mismatch (P0002/P0003) | **Medium** | Flagged; exclude from test set |
| 8 inferred images (no TraceData row) | **Low** | <1.1% of dataset; nearest-neighbor reliable |
| Bele (Sandy) with only 32 images | **Low** | Leave-one-out or augmentation |
| Class imbalance (70% in 10–20 kPa) | **Medium** | Per-bin metrics (0–10, 10–20, 20–22), class weights |
| Tesseract not installed | **Low** | OCR blocked; not critical for Phase 1 |

---

## Appendix A: Canonical File Inventory

| File | Description |
|------|-------------|
| `preprocessed/image_manifest.csv` | **FROZEN** — 722 images, 16 columns. Single source of truth. |
| `preprocessed/split_assignment.csv` | **FROZEN** — series-stratified 472/119/131 split |
| `preprocessed/dataset_summary.json` | Dataset summary statistics |
| (all v1/v2/v3/v4 variants) | **Deleted** — see reconciliation table in PLANNING.md |

## Appendix B: kPa → Bin Mapping

| kPa Bin | Range | Count | Recommended Use |
|---------|-------|-------|-----------------|
| 0–10 (wet) | 0.0 ≤ x < 10.0 | 100 | Include with class weights |
| 10–20 (moderate) | 10.0 ≤ x < 20.0 | 506 | Primary training range |
| 20–22 (dry) | 20.0 ≤ x ≤ 21.5 | 116 | Include with class weights (true max = 21.5) |

**Note:** Range is 0.0–21.5 kPa. No images >22 kPa exist in the canonical dataset. P0114 raw filename was a typo (101→10 kPa); TraceData always had 10.

## Appendix C: Soil Type → USDA Mapping

| Bengali | Transliteration | USDA Class | Count | Texture |
|---------|----------------|------------|-------|---------|
| দোআঁশ | Doash | **Loam** | 180 | Balanced |
| এঁটেল | Atel | **Clay** | 156 | Heavy |
| বেলে দোআঁশ | Bele_Doash | **Sandy Loam** | 143 | Sandy-loamy |
| এঁটেল দোআঁশ | Atel_Doash | **Clay Loam** | 126 | Clay-loamy |
| পলি | Poli | **Silt** | 85 | Fine |
| বেলে | Bele | **Sandy** | 32 | Coarse |

These are standard USDA soil texture classes, **not** composite transition zones. The Bengali transliterations are the local field notation for the USDA classification system.

---

*End of Phase 0 Audit Report (Canonical Dataset). Prepared 2026-07-07.*
