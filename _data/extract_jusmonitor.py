import json, re

with open('lawfare.json', encoding='utf-8') as f:
    data = json.load(f)

assuntos = data['assuntos']
sync_date = data['data_extração']

keywords = ['venda-de-sentencas','corrupcao-judicial','cnj','desembargador','judiciario',
            'magistrado','aposentadoria-compulsoria','vazatoga','vaza-toga']

def relevant(e):
    if e.get('categoria') in ('justica','vazatoga'):
        return True
    if e.get('tipo_escandalo') == 'Judiciário':
        return True
    tags = e.get('tags', [])
    if any(k in tags for k in keywords):
        return True
    return False

filtered = [e for e in assuntos if relevant(e)]
good = [e for e in filtered if e.get('descricao') and e['descricao'] not in ('', '>', 'N/A') and len(e['descricao']) > 20]
excluded = [e for e in filtered if e not in good]

def classify(e):
    tags = e.get('tags', [])
    cat = e.get('categoria')
    if 'venda-de-sentencas' in tags or 'corrupcao-judicial' in tags:
        return 'corrupcao_judicial'
    if cat == 'penduricalhos':
        return 'penduricalhos'
    if cat in ('stf', 'vazatoga'):
        return 'chokepoint_stf'
    if cat == 'tse':
        return 'eleitoral_tse'
    if cat == 'justica':
        if 'cnj' in tags or 'aposentadoria-compulsoria' in tags or 'assedio-sexual' in tags:
            return 'cnj_disciplinar'
        return 'outros_judiciario'
    return 'outros_judiciario'

def evidence_status(e):
    fontes = e.get('fontes', [])
    real = [s for s in fontes if s and s != 'N/A']
    if len(real) >= 2:
        return 'ev-confirmed'
    if len(real) == 1:
        return 'ev-confirmed'  # fonte primária/jornalística única já curada no corpus
    return 'ev-alleged'

cards = []
for e in good:
    real_sources = [s for s in e.get('fontes', []) if s and s != 'N/A']
    cards.append({
        'id': e.get('id'),
        'data': e.get('data_iso', '')[:10],
        'titulo': e.get('titulo', '').strip(),
        'descricao': e.get('descricao', '').strip(),
        'grupo': classify(e),
        'gravidade': next((t.replace('gravidade-', '') for t in e.get('tags', []) if t.startswith('gravidade-')), None),
        'relevancia': e.get('relevancia'),
        'instituicoes': e.get('instituicoes_envolvidas', []),
        'tags': [t for t in e.get('tags', []) if not t.startswith('gravidade-')],
        'fontes': real_sources,
        'evidence_status': evidence_status(e),
        'valor_envolvido': e.get('valor_envolvido') if e.get('valor_envolvido') not in ('N/A', None) else None,
    })

cards.sort(key=lambda c: c['data'], reverse=True)

print('total cards:', len(cards))
from collections import Counter
print(Counter(c['grupo'] for c in cards))
print(Counter(c['evidence_status'] for c in cards))
print('excluded (data gap, pending enrichment):', len(excluded))

with open('jusmonitor_data.json', 'w', encoding='utf-8') as f:
    json.dump({'gerado_de': 'lawfare.json', 'sync_date': sync_date, 'total': len(cards),
               'excluidos_pendente_enriquecimento': len(excluded), 'cards': cards}, f, ensure_ascii=False, indent=1)
