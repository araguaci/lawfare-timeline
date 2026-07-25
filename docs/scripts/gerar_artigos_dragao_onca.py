#!/usr/bin/env python3
"""
Gera posts Jekyll (_posts/dragao-onca/) automaticamente a partir dos batches JSON
da série "O Dragão e a Onça" localizados em _data/todo/

Versão: 2026-07-24
Autor: Claude Code
Propósito: Converter dados estruturados JSON em artigos MD com referências, links internos e assets
"""

import json
import os
import re
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote

# ===================== CONFIG =====================
ROOT = Path(__file__).resolve().parents[1]
TODO_DIR = ROOT / "_data" / "todo"
POSTS_DIR = ROOT / "_posts" / "dragao-onca"
ASSETS_DIR = ROOT / "assets" / "img"

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
    "sintese": "dragao-onca-sintese.webp",
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
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


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

def generate_post_from_entry(entry: Dict, batch_name: str) -> Tuple[str, str]:
    """
    Gera um post Jekyll (arquivo .md) a partir de uma entry JSON.
    Retorna (filepath, status_message)

    Suporta dois formatos:
    1. Batch entries (com 'date', 'summary', etc.)
    2. Thematic entries (com 'topic', 'notes', 'artifact', etc.)
    """
    entry_id = str(entry.get("id", "")).strip()

    # Suporte para ambos os formatos
    title = entry.get("title") or entry.get("topic", "Sem título")
    title = title.strip()

    if not entry_id or not title:
        return "", f"⚠️  Entrada incompleta: ID ou título faltando"

    # Componentes do arquivo
    date_event = entry.get("date", "")[:10]

    # Para temáticos: usar 'artifact' se disponível, ou slugify do topic
    if not date_event and entry.get("artifact"):
        # Temático: usar artifact como base para nome
        artifact_name = entry.get("artifact", "").replace(".html", "")
        filename = f"2026-07-24-t{entry_id}-{artifact_name}.md"
    else:
        # Batch: padrão normal
        slug = slugify(title)
        filename = f"{date_event}-id{entry_id}-{slug}.md"

    # Criação do diretório
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    filepath = POSTS_DIR / filename

    # Frontmatter
    description = yaml_escape((entry.get("summary") or entry.get("notes", ""))[:200])
    year = extract_year(date_event)
    image_path = resolve_region_image(batch_name)

    # Tags baseadas em categoria e padrões
    tags = [entry.get("category", "dragao-onca"), year]
    if "patterns" in entry and entry["patterns"]:
        tags.extend(entry["patterns"][:2])  # Primeiros 2 padrões
    tags = [tag for tag in tags if tag]

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
    connections = entry.get("connections", [])
    main_ids = entry.get("connects_to_main_ids", [])
    all_connections = connections + [f"id_{mid}" for mid in main_ids]

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


def process_batch_file(batch_file: Path) -> Tuple[int, int]:
    """
    Processa um arquivo JSON de batch.
    Retorna (total_processado, total_com_sucesso)
    """
    try:
        with open(batch_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Erro ao ler {batch_file.name}: {e}")
        return 0, 0

    entries = data.get("entries", [])
    if not entries:
        print(f"⚠️  Nenhuma entrada em {batch_file.name}")
        return 0, 0

    batch_name = batch_file.stem
    success_count = 0

    print(f"\n📄 Processando {batch_file.name} ({len(entries)} entradas)...")

    for entry in entries:
        filepath, status_msg = generate_post_from_entry(entry, batch_name)
        if filepath:
            print(f"   {status_msg}")
            success_count += 1
        else:
            print(f"   {status_msg}")

    return len(entries), success_count


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
    batch_files = sorted(TODO_DIR.glob("lawfare-batch-dragao-onca-*.json"))
    thematic_files = sorted(TODO_DIR.glob("lawfare-thematic-*.json"))

    all_files = batch_files + thematic_files

    if not all_files:
        print(f"⚠️  Nenhum arquivo JSON encontrado em {TODO_DIR}")
        return

    print(f"\n🔍 Encontrados {len(all_files)} arquivos JSON")
    print(f"   - {len(batch_files)} batches temáticos")
    print(f"   - {len(thematic_files)} batches geográficos")

    # Processar cada arquivo
    total_processed = 0
    total_success = 0

    for batch_file in all_files:
        processed, success = process_batch_file(batch_file)
        total_processed += processed
        total_success += success

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
