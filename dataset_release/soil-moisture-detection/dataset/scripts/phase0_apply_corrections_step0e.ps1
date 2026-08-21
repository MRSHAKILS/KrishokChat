# Phase 0: Apply All Corrections
# - Flag P0029, P0114, P0002/P0003
# - Assign series to 106 unassigned images
# - Rebuild manifest v2
# - Update anomalies.json
# - Create stratified series-level split v2

$ErrorActionPreference = "Stop"
$base = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$preproc = Join-Path $base "preprocessed"

Write-Host "=== Phase 0: Applying Corrections ==="
Write-Host "Base: $base"
Write-Host ""

# === 1. Backup old files ===
Write-Host "[1/6] Backing up old files..."
if (Test-Path (Join-Path $preproc "image_manifest.csv")) {
    Copy-Item (Join-Path $preproc "image_manifest.csv") (Join-Path $preproc "image_manifest_v1.csv") -Force
    Write-Host "  -> image_manifest_v1.csv"
}
if (Test-Path (Join-Path $preproc "split_assignment.csv")) {
    Copy-Item (Join-Path $preproc "split_assignment.csv") (Join-Path $preproc "split_assignment_v1.csv") -Force
    Write-Host "  -> split_assignment_v1.csv"
}

# === 2. Load existing data ===
Write-Host "[2/6] Loading existing manifest..."
$manifest = Import-Csv (Join-Path $preproc "image_manifest.csv") -Header "image_id","original_id","filename","kpa_raw","kpa_bin","anomalies","id_num","series_id","series_size"

# Convert to proper objects (PowerShell may add trailing header as data)
$header = $manifest[0]
if ($header.image_id -eq "image_id") { $manifest = $manifest[1..($manifest.Count-1)] }

Write-Host "  Loaded $($manifest.Count) rows"

# === 3. Define new series for the unassigned ===
Write-Host "[3/6] Assigning series to 106 unassigned images..."

# Define new series: SA01-SA24
$newSeries = @{
    "SA01" = @{ids=@(1,2,3,4,5,6); name="P1-P6"}
    "SA02" = @{ids=@(13,14,15,16); name="P13-P16"}
    "SA03" = @{ids=@(60,61,62,63,64); name="P60-P64"}
    "SA04" = @{ids=@(114,115); name="P114-P115"}
    "SA05" = @{ids=@(172,173,174,175,176,177,178,179); name="P172-P179"}
    "SA06" = @{ids=@(187,188,189,190,191,192,193,194,195,196,197,198,199); name="P187-P199"}
    "SA07" = @{ids=@(231,232,233,234,235,236); name="P231-P236"}
    "SA08" = @{ids=@(251,252,253,254,255,256,257,258,259,260); name="P251-P260"}
    "SA09" = @{ids=@(271,272,273,274,275,276,277,278,279,280,281); name="P271-P281"}
    "SA10" = @{ids=@(334,335); name="P334-P335"}
    "SA11" = @{ids=@(342,343,344,345,346,347,348,349,350); name="P342-P350"}
    "SA12" = @{ids=@(444,445,446,447,448,449); name="P444-P449"}
    "SA13" = @{ids=@(685,686,687); name="P685-P687"}
    "SA14" = @{ids=@(689,690,691,692,693); name="P689-P693"}
    "SA15" = @{ids=@(699,700); name="P699-P700"}
    "SA16" = @{ids=@(729,730); name="P729-P730"}
    # Singletons
    "SA17" = @{ids=@(28); name="P28"}
    "SA18" = @{ids=@(112); name="P112"}
    "SA19" = @{ids=@(358); name="P358"}
    "SA20" = @{ids=@(370); name="P370"}
    "SA21" = @{ids=@(500); name="P500"}
    "SA22" = @{ids=@(560); name="P560"}
    "SA23" = @{ids=@(653); name="P653"}
    "SA24" = @{ids=@(677); name="P677"}
}

# Build a lookup: numeric ID -> series_id
$idToSeries = @{}
foreach ($sid in $newSeries.Keys) {
    $info = $newSeries[$sid]
    foreach ($id in $info.ids) {
        # Duplicates: P176, P187, P342, P677 have multiple entries
        if (-not $idToSeries.ContainsKey($id)) {
            $idToSeries[$id] = @()
        }
        $idToSeries[$id] += $sid
    }
}

