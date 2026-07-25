import json
import argparse
import unicodedata
import urllib.parse
from datetime import datetime

def sanitize_filename(text):
    """Sanitiza o texto para uso em nomes de arquivos: remove especiais, normaliza acentos, converte para lowercase, substitui espaços por hifens."""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = text.lower()
    text = text.replace(' ', '-')
    text = ''.join(c for c in text if c.isalnum() or c in ['_', '-'])
    while '--' in text:
        text = text.replace('--', '-')
    while '__' in text:
        text = text.replace('__', '_')
    return text.strip('_-')

parser = argparse.ArgumentParser(description='Gera arquivos Markdown a partir de um JSON de eventos.')
parser.add_argument('json_file', type=str, help='Caminho para o arquivo JSON de entrada.')

args = parser.parse_args()

with open(args.json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    data_original = item.get('data', '')
    acao = item.get('acao', '')
    descricao_completa = item.get('descricao_completa', '')
    violacao = item.get('violacao', [])
    envolvidos = item.get('envolvidos', [])
    fontes = item.get('fontes', [])
    year = item.get('year', 0)
    gravidade = item.get('gravidade', 'não definido')
    faicon = item.get('faicon', 'fa-question-circle')
    tags = item.get('tags', [])  # Adicionado para ler tags do JSON
    
    # Converte data para filename
    try:
        parsed_date = datetime.strptime(data_original, '%Y/%m/%d')
        data_evento = parsed_date.strftime('%Y-%m-%d')
    except ValueError:
        data_evento = sanitize_filename(data_original.replace('/', '-'))
    
    # Trunca acao
    positions = [pos for pos in [acao.find('.'), acao.find(',')] if pos != -1]
    truncated_acao = acao[:min(positions)].strip() if positions else acao.strip()
    safe_acao = sanitize_filename(truncated_acao)
    filename = f"{data_evento}-{safe_acao}.md"
    
    # Query de busca
    search_query = ' ' + acao + ' ' + descricao_completa + ' ' + ' '.join(violacao) + ' ' + str(year) + ' gravidade ' + gravidade
    encoded_query = urllib.parse.quote(search_query)
    
    # Tags: violacao + envolvidos + gravidade + tags do JSON
    sanitized_violacoes = [sanitize_filename(v) for v in violacao]
    sanitized_envolvidos = [sanitize_filename(e) for e in envolvidos]
    sanitized_gravidade = sanitize_filename(f"gravidade-{gravidade}")
    sanitized_tags = [sanitize_filename(t) for t in tags]  # Sanitiza tags do JSON
    all_tags = sanitized_violacoes + sanitized_envolvidos + [sanitized_gravidade] + sanitized_tags
    escaped_tags = ["'" + tag.replace("'", "''") + "'" for tag in all_tags if tag]
    tags_yaml = f"tags: [{', '.join(escaped_tags)}]" if escaped_tags else "tags: []"
    
    # Formata listas
    violacao_str = '\n'.join(f"  - {v}" for v in violacao) if violacao else "  - Nenhuma violação listada"
    envolvidos_str = '\n'.join(f"  - {e}" for e in envolvidos) if envolvidos else "  - Nenhum envolvido listado"
    fontes_str = '\n'.join(f"  - [{f}]({f})" if f.startswith('http') else f"  - {f}" for f in fontes) if fontes else "  - Nenhuma fonte listada"
    
    # Determina a classe do prompt com base na gravidade
    if gravidade == 'alta':
        prompt_class = 'danger'
    elif gravidade == 'media':
        prompt_class = 'warning'
    elif gravidade == 'baixa':
        prompt_class = 'info'
    else:
        prompt_class = 'tip'  # Default para casos não definidos
    
    # Formata a seção de descrição com base na gravidade
    descricao_section = f"> {descricao_completa}\n{{: .prompt-{prompt_class} }}" if descricao_completa else ""
    
    gravidade_section = f"- **Gravidade**: **{gravidade}** <i class=\"fas {faicon}\"></i>\n"

    fontawesome = faicon.replace('fa-', '')  # Remove prefixo 'fa-' para usar no caminho da imagem
    fontawesome = fontawesome.replace('fa ', '')  # Substitui espaços por hifens
    fontawesome = fontawesome.replace('fas ', '')  # Substitui espaços por hifens
    data_evento = data_evento.replace('/', '-')

    tags_yaml = tags_yaml.replace('crise diplomatica', 'crise-diplomatica')  # Substitui espaços por hifens

    content = f"""---
published: {data_evento}
title: "{acao}"
category: crise-diplomatica
description: > 
  "{descricao_completa}"
faicon: {faicon}
{tags_yaml}
image: "/assets/solid/{fontawesome}.svg"
---

# Ação em {data_original} com violações, envolvidos, fontes e gravidade {gravidade}

{descricao_section}

## Detalhes
- **Data**: {data_original}
- **Ano**: {year}
{gravidade_section}
- **Violações**:
{violacao_str}
- **Envolvidos**:
{envolvidos_str}
- **Fontes**:
{fontes_str}

## Análise por IA
- [🤖 Investigar com IA](https://www.perplexity.ai/search?q={encoded_query})

## Links Relacionados
- [🌐🔍 Busca no Google para o título e descrição](https://www.google.com/search?q={encoded_query})
- [📖🔍 Busca na Wikipedia para o título e descrição](https://pt.wikipedia.org/w/index.php?search={encoded_query})

"""
    
    with open(filename, 'w', encoding='utf-8') as md_file:
        md_file.write(content)