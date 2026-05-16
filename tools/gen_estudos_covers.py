#!/usr/bin/env python3
"""Gera imagens WebP de capa para estudos (tema escuro LAWFARE / Chirpy)."""
from __future__ import annotations

import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "estudos")

W, H = 1280, 720

# Tema: fundo escuro + vinho (#620b47 sidebar) + texto claro
BG_TOP = (22, 20, 28)
BG_BOT = (15, 16, 20)
ACCENT = (98, 11, 71)  # #620b47
SUBTLE = (60, 58, 65)
TITLE_RGB = (230, 228, 225)
SUB_RGB = (160, 158, 155)

CARDS: list[tuple[str, str, str]] = [
    ("p11-loop-extracao.webp", "P11 — loop de extração", "Economia política · proteção social"),
    ("delacao-como-jogo.webp", "Delação como jogo", "Teoria dos jogos · colaboração premiada"),
    ("foro-privilegiado.webp", "Foro privilegiado", "Jurisdição como escudo"),
    ("geocorrupcao.webp", "Geocorrupção", "Mapa da captura institucional"),
    ("liminar-monocratica.webp", "Liminar monocrática", "STF · poder individual"),
    ("dosimetria-impunidade.webp", "Dosimetria da impunidade", "Lei 15.402 · tratamento diferenciado"),
    ("hc-seletivo.webp", "HC seletivo", "Habeas corpus como privilégio"),
    ("penduricalhos-dossie.webp", "Penduricalhos", "Dossiê · custo e resistência"),
    ("estado-como-reu.webp", "Estado como réu", "Weaponização processual"),
    ("captura-regulatoria.webp", "Captura regulatória", "BACEN · CVM · INSS"),
]


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if sys.platform == "win32":
        name = "segoeuib.ttf" if bold else "segoeui.ttf"
        path = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", name)
    else:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def draw_cover(title: str, subtitle: str) -> Image.Image:
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        t = y / (H - 1) if H > 1 else 0
        r = int(BG_TOP[0] + (BG_BOT[0] - BG_TOP[0]) * t)
        g = int(BG_TOP[1] + (BG_BOT[1] - BG_TOP[1]) * t)
        b = int(BG_TOP[2] + (BG_BOT[2] - BG_TOP[2]) * t)
        for x in range(W):
            px[x, y] = (r, g, b)

    draw = ImageDraw.Draw(img, "RGBA")
    # faixa superior acento
    draw.rectangle([0, 0, W, 8], fill=ACCENT)
    # linha decorativa
    draw.line([(48, 420), (W - 48, 420)], fill=SUBTLE, width=2)

    font_title = _load_font(44, bold=True)
    font_sub = _load_font(28, bold=False)

    # wrap title if needed (simple)
    tw = W - 96
    lines = []
    words = title.split()
    cur: list[str] = []
    for w in words:
        test = " ".join(cur + [w])
        bbox = draw.textbbox((0, 0), test, font=font_title)
        if bbox[2] - bbox[0] <= tw or not cur:
            cur.append(w)
        else:
            lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))

    y = 280
    lh = 56
    for ln in lines:
        draw.text((48, y), ln, fill=TITLE_RGB, font=font_title)
        y += lh

    draw.text((48, y + 20), subtitle, fill=SUB_RGB, font=font_sub)

    # canto: selo
    seal = "LAWFARE · estudos"
    font_seal = _load_font(22, bold=False)
    sb = draw.textbbox((0, 0), seal, font=font_seal)
    sw = sb[2] - sb[0]
    draw.text((W - 48 - sw, H - 56), seal, fill=SUB_RGB, font=font_seal)

    return img.convert("RGB")


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for fname, title, sub in CARDS:
        path = os.path.join(OUT, fname)
        im = draw_cover(title, sub)
        im.save(path, "WEBP", quality=82, method=6)
        print("OK", path)
    print(f"Geradas {len(CARDS)} imagens em {OUT}")


if __name__ == "__main__":
    main()
