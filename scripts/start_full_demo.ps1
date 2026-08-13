param(
    [int]$BackendPort = 8000,
    [int]$FrontendPort = 3100
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$backendRoot = Join-Path $repoRoot "backend"
$frontendRoot = Join-Path $repoRoot "frontend"
$python = Join-Path $backendRoot ".venv\Scripts\python.exe"

function Wait-Http([string]$Url, [int]$Seconds = 60) {
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
    throw "Backend environment missing: $python"
}

& (Join-Path $PSScriptRoot "start_krishokchat_local.ps1")

$backendListener = Get-NetTCPConnection -LocalPort $BackendPort -State Listen -ErrorAction SilentlyContinue
if (-not $backendListener) {
    Start-Process -FilePath $python `
        -ArgumentList "-m uvicorn app.main:app --host 127.0.0.1 --port $BackendPort" `
        -WorkingDirectory $backendRoot `
        -RedirectStandardOutput (Join-Path $backendRoot "uvicorn-live.log") `
        -RedirectStandardError (Join-Path $backendRoot "uvicorn-live.err.log") `
        -WindowStyle Hidden
}
Wait-Http "http://127.0.0.1:$BackendPort/health" 60

$frontendListener = Get-NetTCPConnection -LocalPort $FrontendPort -State Listen -ErrorAction SilentlyContinue
if (-not $frontendListener) {
    $pnpm = (Get-Command pnpm.cmd -ErrorAction Stop).Source
    Start-Process -FilePath $pnpm `
        -ArgumentList "dev -- --port $FrontendPort" `
        -WorkingDirectory $frontendRoot `
        -RedirectStandardOutput (Join-Path $frontendRoot "next-live.log") `
        -RedirectStandardError (Join-Path $frontendRoot "next-live.err.log") `
        -WindowStyle Hidden
}
Wait-Http "http://127.0.0.1:$FrontendPort" 90

$models = Invoke-RestMethod -Uri "http://127.0.0.1:$BackendPort/api/models" -TimeoutSec 10
$local = $models | Where-Object { $_.id -eq "krishokchat-4b" }
if (-not $local.available) {
    throw "Backend is running, but krishokchat-4b is unavailable."
}

Write-Host "KrishokChat demo is ready." -ForegroundColor Green
Write-Host "Frontend: http://localhost:$FrontendPort"
Write-Host "Backend:  http://localhost:$BackendPort"
Write-Host "API docs: http://localhost:$BackendPort/docs"
