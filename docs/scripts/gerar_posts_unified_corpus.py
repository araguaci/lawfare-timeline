#!/usr/bin/env python3
"""
Gera posts Jekyll em _posts/<categoria>/ a partir de _data/lawfare-unified-corpus.json
Respeita jekyll_filename, conexões por id_corpus, links P01–P12 e artigos_gosurf.

Uso:
  python scripts/gerar_posts_unified_corpus.py           # só arquivos ausentes
  python scripts/gerar_posts_unified_corpus.py --force  # sobrescreve tudo
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS_PATH = ROOT / "_data" / "lawfare-unified-corpus.json"
POSTS_DIR = ROOT / "_posts"

PADROES_ARTIGO_TIMELINE = "/posts/padroes-sistemicos/"
PADROES_URL_TIMELINE_ABS = "https://lawfare-timeline.vercel.app/posts/padroes-sistemicos/"
PADROES_URL_DASHBOARD = "https://gosurf.site/padroes-sistemicos-dashboard"

# Ícone base por pasta Jekyll (temas Chirpy / assets/solid)
IMAGE_BY_CATEGORY: dict[str, str] = {
    "lawfare": "/assets/solid/weight-scale.svg",
    "stf": "/assets/solid/gavel.svg",
    "escandalos": "/assets/solid/skull.svg",
    "estudos": "/assets/solid/book.svg",
    "operacoes": "/assets/solid/bullseye.svg",
    "justica": "/assets/solid/hammer.svg",
    "impunidade": "/assets/solid/lock-open.svg",
    "bancos": "/assets/solid/landmark.svg",
    "crise-diplomatica": "/assets/solid/globe.svg",
    "vazatoga": "/assets/solid/user-secret.svg",
    "dossie": "/assets/solid/file-alt.svg",
    "indecoro": "/assets/solid/exclamation-triangle.svg",
    "tse": "/assets/solid/check-to-slot.svg",
    "penduricalhos": "/assets/solid/dollar-sign.svg",
    "extravagancia": "/assets/solid/gem.svg",
    "decano": "/assets/solid/user-tie.svg",
    "governo": "/assets/solid/sitemap.svg",
}

# Sobrescreve por tag (primeira correspondência)
TAG_IMAGE_RULES: list[tuple[str, str]] = [
    ("narco-fluxo", "/assets/solid/pills.svg"),
    ("choquei", "/assets/solid/bullhorn.svg"),
    ("funk", "/assets/solid/music.svg"),
    ("cultura-massa", "/assets/solid/music.svg"),
    ("carbono-oculto", "/assets/solid/leaf.svg"),
    ("fintech", "/assets/solid/credit-card.svg"),
    ("fintechs", "/assets/solid/credit-card.svg"),
    ("lavagem-dinheiro", "/assets/solid/dollar-sign.svg"),
    ("lavagem-de-dinheiro", "/assets/solid/dollar-sign.svg"),
    ("ofac", "/assets/solid/flag-usa.svg"),
    ("portugal", "/assets/solid/globe.svg"),
    ("europa", "/assets/solid/globe.svg"),
    ("wall-street-journal", "/assets/solid/newspaper.svg"),
    ("wsj", "/assets/solid/newspaper.svg"),
    ("yakuza", "/assets/solid/dragon.svg"),
    ("ndrangheta", "/assets/solid/flag.svg"),
    ("mafia-italiana", "/assets/solid/flag.svg"),
    ("hezbollah", "/assets/solid/star-and-crescent.svg"),
    ("tri-fronteira", "/assets/solid/map-location-dot.svg"),
    ("pcc", "/assets/solid/users.svg"),
    ("prisao-preventiva-indevida", "/assets/solid/handcuffs.svg"),
    ("erro-judiciario", "/assets/solid/triangle-exclamation.svg"),
]


def _yaml_escape(s: str) -> str:
    if not s:
        return ""
    return s.replace('"', '\\"')


def pick_image(category: str, tags: list[str]) -> str:
    tl = [t.lower() for t in tags]
    for key, path in TAG_IMAGE_RULES:
        if any(key in t for t in tl):
            p = ROOT / "assets" / "solid" / path.split("/")[-1]
            if p.is_file():
                return path
    base = IMAGE_BY_CATEGORY.get(category, "/assets/solid/circle-exclamation.svg")
    check = ROOT / "assets" / "solid" / base.split("/")[-1]
    if check.is_file():
        return base
    return "/assets/solid/circle-exclamation.svg"


def slug_from_jekyll_filename(jekyll_filename: str) -> str:
    stem = Path(jekyll_filename).stem
    m = re.match(r"^\d{4}-\d{2}-\d{2}-(.+)$", stem)
    return m.group(1) if m else stem


def post_url_from_filename(jekyll_filename: str) -> str:
    return f"/posts/{slug_from_jekyll_filename(jekyll_filename)}/"


def normalize_conn(raw: str) -> str | None:
    s = raw.strip()
    m = re.match(r"id[_]?(\d+)$", s, re.I)
    return m.group(1) if m else None


def format_iso_date(date_str: str) -> str:
    d = (date_str or "2026-01-01")[:10]
    return f"{d}T12:00:00.000Z"


def build_connection_lines(
    conexoes: list[str],
    by_id: dict[str, dict],
) -> str:
    if not conexoes:
        return ""
    lines = ["## 🔗 Registros relacionados", ""]
    for c in conexoes:
        nid = normalize_conn(c)
        if not nid:
            lines.append(f"- Referência: `{c}`")
            continue
        other = by_id.get(nid)
        if not other:
            lines.append(
                f"- ID de corpus **{nid}** — entrada não listada neste corpus unificado (ver [linha do tempo](/))."
            )
            continue
        title = other.get("titulo", nid)
        oname = other.get("jekyll_filename") or ""
        perm = post_url_from_filename(oname) if oname else "#"
        lines.append(f"- [{title}]({perm}) (`id_corpus` {nid})")
    lines.append("")
    return "\n".join(lines)


def padroes_section(padroes: list[str], defs: dict[str, str]) -> str:
    intro = (
        f"Os códigos **P01** a **P12** seguem o glossário do corpus unificado. "
        f"Síntese editorial: [Matriz de indulgência sistêmica]({PADROES_ARTIGO_TIMELINE}) "
        f"(mirror: [{PADROES_URL_TIMELINE_ABS}]({PADROES_URL_TIMELINE_ABS})); "
        f"painel interativo: [{PADROES_URL_DASHBOARD}]({PADROES_URL_DASHBOARD}).\n"
    )
    if not padroes:
        return (
            "## 📐 Padrões sistêmicos (P01–P12)\n\n"
            + intro
            + "\n*Neste registro não há códigos P01–P12 associados.*\n\n"
        )
    rows = [intro, "", "| Código | Descrição (corpus) |", "| --- | --- |"]
    for p in sorted(set(padroes), key=lambda x: int(x[1:]) if len(x) > 1 and x[1:].isdigit() else x):
        label = defs.get(p, "—")
        link_p = (
            f"[{p}]({PADROES_URL_TIMELINE_ABS}) · "
            f"[dashboard]({PADROES_URL_DASHBOARD})"
        )
        rows.append(f"| {link_p} | {label} |")
    rows.append("")
    rows.append(
        f"*Referência cruzada:* [artigo na timeline]({PADROES_ARTIGO_TIMELINE}) · "
        f"[dashboard Gosurf]({PADROES_URL_DASHBOARD})\n"
    )
    return "## 📐 Padrões sistêmicos (P01–P12)\n\n" + "\n".join(rows) + "\n"


def gosurf_section(items: list[dict]) -> str:
    if not items:
        return ""
    lines = ["## 📎 Artigos de apoio (Gosurf)", ""]
    for it in items:
        url = it.get("url") or ""
        slug = it.get("slug") or ""
        tit = slug.replace("-", " ").title() if slug else url
        if url:
            lines.append(f"- [{tit}]({url}) (`{slug}`)")
    lines.append("")
    return "\n".join(lines)


def fontes_section(fontes: list[dict]) -> str:
    lines = ["## 📚 Fontes verificáveis", ""]
    for i, f in enumerate(fontes, 1):
        url = f.get("url", "")
        tit = f.get("titulo") or "Fonte"
        veic = f.get("veiculo", "")
        data = f.get("data", "")
        meta = " — ".join(x for x in [veic, data] if x)
        if url:
            lines.append(f"{i}. [{tit}]({url}){(' — ' + meta) if meta else ''}")
        else:
            lines.append(f"{i}. {tit}{(' — ' + meta) if meta else ''}")
    lines.append("")
    return "\n".join(lines)


def render_post(entry: dict, by_id: dict[str, dict], defs: dict[str, str], jekyll_filename: str) -> str:
    cats = entry.get("jekyll_categories") or ["lawfare"]
    category = cats[0] if isinstance(cats, list) else str(cats)
    tags = entry.get("jekyll_tags") or []
    title = entry.get("titulo", "Sem título")
    resumo = entry.get("resumo", "")
    desc = _yaml_escape((resumo[:157] + "…") if len(resumo) > 157 else resumo)

    image_path = pick_image(category, tags)
    date_iso = format_iso_date(entry.get("jekyll_date") or entry.get("data", ""))
    post_perm = post_url_from_filename(jekyll_filename)

    fm_tags = json.dumps(tags, ensure_ascii=False)

    body_parts = [
        "- &nbsp;",
        "{:toc .large-only}",
        "",
        f"# {title}",
        "",
        "***",
        "",
        "## 🧭 Resumo",
        "",
        resumo,
        "",
        "***",
        "",
        "## 🏷️ Metadados do corpus",
        "",
        f"| Campo | Valor |",
        f"| --- | --- |",
        f"| `id_corpus` | **{entry.get('id_corpus', '')}** |",
        f"| Categoria analítica | {entry.get('categoria', '—')} |",
        f"| País / âmbito | {entry.get('pais', '—')} |",
        f"| Dimensão global | {'sim' if entry.get('dimensao_global') else 'não'} |",
        "",
    ]
    if entry.get("conflito_nota"):
        body_parts.extend(["> **Nota de conflito ID:** " + entry["conflito_nota"], ""])

    atores = entry.get("atores") or []
    inst = entry.get("instituicoes") or []
    if atores:
        body_parts.extend(["### Atores", "", *[f"- {a}" for a in atores], ""])
    if inst:
        body_parts.extend(["### Instituições", "", *[f"- {i}" for i in inst], ""])

    body_parts.append(
        padroes_section(entry.get("padroes") or [], defs)
    )
    body_parts.append(
        build_connection_lines(entry.get("conexoes") or [], by_id)
    )
    body_parts.append(
        gosurf_section(entry.get("artigos_gosurf") or [])
    )
    body_parts.append(
        fontes_section(entry.get("fontes_verificadas") or [])
    )

    frontmatter = f"""---
