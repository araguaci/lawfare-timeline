# Próximos passos · lawfare-timeline

**Atualizado:** 2026-07-29 (batch INQ 4.781 · IDs 1777–1796)

> Espelho: `docs/TODO.md` · Notas: `_data/processados/todo.md` · Legado: `docs/TODO-LEGACY.md`

---

## Snapshot

| Track | Last | Próximo | Validação |
|-------|------|---------|-----------|
| Main | **1796** | **1797** | lawfare.json **1758** entradas |
| Dragão e a Onça | **1770** / **T-246** | **1771** / **T-247** | `dragao-onca.json` **151** · 151 posts YAML OK |
| Thematic (geral) | **T-246** | **T-247** | — |
| Historical pre-1990 | PREC-1930-07 | — | 14 entradas · T-224 |
| Historical pos-1990 | PREC-1997-05 | — | 1 entrada · sidecar |
| Fila `_data/todo/` | **vazia** | — | 2 batches em `_hold/` |

---

## Rodada 29/07/2026 (b) ✅ — Sessão INQ 4.781 + desdobramentos (1777–1796)

| Faixa | Conteúdo |
|-------|----------|
| **1777–1786** | INQ 4.781 — origem, bloqueios TSE/AEED 2022, cluster desmonetização |
| **1787–1790** | Autocensura Sivis, PF jornalista, escândalo Master/Londres (STF/STJ) |
| **1791–1796** | Magnitsky Moraes (jul/dez 2025), desdobramentos diplomáticos |

**20 posts** · batch `lawfare-batch-sessao-2026-07-29-1777-1796.json` arquivado.

---

## Rodada 29/07/2026 ✅ — Sync fila + síntese final

| Item | Entrega |
|------|---------|
| **1775–1776** | Sigilo 100 anos Vorcaro + Alcolumbre (`bancos`) — realocados após conflito com dragao-onca 1763/1764 |
| **T-1765** | Síntese P10 sigilo centenário (`estudos`) |
| **T-1766** | Ricardo Salles patrimônio TSE (`estudos`) |
| **T-243** | Síntese final cross-state atualizada (151 entradas, AP/RJ/SC, tipologia 14 mecanismos, correções MG/RS/CEEE-T) |
| **Sync** | `sync_todo_current.py` · `claude.ai-corpus-ids-sync.json` · GDrive export |
| **Build** | `bundle exec jekyll build` → `docs/` |

---

## Rodada 27/07/2026 ✅ — Amapá, RJ, SC (T-244–T-246)

| Faixa | Conteúdo |
|-------|----------|
| **1757–1759** | Amapá — Amazonbai/açaí, GACC, leilão ANP |
| **1760–1761** | Rio de Janeiro — CMPort/Vast, Castro/Hikvision |
| **1763–1770** | RS CEEE-T, SC JMEV/ferrovias/GACC, ES GWM duplo |
| **T-244–T-246** | Capítulos temáticos finais da série |

**151 posts** em `_posts/dragao-onca/`.

---

## `_hold/` — conflito de IDs (não processar automaticamente)

| Batch | Motivo |
|-------|--------|
| `lawfare-batch-lula-traidor-pvtac-1749-1752.json` | Faixa 1749–1752 já ocupada (MG/RS dragao-onca) |
| `lawfare-batch-havengate-calixto-1767-1768.json` | IDs 1767–1768 já usados (SC ferrovias/GACC) |

Ver `_data/todo/_hold/README-conflito-1749-1752.md`.

---

## Pendências abertas

| Item | Prioridade |
|------|------------|
| T-242 (ranking CEBC) | ✅ Concluído |
| Revisão editorial T-243 vs T-233 | ✅ Concluída |
| `bundle exec jekyll build` | ✅ Concluído (29/jul · batch 1777–1796) |
| Reatribuir IDs batches `_hold/` | Média |
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
python scripts/export_dragao_onca_json.py
python scripts/validate_dragao_onca_yaml.py
python tools/reconcile_lawfare_batch.py
python tools/sync_corpus_ids.py
bundle exec jekyll build
pwsh -File tools/validate-ids.ps1
```

---

## Referências

- Corpus: `_data/lawfare.json` (1758 entradas · ID 1–1796)
- Unified: `_data/lawfare-unified-corpus.json` (136 entradas verificadas)
- Sidecar dragão: `_data/dragao-onca.json` (151 assuntos · 1639–1770 + T-228–T-246)
- Sidecars: `precedentes-republica.json` · `precedentes-pos-1990.json`
- [lawfare-timeline.vercel.app](https://lawfare-timeline.vercel.app)
