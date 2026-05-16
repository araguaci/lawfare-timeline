#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert _posts/estudos/*-xarticle.md to Jekyll posts with Chirpy-style frontmatter."""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
from pathlib import Path

GOSURF = Path(r"D:\ai-projects\gosurf.site").resolve()
DEPLOY = Path(r"D:\_deploy\lawfare-timeline").resolve()
POSTS_ESTUDOS = DEPLOY / "_posts" / "estudos"
PAGES_JSON = GOSURF / "pages.json"
SRC_IMG = GOSURF / "assets" / "img"
DST_IMG = DEPLOY / "assets" / "img"


def norm_slug_from_filename(name: str) -> str:
    base = re.sub(r"-xarticle\.md$", "", name, flags=re.I)
    return base.replace("_", "-")


def load_pages_index() -> dict[str, dict]:
    data = json.loads(PAGES_JSON.read_text(encoding="utf-8"))
    return {p["slug"]: p for p in data if "slug" in p}


def strip_first_h1(md: str) -> str:
    lines = md.splitlines()
    if lines and lines[0].startswith("# "):
        return "\n".join(lines[1:]).lstrip("\n")
    return md


def first_h1(md: str) -> str | None:
    for line in md.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def yaml_escape_desc(s: str) -> str:
    s = s.strip().replace("\n", " ")
    if not s:
        return '""'
    if any(c in s for c in ':"\'') or s.endswith(":"):
        return json.dumps(s, ensure_ascii=False)
    return s


def rewrite_body(md: str, copied_basenames: set[str]) -> str:
    # gosurf: drop .html from paths
    md = re.sub(
        r"https://gosurf\.site/([a-zA-Z0-9_./-]+)\.html",
        r"https://gosurf.site/\1",
        md,
    )
    # relative assets/img/foo -> /assets/img/foo (deploy)
    def repl_assets(m: re.Match) -> str:
        path = m.group(1).lstrip("/")
        if path.startswith("assets/img/"):
            copied_basenames.add(Path(path).name)
        return "](/assets/img/" + path.split("assets/img/", 1)[-1] + ")"

    md = re.sub(r"\]\((assets/img/[^)]+)\)", repl_assets, md)
    md = re.sub(r"\]\((/assets/img/[^)]+)\)", lambda m: m.group(0), md)
    # bare ](foo.png) in same folder — already handled if path has assets/img
    md = re.sub(
        r"\]\((?!https?://)([a-zA-Z0-9_.-]+\.(?:png|jpe?g|gif|webp))\)",
        r"](/assets/img/\1)",
        md,
    )
    for m in re.finditer(r"\]\(/assets/img/([^)]+)\)", md):
        copied_basenames.add(m.group(1))
    return md


def list_img_files() -> list[Path]:
    if not SRC_IMG.is_dir():
        return []
    return [p for p in SRC_IMG.iterdir() if p.suffix.lower() == ".png"]


def resolve_local_image_ref(ref: str, files: list[Path]) -> Path | None:
    name = Path(ref).name
    direct = SRC_IMG / name
    if direct.is_file():
        return direct
    stem = Path(name).stem
    candidates = [p for p in files if p.stem == stem or p.name == name]
    if len(candidates) == 1:
        return candidates[0]
        if stem:
            pref = [p for p in files if p.name.startswith(stem)]
            if pref:
                pref.sort(
                    key=lambda p: (
                        "_hero_xarticle" in p.name,
                        " copia" not in p.name.lower(),
                        -len(p.name),
                    ),
                    reverse=True,
                )
                return pref[0]
    return None


