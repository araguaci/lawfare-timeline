#!/usr/bin/env python3
"""
Extrai artigos de _posts e gera JSON com estrutura similar a lawfare-ataques-bolsonaro-apoiadores.json.

Requer apenas Python 3.10+ (stdlib). Processa front matter YAML e corpo Markdown para extrair:
titulo, data_evento, categoria, tags, descricao, impacto_diplomatico, tipo_escandalo,
valor_envolvido, fontes (URLs de Referencias), pessoas_envolvidas, instituicoes_envolvidas.

Uso:
    python scripts/extrair_posts_para_json.py
    python scripts/extrair_posts_para_json.py --output _data/posts-extraidos.json
    python scripts/extrair_posts_para_json.py --posts-dir _posts --limit 10
    python scripts/extrair_posts_para_json.py --no-pretty   # JSON compacto
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime


def _relpath(filepath: Path, base: Path) -> str:
    """Retorna caminho relativo ou nome do arquivo."""
    try:
        return str(filepath.relative_to(base))
    except ValueError:
        return filepath.name


def parse_front_matter(content: str) -> tuple[dict, str]:
    """Extrai front matter YAML e retorna (dict, corpo)."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        return {}, content

    fm_str, body = match.groups()
    front = {}

    # Parse simples de YAML para campos comuns
    for line in fm_str.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            key, _, val = line.partition(':')
            key = key.strip().lower()
            val = val.strip()
            if val.startswith('"') or val.startswith("'"):
                val = val[1:-1].replace('\\"', '"')
            elif val.startswith('['):
                # Tags como ['a','b'] ou ["a","b"]
                val = re.findall(r"['\"]([^'\"]+)['\"]", val)
            front[key] = val

    return front, body


def extract_date(front: dict, filepath: Path) -> tuple[str, str]:
    """Retorna (data_evento YYYY-MM-DD, data_iso)."""
    date_val = front.get('date') or front.get('date_evento')
    filename = filepath.name

    # Tenta YYYY-MM-DD no nome do arquivo
    m = re.search(r'^(\d{4}-\d{2}-\d{2})', filename)
    base = m.group(1) if m else "0001-01-01"

    if date_val and isinstance(date_val, str):
        iso_match = re.search(r'(\d{4}-\d{2}-\d{2})', str(date_val))
        if iso_match:
            base = iso_match.group(1)

    return base, f"{base}T00:00:00.000Z"


def extract_from_body(body: str) -> dict:
    """Extrai campos do corpo do artigo."""
    out = {
        'impacto_diplomatico': 'N/A',
        'tipo_escandalo': 'N/A',
        'valor_envolvido': 'N/A',
        'fontes': [],
        'pessoas_envolvidas': [],
        'instituicoes_envolvidas': []
    }

    # Resumo (entre ## 🧭 Resumo e próximo ## ou ***)
    resumo_match = re.search(
        r'##\s*🧭\s*Resumo\s*\n\s*\*?\*?\*?\s*\n(.*?)(?=\n\*{3}|\n##|\Z)',
        body, re.DOTALL | re.IGNORECASE
    )
    if resumo_match:
        resumo = resumo_match.group(1).strip()
        # Remove linhas **Impacto** e **Tipo** do resumo puro
        resumo_limpo = re.sub(r'\*\*Impacto Diplomático:\*\*\s*\S+.*', '', resumo)
        resumo_limpo = re.sub(r'\*\*Tipo de Escândalo:\*\*\s*\S+.*', '', resumo_limpo)
        resumo_limpo = re.sub(r'\*\*Valor Envolvido:\*\*\s*.*', '', resumo_limpo)
        out['resumo'] = resumo_limpo.strip() or resumo[:500]

    # Impacto Diplomático
    imp = re.search(r'\*\*Impacto Diplomático:\*\*\s*(\w+)', body, re.IGNORECASE)
    if imp:
        out['impacto_diplomatico'] = imp.group(1).strip().lower()

    # Tipo de Escândalo
    tipo = re.search(r'\*\*Tipo de Escândalo:\*\*\s*([^\n*]+)', body, re.IGNORECASE)
    if tipo:
        out['tipo_escandalo'] = tipo.group(1).strip()

    # Valor Envolvido
    val = re.search(r'\*\*Valor Envolvido:\*\*\s*([^\n*]+)', body, re.IGNORECASE)
    if val:
        out['valor_envolvido'] = val.group(1).strip()
    # Alternativa: R$ X no título ou corpo
    if out['valor_envolvido'] == 'N/A':
        vr = re.search(r'R\$\s*[\d,\.]+\s*(?:milhões|bilhões|bi|mi)?', body, re.IGNORECASE)
        if vr:
            out['valor_envolvido'] = vr.group(0)

    # Referências: URLs em ## Referências
    ref_section = re.search(
        r'##\s*Referências\s*\n(.*?)(?=\n##|\Z)',
        body, re.DOTALL | re.IGNORECASE
    )
    if ref_section:
        urls = re.findall(r'\[([^\]]+)\]\((https?://[^\)]+)\)', ref_section.group(1))
        out['fontes'] = [url for _, url in urls if not url.startswith('https://www.perplexity') 
                        and 'google.com/search' not in url and 'wikipedia.org' not in url]
        if not out['fontes']:
            out['fontes'] = [url for _, url in urls]

    # Pessoas (padrão - Nome em negrito em listas)
    pessoas = re.findall(r'-\s*\*\*([^*]+)\*\*[:\s]', body)
    if pessoas:
        out['pessoas_envolvidas'] = list(dict.fromkeys(p.strip() for p in pessoas[:15]))

    # Instituições (STF, PF, etc. mencionadas)
    instituicoes = ['STF', 'TSE', 'PF', 'PGR', 'TCU', 'CNJ', 'Câmara', 'Senado', 'INSS', 'FAB', 'Banco Central', 'BRB']
    found = []
    for inst in instituicoes:
        if inst.lower() in body.lower():
            found.append(inst)
    if found:
        out['instituicoes_envolvidas'] = found[:10]

    return out


