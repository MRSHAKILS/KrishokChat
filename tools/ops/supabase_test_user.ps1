# supabase_test_user.ps1 — Auto test-login for KrishokChat Supabase Auth
#
# Purpose:
#   Ensures the test user exists and is email-CONFIRMED, then performs a password
#   login and prints session details. Works against ANY Supabase project:
#     - Hosted : https://<ref>.supabase.co  (use -AdminKey with the service role
#               key so the user is created pre-confirmed; no email needed)
#     - Local  : http://127.0.0.1:54321      (confirmation disabled; admin key optional)
#
# Admin mode is idempotent: re-running resets the test user's password and
# confirmation, so the test credentials always work ("auto test login").
#
# Deployment note: this script never hardcodes values. It reads them from
# parameters -> environment -> .env files, so swapping local -> hosted is a
# pure configuration change (SUPABASE_URL / NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY).
#
# Usage:
#   .\scripts\supabase_test_user.ps1                        # uses env / .env files
#   .\scripts\supabase_test_user.ps1 -DryRun                # resolve config only, no network
#   .\scripts\supabase_test_user.ps1 -Email x -Password y -BaseUrl <url> -ApiKey <key> [-AdminKey <service-role-key>]

param(
    [string]$Email,
    [string]$Password,
    [string]$BaseUrl,
    [string]$ApiKey,
    [string]$AdminKey,
    [switch]$DryRun,
    # Amendment 02: provision the three test personas (free/premium/admin),
    # verify each can log in, and set their profiles plan/role labels.
    [switch]$Personas
)

$ErrorActionPreference = "Stop"

function Read-EnvFile([string]$Path) {
    $map = @{}
    if (-not (Test-Path -LiteralPath $Path)) { return $map }
    Get-Content -LiteralPath $Path | ForEach-Object {
        $line = $_.Trim()
        if ($line -and -not $line.StartsWith("#") -and $line.Contains("=")) {
            $idx = $line.IndexOf("=")
            $map[$line.Substring(0, $idx).Trim()] = $line.Substring($idx + 1).Trim().Trim('"', "'")
        }
    }
    return $map
}

function Get-ErrorMessage($ex) {
    try {
        $resp = $ex.Exception.Response
        if ($resp) {
            $stream = $resp.GetResponseStream()
            $reader = New-Object System.IO.StreamReader($stream)
            $txt = $reader.ReadToEnd()
            return "HTTP $($resp.StatusCode.value__): $txt"
        }
    } catch { }
    return $ex.Exception.Message
}

# ---- 1. Resolve configuration: params > environment > .env files ----
$envMap = @{}
@("$PSScriptRoot\..\.env", "$PSScriptRoot\..\backend\.env.local", "$PSScriptRoot\..\frontend\.env.local") | ForEach-Object {
    $fileMap = (Read-EnvFile $_)
    foreach ($k in $fileMap.Keys) {
        # first file wins (earlier precedence); never overwrite existing keys
        if (-not $envMap.ContainsKey($k)) { $envMap[$k] = $fileMap[$k] }
    }
}

if (-not $BaseUrl) { $BaseUrl = if ($env:SUPABASE_URL) { $env:SUPABASE_URL } else { $envMap["SUPABASE_URL"] } }
if (-not $BaseUrl) { $BaseUrl = if ($env:NEXT_PUBLIC_SUPABASE_URL) { $env:NEXT_PUBLIC_SUPABASE_URL } else { $envMap["NEXT_PUBLIC_SUPABASE_URL"] } }
if (-not $ApiKey)  { $ApiKey  = if ($env:NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY) { $env:NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY } else { $envMap["NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY"] } }
if (-not $ApiKey)  { $ApiKey  = $envMap["SUPABASE_ANON_KEY"] }  # legacy local key fallback
if (-not $AdminKey){ $AdminKey = if ($env:SUPABASE_SERVICE_ROLE_KEY) { $env:SUPABASE_SERVICE_ROLE_KEY } else { $envMap["SUPABASE_SERVICE_ROLE_KEY"] } }
if (-not $Email)   { $Email   = if ($env:TEST_USER_EMAIL) { $env:TEST_USER_EMAIL } else { $envMap["TEST_USER_EMAIL"] } }
if (-not $Password){ $Password = if ($env:TEST_USER_PASSWORD) { $env:TEST_USER_PASSWORD } else { $envMap["TEST_USER_PASSWORD"] } }

$missing = @()
if (-not $BaseUrl)  { $missing += "SUPABASE_URL (or NEXT_PUBLIC_SUPABASE_URL)" }
if (-not $ApiKey)   { $missing += "NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY" }
if (-not $Email)    { $missing += "TEST_USER_EMAIL" }
if (-not $Password) { $missing += "TEST_USER_PASSWORD" }

