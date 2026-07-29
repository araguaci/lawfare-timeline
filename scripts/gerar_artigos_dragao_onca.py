#!/usr/bin/env python3
"""
Gera posts Jekyll (_posts/dragao-onca/) automaticamente a partir dos batches JSON
da série "O Dragão e a Onça" localizados em _data/todo/

Versão: 2026-07-24
Autor: Claude Code
Propósito: Converter dados estruturados JSON em artigos MD com referências, links internos e assets
"""

import json
import re
import shutil
import unicodedata
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote

# ===================== CONFIG =====================
ROOT = Path(__file__).resolve().parents[1]
TODO_DIR = ROOT / "_data" / "todo"
PROC_DIR = ROOT / "_data" / "processados"
POSTS_DIR = ROOT / "_posts" / "dragao-onca"
ASSETS_DIR = ROOT / "assets" / "img"
LAWFARE = ROOT / "_data" / "lawfare.json"
SYNC = ROOT / "_data" / "claude.ai-corpus-ids-sync.json"

# Mapa de regiões para imagens
REGION_IMAGE_MAP = {
    "brasil": "dragao-onca-brasil-federal.webp",
    "federal": "dragao-onca-brasil-federal.webp",
    "goias": "dragao-onca-goias.webp",
    "para": "dragao-onca-para.webp",
    "amazonas": "dragao-onca-amazonas.webp",
    "minas": "dragao-onca-minas-gerais.webp",
    "minas-gerais": "dragao-onca-minas-gerais.webp",
    "pl2780": "dragao-onca-pl2780.webp",
    "juridico": "dragao-onca-braco-juridico.webp",
    "braco-juridico": "dragao-onca-braco-juridico.webp",
    "diplomatico": "dragao-onca-brasil-federal.webp",
    "diplomatic": "dragao-onca-brasil-federal.webp",
    "espirito": "dragao-onca-espirito-santo.webp",
    "es": "dragao-onca-espirito-santo.webp",
    "bahia": "dragao-onca-bahia.webp",
    "sao-paulo": "dragao-onca-sao-paulo.webp",
    "sp": "dragao-onca-sao-paulo.webp",
    "parana": "dragao-onca-parana.webp",
    "pr": "dragao-onca-parana.webp",
    "rs": "dragao-onca-rio-grande-do-sul.webp",
    "rio-grande-do-sul": "dragao-onca-rio-grande-do-sul.webp",
    "rio-grande": "dragao-onca-rio-grande-do-sul.webp",
    "china": "dragao-onca.webp",
    "ranking": "dragao-onca-ranking-cebc.webp",
    "cebc": "dragao-onca-ranking-cebc.webp",
    "sintese": "dragao-onca-sintese.webp",
    "amapa": "dragao-onca-amapa.webp",
    "ap": "dragao-onca-amapa.webp",
    "rj": "dragao-onca-rj.webp",
    "rio-de-janeiro": "dragao-onca-rj.webp",
    "rio": "dragao-onca-rj.webp",
    "santa-catarina": "dragao-onca-santa-catarina.webp",
    "sc": "dragao-onca-santa-catarina.webp",
}

DEFAULT_IMAGE = "dragao-onca.webp"

# ===================== UTILITIES =====================

def slugify(text: str, max_len: int = 80) -> str:
    """Converte texto em slug URL-safe."""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text).strip('-')
    return text[:max_len].rstrip('-')


def post_slug_from_filename(filename: str) -> str:
    """Extrai slug Jekyll (:title) a partir do nome do arquivo do post."""
    stem = Path(filename).stem
    if len(stem) > 11 and stem[4] == "-" and stem[7] == "-" and stem[10] == "-":
        return stem[11:]
    return stem


def extract_post_title(text: str) -> str:
    """Extrai título legível do front matter ou H1."""
    match = re.search(r'^title:\s*"(.*)"\s*$', text, re.MULTILINE)
    if match:
        return match.group(1).replace('\\"', '"')
    match = re.search(r"^title:\s*'(.*)'\s*$", text, re.MULTILINE)
    if match:
        return match.group(1)
    h1 = re.search(r"^# (.+)$", text, re.MULTILINE)
    return h1.group(1).strip() if h1 else ""


