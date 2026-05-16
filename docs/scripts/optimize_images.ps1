# Script de Otimização de Imagens para Windows
# Uso: .\scripts\optimize_images.ps1
# Requer: ImageMagick e cwebp instalados

param(
    [string]$Path = "assets\img",
    [int]$Quality = 80,
    [int]$MaxWidth = 1920,
    [switch]$ConvertToWebP = $true,
    [switch]$Resize = $true,
    [switch]$Compress = $true,
    [switch]$DryRun = $false
)

Write-Host "🖼️  Script de Otimização de Imagens" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se ImageMagick está instalado
$magickInstalled = $false
try {
    $magickVersion = & magick -version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $magickInstalled = $true
        Write-Host "✅ ImageMagick encontrado" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  ImageMagick não encontrado" -ForegroundColor Yellow
    Write-Host "   Instale em: https://imagemagick.org/script/download.php#windows" -ForegroundColor Yellow
}

# Verificar se cwebp está instalado
$webpInstalled = $false
try {
    $webpVersion = & cwebp -version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $webpInstalled = $true
        Write-Host "✅ cwebp encontrado" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  cwebp não encontrado" -ForegroundColor Yellow
    Write-Host "   Instale em: https://developers.google.com/speed/webp/download" -ForegroundColor Yellow
    Write-Host "   Ou use: choco install webp" -ForegroundColor Yellow
}

