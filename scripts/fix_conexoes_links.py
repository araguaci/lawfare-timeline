#!/usr/bin/env python3
"""Corrige referências id_NNN em seções ## Conexoes dos posts Jekyll."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from corpus_links import build_corpus_index, build_thematic_index, fix_conexoes_section  # noqa: E402

POSTS = ROOT / "_posts"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--glob", default="**/*.md", help="Glob relativo a _posts/")
    args = ap.parse_args()

    index = build_corpus_index()
    thematic = build_thematic_index()
    total_files = 0
    total_links = 0

    for path in sorted(POSTS.glob(args.glob)):
        text = path.read_text(encoding="utf-8")
        new_text, n = fix_conexoes_section(text, index, thematic)
        if n == 0:
            continue
        total_files += 1
        total_links += n
        rel = path.relative_to(ROOT)
        if args.dry_run:
            print(f"  [dry-run] {rel}: {n} link(s)")
        else:
            path.write_text(new_text, encoding="utf-8")
            print(f"  OK {rel}: {n} link(s)")

    print(f"\nConcluido: {total_links} link(s) em {total_files} arquivo(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
