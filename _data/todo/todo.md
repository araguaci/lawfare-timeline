# Notas locais · `_data/todo/`

**Último processamento:** 2026-07-20 (1631–1634 + T-226)

## Snapshot

| Track | Last | Próximo |
|-------|------|---------|
| Main | **1634** | **1635** |
| Thematic | **226** | **T-227** |
| Historical | PREC-1930-07 | 14 entradas |

Validação: `pwsh -File tools/validate-ids.ps1` → **0 erros**

## Main recente (1629–1634)

| ID | Evento |
|----|--------|
| 1629 | UK CPIN PCC/CV |
| 1630 | Efetivo PCC 20k vs 100k |
| 1631 | Dantas / Porto Santos R$ 1 bi |
| 1632 | ACX ITC / Sterman STM |
| 1633 | STF penduricalhos (30/06) |
| 1634 | Moraes/Dino supersalários 48h |

## Colisão resolvida

**1635** → patch **1621** (oitiva Flávio 28/07). Demais elementos já em 1621.

## Fila

*(vazio)* — próximo batch → **1635+** ou **T-227**

## Pipeline

```bash
python scripts/sync_todo_current.py
python tools/sync_corpus_ids.py
pwsh -File tools/validate-ids.ps1
```

Detalhes: `TODO.md` · `docs/TODO.md`
