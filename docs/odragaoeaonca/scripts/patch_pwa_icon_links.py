#!/usr/bin/env python3
"""Insere links de favicon/PWA em todos os HTML do projeto."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SNIPPET = """\
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/public/icons/icon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<meta name="theme-color" content="#080c10">
"""

# Remove blocos antigos de icon / apple / manifest / theme-color
OLD = re.compile(
    r'[ \t]*<link\s+rel="(?:icon|apple-touch-icon|manifest)"[^>]*>\s*'
    r'|[ \t]*<meta\s+name="theme-color"[^>]*>\s*',
    re.I,
)


def patch(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "<head" not in text.lower():
        return False
    cleaned = OLD.sub("", text)
    # Inserir após viewport, senão após charset, senão após <head>
    m = re.search(r'(<meta\s+name="viewport"[^>]*>\s*)', cleaned, re.I)
    if m:
        new = cleaned[: m.end()] + SNIPPET + cleaned[m.end() :]
    else:
        m = re.search(r'(<meta\s+charset="[^"]*"\s*/?>\s*)', cleaned, re.I)
        if m:
            new = cleaned[: m.end()] + SNIPPET + cleaned[m.end() :]
        else:
            m = re.search(r'(<head[^>]*>\s*)', cleaned, re.I)
            if not m:
                return False
            new = cleaned[: m.end()] + SNIPPET + cleaned[m.end() :]
    if new == text:
        return False
    path.write_text(new, encoding="utf-8")
    return True


def main() -> None:
    files = list(ROOT.glob("*.html")) + list((ROOT / "timeline").glob("*.html"))
    n = 0
    for path in sorted(files):
        if patch(path):
            print("patched", path.relative_to(ROOT))
            n += 1
    print(f"OK — {n} arquivos")


if __name__ == "__main__":
    main()
