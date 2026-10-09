# PowerShell runner for Bloodborne on Windows (bloodborne_pc)
[CmdletBinding()]
param(
    [string]$GameDir,
    [string]$Fps = "uncap",
    [string]$DataDir = ".",
    [string]$Config,
    [string]$RenderRes,
    [string]$OutputRes,
    [string]$Patches = "",
    [string]$ModsDir,
    [string]$UserDir,
    [int]$Timeout = 0,
    [switch]$SaveLog,
    [switch]$BuildIfMissing = $true,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ExtraProbeArgs
)

$ErrorActionPreference = 'Stop'
$repoRoot = $PSScriptRoot
Set-Location $repoRoot

$outDir = Join-Path $DataDir "out"
if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir | Out-Null }

$configPath = if ($Config) { $Config } elseif ($env:BB_CONFIG) { $env:BB_CONFIG } else { Join-Path $DataDir "bbport.ini" }
$env:BB_CONFIG = $configPath

# Locate Python 3
$python = Get-Command python -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python3 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue
}
if (-not $python) {
    Write-Error "Python 3 is required. Please install Python or add it to PATH."
    exit 1
}

# Resolve Game Directory
$candidates = @()
if ($GameDir) {
    $candidates += $GameDir
}
if ($env:BB_GAME_DIR) {
    $candidates += $env:BB_GAME_DIR
}

# Check bbport.ini for configured game_dir
if (Test-Path $configPath) {
    $iniLines = Get-Content $configPath -ErrorAction SilentlyContinue
    foreach ($line in $iniLines) {
        if ($line -match "^\s*game_dir\s*=\s*(.+)$") {
            $candidates += $matches[1].Trim()
        }
    }
}

# Common relative and desktop locations
$candidates += (Join-Path $repoRoot "game")
$candidates += (Join-Path $repoRoot "game\CUSA03173")
$candidates += (Join-Path $repoRoot "..\CUSA03173")
$candidates += (Join-Path $repoRoot "..\Bloodborne")

if ($env:USERPROFILE) {
    $desktop = Join-Path $env:USERPROFILE "Desktop"
    $candidates += (Join-Path $desktop "Ps4 oyun\CUSA03173")
    $candidates += (Join-Path $desktop "Ps4 oyun")
    $candidates += (Join-Path $desktop "CUSA03173")
    $candidates += (Join-Path $desktop "Bloodborne")
}

$gamePath = $null
foreach ($cand in $candidates) {
    $candFull = if ([System.IO.Path]::IsPathRooted($cand)) { [System.IO.Path]::GetFullPath($cand) } else { [System.IO.Path]::GetFullPath((Join-Path $repoRoot $cand)) }
    if (Test-Path (Join-Path $candFull "eboot.bin")) {
        $gamePath = $candFull
        break
    }
    # Check immediate subdirectories (e.g. CUSA03173, CUSA00900)
    $subEboot = Get-ChildItem -Path $candFull -Filter "eboot.bin" -Recurse -Depth 2 -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($subEboot) {
        $gamePath = $subEboot.DirectoryName
        break
    }
}

if (-not $gamePath -or -not (Test-Path (Join-Path $gamePath "eboot.bin"))) {
    Write-Error @"
Game dump not found!
Please provide the path to your Bloodborne PS4 (v1.09) dump using -GameDir,
set 'game_dir' in bbport.ini, or set the BB_GAME_DIR environment variable:
Example: .\run.ps1 -GameDir `"D:\Games\Bloodborne\CUSA03173`"
"@
    exit 1
}

Write-Host "Found Bloodborne dump at: $gamePath" -ForegroundColor Green

# Build binaries if missing
$probeExe = Join-Path $outDir "bb-probe.exe"
$capsExe = Join-Path $outDir "bb-gpu-capabilities.exe"
if (-not (Test-Path $probeExe) -or -not (Test-Path $capsExe)) {
    if ($BuildIfMissing) {
        Write-Host "Building missing Windows binaries..." -ForegroundColor Cyan
        & .\build.ps1
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    } else {
        Write-Error "Binaries missing. Please run .\build.ps1 first."
        exit 1
    }
}

