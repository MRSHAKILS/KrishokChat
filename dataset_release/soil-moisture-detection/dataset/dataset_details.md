# Dataset Details: Tensiometer-Based Soil Moisture Image Dataset

**Project:** Soil Moisture Detection (CSE498R)  
**Version:** 1.0  
**Last Updated:** 2026-07-07  
**Author:** Reza (researcher)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Collection Context](#2-collection-context)
3. [Data Composition](#3-data-composition)
4. [Naming Convention](#4-naming-convention)
5. [Image Specifications](#5-image-specifications)
6. [Pressure (kPa) Distribution](#6-pressure-kpa-distribution)
7. [Consecutive Series](#7-consecutive-series)
8. [Metadata Schema](#8-metadata-schema)
9. [Planned Labels (Unannotated)](#9-planned-labels-unannotated)
10. [Data Quality Issues](#10-data-quality-issues)
11. [Anomaly Catalog](#11-anomaly-catalog)
12. [Duplicate IDs](#12-duplicate-ids)
13. [Missing IDs](#13-missing-ids)
14. [Outlier Analysis](#14-outlier-analysis)
15. [Filename Normalization](#15-filename-normalization)
16. [EXIF Metadata](#16-exif-metadata)
17. [Train/Val/Test Split](#17-trainvaltest-split)
18. [File Inventory](#18-file-inventory)
19. [Preprocessing Pipeline](#19-preprocessing-pipeline)
20. [Known Limitations](#20-known-limitations)
21. [Recommendations](#21-recommendations)
22. [Citation](#22-citation)

---

## 1. Overview

| Attribute | Value |
|-----------|-------|
| **Dataset Name** | Tensiometer-Based Soil Moisture Image Dataset |
| **Domain** | Agricultural soil moisture detection |
| **Modality** | RGB photographs (ground-level) + tensiometer pressure readings |
| **Task Type** | Regression (kPa prediction from image) or Classification (moisture bin) |
| **Total Images** | 722 |
| **Image IDs** | P0001 – P0722 (all unique, no duplicates; 12 previously missing IDs filled from canonical source) |
| **Total Disk Size** | ~140 MB (canonical corrected images) |
| **Average File Size** | ~194 KB |
| **File Format** | JPEG (.jpg) |
| **Target Variable** | Soil water tension in kilopascals (kPa) |
| **Collection Period** | May 29 – May 31, 2026 (3 days, per TraceData) |
| **Geographic Region** | Pabna District, Rajshahi Division, Bangladesh |
| **Number of Locations** | 7 |
| **Soil Texture Labels** | 6 USDA classes (Bengali transliteration) — all labeled |
| **Crop Labels** | 14 crop types — all labeled |
| **Growth Stage Labels** | 8 stages — all labeled |
| **Land Type Labels** | High, Medium, Low — all labeled |
| **Canonical Source** | `correct_image/` + `TraceData.xlsx` from `updated_dataset/` |

---

## 2. Collection Context

### 2.1 Purpose
This dataset captures ground-level photographs of agricultural soil surfaces alongside simultaneous tensiometer readings to enable machine learning-based soil moisture estimation from visual data.

### 2.2 Data Collection Method
- **Instrument:** Tensiometer (measures soil water tension / matric potential)
- **Unit:** kilopascals (kPa)
- **Interpretation:** Lower kPa = wetter soil; Higher kPa = drier soil
- **Photography:** Handheld smartphone camera, ground-level perspective
- **Timestamp:** Visible as watermark overlay on each image (e.g., "30 May 2026 9:11 am")
- **Location:** GPS coordinates not embedded; locations identified by name only

### 2.3 Geographic Locations (7 total)

| # | Location | District | Notes |
|---|----------|----------|-------|
| 1 | Ishwardi | Pabna | Upazila headquarters |
| 2 | Pabna Sadar | Pabna | District headquarters |
| 3 | Rajapur | Pabna | Upazila |
| 4 | Shibpur | Pabna | Union area |
| 5 | Atgharia | Pabna | Upazila |
| 6 | Bera | Pabna | Upazila |
| 7 | Sujanagar | Pabna | Upazila |

All locations are within a ~30 km radius in Pabna District, Bangladesh.

### 2.4 Collection Dates

| Date | Time Range (from pixel watermarks) | Notes |
|------|-----------------------------------|-------|
| May 30, 2026 | 9:11 AM – 12:04 PM | First batch |
| May 31, 2026 | 6:56 AM – 8:58 AM | Second batch |

The last irrigation/rain date (from TraceData.xlsx) for most images is **May 29, 2026 at 4:00 PM**, meaning photos were taken the day after irrigation and the following morning — a span of ~3 calendar days but only 2 capture days.

**Limitation:** The dataset covers only 2 capture days. Seasonal variation (dry season, monsoon, winter) is not captured.

---

## 3. Data Composition

### 3.1 Image Count by Source

| Source | Count | Notes |
|--------|-------|-------|
| `correct_image/` (canonical source) | 722 | Field-team corrected images |
| `clean/` and `raw/` (copies) | 722 | Identical copies of canonical images |
| `image_manifest.csv` | 722 | One row per image, 16 columns |

### 3.2 Pressure Bin Distribution

| kPa Range | Image Count | Percentage | Moisture Level |
|-----------|-------------|------------|----------------|
| **0–10 Kpa** | 100 | 13.9% | Wet to saturated |
| **10–20 Kpa** | 506 | 70.1% | Moderate (optimal for most crops) |
| **20–30 Kpa** | 116 | 16.1% | Dry (irrigation needed) |
| **Total** | **722** | **100%** | |

**Class imbalance note:** The 10–20 Kpa range dominates with 70.1% of all images. The 0–10 Kpa range is particularly underrepresented.

### 3.3 Soil Texture Distribution (USDA Classes, Bengali Transliteration)

The `correct_image/` dataset comes with full soil texture labels from TraceData.xlsx. These are standard USDA texture classes recorded in Bengali transliteration:

| USDA Class | Bengali (Dataset Label) | Count | % |
|------------|------------------------|-------|---|
| **Loam** | Doash (দোআঁশ) | 180 | 24.9% |
| **Clay** | Atel (এঁটেল) | 156 | 21.6% |
| **Sandy Loam** | Bele_Doash (বেলে দোআঁশ) | 143 | 19.8% |
| **Clay Loam** | Atel_Doash (এঁটেল দোআঁশ) | 126 | 17.5% |
| **Silt** | Poli (পলি) | 85 | 11.8% |
| **Sandy** | Bele (বেলে) | 32 | 4.4% |

These 6 classes represent half of the 12 standard USDA soil texture classes. No images map to Loamy Sand, Sandy Clay, Silty Clay, Silty Clay Loam, Sandy Clay Loam, or Silty Loam.

### 3.4 Land Type Distribution

| Land Type | Count | % |
|-----------|-------|---|
| Medium | 308 | 42.7% |
| High | 289 | 40.0% |
| Low | 117 | 16.2% |
| Unknown | 8 | 1.1% |

### 3.5 Crop Distribution (Top 10)

| Crop | Count | % |
|------|-------|---|
| Rich | 119 | 16.5% |
| No crop | 107 | 14.8% |
| Jute | 96 | 13.3% |
| Grass | 81 | 11.2% |
| Mango | 77 | 10.7% |
| Sponge Gourd | 48 | 6.6% |
| Meheguni | 46 | 6.4% |
| Maize | 44 | 6.1% |
| Eggplant | 32 | 4.4% |
| Lemon | 28 | 3.9% |

### 3.6 Pressure Value Frequency (Top 20)

| Pressure (kPa) | Count | Percentage |
|----------------|-------|------------|
| 14.0 | 79 | 10.9% |
| 15.0 | 67 | 9.3% |
| 10.0 | 66 | 9.1% |
| 11.0 | 50 | 6.9% |
| 0.0 | 48 | 6.6% |
| 20.0 | 43 | 6.0% |
| 15.6 | 33 | 4.6% |
| 17.0 | 32 | 4.4% |
| 8.0 | 31 | 4.3% |
| 18.0 | 29 | 4.0% |
| 12.0 | 17 | 2.4% |
| 9.8 | 15 | 2.1% |
| 13.0 | 20 | 2.8% |
| 19.0 | 22 | 3.0% |
| 20.5 | 29 | 4.0% |
| 21.0 | 21 | 2.9% |
| 13.5 | 19 | 2.6% |
| 15.2 | 28 | 3.9% |
| 12.5 | 9 | 1.2% |
| 20.1 | 11 | 1.5% |

### 3.7 Unique Pressure Values

- **Total unique pressure values:** 50
- **Range:** 0.00 – 21.50 Kpa
- **Mean:** 13.74 Kpa
- **Median:** 14.00 Kpa
- **Standard deviation:** ~5.3 Kpa (estimated)
- **Most common value:** 14.0 Kpa (79 images)

---

## 4. Naming Convention

### 4.1 Original Filename Pattern

```
P{XXXX}_{pressure}Kpa.jpg
```

| Component | Format | Example | Description |
|-----------|--------|---------|-------------|
| `P` | Fixed prefix | `P` | Indicates "Picture" or sample identifier |
| `{XXXX}` | 4-digit zero-padded integer | `0001` | Sequential image ID |
| `_` | Underscore separator | `_` | Separates ID from pressure |
| `{pressure}` | Float or integer | `15.25` | Tensiometer reading in kPa |
| `Kpa` | Unit suffix | `Kpa` | Kilopascal (sometimes truncated) |
| `.jpg` | Extension | `.jpg` | JPEG format |

### 4.2 Filename Examples

| Filename | Parsed ID | Parsed kPa | Anomalies |
|----------|-----------|------------|-----------|
| `P0001_8Kpa.jpg` | P0001 | 8.0 | None |
| `P0001_8Kpa.jpg` | P0001 | 8.0 | None — canonical |
| `P0002_11Kpa.jpg` | P0002 | 11.0 | None — canonical |
| `P0065_0Kpa.jpg` | P0065 | 0.0 | None — canonical |
| `P0275_21Kpa.jpg` | P0275 | 21.0 | None — canonical |
| `P0114_10Kpa.jpg` | P0114 | 10.0 | Corrected from 101 kPa (filename typo — TraceData confirmed 10) |

### 4.3 Canonical Filename Pattern

```
P{XXXX}_{pressure}Kpa.jpg
```

| Component | Format | Example |
|-----------|--------|---------|
| `P` | Fixed prefix | `P` |
| `{XXXX}` | 4-digit zero-padded integer | `0001` |
| `_` | Underscore separator | `_` |
| `{pressure}` | Integer or decimal (no fixed decimals) | `8`, `15.25`, `9.85` |
| `Kpa` | Unit suffix | `Kpa` |
| `.jpg` | Extension | `.jpg` |

**No duplicate suffixes needed** — the canonical dataset has unique 1:1 ID→file mapping.

---

## 5. Image Specifications

### 5.1 Technical Properties

| Property | Value |
|----------|-------|
| **File format** | JPEG (.jpg) |
| **Color mode** | RGB |
| **Dimensions** | 720 x 1280 pixels (portrait) |
| **Aspect ratio** | 9:16 (portrait/vertical) |
| **Orientation** | Portrait (taller than wide) |
| **EXIF data** | None (no timestamps, GPS, or camera info) |
| **Watermark** | Visible text overlay: "location id number" + date/time |
| **Total size** | ~188 MB (canonical) |
| **Average size** | ~261 KB |
| **Min size** | ~46 KB |
| **Max size** | ~486 KB |
| **Median size** | ~262 KB |

### 5.2 Visual Content Description

The images fall into two拍摄 (shooting) perspectives:

#### Perspective A: Macro/Close-up (Most Common)
- **View angle:** Top-down, looking directly at soil surface
- **Subject:** Bare soil, organic debris, small seedlings, leaves
- **Moisture cues:** Soil color (dark = wet, light = dry), surface sheen, visible water
- **Example pressure range:** 0–21 Kpa
- **Typical contents:**
  - Soil texture (smooth muddy vs. rough dry)
  - Fallen leaves (brown, decaying)
  - Small green seedlings/weeds
  - Straw/residue from previous harvest
  - Occasional small rocks or debris

#### Perspective B: Wide/Field View (Less Common)
- **View angle:** Landscape/horizon level
- **Subject:** Entire agricultural field with crop stubble
- **Moisture cues:** Standing water, green vegetation density
- **Typical pressure range:** 0–10 Kpa (wetter conditions)
- **Typical contents:**
  - Rice paddy stubble (brown, cut stems)
  - Standing water between rows
  - Green grass/vegetation patches
  - Distant horizon with trees/power lines
  - Overcast sky

### 5.3 Visual Moisture Indicators

| kPa Range | Soil Color | Surface | Water | Vegetation |
|-----------|-----------|---------|-------|------------|
| 0–5 Kpa | Dark brown/black | Smooth, muddy | Standing water visible | Rice stubble, green patches |
| 5–10 Kpa | Dark brown | Moist, slight sheen | No standing water | Small seedlings, wet leaves |
| 10–15 Kpa | Medium brown | Moderately textured | Dry surface | Dry leaves, some green |
| 15–20 Kpa | Light-medium brown | Rough, dry texture | None | Dry straw, sparse green |
| 20–21 Kpa | Light brown/tan | Dry, crumbly | None | Dry residue, very sparse |

---

## 6. Pressure (kPa) Distribution

### 6.1 Detailed Breakdown by Fine-Grained Value

```
  0.0 Kpa:   48 images ( 6.6%)
  2.0 Kpa:    1 image  ( 0.1%)
  4.0 Kpa:    3 images ( 0.4%)
  5.0 Kpa:    1 image  ( 0.1%)
  8.0 Kpa:   31 images ( 4.3%)
  9.5 Kpa:    1 image  ( 0.1%)
  9.8 Kpa:   15 images ( 2.1%)
 10.0 Kpa:   66 images ( 9.1%)
 11.0 Kpa:   50 images ( 6.9%)
 12.0 Kpa:   17 images ( 2.4%)
 12.2 Kpa:    1 image  ( 0.1%)
 12.3 Kpa:    1 image  ( 0.1%)
 12.5 Kpa:    9 images ( 1.2%)
 12.6 Kpa:    2 images ( 0.3%)
 12.8 Kpa:    2 images ( 0.3%)
 13.0 Kpa:   20 images ( 2.8%)
 13.5 Kpa:   19 images ( 2.6%)
 14.0 Kpa:   79 images (10.9%)
 14.8 Kpa:    5 images ( 0.7%)
 14.9 Kpa:    8 images ( 1.1%)
 15.0 Kpa:   67 images ( 9.3%)
 15.2 Kpa:   28 images ( 3.9%)
 15.5 Kpa:    1 image  ( 0.1%)
 15.6 Kpa:   33 images ( 4.6%)
 16.5 Kpa:    7 images ( 1.0%)
 17.0 Kpa:   32 images ( 4.4%)
 17.1 Kpa:    1 image  ( 0.1%)
 18.0 Kpa:   29 images ( 4.0%)
 19.0 Kpa:   22 images ( 3.0%)
 19.5 Kpa:    1 image  ( 0.1%)
 19.6 Kpa:    1 image  ( 0.1%)
 19.7 Kpa:    1 image  ( 0.1%)
 19.8 Kpa:    1 image  ( 0.1%)
 19.9 Kpa:    2 images ( 0.3%)
 20.0 Kpa:   43 images ( 6.0%)
 20.1 Kpa:   11 images ( 1.5%)
 20.2 Kpa:    1 image  ( 0.1%)
 20.5 Kpa:   29 images ( 4.0%)
 20.8 Kpa:    1 image  ( 0.1%)
 21.0 Kpa:   21 images ( 2.9%)
 21.1 Kpa:    1 image  ( 0.1%)
 21.2 Kpa:    1 image  ( 0.1%)
 21.3 Kpa:    1 image  ( 0.1%)
 21.4 Kpa:    1 image  ( 0.1%)
  21.5 Kpa:    6 images ( 0.8%)
```

### 6.2 Pressure Statistics Summary

| Statistic | Value |
|-----------|-------|
| Minimum | 0.00 Kpa |
| Maximum | 21.50 Kpa |
| Mean | ~13.9 Kpa |
| Median | 14.00 Kpa |
| Unique values | 50 |
| Most frequent | 14.0 Kpa (79 images) |

**No outlier exists in the canonical dataset** — P0114's raw/ filename was a typo (101→10 kPa); the true value from TraceData.xlsx was always 10 kPa.

---

## 7. Consecutive Series

Images are organized in **consecutive series** — batches of images captured at the same location/pressure in sequence. These are important for train/test splitting to avoid data leakage.

### 7.1 Series Definition

A "series" is defined as 5+ consecutive image IDs with pressure values differing by less than 0.15 Kpa. Series likely represent the **same field photographed repeatedly** in quick succession.

### 7.2 Series Inventory

| # | Series ID | ID Range | kPa Range | Count | Primary Soil Type |
|---|-----------|----------|-----------|-------|-------------------|
| 1 | S0001 | P001 | 8.0 | 1 | Doash (Loam) |
| 2 | S0002 | P002-P003 | 11.0 | 2 | Doash (Loam) |
| 3 | S0003 | P004-P005 | 15.2 | 2 | Doash (Loam) |
| 4 | S0004 | P006 | 20.0 | 1 | Doash (Loam) |
| 5 | S0005 | P007-P012 | 15.2 | 6 | Doash (Loam) |
| 6 | S0006 | P013 | 20.0 | 1 | Bele (Sandy) |
| 7 | S0007 | P014 | 17.1 | 1 | Bele (Sandy) |
| 8 | S0008 | P015-P027 | 19.9-20.2 | 13 | Bele (Sandy) |
| 9 | S0009 | P028-P045 | 15.2 | 18 | Bele/Doash |
| 10 | S0010 | P046-P058 | 9.8 | 13 | Bele/Doash |
| 11 | S0011 | P059 | 15.2 | 1 | Bele (Sandy) |
| 12 | S0012 | P060-P061 | 19.9-20.1 | 2 | Doash (Loam) |
| 13 | S0013 | P062 | 15.2 | 1 | Bele (Sandy) |
| 14 | S0014 | P063 | 9.8 | 1 | Doash (Loam) |
| 15 | S0015 | P064-P110 | 0.0 | 47 | Bele/Poli (Sandy/Silt) |
| 16 | S0016 | P111-P166 | 9.5-10.1 | 56 | Doash (Loam) |
| 17 | S0017 | P167-P196 | 12.0-13.0 | 30 | Atel_Doash (Clay Loam) |
| 18 | S0018 | P197-P227 | 17.0 | 31 | Atel (Clay) |
| 19 | S0019 | P228-P257 | 12.5-13.5 | 30 | Atel (Clay) |
| 20 | S0020 | P258-P271 | 19.5-20.0 | 14 | Atel (Clay) |
| 21 | S0021 | P272-P278 | 21.0-21.5 | 7 | Atel (Clay) |
| 22 | S0022 | P279-P303 | 20.0 | 25 | Atel (Clay) |
| 23 | S0023 | P304-P330 | 15.0 | 27 | Poli (Silt) |
| 24 | S0024 | P331 | 17.0 | 1 | Doash (Loam) |
| 25 | S0025 | P332-P339 | 13.0-14.0 | 8 | Doash (Loam) |
| 26 | S0026 | P340 | 10.0 | 1 | Doash (Loam) |
| 27 | S0027 | P341-P343 | 13.0 | 3 | Doash (Loam) |
| 28 | S0028 | P344-P401 | 20.0-21.5 | 58 | Atel/Doash (Clay/Loam) |
| 29 | S0029 | P402-P484 | 14.8-16.5 | 83 | Atel (Clay) |
| 30 | S0030 | P485-P496 | 10.0 | 12 | Atel_Doash (Clay Loam) |
| 31 | S0031 | P497-P506 | 14.8-15.0 | 10 | Poli (Silt) |
| 32 | S0032 | P507-P554 | 11.0 | 48 | Doash (Loam) |
| 33 | S0033 | P555-P577 | 18.0-19.0 | 23 | Atel_Doash (Clay Loam) |
| 34 | S0034 | P578-P656 | 13.0-14.0 | 79 | Bele_Doash (Sandy Loam) |
| 35 | S0035 | P657-P670 | 8.0 | 14 | Bele_Doash (Sandy Loam) |
| 36 | S0036 | P671 | 5.0 | 1 | Bele_Doash (Sandy Loam) |
| 37 | S0037 | P672-P677 | 8.0 | 6 | Bele_Doash (Sandy Loam) |
| 38 | S0038 | P678-P679 | 4.0 | 2 | Bele_Doash (Sandy Loam) |
| 39 | S0039 | P680-P684 | 8.0 | 5 | Bele_Doash (Sandy Loam) |
| 40 | S0040 | P685 | 2.0 | 1 | Bele_Doash (Sandy Loam) |
| 41 | S0041 | P686-P690 | 8.0 | 5 | Bele_Doash (Sandy Loam) |
| 42 | S0042 | P691 | 0.0 | 1 | Bele_Doash (Sandy Loam) |
| 43 | S0043 | P692 | 4.0 | 1 | Bele_Doash (Sandy Loam) |
| 44 | S0044 | P693-P720 | 18.0 | 28 | Bele_Doash (Sandy Loam) |
| 45 | S0045 | P721 | 20.5 | 1 | Atel_Doash (Clay Loam) |
| 46 | S0046 | P722 | 15.6 | 1 | Doash (Loam) |

### 7.3 Series Statistics

| Metric | Value |
|--------|-------|
| Total series | 46 |
| Largest series | 83 images (S0029, IDs P402-P484, ~14.8-16.5 Kpa) |
| Smallest series | 1 image (15 singleton series) |
| Median series size | 6 images |

---

## 8. Metadata Schema

The canonical dataset includes metadata sourced from `TraceData.xlsx` (722 rows, 12 columns) merged with image filenames. The manifest is the master record.

### 8.1 Manifest Columns

| # | Column | Type | Source | Description |
|---|--------|------|--------|-------------|
| 1 | `image_id` | String | Filename | Unique image identifier (P0001–P0722) |
| 2 | `filename` | String | correct_image/ | Canonical filename |
| 3 | `kpa_raw` | Float | TraceData.xlsx | Tensiometer reading in kPa |
| 4 | `kpa_bin` | String | Derived | Categorical: 0-10, 10-20, 20-22 (true max = 21.5 kPa) |
| 5 | `soil_type` | String | TraceData.xlsx | USDA texture class (Bengali transliteration: Doash, Atel, Bele, Poli, Bele_Doash, Atel_Doash) |
| 6 | `land_type` | String | TraceData.xlsx | High, Medium, Low |
| 7 | `crop` | String | TraceData.xlsx | Primary crop (14 types) |
| 8 | `growth_stage` | String | TraceData.xlsx | Growth stage (8 stages) |
| 9 | `rain_date` | Date | TraceData.xlsx | Last irrigation/rain date |
| 10 | `rain_time` | Time | TraceData.xlsx | Last irrigation/rain time |
| 11 | `capture_date` | Date | TraceData.xlsx | Collection date |
| 12 | `capture_time` | Time | TraceData.xlsx | Collection time |
| 13 | `location` | String | TraceData.xlsx | Location name |
| 14 | `series_id` | String | Derived | Series group ID (S0001–S0046) |
| 15 | `series_size` | Integer | Derived | Number of images in series |
| 16 | `file_size` | Integer | Filesystem | Image file size in bytes |

### 8.2 Annotation Status

| Status | Count |
|--------|-------|
| Auto-filled from TraceData.xlsx | **11 columns** (all labels) |
| Derived from analysis | 3 columns (kpa_bin, series_id, series_size) |
| From filesystem | 1 column (file_size) |
| **Unlabeled** | **0 columns** |

All metadata columns are fully populated. No manual annotation needed.

---

## 9. Soil Type Labels (Fully Annotated from TraceData.xlsx)

### 9.1 Soil Texture Classes (6 USDA classes)

All images have soil texture labels from `TraceData.xlsx`. The labels use Bengali transliteration of standard USDA soil texture classes:

| Bengali Label | Transliteration | USDA Class | Count | Description |
|---------------|----------------|------------|-------|-------------|
| দোআঁশ | Doash | **Loam** | 180 | Balanced sand/silt/clay, ideal for farming |
| এঁটেল | Atel | **Clay** | 156 | Heavy, retains water, slow drainage |
| বেলে দোআঁশ | Bele_Doash | **Sandy Loam** | 143 | Sandy with some loam, drains quickly |
| এঁটেল দোআঁশ | Atel_Doash | **Clay Loam** | 126 | Clay mixed with loam |
| পলি | Poli | **Silt** | 85 | Fine particles, moderate drainage |
| বেলে | Bele | **Sandy** | 32 | Fast-draining, low water retention |

### 9.2 Actual Crop Types (14 types from TraceData.xlsx)

| # | Crop | Count | % |
|---|------|-------|---|
| 1 | Rich (ধান) | 119 | 16.5% |
| 2 | No crop | 107 | 14.8% |
| 3 | Jute (পাট) | 96 | 13.3% |
| 4 | Grass (ঘাস) | 81 | 11.2% |
| 5 | Mango (আম) | 77 | 10.7% |
| 6 | Sponge Gourd (লাউ) | 48 | 6.6% |
| 7 | Meheguni (মেহগনি) | 46 | 6.4% |
| 8 | Maize (ভুট্টা) | 44 | 6.1% |
| 9 | Eggplant (বেগুন) | 32 | 4.4% |
| 10 | Lemon (লেবু) | 28 | 3.9% |
| 11 | Lechee (লিচু) | 19 | 2.6% |
| 12 | Okra (ঢেঁড়স) | 13 | 1.8% |
| 13 | Betel_Nut (সুপারি) | 11 | 1.5% |
| 14 | Turmeric (হলুদ) | 1 | 0.1% |

### 9.3 Actual Growth Stages (8 stages from TraceData.xlsx)

| # | Stage | Count | % | Description |
|---|-------|-------|---|-------------|
| 1 | Mature | 280 | 38.8% | Crop ready or nearly ready for harvest |
| 2 | Seedling | 100 | 13.9% | Early emergence, tiny green sprouts |
| 3 | Pre_hervest | 79 | 10.9% | Pre-harvest stage |
| 4 | Post_Harvest | 62 | 8.6% | After harvest, bare/stubble field |
| 5 | Fruiting | 60 | 8.3% | Fruit/seed development visible |
| 6 | Seed_Sowing | 60 | 8.3% | Just planted, bare soil |
| 7 | Post-Harvest | 48 | 6.6% | (variant spelling) |
| 8 | Land_Preparation | 25 | 3.5% | Soil tilled, ready for sowing |

**Note:** Stages Pre_hervest and Post_Harvest are likely pre-harvest and post-harvest. There are two variant spellings of Post-Harvest (with and without underscore). These should be standardized before analysis.

### 9.4 Land Types (3 types from TraceData.xlsx)

| Type | Count | Description |
|------|-------|-------------|
| Medium | 308 (42.7%) | Standard agricultural land |
| High | 289 (40.0%) | Elevated land, well-drained |
| Low | 117 (16.2%) | Low-lying, flood-prone |
| Unknown | 8 (1.1%) | 8 inferred images (no TraceData row) |

**Note:** Weather condition labels are not available in the dataset. The rainfall date field records the last irrigation/rain event, not current weather.

---

## 10. Data Quality Issues (Canonical Dataset)

### 10.1 Summary

| Issue Category | Count | Severity | Status |
|---------------|-------|----------|--------|
| Filename anomalies | 0 (all resolved by field team) | ✅ Resolved | N/A |
| Duplicate image IDs | 0 (all resolved by canonical dataset) | ✅ Resolved | N/A |
| Missing IDs in sequence | 0 (all 12 filled by canonical dataset) | ✅ Resolved | N/A |
| Outlier pressure values | 0 (P0114 corrected to 10 kPa) | ✅ Resolved | N/A |
| No EXIF metadata | 722 files | Medium | Ongoing |
| No location GPS | 722 files | Medium | Ongoing |
| No capture date/time | 722 files (DATE/TIME empty in TraceData) | Medium | Ongoing |
| Class imbalance (70% in 10-20 kPa) | 3 bins | High | Ongoing |
| Narrow temporal coverage (3 days) | May 29-31 | High | Cannot fix |
| 8 inferred images (no TraceData row) | 8 files (1.1%) | Low | Acceptable |
| **Contamination: P0029 (foot)** | 1 file | High | Exclude from training (confirmed visually) |
| **Contamination: P0166 (hand)** | 1 file | High | Exclude from training (confirmed visually 2026-07-08) |
| **Viewpoint shift: P0677 (wide field)** | 1 file | Medium | Flag; may need separate bucket in Phase 3 |
| **Orientation inconsistency** | 125 landscape/non-standard of 722 | Medium | Center-crop to square before model input |

### 10.2 Severity Definitions

- **High:** Could cause incorrect model training or evaluation
- **Medium:** Reduces data quality but manageable with preprocessing
- **Low:** Minor inconsistency, no impact on modeling

---

## 11. Anomaly Catalog (Historical)

The following are issues found in the **original raw/ directory** that were resolved by the canonical dataset. They are preserved for documentation only.

### 11.1 Historical Filename Anomalies (Resolved by Canonical Dataset)

| Filename (raw/) | Anomaly Type | Resolution in Canonical Dataset |
|-----------------|-------------|-------------------------------|
| P0039_15.15Kp.jpg | Truncated unit | Corrected in `correct_image/` |
| P0049_985Kpa.jpg | Missing decimal | Corrected |
| P0050_9,85Kpa.jpg → P0059_9,85Kpa.jpg | Comma decimal (10 files) | Corrected |
| P0053_9,85Kp.jpg | Comma + truncated | Corrected |
| P0114_101Kpa.jpg | Outlier value | Corrected to `P0114_10Kpa.jpg` |

**All are resolved.** The canonical `correct_image/` has no filename anomalies.

### 11.2 Active Anomalies in Canonical Dataset

| ID | Type | Detail | Action |
|----|------|--------|--------|
| P0029 | Contamination | Human foot + blue fabric in frame | **Exclude from training** (confirmed visually 2026-07-08) |
| P0166 | Contamination | Human hand touching soil (upper-right) | **Exclude from training** (found 2026-07-08) |
| P0002, P0003 | Visual-label mismatch | Same kPa (11), different crops (Lechee vs Mango); brightness diff only 2.7 | Flagged — note in paper |
| P0677 | Viewpoint shift | Wide-angle paddy field, not macro soil close-up | Flag in metadata; consider separate viewpoint bucket in Phase 3 |
| P0171, P0172, P0183, P0184, P0339, P0340, P0670, P0671 | Inferred metadata | Not in TraceData.xlsx; inferred from nearest neighbor | Flagged — <1.1% of dataset, visually confirmed consistent |

### 11.3 Orientation Summary (Canonical Dataset)

| Orientation | Count | Notes |
|-------------|-------|-------|
| Portrait 720×1280 | 565 | Standard |
| Landscape 1280×720 | 82 | Intentional horizontal shot (watermark proves not OS-rotated) |
| Landscape 1280×964 | 41 | Intentional horizontal shot |
| Portrait 964×1280 | 32 | Taller portrait |
| Tiny (595×438, 720×521) | 2 | Odd; verify before training |

**All 125 non-standard images are valid soil photos.** They must be center-cropped to square (not rotated) before model input. See Section 19 for preprocessing.

---

## 12. Duplicate IDs (Resolved in Canonical Dataset)

In the original raw/ data, 4 IDs (P0176, P0187, P0342, P0677) had dual files with conflicting kPa values. The canonical `correct_image/` dataset resolves all duplicates — each ID now has a **single corrected file** matching the TraceData.xlsx value.

| Original ID | Old Raw Conflict (2 files each) | Canonical Resolution |
|-------------|-------------------------------|---------------------|
| P0176 | 12.5 vs 12.6 Kpa | `P0176_12Kpa.jpg` (12.0 Kpa, from TraceData) |
| P0187 | 12.0 vs 12.8 Kpa | `P0187_12Kpa.jpg` (12.0 Kpa, from TraceData) |
| P0342 | 10.0 (278 KB) vs 13.0 (1020 KB) Kpa | `P0342_13Kpa.jpg` (13.0 Kpa, from TraceData) |
| P0677 | 5.0 vs 8.0 Kpa | `P0677_8Kpa.jpg` (8.0 Kpa, from TraceData) |

**No duplicate IDs remain** in the canonical dataset.

---

## 13. Missing IDs (Filled by Canonical Dataset)

The original `raw/` directory had 12 missing IDs in the P0001–P0730 sequence. The canonical `correct_image/` dataset **fills all 12 gaps** with corrected images:

| Previously Missing | Canonical File | kPa |
|-------------------|----------------|-----|
| P0017 | `P0017_20.15Kpa.jpg` | 20.15 |
| P0113 | `P0113_9.5Kpa.jpg` | 9.5 |
| P0153 | `P0153_10Kpa.jpg` | 10.0 |
| P0154 | `P0154_10Kpa.jpg` | 10.0 |
| P0164 | `P0164_10Kpa.jpg` | 10.0 |
| P0464 | `P0464_15Kpa.jpg` | 15.0 |
| P0547 | `P0547_11Kpa.jpg` | 11.0 |
| P0559 | `P0559_19Kpa.jpg` | 19.0 |
| P0578 | `P0578_14Kpa.jpg` | 14.0 |
| P0634 | `P0634_14Kpa.jpg` | 14.0 |
| P0678 | `P0678_4Kpa.jpg` | 4.0 |
| P0688 | `P0688_8Kpa.jpg` | 8.0 |

**All 722 image IDs from P0001–P0722 are now present** (IDs P0723–P0730 never existed — the sequence ends at P0722).

---

## 14. P0114 Analysis — Filename Typo, Not a Sensor Spike

### What Actually Happened

| Attribute | Value |
|-----------|-------|
| **Raw/ filename** | `P0114_101Kpa.jpg` (typo — someone typed 101 instead of 10) |
| **TraceData.xlsx entry** | `P0114_10Kpa.jpg`, Kpa=**10** (field log — correct) |
| **Canonical file** | `P0114_10Kpa.jpg` (matches field log) |
| **Canonical kPa** | **10.0 Kpa** (verified in TraceData, row 115) |
| **Crop / Soil** | Jute / Doash (Loam) |
| **Series** | S0016 (P0111–P0166, 9.5–10.1 Kpa range) |

### Resolution

**The 101 Kpa reading was a filename entry error, not a sensor spike.** The tensiometer read 10 Kpa correctly — matching the nearby images P0112 (9.85 Kpa) and P0115 (9.5 Kpa) in the same series. The original old-audit conclusion ("sensor spike, 2.4x larger file, exceeds tensiometer range") was based on the wrong filename; the canonical file `P0114_10Kpa.jpg` has normal size and is consistent with its neighbors.

**No outlier exists in the canonical dataset.** The maximum kPa value is 21.5.

---

## 15. Filename Normalization (Canonical Dataset)

The canonical `correct_image/` dataset uses corrected filenames directly — the field team already resolved all anomalies. The `clean/` directory is a direct copy of `correct_image/`.

### 15.1 Key Differences Between Raw and Canonical Filenames

The canonical filenames were corrected for:

| Issue | Raw Example | Canonical Example |
|-------|-------------|-------------------|
| Comma decimal | `P0050_9,85Kpa.jpg` | `P0050_9.85Kpa.jpg` |
| Missing decimal | `P0049_985Kpa.jpg` | `P0049_9.85Kpa.jpg` |
| Truncated unit | `P0039_15.15Kp.jpg` | `P0039_15.15Kpa.jpg` |
| Outlier value | `P0114_101Kpa.jpg` | `P0114_10Kpa.jpg` |
| Anomalous ID padding | `P00060_15.25Kpa.jpg` | `P0060_19.85Kpa.jpg` (reassigned) |
| Missing IDs | (12 gaps) | All filled with corrected images |

### 15.2 Normalization: 106 kPa Value Corrections

Beyond filename fixes, the canonical dataset corrected **106 kPa values** that were recorded incorrectly in the raw filenames. Examples:

| Image | Raw kPa | Canonical kPa | Change |
|-------|---------|---------------|--------|
| P0028 | 19.95 | 15.25 | -4.70 |
| P0046 | 15.15 | 9.85 | -5.30 |
| P0064 | 9.85 | 0.0 | -9.85 |
| P0114 | 101.0 | 10.0 | -91.0 |
| P0167 | 10.0 | 12.0 | +2.0 |

### 15.3 All 722 Canonical Filenames

The canonical filenames match `correct_image/` (P0001_8Kpa.jpg through P0722_15.6Kpa.jpg) and are copied verbatim to `clean/` and `raw/`.

---

## 16. EXIF Metadata

### 16.1 EXIF Extraction Results

| Property | Result |
|----------|--------|
| Images with EXIF | **0** (0%) |
| Images without EXIF | **722** (100%) |
| EXIF errors | 0 |

### 16.2 Available Image Properties

| Property | Value | Source |
|----------|-------|--------|
| Width | 720 px | Image header |
| Height | 1280 px | Image header |
| Format | JPEG | File extension |
| Color mode | RGB | Image header |
| File size | 65–474 KB | Filesystem |
| Timestamps | None | Not embedded |
| GPS coordinates | None | Not embedded |
| Camera model | None | Not embedded |

### 16.3 Watermark Content

Each image contains a visible text watermark (pixel-embedded, not EXIF):

```
location id number
30 May 2026 9:11 am
```

To extract these programmatically, **OCR (Optical Character Recognition)** would be required.

---

## 17. Train/Val/Test Split

### 17.1 Split Configuration

| Parameter | Value |
|-----------|-------|
| Train ratio | ~65% |
| Validation ratio | ~17% |
| Test ratio | ~18% |
| Random seed | 42 |
| Splitting method | Group-aware (series stay together) |
| Stratification | By soil_type + kpa_bin |

### 17.2 Split Results

| Split | Count | % | 0-10 Kpa | 10-20 Kpa | 20-22 Kpa |
|-------|-------|---|----------|-----------|-----------|
| **Train** | 472 | 65.4% | 84 | 344 | 44 |
| **Val** | 119 | 16.5% | 3 | 58 | 58 |
| **Test** | 131 | 18.1% | 13 | 104 | 14 |

### 17.3 Leakage Prevention

- **Series leakage check:** PASS — No consecutive series spans multiple splits
- **Method:** All images from the same series are assigned to the same split
- **Stratification:** Stratified by soil_type × kpa_bin to ensure each split covers all soil textures

---

## 18. File Inventory

### 18.1 Directory Structure

```
Soil Moisture Detection/
├── dataset/
│   ├── dataset_details.md              # This file (full documentation)
│   ├── raw/                            # 722 canonical JPEGs (from correct_image/)
│   ├── clean/                          # 722 canonical JPEGs (same as raw/)
│   ├── updated_dataset/                # Canonical data source
│   │   ├── correct_image/              # 722 corrected images (THE canonical set)
│   │   ├── TraceData.xlsx              # Full metadata (722 rows, 12 columns)
│   │   └── trace_deta_analysis.xlsx    # Summary analysis
│   ├── preprocessed/
│   │   ├── image_manifest.csv      # **FROZEN** — 722 rows, 16 cols. Single source of truth.
│   │   ├── split_assignment.csv    # **FROZEN** — 472/119/131 split
│   │   └── dataset_summary.json    # Summary statistics
│   ├── scripts/
│   │   ├── rebuild_canonical_dataset_step2b.py     # Build canonical manifest
│   │   ├── fix_unmatched_metadata_step2c.py        # Fix 8 unmatched images
│   │   ├── finalize_canonical_manifest_step2d.py   # Finalize + split
│   │   ├── analyze_soil_types_step3a.py            # Soil type taxonomy analysis
│   │   ├── check_soil_types_step1a.py              # Image feature extraction
│   │   ├── select_cluster_samples_step1b.py        # Cluster sampling
│   │   └── merge_updated_metadata_step2a.py        # Initial merge attempt
│   └── reports/
│       ├── PHASE0_AUDIT_REPORT.md      # Phase 0 data integrity audit
│       ├── preprocessing_report.md     # Preprocessing summary
│       └── canonical_migration_log.md  # Canonical dataset migration notes
├── literature review/                  # Literature review materials
├── docs/                               # Project documentation
└── paper/                              # Research paper
```

### 18.2 Key File Sizes

| File/Directory | Size | Contents |
|---------------|------|----------|
| `dataset/raw/` | ~140 MB | 722 canonical JPEGs (from correct_image/) |
| `dataset/clean/` | ~140 MB | 722 canonical JPEGs (same as raw/) |
| `dataset/updated_dataset/` | ~1 MB | Canonical data source (TraceData.xlsx + correct_image/) |
| `dataset/preprocessed/image_manifest.csv` | ~80 KB | 722 rows, 16 columns — canonical manifest |
| `dataset/preprocessed/split_assignment.csv` | ~20 KB | 722 rows — train/val/test assignments |
| `dataset/preprocessed/dataset_summary.json` | ~2 KB | Dataset summary statistics |

---

## 19. Preprocessing Pipeline

### 19.1 Canonical Dataset Build Pipeline

The canonical dataset was built using scripts in `dataset/scripts/`. Unlike traditional preprocessing, the field team delivered corrected images — the scripts exist to **merge, validate, and split** the already-processed data.

| Step | Script | Input | Output |
|------|--------|-------|--------|
| 2a | `merge_updated_metadata_step2a.py` | `correct_image/` + `TraceData.xlsx` | Canonical manifest v1 |
| 2b | `rebuild_canonical_dataset_step2b.py` | `correct_image/` + `TraceData.xlsx` | `image_manifest.csv` |
| 2c | `fix_unmatched_metadata_step2c.py` | 8 unmatched images | Gap analysis report |
| 2d | `finalize_canonical_manifest_step2d.py` | Manifest + gap analysis | Final manifest + `split_assignment.csv` |
| 3a | `analyze_soil_types_step3a.py` | Manifest | Soil type taxonomy analysis |

The original preprocessing pipeline (`preprocess_step0.py` through `split_planner_step0d.py`) was used on the deprecated `raw/` data and should **not** be re-run on the canonical dataset.

### 19.2 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Python | 3.12+ | Runtime |
| openpyxl | 3.1.5 | Excel file reading (TraceData.xlsx) |
| Pillow | 10.4.0 | Image reading |
| Standard library | - | csv, json, re, os, shutil |

### 19.3 Regenerating the Canonical Manifest

To regenerate from scratch:
```bash
# Ensure updated_dataset/correct_image/ and updated_dataset/TraceData.xlsx exist
python dataset/scripts/merge_updated_metadata_step2a.py
python dataset/scripts/rebuild_canonical_dataset_step2b.py
python dataset/scripts/fix_unmatched_metadata_step2c.py
python dataset/scripts/finalize_canonical_manifest_step2d.py
```

**Note:** The canonical source (`correct_image/` + `TraceData.xlsx`) is the *only* authoritative source. Do NOT use the original `raw/` directory.

---

## 20. Known Limitations

| # | Limitation | Impact | Mitigation |
|---|-----------|--------|------------|
| 1 | **Class imbalance** (70% in 10-20 kPa) | Model biased toward moderate moisture | Per-bin RMSE, class weights, oversampling |
| 2 | **Narrow temporal scope** (2 capture days) | No seasonal variation captured | Document as limitation; plan future collection |
| 3 | **Geographic concentration** (Pabna only) | Limited generalizability | Test on external datasets if available |
| 4 | **No EXIF metadata** | No timestamps, GPS, camera info | Rely on watermark OCR if needed |
| 5 | **No capture date/time in TraceData** | DATE/TIME and Location columns empty | Temporal info from watermarks only |
| 6 | **Portrait orientation** (720×1280) | Non-standard for many models | Resize/augment during training |
| 7 | **Single-site collection** | Cannot assess cross-site variability | Document as limitation |
| 8 | **8 inferred images** (1.1%) | Slight metadata uncertainty for 8/722 | Flagged; minimal impact |
| 9 | **Contamination (P0029 foot in frame)** | Spurious visual feature | Flagged; exclude from training |
| 10 | **P0002/P0003 visual-label mismatch** | Same kPa, different appearance | Flagged; document as data quality issue |
| 11 | **No multi-modal data** | Only RGB + kPa | Could add soil sensors, weather APIs |
| 12 | **Small dataset** (722 images) | Limited for deep learning | Use transfer learning, augmentation |

---

## 21. Recommendations

### 21.1 Completed Actions

1. ✅ **Outlier P0114 resolved** — Corrected to 10 kPa by field team in canonical dataset
2. ✅ **Metadata fully labeled** — All 12 columns populated from TraceData.xlsx
3. ✅ **Stratified split generated** — 472/119/131, stratified by soil_type × kpa_bin
4. ✅ **Missing IDs filled** — All 12 previously missing IDs present in canonical dataset

### 21.2 For Model Training

1. **Use `dataset/clean/`** as input (canonical images)
2. **Use `dataset/preprocessed/split_assignment.csv`** for train/val/test grouping
3. **Keep series together** — Never split a series across train/test
4. **Apply per-bin metrics** — Report RMSE separately for 0-10, 10-20, 20-22 kPa bins
5. **Use transfer learning** — Pre-trained ImageNet models fine-tuned
6. **Data augmentation** — Rotation, flip, color jitter (images are portrait)
7. **Input resolution** — Resize to 224×224 or 384×384 for standard models

### 21.3 For Future Data Collection

1. **Enable EXIF GPS** on collection device
2. **Collect more days** — Cover dry season, monsoon, winter
3. **Expand locations** — Include other Bangladesh districts
4. **Balance pressure bins** — Target equal samples per kPa range
5. **Add soil sensors** — pH, organic matter, electrical conductivity
6. **Record capture dates** — The DATE/TIME columns in TraceData were empty;
   ensure timestamps are captured in future collections

---

## 22. Citation

If you use this dataset in your research, please cite:

```
Tensiometer-Based Soil Moisture Image Dataset.
Collected: May 30-31, 2026.
Pabna District, Rajshahi Division, Bangladesh.
722 RGB images with simultaneous tensiometer readings (0-21.5 kPa).
CSE498R Research Project.
```

---

## Appendix A: Complete kPa Value List

All 50 unique pressure values found in the dataset:

```
0.00, 2.00, 4.00, 5.00, 8.00, 9.50, 9.80, 10.00, 11.00, 12.00,
12.20, 12.30, 12.50, 12.60, 12.80, 13.00, 13.50, 14.00, 14.75,
14.80, 14.85, 14.90, 14.95, 15.00, 15.15, 15.20, 15.25, 15.50,
15.60, 16.50, 17.00, 17.10, 17.15, 18.00, 19.00, 19.50, 19.60,
19.70, 19.80, 19.85, 19.90, 19.95, 20.00, 20.10, 20.15, 20.20,
20.25, 20.50, 20.80, 21.00, 21.10, 21.20, 21.30, 21.40, 21.50
```

**Note:** P0114 was originally mis-typed as "101 kPa" in the raw filename. The correct field-log value is 10 kPa and is NOT an outlier. Value does not appear in this list.

## Appendix B: File Hash Verification

To verify dataset integrity, compute SHA-256 hashes:

```bash
# Windows PowerShell (run from dataset/)
Get-ChildItem "clean\*.jpg" | ForEach-Object {
    [PSCustomObject]@{
        File = $_.Name
        Hash = (Get-FileHash $_.FullName -Algorithm SHA256).Hash
    }
} | Export-Csv "dataset_checksums_canonical.csv" -NoTypeInformation
```

## Appendix C: Quick Start

```bash
# 1. Canonical dataset already built. Verify:
python -c "import csv; rows=list(csv.DictReader(open('dataset/preprocessed/image_manifest.csv'))); print(f'Images: {len(rows)}, span: {rows[0][\"image_id\"]}-{rows[-1][\"image_id\"]}')"

# 2. Verify output
dir dataset\preprocessed\image_manifest.csv
dir dataset\clean\ | Measure-Object   # Should show 722 files

# 3. Load canonical manifest
import pandas as pd
df = pd.read_csv("dataset/preprocessed/image_manifest.csv")
print(f"Images: {len(df)}, kPa range: {df['kpa_raw'].min()}-{df['kpa_raw'].max()}")
print(f"Soil types: {df['soil_type'].value_counts().to_dict()}")

# 4. Load split assignments
splits = pd.read_csv("dataset/preprocessed/split_assignment.csv")
print(splits['split'].value_counts())

# 5. Images are in clean/ directory
# Images are already 720x1280 RGB JPEGs, ready for model input
```
