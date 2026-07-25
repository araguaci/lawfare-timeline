#!/usr/bin/env python3
"""Gera artigos em _posts/ a partir de _data/lawfare-timeline-124-145.json."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "_data" / "lawfare-timeline-124-145.json"
POSTS = ROOT / "_posts"

# Mapeamento categoria/subcategoria/tags -> pasta _posts (slug Jekyll categories)
def resolve_folder(item: dict) -> str:
    cat = (item.get("category") or "").lower()
    sub = (item.get("subcategory") or "").lower()
    title_l = (item.get("title") or "").lower()
    inst = " ".join(item.get("institutions") or []).lower()
    tags_l = " ".join(str(t) for t in (item.get("tags") or [])).lower()

    blob = f"{title_l} {inst} {tags_l}"

    # Sínteses de status não vão para STF só por citar o STF na lista de órgãos
    if cat in ("atualização_status", "atualizacao_status"):
        return "escandalos"

    if "stf" in blob or "toffoli" in blob or "supremo tribunal federal" in inst:
        return "stf"

    if cat == "ato_institucional":
        return "bancos"

    if cat == "operacao_policial":
        return "operacoes"

    if cat == "crime_financeiro":
        return "escandalos"

    if cat in ("revelação_investigativa", "revelacao_investigativa"):
        return "escandalos"

    if cat == "ato_legislativo":
        return "governo"

    if cat == "ato_normativo":
        return "governo"

    if cat == "ato_judicial":
        return "justica"

    if cat in ("falha_institucional", "análise_editorial", "analise_editorial"):
        return "escandalos"

    if cat == "dado_institucional":
        return "escandalos"

    if cat == "lacuna_investigativa":
        return "escandalos"

    if cat == "atualização_status" or cat == "atualizacao_status":
        return "escandalos"

    return "escandalos"


def image_for_folder(folder: str) -> str:
    return {
        "stf": "/assets/solid/balance-scale-left.svg",
        "bancos": "/assets/solid/landmark.svg",
        "operacoes": "/assets/solid/shield-halved.svg",
        "governo": "/assets/solid/landmark.svg",
        "justica": "/assets/solid/balance-scale-left.svg",
        "escandalos": "/assets/solid/exclamation-triangle.svg",
    }.get(folder, "/assets/solid/circle-exclamation.svg")


def emoji_for_folder(folder: str) -> str:
    return {
        "stf": "⚖️",
        "bancos": "🏦",
        "operacoes": "🚔",
        "governo": "🏛️",
        "justica": "⚖️",
        "escandalos": "⚠️",
    }.get(folder, "📌")


def slugify(title: str, max_len: int = 72) -> str:
    s = unicodedata.normalize("NFKD", title)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[—–]", "-", s)
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[-\s]+", "-", s).strip("-")
    return s[:max_len].rstrip("-")


def norm_tags(item: dict, folder: str) -> list[str]:
    raw = list(item.get("tags") or [])
    sub = (item.get("subcategory") or "").replace("_", "-")
    cat = (item.get("category") or "").replace("_", "-")
    out = [folder, cat, sub] if sub else [folder, cat]
    for t in raw:
        s = unicodedata.normalize("NFKD", str(t))
        s = "".join(c for c in s if not unicodedata.combining(c))
        s = re.sub(r"[^\w\-]", "", s.lower().replace("_", "-"))
        if s and s not in out:
            out.append(s)
    # dedupe preserve order
    seen = set()
    deduped = []
    for x in out:
        if x and x not in seen:
            seen.add(x)
            deduped.append(x)
    return deduped[:20]


def impacto_e_tipo(item: dict) -> tuple[str, str]:
    title_l = (item.get("title") or "").lower()
    tags = " ".join(str(t) for t in item.get("tags") or []).lower()
    if any(
        w in title_l or w in tags
        for w in ("eua", "houston", "internacional", "cop28", "multinacional", "faria lima", "boeing", "nestlé", "nestle")
    ):
        impacto = "Médio"
    else:
        impacto = "Baixo"

    sub = item.get("subcategory") or ""
    tipo_map = {
        "crime_ambiental": "Ambiental / organização criminosa",
        "crime_organizado": "Crime organizado / lavagem",
        "crime_financeiro": "Sistema financeiro",
        "denúncia_regulatória": "Regulatório / mercado de capitais",
        "sonegação_fiscal": "Tributário / lavagem",
        "fraude_financeira": "Fraude financeira",
        "lavagem_dinheiro": "Lavagem de dinheiro",
        "CPI": "Legislativo / CPI",
        "denúncia_criminal": "Judiciário / denúncia",
        "regulação_financeira": "Normativo tributário",
        "regulação_ambiental": "Legislativo ambiental",
        "indiciamento": "Judiciário / inquérito",
        "integridade_empresarial": "Compliance / dados",
        "dimensão_internacional": "Cooperação internacional",
        "padrão_transversal": "Análise comparativa",
        "status_investigativo": "Síntese investigativa",
    }
    tipo = tipo_map.get(sub, sub.replace("_", " ").title() or "Institucional")
    return impacto, tipo


def fmt_values(values: dict) -> str:
    if not values:
        return ""
    lines = []
    for k, v in values.items():
        key = str(k).replace("_", " ")
        lines.append(f"- **{key}**: {v}")
    return "\n".join(lines)


def render_actor_block(actors: list) -> str:
    if not actors:
        return ""
    lines = []
    for a in actors:
        name = a.get("name", "")
        role = a.get("role", "")
        org = a.get("organization", "")
        lines.append(f"- **{name}** ({role}) — {org}")
    return "\n".join(lines)


def render_sources(sources: list) -> str:
    out = []
    for s in sources or []:
        title = s.get("title", "Fonte")
        url = s.get("url", "#")
        outlet = s.get("outlet", "")
        if outlet:
            out.append(f"- [{outlet} — {title}]({url})")
        else:
            out.append(f"- [{title}]({url})")
    return "\n".join(out)


def legal_block(legal: list) -> str:
    if not legal:
        return "_Não listado no registro de origem._"
    return "\n".join(f"- {x}" for x in legal)


def build_markdown(item: dict) -> tuple[str, Path]:
    folder = resolve_folder(item)
    tid = item.get("id")
    date_str = item.get("date") or "1970-01-01"
    # Jekyll date
    iso = f"{date_str}T12:00:00.000Z" if len(date_str) == 10 else date_str

    title = item.get("title", "Sem título").strip()
    summary = (item.get("summary") or "").strip()
    desc = summary[:220] + ("…" if len(summary) > 220 else "")
    slug = slugify(title)
    fname = f"{date_str}-timeline-{tid}-{slug}.md"
    path = POSTS / folder / fname

    impacto, tipo_esc = impacto_e_tipo(item)
    em = emoji_for_folder(folder)
    img = image_for_folder(folder)
    tags = norm_tags(item, folder)

    # YAML tags single-line style
    tags_yaml = "[" + ", ".join(repr(t) for t in tags) + "]"

    values_md = fmt_values(item.get("values") or {})
    actors_md = render_actor_block(item.get("actors") or [])
    insts = item.get("institutions") or []
    inst_md = "\n".join(f"- {x}" for x in insts) if insts else "_—_"
    notes = (item.get("notes") or "").strip()
    status = item.get("status") or ""

    if notes and len(summary) < 350:
        intro = f"{summary}\n\n{notes[:900]}"
    else:
        intro = summary

    conclusao = (
        notes[:1200]
        if notes
        else f"O registro timeline **#{tid}** documenta o evento no arc Greenwashing, Carbono Oculto e Compliance Zero."
    )

    body = f"""---
