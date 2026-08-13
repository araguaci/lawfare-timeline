#!/usr/bin/env python3
"""Gera pack PWA a partir de public/Gemini_Generated_Transparent.png."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "public" / "Gemini_Generated_Transparent.png"
ICONS = ROOT / "public" / "icons"
BG = (8, 12, 16, 255)  # #080c10
ANY_SIZES = (72, 96, 128, 144, 152, 192, 384, 512)
MASKABLE_SIZES = (192, 512)
# Fração do canvas ocupada pelo emblema (safe zone maskable ~80%)
MASKABLE_SCALE = 0.72
ANY_SCALE = 0.92


def fit_on_canvas(src: Image.Image, size: int, scale: float, opaque_bg: bool) -> Image.Image:
    canvas = Image.new("RGBA", (size, size), BG if opaque_bg else (0, 0, 0, 0))
    side = max(1, int(size * scale))
    icon = src.copy()
    icon.thumbnail((side, side), Image.Resampling.LANCZOS)
    x = (size - icon.width) // 2
    y = (size - icon.height) // 2
    canvas.paste(icon, (x, y), icon)
    return canvas


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"Fonte ausente: {SRC}")
    src = Image.open(SRC).convert("RGBA")
    ICONS.mkdir(parents=True, exist_ok=True)

    # Master 1024
    master = fit_on_canvas(src, 1024, ANY_SCALE, opaque_bg=True)
    master_path = ICONS / "icon-1024.png"
    master.convert("RGB").save(master_path, "PNG", optimize=True)
    print("wrote", master_path.relative_to(ROOT))

    for size in ANY_SIZES:
        # any: fundo escuro (melhor legibilidade em tabs / splash)
        im = fit_on_canvas(src, size, ANY_SCALE, opaque_bg=True)
        path = ICONS / f"icon-{size}.png"
        im.convert("RGB").save(path, "PNG", optimize=True)
        print("wrote", path.relative_to(ROOT))

    for size in MASKABLE_SIZES:
        im = fit_on_canvas(src, size, MASKABLE_SCALE, opaque_bg=True)
        path = ICONS / f"icon-{size}-maskable.png"
        im.convert("RGB").save(path, "PNG", optimize=True)
        print("wrote", path.relative_to(ROOT))

    # apple-touch 180
    apple = fit_on_canvas(src, 180, ANY_SCALE, opaque_bg=True).convert("RGB")
    apple_path = ROOT / "apple-touch-icon.png"
    apple.save(apple_path, "PNG", optimize=True)
    print("wrote", apple_path.relative_to(ROOT))

    # favicon.ico multi-size
    ico_sizes = [16, 32, 48]
    ico_images = [fit_on_canvas(src, s, ANY_SCALE, opaque_bg=True).convert("RGBA") for s in ico_sizes]
    ico_path = ROOT / "favicon.ico"
    ico_images[0].save(
        ico_path,
        format="ICO",
        sizes=[(s, s) for s in ico_sizes],
        append_images=ico_images[1:],
    )
    # espelho em public/
    ico_images[0].save(
        ROOT / "public" / "favicon.ico",
        format="ICO",
        sizes=[(s, s) for s in ico_sizes],
        append_images=ico_images[1:],
    )
    print("wrote", ico_path.relative_to(ROOT))

    # PNG 32 para <link rel=icon type=png>
    fit_on_canvas(src, 32, ANY_SCALE, opaque_bg=True).convert("RGB").save(
        ICONS / "icon-32.png", "PNG", optimize=True
    )
    print("wrote public/icons/icon-32.png")
    print("OK — fonte:", SRC.relative_to(ROOT))


if __name__ == "__main__":
    main()
