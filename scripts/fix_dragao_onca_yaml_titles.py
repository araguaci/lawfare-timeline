#!/usr/bin/env python3
"""Corrige títulos YAML com aspas internas nos posts dragao-onca."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "_posts" / "dragao-onca"


def yaml_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def fix_title_line(text: str) -> tuple[str, bool]:
    match = re.search(r"^(title:\s*)\"(.+)\"(\s*)$", text, re.MULTILINE)
    if not match:
        return text, False

    title = match.group(2)
    if '"' not in title and "\\\"" not in title:
        return text, False

    escaped = yaml_escape(title)
    if escaped == title:
        return text, False

    new_line = f'{match.group(1)}"{escaped}"{match.group(3)}'
    new_text = text[: match.start()] + new_line + text[match.end() :]
    return new_text, True


def main() -> None:
    fixed = 0
    for path in sorted(POSTS_DIR.glob("*.md")):
        original = path.read_text(encoding="utf-8")
        updated, changed = fix_title_line(original)
        if changed:
            path.write_text(updated, encoding="utf-8")
            fixed += 1
            print(path.name)
    print(f"fixed {fixed}")


if __name__ == "__main__":
    main()
