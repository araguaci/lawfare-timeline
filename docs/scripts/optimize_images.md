# Guia de Otimização de Imagens

Este guia fornece instruções para otimizar imagens do projeto, melhorando a performance do site.

## Ferramentas Necessárias

### Windows
- [ImageMagick](https://imagemagick.org/script/download.php#windows)
- [cwebp](https://developers.google.com/speed/webp/download) (Google WebP)

### Linux/Mac
```bash
# Ubuntu/Debian
sudo apt-get install imagemagick webp

# macOS
brew install imagemagick webp
```

## Métodos de Otimização

### 1. Converter para WebP

WebP oferece melhor compressão que JPEG/PNG mantendo qualidade visual.

#### Usando cwebp (Google)
```bash
# Converter uma imagem
cwebp input.jpg -q 80 -o output.webp

# Converter todas as imagens em lote (Linux/Mac)
find assets/img -name "*.jpg" -o -name "*.png" | while read img; do
  cwebp "$img" -q 80 -o "${img%.*}.webp"
done

# Windows PowerShell
Get-ChildItem -Path "assets\img" -Include *.jpg,*.png -Recurse | ForEach-Object {
  $webp = $_.FullName -replace '\.(jpg|png)$', '.webp'
  cwebp $_.FullName -q 80 -o $webp
}
```

### 2. Redimensionar Imagens Grandes

Imagens muito grandes aumentam o tempo de carregamento.

```bash
# Redimensionar mantendo proporção (max 1920px)
magick convert input.jpg -resize 1920x1920> output.jpg

# Criar versões em diferentes tamanhos
magick convert input.jpg -resize 800x800> thumb.jpg
magick convert input.jpg -resize 1920x1920> large.jpg
```

### 3. Comprimir JPEG/PNG

```bash
# JPEG com qualidade 85 (boa qualidade, menor tamanho)
magick convert input.jpg -quality 85 output.jpg

# PNG com compressão
magick convert input.png -strip -quality 85 output.png
```

### 4. Lazy Loading

Adicione `loading="lazy"` nas tags de imagem no HTML:

```html
<img src="image.jpg" alt="Descrição" loading="lazy">
```

Para Jekyll, você pode criar um include:

```liquid
{% assign image_path = include.path %}
{% assign image_alt = include.alt | default: "" %}
{% assign image_class = include.class | default: "" %}

<picture>
  <source srcset="{{ image_path | replace: '.jpg', '.webp' | replace: '.png', '.webp' }}" type="image/webp">
  <img src="{{ image_path }}" alt="{{ image_alt }}" class="{{ image_class }}" loading="lazy">
</picture>
```

## Script Automatizado

Crie um script `scripts/optimize_images.sh` (Linux/Mac) ou `scripts/optimize_images.ps1` (Windows):

### Linux/Mac (optimize_images.sh)
```bash
#!/bin/bash

# Converter para WebP
find assets/img -type f \( -name "*.jpg" -o -name "*.png" \) | while read img; do
  if [ ! -f "${img%.*}.webp" ]; then
    echo "Convertendo $img para WebP..."
    cwebp "$img" -q 80 -o "${img%.*}.webp"
  fi
done

# Redimensionar imagens muito grandes
find assets/img -type f \( -name "*.jpg" -o -name "*.png" \) | while read img; do
  width=$(magick identify -format "%w" "$img")
  if [ $width -gt 1920 ]; then
    echo "Redimensionando $img..."
    magick convert "$img" -resize 1920x1920> "$img"
  fi
done

echo "Otimização concluída!"
```

### Windows (optimize_images.ps1)
**Script completo disponível em:** `scripts/optimize_images.ps1`

**Uso básico:**
```powershell
.\scripts\optimize_images.ps1
```

**Com opções:**
```powershell
# Qualidade personalizada
.\scripts\optimize_images.ps1 -Quality 85

# Modo de teste (não modifica arquivos)
.\scripts\optimize_images.ps1 -DryRun

# Pasta específica
.\scripts\optimize_images.ps1 -Path "assets\icons"
```

**Ver documentação completa:** `scripts/README_OTIMIZACAO.md`

## Boas Práticas

1. **Use WebP com fallback**: Sempre forneça versão JPEG/PNG para navegadores antigos
2. **Lazy loading**: Carregue imagens apenas quando necessário
3. **Tamanhos responsivos**: Use `srcset` para diferentes resoluções
4. **Compressão adequada**: 80-85% de qualidade geralmente é suficiente
5. **Remova metadados**: Use `-strip` para remover EXIF data
6. **Otimize antes de commit**: Não commite imagens não otimizadas

## Verificar Resultados

```bash
# Verificar tamanho das imagens
du -sh assets/img/*

# Comparar antes/depois
ls -lh assets/img/*.jpg
ls -lh assets/img/*.webp
```

## Recursos Adicionais

- [Web.dev - Image Optimization](https://web.dev/fast/#optimize-your-images)
- [Squoosh](https://squoosh.app/) - Ferramenta online de otimização
- [TinyPNG](https://tinypng.com/) - Compressão online
- [ImageOptim](https://imageoptim.com/) - Ferramenta desktop