def markdown_link_label(text: str) -> str:
    return text.replace("[", "\\[").replace("]", "\\]")


def build_post_index(posts_dir: Path = POSTS_DIR) -> dict[str, dict[str, str]]:
    """Mapeia timeline_id -> slug e título do post."""
    index: dict[str, dict[str, str]] = {}
    for path in sorted(posts_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        match = re.search(r"^timeline_id:\s*(\d+)\s*$", text, re.MULTILINE)
        if not match:
            continue
        timeline_id = match.group(1)
        if timeline_id in index and path.name.startswith("-"):
            continue
        index[timeline_id] = {
            "slug": post_slug_from_filename(path.name),
            "title": extract_post_title(text),
        }
    return index


def post_url_for_timeline_id(
    timeline_id: str, post_index: dict[str, dict[str, str]] | None = None
) -> str:
    """Retorna URL interna do post Jekyll para um timeline_id."""
    index = post_index or build_post_index()
    meta = index.get(str(timeline_id).replace("id_", "").replace("_", ""))
    if meta and meta.get("slug"):
        return f"/posts/{meta['slug']}/"
    return f"/timeline/entries/{timeline_id}"


def post_title_for_timeline_id(
    timeline_id: str, post_index: dict[str, dict[str, str]] | None = None
) -> str:
    """Retorna título do post para um timeline_id."""
    index = post_index or build_post_index()
    meta = index.get(str(timeline_id).replace("id_", "").replace("_", ""))
    if meta and meta.get("title"):
        return meta["title"]
    return f"Entrada {timeline_id}"


def resolve_region_image(batch_name: str) -> str:
    """Identifica a imagem apropriada baseada no nome do batch."""
    batch_lower = batch_name.lower()
    for region_key, img_name in REGION_IMAGE_MAP.items():
        if region_key in batch_lower:
            return f"/assets/img/{img_name}"
    return f"/assets/img/{DEFAULT_IMAGE}"


def resolve_entry_image(entry: dict, batch_name: str) -> str:
    """Hero regional por tags da entrada; fallback no nome do batch."""
    for raw in entry.get("tags") or []:
        key = str(raw).lower().replace("_", "-")
        if key in REGION_IMAGE_MAP:
            return f"/assets/img/{REGION_IMAGE_MAP[key]}"
    return resolve_region_image(batch_name)


def normalize_lawfare_entry(entry: dict, batch_file: Path | None = None) -> dict:
    """Normaliza entries lawfare.json / todo → formato do gerador."""
    e = dict(entry)
    e["title"] = (e.get("title") or e.get("titulo") or "").strip()
    e["summary"] = e.get("summary") or e.get("descricao") or e.get("notes") or ""
    e["date"] = (e.get("date") or e.get("data_evento") or e.get("data_iso") or "")[:10]
    if is_dragao_onca_batch(batch_file):
        e["category"] = "dragao-onca"
    else:
        e["category"] = e.get("category") or e.get("categoria") or "dragao-onca"
    tid = parse_thematic_id(e.get("id"))
    if tid is not None and is_dragao_onca_batch(batch_file) and batch_file.name.startswith("lawfare-thematic-"):
        e["id"] = tid
    patterns = list(e.get("patterns") or [])
    for tag in e.get("tags") or []:
        if re.match(r"^P\d", str(tag), re.I) and tag not in patterns:
            patterns.append(tag)
    e["patterns"] = patterns
    if not e.get("actors") and e.get("pessoas_envolvidas"):
        e["actors"] = [
            {"name": n, "role": "", "institution": ""}
            for n in e["pessoas_envolvidas"]
        ]
    if not e.get("institutions") and e.get("instituicoes_envolvidas"):
        e["institutions"] = list(e["instituicoes_envolvidas"])
    if not e.get("sources") and e.get("fontes"):
        e["sources"] = [
            {"title": "Fonte", "url": u}
            if isinstance(u, str)
            else u
            for u in e["fontes"]
        ]
    if e.get("impacto_diplomatico") and not e.get("result"):
        e["result"] = e["impacto_diplomatico"]
    return e


def entry_to_assunto(entry: dict, rel_post: str) -> dict:
    """Converte entry normalizada → assunto lawfare.json."""
    e = normalize_lawfare_entry(entry)
    tags = list(e.get("tags") or [])
    for p in e.get("patterns") or []:
        if p not in tags:
            tags.append(p)
    if e.get("category") and e["category"] not in tags:
        tags.insert(0, e["category"])
    fontes = []
    for s in e.get("sources") or []:
        if isinstance(s, dict) and s.get("url"):
            fontes.append(s["url"])
        elif isinstance(s, str) and s.startswith("http"):
            fontes.append(s)
    return {
        "titulo": e["title"],
        "data_evento": e["date"],
        "data_iso": format_iso(e["date"]),
        "categoria": e["category"],
        "tags": tags[:12],
        "descricao": e["summary"],
        "relevancia": entry.get("relevancia") or "alta",
        "impacto_diplomatico": entry.get("impacto_diplomatico") or e.get("result") or "N/A",
        "tipo_escandalo": entry.get("tipo_escandalo") or "N/A",
        "fontes": fontes,
        "pessoas_envolvidas": [a.get("name", a) if isinstance(a, dict) else a for a in (e.get("actors") or [])],
        "instituicoes_envolvidas": e.get("institutions") or [],
        "pais": entry.get("pais") or "Brasil",
        "valor_envolvido": entry.get("valor_envolvido") or "N/A",
        "prioridade": entry.get("prioridade") or 1,
        "analise": entry.get("analise") or "",
        "lacuna_investigativa": entry.get("lacuna_investigativa") or "",
        "connections": entry.get("connections") or [],
        "fonte_arquivo": rel_post.replace("/", "\\"),
        "id": int(e["id"]),
    }


def format_iso(d: str) -> str:
    return f"{(d or '2026-01-01')[:10]}T12:00:00.000Z"


def format_date_yaml(date_str: str) -> str:
    """Formata data para YAML front matter (YYYY-MM-DD)."""
    if not date_str:
        return "2026-01-01"
    try:
        # Remove hora se presente
        date_part = date_str.split('T')[0] if 'T' in date_str else date_str[:10]
        return date_part
    except:
        return "2026-01-01"


def yaml_escape(s: str) -> str:
    return s.replace('"', '\\"').replace("\n", " ")


def assunto_to_entry(assunto: dict) -> dict:
    """Converte assunto lawfare.json → entry do gerador."""
    tags = assunto.get("tags") or []
    patterns = [t for t in tags if re.match(r"^P\d", str(t), re.I)]
    fontes = assunto.get("fontes") or []
    sources = []
    for f in fontes:
        if isinstance(f, str) and f.startswith("http"):
            sources.append({"title": "Fonte", "url": f})
        elif isinstance(f, dict):
            sources.append(f)
    actors = [{"name": n, "role": "", "institution": ""} for n in (assunto.get("pessoas_envolvidas") or [])]
    return {
        "id": str(assunto.get("id", "")),
        "date": (assunto.get("data_evento") or assunto.get("data_iso") or "")[:10],
        "title": assunto.get("titulo") or assunto.get("title", ""),
        "summary": assunto.get("descricao") or assunto.get("summary", ""),
        "category": assunto.get("categoria") or "dragao-onca",
        "actors": actors,
        "institutions": assunto.get("instituicoes_envolvidas") or [],
        "patterns": patterns,
        "sources": sources,
        "connections": assunto.get("connections") or [],
        "status": "confirmado",
        "lacuna_investigativa": assunto.get("lacuna_investigativa") or "",
        "analise": assunto.get("analise") or "",
        "result": assunto.get("result") or assunto.get("impacto_diplomatico") or "",
    }


def parse_thematic_id(raw) -> int | None:
    """Converte id temático (244, 'T-244', 't244') → int."""
    if raw is None:
        return None
    s = str(raw).strip().upper()
    m = re.match(r"^T-?(\d+)$", s)
    if m:
        return int(m.group(1))
    if s.isdigit():
        return int(s)
    return None


def is_dragao_onca_batch(batch_file: Path | None) -> bool:
    return bool(batch_file and "dragao-onca" in batch_file.stem.lower())


def thematic_slug_from_batch(batch_file: Path, entry_id: str) -> str:
    stem = batch_file.stem
    m = re.search(rf"T-?{entry_id}-(.+)$", stem, re.I)
    if m:
        return f"t{entry_id}-{m.group(1)}"
    return f"t{entry_id}-dragao-onca"


def extract_entries_from_batch(data, batch_file: Path) -> list[dict]:
    entries: list[dict] = []
    if isinstance(data, list):
        data = {"entries": data}
    if isinstance(data.get("entries"), list):
        entries.extend(normalize_lawfare_entry(x, batch_file) for x in data["entries"])
    if isinstance(data.get("assuntos"), list):
        entries.extend(assunto_to_entry(a) for a in data["assuntos"])
    if not entries and isinstance(data, dict) and data.get("id") is not None:
        if data.get("topic") or data.get("title"):
            entries.append(normalize_lawfare_entry(data, batch_file))
    return entries


def generate_synthesis_sections(entry: dict) -> str:
    """Seções extras para síntese cross-state (T-243)."""
    parts: list[str] = []
    if entry.get("correcao_metodologica"):
        parts.extend(["## ⚠️ Correção metodológica", "", entry["correcao_metodologica"], ""])
    if entry.get("escopo_real_da_serie"):
        escopo = entry["escopo_real_da_serie"]
        parts.extend(["## 📊 Escopo da série", ""])
        if isinstance(escopo, dict):
            for k, v in escopo.items():
                parts.append(f"- **{k.replace('_', ' ').title()}:** {v}")
        else:
            parts.append(str(escopo))
        parts.append("")
    rows = entry.get("tabela_comparativa_estados") or []
    if rows:
        parts.extend(["## 🗺️ Comparativo entre estados", ""])
        for row in rows:
            if not isinstance(row, dict):
                continue
            estado = row.get("estado", "—")
            parts.append(f"### {estado}")
            for key in ("potencia", "mecanismo", "resultado", "captura_de_valor"):
                if row.get(key):
                    parts.append(f"- **{key.replace('_', ' ').title()}:** {row[key]}")
            parts.append("")
    tipologia = entry.get("tipologia_mecanismos_identificados") or {}
    if tipologia:
        parts.extend(["## 🔬 Tipologia de mecanismos", ""])
        for nome, info in tipologia.items():
            if isinstance(info, dict):
                parts.append(f"- **{nome.replace('_', ' ')}** — casos: {', '.join(info.get('casos', []))}; {info.get('nota', '')}")
            else:
                parts.append(f"- **{nome}:** {info}")
        parts.append("")
    ranking = entry.get("ranking_cebc_2007_2025") or {}
    if ranking:
        parts.extend(["## 📊 Ranking CEBC (2007-2025)", ""])
        if isinstance(ranking, dict):
            if ranking.get("fonte"):
                parts.append(f"**Fonte:** {ranking['fonte']}")
            meta = []
            for k in ("estoque_total_usd", "projetos_total", "ufs_com_projetos"):
                if ranking.get(k):
                    meta.append(f"{k.replace('_', ' ')}: {ranking[k]}")
            if meta:
                parts.append(" · ".join(meta))
            parts.append("")
            top = ranking.get("top_estados_serie") or []
            if top:
                parts.append("| # | Estado | Projetos | Variação | Capítulo |")
                parts.append("|---|--------|----------|----------|----------|")
                for row in top:
                    if isinstance(row, dict):
                        parts.append(
                            f"| {row.get('posicao', '—')} | {row.get('estado', '—')} | "
                            f"{row.get('projetos', '—')} | {row.get('variacao', '—')} | {row.get('capitulo', '—')} |"
                        )
                parts.append("")
            if ranking.get("setor_lider_valor"):
                parts.append(f"- **Setor líder (valor):** {ranking['setor_lider_valor']}")
            if ranking.get("distribuicao_regional"):
                parts.append(f"- **Distribuição regional:** {ranking['distribuicao_regional']}")
            parts.append("")
    if entry.get("ponto_de_inflexao"):
        parts.extend(["## 📌 Ponto de inflexão", "", entry["ponto_de_inflexao"], ""])
    return "\n".join(parts)


def extract_year(date_str: str) -> str:
    """Extrai ano da data."""
    if not date_str or len(date_str) < 4:
        return "2026"
    try:
        return date_str[:4]
    except Exception:
        return "2026"


def format_source(source: Dict) -> Tuple[str, str, str]:
    """Extrai título, URL e outlet de uma fonte."""
    if isinstance(source, str):
        return source, "", ""

    title = source.get("title", "Fonte")
    url = source.get("url", "")
    outlet = source.get("outlet", "")
    return title, url, outlet


def generate_actors_section(actors: List) -> str:
    """Gera seção de atores."""
    if not actors:
        return "—"

    lines = []
    for actor in actors:
        if isinstance(actor, dict):
            name = actor.get("name", "")
            role = actor.get("role", "")
            institution = actor.get("institution", "")

            parts = [name]
            if role:
                parts.append(f"({role})")
            if institution:
                parts.append(f"[{institution}]")

            lines.append(" ".join(parts))
        else:
            lines.append(str(actor))

    return "\n".join(f"- {line}" for line in lines) if lines else "—"


def generate_sources_section(sources: List) -> str:
    """Gera seção de fontes externas com links."""
    if not sources:
        return ""

    section = "## 🔗 Fontes Externas\n\n"

    for source in sources:
        title, url, outlet = format_source(source)
        date = ""

        if isinstance(source, dict):
            date = source.get("date", "")

        if url:
            metadata = []
            if outlet:
                metadata.append(f"*{outlet}*")
            if date:
                metadata.append(f"{date}")

            meta_str = " · ".join(metadata) if metadata else ""
            section += f"- [{title}]({url}) {meta_str}\n"
        else:
            section += f"- {title}\n"

    return section


def generate_connections_section(
    connections: List, entry_id: str, post_index: dict[str, dict[str, str]] | None = None
) -> str:
    """Gera seção de referências internas (IDs conectados)."""
    if not connections:
        return ""

    index = post_index or build_post_index()
    section = "## 🔗 Artigos Relacionados\n\n"
    section += "Entradas conectadas nesta série:\n\n"

    for conn_id in connections:
        conn_id_clean = str(conn_id).replace("id_", "").replace("_", "")
        url = post_url_for_timeline_id(conn_id_clean, index)
        label = markdown_link_label(post_title_for_timeline_id(conn_id_clean, index))
        section += f"- [{label}]({url})\n"

    return section


def generate_patterns_section(patterns: List) -> str:
    """Gera seção de padrões analíticos."""
    if not patterns:
        return ""

    section = "## 📊 Padrões Analíticos\n\n"

    pattern_descriptions = {
        "P04b": "Both-sidesism funcional — padrão de falsa equivalência",
        "P05": "Uso de recursos/ativos públicos como vetor de apropriação privada",
        "P09": "Captura regulatória — controle de agências por interesses capturados",
        "P10": "Infraestrutura de serviço compartilhada — institucionalização permanente",
        "P11": "Escalada de consolidação — replicação e amplificação de padrão",
        "P06": "Exclusão de voz — negação de direito a voto ou fala",
    }

    for pattern in patterns:
        desc = pattern_descriptions.get(pattern, "")
        if desc:
            section += f"- **{pattern}** — {desc}\n"
        else:
            section += f"- **{pattern}**\n"

    return section


def generate_analysis_section(analysis: str, title: str) -> str:
    """Gera seção de análise com links para IA."""
    if not analysis:
        return ""

    section = "## 🔍 Análise\n\n"
    section += f"{analysis}\n\n"

    # Links para pesquisa
    query = quote(f"{title}")
    section += "### Links para Pesquisa\n\n"
    section += f"- [🤖 Pesquisar com Perplexity](https://www.perplexity.ai/search?q={query})\n"
    section += f"- [🌐 Buscar no Google](https://www.google.com/search?q={query})\n"
    section += f"- [📖 Buscar na Wikipedia](https://pt.wikipedia.org/w/index.php?search={query})\n"

    return section


def generate_lacunas_section(lacuna: str) -> str:
    """Gera seção de lacunas investigativas."""
    if not lacuna:
        return ""

    section = "## ❓ Lacunas Investigativas\n\n"
    section += f"{lacuna}\n\n"
    return section


# ===================== MAIN GENERATION =====================

def generate_post_from_entry(
    entry: Dict, batch_name: str, batch_file: Optional[Path] = None
) -> Tuple[str, str]:
    """
    Gera um post Jekyll (arquivo .md) a partir de uma entry JSON.
    Retorna (filepath, status_message)

    Suporta dois formatos:
    1. Batch entries (com 'date', 'summary', etc.)
    2. Thematic entries (com 'topic', 'notes', 'artifact', etc.)
    """
    is_thematic = is_dragao_onca_batch(batch_file) and batch_file.name.startswith("lawfare-thematic-")
    raw_id = entry.get("id", "")
    thematic_num = parse_thematic_id(raw_id) if is_thematic else None
    entry_id = str(thematic_num if thematic_num is not None else raw_id).strip()

    # Suporte para ambos os formatos
    title = entry.get("title") or entry.get("topic", "Sem título")
    title = title.strip()

    if not entry_id or not title:
        return "", f"⚠️  Entrada incompleta: ID ou título faltando"

    # Componentes do arquivo
    date_event = entry.get("date", "")[:10]

    if is_thematic and batch_file:
        date_event = "2026-01-01"
        slug_part = thematic_slug_from_batch(batch_file, entry_id)
        filename = f"2026-07-24-{slug_part}.md"
    elif not date_event and entry.get("artifact"):
        if batch_file:
            slug_part = thematic_slug_from_batch(batch_file, entry_id)
            filename = f"2026-07-24-{slug_part}.md"
        else:
            artifact_name = entry.get("artifact", "").replace(".html", "")
            filename = f"2026-07-24-t{entry_id}-{artifact_name}.md"
    else:
        slug = slugify(title)
        filename = f"{date_event}-id{entry_id}-{slug}.md"

    # Criação do diretório
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    filepath = POSTS_DIR / filename

    # Frontmatter
    description = yaml_escape((entry.get("summary") or entry.get("notes", ""))[:200])
    year = extract_year(date_event)
    image_path = resolve_entry_image(entry, batch_name)

    # Tags baseadas em categoria e padrões
    tags = [entry.get("category", "dragao-onca"), year]
    if entry.get("patterns"):
        tags.extend(entry["patterns"][:2])
    state_tags = [
        t for t in (entry.get("tags") or [])
        if t not in tags and t not in ("dragao-onca", "china", "diplomacia", "simetria")
        and not re.match(r"^P\d", str(t), re.I)
    ]
    tags.extend(state_tags[:2])
    tags = list(dict.fromkeys(tag for tag in tags if tag))

    frontmatter = f"""---
layout: post
title: "{yaml_escape(title)}"
description: "{description}..."
date: {format_date_yaml(date_event)}
image: {image_path}
tags: {json.dumps(tags, ensure_ascii=False)}
categories: dragao-onca
timeline_id: {entry_id}
status: {entry.get('status', 'confirmado')}
---

"""

    # Body
    body = ""
    body += f"# {title}\n\n"
    body += f"**Data:** {date_event} | **ID:** {entry_id} | **Status:** {entry.get('status', 'confirmado')}\n\n"
    body += f"***\n\n"

    # Resumo
    body += "## 📋 Resumo\n\n"
    summary = entry.get('summary') or entry.get('notes', 'Sem descrição disponível.')
    body += f"{summary}\n\n"

    # Resultado/Consequência
    if entry.get("result"):
        body += "### Resultado\n\n"
        body += f"{entry.get('result')}\n\n"

    # Atores
    actors = entry.get("actors", [])
    if actors:
        body += "## 👥 Atores Envolvidos\n\n"
        body += generate_actors_section(actors)
        body += "\n\n"

    # Instituições
    institutions = entry.get("institutions", [])
    if institutions:
        body += "## 🏛️ Instituições\n\n"
        for inst in institutions:
            body += f"- {inst}\n"
        body += "\n"

    # Base jurídica
    legal_basis = entry.get("legal_basis", [])
    if legal_basis:
        body += "## ⚖️ Base Jurídica\n\n"
        for basis in legal_basis:
            body += f"- {basis}\n"
        body += "\n"

    # Padrões analíticos
    patterns = entry.get("patterns", [])
    if patterns:
        body += generate_patterns_section(patterns)
        body += "\n"

    body += generate_synthesis_sections(entry)

    # Lacunas investigativas
    if entry.get("lacuna_investigativa"):
        body += generate_lacunas_section(entry.get("lacuna_investigativa"))

    # Análise
    if entry.get("analise"):
        body += generate_analysis_section(entry.get("analise"), title)

    # Fontes externas
    sources = entry.get("sources", [])
    if sources:
        body += generate_sources_section(sources)
        body += "\n"

    # Referências internas (connections + connects_to_main_ids)
    connections = entry.get("connections") or []
    main_ids = entry.get("connects_to_main_ids") or entry.get("connections_main_track") or []
    all_connections = list(connections) + [
        f"id_{mid}" if not str(mid).startswith("id") else str(mid) for mid in main_ids
    ]

    if all_connections:
        body += generate_connections_section(all_connections, entry_id)
        body += "\n"

    # Rodapé
    body += "---\n\n"
    body += f"*Entrada gerada automaticamente • Série O Dragão e a Onça • {batch_name}*\n"

    # Escrita do arquivo
    full_content = frontmatter + body

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_content)
        return str(filepath.relative_to(ROOT)), f"✅ Gerado: {filename}"
    except Exception as e:
        return "", f"❌ Erro ao escrever {filename}: {str(e)}"


