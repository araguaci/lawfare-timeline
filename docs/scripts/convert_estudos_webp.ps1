# Converte imagens raster usadas nos artigos da categoria estudos para WebP.
# Mesma ordem de ferramentas que convert_to_webp.ps1 / optimize_images.ps1:
#   cwebp > ImageMagick > Python (Pillow via convert_to_webp_python.py).
#
# Por defeito processa:
#   - assets\img\estudos  (capas referenciadas em image.target dos posts estudos)
# Opcionalmente:
#   - artigos\*.png correspondentes a heroes X Article (-IncludeArtigosHero)
#
# Uso:
#   .\scripts\convert_estudos_webp.ps1
#   .\scripts\convert_estudos_webp.ps1 -Force
#   .\scripts\convert_estudos_webp.ps1 -Quality 82 -IncludeArtigosHero

param(
    [string]$EstudosImgPath = "assets\img\estudos",
    [string]$ArtigosPath = "artigos",
    [int]$Quality = 82,
    [switch]$IncludeArtigosHero,
    [switch]$Force,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptRoot

function Resolve-RepoPath {
    param([string]$Relative)
    return Join-Path $repoRoot $Relative
}

function Initialize-Converters {
    $useCwebp = $false
    $useImageMagick = $false
    $usePython = $false

    try {
        & cwebp -version 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) { $useCwebp = $true }
    } catch { }

    if (-not $useCwebp) {
        try {
            & magick -version 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) { $useImageMagick = $true }
        } catch { }
    }

    if (-not $useCwebp -and -not $useImageMagick) {
        $pythonCheck = & python -c "from PIL import Image; print('ok')" 2>&1
        if ($LASTEXITCODE -eq 0) { $usePython = $true }
    }

    if (-not $useCwebp -and -not $useImageMagick -and -not $usePython) {
        Write-Host "Nenhuma ferramenta encontrada (cwebp, magick ou Python+Pillow)." -ForegroundColor Red
        Write-Host "Instale uma delas ou execute: pip install Pillow" -ForegroundColor Yellow
        exit 1
    }

    if ($useCwebp) { Write-Host "Usando: cwebp" -ForegroundColor Green }
    elseif ($useImageMagick) { Write-Host "Usando: ImageMagick (magick)" -ForegroundColor Green }
    else { Write-Host "Usando: Python Pillow (scripts\convert_to_webp_python.py)" -ForegroundColor Green }

    return @{
        Cwebp           = $useCwebp
        ImageMagick     = $useImageMagick
        Python          = $usePython
        PythonConverter = Join-Path $scriptRoot "convert_to_webp_python.py"
    }
}

function Convert-OneToWebP {
    param(
        [System.IO.FileInfo]$File,
        [hashtable]$Tools,
        [int]$Quality,
        [bool]$ForceConv,
        [bool]$DryRunMode
    )

    $webpPath = Join-Path $File.DirectoryName ("{0}.webp" -f $File.BaseName)
    if ((Test-Path $webpPath) -and -not $ForceConv) {
        Write-Host "  Ignorado (WebP ja existe, use -Force): $($File.Name)" -ForegroundColor Gray
        return @{ Ok = $true; Skipped = $true }
    }

    if ($DryRunMode) {
        Write-Host "  [DRY RUN] $($File.Name) -> $(Split-Path -Leaf $webpPath)" -ForegroundColor Yellow
        return @{ Ok = $true; Skipped = $false }
    }

    $srcPath = $File.FullName
    $ok = $false

    if ($Tools.Cwebp) {
        $argLine = '-q ' + $Quality + ' "' + $srcPath + '" -o "' + $webpPath + '"'
        cmd /c "cwebp $argLine >nul 2>&1"
        $ok = (Test-Path $webpPath) -and ($LASTEXITCODE -eq 0)
    }
    elseif ($Tools.ImageMagick) {
        & magick convert $srcPath -quality $Quality $webpPath 2>&1 | Out-Null
        $ok = ($LASTEXITCODE -eq 0) -and (Test-Path $webpPath)
    }
    elseif ($Tools.Python) {
        & python $Tools.PythonConverter $srcPath $Quality 2>&1 | Out-Host
        $ok = Test-Path $webpPath
    }

    if (-not $ok) {
        Write-Host "  ERRO: $($File.Name)" -ForegroundColor Red
        return @{ Ok = $false; Skipped = $false }
    }

    $before = $File.Length
    $after = (Get-Item $webpPath).Length
    $pct = if ($before -gt 0) { [math]::Round((1 - ($after / $before)) * 100, 1) } else { 0 }
    Write-Host ('  OK: {0} -> {1} ({2} KB -> {3} KB; ~{4}% menor vs raster)' -f $File.Name, (Split-Path -Leaf $webpPath), [math]::Round($before / 1KB, 1), [math]::Round($after / 1KB, 1), $pct) -ForegroundColor Green
    return @{ Ok = $true; Skipped = $false }
}

Write-Host "Conversao WebP - estudos / artigos" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

$tools = Initialize-Converters

$dirs = @()
$estudosAbs = Resolve-RepoPath $EstudosImgPath
if (-not (Test-Path $estudosAbs)) {
    Write-Host "Pasta nao existe (crie ou ajuste -EstudosImgPath): $estudosAbs" -ForegroundColor Yellow
} else {
    $dirs += $estudosAbs
}

$targets = @()
foreach ($d in $dirs) {
    $targets += Get-ChildItem -LiteralPath $d -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Extension -match '^\.(png|jpe?g)$' }
}

if ($IncludeArtigosHero) {
    $artAbs = Resolve-RepoPath $ArtigosPath
    if (Test-Path $artAbs) {
        # Heroes gerados para X Articles (*.png na pasta artigos)
        $targets += Get-ChildItem -LiteralPath $artAbs -File -Filter "*.png" -ErrorAction SilentlyContinue
    }
}

if ($targets.Count -eq 0) {
    Write-Host "Nenhum PNG/JPEG encontrado em assets/img/estudos" -ForegroundColor Yellow
    if ($IncludeArtigosHero) {
        Write-Host "(nem heroes PNG em artigos/)" -ForegroundColor Yellow
    }
    Write-Host "Coloque masters raster na pasta ou use -IncludeArtigosHero para heroes." -ForegroundColor Gray
    exit 0
}

Write-Host ""
Write-Host "Ficheiros a converter: $($targets.Count) | Qualidade: $Quality | Force: $Force" -ForegroundColor White
Write-Host ""

$okCount = 0
$skipCount = 0
$failCount = 0

$i = 0
foreach ($f in $targets) {
    $i++
    $rel = $f.FullName.Substring($repoRoot.Length).TrimStart('\')
    Write-Host "[$i/$($targets.Count)] $rel"
    $r = Convert-OneToWebP -File $f -Tools $tools -Quality $Quality -ForceConv:$Force -DryRunMode:$DryRun
    if (-not $r.Ok) { $failCount++ }
    elseif ($r.Skipped) { $skipCount++ }
    else { $okCount++ }
}

Write-Host ""
$summaryColor = if ($failCount -gt 0) { "Yellow" } else { "Cyan" }
Write-Host "Convertidos: $okCount | Ignorados: $skipCount | Falhas: $failCount" -ForegroundColor $summaryColor

if ($failCount -gt 0) { exit 1 }
