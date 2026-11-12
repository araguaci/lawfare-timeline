#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sincroniza _data/todo/*.json pendentes com artigos Jekyll e corpus.

Detecta automaticamente:
  - Arquivos T-NNN*.json ou tipo analise_estrutural -> estudos (thematic track)
  - Demais JSON com id numerico -> posts timeline (main track)

Uso:
  python scripts/sync_todo_current.py
  python scripts/sync_todo_current.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "scripts"))
from corpus_links import (
    build_corpus_index,
    build_thematic_index,
    fix_conexoes_section,
    format_connection,
)
from gdrive_sync_export import export_sync_to_gdrive
TODO = ROOT / "_data" / "todo"
PROC = ROOT / "_data" / "processados"
POSTS = ROOT / "_posts"
LAWFARE = ROOT / "_data" / "lawfare.json"
UNIFIED = ROOT / "_data" / "lawfare-unified-corpus.json"
SYNC = ROOT / "_data" / "claude.ai-corpus-ids-sync.json"

IMAGE_BY_CATEGORY = {
    "operacoes": "/assets/solid/bullseye.svg",
    "escandalos": "/assets/solid/skull.svg",
    "stf": "/assets/solid/gavel.svg",
    "justica": "/assets/solid/hammer.svg",
    "impunidade": "/assets/solid/scale-balanced.svg",
    "bancos": "/assets/solid/landmark.svg",
    "lawfare": "/assets/solid/weight-scale.svg",
    "crise-diplomatica": "/assets/solid/globe.svg",
    "vazatoga": "/assets/solid/shield-virus.svg",
    "tse": "/assets/solid/gavel.svg",
}


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")[:90]


def yaml_escape(s: str) -> str:
    return s.replace('"', '\\"').replace("\n", " ")


def format_iso(d: str) -> str:
    return f"{(d or '2026-01-01')[:10]}T12:00:00.000Z"


def thematic_id_from_file(path: Path, data: dict) -> int | None:
    if not isinstance(data, dict):
        return None
    m = re.match(r"^lawfare-thematic-T(\d+)", path.stem, re.I)
    if m:
        return int(m.group(1))
    eid = data.get("id")
    tipo = (data.get("tipo") or "").lower()
    if tipo in ("analise_estrutural", "lacuna_investigativa") and isinstance(eid, int) and eid >= 100:
        return eid
    return None


def thematic_id_from_entry(entry: dict) -> int | None:
    eid = entry.get("id")
    if eid is None:
        eid = entry.get("id_corpus")
    if eid is None:
        return None
    if isinstance(eid, str):
        m = re.match(r"^T-(\d+)$", eid.strip(), re.I)
        if m:
            return int(m.group(1))
    tipo = (
        entry.get("tipo")
        or entry.get("category")
        or entry.get("categoria")
        or ""
    ).lower()
    if tipo in ("analise_estrutural", "lacuna_investigativa", "analise_editorial"):
        if isinstance(eid, int):
            # IDs main track (>=1000) nunca viram T-NNN automático
            if eid >= 1000:
                return None
            if eid >= 100:
                return eid
    return None


def parse_main_id(eid) -> int | None:
    if isinstance(eid, int):
        return eid
    if isinstance(eid, str):
        if re.match(r"^T-\d+$", eid.strip(), re.I):
            return None
        if "PENDENTE" in eid.upper():
            return None
        try:
            return int(eid)
        except ValueError:
            return None
    return None


def normalize_date(d: str) -> str:
    raw = (d or "").strip()
    if re.fullmatch(r"\d{4}-\d{2}$", raw):
        return raw + "-01"
    if re.fullmatch(r"\d{4}$", raw):
        return raw + "-01-01"
    return raw[:10] if raw else "2026-01-01"


def resolve_category(entry: dict) -> str:
    override = entry.get("jekyll_category") or entry.get("jekyll_categories")
    if isinstance(override, list) and override:
        return str(override[0]).strip().lower()
    if isinstance(override, str) and override.strip():
        return override.strip().lower()
    cat = (entry.get("category") or entry.get("categoria") or entry.get("tipo") or "").lower()
    title = (entry.get("title") or entry.get("titulo") or "").lower()
    tags = [str(t).lower() for t in entry.get("tags") or entry.get("padroes_ativados") or []]

    mapping = {
        "operacao_policial": "operacoes",
        "operacao": "operacoes",
        "operacoes": "operacoes",
        "perseguicao_processual": "stf",
        "perseguicao-institucional": "stf",
        "mecanismo_sistemico": "bancos",
        "incidente_diplomatico": "crise-diplomatica",
        "judicial": "justica",
        "crise-diplomatica": "crise-diplomatica",
        "censura-digital": "lawfare",
        "impunidade": "impunidade",
        "abuso_processual": "impunidade",
        "erro-judiciario": "impunidade",
        "chokepoint_judicial": "stf",
        "ato_legislativo": "lawfare",
        "lacuna_investigativa": "justica",
        "analise_editorial": "estudos",
        "vazatoga": "vazatoga",
        "tse": "tse",
        "stf": "stf",
        "escandalos": "escandalos",
        "congresso": "escandalos",
        "bancos": "bancos",
    }
    if cat in mapping:
        return mapping[cat]
    if "operacao" in cat or "operacao" in tags:
        return "operacoes"
    if "moraes" in title or "stf" in title or "calunia" in title:
        return "stf"
    lawfare_kw = (
        "fake news",
        "pl 2630",
        "marco civil",
        "eca digital",
        "lei 15.211",
        "anpd",
    )
    if any(k in title for k in lawfare_kw):
        return "lawfare"
    if "pcc" in title or "cv" in title or "garimpo" in title:
        return "operacoes"
    if "master" in title or "vorcaro" in title:
        return "bancos"
    return "escandalos"