title: {json.dumps(title, ensure_ascii=False)}
description: {json.dumps(desc, ensure_ascii=False)}
date: {iso}
image:
  path: "{img}"
tags: {tags_yaml}
categories: {folder}
timeline_id: {tid}
source_data: lawfare-timeline-124-145.json
---

- &nbsp;
{{:toc .large-only}}

# {em} {title}

***

## 🧭 Resumo

{summary}

**Impacto Diplomático:** {impacto}  
**Tipo de Escândalo:** {tipo_esc}

***

## 🏁 Introdução

{intro}

## 📊 Análise

### Contexto e status

- **ID timeline:** {tid}
- **Precisão da data:** {item.get("date_precision", "—")}
- **Status (registro):** {status or "—"}

### Atores

{actors_md or "_Nenhum ator nomeado no registro._"}

### Instituições

{inst_md}

### Valores e quantitativos

{values_md or "_—_"}

### Base legal (referência)

{legal_block(item.get("legal_basis") or [])}

### Conexões

{", ".join(str(c) for c in (item.get("connections") or [])) or "—"}

## 🎯 Conclusão

{conclusao}

## Referências

{render_sources(item.get("sources") or [])}
"""
    return body, path


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    POSTS.mkdir(parents=True, exist_ok=True)
    written = []
    for item in data:
        md, path = build_markdown(item)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(md, encoding="utf-8")
        written.append(path.relative_to(ROOT))
    print(f"Escritos {len(written)} artigos em _posts/")
    for p in sorted(written):
        print(f"  {p}")


if __name__ == "__main__":
    main()
