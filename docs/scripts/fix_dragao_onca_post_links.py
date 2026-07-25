#!/usr/bin/env python3
"""Substitui links /timeline/entries/ID por /posts/slug/ nos posts dragao-onca."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from gerar_artigos_dragao_onca import (
    POSTS_DIR,
    build_post_index,
    markdown_link_label,
    post_title_for_timeline_id,
    post_url_for_timeline_id,
)

TIMELINE_LINK_RE = re.compile(
    r"\[Entrada (\d+)\]\(/timeline/entries/\1\)"
)
ENTRY_LINK_RE = re.compile(
    r"(\-\s+\[)(Entrada (\d+)|[^\]]+)(\]\(/posts/[^)]+/\))"
)


def fix_timeline_links(path: Path, post_index: dict[str, dict[str, str]]) -> bool:
    text = path.read_text(encoding="utf-8")

    def repl(match: re.Match[str]) -> str:
        entry_id = match.group(1)
        url = post_url_for_timeline_id(entry_id, post_index)
        return f"[Entrada {entry_id}]({url})"

    updated = TIMELINE_LINK_RE.sub(repl, text)
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def fix_entry_link_labels(path: Path, post_index: dict[str, dict[str, str]]) -> bool:
    text = path.read_text(encoding="utf-8")

    def repl(match: re.Match[str]) -> str:
        prefix, _, entry_id, suffix = match.groups()
        if not entry_id:
            return match.group(0)
        label = markdown_link_label(post_title_for_timeline_id(entry_id, post_index))
        return f"{prefix}{label}{suffix}"

    updated = ENTRY_LINK_RE.sub(repl, text)
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> None:
    post_index = build_post_index()
    fixed_urls = 0
    fixed_labels = 0

    for path in sorted(POSTS_DIR.glob("*.md")):
        if fix_timeline_links(path, post_index):
            fixed_urls += 1
            print(f"url  {path.name}")

    for path in sorted(POSTS_DIR.glob("2026-07-24-t*.md")):
        if fix_entry_link_labels(path, post_index):
            fixed_labels += 1
            print(f"label {path.name}")

    print(f"fixed urls in {fixed_urls} files, labels in {fixed_labels} thematic files")


if __name__ == "__main__":
    main()