def build_tags(entry: dict, category: str) -> list[str]:
    tags: list[str] = []
    for src in (entry.get("padroes_ativados"), entry.get("patterns"), entry.get("tags")):
        if src:
            tags.extend(str(x).lower() for x in src)
    if entry.get("slug"):
        tags.append(entry["slug"][:40])
    if category not in tags:
        tags.insert(0, category)
    return list(dict.fromkeys(tags))[:10]


def parse_actors(raw_actors) -> list[str]:
    out: list[str] = []
    for a in raw_actors or []:
        if isinstance(a, dict):
            n = a.get("name") or a.get("nome", "")
            r = a.get("role") or a.get("papel", "")
            out.append(f"{n} ({r})" if r else n)
        else:
            out.append(str(a))
    return out


def parse_fontes(entry: dict) -> list[dict]:
    fontes: list[dict] = []
    ev = entry.get("evidencia_primaria") or {}
    if ev.get("url_referencia"):
        for url in str(ev["url_referencia"]).split(";"):
            url = url.strip()
            if url:
                fontes.append({"titulo": ev.get("fonte", "Fonte"), "url": url})
    for s in entry.get("sources") or entry.get("fontes") or []:
        if isinstance(s, dict):
            fontes.append({
                "titulo": s.get("title") or s.get("titulo") or s.get("name") or s.get("outlet") or "Fonte",
                "url": s.get("url") or "",
            })
        elif isinstance(s, str) and s.startswith("http"):
            fontes.append({"titulo": "Fonte", "url": s})
    return fontes


def occupied_main_ids() -> set[int]:
    if not LAWFARE.is_file():
        return set()
    data = json.loads(LAWFARE.read_text(encoding="utf-8"))
    return {int(a["id"]) for a in data.get("assuntos") or [] if isinstance(a.get("id"), int)}


def occupied_thematic_ids() -> set[int]:
    taken: set[int] = set()
    if SYNC.is_file():
        sync = json.loads(SYNC.read_text(encoding="utf-8"))
        for e in sync.get("tracks", {}).get("thematic", {}).get("entries") or []:
            if isinstance(e.get("id"), int):
                taken.add(int(e["id"]))
    for p in (POSTS / "estudos").glob("*.md"):
        text = p.read_text(encoding="utf-8", errors="replace")
        m = re.search(r'^id_corpus:\s*["\']?T-(\d+)["\']?\s*$', text, re.M)
        if m:
            taken.add(int(m.group(1)))
    return taken


def allocate_id(requested: int, taken: set[int]) -> tuple[int, int | None]:
    """Devolve (id_final, id_antigo) sem reutilizar ocupados. id_antigo só vem preenchido se houve realocação."""
    if requested not in taken:
        taken.add(requested)
        return requested, None
    nxt = requested + 1
    while nxt in taken:
        nxt += 1
    taken.add(nxt)
    return nxt, requested


REF_KEYS = (
    "connections",
    "lacuna_investigativa",
    "analise",
    "summary",
    "descricao",
    "resumo",
    "result",
    "ponto_de_inflexao",
    "evidence_note",
    "title",
    "titulo",
)


def remap_id_refs(value, id_map: dict[int, int]):
    if not id_map:
        return value

    def repl(m: re.Match) -> str:
        old = int(m.group(1))
        return f"id_{id_map.get(old, old)}"

    if isinstance(value, str):
        return re.sub(r"id_(\d+)", repl, value)
    if isinstance(value, list):
        return [remap_id_refs(v, id_map) for v in value]
    return value


def remap_known_mentions(value, id_map: dict[int, int]):
    """Reescreve id_N, 'ver N' e pares '(N/M)' quando N/M foram realocados.

    Anos soltos (2026, 17/11/2025) ficam intactos.
    """
    if not id_map:
        return value
    if isinstance(value, list):
        return [remap_known_mentions(v, id_map) for v in value]
    if not isinstance(value, str):
        return value
    value = remap_id_refs(value, id_map)

    def repl_ver(m: re.Match) -> str:
        old = int(m.group(1))
        if old not in id_map:
            return m.group(0)
        return f"ver {id_map[old]}"

    value = re.sub(r"\bver (\d+)\b", repl_ver, value)

    def repl_pair(m: re.Match) -> str:
        a, b = int(m.group(1)), int(m.group(2))
        if a not in id_map and b not in id_map:
            return m.group(0)
        return f"({id_map.get(a, a)}/{id_map.get(b, b)})"

    return re.sub(r"\((\d{4})/(\d{4})\)", repl_pair, value)


