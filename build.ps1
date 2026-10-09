# PowerShell build script for bloodborne_pc on Windows
[CmdletBinding()]
param(
    [switch]$Rebuild,
    [switch]$Test
)

$ErrorActionPreference = 'Stop'
$repoRoot = $PSScriptRoot

# Locate MSYS2 UCRT64 toolchain dynamically
$prefix = if ($env:MINGW_PREFIX) {
    $env:MINGW_PREFIX
} elseif (Test-Path 'C:\msys64\ucrt64') {
    'C:\msys64\ucrt64'
} elseif (Test-Path 'D:\msys64\ucrt64') {
    'D:\msys64\ucrt64'
} else {
    ""
}

if ($prefix -and (Test-Path (Join-Path $prefix "bin"))) {
    $binDir = Join-Path $prefix "bin"
    if ($env:PATH -notlike "*$binDir*") {
        $env:PATH = "$binDir;$env:PATH"
    }
}

$gcc = Get-Command gcc -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue
$gxx = Get-Command g++ -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue
if (-not $gcc) {
    Write-Error "GCC not found! Please ensure MSYS2 UCRT64 (gcc) is installed."
    exit 1
}
if (-not $gxx) {
    $gxx = 'g++'
}

$ar = 'ar'
if ($prefix -and (Test-Path (Join-Path $prefix "bin\ar.exe"))) { $ar = Join-Path $prefix "bin\ar.exe" }
$cmake = 'cmake'
if ($prefix -and (Test-Path (Join-Path $prefix "bin\cmake.exe"))) { $cmake = Join-Path $prefix "bin\cmake.exe" }
$ninja = 'ninja'
if ($prefix -and (Test-Path (Join-Path $prefix "bin\ninja.exe"))) { $ninja = Join-Path $prefix "bin\ninja.exe" }

$incDir = if ($prefix) { ($prefix.Replace('\', '/') + "/include") } else { "C:/msys64/ucrt64/include" }
$libDir = if ($prefix) { ($prefix.Replace('\', '/') + "/lib") } else { "C:/msys64/ucrt64/lib" }

$outDir = Join-Path $repoRoot "out"
if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir | Out-Null }

# Build libatrac9.a if needed
$atrac9Archive = Join-Path $outDir "libatrac9.a"
$atrac9Src = Join-Path $repoRoot "third_party\LibAtrac9\C\src"
if ($Rebuild -or (-not (Test-Path $atrac9Archive))) {
    Write-Host "Building LibAtrac9..." -ForegroundColor Cyan
    $atrac9ObjDir = Join-Path $outDir "atrac9"
    if (-not (Test-Path $atrac9ObjDir)) { New-Item -ItemType Directory -Path $atrac9ObjDir | Out-Null }
    Get-ChildItem -Path $atrac9Src -Filter *.c | ForEach-Object {
        $obj = Join-Path $atrac9ObjDir "$($_.BaseName).o"
        & $gcc -std=c99 -O2 -g -w -c $_.FullName -o $obj
    }
    $objs = Get-ChildItem -Path $atrac9ObjDir -Filter *.o | Select-Object -ExpandProperty FullName
    & $ar rcs $atrac9Archive @objs
}

# Build libbbgpu.a if needed
$gpuLib = Join-Path $outDir "gpu\libbbgpu.a"
if ($Rebuild -or (-not (Test-Path $gpuLib))) {
    Write-Host "Building GPU subsystem (libbbgpu.a)..." -ForegroundColor Cyan
    $gpuOut = Join-Path $outDir "gpu"
    if (-not (Test-Path $gpuOut)) { New-Item -ItemType Directory -Path $gpuOut | Out-Null }
    Push-Location $repoRoot
    try {
        & $cmake -S gpu -B out/gpu -G Ninja -DCMAKE_BUILD_TYPE=RelWithDebInfo
        & $ninja -C out/gpu bbgpu
    } finally {
        Pop-Location
    }
}

# Compile runtime C files
Write-Host "Compiling runtime backend..." -ForegroundColor Cyan
$cflags = @(
    "-std=c11", "-O2", "-g", "-Wall", "-Wextra",
    "-pthread", "-I.", "-Isrc", "-I$incDir"
)

$cFiles = @(
    "src/probe.c",
    "src/runtime.c",
    "src/runtime_ajm.c",
    "src/runtime_audio.c",
    "src/runtime_content.c",
    "src/runtime_file.c",
    "src/runtime_kernel.c",
    "src/runtime_memory.c",
    "src/runtime_mutex.c",
    "src/runtime_pad.c",
    "src/runtime_rtc.c",
    "src/runtime_rwlock.c",
    "src/runtime_savedata.c",
    "src/runtime_sema.c",
    "src/runtime_services.c",
    "src/runtime_thread.c",
    "src/runtime_time.c",
    "src/vulkan_smoke.c"
)

$objFiles = @()
foreach ($file in $cFiles) {
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($file)
    $objPath = Join-Path $outDir "$baseName.o"
    $objFiles += $objPath
    $srcPath = Join-Path $repoRoot $file
    
    $shouldCompile = $Rebuild -or (-not (Test-Path $objPath)) -or ((Get-Item $srcPath).LastWriteTime -gt (Get-Item $objPath).LastWriteTime)
    if ($shouldCompile) {
        Write-Host "  Compiling $file -> $baseName.o"
        & $gcc @cflags -c $srcPath -o $objPath
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
}

# Link bb-probe.exe
Write-Host "Linking out/bb-probe.exe..." -ForegroundColor Cyan
$ldflags = @(
    "-Wl,--image-base=0x140000000",
    "-Lout/gpu", "-lbbgpu",
    "out/gpu/third_party/fsr-vulkan/libffx_vulkan_portable.a",
    "out/gpu/third_party/fsr-vulkan/libffx_vulkan_fsr3_vk_backend_1_1_4.a",
    "out/gpu/third_party/fsr-vulkan/libffx_vulkan_fsr3_host_1_1_4.a",
    "out/gpu/third_party/fsr-vulkan/libffx_vulkan_fsr4_v07_vulkan.a",
    "out/gpu/third_party/fsr-vulkan/libffx_vulkan_fsr4_v07_assets.a",
    "out/gpu/third_party/sirit/src/libsirit.a",
    "-L$libDir",
    "-lfmt", "-lxxhash", "-lSDL3",
    "-lavformat", "-lavcodec", "-lswscale", "-lswresample", "-lavutil",
    "-lminiz", "-lZydis", "-lZycore",
    "-lvulkan-1", "-lws2_32", "-lntdll", "-ldxgi", "-lwinmm"
)

$probeExe = Join-Path $outDir "bb-probe.exe"
& $gxx @objFiles $atrac9Archive @ldflags -o $probeExe
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Successfully built $probeExe" -ForegroundColor Green

# Build bb-gpu-capabilities.exe
Write-Host "Building out/bb-gpu-capabilities.exe..." -ForegroundColor Cyan
$capsExe = Join-Path $outDir "bb-gpu-capabilities.exe"
& $gcc -std=c11 -O2 -Wall -Wextra -I$incDir (Join-Path $repoRoot "tools/gpu_capabilities.c") -L$libDir -lvulkan-1 -lSDL3 -o $capsExe
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Successfully built $capsExe" -ForegroundColor Green

if ($Test) {
    Write-Host "Running Vulkan smoke test..." -ForegroundColor Cyan
    & $probeExe --vulkan-only
    & $capsExe --live-resolution
}
