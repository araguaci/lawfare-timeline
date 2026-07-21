# Próximos passos · lawfare-timeline

**Atualizado:** 2026-07-20 (batch UK CPIN 1629–1630 + T-225)

> Espelho canônico: `docs/TODO.md` · Notas operacionais: `_data/todo/todo.md` · Legado social: `docs/TODO-LEGACY.md`

---

## Snapshot

| Track | Last | Próximo | Status |
|-------|------|---------|--------|
| Main | **1630** | **1631** | UK CPIN + correção efetivo PCC |
| Thematic | **T-225** | **T-226** | GI-TOC 8/10 mafia-style, resiliência 4,92/10 |
| Historical | **PREC-1930-07** | — | 14 entradas sidecar |
| Fila `_data/todo/` | — | — | vazio (exc. notas) |
| Validação | — | — | **0 erros** (gaps 1449–1480, 1506–1510 permanentes) |

---

## Fila editorial

| Arquivo | Status |
|---------|--------|
| *(vazio)* | Próximo batch → main **1631+** ou T-226 |
| `proposta-padrao-P13.md` | Arquivado (referência) |

---

## Rodadas recentes (jul/2026)

### 1629–1630 + T-225 ✅ (20/07/2026)

| ID | Evento | Padrão |
|----|--------|--------|
| 1629 | UK Home Office CPIN — PCC/CV (missão campo set/2024) | P10 |
| 1630 | Correção efetivo PCC: 20k núcleo vs 100k agregado (ev-contested) | P04 |
| T-225 | GI-TOC — 8/10 mafia-style, resiliência 4,92/10 | P10/P11 |

Batch: `_data/processados/lawfare-batch-pcc-cv-ukcpin-1629-1630-T225.json`

### T-224 sidecar PREC-* ✅ (19/07/2026)

14 precedentes 1890–1930 · lacuna **PREC-1891-14** (Castilhos) · índice `_posts/estudos/2026-07-19-precedentes-republica-1891-1930.md`

### Faixa 1620–1628 ✅ (18–19/07/2026)

1620 Master/Reag (P10) · 1621 Moraes/Milei · 1622 Hawala · 1623 Consulado HK (P02) · 1624 Bolsonaro revisão · 1625 CPI CO (P06-B) · 1626–1627 RJ/Fux (P03) · 1628 USTR/Pix

### Taxonomia ✅ (18/07/2026)

Dashboard **v3.3** · METHODOLOGY **v2.4** · P06-B formalizado · P10 autônomo vs P11 · P13 arquivado

---

## Colisões resolvidas (referência)

| Batch propôs | Ocupado por | → |
|--------------|-------------|---|
| 1609 USTR | OFAC Shimada | **1628** |
| 1624 CPI | Bolsonaro revisão | **1625** |
| 1577/1580 RJ | Cremesp / Virgílio | **1626–1627** |
| 1520/176 | P04b imprensa / Bolsonaro | 1520 restaurado · **1624** |

---

## Pendências abertas

| Item | Prioridade | Notas |
|------|------------|-------|
| Posts PREC individuais (14 slugs) | Baixa | Fase 3 T-224 — opcional |
| Formalizar P04b em METHODOLOGY | Média | Proposta documentada |
| Archive.org espelhamento | Média | `tools/archive_org_mirror.py` — 1663 URLs |
| Recuperação shadowban @araguaci | Externa | — |
| X Article jul/2026 | ✅ | `artigos/corpus-julho-7-20-2026-xarticle.md` |

Histórico completo T-180–T-223: ver commits e `_data/processados/`.

---

## Comandos

```bash
python scripts/sync_todo_current.py    # merge batch _data/todo/*.json
python tools/sync_corpus_ids.py        # alinha sync file
pwsh -File tools/validate-ids.ps1      # gate: 0 erros obrigatório
```

---

## Referências

- Sync: `_data/claude.ai-corpus-ids-sync.json`
- Corpus: `_data/lawfare.json` (1593 entradas · ID 1–1630)
- Sidecar: `_data/precedentes-republica.json`
- Portal: [lawfare-timeline.vercel.app](https://lawfare-timeline.vercel.app)
- Dashboard: [gosurf.site/padroes-sistemicos-dashboard](https://gosurf.site/padroes-sistemicos-dashboard)