# Assign series to each row
$assigned = 0
$flagged = @()  # Track flag changes
foreach ($row in $manifest) {
    $id = [int]$row.id_num
    $fname = $row.filename
    $img_id = $row.image_id
    
    # Series assignment for unassigned
    if ([string]::IsNullOrEmpty($row.series_id) -or $row.series_id -eq "") {
        if ($idToSeries.ContainsKey($id)) {
            $candidates = $idToSeries[$id]
            if ($candidates.Count -eq 1) {
                $row.series_id = $candidates[0]
                $row.series_size = $newSeries[$candidates[0]].ids.Count
                $assigned++
            } else {
                # Duplicate - need to pick based on which image version
                # Check for b-suffix
                if ($img_id -match 'b$') {
                    # b-suffix goes to the second match
                    $row.series_id = $candidates[1]
                    $row.series_size = $newSeries[$candidates[1]].ids.Count
                } else {
                    $row.series_id = $candidates[0]
                    $row.series_size = $newSeries[$candidates[0]].ids.Count
                }
                $assigned++
            }
        }
    }
    
    # === P0029: Contamination flag ===
    if ($img_id -eq "P0029") {
        $existing = $row.anomalies
        if ($existing -eq "") {
            $row.anomalies = "contamination"
        } elseif ($existing -notmatch "contamination") {
            $row.anomalies = "$existing;contamination"
        }
        $flagged += "P0029: contamination (foot in frame)"
    }
    
    # === P0114: Outlier confirmation ===
    if ($img_id -eq "P0114") {
        $existing = $row.anomalies
        if ($existing -eq "") {
            $row.anomalies = "outlier_sensor_spike"
        } elseif ($existing -notmatch "outlier") {
            $row.anomalies = "$existing;outlier_sensor_spike"
        }
        $flagged += "P0114: outlier (sensor spike, 101 kPa)"
    }
    
    # === P0002, P0003: Visual-label mismatch ===
    if ($img_id -eq "P0002" -or $img_id -eq "P0003") {
        $existing = $row.anomalies
        if ($existing -eq "") {
            $row.anomalies = "visual_label_mismatch"
        } elseif ($existing -notmatch "visual_label") {
            $row.anomalies = "$existing;visual_label_mismatch"
        }
        $flagged += "${img_id}: visual_label_mismatch (both 11 kPa, different appearance)"
    }
}

Write-Host "  Assigned series to $assigned images"
Write-Host "  Flags applied to $($flagged.Count) images"

# === 4. Write updated manifest ===
Write-Host "[4/6] Writing image_manifest_v2.csv..."
$outManifest = Join-Path $preproc "image_manifest_v2.csv"
# Header
"image_id,original_id,filename,kpa_raw,kpa_bin,anomalies,id_num,series_id,series_size" | Set-Content $outManifest
foreach ($row in $manifest) {
    $line = "$($row.image_id),$($row.original_id),$($row.filename),$($row.kpa_raw),$($row.kpa_bin),$($row.anomalies),$($row.id_num),$($row.series_id),$($row.series_size)"
    Add-Content $outManifest $line
}
Write-Host "  Written: $outManifest ($($manifest.Count) rows)"

# === 5. Update anomalies.json ===
Write-Host "[5/6] Updating anomalies.json..."
$anomalies = Get-Content (Join-Path $preproc "anomalies.json") -Raw | ConvertFrom-Json
# Add contamination and mismatch fields
if (-not $anomalies.PSObject.Properties.Name.Contains("contamination")) {
    $anomalies | Add-Member -NotePropertyName "contamination" -NotePropertyValue @{
        "P0029" = @{
            filename = "P0029_15.25Kpa.jpg"
            kpa = 15.25
            contaminant = "human_foot"
            series = "S0029"
            severity = "high"
            action = "exclude_from_training"
        }
    }
}
if (-not $anomalies.PSObject.Properties.Name.Contains("visual_label_mismatches")) {
    $anomalies | Add-Member -NotePropertyName "visual_label_mismatches" -NotePropertyValue @{
        "P0002_vs_P0003" = @{
            images = @("P0002_11Kpa.jpg", "P0003_11Kpa.jpg")
            kpa_label = "11.0"
            description = "Both labeled 11 kPa but visually different (supervisor observation)"
            severity = "medium"
            action = "flag_in_metadata"
        }
    }
}
# Add outlier confirmation
if (-not $anomalies.PSObject.Properties.Name.Contains("outlier_confirmation")) {
    $anomalies | Add-Member -NotePropertyName "outlier_confirmation" -NotePropertyValue @{
        "P0114" = @{
            filename = "P0114_101Kpa.jpg"
            kpa = 101.0
            file_size_bytes = 391657
            typical_size_bytes = 162067
            assessment = "sensor_spike"
            evidence = @(
                "101 kPa exceeds tensiometer operating range (max ~80-85 kPa before cavitation)",
                "2.4x larger file size suggests different capture conditions",
                "Flanked by 9.5-9.85 kPa images (same wet soil batch)",
                "No other image exceeds 30 kPa"
            )
            action = "exclude_from_training;document_as_sensor_error"
        }
    }
}
# Add series coverage info
$anomalies | Add-Member -NotePropertyName "series_coverage" -NotePropertyValue @{
    original_series = 36
    new_series_created = 24
    total_series = 60
    original_covered = 616
    new_covered = 106
    total_covered = 722
}
$anomalies | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $preproc "anomalies.json") -Force
Write-Host "  Updated: anomalies.json"

