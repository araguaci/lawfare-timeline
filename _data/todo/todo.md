# Notas locais · `_data/todo/`

**Último processamento:** 2026-07-20 (1629–1630 + T-225)

## Snapshot IDs (canônico)

| Track | Last | Próximo | Fonte |
|-------|------|---------|-------|
| Main | **1630** | **1631** | `lawfare.json` + sync JSON |
| Thematic | **225** | **T-226** | `_posts/estudos/` |
| Historical | **PREC-1930-07** | — | `precedentes-republica.json` (14 entradas) |

Validação: `pwsh -File tools/validate-ids.ps1` · Sync: `python tools/sync_corpus_ids.py`

## Main track recente (1620–1630)

| ID | Evento |
|----|--------|
| 1620 | Auditorias Master/Reag (P10) |
| 1621 | Moraes/Milei |
| 1622 | Hawala |
| 1623 | Consulado HK (P02) |
| 1624 | Revisão criminal Bolsonaro |
| 1625 | CPI CO (P06-B) |
| 1626–1627 | Sucessão RJ / Fux (P03) |
| 1628 | USTR +25% Pix/STF |
| 1629 | UK CPIN PCC/CV (P10) |
| 1630 | Efetivo PCC 20k vs 100k (ev-contested, P04) |

## Fila

| Arquivo | Status |
|---------|--------|
| *(vazio)* | Aguardando batch JSON |
| `proposta-padrao-P13.md` | Arquivado |

## Pipeline

```bash
python scripts/sync_todo_current.py
python tools/sync_corpus_ids.py
pwsh -File tools/validate-ids.ps1
```

## Colisões resolvidas

| Batch | → ID |
|-------|------|
| USTR 1609 | 1628 |
| CPI 1624 | 1625 |
| RJ 1577/1580 | 1626–1627 |

Detalhes e histórico: `TODO.md` (raiz) · espelho `docs/TODO.md`
