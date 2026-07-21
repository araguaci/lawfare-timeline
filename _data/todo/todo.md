# Notas locais · `_data/todo/`

**Último processamento:** 2026-07-19 (Sidecar PREC-* + T-224)

## Snapshot IDs (canônico)

| Track | Last | Próximo | Fonte de verdade |
|-------|------|---------|------------------|
| Main | **1628** | **1629** | `_data/lawfare.json` + `claude.ai-corpus-ids-sync.json` |
| Thematic | **224** | **T-225** | `_posts/estudos/` (`id_corpus: T-NNN`) |
| Historical | **PREC-1930-07** | — | `_data/precedentes-republica.json` (sidecar) |

Validação: `pwsh -File tools/validate-ids.ps1` · Sync IDs: `python tools/sync_corpus_ids.py`

## Main track recente (1620–1628)

| ID | Evento |
|----|--------|
| 1620 | Auditorias Master/Reag (P10) |
| 1621 | Moraes/Milei — domiciliar Bolsonaro |
| 1622 | Operação Hawala |
| 1623 | Consulado HK (P02) |
| 1624 | Revisão criminal Bolsonaro |
| 1625 | CPI Crime Organizado (P06-B) |
| 1626–1627 | Sucessão RJ / Fux (P03) |
| 1628 | USTR +25% Pix/STF (ex-colisão 1609) |

## Fila `_data/todo/` — pendente

| Arquivo | Status | Ação |
|---------|--------|------|
| *(vazio)* | — | Próximo batch numérico 2026+ → main 1629+ |
| `proposta-padrao-P13.md` | Arquivado | Referência only |

---

## ✅ Concluído: `precedentes-republica-1891-1930.json` (2026-07-19)

| Fase | Status | Artefato |
|------|--------|----------|
| 0 Gate | ✅ | Categorias PREC-1899-05 e PREC-1926-13 → `captura-institucional` |
| 1 Sidecar | ✅ | `_data/precedentes-republica.json` (**14** entradas, revisão PREC-1891-14) |
| 1 Sync track | ✅ | `tracks.historical_precedents` em sync JSON |
| 1 Arquivo | ✅ | `_data/processados/precedentes-republica-1891-1930.json` |
| 2 T-224 | ✅ | `_posts/estudos/2026-07-19-precedentes-republica-1891-1930.md` (revisão 14 entradas) |
| 3 Posts PREC | ⏸ | Opcional — 13 slugs `prec-*.md` |
| 4 Pipeline | ✅ | `sync_corpus_ids.py` + `validate-ids.ps1` → **0 erros** |

---

## Plano (referência): `precedentes-republica-1891-1930.json`

### Inventário

- **13 entradas** · namespace **`PREC-AAAA-NN`** (correto — não colide com main 1–1628)
- **Período:** 1890–1930 (Primavera Republicana / República Velha)
- **Todas** com `revisao_humana_necessaria: true` e `escopo: precedente-historico-pre-1990`
- **Metadado stale:** `_proximo_id_main_track_conhecido: 1577` → ignorar; canônico é **1629**

### Categorias no batch

| Categoria | N | Exemplos |
|-----------|---|----------|
| captura-institucional | 6 | Castilhos 1891, Política dos Governadores, Encilhamento |
| registro-analitico | 3 | Guerra da Degola, Potreiro das Almas, Contestado |
| lawfare *(analogia)* | 2 | Comissão Verificadora 1899, HC 1926 — **revisar rótulo** |
| perseguicao-institucional | 1 | Revolta da Vacina |

### Riscos metodológicos (antes de merge)

