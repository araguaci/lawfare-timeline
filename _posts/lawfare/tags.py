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
                try:
                    return yaml.safe_load(frontmatter_str)
                except yaml.YAMLError as e:
                    print(f"Erro ao parsear YAML em {file_path}: {e}")
                    return None
    return None

def main(directory):
    """Processa arquivos .md, extrai tags únicas e cria arquivos de tags."""
    tags_set = set()
    md_files = list(Path(directory).glob('*.md'))
    
    for file in md_files:
        frontmatter = extract_frontmatter(file)
        if frontmatter and 'tags' in frontmatter:
            # Supondo que tags seja uma string ou lista; trata como lista
            tags = [frontmatter['tags']] if isinstance(frontmatter['tags'], str) else frontmatter['tags']
            for tag in tags:
                normalized_tag = tag.strip()
                if normalized_tag:
                    tags_set.add(normalized_tag)
    
    for tag in tags_set:
        slug = sanitize_filename(tag)
        # Title: primeiras letras uppercase, replace - por espaço
        title = ' '.join(word.capitalize() for word in slug.split('-'))
        
        content = f"""---
layout: tag-list
type: tag
title: {title}
slug: {slug}
category: lawfare
sidebar: true
description: >
   Artigos relacionados com {title}
---
"""
        output_file = Path(directory) / f"{slug}.md"
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