title: "{_yaml_escape(title)}"
description: "{desc}"
date: {date_iso}
image:
  path: "{image_path}"
tags: {fm_tags}
categories: {category}
permalink: {post_perm}
id_corpus: "{entry.get('id_corpus', '')}"
corpus_unificado: true
---

"""
    return frontmatter + "\n".join(body_parts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="Sobrescreve arquivos existentes")
    args = ap.parse_args()

    if not CORPUS_PATH.is_file():
        print(f"Arquivo não encontrado: {CORPUS_PATH}", file=sys.stderr)
        return 1

    data = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    entries: list[dict] = data.get("entradas") or []
    defs: dict[str, str] = data.get("padroes_referencia") or {}

    by_id: dict[str, dict] = {}
    for e in entries:
        k = str(e.get("id_corpus", ""))
        if k:
            by_id[k] = e

    written = 0
    skipped = 0
    for entry in entries:
        cats = entry.get("jekyll_categories") or ["lawfare"]
        category = cats[0] if isinstance(cats, list) else str(cats)
        fname = entry.get("jekyll_filename")
        if not fname:
            print(f"Pulando entrada sem jekyll_filename: {entry.get('id_corpus')}", file=sys.stderr)
            skipped += 1
            continue

        target_dir = POSTS_DIR / category
        target_dir.mkdir(parents=True, exist_ok=True)
        path = target_dir / fname

        if path.is_file() and not args.force:
            skipped += 1
            continue

        path.write_text(render_post(entry, by_id, defs, fname), encoding="utf-8")
        written += 1
        print(path.relative_to(ROOT))

    print(f"Gerados: {written}; ignorados (já existentes ou erro): {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