def find_hero_path(slug: str, body: str, files: list[Path]) -> Path | None:
    for m in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", body):
        ref = m.group(1).strip()
        if ref.startswith("http"):
            continue
        hit = resolve_local_image_ref(ref, files)
        if hit:
            return hit

    u = slug.replace("-", "_")
    for name in (
        f"{u}_hero_xarticle.png",
        f"{u}_hero.png",
        f"{u.replace('_', '-')}-xarticle-hero.png",
        f"{slug}-xarticle-hero.png",
    ):
        p = SRC_IMG / name
        if p.is_file():
            return p

    og = GOSURF / f"og-{slug}.png"
    if og.is_file():
        return og

    scored: list[tuple[int, Path]] = []
    parts = [x for x in slug.split("-") if len(x) > 2]
    slug_underscore = slug.replace("-", "_")
    for p in files:
        pl = p.name.lower()
        score = 0
        if slug_underscore in pl:
            score += 80
        elif parts and all(part.lower() in pl for part in parts):
            score += 40 + len(parts) * 2
        elif parts:
            hit = sum(1 for part in parts if part.lower() in pl)
            if hit:
                score += 10 + hit * 8
        if score > 0 and ("hero" in pl or pl.startswith("og-") or "_hero" in pl):
            score += 4
        if score > 0:
            scored.append((score, p))
    if scored:
        scored.sort(key=lambda x: -x[0])
        return scored[0][1]

    return None


def tags_yaml(tags: list) -> str:
    out = []
    for t in tags:
        out.append(json.dumps(str(t), ensure_ascii=False))
    return "[" + ", ".join(out) + "]"


def main() -> int:
    if not GOSURF.is_dir() or not DEPLOY.is_dir():
        print("Paths missing", file=sys.stderr)
        return 1

    DST_IMG.mkdir(parents=True, exist_ok=True)
    pages = load_pages_index()
    files = list_img_files()
    copied: set[str] = set()

    def copy_one(src: Path | None) -> str | None:
        if src is None or not src.is_file():
            return None
        dst = DST_IMG / src.name
        if not dst.exists() or dst.stat().st_size != src.stat().st_size:
            shutil.copy2(src, dst)
        copied.add(src.name)
        return f"/assets/img/{src.name}"

    xarticles = sorted(POSTS_ESTUDOS.glob("*-xarticle.md"))
    if not xarticles:
        print("No *-xarticle.md under", POSTS_ESTUDOS)
        return 0

    for src_path in xarticles:
        raw = src_path.read_text(encoding="utf-8")
        slug = norm_slug_from_filename(src_path.name)
        meta = pages.get(slug, {})
        title = meta.get("title") or first_h1(raw) or slug
        _desc_fallback = ""
        for line in raw.splitlines()[1:]:
            t = line.strip()
            if t and not t.startswith("#") and not t.startswith("!["):
                _desc_fallback = t[:280]
                break
        desc = meta.get("description") or _desc_fallback or title
        date_str = meta.get("date") or "2026-05-01"
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str):
            date_iso = f"{date_str}T12:00:00-03:00"
        else:
            date_iso = date_str

        tag_list = meta.get("tags") or ["estudos", "lawfare", "brasil"]
        hero_src = find_hero_path(slug, raw, files)
        body_for_md = strip_first_h1(raw)
        refs: set[str] = set()
        body_for_md = rewrite_body(body_for_md, refs)

        image_path = copy_one(hero_src)
        if image_path is None:
            image_path = copy_one(SRC_IMG / "lawfare_timeline_hero_xarticle.png")

        for base in list(refs):
            hit = resolve_local_image_ref(base, files)
            if hit:
                copy_one(hit)
        for m in re.finditer(r"/assets/img/([^)\s\"']+)", body_for_md):
            hit = resolve_local_image_ref(m.group(1), files)
            if hit:
                copy_one(hit)

        fm = f"""---
title: {json.dumps(str(title), ensure_ascii=False)}
description: {yaml_escape_desc(str(desc))}
date: {date_iso}
image:
  path: {json.dumps(image_path or "/assets/img/lawfare_timeline_hero_xarticle.png")}
tags: {tags_yaml(tag_list)}
categories: estudos
mermaid: false
pin: false
---

- &nbsp;
{{:toc .large-only}}

{body_for_md}
"""
        out_name = f"{date_str}-{slug}.md"
        out_path = POSTS_ESTUDOS / out_name
        out_path.write_text(fm.rstrip() + "\n", encoding="utf-8")
        old_name = src_path.name
        src_path.unlink()
        print("OK", out_path.name, "<-", old_name, "img:", image_path)

    print("Copied", len(copied), "unique images to", DST_IMG)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
