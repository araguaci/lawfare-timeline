#!/usr/bin/env python3
"""Corrige links internos em _posts/dragao-onca/2026-07-24-t*.md."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "_posts" / "dragao-onca"

THEMATIC_SHORT = {
    "228": "Goiás",
    "229": "Brasil federal",
    "230": "Pará",
    "231": "Amazonas",
    "232": "Minas Gerais",
    "233": "Síntese v1",
    "234": "Braço jurídico",
    "235": "PL 2.780/2024",
    "236": "Braço diplomático",
    "237": "Bahia",
    "238": "São Paulo",
    "239": "Paraná",
    "240": "Rio Grande do Sul",
    "241": "Espírito Santo",
    "242": "Ranking CEBC",
    "243": "Síntese final",
    "244": "Amapá",
    "245": "Rio de Janeiro",
    "246": "Santa Catarina",
}


def extract_title(text: str) -> str:
    m = re.search(r'^title:\s*"(.*)"\s*$', text, re.M)
    if m:
        return m.group(1).replace('\\"', '"')
    m = re.search(r"^title:\s*'(.*)'\s*$", text, re.M)
    return m.group(1) if m else ""


def build_index() -> dict[str, dict[str, str]]:
    index: dict[str, dict[str, str]] = {}
    for path in sorted(POSTS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        tid = None
        m = re.search(r"^timeline_id:\s*(\d+)\s*$", text, re.M)
        if m:
            tid = m.group(1)
        else:
            m2 = re.search(r"2026-07-24-t(\d+)", path.name)
            if m2:
                tid = m2.group(1)
        if not tid:
            continue
        slug = path.stem
        index[tid] = {"slug": slug, "title": extract_title(text), "path": path.name}
    return index


def link_for_id(tid: str, index: dict) -> tuple[str, str] | None:
    meta = index.get(str(tid).replace("id_", ""))
    if not meta:
        return None
    label = meta["title"]
    if len(label) > 90:
        short = THEMATIC_SHORT.get(str(tid))
        if short:
            label = f"T-{tid} — {short}"
        else:
            label = label[:87] + "..."
    return label, f"/posts/{meta['slug']}/"


def fix_file(path: Path, index: dict) -> int:
    text = path.read_text(encoding="utf-8")
    orig = text
    n = 0

    def repl_entrada(m: re.Match) -> str:
        nonlocal n
        tid = m.group(1)
        got = link_for_id(tid, index)
        if not got:
            return m.group(0)
        n += 1
        label = got[0]
        if tid in THEMATIC_SHORT and not label.startswith("T-"):
            label = f"T-{tid} — {THEMATIC_SHORT[tid]}"
        return f"[{label}]({got[1]})"

    text = re.sub(
        r"\[Entrada T-(\d+)\]\(/timeline/entries/T-\d+\)",
        repl_entrada,
        text,
    )

    def repl_t_short(m: re.Match) -> str:
        nonlocal n
        tid = m.group(1)
        got = link_for_id(tid, index)
        if not got:
            return m.group(0)
        n += 1
        short = THEMATIC_SHORT.get(tid, m.group(2).strip())
        return f"[T-{tid} — {short}]({got[1]})"

    text = re.sub(
        r"\[T-(\d+) — ([^\]]+)\]\(/posts/t\d+[^)]*\)",
        repl_t_short,
        text,
    )

    text = re.sub(
        r"\[T-(\d+)\]\(/posts/t\d+[^)]*\)",
        repl_entrada,
        text,
    )

    def repl_main_broken(m: re.Match) -> str:
        nonlocal n
        tid = m.group(1)
        got = link_for_id(tid, index)
        if not got:
            return m.group(0)
        n += 1
        return f"[{got[0]}]({got[1]})"

    text = re.sub(
        r"\[[^\]]+\]\(/posts/id(\d+)[^)]*\)",
        repl_main_broken,
        text,
    )

    if text != orig:
        path.write_text(text, encoding="utf-8")
    return n


def main() -> None:
    index = build_index()
    total = 0
    for path in sorted(POSTS.glob("2026-07-24-t*.md")):
        c = fix_file(path, index)
        if c:
            print(f"  {path.name}: {c} links")
            total += c
    print(f"Total: {total} links corrigidos em {len(list(POSTS.glob('2026-07-24-t*.md')))} capítulos")


if __name__ == "__main__":
    main()
