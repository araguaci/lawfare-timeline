# Próximos passos · lawfare-timeline

**Atualizado:** 2026-07-21 (1635 Gritzbach + T-227 + PREC-1997-05 · reconcile 1631–1634)

> Espelho: `docs/TODO.md` · Notas: `_data/todo/todo.md` · Legado: `docs/TODO-LEGACY.md`

---

## Snapshot

| Track | Last | Próximo | Validação |
|-------|------|---------|-----------|
| Main | **1635** | **1636** | **0 erros** |
| Thematic | **T-227** | **T-228** | gaps 1449–1480 permanentes |
| Historical pre-1990 | PREC-1930-07 | — | 14 entradas · T-224 |
| Historical pos-1990 | PREC-1997-05 | — | 1 entrada · sidecar |
| Fila `_data/todo/` | vazio | — | — |

---

## Rodada 21/07/2026 ✅

| ID | Evento | Padrão / track |
|----|--------|----------------|
| 1635 | Júri Gritzbach anulado (PMs / delator PCC) | P02/P06 |
| T-227 | P04 pela Direita — espelhos P04b (OBS) | P04/P04b |
| PREC-1997-05 | Privatização Vale R$ 3,3 bi | sidecar pos-1990 · P05/P09 |

**Reconcile:** IDs 1631–1634 reintegrados em `lawfare.json` (posts já existiam; sync divergia).

**Colisão evitada:** id_1635 (Gritzbach) ≠ id_1635 Bolsonaro (batch jul/2020 rejeitado → patch 1621).

---

## Main track recente (1631–1635)

| ID | Evento |
|----|--------|
| 1631 | Bruno Dantas / Porto Santos R$ 1 bi |
| 1632 | ACX ITC / Sterman STM |
| 1633 | STF penduricalhos (30/06) |
| 1634 | Moraes/Dino supersalários 48h |
| 1635 | Júri Gritzbach anulado |

---

## Pendências abertas

| Item | Prioridade |
|------|------------|
| Posts PREC individuais | Baixa |
| Formalizar P04b em METHODOLOGY | Média |
| P11-B Judiciário (T-226) | Média |
| Archive.org espelhamento | Média |
| Índice temático pos-1990 PREC | Baixa |

---

## Comandos

```bash
python scripts/sync_todo_current.py
python tools/reconcile_lawfare_batch.py   # se posts existem sem lawfare.json
python tools/sync_corpus_ids.py
pwsh -File tools/validate-ids.ps1
```

---

## Referências

- Corpus: `_data/lawfare.json` (1598 entradas · ID 1–1635)
- Sidecars: `precedentes-republica.json` · `precedentes-pos-1990.json`
- [lawfare-timeline.vercel.app](https://lawfare-timeline.vercel.app)
