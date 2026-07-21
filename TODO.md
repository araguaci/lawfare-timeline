# Próximos passos · lawfare-timeline

**Atualizado:** 2026-07-20 (varredura 1631–1634 + T-226 · colisão 1635→1621)

> Espelho: `docs/TODO.md` · Notas: `_data/todo/todo.md` · Legado: `docs/TODO-LEGACY.md`

---

## Snapshot

| Track | Last | Próximo | Validação |
|-------|------|---------|-----------|
| Main | **1634** | **1635** | **0 erros** |
| Thematic | **T-226** | **T-227** | gaps 1449–1480 permanentes |
| Historical | PREC-1930-07 | — | 14 entradas sidecar |
| Fila `_data/todo/` | vazio | — | — |

---

## Rodada varredura 08–20/jul ✅ (20/07/2026)

| ID | Evento | Padrão |
|----|--------|--------|
| 1631 | Bruno Dantas / licitação R$ 1 bi Porto Santos | P05/P07/P09/P11 |
| 1632 | ACX ITC → ministra STM Sterman R$ 700 mil (laranja) | P08/P10 |
| 1633 | STF libera parte dos penduricalhos (30/06) | P11/P03 |
| 1634 | Moraes/Dino 48h supersalários 7 TJs | P11/P06 |
| T-226 | Ciclo do Penduricalho — P11 Judiciário mar–jul/2026 | P11 |

**Colisão resolvida:** id_1635 (Moraes/Bolsonaro 17/07) → **patch id_1621** (oitiva Flávio 28/07). id_1628 USTR não reproduzido.

Batch: `_data/processados/lawfare-batch-1631-1635-varredura-jul2026.json`

---

## Rodadas anteriores (jul/2026)

| Faixa | Conteúdo |
|-------|----------|
| 1629–1630 + T-225 | UK CPIN PCC/CV · efetivo PCC 20k vs 100k · GI-TOC |
| T-224 | Sidecar PREC-* (14 entradas, PREC-1891-14) |
| 1620–1628 | Master · Hawala · HK · CPI · RJ · USTR |
| Taxonomia 18/07 | Dashboard v3.3 · P06-B · P10/P11 · P13 arquivado |

---

## Pendências abertas

| Item | Prioridade |
|------|------------|
| Posts PREC individuais (14 slugs) | Baixa |
| Formalizar P04b em METHODOLOGY | Média |
| Archive.org espelhamento (1663 URLs) | Média |
| P11-B Judiciário (T-226) — formalizar subpattern | Média |
| Recuperação shadowban @araguaci | Externa |

---

## Comandos

```bash
python scripts/sync_todo_current.py
python tools/sync_corpus_ids.py
pwsh -File tools/validate-ids.ps1
```

---

## Referências

- Corpus: `_data/lawfare.json` (1597 entradas · ID 1–1634)
- Sync: `_data/claude.ai-corpus-ids-sync.json`
- [lawfare-timeline.vercel.app](https://lawfare-timeline.vercel.app)
