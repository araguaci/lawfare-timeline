# Próximos passos · lawfare-timeline

**Atualizado:** 2026-08-19 (merge 1857–1864 + T-253/T-254; colisões resolvidas)

> Espelho: `docs/TODO.md` · Notas: `_data/processados/todo.md` · Legado: `docs/TODO-LEGACY.md`

---

## Snapshot

| Track | Last | Próximo | Validação |
|-------|------|---------|-----------|
| Main | **1864** | **1865** | lawfare.json **1825** entradas |
| Thematic | **T-254** | **T-255** | sync 100–254 |
| Dragão e a Onça | **1770** / **T-246** | — | `dragao-onca.json` **151** |
| Fila `_data/todo/` | staging HTML/MD | — | JSON arquivado 19/08 |

---

## Rodada 19/08/2026 ✅ — Fila 1857–1864 + T-253/T-254

Colisões evitadas:

| Conflito | Resolução |
|----------|-----------|
| **1857** ×3 (revisões do filtro X) | Canônico = revisão 5 / arquivo `(2)` |
| **T-253** ×2 | AP 470 permanece **T-253**; P13 Porta Giratória → **T-254** |
| Main 1857–1864 vs corpus | Livres (last era **1856**) |

| Faixa | Conteúdo |
|-------|----------|
| **1857** | X Brazil2026ElectionFilter (P12-B) |
| **1858** | Mendonça / IterCast — competência penal originária |
| **1859–1860** | Baptista Júnior / Airbus + filho na AEL |
| **1861–1864** | Âncoras P13 (Burnier, Campos Neto, Faria/BTG, agregada 67%) |
| **T-253** | AP 470 — critério evidencial STF |
| **T-254** | P13 Porta Giratória (proposta de promoção) |

**Script:** `scripts/merge_todo_queue_1857_1864.py`

---

## Pendências abertas

| Item | Prioridade |
|------|------------|
| Formalizar **P13 Porta Giratória** em METHODOLOGY.md (T-254; distinto do P13 arquivado 18/07) | Média |
| Formalizar P04b em METHODOLOGY | Média |
| Renomear estudos mislabel `T-1512`/`T-1765`/`T-1766` → faixa T-255+ | Baixa |
| Gap main **1820** (editorial → T-248) | Informativo |
| Jonathan Macedo (SP) — 2ª fonte | Baixa |
| Staging `todo/p13-porta-giratoria.html` + `prompt-tratamento-pdfs-mensalao.md` | Baixa |
| `bundle exec jekyll build` | Rodar após esta rodada |

---

## Comandos

```bash
python scripts/reassign_todo_batch_ids.py   # antes de sync, se batch conflitar
python scripts/sync_todo_current.py
python tools/sync_corpus_ids.py
pwsh -File tools/validate-ids.ps1
bundle exec jekyll build
```

---

## Referências

- Corpus: `_data/lawfare.json` (**1825** entradas · main até **1864**)
- Unified: `_data/lawfare-unified-corpus.json`
- Sidecar dragão: `_data/dragao-onca.json` (151 · **1763/1764** = CEEE-T / JMEV intactos)
- Hold resolvido: `_data/processados/README-hold-resolvido-1749-1768.md`