def apply_id_map(item: dict, id_map: dict[int, int]) -> None:
    if not id_map:
        return
    for key in REF_KEYS:
        if key in item:
            item[key] = remap_known_mentions(item[key], id_map)


def normalize_main_entry(entry: dict, source: str) -> dict | None:
    cat_raw = (entry.get("category") or entry.get("categoria") or entry.get("tipo") or "").lower()
    # IDs < 1000 com categoria editorial viram estudo temático em outro caminho.
    # IDs de track principal (>= 1000) publicam como evento, senão a ficha some da fila.
    if cat_raw == "analise_editorial":
        main_probe = parse_main_id(entry.get("id"))
        if main_probe is None or main_probe < 1000:
            return None

    eid = entry.get("id")
    if eid is None:
        return None
    main_id = parse_main_id(eid)
    if main_id is None:
        if isinstance(eid, str) and eid.startswith("__"):
            print(f"  SKIP {source}: ID pendente ({eid})")
        return None

    title = entry.get("title") or entry.get("titulo", "")
    if not title:
        return None

    jdate = normalize_date(
        entry.get("date")
        or entry.get("data_evento")
        or entry.get("data_registro")
        or entry.get("jekyll_date")
        or ""
    )

    ev = entry.get("evidencia_primaria") or {}
    resumo = (
        entry.get("summary")
        or entry.get("descricao")
        or ev.get("descricao")
        or entry.get("resumo")
        or ""
    )

    cat = resolve_category(entry)
    slug = entry.get("slug") or slugify(title)
    fname_md = entry.get("jekyll_filename") or f"{jdate}-{slugify(title)}.md"
    if not fname_md.endswith(".md"):
        fname_md += ".md"

    lacunas = entry.get("lacuna_investigativa") or entry.get("evidentiary_caveat") or ""
    if isinstance(lacunas, str):
        lacunas_list = [lacunas] if lacunas else []
    else:
        lacunas_list = list(lacunas)

    return {
        "id_corpus": str(main_id),
        "jekyll_filename": fname_md,
        "jekyll_date": jdate,
        "jekyll_categories": [cat],
        "jekyll_tags": build_tags(entry, cat),
        "jekyll_permalink": f"/posts/{Path(fname_md).stem}/",
        "titulo": title,
        "resumo": resumo,
        "categoria": entry.get("category") or entry.get("categoria") or entry.get("tipo") or cat,
        "pais": entry.get("pais", "Brasil"),
        "atores": parse_actors(
            entry.get("actors")
            or entry.get("atores")
            or [{"name": n} for n in (entry.get("pessoas_envolvidas") or [])]
        ),
        "instituicoes": (
            entry.get("institutions")
            or entry.get("instituicoes")
            or entry.get("instituicoes_envolvidas")
            or []
        ),
        "fontes_verificadas": parse_fontes(entry),
        "_analise": entry.get("analise") or entry.get("observacao_analitica") or "",
        "_result": entry.get("result") or "",
        "_legal": entry.get("legal_basis") or entry.get("legal_refs") or [],
        "_lacunas": lacunas_list,
        "_open_questions": entry.get("open_questions") or [],
        "_cadeia": entry.get("cadeia_logica") or "",
        "_ponto_inflexao": entry.get("ponto_de_inflexao") or "",
        "_connections": entry.get("connections") or [],
        "_evidence_status": entry.get("evidence_status") or entry.get("evidencia") or "",
        "_evidence_note": entry.get("evidence_note") or "",
        "_nota_correcao": entry.get("nota_correcao_midiatica"),
        "padroes": entry.get("patterns") or entry.get("padroes") or entry.get("padroes_sistemicos") or [],
        "_source": source,
    }


