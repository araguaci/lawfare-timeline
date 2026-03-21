#!/usr/bin/env python3
"""
Extrai front matter de todos os artigos (_posts/**/*.md) e gera arquivos JSON
no modelo de _data/2025-11-17.json, incluindo urlrefer.

Uso: python tools/extract_frontmatter_to_json.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Union

try:
    import yaml
except ImportError:
    print("Instale PyYAML: pip install pyyaml")
    exit(1)


# Configuração do site (de _config.yml)
SITE_URL = "https://lawfare-timeline.vercel.app"
POSTS_DIR = Path(__file__).resolve().parent.parent / "_posts"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "_data"
PERMALINK_PREFIX = "/posts/"


def parse_frontmatter(content: str) -> tuple[Union[dict, None], str]:
    """Extrai front matter YAML do conteúdo. Retorna (front_matter, corpo)."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        return None, content

    try:
        fm = yaml.safe_load(match.group(1))
        body = match.group(2).strip()
        return fm or {}, body
    except yaml.YAMLError:
        return None, content


def slug_from_filename(filepath: Path) -> str:
    """
    Extrai slug do nome do arquivo para montar a URL.
    Ex: 2025-11-17-vorcaro-troca-mensagens...md -> vorcaro-troca-mensagens...
    """
    name = filepath.stem
    # Remove prefixo YYYY-MM-DD- ou YYYY-MM-DD
    m = re.match(r'^\d{4}-\d{2}-\d{2}-?(.*)$', name)
    if m and m.group(1):
        return m.group(1)
    return name


def build_url(slug: str) -> str:
    """Monta URL completa do artigo."""
    base = SITE_URL.rstrip("/")
    path = f"{PERMALINK_PREFIX}{slug}/"
    return f"{base}{path}"


def infer_relevancia(tags: list) -> str:
    """Inferir relevância a partir de tags como 'gravidade-alta'."""
    if not tags:
        return "media"
    tags_lower = [t.lower() if isinstance(t, str) else "" for t in tags]
    if "gravidade-alta" in tags_lower or "gravidadealta" in tags_lower:
        return "alta"
    if "gravidade-baixa" in tags_lower or "gravidadebaixa" in tags_lower:
        return "baixa"
    return "media"


def extract_refs_from_body(body: str) -> list[str]:
    """Tenta extrair links da seção Referências do corpo."""
    refs = []
    # Padrão: - [texto](url) ou * [texto](url)
    for m in re.finditer(r'\]\((https?://[^)\s]+)\)', body):
        refs.append(m.group(1))
    return refs


def artigo_to_assunto(
    filepath: Path,
    fm: dict,
    body: str,
    assunto_id: int,
) -> dict:
    """
    Converte front matter + metadados em um item do modelo 'assunto'.
    """
    slug = slug_from_filename(filepath)
    urlrefer = build_url(slug)

    title = fm.get("title") or ""
    if isinstance(title, str):
        titulo = title.strip()
    else:
        titulo = str(title)

    date_val = fm.get("date")
    if date_val:
        if hasattr(date_val, "strftime"):
            data_evento = date_val.strftime("%Y-%m-%d")
            data_iso = date_val.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        elif isinstance(date_val, str):
            try:
                dt = datetime.fromisoformat(date_val.replace("Z", "+00:00"))
                data_evento = dt.strftime("%Y-%m-%d")
                data_iso = dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            except ValueError:
                data_evento = date_val[:10] if len(date_val) >= 10 else ""
                data_iso = date_val
        else:
            data_evento = ""
            data_iso = ""
    else:
        # Fallback: data do nome do arquivo
        m = re.match(r'^(\d{4}-\d{2}-\d{2})', filepath.stem)
        if m:
            data_evento = m.group(1)
            data_iso = f"{data_evento}T00:00:00.000Z"
        else:
            data_evento = ""
            data_iso = ""

    cats = fm.get("categories")
    if isinstance(cats, str):
        categoria = cats
    elif isinstance(cats, list):
        categoria = cats[0] if cats else ""
    else:
        categoria = str(cats) if cats else ""

    tags = fm.get("tags") or []
    if isinstance(tags, str):
        tags = [tags] if tags else []
    tags = [str(t) for t in tags]

    desc = fm.get("description") or ""
    descricao = desc.strip() if isinstance(desc, str) else str(desc)

    fontes = extract_refs_from_body(body)

    assunto = {
        "id": assunto_id,
        "titulo": titulo,
        "data_evento": data_evento,
        "data_iso": data_iso,
        "categoria": categoria,
        "tags": tags,
        "descricao": descricao,
        "relevancia": infer_relevancia(tags),
        "urlrefer": urlrefer,
        "fontes": fontes,
        "pessoas_envolvidas": [],
        "instituicoes_envolvidas": [],
        "pais": "Brasil",
        "prioridade": assunto_id,
    }
    return assunto


def collect_posts() -> list[tuple[Path, dict, str]]:
    """Coleta todos os .md em _posts e retorna (path, front_matter, body)."""
    results = []
    for path in sorted(POSTS_DIR.rglob("*.md")):
        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Erro ao ler {path}: {e}")
            continue
        fm, body = parse_frontmatter(content)
        if fm is None:
            continue
        results.append((path, fm, body))
    return results


def main():
    posts = collect_posts()
    print(f"Encontrados {len(posts)} artigos.")

    assuntos = []
    for i, (path, fm, body) in enumerate(posts, start=1):
        assunto = artigo_to_assunto(path, fm, body, i)
        assuntos.append(assunto)

    # Agrupar por data para gerar um JSON por dia (como 2025-11-17.json)
    by_date = {}
    for a in assuntos:
        d = a["data_evento"] or "sem-data"
        by_date.setdefault(d, []).append(a)

    # Renumerar ids e prioridade dentro de cada arquivo por data
    for data, itens in by_date.items():
        for j, item in enumerate(itens, start=1):
            item["id"] = j
            item["prioridade"] = j
        output_file = OUTPUT_DIR / f"{data}.json"
        payload = {
            "assuntos": itens,
            "total": len(itens),
            "data_pesquisa": datetime.now().strftime("%Y-%m-%d"),
            "periodo": data,
        }
        output_file.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"  {output_file.name}: {len(itens)} assunto(s)")

    # Também gerar um JSON consolidado com TODOS os artigos
    payload_all = {
        "assuntos": assuntos,
        "total": len(assuntos),
        "data_pesquisa": datetime.now().strftime("%Y-%m-%d"),
        "periodo": f"todos os artigos",
    }
    all_file = OUTPUT_DIR / "lawfare-artigos-todos.json"
    all_file.write_text(
        json.dumps(payload_all, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nArquivo consolidado: {all_file.name} ({len(assuntos)} artigos)")


if __name__ == "__main__":
    main()