Write-Host "[config] base_url     = $BaseUrl"
Write-Host "[config] api_key      = $($ApiKey.Substring(0, [Math]::Min(12, $ApiKey.Length)))... (truncated)"
if ($AdminKey) { Write-Host "[config] admin_key    = present (service role; server-side only)" }
Write-Host "[config] email        = $Email"
Write-Host "[config] password     = $('*' * $Password.Length)"

if ($missing.Count -gt 0) {
    Write-Host "[FAIL] Missing configuration: $($missing -join ', ')" -ForegroundColor Red
    Write-Host "       Set them in .env files (see .env.example) or pass -Email/-Password/-BaseUrl/-ApiKey."
    exit 1
}

if ($DryRun) {
    Write-Host "[OK]   Config resolution succeeded (dry run, no network call made)." -ForegroundColor Green
    exit 0
}

# GoTrue v2.195 (hosted, new key system) requires BOTH headers on every call.
$clientHeaders = @{ apikey = $ApiKey; Authorization = "Bearer $ApiKey"; "Content-Type" = "application/json" }
$adminHeaders  = @{ apikey = $AdminKey; Authorization = "Bearer $AdminKey"; "Content-Type" = "application/json" }
$userBody = @{ email = $Email; password = $Password } | ConvertTo-Json

# ---- Personas mode (amendment 02): free / premium / admin -----------------
if ($Personas) {
    if (-not $AdminKey) {
        Write-Host "[FAIL] -Personas needs the service role key (SUPABASE_SERVICE_ROLE_KEY / -AdminKey)." -ForegroundColor Red
        exit 1
    }
    $personas = @(
        @{ email = $envMap["TEST_FREE_USER_EMAIL"];     password = $envMap["TEST_FREE_USER_PASSWORD"];     plan = "free";     role = "user"  },
        @{ email = $envMap["TEST_PREMIUM_USER_EMAIL"];  password = $envMap["TEST_PREMIUM_USER_PASSWORD"];  plan = "premium";  role = "user"  },
        @{ email = $envMap["TEST_ADMIN_USER_EMAIL"];    password = $envMap["TEST_ADMIN_USER_PASSWORD"];    plan = "free";     role = "admin" }
    )
    foreach ($p in $personas) {
        if (-not $p.email -or -not $p.password) {
            Write-Host "[SKIP] $($p.role)/$($p.plan): TEST vars not set in .env(.example) files." -ForegroundColor Yellow
            continue
        }
        Write-Host ""
        Write-Host "== persona $($p.email) (plan=$($p.plan), role=$($p.role)) ==" -ForegroundColor Cyan
        $body = @{ email = $p.email; password = $p.password; email_confirm = $true } | ConvertTo-Json
        $uid = $null
        try {
            $created = Invoke-RestMethod -Method Post -Uri "$BaseUrl/auth/v1/admin/users" -Headers $adminHeaders -Body $body -TimeoutSec 20
            $uid = $created.id
            Write-Host "[1/3] created (id=$uid)."
        } catch {
            $err = Get-ErrorMessage $_
            if ($err -match "already registered|email_exists|duplicate") {
                $list = Invoke-RestMethod -Method Get -Uri "$BaseUrl/auth/v1/admin/users?email=$([uri]::EscapeDataString($p.email))" -Headers $adminHeaders -TimeoutSec 20
                $uid = @($list.users)[0].id
                $null = Invoke-RestMethod -Method Put -Uri "$BaseUrl/auth/v1/admin/users/$uid" -Headers $adminHeaders -Body $body -TimeoutSec 20
                Write-Host "[1/3] existing user reset (id=$uid)."
            } else {
                Write-Host "[FAIL] ensure failed: $err" -ForegroundColor Red
                continue
            }
        }
        # profiles row with plan/role (PostgREST upsert on id; merge-duplicates
        # merges plan/role into an existing row instead of failing)
        $profileBody = @{ id = $uid; email = $p.email; plan = $p.plan; role = $p.role } | ConvertTo-Json
        try {
            $h = $adminHeaders.Clone(); $h["Prefer"] = "resolution=merge-duplicates"
            $null = Invoke-RestMethod -Method Post -Uri "$BaseUrl/rest/v1/profiles?on_conflict=id" -Headers $h -Body $profileBody -TimeoutSec 20
        } catch {
            Write-Host "[WARN] profiles upsert failed: $(Get-ErrorMessage $_)" -ForegroundColor Yellow
        }
        Write-Host "[2/3] profiles row ensured (plan=$($p.plan), role=$($p.role))."
        try {
            $login = Invoke-RestMethod -Method Post -Uri "$BaseUrl/auth/v1/token?grant_type=password" -Headers $clientHeaders -Body (@{ email = $p.email; password = $p.password } | ConvertTo-Json) -TimeoutSec 15
            Write-Host "[3/3] login OK." -ForegroundColor Green
        } catch {
            Write-Host "[3/3] LOGIN FAILED: $(Get-ErrorMessage $_)" -ForegroundColor Red
        }
    }
    Write-Host ""
    Write-Host "Personas done. Set NEXT_PUBLIC_DEV_USER_SWITCHER=true + NEXT_PUBLIC_TEST_* in frontend/.env.local for the /auth one-click switcher." -ForegroundColor Cyan
    exit 0
}