def process_batch_file(batch_file: Path) -> Tuple[int, int, list[dict]]:
    """
    Processa um arquivo JSON de batch.
    Retorna (total_processado, total_com_sucesso, assuntos_para_lawfare)
    """
    try:
        with open(batch_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Erro ao ler {batch_file.name}: {e}")
        return 0, 0, []

    if isinstance(data, list):
        data = {"entries": data}

    entries = extract_entries_from_batch(data, batch_file)
    is_thematic = batch_file.name.startswith("lawfare-thematic-")
    assuntos_raw = list(data.get("assuntos") or []) if not is_thematic else []
    if not entries:
        print(f"⚠️  Nenhuma entrada em {batch_file.name}")
        return 0, 0, []

    batch_name = batch_file.stem
    success_count = 0

    print(f"\n📄 Processando {batch_file.name} ({len(entries)} entradas)...")

    for entry in entries:
        filepath, status_msg = generate_post_from_entry(entry, batch_name, batch_file)
        if filepath:
            print(f"   {status_msg}")
            success_count += 1
            if not is_thematic:
                assuntos_raw.append(entry_to_assunto(entry, filepath))
        else:
            print(f"   {status_msg}")

    return len(entries), success_count, assuntos_raw


def merge_lawfare_assuntos(assuntos: list[dict]) -> int:
    if not assuntos or not LAWFARE.is_file():
        return 0
    lf = json.loads(LAWFARE.read_text(encoding="utf-8"))
    items = lf.get("assuntos") or []
    new_ids = {int(a["id"]) for a in assuntos if a.get("id") is not None}
    items = [a for a in items if a.get("id") not in new_ids]
    items.extend(assuntos)
    items.sort(key=lambda x: x.get("id") or 0)
    lf["assuntos"] = items
    lf["total"] = len(items)
    lf["data_extração"] = date.today().isoformat()
    datas = [a["data_evento"] for a in items if a.get("data_evento") and a["data_evento"] != "0001-01-01"]
    if datas:
        lf["periodo"] = f"{min(datas)} a {max(datas)}"
    LAWFARE.write_text(json.dumps(lf, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"lawfare.json: +{len(assuntos)} assuntos (total {len(items)})")
    return len(assuntos)


def update_sync_json(main_ids: list[int], thematic_ids: list[int], batch_names: list[str]) -> None:
    if not SYNC.is_file():
        return
    sync = json.loads(SYNC.read_text(encoding="utf-8"))
    note = f"Dragão e a Onça merge {date.today().isoformat()}: {', '.join(batch_names[:5])}{'…' if len(batch_names) > 5 else ''}"
    if main_ids:
        last = max(main_ids)
        main = sync.setdefault("tracks", {}).setdefault("main", {})
        main["last_id"] = last
        main["next_available"] = last + 1
        main["last_confirmed"] = last
        main["last_jekyll_published"] = last
        main["last_produced"] = last
        main["last_session_produced"] = last
        main.setdefault("confirmed_batches", []).append({
            "range": [min(main_ids), last],
            "status": "confirmed",
            "notes": note,
        })
    if thematic_ids:
        last_t = max(thematic_ids)
        th = sync.setdefault("tracks", {}).setdefault("thematic", {})
        prev_last = int(th.get("last_id") or 0)
        if last_t < prev_last:
            last_t = prev_last
        th["last_id"] = last_t
        th["next_available"] = last_t + 1
        entries = th.setdefault("entries", [])
        existing = {int(e["id"]) for e in entries}
        for tid in thematic_ids:
            if tid not in existing:
                entries.append({
                    "id": tid,
                    "status": "confirmed",
                    "topic": f"T-{tid} dragao-onca",
                    "artifact": f"2026-07-24-t{tid}-dragao-onca.md",
                    "notes": note,
                })
        entries.sort(key=lambda x: int(x["id"]))
    st = sync.setdefault("sync_status", {})
    st["main_track_last_sync"] = date.today().isoformat()
    st["thematic_track_last_sync"] = date.today().isoformat()
    st["dragao_onca_series_sync"] = f"{date.today().isoformat()}T12:00:00-03:00"
    if main_ids:
        st.setdefault("ids_confirmed_total", {})["main_track"] = str(max(main_ids))
    SYNC.write_text(json.dumps(sync, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("claude.ai-corpus-ids-sync.json atualizado.")


def archive_todo_files(files: list[Path]) -> None:
    PROC_DIR.mkdir(parents=True, exist_ok=True)
    for src in files:
        if not src.is_file():
            continue
        dst = PROC_DIR / src.name
        if dst.is_file():
            dst.unlink()
        shutil.move(str(src), str(dst))
        print(f"  archive -> processados/{src.name}")


def main():
    """Função principal."""
    print("=" * 70)
    print("🐉 Gerador de Artigos — Série O Dragão e a Onça")
    print("=" * 70)

    # Verificar diretórios
    if not TODO_DIR.exists():
        print(f"❌ Diretório não encontrado: {TODO_DIR}")
        return

    # Listar arquivos JSON
    batch_files = sorted(
        p for p in TODO_DIR.glob("lawfare-batch-dragao-onca-*.json")
    )
    thematic_files = sorted(
        p for p in TODO_DIR.glob("lawfare-thematic-*.json")
        if " (1)" not in p.name
    )

    all_files = batch_files + thematic_files

    if not all_files:
        print(f"⚠️  Nenhum arquivo JSON encontrado em {TODO_DIR}")
        return

    print(f"\n🔍 Encontrados {len(all_files)} arquivos JSON")
    print(f"   - {len(batch_files)} batches main track")
    print(f"   - {len(thematic_files)} capítulos temáticos")

    total_processed = 0
    total_success = 0
    all_assuntos: list[dict] = []
    main_ids: list[int] = []
    thematic_ids: list[int] = []
    processed_files: list[Path] = []

    for batch_file in all_files:
        processed, success, assuntos = process_batch_file(batch_file)
        total_processed += processed
        total_success += success
        if success:
            processed_files.append(batch_file)
        if assuntos:
            all_assuntos.extend(assuntos)
            main_ids.extend(int(a["id"]) for a in assuntos if a.get("id") is not None)
        if batch_file.name.startswith("lawfare-thematic-"):
            try:
                data = json.loads(batch_file.read_text(encoding="utf-8"))
                tid = parse_thematic_id(data.get("id"))
                if tid is not None:
                    thematic_ids.append(tid)
            except json.JSONDecodeError:
                pass

    if all_assuntos:
        merge_lawfare_assuntos(all_assuntos)
    if main_ids or thematic_ids:
        update_sync_json(main_ids, thematic_ids, [p.name for p in processed_files])
    if processed_files:
        print("\n📦 Arquivando JSON processados...")
        archive_todo_files(processed_files)

    # Resumo final
    print("\n" + "=" * 70)
    print("📊 RESUMO DA GERAÇÃO")
    print("=" * 70)
    print(f"✅ Total processado: {total_processed} entradas")
    print(f"✅ Total com sucesso: {total_success} artigos")

    if total_processed > 0:
        success_rate = (total_success / total_processed) * 100
        print(f"📈 Taxa de sucesso: {success_rate:.1f}%")

    print(f"📁 Artigos salvos em: {POSTS_DIR.relative_to(ROOT)}")
    print("=" * 70)


if __name__ == "__main__":
    main()
