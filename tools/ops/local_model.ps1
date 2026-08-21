# ============================================================================
# local_model.ps1 — One-command activation of the local KrishokChat-4B model.
#
# Prerequisites:
#   - Ollama installed (https://ollama.com/download) and on PATH
#   - The fine-tuned GGUF file present, default:
#       backend\ml_assets\gemma\model.gguf
#     (override with -GgufPath, or pass -DownloadUrl to fetch it automatically)
#
# What it does:
#   1. Ensures the GGUF exists (optionally downloads it from -DownloadUrl)
#   2. Starts the Ollama server if it is not already running
#   3. Creates the Ollama model tag "krishokchat-4b" from scripts\Modelfile
#   4. Verifies: ollama list + backend GET /api/models
#   5. Restarts the backend so the frontend "KrishokChat-4B" button enables
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File scripts\local_model.ps1
#   powershell -ExecutionPolicy Bypass -File scripts\local_model.ps1 -GgufPath "D:\models\krishokchat-4b-q4.gguf"
#   powershell -ExecutionPolicy Bypass -File scripts\local_model.ps1 -DownloadUrl "https://huggingface.co/<org>/<repo>/resolve/main/<file>.gguf"
# ============================================================================

param(
    [string]$GgufPath = "",
    [string]$DownloadUrl = "",
    [switch]$SkipBackendRestart
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot

function Write-Step([string]$msg) { Write-Host "==> $msg" -ForegroundColor Cyan }
function Write-Ok([string]$msg)   { Write-Host "    $msg" -ForegroundColor Green }
function Write-Fail([string]$msg) { Write-Host "    $msg" -ForegroundColor Red }

# ---------------------------------------------------------------------------
# 0. Resolve GGUF path
# ---------------------------------------------------------------------------
if (-not $GgufPath) {
    $GgufPath = Join-Path $repoRoot "backend\ml_assets\gemma\model.gguf"
}
if (-not [System.IO.Path]::IsPathRooted($GgufPath)) {
    $GgufPath = Join-Path $repoRoot $GgufPath
}
$GgufPath = [System.IO.Path]::GetFullPath($GgufPath)
$ggufDir = Split-Path -Parent $GgufPath
$ggufName = Split-Path -Leaf $GgufPath

# ---------------------------------------------------------------------------
# 1. Ensure GGUF exists (download if requested)
# ---------------------------------------------------------------------------
if (-not (Test-Path -LiteralPath $GgufPath)) {
    if ($DownloadUrl) {
        Write-Step "Downloading GGUF from $DownloadUrl"
        New-Item -ItemType Directory -Force -Path $ggufDir | Out-Null
        Invoke-WebRequest -Uri $DownloadUrl -OutFile $GgufPath -UseBasicParsing
        Write-Ok "Downloaded to $GgufPath"
    } else {
        Write-Fail "GGUF not found: $GgufPath"
        Write-Host "  Drop your fine-tuned GGUF at that path, then re-run this script."
        Write-Host "  Or download it automatically:  -DownloadUrl https://huggingface.co/<org>/<repo>/resolve/main/<file>.gguf"
        exit 1
    }
} else {
    Write-Ok "GGUF found: $GgufPath"
}

# ---------------------------------------------------------------------------
# 2. Start Ollama server if not running
# ---------------------------------------------------------------------------
Write-Step "Checking Ollama server"
$ollamaUp = $false
try {
    $tags = Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 3
    $ollamaUp = $true
    Write-Ok "Ollama already running"
} catch { }

if (-not $ollamaUp) {
    $ollamaCmd = Get-Command ollama -ErrorAction SilentlyContinue
    if (-not $ollamaCmd) {
        Write-Fail "ollama not found on PATH. Install from https://ollama.com/download and re-run."
        exit 1
    }
    Write-Step "Starting Ollama server (ollama serve)"
    Start-Process -FilePath (Get-Command ollama).Source -ArgumentList "serve" -WindowStyle Hidden
    $deadline = (Get-Date).AddSeconds(15)
    while ((Get-Date) -lt $deadline) {
        Start-Sleep -Milliseconds 800
        try {
            Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 2 | Out-Null
            $ollamaUp = $true
            break
        } catch { }
    }
    if ($ollamaUp) { Write-Ok "Ollama server started" }
    else {
        Write-Fail "Ollama did not come up on port 11434. Start it manually (Ollama app or 'ollama serve')."
        exit 1
    }
}

# ---------------------------------------------------------------------------
# 3. Create the model tag from scripts\Modelfile
# ---------------------------------------------------------------------------
Write-Step "Creating model tag 'krishokchat-4b' from scripts\Modelfile"

$modelfileSource = Join-Path $PSScriptRoot "Modelfile"
$modelfileTarget = Join-Path $ggufDir "Modelfile"
if (-not (Test-Path -LiteralPath $modelfileSource)) {
    Write-Fail "Modelfile not found: $modelfileSource"
    exit 1
}
Copy-Item -LiteralPath $modelfileSource -Destination $modelfileTarget -Force

# FROM ./model.gguf resolves relative to the Modelfile's own directory,
# so we place the Modelfile next to the GGUF and that already works as long
# as the GGUF is named model.gguf. If it is named differently, rewrite FROM.
if ($ggufName -ne "model.gguf") {
    (Get-Content -LiteralPath $modelfileTarget -Raw) `
        -replace "FROM ./model\.gguf", "FROM ./$ggufName" | `
        Set-Content -LiteralPath $modelfileTarget -Encoding UTF8
}

$create = & ollama create krishokchat-4b -f $modelfileTarget 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Fail "ollama create failed:"
    Write-Host $create
    Write-Host "  Tip: ensure the GGUF is a valid GGUF (q4_k_m etc.) compatible with your Ollama version."
    exit 1
}
Write-Ok "Tag created (ollama create ok)"

