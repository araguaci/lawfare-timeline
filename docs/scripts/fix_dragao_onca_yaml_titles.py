#!/usr/bin/env python3
"""Corrige títulos YAML com aspas internas nos posts dragao-onca."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "_posts" / "dragao-onca"


def yaml_escape(s: str) -> str:
    return s.replace('"', '\\"').replace("\n", " ")


def rebuild_titles_from_h1() -> None:
    fixed = 0
    for path in sorted(POSTS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        h1 = re.search(r"^# (.+)$", text, re.MULTILINE)
        if not h1:
            continue
        title = yaml_escape(h1.group(1).strip())
        new_text, count = re.subn(
            r'^title: ".*"$',
            f'title: "{title}"',
            text,
            count=1,
            flags=re.MULTILINE,
        )
        if count and new_text != text:
            path.write_text(new_text, encoding="utf-8")
            fixed += 1
            print(path.name)
    print(f"rebuilt {fixed}")


def fix_title_line(text: str) -> tuple[str, bool]:
    match = re.search(r"^(title:\s*)\"(.+)\"(\s*)$", text, re.MULTILINE)
    if not match:
        return text, False

    title = match.group(2)
    if "\\\"" in title:
        return text, False
    if '"' not in title:
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


def fix_empty_year_tags() -> None:
    fixed = 0
    for path in sorted(POSTS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        updated = text.replace('["dragao-onca", "",', '["dragao-onca", "2026",', 1)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            fixed += 1
            print(path.name)
    print(f"tags fixed {fixed}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--tags":
        fix_empty_year_tags()
    elif len(sys.argv) > 1 and sys.argv[1] == "--rebuild-titles":
        rebuild_titles_from_h1()
    else:
        main()
