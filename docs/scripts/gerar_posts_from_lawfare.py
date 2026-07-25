#!/usr/bin/env python3
"""
Gera posts Jekyll (_posts/) automaticamente a partir de _data/lawfare.json
Versão: 2026-05-04
Autor: Grok (para Lawfare Timeline)
"""

import json
import os
import re
import unicodedata
from datetime import datetime
from pathlib import Path

# ===================== CONFIG =====================
ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "_data" / "lawfare-mare-liberum-timeline.json"
POSTS_DIR = ROOT / "_posts"

CATEGORY_MAP = {
    # Categorias diretas do lawfare.json
    "lawfare": "lawfare",
    "stf": "stf",
    "tse": "tse",
    "bancos": "bancos",
    "indecoro": "indecoro",
    "dossie": "dossie",
    "crise-diplomatica": "crise-diplomatica",
    "decano": "decano",
    "escandalos": "escandalos",
    "estudos": "estudos",
    "extravagancia": "extravagancia",
    "geral": "lawfare",
    "governo": "governo",
    "impunidade": "impunidade",
    "justica": "justica",
    "operacoes": "operacoes",
    "penduricalhos": "penduricalhos",
    "vazatoga": "vazatoga",
    # Aliases e variações comuns
    "perseguicao-institucional": "stf",
    "captura-institucional": "stf",
    "interferencia-externa": "lawfare",
    "registro-analitico": "dossie",
    "banco-master": "bancos",
    "crise": "crise-diplomatica",
    "diplomatica": "crise-diplomatica",
    "operacao": "operacoes",
    "escandalo": "escandalos",
}

IMAGE_MAP = {
    "stf": "/assets/solid/gavel.svg",
    "lawfare": "/assets/solid/scale-balanced.svg",
    "bancos": "/assets/solid/landmark.svg",
    "indecoro": "/assets/solid/exclamation-triangle.svg",
    "dossie": "/assets/solid/file-shield.svg",
    "crise-diplomatica": "/assets/solid/globe.svg",
    "decano": "/assets/solid/user-tie.svg",
    "escandalos": "/assets/solid/bomb.svg",
    "estudos": "/assets/solid/book.svg",
    "extravagancia": "/assets/solid/gem.svg",
    "governo": "/assets/solid/sitemap.svg",
    "impunidade": "/assets/solid/lock-open.svg",
    "justica": "/assets/solid/hammer.svg",
    "operacoes": "/assets/solid/crosshairs.svg",
    "penduricalhos": "/assets/solid/coins.svg",
    "tse": "/assets/solid/check-to-slot.svg",
    "vazatoga": "/assets/solid/user-secret.svg",
}

DEFAULT_IMAGE = "/assets/solid/circle-exclamation.svg"


def slugify(text: str, max_len: int = 80) -> str:
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text).strip('-')
    return text[:max_len].rstrip('-')


def format_date(date_str: str) -> str:
    if not date_str:
        return "2026-01-01T12:00:00.000Z"
    try:
        if len(date_str) >= 10:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00")[:19])
            return dt.strftime("%Y-%m-%dT12:00:00.000Z")
        return f"{date_str}T12:00:00.000Z"
    except:
        return "2026-01-01T12:00:00.000Z"


def resolve_category(entry: dict) -> str:
    cat = (entry.get("categoria") or "").lower()
    tags = [t.lower() for t in entry.get("tags", [])]
    title = (entry.get("titulo") or "").lower()

    for key, folder in CATEGORY_MAP.items():
        if key in cat or key in tags or key in title:
            return folder

    # fallback inteligente
    if any(k in title or k in cat for k in ["moraes", "gilmar", "toffoli", "stf", "supremo"]):
        return "stf"
    if any(k in title or k in cat for k in ["banco master", "master", "cdb", "fgc", "financeiro"]):
        return "bancos"
    if any(k in title or k in cat for k in ["diplomacia", "sancao", "visto", "eua", "trump"]):
        return "crise-diplomatica"
    if any(k in title or k in cat for k in ["operacao", "pf", "policia federal"]):
        return "operacoes"
    if any(k in title or k in cat for k in ["eleicao", "eleitoral", "tse", "urna"]):
        return "tse"
    if any(k in title or k in cat for k in ["salario", "penduricalho", "beneficio", "supersalario"]):
        return "penduricalhos"
    if any(k in title or k in cat for k in ["vazamento", "toga", "vazatoga"]):
        return "vazatoga"
    if any(k in title or k in cat for k in ["decano", "celso de mello", "marco aurelio"]):
        return "decano"
    if any(k in title or k in cat for k in ["impunidade", "soltura", "liberacao"]):
        return "impunidade"
    if any(k in title or k in cat for k in ["extravagancia", "luxo", "gastos"]):
        return "extravagancia"
    if any(k in title or k in cat for k in ["escandalo", "corrupcao", "fraude"]):
        return "escandalos"
    return "lawfare"


def generate_post(entry: dict):
    title = entry.get("titulo", "Sem título").strip()
    date_event = entry.get("data_evento") or entry.get("data_iso", "")[:10]
    cat_folder = resolve_category(entry)
    slug = slugify(title)
    filename = f"{date_event}-{slug}.md"

    target_dir = POSTS_DIR / cat_folder
    target_dir.mkdir(parents=True, exist_ok=True)
    filepath = target_dir / filename

    desc_short = (entry.get("descricao") or "")[:250].replace('"', "'").replace('\n', ' ')
    tags = entry.get("tags", [])
    if isinstance(tags, str):
        tags = [tags]

    image_path = IMAGE_MAP.get(cat_folder, DEFAULT_IMAGE)

    frontmatter = f"""---
title: "{title}"
description: "{desc_short}..."
date: {format_date(entry.get("data_iso") or date_event)}
image:
  path: "{image_path}"
tags: {json.dumps(tags, ensure_ascii=False)}
categories: {cat_folder}
timeline_id: {entry.get("id")}
---

- &nbsp;
{{:toc .large-only}}

# ⚖️ {title}

***

## 🧭 Resumo

{entry.get("descricao", "Sem descrição disponível.")}

**Relevância:** {entry.get("relevancia", "média").title()}  
**Prioridade:** {entry.get("prioridade", 2)}

"""

    # Corpo adicional
    body = f"""
## 📋 Detalhes do Evento

**Pessoas envolvidas:** {', '.join(entry.get('pessoas_envolvidas', [])) or '—'}  
**Instituições:** {', '.join(entry.get('instituicoes_envolvidas', [])) or '—'}

## 🔗 Fontes

"""
    for fonte in entry.get("fontes", []):
        body += f"- {fonte}\n"

    body += f"""
---

**ID do registro:** {entry.get("id")}  
**Categoria analítica:** {entry.get("categoria")}  
**Meta:** {json.dumps(entry.get("meta", {}), ensure_ascii=False, indent=2)}
"""

    full_content = frontmatter + body

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(full_content)

    print(f"✅ Gerado: {filepath.relative_to(ROOT)}")


# ===================== MAIN =====================
def main():
    if not DATA_FILE.exists():
        print(f"❌ Arquivo não encontrado: {DATA_FILE}")
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    entries = data.get("assuntos", []) if isinstance(data, dict) else data

    print(f"🔄 Processando {len(entries)} registros...")
    for entry in entries:
        if isinstance(entry, dict) and entry.get("id") and entry.get("titulo"):
            generate_post(entry)

    print("\n🎉 Geração concluída!")


if __name__ == "__main__":
    main()