# P0-12: production-style start script (single box, no orchestration).
#
# Starts the backend under uvicorn with proxy-headers (reverse-proxy safe),
# a graceful-shutdown window, and a bounded concurrency ceiling, then starts
# the Next.js production server (pnpm start) on the frontend port.
#
# Requirements:
#   - backend: .venv exists (uv sync) and .env is configured
#   - frontend: production build exists (run `pnpm build` once; this script
#     does not build to keep startup fast and deterministic)
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File scripts/start_prod.ps1
#   powershell -ExecutionPolicy Bypass -File scripts/start_prod.ps1 -BackendPort 8000 -FrontendPort 3100

param(
    [int]$BackendPort = 8000,
    [int]$FrontendPort = 3100,
    [int]$UvicornLimitConcurrency = 32
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$backendRoot = Join-Path $repoRoot "backend"
$frontendRoot = Join-Path $repoRoot "frontend"
$python = Join-Path $backendRoot ".venv\Scripts\python.exe"
$logDir = Join-Path $backendRoot "logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

function Wait-Http([string]$Url, [int]$Seconds = 90) {
    $deadline = (Get-Date).AddSeconds($Seconds)
    while ((Get-Date) -lt $deadline) {
        Start-Sleep -Seconds 2
        try {
            $response = Invoke-WebRequest -UseBasicParsing -Uri $Url -TimeoutSec 4
            if ($response.StatusCode -eq 200) { return }
        } catch { }
    }
    throw "Service did not become ready: $Url"
}

if (-not (Test-Path -LiteralPath $python)) {
    throw "Backend environment missing: $python (run `uv sync` in backend/)"
}
if (-not (Test-Path -LiteralPath (Join-Path $frontendRoot ".next\BUILD_ID"))) {
    throw "Frontend production build missing: run `pnpm build` in frontend/ once first"
}

# --- Backend: uvicorn with production-friendly flags ---------------------
$backendListener = Get-NetTCPConnection -LocalPort $BackendPort -State Listen -ErrorAction SilentlyContinue
if ($backendListener) {
    Write-Host "Backend port $BackendPort already in use — leaving it running." -ForegroundColor Yellow
} else {
    Start-Process -FilePath $python `
        -ArgumentList @(
            "-m", "uvicorn", "app.main:app",
            "--host", "0.0.0.0",
            "--port", "$BackendPort",
            "--proxy-headers",
            "--timeout-graceful-shutdown", "30",
            "--limit-concurrency", "$UvicornLimitConcurrency"
        ) `
        -WorkingDirectory $backendRoot `
        -RedirectStandardOutput (Join-Path $logDir "prod-uvicorn.log") `
        -RedirectStandardError (Join-Path $logDir "prod-uvicorn.err.log") `
        -WindowStyle Hidden
}
Wait-Http "http://127.0.0.1:$BackendPort/health" 90

# /readyz is informational by default; warn loudly but do not abort when a
# check is degraded — the demo must stay reachable (AGENTS.md §2.1).
try {
    $ready = Invoke-RestMethod -Uri "http://127.0.0.1:$BackendPort/readyz" -TimeoutSec 10
    if (-not $ready.ready) {
        Write-Host "Backend /readyz reports degraded: $($ready.degraded -join ', ')" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Could not query /readyz: $_" -ForegroundColor Yellow
}

# --- Frontend: production server (requires a prior pnpm build) -----------
$frontendListener = Get-NetTCPConnection -LocalPort $FrontendPort -State Listen -ErrorAction SilentlyContinue
if ($frontendListener) {
    Write-Host "Frontend port $FrontendPort already in use — leaving it running." -ForegroundColor Yellow
} else {
    $pnpm = (Get-Command pnpm.cmd -ErrorAction Stop).Source
    Start-Process -FilePath $pnpm `
        -ArgumentList "start", "--", "--port", "$FrontendPort" `
        -WorkingDirectory $frontendRoot `
        -RedirectStandardOutput (Join-Path $logDir "prod-next.log") `
        -RedirectStandardError (Join-Path $logDir "prod-next.err.log") `
        -WindowStyle Hidden
}
Wait-Http "http://127.0.0.1:$FrontendPort" 90

Write-Host "KrishokChat production start complete." -ForegroundColor Green
Write-Host "Frontend: http://localhost:$FrontendPort"
Write-Host "Backend:  http://localhost:$BackendPort"
Write-Host "Docs:     http://localhost:$BackendPort/docs (DOCS_ENABLED=true only)"
Write-Host "Logs:     $logDir\prod-*.log"