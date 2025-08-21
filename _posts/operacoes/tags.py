import os
import argparse
import yaml
from pathlib import Path
import unicodedata

def sanitize_filename(text):
    """Sanitiza o texto para uso em nomes de arquivos: remove especiais, normaliza acentos, converte para lowercase, substitui espaços por hifens."""
    # Normaliza para remover acentos
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    # Converte para lowercase
    text = text.lower()
    # Substitui espaços por hifens
    text = text.replace(' ', '-')
    # Mantém apenas alfanuméricos, _ e -
    text = ''.join(c for c in text if c.isalnum() or c in ['_', '-'])
    # Remove múltiplos hifens ou sublinhados consecutivos
    while '--' in text:
        text = text.replace('--', '-')
    while '__' in text:
        text = text.replace('__', '_')
    # Remove prefixos e sufixos indesejados
    return text.strip('_-')

def extract_frontmatter(file_path):
    """Extrai o frontmatter YAML de um arquivo Markdown."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if content.startswith('---'):
            end = content.find('---', 3)
            if end != -1:
                frontmatter_str = content[3:end].strip()
                return yaml.safe_load(frontmatter_str)
    return None

def main(directory):
    """Processa arquivos .md, extrai tags únicas e cria arquivos de tags."""
    tags_set = set()
    md_files = list(Path(directory).glob('*.md'))

    for file in md_files:
        # Filtra arquivos com prefixo de data (ex.: 1990- ou 2025-)
        if file.name[:4].isdigit() and (file.name.startswith('19') or file.name.startswith('20')):
            frontmatter = extract_frontmatter(file)
            if frontmatter and 'tags' in frontmatter:
                for tag in frontmatter['tags']:
                    normalized_tag = tag.lower().strip()
                    if normalized_tag:
                        tags_set.add(normalized_tag)

    for tag in tags_set:
        slug = sanitize_filename(tag)
        title = ' '.join(word.capitalize() for word in tag.split())
        if 'ambiental' in tag:
            title = 'Crimes Ambientais'
            desc = 'Operações contra Crimes Ambientais'
        else:
            desc = f'Operações relacionadas a {title}'

        content = f"""---
layout: tag-list
type: tag
title: {title}
slug: {slug}
category: operacoes
sidebar: true
description: >
   {desc}
---
"""
        output_file = "D:/app_aragua/jekyll-theme-deepdive/_featured_tags/" / f"{slug}.md"
        if not output_file.exists():
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Arquivo criado: {output_file}")
        else:
            print(f"Arquivo {output_file} já existe, pulando.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analisa arquivos .md e cria arquivos de tags.')
    parser.add_argument('directory', type=str, nargs='?', default='.', help='Diretório contendo arquivos .md.')
    args = parser.parse_args()
    main(args.directory)
