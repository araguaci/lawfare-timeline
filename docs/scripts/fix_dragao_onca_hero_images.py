#!/usr/bin/env python3
"""Atualiza image: nos posts dragao-onca para heroes regionais dedicados."""

import re
from pathlib import Path

POSTS = Path(__file__).resolve().parents[1] / "_posts" / "dragao-onca"

RANGES = [
    (1719, 1725, "dragao-onca-bahia.webp"),
    (1726, 1730, "dragao-onca-sao-paulo.webp"),
    (1731, 1734, "dragao-onca-parana.webp"),
    (1735, 1737, "dragao-onca-rio-grande-do-sul.webp"),
    (1738, 1739, "dragao-onca-espirito-santo.webp"),
]

THEMATIC = {
    "t237": "dragao-onca-bahia.webp",
    "t238": "dragao-onca-sao-paulo.webp",
    "t239": "dragao-onca-parana.webp",
    "t240": "dragao-onca-rio-grande-do-sul.webp",
    "t241": "dragao-onca-espirito-santo.webp",
    "t242": "dragao-onca-ranking-cebc.webp",
}


def image_for(path: Path) -> str | None:
    stem = path.stem.lower()
    for key, img in THEMATIC.items():
        if key in stem:
            return img
    m = re.search(r"id(\d+)", stem)
    if m:
        tid = int(m.group(1))
        for lo, hi, img in RANGES:
            if lo <= tid <= hi:
                return img
    return None


def main() -> None:
    changed = 0
    for path in sorted(POSTS.glob("*.md")):
        img = image_for(path)
        if not img:
            continue
        text = path.read_text(encoding="utf-8")
        new_line = f"image: /assets/img/{img}"
        new_text, n = re.subn(
            r"^image:\s*[^\r\n]+$",
            new_line,
            text,
            count=1,
            flags=re.M,
        )
        if n and new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed += 1
            print(f"  {path.name} -> {img}")
    print(f"CHANGED: {changed}")


if __name__ == "__main__":
    main()
