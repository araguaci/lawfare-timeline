#!/usr/bin/env python3
"""
Filtra lawfare.json para extrair apenas ataques de lawfare contra Bolsonaro e apoiadores.

Critérios de inclusão:
- Categoria: lawfare, dossie, vazatoga
- Ou keywords em titulo/descricao/tags: bolsonaro, censura, bloqueio, inquerito,
  X/Twitter, 8 de janeiro, Eduardo Bolsonaro, perseguição, etc.

Uso:
    python scripts/filtrar_lawfare_bolsonaro.py
    python scripts/filtrar_lawfare_bolsonaro.py --input _data/lawfare.json --output _data/lawfare-ataques-bolsonaro-apoiadores.json
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime


# Palavras-chave que indicam ataque a Bolsonaro/apoiadores (evitar termos genéricos)
KEYWORDS = [
    'bolsonaro', 'bolsonarista', 'bolsonaristas', 'eduardo bolsonaro', 'eduardo-bolsonaro',
    'bloqueio do x', 'x-twitter', 'bloqueio.*x', 'starlink', 'elon',
    'inquerito fake', 'inquérito fake', 'fake news', 'fake-news', 'atos antidemocraticos',
    '8 de janeiro', '8/1', '8-de-janeiro', 'presos 8', 'dosimetria',
    'tagliaferro', 'david agape', 'david-agape', 'eli vieira', 'eli-vieira',
    'vaza toga', 'vazatoga', 'perseguic', 'gabinete paralelo',
    'alexandre de moraes', 'alexandre-de-moraes',
    'sancoes', 'sanções', 'magnitsky', 'coacao', 'coação',
    'zambelli', 'carla zambelli', 'carlos bolsonaro', 'michelle bolsonaro',
    'weintraub', 'ramagem', 'augusto heleno', 'braga netto',
    'busca.*bolsonaro', 'minuta.*golpe'
]

# Categorias que tipicamente contêm lawfare contra Bolsonaro
CATEGORIAS_LAWFARE = {'lawfare', 'dossie', 'vazatoga', 'crise-diplomatica'}


def texto_contem_keywords(texto: str) -> bool:
    """Verifica se texto contém alguma keyword (case-insensitive)."""
    if not texto:
        return False
    txt = texto.lower()
    for kw in KEYWORDS:
        if '*' in kw:
            if re.search(kw.replace('*', '.*'), txt):
                return True
        elif kw.lower() in txt:
            return True
    return False


def tags_contem_keywords(tags: list) -> bool:
    """Verifica se tags contêm keywords relevantes."""
    if not tags:
        return False
    tags_str = ' '.join(str(t).lower() for t in tags)
    return any(kw.lower() in tags_str for kw in KEYWORDS)


def eh_ataque_bolsonaro(item: dict) -> bool:
    """
    Retorna True se o item representa ataque de lawfare contra Bolsonaro/apoiadores.
    """
    cat = (item.get('categoria') or '').lower()
    titulo = item.get('titulo') or ''
    descricao = item.get('descricao') or ''
    tags = item.get('tags') or []
    tudo = f"{titulo} {descricao}"

    # Inclui por categoria lawfare/dossie/vazatoga (foco em judicial vs oposição)
    if cat in {'lawfare', 'dossie', 'vazatoga'}:
        return True

    # crise-diplomatica: incluir se Eduardo Bolsonaro, sanções, etc.
    if cat == 'crise-diplomatica':
        return texto_contem_keywords(tudo) or tags_contem_keywords(tags)

    # Outras categorias: só incluir se (a) data >= 2018 E (b) menção explícita
    # Evita falsos positivos (CPI 1988, Caso Toninho 2005, etc.)
    data = (item.get('data_evento') or '')[:4]
    if data and data.isdigit() and int(data) < 2018:
        return False
    return texto_contem_keywords(tudo) or tags_contem_keywords(tags)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', default='_data/lawfare.json')
    parser.add_argument('--output', '-o', default='_data/lawfare-ataques-bolsonaro-apoiadores.json')
    args = parser.parse_args()

    base = Path(__file__).resolve().parent.parent
    in_path = base / args.input
    out_path = base / args.output

    if not in_path.exists():
        print(f"Erro: {in_path} nao encontrado.", file=sys.stderr)
        sys.exit(1)

    with open(in_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    assuntos = data.get('assuntos', [])
    filtrados = [it for it in assuntos if eh_ataque_bolsonaro(it)]

    # Renumerar IDs
    for i, it in enumerate(filtrados, 1):
        it['id'] = i

    datas = [a['data_evento'] for a in filtrados if a.get('data_evento') and a['data_evento'] != '0001-01-01']
    periodo = f"{min(datas)} a {max(datas)}" if datas else "N/A"

    resultado = {
        'assuntos': filtrados,
        'total': len(filtrados),
        'data_extracao': datetime.now().strftime('%Y-%m-%d'),
        'periodo': periodo,
        'fonte_original': str(in_path),
        'criterio_filtro': 'Ataques de lawfare contra Bolsonaro e apoiadores: perseguição judicial, censura digital, inquéritos, bloqueios, sanções e ações que prejudicam o ex-presidente e seus aliados.',
        'nota': f'Filtrado de {len(assuntos)} itens em lawfare.json. Critérios: categorias lawfare/dossie/vazatoga ou keywords em titulo/descricao/tags.'
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print(f"Filtrados {len(filtrados)} de {len(assuntos)} itens -> {out_path}")


if __name__ == '__main__':
    main()
