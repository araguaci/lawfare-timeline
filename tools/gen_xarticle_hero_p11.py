#!/usr/bin/env python3
"""Hero 1024x600 px para X Article — tema P11 / loop de extração."""
from __future__ import annotations

import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(
    ROOT,
    "artigos",
    "p11-expandido-loop-extracao-perpetua-xarticle-hero.png",
)

W, H = 1024, 600
BG_TOP = (22, 20, 28)
BG_BOT = (15, 16, 20)
ACCENT = (98, 11, 71)
TITLE_RGB = (230, 228, 225)
SUB_RGB = (160, 158, 155)


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if sys.platform == "win32":
        name = "segoeuib.ttf" if bold else "segoeui.ttf"
        path = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", name)
    else:
        path = (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        )
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def main() -> None:
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        t = y / (H - 1) if H > 1 else 0
        r = int(BG_TOP[0] + (BG_BOT[0] - BG_TOP[0]) * t)
        g = int(BG_TOP[1] + (BG_BOT[1] - BG_TOP[1]) * t)
        b = int(BG_TOP[2] + (BG_BOT[2] - BG_TOP[2]) * t)
        for x in range(W):
            px[x, y] = (r, g, b)

    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, 10], fill=ACCENT)

    title = "P11 — loop de extração perpétua"
    sub = "Economia política brasileira · equilíbrio de Nash"
    seal = "LAWFARE · X Article"

    ft = _font(46, bold=True)
    fs = _font(26, bold=False)
    fk = _font(20, bold=False)

    tw = W - 160
    lines: list[str] = []
    words = title.split()
    cur: list[str] = []
    for w in words:
        test = " ".join(cur + [w])
        bbox = draw.textbbox((0, 0), test, font=ft)
        if bbox[2] - bbox[0] <= tw or not cur:
            cur.append(w)
        else:
            lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))

    y = 190
    lh = 56
    for ln in lines:
        draw.text((80, y), ln, fill=TITLE_RGB, font=ft)
        y += lh

    draw.text((80, y + 8), sub, fill=SUB_RGB, font=fs)

    sb = draw.textbbox((0, 0), seal, font=fk)
    sw = sb[2] - sb[0]
    draw.text((W - 80 - sw, H - 48), seal, fill=SUB_RGB, font=fk)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print("OK", OUT, img.size)


if __name__ == "__main__":
    main()