# Process loose-file mods
$modsDirectory = if ($ModsDir) { $ModsDir } elseif ($env:BB_MODS_DIR) { $env:BB_MODS_DIR } else { Join-Path $DataDir "mods" }
$modsConfig = if ($env:BB_MODS_CONFIG) { $env:BB_MODS_CONFIG } else { Join-Path $DataDir "mods.json" }
$modsEnabled = if ($env:BB_MODS_ENABLED) { $env:BB_MODS_ENABLED } else { "1" }

$gameView = & $python scripts/mods.py $gamePath --out $outDir --mods-dir $modsDirectory --config $modsConfig --enabled $modsEnabled
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$gameView = $gameView.Trim()

# Game preparation and linking pipeline
Write-Host "Preparing native game image..." -ForegroundColor Cyan
& $python scripts/prepare.py $gameView --out $outDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Linking native libc..." -ForegroundColor Cyan
& $python scripts/link_libc.py $gameView --out $outDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Linking game modules..." -ForegroundColor Cyan
& $python scripts/link_modules.py $gameView --out $outDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Generating AppContent profile..." -ForegroundColor Cyan
$sku = if ($env:BB_CONTENT_SKU) { $env:BB_CONTENT_SKU } else { "full" }
& $python scripts/content_profile.py $gameView --out $outDir --sku $sku
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# Resolution and GPU scaling check
$scaledRender = if ($RenderRes) { $RenderRes } elseif ($env:BB_RENDER_RES) { $env:BB_RENDER_RES } else { "" }
$scaledOutput = if ($OutputRes) { $OutputRes } elseif ($env:BB_OUTPUT_RES) { $env:BB_OUTPUT_RES } else { "" }

if (-not $scaledRender) {
    $scaledSizes = & $python scripts/patches.py --print-scaled --settings $configPath
    if ($scaledSizes) {
        $parts = $scaledSizes.Trim().Split(" ")
        if ($parts.Count -ge 2) {
            $scaledRender = $parts[0]
            $scaledOutput = $parts[1]
        }
    }
}

$live = 0
if ($env:BB_LIVE_RES) {
    $live = [int]$env:BB_LIVE_RES
} elseif (Test-Path $configPath) {
    $iniLive = Get-Content $configPath | Where-Object { $_ -match '^live_resolution=([01]|auto)$' }
    if ($iniLive -match 'auto') {
        $capsOutput = & $capsExe --live-resolution 2>&1
        $lastLine = ($capsOutput | Select-Object -Last 1).Trim()
        if ($lastLine -eq "1") { $live = 1 } else { $live = 0 }
    } elseif ($iniLive -match '1') {
        $live = 1
    }
}

# If live resolution is OFF (or startup patch preferred) and no scaled sizes from --print-scaled:
# Check if an upscaler preset is active to generate the startup resolution patch.
if ($live -eq 0 -and -not $scaledRender) {
    $presetSize = (& $python scripts/patches.py --print-preset-size --settings $configPath)
    if ($presetSize -and $presetSize.Trim()) {
        $scaledRender = $presetSize.Trim()
        if (Test-Path $configPath) {
            $iniOutput = Get-Content $configPath | Where-Object { $_ -match '^\s*output_res\s*=\s*([0-9xX]+)' }
            if ($iniOutput) {
                $scaledOutput = ($iniOutput -replace '^\s*output_res\s*=\s*', '').Trim()
            }
        }
        if (-not $scaledOutput) { $scaledOutput = "1920x1080" }
    }
}

if ($live -eq 1 -and $scaledOutput -and $scaledOutput -ne "1920x1080") {
    Write-Host "Output $scaledOutput : live resolution changes enabled" -ForegroundColor Yellow
} elseif ($scaledOutput -and $scaledRender) {
    $env:BB_RENDER_RES = $scaledRender
    $env:BB_OUTPUT_RES = $scaledOutput
    $env:BB_AUTO_RENDER_RES = "1"
    if (-not $env:BB_DMEM_MB) {
        if ($env:BB_VRAM_SAFE_MODE -eq "1" -or ((Test-Path $configPath) -and (Get-Content $configPath | Where-Object { $_ -match '^\s*vram_safe_mode\s*=\s*1' }))) {
            $env:BB_DMEM_MB = "6144"
        } else {
            $env:BB_DMEM_MB = "9152"
        }
    }
    Write-Host "Output $scaledOutput : scene $scaledRender, direct memory $($env:BB_DMEM_MB) MiB (live_resolution=0: startup patch)" -ForegroundColor Yellow
}

