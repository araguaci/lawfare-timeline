# Notas locais · `_data/todo/`

**Último processamento:** 2026-07-22 (1636–1638 + enrich 1633)

## Snapshot

| Track | Last | Próximo |
|-------|------|---------|
| Main | **1638** | **1639** |
| Thematic | **227** | **T-228** |
| Historical pre-1990 | PREC-1930-07 | 14 · T-224 |
| Historical pos-1990 | PREC-1997-05 | 1 |

Validação: **0 erros** · `pwsh -File tools/validate-ids.ps1`

## Rodada 22/07

- **1636** Lula Catalão (traidores/enforcamento)
- **1637** Notícia-crime Flávio × Lula (STF)
- **1638** Lula repete PDT (20/jul)
- **STF PVTAC** → duplicata **1633** (PVTAC/embargos absorvidos no post existente)

## Main recente (1633–1638)

1633 PVTAC · 1634 supersalários · 1635 Gritzbach · 1636–1638 cluster Lula/Flávio

## Fila

*(vazio)* — próximo **1639+** ou **T-228**

## Pipeline

```bash
python scripts/sync_todo_current.py
python tools/reconcile_lawfare_batch.py
python tools/sync_corpus_ids.py
pwsh -File tools/validate-ids.ps1
```

Detalhes: `TODO.md` · `docs/TODO.md`