def normalize_tags(tags) -> list:
    """Normaliza tags para lista de strings."""
    if isinstance(tags, list):
        return [str(t) for t in tags]
    if isinstance(tags, str):
        return [t.strip() for t in re.findall(r"['\"]([^'\"]+)['\"]", tags)] or tags.split(',')
    return []


def get_category(front: dict, filepath: Path, posts_dir: Path) -> str:
    """Obtém categoria do front matter ou do path."""
    cat = front.get('categories') or front.get('categoria')
    if isinstance(cat, list):
        cat = cat[0] if cat else ''
    if cat:
        return str(cat).strip()
    # Fallback: subpasta imediata sob _posts (ex: _posts/escandalos/xxx.md -> escandalos)
    try:
        rel = filepath.parent.relative_to(posts_dir)
        if rel != Path('.'):
            return rel.parts[0]
    except ValueError:
        pass
    return 'geral'


def process_post(filepath: Path, base: Path, posts_dir: Path) -> dict | None:
    """Processa um arquivo .md e retorna dict no formato do JSON alvo."""
    try:
        content = filepath.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        print(f"[AVISO] Erro ao ler {filepath}: {e}", file=sys.stderr)
        return None

    front, body = parse_front_matter(content)
    extracted = extract_from_body(body)

    data_evento, data_iso = extract_date(front, filepath)
    titulo = front.get('title') or front.get('titulo') or filepath.stem.replace('-', ' ').title()
    if isinstance(titulo, str) and (titulo.startswith('"') or titulo.startswith("'")):
        titulo = titulo[1:-1]

    descricao = front.get('description') or front.get('descricao') or extracted.get('resumo', '')[:300]
    if isinstance(descricao, str) and len(descricao) > 500:
        descricao = descricao[:500] + '...'

    categoria = get_category(front, filepath, posts_dir)
    tags = normalize_tags(front.get('tags', []))
    if categoria and categoria not in tags:
        tags.insert(0, categoria)

    assunto = {
        'titulo': titulo,
        'data_evento': data_evento,
        'data_iso': data_iso,
        'categoria': categoria,
        'tags': tags,
        'descricao': descricao,
        'relevancia': 'alta' if extracted.get('impacto_diplomatico') != 'N/A' else 'media',
        'impacto_diplomatico': extracted['impacto_diplomatico'],
        'tipo_escandalo': extracted['tipo_escandalo'],
        'fontes': extracted['fontes'] or ['N/A'],
        'pessoas_envolvidas': extracted['pessoas_envolvidas'] or [],
        'instituicoes_envolvidas': extracted['instituicoes_envolvidas'] or [],
        'pais': 'Brasil',
        'valor_envolvido': extracted['valor_envolvido'],
        'prioridade': 2,
        'fonte_arquivo': _relpath(filepath, base)
    }

    return assunto


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Extrai posts para JSON')
    parser.add_argument('--posts-dir', default='_posts', help='Diretório de posts')
    parser.add_argument('--output', '-o', default='_data/posts-extraidos.json', help='Arquivo JSON de saída')
    parser.add_argument('--limit', type=int, default=0, help='Limitar número de posts (0=ilimitado)')
    parser.add_argument('--pretty', action='store_true', default=True, help='JSON formatado (padrão: sim)')
    parser.add_argument('--no-pretty', action='store_false', dest='pretty', help='JSON compacto')
    args = parser.parse_args()

    base = Path(__file__).resolve().parent.parent
    posts_dir = base / args.posts_dir
    out_path = base / args.output

    if not posts_dir.exists():
        print(f"Erro: diretório {posts_dir} não encontrado.", file=sys.stderr)
        sys.exit(1)

    arquivos = sorted(posts_dir.rglob('*.md'), key=lambda p: (p.name, str(p)))
    if args.limit:
        arquivos = arquivos[:args.limit]

    assuntos = []
    for i, fp in enumerate(arquivos):
        item = process_post(fp, base, posts_dir)
        if item:
            item['id'] = i + 1
            assuntos.append(item)

    datas = [a['data_evento'] for a in assuntos if a['data_evento'] != '0001-01-01']
    periodo = f"{min(datas)} a {max(datas)}" if datas else "N/A"

    resultado = {
        'assuntos': assuntos,
        'total': len(assuntos),
        'data_extração': datetime.now().strftime('%Y-%m-%d'),
        'periodo': periodo,
        'fonte_original': str(posts_dir),
        'nota': 'Extraído automaticamente de _posts por scripts/extrair_posts_para_json.py'
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2 if args.pretty else None)

    print(f"Extraidos {len(assuntos)} artigos -> {out_path}")


if __name__ == '__main__':
    main()