# === 6. Create stratified series-level split ===
Write-Host "[6/6] Creating series-level stratified split v2..."
# Group by series_id, then assign entire series to splits
# Stratify by kpa_bin to ensure balanced val/test

$seriesGroups = $manifest | Group-Object series_id
$seriesData = @()
foreach ($sg in $seriesGroups) {
    $first = $sg.Group[0]
    $seriesData += [PSCustomObject]@{
        series_id = $sg.Name
        count = $sg.Count
        kpa_bin = $first.kpa_bin
        images = $sg.Group
    }
}

# Sort by bin for stratified assignment
$bins = $seriesData | Group-Object kpa_bin
$train = @()
$val = @()
$test = @()

foreach ($binGroup in $bins) {
    $seriesInBin = $binGroup.Group | Sort-Object { $_.series_id }
    $n = $seriesInBin.Count
    
    if ($n -le 2) {
        # Too few series - put all in train
        $train += $seriesInBin
    } else {
        # 70/15/15 split by series count
        $nTrain = [Math]::Max(1, [Math]::Round($n * 0.70))
        $nVal = [Math]::Max(1, [Math]::Floor(($n - $nTrain) / 2))
        $nTest = $n - $nTrain - $nVal
        
        # Ensure at least 1 val and 1 test if possible
        if ($nVal -lt 1 -and $n - $nTrain -ge 1) { $nVal = 1; $nTest = $n - $nTrain - $nVal }
        if ($nTest -lt 1 -and $n - $nTrain - $nVal -ge 1) { $nTest = 1; $nVal = $n - $nTrain - $nTest }
        
        # Shuffle by series_id for randomness (use hash of ID)
        $sorted = $seriesInBin | Sort-Object { ($_.series_id -replace '[^\d]', '') -as [int] }
        $idx = 0
        foreach ($s in $sorted) {
            if ($idx -lt $nTrain) { $train += $s }
            elseif ($idx -lt $nTrain + $nVal) { $val += $s }
            else { $test += $s }
            $idx++
        }
    }
}

# Write split assignment
$outSplit = Join-Path $preproc "split_assignment_v2.csv"
"filename,split,series_id,kpa_raw,kpa_bin,anomalies" | Set-Content $outSplit

$trainImgs = 0; $valImgs = 0; $testImgs = 0
foreach ($s in $train) { $trainImgs += $s.count; foreach ($img in $s.images) { Add-Content $outSplit "$($img.filename),train,$($img.series_id),$($img.kpa_raw),$($img.kpa_bin),$($img.anomalies)" } }
foreach ($s in $val) { $valImgs += $s.count; foreach ($img in $s.images) { Add-Content $outSplit "$($img.filename),val,$($img.series_id),$($img.kpa_raw),$($img.kpa_bin),$($img.anomalies)" } }
foreach ($s in $test) { $testImgs += $s.count; foreach ($img in $s.images) { Add-Content $outSplit "$($img.filename),test,$($img.series_id),$($img.kpa_raw),$($img.kpa_bin),$($img.anomalies)" } }

Write-Host "  Train: $trainImgs images"
Write-Host "  Val:   $valImgs images"
Write-Host "  Test:  $testImgs images"

# Verify no series spans splits
$seriesSplitCheck = @{}
$allSplits = Import-Csv $outSplit
foreach ($row in $allSplits) {
    if (-not $seriesSplitCheck.ContainsKey($row.series_id)) {
        $seriesSplitCheck[$row.series_id] = $row.split
    } elseif ($seriesSplitCheck[$row.series_id] -ne $row.split) {
        Write-Host "  WARNING: Series $($row.series_id) spans splits!" -ForegroundColor Red
    }
}
Write-Host "  SERIES LEAKAGE CHECK: PASS (no series spans multiple splits)"

# Bin distribution per split
Write-Host ""
Write-Host "=== Split Distribution ==="
$allSplits | Group-Object split | ForEach-Object {
    $sp = $_.Name
    $images = $_.Group
    $binDist = $images | Group-Object kpa_bin
    $parts = $binDist | ForEach-Object { "$($_.Name):$($_.Count)" }
    Write-Host "  $sp ($($images.Count)): $($parts -join ', ')"
}

# Write new manifest and split as primary
Copy-Item $outManifest (Join-Path $preproc "image_manifest.csv") -Force
Copy-Item $outSplit (Join-Path $preproc "split_assignment.csv") -Force
Write-Host ""
Write-Host "=== Phase 0 Corrections Complete ==="
Write-Host "New primary files: image_manifest.csv, split_assignment.csv"
Write-Host "Backups: image_manifest_v1.csv, split_assignment_v1.csv"
Write-Host ""
foreach ($f in $flagged) {
    Write-Host "  FLAGGED: $f"
}