def render_timeline_post(u: dict) -> str:
    category = u["jekyll_categories"][0]
    tags = u.get("jekyll_tags") or []
    title = u["titulo"]
    resumo = u["resumo"]
    desc = yaml_escape((resumo[:157] + "...") if len(resumo) > 157 else resumo)
    image = IMAGE_BY_CATEGORY.get(category, "/assets/solid/circle-exclamation.svg")
    fm_tags = json.dumps(tags, ensure_ascii=False)

    parts = [
        "- &nbsp;",
        "{:toc .large-only}",
        "",
        f"# {title}",
        "",
        "***",
        "",
        "## Resumo",
        "",
        resumo,
        "",
        "***",
        "",
        "## Metadados do corpus",
        "",
        "| Campo | Valor |",
        "| --- | --- |",
        f"| `id_corpus` | **{u.get('id_corpus', '')}** |",
        f"| Categoria analitica | {u.get('categoria', '-') } |",
    ]
    if u.get("_evidence_status"):
        parts.append(f"| Evidencia | {u['_evidence_status']} |")
    parts.append("")
    if u.get("_evidence_note"):
        parts.extend([u["_evidence_note"], ""])
    if u.get("conflito_nota"):
        parts.extend([f"> **Nota de conflito ID:** {u['conflito_nota']}", ""])
    if u.get("_cadeia"):
        parts.extend(["## Cadeia logica", "", u["_cadeia"], ""])
    if u.get("atores"):
        parts.extend(["### Atores", ""] + [f"- {a}" for a in u["atores"]] + [""])
    if u.get("instituicoes"):
        parts.extend(["### Instituicoes", ""] + [f"- {i}" for i in u["instituicoes"]] + [""])
    if u.get("_result"):
        parts.extend(["## Resultado documentado", "", u["_result"], ""])
    if u.get("_ponto_inflexao"):
        parts.extend(["## Ponto de inflexao", "", u["_ponto_inflexao"], ""])
    if u.get("_analise") and u["_analise"] != resumo:
        parts.extend(["## Analise", "", u["_analise"], ""])
    if u.get("_legal"):
        parts.extend(["## Base legal", ""] + [f"- {lb}" for lb in u["_legal"]] + [""])
    nc = u.get("_nota_correcao")
    if nc:
        parts.extend([
            "## Nota de correcao midiatica",
            "",
            f"**Alegacao:** {nc.get('alegacao_circulando', '')}",
            "",
            f"**Correcao:** {nc.get('correcao', '')}",
            "",
        ])
    conns = u.get("_connections") or []
    if conns:
        conn_index = build_corpus_index()
        theme_index = build_thematic_index()
        conn_lines = [
            f"- {format_connection(c, conn_index, theme_index)}" for c in conns
        ]
        parts.extend(["## Conexoes", ""] + conn_lines + [""])
    lacunas = u.get("_lacunas") or []
    if lacunas:
        parts.extend(["## Lacunas investigativas", ""] + [f"- {x}" for x in lacunas] + [""])
    oq = u.get("_open_questions") or []
    if oq:
        parts.extend(["## Questoes em aberto", ""] + [f"- {x}" for x in oq] + [""])
    fontes = u.get("fontes_verificadas") or []
    if fontes:
        parts.extend(["## Fontes verificaveis", ""])
        for i, f in enumerate(fontes, 1):
            url = f.get("url", "")
            tit = f.get("titulo", "Fonte")
            if url:
                parts.append(f"{i}. [{tit}]({url})")
            elif tit:
                parts.append(f"{i}. {tit}")
        parts.append("")

    fm = f"""---
title: "{yaml_escape(title)}"
description: "{desc}"
date: {format_iso(u.get('jekyll_date', ''))}
image:
  path: "{image}"
tags: {fm_tags}
categories: {category}
permalink: {u.get('jekyll_permalink', '')}
id_corpus: "{u.get('id_corpus', '')}"
corpus_unificado: true
source_data: "{u.get('_source', '')}"
---

"""
    return fm + "\n".join(parts)


def study_title(data: dict) -> str:
    return data.get("titulo") or data.get("title") or ""


def study_date(data: dict) -> str:
    return normalize_date(
        data.get("data_registro") or data.get("data_evento") or data.get("date") or "2026-01-01"
    )


