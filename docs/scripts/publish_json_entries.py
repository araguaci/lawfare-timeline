import json
import os
import re
from datetime import datetime
import unicodedata

def slugify(text):
    # Remove accents
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text).strip('-')
    return text

def format_date(date_str):
    if not date_str: return ""
    try:
        # Try YYYY-MM-DD
        dt = datetime.strptime(date_str[:10], "%Y-%m-%d")
        return dt.strftime("%Y-%m-%dT12:00:00.000Z")
    except:
        return date_str

def create_post(entry, category_map=None):
    title = entry.get('titulo', 'Sem Título')
    date_val = entry.get('data') or entry.get('data_evento') or entry.get('data_iso')
    if not date_val: date_val = "2026-04-15"
    
    # Extract date for filename
    date_part = date_val[:10]
    slug = slugify(title)
    filename = f"{date_part}-{slug}.md"
    
    category = entry.get('categoria')
    operacao = entry.get('operacao', '')
    
    if not category:
        if any(keyword in operacao for keyword in ["Vaza Toga", "AP 2720", "Caso Tagliaferro"]):
            category = "vazatoga"
        elif any(keyword in operacao or keyword in title for keyword in ["Inquerito", "STF", "Moraes", "Gilmar", "Tofoli"]):
            category = "stf"
        elif any(keyword in title for keyword in ["CDBs", "Master"]):
            category = "bancos"
        else:
            category = "lawfare"
            
    if category_map and category in category_map:
        category = category_map[category]
    
    # Ensure category directory exists
    target_dir = os.path.join("_posts", category)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
    
    filepath = os.path.join(target_dir, filename)
    
    # Frontmatter
    tags = entry.get('tags', [])
    if isinstance(tags, str): tags = [tags]
    
    image_path = "/assets/solid/file-shield.svg"
    if category == "vazatoga": image_path = "/assets/solid/shield-virus.svg"
    elif category == "stf": image_path = "/assets/solid/gavel.svg"
    elif category == "lawfare": image_path = "/assets/solid/scale.svg"
    elif category == "bancos": image_path = "/assets/solid/landmark.svg"

    desc = entry.get('descricao', '')[:200].replace('"', "'")
    content = f"""---
title: "{title}"
description: "{desc}..."
date: {format_date(date_val)}
image:
  path: "{image_path}"
tags: {tags}
categories: {category}
---

- &nbsp;
{{:toc .large-only}}

# ⚖️📁 {title}

***

## 🧭 Resumo

{entry.get('descricao', '')}

**Impacto:** {entry.get('impacto', 'N/A').title()}  
**Status:** {entry.get('status', 'N/A')}

***

## 🏁 Introdução

{entry.get('descricao', '')}

## 📊 Análise

"""
    # Dimensions / Analysis
    dims = entry.get('dimensoes', {})
    if isinstance(dims, dict):
        for dim_name, dim_text in dims.items():
            if dim_text:
                content += f"### Dimensão {dim_name.title()}\n\n{dim_text}\n\n"
    
    # Actors
    atores = entry.get('atores', [])
    if atores:
        content += "### Pessoas e Instituições Envolvidas\n\n"
        for ator in atores:
            if isinstance(ator, dict):
                content += f"- **{ator.get('nome')}**: {ator.get('papel')} ({ator.get('status')})\n"
            else:
                content += f"- {ator}\n"
        content += "\n"

    # Lacunas
    lacuna = entry.get('lacuna_investigativa', '')
    if lacuna:
        content += f"### Lacuna Investigativa\n\n{lacuna}\n\n"

    # Conclusion
    content += "## 🎯 Conclusão\n\n"
    content += entry.get('analise_editorial', 'Análise em andamento.') + "\n\n"

    # Sources
    sources = entry.get('fontes', [])
    if sources:
        content += "## Referências\n\n"
        for src in sources:
            if isinstance(src, dict):
                content += f"- [{src.get('veiculo', 'Link')}]({src.get('url', '#')}) - {src.get('descricao', '')}\n"
            else:
                content += f"- {src}\n"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {filepath}")

# Category Mapping
cat_map = {
    "falha_institucional": "stf",
    "corrupção_regulatória": "bancos",
    "investigação_parlamentar": "lawfare",
    "analise_editorial": "dossie",
    "lacuna_investigativa": "dossie",
    "stf": "stf",
    "vazatoga": "vazatoga",
    "lawfare": "lawfare",
    "cpi": "stf"
}

# Process files
files = [
    "_data/entries-153-158.json",
    "_data/lawfare-timeline-entry-160.json",
    "_data/lawfare-timeline-entries-153-159.json",
    "_data/lawfare-1441-1447.json"
]

for fpath in files:
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                for entry in data:
                    create_post(entry, cat_map)
            else:
                create_post(data, cat_map)
