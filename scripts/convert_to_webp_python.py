#!/usr/bin/env python3
"""Converte uma imagem para WebP ao lado do original (fallback para convert_to_webp.ps1)."""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image


def main() -> None:
    if len(sys.argv) < 3:
        print("Uso: convert_to_webp_python.py <imagem.png|jpg> <qualidade 1-100>", file=sys.stderr)
        sys.exit(1)
    src = Path(sys.argv[1]).resolve()
    quality = max(1, min(100, int(sys.argv[2])))
    if not src.is_file():
        print(f"Arquivo nao encontrado: {src}", file=sys.stderr)
        sys.exit(1)
    dest = src.with_suffix(".webp")

    im = Image.open(src)
    if im.mode == "P":
        im = im.convert("RGBA")
    elif im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGB")

    im.save(dest, format="WEBP", quality=quality, method=6)
    print(dest)


if __name__ == "__main__":
    main()
