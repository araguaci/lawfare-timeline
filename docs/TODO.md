# Próximos passos · lawfare-timeline

**Atualizado:** 2026-07-22 (1636–1638 Lula/enforcamento · 1633 enriquecido PVTAC)

> Espelho: `docs/TODO.md` · Notas: `_data/todo/todo.md` · Legado: `docs/TODO-LEGACY.md`

---

## Snapshot

| Track | Last | Próximo | Validação |
|-------|------|---------|-----------|
| Main | **1638** | **1639** | **0 erros** |
| Thematic | **T-227** | **T-228** | gaps 1449–1480 permanentes |
| Historical pre-1990 | PREC-1930-07 | — | 14 entradas · T-224 |
| Historical pos-1990 | PREC-1997-05 | — | 1 entrada · sidecar |
| Fila `_data/todo/` | vazio | — | — |

---

## Rodada 22/07/2026 ✅

| ID | Evento | Padrão / track |
|----|--------|----------------|
| 1636 | Lula associa Flávio a "traidores" + enforcamento (Catalão, 02/jun) | escândalos |
| 1637 | Flávio protocola notícia-crime contra Lula no STF (11/jun) | P03 · stf |
| 1638 | Lula repete enforcamento de "traidores" na convenção PDT (20/jul) | escândalos |
| — | STF PVTAC batch → **duplicata id_1633** (enriquecimento, sem novo ID) | penduricalhos |

---

## Main track recente (1633–1638)

| ID | Evento |
|----|--------|
| 1633 | STF libera penduricalhos + PVTAC (30/06) — enriquecido |
| 1634 | Moraes/Dino supersalários 48h |
| 1635 | Júri Gritzbach anulado |
| 1636 | Lula "traidores/enforcamento" Catalão |
| 1637 | Notícia-crime Flávio × Lula |
| 1638 | Lula repete enforcamento PDT |

---

## Pendências abertas

| Item | Prioridade |
|------|------------|
| Posts PREC individuais | Baixa |
| Formalizar P04b em METHODOLOGY | Média |
| P11-B Judiciário (T-226) | Média |
| Archive.org espelhamento | Média |
| Índice temático pos-1990 PREC | Baixa |
| Desfecho notícia-crime 1637 (relator STF) | Média |

---

## Comandos

```bash
python scripts/sync_todo_current.py
python tools/reconcile_lawfare_batch.py   # se posts existem sem lawfare.json
python tools/sync_corpus_ids.py          # exporta sync → Google Drive se configurado
python tools/gdrive_sync_export.py       # export manual
pwsh -File tools/validate-ids.ps1
```

---

## Referências

- Corpus: `_data/lawfare.json` (1601 entradas · ID 1–1638)
- Sidecars: `precedentes-republica.json` · `precedentes-pos-1990.json`
- [lawfare-timeline.vercel.app](https://lawfare-timeline.vercel.app)
