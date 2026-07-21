# Notas locais · `_data/todo/`

**Último processamento:** 2026-07-21 (1635 + T-227 + PREC-1997-05)

## Snapshot

| Track | Last | Próximo |
|-------|------|---------|
| Main | **1635** | **1636** |
| Thematic | **227** | **T-228** |
| Historical pre-1990 | PREC-1930-07 | 14 · T-224 |
| Historical pos-1990 | PREC-1997-05 | 1 |

Validação: **0 erros** · `pwsh -File tools/validate-ids.ps1`

## Reconcile 21/07

Posts 1631–1634 existiam; `lawfare.json` parava em 1630 → `tools/reconcile_lawfare_batch.py` (+4 sem recriar posts).

## Main recente (1631–1635)

1631 Dantas · 1632 ACX/STM · 1633 penduricalhos · 1634 supersalários · **1635 Gritzbach**

## Fila

*(vazio)* — próximo **1636+** ou **T-228**

## Pipeline

```bash
python scripts/sync_todo_current.py
python tools/reconcile_lawfare_batch.py   # se necessário
python tools/sync_corpus_ids.py
pwsh -File tools/validate-ids.ps1
```

Detalhes: `TODO.md` · `docs/TODO.md`