1. **Fontes:** várias entradas dependem de Wikipedia/Toda Matéria — reforçar com CPDOC/AN/Conjur onde possível
2. **Lawfare retroativo:** PREC-1899-05 e PREC-1926-13 usam categoria `lawfare` por analogia — decidir se mantém ou vira `captura-institucional` + nota P03/P06-B histórico
3. **Padrões Px:** arquivo declara explicitamente *não* forçar P01–P12 — correto; opcional mapear **paralelos estruturais** no estudo T-224 (não nos eventos individuais)
4. **Cross-link:** PREC-1890-11 (Encilhamento) → cluster Master/Compliance Zero (IDs 1600+, T-192) — documentar no estudo, não no main track ainda
5. **`sync_todo_current.py`:** ignora silenciosamente o wrapper (`entradas` ≠ `entries`) — seguro hoje, mas renomear para `*.staging.json` ou mover para `_data/staging/` até aprovação

### Decisão de track (escolher uma)

| Opção | Prós | Contras |
|-------|------|---------|
| **A — Sidecar** `_data/precedentes-republica.json` | Zero colisão; escopo pre-1990 explícito | Fora de `lawfare.json`; busca separada |
| **B — Thematic T-224** (estudo + posts opcionais) | Alinha com corpus-bridge; um dossie | 13 posts individuais = trabalho grande |
| **C — Main 1629–1641** | Timeline unificada | Dilui escopo 1990+; IDs consumidos sem evento contemporâneo |
| **D — Track sync `historical`** (PREC-* no sync.json) | Namespace formal no sync | Requer patch em `sync_corpus_ids.py` + validate |

**Recomendação:** **A + B** — sidecar JSON canônico + **T-224** estudo índice (`_posts/estudos/`) com tabela PREC × paralelos P03/P05/P06-B/P11. Main **1629+** reservado para eventos 2026.

### Sequência de execução (sem colisão)

```
Fase 0 — Gate
  □ Revisão humana das 13 entradas (fontes + categorias lawfare)
  □ Atualizar _proximo_id no JSON → 1629 ou remover campo
  □ Renomear para precedentes-republica-1891-1930.staging.json OU mover staging/

Fase 1 — Sidecar
  □ Extrair entradas → _data/precedentes-republica.json (schema v2.2 + campo prec_id)
  □ Registrar track em claude.ai-corpus-ids-sync.json:
      tracks.historical_precedents { last: "PREC-1930-07", entries: [...] }
  □ Arquivar batch → _data/processados/

Fase 2 — Artefato editorial (T-224)
  □ Post estudo: precedentes-republica-1891-1930 — índice + paralelos estruturais
  □ id_corpus: T-224 · categoria: estudos
  □ Diagrama opcional: linha do tempo 1890–1930 ↔ P03/P05/P11 modernos
  □ Hero gosurf / xarticle se publicar

Fase 3 — Posts evento (opcional, baixa prioridade)
  □ Só após Fase 1: 13 posts em _posts/estudos/ ou _posts/decano/
  □ Slug: prec-1899-comissao-verificadora-de-poderes.md
  □ Front matter: prec_id + sem id_corpus numérico main

Fase 4 — Sync pipeline
  □ python tools/sync_corpus_ids.py
  □ pwsh tools/validate-ids.ps1
  □ Espelhar TODO.md / docs/TODO.md
```

### Próximos main track (contemporâneos — reservar 1629+)

Não alocar IDs até batch JSON com `id` numérico explícito e `date` 2026+:

| Slot | Candidato (fila externa) | Notas |
|------|--------------------------|-------|
| 1629 | *(livre)* | Próximo evento lawfare.json |
| — | Hawala follow-ups / Moraes domiciliar jul/2026 | Ver posts STF já publicados sem ID? |

### Comandos (main track — quando houver batch numérico)

```bash
python scripts/sync_todo_current.py          # merge → lawfare.json + posts
python tools/sync_corpus_ids.py              # alinha sync file
pwsh -File tools/validate-ids.ps1            # 0 erros obrigatório
```

### Colisões já resolvidas (referência)

| Batch propôs | Ocupado por | Resolvido |
|--------------|-------------|-----------|
| 1609 USTR | OFAC Shimada 1609 | → **1628** |
| 1624 CPI CO | Bolsonaro revisão 1624 | → **1625** |
| 1577/1580 RJ | ADPF Cremesp / Virgílio | → **1626–1627** |
