import json
import os
import argparse
import unicodedata
import urllib.parse
from datetime import datetime

def sanitize_filename(text):
    text = unicodedata.normalize('NFKD', str(text)).encode('ascii', 'ignore').decode('utf-8')
    text = text.lower().replace(' ', '-')
    text = ''.join(c for c in text if c.isalnum() or c in ['_', '-'])
    while '--' in text:
        text = text.replace('--', '-')
    return text.strip('_-')

FAICON_MAP = {
    'diplomatico':  'fa-globe',
    'vexame':       'fa-theater-masks',
    'gastos':       'fa-money-bill-wave',
    'corrupcao':    'fa-hand-holding-usd',
}

PROMPT_CLASS_MAP = {
    'alta':  'danger',
    'medio': 'warning',
    'media': 'warning',
    'baixo': 'info',
    'baixa': 'info',
}

parser = argparse.ArgumentParser(description='Gera arquivos Markdown Jekyll a partir de JSON de crise diplomática.')
parser.add_argument('json_file', help='Caminho para o arquivo JSON de entrada.')
parser.add_argument('--output-dir', default='crise-diplomatica', help='Diretório de saída (padrão: crise-diplomatica)')
args = parser.parse_args()

with open(args.json_file, 'r', encoding='utf-8') as f:
    root = json.load(f)

# Suporta tanto {"assuntos": [...]} quanto array direto
if isinstance(root, dict):
    data = root.get('assuntos', [])
    data_pesquisa = root.get('data_pesquisa', '')
    periodo = root.get('periodo', '')
else:
    data = root
    data_pesquisa = ''
    periodo = ''

os.makedirs(args.output_dir, exist_ok=True)

for item in data:
    item_id              = item.get('id', '')
    titulo               = item.get('titulo', '')
    data_evento_str      = item.get('data_evento', '')
    categoria            = item.get('categoria', 'crise-diplomatica')
    tags                 = item.get('tags', [])
    descricao            = item.get('descricao', '')
    relevancia           = item.get('relevancia', 'nao-definido')
    impacto_diplomatico  = item.get('impacto_diplomatico', '')
    tipo_escandalo       = item.get('tipo_escandalo', '')
    fontes               = item.get('fontes', [])
    pessoas_envolvidas   = item.get('pessoas_envolvidas', [])
    instituicoes         = item.get('instituicoes_envolvidas', [])
    pais                 = item.get('pais', '')
    valor_envolvido      = item.get('valor_envolvido', 'N/A')
    prioridade           = item.get('prioridade', 0)

    # Parse da data e extração do ano
    try:
        parsed_date = datetime.strptime(data_evento_str, '%Y-%m-%d')
        data_formatada = parsed_date.strftime('%Y-%m-%d')
        year = parsed_date.year
    except ValueError:
        data_formatada = data_evento_str.replace('/', '-')
        year = data_evento_str[:4] if data_evento_str else ''

    # Ícone FontAwesome derivado do tipo_escandalo
    faicon = FAICON_MAP.get(tipo_escandalo, 'fa-exclamation-circle')
    fontawesome = faicon.replace('fa-', '')

    # Nome do arquivo: data + primeiras palavras do título
    positions = [pos for pos in [titulo.find(':'), titulo.find(',')] if pos != -1]
    truncated = titulo[:min(positions)].strip() if positions else titulo[:70].strip()
    safe_titulo = sanitize_filename(truncated)
    filename = os.path.join(args.output_dir, f"{data_formatada}-{safe_titulo}.md")

    # Query para links de busca
    search_query = f"{titulo} {descricao} {tipo_escandalo} {year}"
    encoded_query = urllib.parse.quote(search_query)

    # Monta tags YAML: tags do JSON + pessoas + relevância
    sanitized_tags     = [sanitize_filename(t) for t in tags]
    sanitized_pessoas  = [sanitize_filename(p) for p in pessoas_envolvidas]
    sanitized_rel      = sanitize_filename(f"relevancia-{relevancia}")
    all_tags = sanitized_tags + sanitized_pessoas + [sanitized_rel]
    escaped_tags = ["'" + t.replace("'", "''") + "'" for t in all_tags if t]
    tags_yaml = f"tags: [{', '.join(escaped_tags)}]" if escaped_tags else "tags: []"

    # Formata listas para o corpo do artigo
    pessoas_str      = '\n'.join(f"  - {p}" for p in pessoas_envolvidas) or "  - Nenhuma pessoa listada"
    instituicoes_str = '\n'.join(f"  - {i}" for i in instituicoes) or "  - Nenhuma instituição listada"
    fontes_str       = '\n'.join(
        f"  - [{f}]({f})" if f.startswith('http') else f"  - {f}"
        for f in fontes
    ) or "  - Nenhuma fonte listada"

    # Bloco de destaque com nível de gravidade
    prompt_class = PROMPT_CLASS_MAP.get(relevancia, 'tip')
    descricao_section = f"> {descricao}\n{{: .prompt-{prompt_class} }}" if descricao else ""

    content = f"""---
layout: post
title: "{titulo}"
categories: {categoria}
description: >
  "{descricao}"
faicon: {faicon}
relevancia: {relevancia}
impacto_diplomatico: {impacto_diplomatico}
tipo_escandalo: {tipo_escandalo}
pais: "{pais}"
valor_envolvido: "{valor_envolvido}"
prioridade: {prioridade}
{tags_yaml}
image:
  path: "/assets/solid/{fontawesome}.svg"
---

# {titulo}

{descricao_section}

## Detalhes

- **ID**: {item_id}
- **Data**: {data_formatada}
- **Ano**: {year}
- **Categoria**: {categoria}
- **Relevância**: **{relevancia}** <i class="fas {faicon}"></i>
- **Impacto Diplomático**: {impacto_diplomatico}
- **Tipo de Escândalo**: {tipo_escandalo}
- **País**: {pais}
- **Valor Envolvido**: {valor_envolvido}
- **Prioridade**: {prioridade}

## Pessoas Envolvidas

{pessoas_str}

## Instituições Envolvidas

{instituicoes_str}

## Fontes

{fontes_str}

## Análise por IA

- [🤖 Investigar com IA](https://www.perplexity.ai/search?q={encoded_query})

## Links Relacionados

- [🌐🔍 Busca no Google](https://www.google.com/search?q={encoded_query})
- [📖🔍 Busca na Wikipedia](https://pt.wikipedia.org/w/index.php?search={encoded_query})

"""

    with open(filename, 'w', encoding='utf-8') as md_file:
        md_file.write(content)

    print(f"Gerado: {filename}")

print(f"\nTotal: {len(data)} arquivos gerados em '{args.output_dir}/'")
if data_pesquisa:
    print(f"Data da pesquisa: {data_pesquisa}  |  Período: {periodo}")