# ---------------------------------------------------------------------------
# 4. Verify
# ---------------------------------------------------------------------------
Write-Step "Verifying"
$list = & ollama list 2>&1
Write-Host ($list | Out-String)

$matches = $list | Where-Object { $_ -match "krishokchat-4b" }
if (-not $matches) {
    Write-Fail "Tag 'krishokchat-4b' not visible in 'ollama list'."
    exit 1
}
Write-Ok "ollama list shows krishokchat-4b"

try {
    $models = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/models" -TimeoutSec 5
    $local = $models | Where-Object { $_.id -eq "krishokchat-4b" }
    if ($local -and $local.available) {
        Write-Ok "Backend /api/models reports krishokchat-4b available=True — the frontend button is now enabled."
    } else {
        Write-Fail "Backend /api/models reports available=False. Restart the backend to refresh the probe."
    }
} catch {
    Write-Fail "Backend not reachable on :8000 — start it, then refresh. Model is registered in Ollama regardless."
}

# ---------------------------------------------------------------------------
# 5. Optional backend restart
# ---------------------------------------------------------------------------
if (-not $SkipBackendRestart) {
    $py = Join-Path $repoRoot "backend\.venv\Scripts\python.exe"
    if (Test-Path -LiteralPath $py) {
        Write-Step "Restarting backend (fresh /api/models probe)"
        Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" |
            Where-Object { $_.CommandLine -match 'uvicorn.*8000' } |
            ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
        Start-Sleep -Seconds 3
        cmd.exe /c "start `"KrishokChatBackend`" /b `"$py`" -m uvicorn app.main:app --app-dir `"$repoRoot\backend`" --host 0.0.0.0 --port 8000 > `"$repoRoot\backend\uvicorn-live.log`" 2>&1"
        Start-Sleep -Seconds 12
        Write-Ok "Backend restarted — check http://localhost:8000/api/models"
    } else {
        Write-Host "  (backend venv not found at $py — restart it manually)"
    }
}

Write-Host ""
Write-Host "Done. KrishokChat-4B is now available as the 'KrishokChat-4B (লোকাল)' chat option."