def render_estudos_post(data: dict, tid: int) -> tuple[str, str]:
    short_title = study_title(data)
    slug = data.get("slug") or slugify(short_title)
    slug = re.sub(r"^revisar-t\d+-", "", slug, flags=re.I)
    jdate = study_date(data)
    fname = f"{jdate}-{slug}.md"
    title = f"T-{tid} · {short_title.split('—')[0].strip()}" if "—" in short_title else f"T-{tid} · {short_title[:70]}"
    ev = data.get("evidencia_primaria") or {}
    resumo = (
        ev.get("descricao")
        or data.get("summary")
        or (data.get("analise") or "")[:400]
    )
    desc = yaml_escape((resumo[:157] + "...") if len(resumo) > 157 else resumo)
    padroes = data.get("padroes_ativados") or data.get("patterns") or []
    extra = data.get("tags") or []
    tags = ["estudo", "lawfare"] + [str(p).lower() for p in padroes] + [str(t).lower() for t in extra]
    if data.get("slug"):
        tags.append(data["slug"][:35])
    tags = list(dict.fromkeys(tags))[:10]
    fm_tags = json.dumps(tags, ensure_ascii=False)

    parts = [
        "- &nbsp;",
        "{:toc .large-only}",
        "",
        f"# {title}",
        "",
        resumo[:800] + ("..." if len(resumo) > 800 else ""),
        "",
    ]
    if data.get("cadeia_logica"):
        parts.extend(["## Cadeia logica", "", data["cadeia_logica"], ""])
    correcoes = data.get("correcoes_fonte_secundaria") or []
    if correcoes:
        parts.extend(["## Correcoes de fonte secundaria", "", "| Item | Citado | Correto |", "| --- | --- | --- |"])
        for c in correcoes:
            parts.append(
                f"| {c.get('item', '-')} | {c.get('citado_incorretamente_como', '-')} | {c.get('correto', '-')} |"
            )
        parts.append("")
    linha = data.get("linha_do_tempo") or []
    if isinstance(linha, list) and linha:
        parts.extend([
            "## Linha do tempo",
            "",
            "| Data | Ator | Tipo | Evidencia | Conteudo |",
            "| --- | --- | --- | --- | --- |",
        ])
        for row in linha:
            if not isinstance(row, dict):
                continue
            conteudo = str(row.get("conteudo", "")).replace("|", "/").replace("\n", " ")
            parts.append(
                "| {data} | {ator} | {tipo} | {evidencia} | {conteudo} |".format(
                    data=row.get("data", ""),
                    ator=str(row.get("ator", "")).replace("|", "/"),
                    tipo=row.get("tipo", ""),
                    evidencia=str(row.get("evidencia", "")).replace("|", "/"),
                    conteudo=conteudo,
                )
            )
        parts.append("")
    if data.get("analise"):
        parts.extend(["## Analise", "", data["analise"], ""])
    if data.get("result"):
        parts.extend(["## Resultado documentado", "", data["result"], ""])
    if data.get("ponto_de_inflexao"):
        parts.extend(["## Ponto de inflexao", "", data["ponto_de_inflexao"], ""])
    if data.get("lacuna_investigativa"):
        parts.extend(["## Lacuna investigativa", "", data["lacuna_investigativa"], ""])
    pats = data.get("patterns_cruzados") or padroes
    if pats:
        parts.extend(["## Padroes", ""])
        if pats and isinstance(pats[0], dict):
            for p in pats:
                parts.append(f"- **{p.get('id', '')}** — {p.get('descricao', '')}")
        else:
            parts.extend([f"- {p}" for p in pats])
        parts.append("")
    conns = data.get("connections") or []
    if conns:
        conn_index = build_corpus_index()
        theme_index = build_thematic_index()
        conn_lines = [
            f"- {format_connection(c, conn_index, theme_index)}" for c in conns
        ]
        parts.extend(["## Conexoes", ""] + conn_lines + [""])
    fonte_lines: list[str] = []
    url = ev.get("url_referencia", "")
    if url:
        for u in str(url).split(";"):
            u = u.strip()
            if u:
                fonte_lines.append(f"- [{ev.get('fonte', 'Fonte')}]({u})")
    for s in data.get("sources") or data.get("fontes") or []:
        if isinstance(s, dict) and s.get("url"):
            tit = s.get("title") or s.get("titulo") or s.get("outlet") or "Fonte"
            fonte_lines.append(f"- [{tit}]({s['url']})")
    seen_urls = set(re.findall(r"\((https?://[^)]+)\)", "\n".join(fonte_lines)))
    for row in data.get("linha_do_tempo") or []:
        if not isinstance(row, dict):
            continue
        ator = row.get("ator") or "Fonte"
        for src in row.get("fontes") or []:
            if isinstance(src, str) and src.startswith("http") and src not in seen_urls:
                fonte_lines.append(f"- [{ator}]({src})")
                seen_urls.add(src)
            elif isinstance(src, str) and src and not src.startswith("http"):
                fonte_lines.append(f"- {ator}: {src}")
    if fonte_lines:
        parts.extend(["## Fontes", ""] + fonte_lines + [""])
    parts.append(f"*Dossie T-{tid} · CC0 · lawfare-timeline*")

    fm = f"""---
id_corpus: "T-{tid}"
thematic_track: true
title: "{yaml_escape(title)}"
description: "{desc}"
date: {jdate}T12:00:00-03:00
image:
  path: "/assets/solid/book-open.svg"
tags: {fm_tags}
categories: estudos
mermaid: false
pin: false
permalink: /posts/{Path(fname).stem}/
source_data: "{data.get('_source_file', '')}"
---

"""
    return fm + "\n".join(parts), fname


def to_lawfare_assunto(u: dict, category: str) -> dict:
    rel = POSTS / category / u["jekyll_filename"]
    fonte = str(rel.relative_to(ROOT)).replace("/", "\\")
    tags = u.get("jekyll_tags") or [category]
    fontes = [f.get("url") for f in u.get("fontes_verificadas") or [] if f.get("url")]
    return {
        "titulo": u["titulo"],
        "data_evento": u["jekyll_date"],
        "data_iso": format_iso(u["jekyll_date"]),
        "categoria": category,
        "tags": tags if isinstance(tags, list) else [tags],
        "descricao": u["resumo"],
        "relevancia": "alta",
        "impacto_diplomatico": "N/A",
        "tipo_escandalo": u.get("categoria", "N/A"),
        "fontes": fontes,
        "pessoas_envolvidas": u.get("atores") or [],
        "instituicoes_envolvidas": u.get("instituicoes") or [],
        "pais": u.get("pais", "Brasil"),
        "valor_envolvido": "N/A",
        "prioridade": 1,
        "fonte_arquivo": fonte,
        "id": int(u["id_corpus"]),
    }


def load_todo_files() -> list[Path]:
    return sorted(TODO.glob("*.json"))