# Compile game patches
Write-Host "Compiling executable patches..." -ForegroundColor Cyan
$patchesDir = if ($env:BB_PATCHES_DIR) { $env:BB_PATCHES_DIR } else { Join-Path $DataDir "patches" }
$patchesConfig = if ($env:BB_PATCHES_CONFIG) { $env:BB_PATCHES_CONFIG } else { Join-Path $DataDir "patches.json" }
if (Test-Path $configPath) {
    if (-not $env:BB_FPS_LIMIT) {
        $iniLimit = Get-Content $configPath | Where-Object { $_ -match '^\s*fps_limit\s*=\s*(\d+)' }
        if ($iniLimit) {
            $env:BB_FPS_LIMIT = ($iniLimit -replace '^\s*fps_limit\s*=\s*', '').Trim()
        }
    }
    if (-not $PSBoundParameters.ContainsKey('Fps') -and -not $env:BB_FPS) {
        $iniMode = Get-Content $configPath | Where-Object { $_ -match '^\s*fps_mode\s*=\s*([a-zA-Z0-9_]+)' }
        if ($iniMode) {
            $Fps = ($iniMode -replace '^\s*fps_mode\s*=\s*', '').Trim()
        }
    }
}
$effectiveFps = if ($Fps) { $Fps } elseif ($env:BB_FPS) { $env:BB_FPS } else { "uncap" }
$extraPatches = if ($Patches) { $Patches } else { $env:BB_PATCHES }

$patchArgs = @(
    "scripts/patches.py",
    "--out", $outDir,
    "--fps", $effectiveFps,
    "--settings", $configPath,
    "--game-dir", $gameView,
    "--patches-dir", $patchesDir,
    "--patches-config", $patchesConfig
)
if ($extraPatches) {
    $patchArgs += @("--extra", "$extraPatches")
}
if ($env:BB_RENDER_RES) {
    $patchArgs += @("--render-res", "$($env:BB_RENDER_RES)")
}
if ($env:BB_OUTPUT_RES) {
    $patchArgs += @("--output-res", "$($env:BB_OUTPUT_RES)")
}

& $python @patchArgs
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# Engine and GPU Runtime environment variables
if (-not $env:BB_LANGUAGE) {
    if ((Test-Path $configPath) -and ((Get-Content $configPath) -match '^\s*language\s*=\s*(.+)')) {
        $env:BB_LANGUAGE = ($Matches[1]).Trim()
    } else {
        $env:BB_LANGUAGE = "tr"
    }
}
if (-not $env:BB_PREUPLOAD) { $env:BB_PREUPLOAD = "1" }
if (-not $env:BB_GUEST_IN_PLACE) { $env:BB_GUEST_IN_PLACE = "0" }
if (-not $env:BB_UFFD) { $env:BB_UFFD = "0" }
if (-not $env:BB_COPY_GPU_BUFFERS) { $env:BB_COPY_GPU_BUFFERS = "1" }
if (-not $env:BB_GPU_WRITE_TWINS) { $env:BB_GPU_WRITE_TWINS = "1" }
if (-not $env:BB_GPU_WRITE_TWINS_MAX) { $env:BB_GPU_WRITE_TWINS_MAX = "65536" }
if (-not $env:BB_ASYNC_SUBMIT) { $env:BB_ASYNC_SUBMIT = "0" }

if (-not $env:BB_VBLANK_HZ) {
    switch ($effectiveFps) {
        "uncap" { $env:BB_VBLANK_HZ = "480" }
        "90"    { $env:BB_VBLANK_HZ = "90" }
        default { $env:BB_VBLANK_HZ = "60" }
    }
}
$limitInfo = if ($env:BB_FPS_LIMIT -and [int]$env:BB_FPS_LIMIT -gt 0) { "$($env:BB_FPS_LIMIT) FPS" } else { "Uncapped" }
Write-Host "Target Frame Rate: $limitInfo (Patch preset: $effectiveFps, Vblank: $($env:BB_VBLANK_HZ) Hz)" -ForegroundColor Yellow

