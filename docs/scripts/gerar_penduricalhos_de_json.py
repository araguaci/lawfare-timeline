#!/usr/bin/env python3
"""Gera posts Jekyll e entradas lawfare.json a partir de tools/penduricalhos-*.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "tools" / "penduricalhos-novos-eventos-2025-07-02-2026-05-11.json"
LAWFARE_PATH = ROOT / "_data" / "lawfare.json"
START_ID = 1437


def format_tags(tags: list) -> str:
    out = []
    seen = set()
    for t in tags[:10]:
        t = str(t).strip().lower()
        if not t or t in seen:
            continue
        seen.add(t)
        # aspas se houver espaço ou hífen em compostos longos
        if " " in t:
            out.append(f"'{t}'")
        else:
            out.append(t)
    return "[" + ", ".join(out) + "]"


def yaml_escape_title(title: str) -> str:
    return title.replace('"', '\\"')


def perplexity_url(title: str, desc: str, data_ev: str, beneficiado: str) -> str:
    q = f'"penduricalhos judiciais Brasil" {title} {desc} {data_ev} {beneficiado}'
    return "https://www.perplexity.ai/search?q=" + quote(q, safe="")


def google_url(title: str, desc: str, data_ev: str, beneficiado: str) -> str:
    q = f'"penduricalhos judiciais Brasil" {title} {desc} {data_ev} {beneficiado}'
    return "https://www.google.com/search?q=" + quote(q, safe="")


def wiki_url(title: str, desc: str, data_ev: str, beneficiado: str) -> str:
    q = f'"penduricalhos judiciais Brasil" {title} {desc} {data_ev} {beneficiado}'
    return "https://pt.wikipedia.org/w/index.php?search=" + quote(q, safe="")


def build_markdown(assunto: dict) -> str:
    art = assunto["artigo"]
    fm = art["front_matter"]
    corpo = art["corpo"]
    det = corpo["detalhes"]
    title = fm["title"]
    desc = fm["description"].strip()
    if len(desc) > 160:
        desc = desc[:157] + "..."
    tags_str = format_tags(fm.get("tags", []))

    fontes_block = "\n".join(
        "  - " + line for line in corpo.get("fontes_formatadas", []) if line
    )

    pu = perplexity_url(
        title, assunto.get("descricao", ""), det.get("data", ""), det.get("beneficiado", "")
    )
    yt = yaml_escape_title(title)

    return f"""---
layout: post
title: "{yt}"
categories: penduricalhos
image:
  path: "{fm.get("image_path", "/assets/solid/gift.svg")}"
article_id: {fm["article_id"]}
description: >
  {desc}
tags: {tags_str}
---

# {corpo["heading"]}

## Detalhes
- **Ano**: {det.get("ano", "")}
- **Data**: {det.get("data", "")}
- **Descrição**: <i class="fas fa-money-bill-wave"></i> *{det.get("descricao", "")}*{{: style="color: red;"}}
- **Decisão**: {det.get("decisao", "")}
- **Juiz**: 
- **Beneficiado**: {det.get("beneficiado", "")}
- **Departamento**: {det.get("departamento", "")}
- **Local**: {det.get("local", "")}
- **Valor**: {det.get("valor", "N/A")}
- **Envolvidos**:
{chr(10).join("  - " + e for e in corpo.get("envolvidos", []) if e)}
- **Consequências**:
{chr(10).join("  - " + c for c in corpo.get("consequencias", []) if c)}
- **Categorias**:
{chr(10).join("  - " + s for s in corpo.get("subcategorias", []) if s)}
- **Corpo**: {det.get("descricao", "")}
- **Fontes**:
{fontes_block}

## Contraste constitucional

{corpo.get("contraste_constitucional", "")}

## Contraste social

{corpo.get("contraste_social", "")}

## Analise por IA
- [🤖 Investigar com IA]({pu})

## Links Relacionados
- [🌐🔍 Busca no Google para o título e descrição]({google_url(title, assunto.get("descricao", ""), det.get("data", ""), det.get("beneficiado", ""))})
- [📖🔍 Busca na Wikipedia para o título e descrição]({wiki_url(title, assunto.get("descricao", ""), det.get("data", ""), det.get("beneficiado", ""))})
"""


def lawfare_entry(assunto: dict, id_: int) -> dict:
    tags = list(assunto.get("tags") or [])
    if "penduricalhos" not in tags:
        tags = ["penduricalhos"] + tags
    path = assunto["fonte_arquivo"].replace("/", "\\")
    d = {k: v for k, v in assunto.items() if k != "artigo" and k != "id"}
    d["tags"] = tags[:15]
    d["fonte_arquivo"] = path
    d["id"] = id_
    return d


def main() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assuntos = data["assuntos"]

    for i, a in enumerate(assuntos):
        rel = a["fonte_arquivo"]
        out_path = ROOT / rel
        md = build_markdown(a)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(md, encoding="utf-8", newline="\n")
        print("Wrote", out_path.relative_to(ROOT))

    lw = json.loads(LAWFARE_PATH.read_text(encoding="utf-8"))
    if lw["assuntos"][-1]["id"] != START_ID - 1:
        print(
            "Warning: esperado último id",
            START_ID - 1,
            "encontrado",
            lw["assuntos"][-1]["id"],
            file=sys.stderr,
        )
    for i, a in enumerate(assuntos):
        lw["assuntos"].append(lawfare_entry(a, START_ID + i))

    lw["total"] = lw["assuntos"][-1]["id"]
    lw["data_extração"] = "2026-05-11"
    lw["periodo"] = "1855-01-01 a 2026-05-11"
    lw["nota"] = (
        "Extraído/atualizado: inclusão de 12 entradas categoria penduricalhos "
        "(2025-12 a 2026-05) via scripts/gerar_penduricalhos_de_json.py a partir de "
        "tools/penduricalhos-novos-eventos-2025-07-02-2026-05-11.json; IDs 1437–1448."
    )

    LAWFARE_PATH.write_text(
        json.dumps(lw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print("Updated lawfare.json total=", lw["total"])


if __name__ == "__main__":
    main()