# ---- 2. Ensure test user exists and is CONFIRMED ----
if ($AdminKey) {
    Write-Host "[1/3] Ensuring confirmed test user via admin API ..."
    try {
        $body = @{ email = $Email; password = $Password; email_confirm = $true } | ConvertTo-Json
        $created = Invoke-RestMethod -Method Post -Uri "$BaseUrl/auth/v1/admin/users" -Headers $adminHeaders -Body $body -TimeoutSec 20
        Write-Host "[1/3] User created (id=$($created.id), confirmed)."
    } catch {
        $err = Get-ErrorMessage $_
        if ($err -match "already registered|email_exists|duplicate") {
            # Idempotent reset: find the user, then set password + confirmation.
            $list = Invoke-RestMethod -Method Get -Uri "$BaseUrl/auth/v1/admin/users?email=$([uri]::EscapeDataString($Email))" -Headers $adminHeaders -TimeoutSec 20
            $users = @($list.users)  # response shape: {"users":[...],"aud":"authenticated"}
            if ($users.Count -eq 0) {
                Write-Host "[FAIL] User exists per error but not found by lookup: $err" -ForegroundColor Red
                exit 2
            }
            $uid = $users[0].id
            $body = @{ email = $Email; password = $Password; email_confirm = $true } | ConvertTo-Json
            $null = Invoke-RestMethod -Method Put -Uri "$BaseUrl/auth/v1/admin/users/$uid" -Headers $adminHeaders -Body $body -TimeoutSec 20
            Write-Host "[1/3] Existing user reset (id=$uid, password + confirmation refreshed)."
        } else {
            Write-Host "[FAIL] Admin ensure failed: $err" -ForegroundColor Red
            exit 2
        }
    }
} else {
    Write-Host "[1/3] Ensuring test user exists (signup) ..."
    try {
        $null = Invoke-RestMethod -Method Post -Uri "$BaseUrl/auth/v1/signup" -Headers $clientHeaders -Body $userBody -TimeoutSec 15
        Write-Host "[1/3] Signup request accepted (user may already exist)."
    } catch {
        $err = Get-ErrorMessage $_
        if ($err -match "already registered|User already registered|email_exists") {
            Write-Host "[1/3] User already registered - continuing to login."
        } else {
            Write-Host "[1/3] Signup warning: $err" -ForegroundColor Yellow
        }
    }
}

# ---- 3. Password login ----
Write-Host "[2/3] Logging in with password grant ..."
$login = $null
try {
    $login = Invoke-RestMethod -Method Post -Uri "$BaseUrl/auth/v1/token?grant_type=password" -Headers $clientHeaders -Body $userBody -TimeoutSec 15
} catch {
    Write-Host "[FAIL] Login failed: $(Get-ErrorMessage $_)" -ForegroundColor Red
    Write-Host "       On HOSTED, re-run with -AdminKey (or SUPABASE_SERVICE_ROLE_KEY set) to auto-confirm."
    Write-Host "       On LOCAL CLI, confirmation is disabled by default and login should succeed."
    exit 3
}

# ---- 4. Verify the session against /auth/v1/user ----
Write-Host "[3/3] Verifying access token ..."
$authHeaders = @{ apikey = $ApiKey; Authorization = "Bearer $($login.access_token)" }
$me = Invoke-RestMethod -Method Get -Uri "$BaseUrl/auth/v1/user" -Headers $authHeaders -TimeoutSec 15

Write-Host ""
Write-Host "[OK] TEST LOGIN SUCCEEDED" -ForegroundColor Green
Write-Host "     user_id      : $($me.id)"
Write-Host "     email        : $($me.email)"
Write-Host "     confirmed    : $($me.email_confirmed_at -ne $null)"
Write-Host "     access_token : $($login.access_token.Substring(0, 40))... (truncated)"
Write-Host "     expires_in   : $($login.expires_in)s"
exit 0