def process_all(dry_run: bool) -> tuple[list[dict], list[tuple[int, str, str]], list[str], list[str]]:
    main_entries: list[dict] = []
    thematic: list[tuple[int, str, str]] = []
    archived: list[str] = []
    remaps: list[str] = []
    written_posts: list[Path] = []
    taken_main = occupied_main_ids()
    taken_t = occupied_thematic_ids()
    global_id_map: dict[int, int] = {}

    for fpath in load_todo_files():
        try:
            data = json.loads(fpath.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"ERRO {fpath.name}: {exc}")
            continue

        tid = thematic_id_from_file(fpath, data)
        if tid is not None:
            final_t, old_t = allocate_id(tid, taken_t)
            if old_t is not None:
                note = f"{fpath.name}: T-{old_t} → T-{final_t}"
                remaps.append(note)
                print(f"  REALOCA {note}")
                data["id"] = final_t
                if not dry_run:
                    fpath.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            data["_source_file"] = fpath.name
            content, md_fname = render_estudos_post(data, final_t)
            target = POSTS / "estudos" / md_fname
            if target.exists():
                raise SystemExit(f"post ja existe, sem overwrite: {target.relative_to(ROOT)}")
            if dry_run:
                print(f"  [dry-run] T-{final_t}: {target.relative_to(ROOT)}")
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
                print(f"  OK {target.relative_to(ROOT)}")
            thematic.append((final_t, fpath.name, md_fname))
            archived.append(fpath.name)
            continue

        items: list[dict] = []
        thematic_only: list[dict] = []
        if isinstance(data, dict):
            if isinstance(data.get("main"), list):
                items.extend(data["main"])
            if isinstance(data.get("entries"), list):
                items.extend(data["entries"])
            if isinstance(data.get("entries_main"), list):
                items.extend(data["entries_main"])
            if isinstance(data.get("entradas"), list):
                items.extend(data["entradas"])
            if isinstance(data.get("thematic_entries"), list):
                items.extend(data["thematic_entries"])
            if isinstance(data.get("thematic"), list):
                thematic_only.extend(data["thematic"])
            if isinstance(data.get("entries_thematic"), list):
                thematic_only.extend(data["entries_thematic"])
            if isinstance(data.get("assuntos"), list):
                for assunto in data["assuntos"]:
                    if isinstance(assunto, dict) and assunto.get("id") is None and assunto.get("id_corpus"):
                        assunto["id"] = assunto["id_corpus"]
                    items.append(assunto)
            if (
                not items
                and not thematic_only
                and data.get("id") is not None
                and (data.get("title") or data.get("titulo"))
            ):
                items = [data]
        elif isinstance(data, list):
            items = data
        else:
            items = [data]
        batch_had_output = False
        pending_thematic: list[dict] = list(thematic_only)
        file_id_map: dict[int, int] = {}
        main_items: list[dict] = []
        for item in items:
            tid = thematic_id_from_entry(item)
            if tid is not None:
                pending_thematic.append(item)
                continue
            requested = parse_main_id(item.get("id"))
            if requested is not None:
                final_id, old_id = allocate_id(requested, taken_main)
                if old_id is not None:
                    file_id_map[old_id] = final_id
                    note = f"{fpath.name}: {old_id} → {final_id}"
                    remaps.append(note)
                    print(f"  REALOCA {note}")
                item["id"] = final_id
            main_items.append(item)
        if file_id_map:
            global_id_map.update(file_id_map)
            for item in main_items:
                apply_id_map(item, file_id_map)
        for item in main_items:
            u = normalize_main_entry(item, fpath.name)
            if not u:
                continue
            main_entries.append(u)
            target = POSTS / u["jekyll_categories"][0] / u["jekyll_filename"]
            if target.exists():
                raise SystemExit(f"post ja existe, sem overwrite: {target.relative_to(ROOT)}")
            if dry_run:
                print(f"  [dry-run] ID {u['id_corpus']}: {target.relative_to(ROOT)}")
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(render_timeline_post(u), encoding="utf-8")
                written_posts.append(target)
                print(f"  OK {target.relative_to(ROOT)}")
            batch_had_output = True
        thematic_touched = False
        for item in pending_thematic:
            tid = thematic_id_from_entry(item)
            if tid is None:
                continue
            final_t, old_t = allocate_id(tid, taken_t)
            if old_t is not None:
                note = f"{fpath.name}: T-{old_t} → T-{final_t}"
                remaps.append(note)
                print(f"  REALOCA {note}")
                item["id"] = f"T-{final_t}" if isinstance(item.get("id"), str) else final_t
                thematic_touched = True
            if global_id_map:
                apply_id_map(item, global_id_map)
                thematic_touched = True
            item["_source_file"] = fpath.name
            content, md_fname = render_estudos_post(item, final_t)
            target = POSTS / "estudos" / md_fname
            if target.exists():
                raise SystemExit(f"post ja existe, sem overwrite: {target.relative_to(ROOT)}")
            if dry_run:
                print(f"  [dry-run] T-{final_t}: {target.relative_to(ROOT)}")
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
                written_posts.append(target)
                print(f"  OK {target.relative_to(ROOT)}")
            thematic.append((final_t, fpath.name, md_fname))
            batch_had_output = True
        if (file_id_map or thematic_touched) and not dry_run:
            if isinstance(data, dict):
                meta = data.setdefault("_meta", {})
                if isinstance(meta, dict):
                    meta["realocado_em"] = date.today().isoformat()
                    if file_id_map:
                        meta["realocacao"] = {str(k): v for k, v in file_id_map.items()}
                    elif global_id_map:
                        meta["refs_realocadas"] = {str(k): v for k, v in global_id_map.items()}
            fpath.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if batch_had_output or not isinstance(data, dict) or not data.get("_staging_note"):
            archived.append(fpath.name)

    if not dry_run and written_posts:
        conn_index = build_corpus_index()
        theme_index = build_thematic_index()
        for path in written_posts:
            text = path.read_text(encoding="utf-8")
            new_text, n = fix_conexoes_section(text, conn_index, theme_index)
            if n:
                path.write_text(new_text, encoding="utf-8")
                print(f"  links {path.name}: {n}")

    return main_entries, thematic, archived, remaps


