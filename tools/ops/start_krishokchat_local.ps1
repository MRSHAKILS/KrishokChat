param(
    [string]$LlamaServer = "$HOME\llama.cpp\llama-server.exe",
    [string]$BaseModel = "E:\CSE499 Prototype\backend\models\krishokchat\gemma-4-E4B-it-Q4_K_M.gguf",
    [string]$Adapter = "E:\CSE499 Prototype\backend\models\krishokchat\krishokchat-5362-adapter.gguf",
    [int]$Port = 11435
)

$ErrorActionPreference = "Stop"

foreach ($path in @($LlamaServer, $BaseModel, $Adapter)) {
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Required local-model file not found: $path"
    }
}

$existing = Get-CimInstance Win32_Process -Filter "Name = 'llama-server.exe'" |
    Where-Object { $_.CommandLine -match "--port\s+$Port(?:\s|$)" }
if ($existing) {
    Write-Host "KrishokChat local server is already running on port $Port."
    exit 0
}

$logDir = Join-Path $PSScriptRoot "..\backend\app\logs"
New-Item -ItemType Directory -Path $logDir -Force | Out-Null
$stdout = Join-Path $logDir "llama-server.stdout.log"
$stderr = Join-Path $logDir "llama-server.stderr.log"

$arguments = "-m `"$BaseModel`" --lora `"$Adapter`" --alias krishokchat-4b " +
    "--host 127.0.0.1 --port $Port -c 4096 -np 1 --jinja --reasoning off"

Start-Process -FilePath $LlamaServer -ArgumentList $arguments `
    -RedirectStandardOutput $stdout -RedirectStandardError $stderr -WindowStyle Hidden

$deadline = (Get-Date).AddMinutes(3)
while ((Get-Date) -lt $deadline) {
    Start-Sleep -Seconds 2
    try {
        $models = Invoke-RestMethod -Uri "http://127.0.0.1:$Port/v1/models" -TimeoutSec 3
        if ($models.data.id -contains "krishokchat-4b") {
            Write-Host "KrishokChat local server ready: http://127.0.0.1:$Port/v1"
            exit 0
        }
    } catch { }
}

throw "KrishokChat local server did not become ready. Check $stderr"
