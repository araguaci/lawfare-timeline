# Script para converter imagem específica para WebP
# Uso: .\scripts\convert_to_webp.ps1 -ImagePath "assets\img\pacto-federativo.png"

param(
    [Parameter(Mandatory=$true)]
    [string]$ImagePath,
    [int]$Quality = 80
)

Write-Host "Convertendo Imagem para WebP" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

# Verificar se cwebp, ImageMagick ou Python esta instalado
$useImageMagick = $false
$useCwebp = $false
$usePython = $false

try {
    $null = & cwebp -version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $useCwebp = $true
        Write-Host "cwebp encontrado" -ForegroundColor Green
    }
} catch {
    # Tentar ImageMagick
    try {
        $null = & magick -version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $useImageMagick = $true
            Write-Host "ImageMagick encontrado" -ForegroundColor Green
        }
    } catch {
        # Tentar Python com Pillow
        try {
            $pythonCheck = & python -c "from PIL import Image; print('ok')" 2>&1
            if ($LASTEXITCODE -eq 0) {
                $usePython = $true
                Write-Host "Python com Pillow encontrado (usando como alternativa)" -ForegroundColor Green
            }
        } catch {
            Write-Host "Nenhuma ferramenta encontrada!" -ForegroundColor Red
            Write-Host "   Instale cwebp: https://developers.google.com/speed/webp/download" -ForegroundColor Yellow
            Write-Host "   Ou instale ImageMagick: https://imagemagick.org/script/download.php#windows" -ForegroundColor Yellow
            Write-Host "   Ou instale Python Pillow: pip install Pillow" -ForegroundColor Yellow
            Write-Host "   Ou use: choco install webp imagemagick" -ForegroundColor Yellow
            exit 1
        }
    }
}

# Verificar se o arquivo existe
if (-not (Test-Path $ImagePath)) {
    Write-Host "Arquivo nao encontrado: $ImagePath" -ForegroundColor Red
    exit 1
}

$file = Get-Item $ImagePath
$fileDir = $file.DirectoryName
$fileName = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
$webpPath = Join-Path $fileDir "$fileName.webp"

Write-Host "Arquivo original: $ImagePath" -ForegroundColor White
Write-Host "Arquivo WebP: $webpPath" -ForegroundColor White
Write-Host "Qualidade: $Quality" -ForegroundColor White
Write-Host ""

# Verificar se WebP ja existe
if (Test-Path $webpPath) {
    Write-Host "Arquivo WebP ja existe: $webpPath" -ForegroundColor Yellow
    $overwrite = Read-Host "Deseja sobrescrever? (S/N)"
    if ($overwrite -ne 'S' -and $overwrite -ne 's') {
        Write-Host "Operacao cancelada" -ForegroundColor Gray
        exit 0
    }
}

# Obter tamanho original
$originalSize = $file.Length
Write-Host "Tamanho original: $([math]::Round($originalSize / 1KB, 2)) KB" -ForegroundColor Cyan

# Converter para WebP
Write-Host ""
Write-Host "Convertendo..." -ForegroundColor Yellow

try {
    if ($useCwebp) {
        & cwebp -q $Quality $ImagePath -o $webpPath 2>&1 | Out-Null
        $success = ($LASTEXITCODE -eq 0)
    } elseif ($useImageMagick) {
        & magick convert $ImagePath -quality $Quality $webpPath 2>&1 | Out-Null
        $success = ($LASTEXITCODE -eq 0)
    } elseif ($usePython) {
        $scriptPath = Join-Path (Split-Path $MyInvocation.MyCommand.Path) "convert_to_webp_python.py"
        & python $scriptPath $ImagePath $Quality 2>&1 | Out-Host
        $success = (Test-Path $webpPath)
    } else {
        Write-Host "Nenhuma ferramenta disponivel!" -ForegroundColor Red
        exit 1
    }
    
    if ($success -and (Test-Path $webpPath)) {
        $webpFile = Get-Item $webpPath
        $webpSize = $webpFile.Length
        $savings = $originalSize - $webpSize
        $percent = if ($originalSize -gt 0) { ($savings / $originalSize) * 100 } else { 0 }
        
        Write-Host ""
        Write-Host "Conversao concluida!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Estatisticas:" -ForegroundColor Cyan
        Write-Host "   Original: $([math]::Round($originalSize / 1KB, 2)) KB" -ForegroundColor White
        Write-Host "   WebP: $([math]::Round($webpSize / 1KB, 2)) KB" -ForegroundColor Green
        Write-Host "   Economia: $([math]::Round($savings / 1KB, 2)) KB ($([math]::Round($percent, 1))%)" -ForegroundColor Green
        Write-Host ""
        Write-Host "Arquivo criado: $webpPath" -ForegroundColor Cyan
    } else {
        Write-Host "Erro ao converter imagem" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "Erro: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Processamento concluido!" -ForegroundColor Green