def update_lawfare(entries: list[dict], dry_run: bool) -> None:
    if not entries or dry_run:
        return
    lf_data = json.loads(LAWFARE.read_text(encoding="utf-8"))
    assuntos = lf_data.get("assuntos", [])
    new_ids = {int(u["id_corpus"]) for u in entries}
    if len(new_ids) != len(entries):
        raise SystemExit("IDs duplicados na fila apos alocacao — merge abortado")
    occupied = {a.get("id") for a in assuntos}
    collision = sorted(i for i in new_ids if i in occupied)
    if collision:
        raise SystemExit(f"colisao com lawfare.json (sem overwrite): {collision}")
    for u in entries:
        assuntos.append(to_lawfare_assunto(u, u["jekyll_categories"][0]))
    assuntos.sort(key=lambda x: x.get("id") or 0)
    lf_data["assuntos"] = assuntos
    lf_data["total"] = len(assuntos)
    lf_data["data_extração"] = date.today().isoformat()
    datas = [a["data_evento"] for a in assuntos if a.get("data_evento") and a["data_evento"] != "0001-01-01"]
    if datas:
        lf_data["periodo"] = f"{min(datas)} a {max(datas)}"
    LAWFARE.write_text(json.dumps(lf_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"lawfare.json: +{len(entries)} assuntos (total {len(assuntos)})")


def update_unified(entries: list[dict], dry_run: bool) -> None:
    if not entries or dry_run or not UNIFIED.is_file():
        return
    uni_data = json.loads(UNIFIED.read_text(encoding="utf-8"))
    entradas = uni_data.get("entradas", [])
    new_ids = {int(u["id_corpus"]) for u in entries}
    entradas = [e for e in entradas if int(e.get("id_corpus", 0)) not in new_ids]
    for u in entries:
        clean = {k: v for k, v in u.items() if not k.startswith("_")}
        clean["verificado"] = True
        clean["status_publicacao"] = "coberto_por_artigo"
        clean["id_corpus"] = u["id_corpus"]
        entradas.append(clean)
    entradas.sort(key=lambda x: int(x.get("id_corpus") or 0))
    uni_data["entradas"] = entradas
    UNIFIED.write_text(json.dumps(uni_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"lawfare-unified-corpus.json: +{len(entries)} entradas")


def update_sync(main_entries: list[dict], thematic: list[tuple[int, str, str]], dry_run: bool) -> None:
    if dry_run or not SYNC.is_file():
        return
    sync_data = json.loads(SYNC.read_text(encoding="utf-8"))
    batch_note = f"Merge todo {date.today().isoformat()}"

    if main_entries:
        new_ids = [int(u["id_corpus"]) for u in main_entries]
        new_id_set = set(new_ids)
        lf_ids = sorted(
            int(a["id"])
            for a in json.loads(LAWFARE.read_text(encoding="utf-8")).get("assuntos") or []
            if isinstance(a.get("id"), int)
        )
        last_main = lf_ids[-1] if lf_ids else max(new_ids)
        main = sync_data.setdefault("tracks", {}).setdefault("main", {})
        batches = main.setdefault("confirmed_batches", [])
        max_batch_end = max((b["range"][1] for b in batches if b.get("range")), default=0)
        orphans = [i for i in lf_ids if i > max_batch_end and i not in new_id_set]
        if orphans:
            run_start = orphans[0]
            prev = orphans[0]
            runs: list[tuple[int, int]] = []
            for i in orphans[1:]:
                if i == prev + 1:
                    prev = i
                    continue
                runs.append((run_start, prev))
                run_start = prev = i
            runs.append((run_start, prev))
            for start, end in runs:
                batches.append({
                    "range": [start, end],
                    "status": "confirmed",
                    "notes": (
                        f"Catch-up {date.today().isoformat()}: IDs {start}-{end} "
                        "já estavam em lawfare.json; o sync estava atrás. Sem reescrita de fichas."
                    ),
                })
        main["last_id"] = last_main
        main["next_available"] = last_main + 1
        main["last_confirmed"] = last_main
        main["last_jekyll_published"] = last_main
        batches.append({
            "range": [min(new_ids), max(new_ids)],
            "status": "confirmed",
            "notes": f"{batch_note}: main IDs {min(new_ids)}-{max(new_ids)}.",
        })

    if thematic:
        last_t = max(t[0] for t in thematic)
        thematic_track = sync_data.setdefault("tracks", {}).setdefault("thematic", {})
        thematic_track["last_id"] = last_t
        thematic_track["next_available"] = last_t + 1
        entries = thematic_track.setdefault("entries", [])
        existing_ids = {int(e["id"]) for e in entries}
        for tid, fname, md_fname in thematic:
            note = f"Estudo Jekyll _posts/estudos/{md_fname}"
            if tid in existing_ids:
                for e in entries:
                    if int(e["id"]) == tid:
                        e.update({"status": "confirmed", "artifact": md_fname, "notes": note})
            else:
                entries.append({
                    "id": tid,
                    "status": "confirmed",
                    "topic": f"T-{tid} ({fname})",
                    "artifact": md_fname,
                    "notes": note,
                })
        entries.sort(key=lambda x: int(x["id"]))

    sync_status = sync_data.setdefault("sync_status", {})
    sync_status["main_track_last_sync"] = date.today().isoformat()
    sync_status["thematic_track_last_sync"] = date.today().isoformat()
    if main_entries:
        sync_status.setdefault("ids_confirmed_total", {})["main_track"] = (
            f"{max(int(u['id_corpus']) for u in main_entries)} (Jekyll + lawfare.json)"
        )
    if thematic:
        sync_status.setdefault("ids_confirmed_total", {})["thematic_track"] = max(t[0] for t in thematic)

    today = date.today().isoformat()
    meta = sync_data.setdefault("_meta", {})
    meta["updated"] = today
    meta_tracks = meta.setdefault("tracks", {})
    if main_entries:
        last_main = int(sync_data["tracks"]["main"]["last_id"])
        sync_data["last_main_id"] = last_main
        sync_data["next_available"] = last_main + 1
        sync_data["updated"] = today
        meta_main = meta_tracks.setdefault("main", {})
        meta_main["id_range"] = f"1–{last_main} (confirmed)"
        meta_main["last_confirmed"] = last_main
        meta_main["last_jekyll_published"] = last_main
        meta_main["notes"] = (
            f"lawfare.json confirmado até {last_main}. Próximo ID livre: {last_main + 1}."
        )
    if thematic:
        last_t = max(t[0] for t in thematic)
        meta_t = meta_tracks.setdefault("thematic", {})
        meta_t["id_range"] = f"100–{last_t}"
        meta_t["last_confirmed"] = last_t
        meta_t["last_session_produced"] = last_t
        meta_t["notes"] = f"T-{last_t} confirmado. Próximo thematic livre: T-{last_t + 1}."
    t_on_disk = len(list((POSTS / "estudos").glob("*.md")))
    sync_data.setdefault("session_log", []).append({
        "date": today,
        "session": "cursor — fila todo sem colisao de ID",
        "produced": [
            (
                f"Main track {min(int(u['id_corpus']) for u in main_entries)}-"
                f"{max(int(u['id_corpus']) for u in main_entries)}"
                if main_entries else "Main track sem entradas novas"
            ),
            (
                f"Thematic T-{min(t[0] for t in thematic)}–T-{max(t[0] for t in thematic)}"
                if thematic else "Thematic sem entradas novas"
            ),
        ],
        "summary": {
            "lawfare_max_id": sync_data.get("last_main_id"),
            "next_main_id": sync_data.get("next_available"),
            "thematic_last": (
                f"T-{max(t[0] for t in thematic)}" if thematic else None
            ),
            "next_thematic": (
                f"T-{max(t[0] for t in thematic) + 1}" if thematic else None
            ),
            "t_studies_on_disk": t_on_disk,
        },
        "status": "completed",
    })

    SYNC.write_text(json.dumps(sync_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not dry_run:
        export_sync_to_gdrive(quiet=False)
    print("claude.ai-corpus-ids-sync.json atualizado.")


def archive_files(fnames: list[str], dry_run: bool) -> None:
    PROC.mkdir(parents=True, exist_ok=True)
    for fname in fnames:
        src = TODO / fname
        if not src.is_file():
            continue
        dst = PROC / fname
        if dry_run:
            print(f"  [dry-run] archive {fname}")
            continue
        if dst.is_file():
            shutil.copy2(str(src), str(dst))
            src.unlink()
        else:
            shutil.move(str(src), str(dst))
        print(f"  archive -> processados/{fname}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    files = load_todo_files()
    if not files:
        print("Nenhum JSON em _data/todo/")
        return 0

    print(f"=== Processando {len(files)} arquivo(s) em _data/todo/ ===")
    main_entries, thematic, archived, remaps = process_all(args.dry_run)

    update_lawfare(main_entries, args.dry_run)
    update_unified(main_entries, args.dry_run)
    update_sync(main_entries, thematic, args.dry_run)

    print("\n=== Arquivar JSON processados ===")
    archive_files(list(dict.fromkeys(archived)), args.dry_run)

    if remaps:
        print("\nRealocacoes:")
        for line in remaps:
            print(f"  - {line}")
    print(f"\nConcluido: {len(main_entries)} posts timeline, {len(thematic)} estudos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