if (-not $magickInstalled -and -not $webpInstalled) {
    Write-Host ""
    Write-Host "❌ Nenhuma ferramenta de otimização encontrada!" -ForegroundColor Red
    Write-Host "   Instale pelo menos uma das ferramentas acima." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📁 Processando imagens em: $Path" -ForegroundColor Cyan
Write-Host ""

# Estatísticas
$stats = @{
    Processed = 0
    Converted = 0
    Resized = 0
    Compressed = 0
    Skipped = 0
    Errors = 0
    SizeBefore = 0
    SizeAfter = 0
}

# Função para obter tamanho do arquivo
function Get-FileSize {
    param([string]$FilePath)
    if (Test-Path $FilePath) {
        return (Get-Item $FilePath).Length
    }
    return 0
}

# Função para formatar tamanho
function Format-Size {
    param([long]$Bytes)
    $units = @("B", "KB", "MB", "GB")
    $index = 0
    $size = $Bytes
    while ($size -ge 1024 -and $index -lt $units.Length - 1) {
        $size = $size / 1024
        $index++
    }
    return "{0:N2} {1}" -f $size, $units[$index]
}

# Processar imagens
$imageFiles = Get-ChildItem -Path $Path -Include *.jpg,*.jpeg,*.png -Recurse -File

if ($imageFiles.Count -eq 0) {
    Write-Host "⚠️  Nenhuma imagem encontrada em $Path" -ForegroundColor Yellow
    exit 0
}

Write-Host "📊 Encontradas $($imageFiles.Count) imagens" -ForegroundColor Cyan
Write-Host ""

foreach ($file in $imageFiles) {
    $stats.Processed++
    $fileName = $file.Name
    $filePath = $file.FullName
    $fileDir = $file.DirectoryName
    $fileBase = [System.IO.Path]::GetFileNameWithoutExtension($filePath)
    $fileExt = $file.Extension
    
    Write-Host "[$($stats.Processed)/$($imageFiles.Count)] Processando: $fileName" -ForegroundColor White
    
    $sizeBefore = Get-FileSize -FilePath $filePath
    $stats.SizeBefore += $sizeBefore
    
    # Converter para WebP
    if ($ConvertToWebP -and $webpInstalled) {
        $webpPath = Join-Path $fileDir "$fileBase.webp"
        
        if (-not (Test-Path $webpPath)) {
            if (-not $DryRun) {
                try {
                    & cwebp -q $Quality $filePath -o $webpPath 2>&1 | Out-Null
                    if ($LASTEXITCODE -eq 0) {
                        $stats.Converted++
                        $webpSize = Get-FileSize -FilePath $webpPath
                        $savings = $sizeBefore - $webpSize
                        $percent = if ($sizeBefore -gt 0) { ($savings / $sizeBefore) * 100 } else { 0 }
                        Write-Host "   ✅ WebP criado: $(Format-Size $webpSize) (economia: $(Format-Size $savings) - $([math]::Round($percent, 1))%)" -ForegroundColor Green
                    } else {
                        Write-Host "   ❌ Erro ao converter para WebP" -ForegroundColor Red
                        $stats.Errors++
                    }
                } catch {
                    Write-Host "   ❌ Erro: $_" -ForegroundColor Red
                    $stats.Errors++
                }
            } else {
                Write-Host "   [DRY RUN] Criaria WebP: $webpPath" -ForegroundColor Yellow
                $stats.Converted++
            }
        } else {
            Write-Host "   ⏭️  WebP já existe, pulando" -ForegroundColor Gray
            $stats.Skipped++
        }
    }
    
    # Redimensionar imagens grandes
    if ($Resize -and $magickInstalled) {
        try {
            $image = [System.Drawing.Image]::FromFile($filePath)
            $width = $image.Width
            $height = $image.Height
            $image.Dispose()
            
            if ($width -gt $MaxWidth) {
                if (-not $DryRun) {
                    try {
                        $tempPath = "$filePath.tmp"
                        & magick convert $filePath -resize "${MaxWidth}x${MaxWidth}>" $tempPath 2>&1 | Out-Null
                        if ($LASTEXITCODE -eq 0 -and (Test-Path $tempPath)) {
                            Move-Item -Path $tempPath -Destination $filePath -Force
                            $stats.Resized++
                            $newSize = Get-FileSize -FilePath $filePath
                            Write-Host "   ✅ Redimensionado: ${width}x${height} → $(Get-Item $filePath | Select-Object -ExpandProperty Width)x$(Get-Item $filePath | Select-Object -ExpandProperty Height)" -ForegroundColor Green
                        } else {
                            Write-Host "   ❌ Erro ao redimensionar" -ForegroundColor Red
                            $stats.Errors++
                        }
                    } catch {
                        Write-Host "   ❌ Erro: $_" -ForegroundColor Red
                        $stats.Errors++
                    }
                } else {
                    Write-Host "   [DRY RUN] Redimensionaria: ${width}x${height} → max ${MaxWidth}px" -ForegroundColor Yellow
                    $stats.Resized++
                }
            }
        } catch {
            Write-Host "   ⚠️  Não foi possível ler dimensões da imagem" -ForegroundColor Yellow
        }
    }
    
    # Comprimir JPEG/PNG
    if ($Compress -and $magickInstalled) {
        if ($fileExt -match '\.(jpg|jpeg)$') {
            if (-not $DryRun) {
                try {
                    $tempPath = "$filePath.tmp"
                    & magick convert $filePath -quality $Quality -strip $tempPath 2>&1 | Out-Null
                    if ($LASTEXITCODE -eq 0 -and (Test-Path $tempPath)) {
                        $newSize = Get-FileSize -FilePath $tempPath
                        if ($newSize -lt $sizeBefore) {
                            Move-Item -Path $tempPath -Destination $filePath -Force
                            $stats.Compressed++
                            $savings = $sizeBefore - $newSize
                            $percent = if ($sizeBefore -gt 0) { ($savings / $sizeBefore) * 100 } else { 0 }
                            Write-Host "   ✅ Comprimido: $(Format-Size $newSize) (economia: $(Format-Size $savings) - $([math]::Round($percent, 1))%)" -ForegroundColor Green
                        } else {
                            Remove-Item $tempPath -Force
                            Write-Host "   ⏭️  Compressão não reduziu tamanho" -ForegroundColor Gray
                        }
                    }
                } catch {
                    Write-Host "   ❌ Erro ao comprimir: $_" -ForegroundColor Red
                    $stats.Errors++
                }
            } else {
                Write-Host "   [DRY RUN] Comprimiria JPEG com qualidade $Quality" -ForegroundColor Yellow
            }
        } elseif ($fileExt -eq '.png') {
            if (-not $DryRun) {
                try {
                    $tempPath = "$filePath.tmp"
                    & magick convert $filePath -strip -quality 85 $tempPath 2>&1 | Out-Null
                    if ($LASTEXITCODE -eq 0 -and (Test-Path $tempPath)) {
                        $newSize = Get-FileSize -FilePath $tempPath
                        if ($newSize -lt $sizeBefore) {
                            Move-Item -Path $tempPath -Destination $filePath -Force
                            $stats.Compressed++
                            $savings = $sizeBefore - $newSize
                            $percent = if ($sizeBefore -gt 0) { ($savings / $sizeBefore) * 100 } else { 0 }
                            Write-Host "   ✅ Comprimido: $(Format-Size $newSize) (economia: $(Format-Size $savings) - $([math]::Round($percent, 1))%)" -ForegroundColor Green
                        } else {
                            Remove-Item $tempPath -Force
                        }
                    }
                } catch {
                    Write-Host "   ❌ Erro ao comprimir PNG: $_" -ForegroundColor Red
                    $stats.Errors++
                }
            } else {
                Write-Host "   [DRY RUN] Comprimiria PNG" -ForegroundColor Yellow
            }
        }
    }
    
    $sizeAfter = Get-FileSize -FilePath $filePath
    $stats.SizeAfter += $sizeAfter
}

Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "📊 Resumo da Otimização" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Imagens processadas: $($stats.Processed)" -ForegroundColor Green
Write-Host "🔄 Convertidas para WebP: $($stats.Converted)" -ForegroundColor Cyan
Write-Host "📏 Redimensionadas: $($stats.Resized)" -ForegroundColor Cyan
Write-Host "🗜️  Comprimidas: $($stats.Compressed)" -ForegroundColor Cyan
Write-Host "⏭️  Ignoradas: $($stats.Skipped)" -ForegroundColor Gray
Write-Host "❌ Erros: $($stats.Errors)" -ForegroundColor $(if ($stats.Errors -gt 0) { "Red" } else { "Green" })
Write-Host ""
Write-Host "💾 Tamanho total antes: $(Format-Size $stats.SizeBefore)" -ForegroundColor Yellow
Write-Host "💾 Tamanho total depois: $(Format-Size $stats.SizeAfter)" -ForegroundColor Yellow

if ($stats.SizeBefore -gt 0) {
    $totalSavings = $stats.SizeBefore - $stats.SizeAfter
    $totalPercent = ($totalSavings / $stats.SizeBefore) * 100
    Write-Host "💰 Economia total: $(Format-Size $totalSavings) ($([math]::Round($totalPercent, 1))%)" -ForegroundColor Green
}

Write-Host ""
Write-Host "✨ Otimização concluída!" -ForegroundColor Green