# Intel 12th+ Gen Hybrid CPU Pinning (P-Core Affinity)
if ($env:BB_INTEL_HYBRID_FIX -eq "1" -or ((Test-Path $configPath) -and (Get-Content $configPath | Where-Object { $_ -match '^\s*intel_hybrid_fix\s*=\s*1' }))) {
    try {
        $proc = [System.Diagnostics.Process]::GetCurrentProcess()
        $proc.ProcessorAffinity = [IntPtr]0x0FFF
        Write-Host "Intel Hybrid CPU Optimization: P-Core affinity locked (0x0FFF)" -ForegroundColor Green
    } catch {
        Write-Warning "Could not set CPU affinity: $_"
    }
}

# 6GB/8GB VRAM Safe Mode (Texture Eviction & memory cap)
if ($env:BB_VRAM_SAFE_MODE -eq "1" -or ((Test-Path $configPath) -and (Get-Content $configPath | Where-Object { $_ -match '^\s*vram_safe_mode\s*=\s*1' }))) {
    $env:BB_DMEM_MB = "6144"
    $env:BB_COPY_GPU_BUFFERS = "1"
    $env:BB_GPU_WRITE_TWINS = "1"
    $env:BB_GPU_WRITE_TWINS_MAX = "32768"
    Write-Host "VRAM Safe Mode: Texture cache capped (6144 MiB) for 6GB/8GB GPUs" -ForegroundColor Yellow
}

# Logging setup
$targetUserDir = if ($UserDir) { $UserDir } elseif ($env:BB_USER_DIR) { $env:BB_USER_DIR } else { Join-Path $DataDir "user" }
if (-not (Test-Path $targetUserDir)) { New-Item -ItemType Directory -Path $targetUserDir | Out-Null }

if ($SaveLog -or ($env:BB_SAVE_LOG -eq "1")) {
    $logsDir = Join-Path $DataDir "logs"
    if (-not (Test-Path $logsDir)) { New-Item -ItemType Directory -Path $logsDir | Out-Null }
    $stamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $env:BB_FRAME_STATS = "1"
    if (-not $env:BB_FRAME_LOG) {
        $env:BB_FRAME_LOG = Join-Path $logsDir "$stamp.frames.csv"
    }
    if (-not $env:BB_READBACK_LOG) {
        $env:BB_READBACK_LOG = Join-Path $logsDir "$stamp.readbacks.csv"
    }
    $mainLog = Join-Path $logsDir "$stamp.log"
    Write-Host "Logging to: $mainLog" -ForegroundColor Cyan
}

# Launch Game
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "Launching Bloodborne via Native Windows Loader..." -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green

$bootLinked = Join-Path $outDir "boot-linked.bin"
$contentBin = Join-Path $outDir "content.bin"
$patchesBin = Join-Path $outDir "patches.bin"

$probeArgs = @(
    $bootLinked,
    "--content-profile", $contentBin,
    "--patches", $patchesBin,
    "--app0", $gameView,
    "--user", $targetUserDir,
    "--timeout", "$Timeout"
)

if ($ExtraProbeArgs) {
    $probeArgs += $ExtraProbeArgs
}

$ErrorActionPreference = 'Continue'
try {
    if ($SaveLog -or ($env:BB_SAVE_LOG -eq "1")) {
        & $probeExe @probeArgs 2>&1 | ForEach-Object { [string]$_ } | Tee-Object -FilePath $mainLog
    } else {
        & $probeExe @probeArgs
    }
} finally {
    # Clean up temporary mod overlay directory if created
    if ($gameView -and ($gameView -ne $gamePath) -and (Test-Path $gameView)) {
        Write-Host "Cleaning up mod overlay view..." -ForegroundColor Gray
        Remove-Item -Recurse -Force $gameView -ErrorAction SilentlyContinue
    }
}

if ($LASTEXITCODE -ne $null -and $LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
