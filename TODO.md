# Próximos passos · lawfare-timeline

**Atualizado:** 2026-08-20 (merge 1874–1888 Vaza Toga 5/2/3)

> Espelho: `docs/TODO.md` · Notas: `_data/processados/todo.md` · Legado: `docs/TODO-LEGACY.md`

---

## Snapshot

| Track | Last | Próximo | Validação |
|-------|------|---------|-----------|
| Main | **1888** | **1889** | lawfare.json **1849** entradas |
| Thematic | **T-254** | **T-255** | sync 100–254 |
| Dragão e a Onça | **1770** / **T-246** | — | `dragao-onca.json` **151** |
| Fila `_data/todo/` | staging HTML/MD | — | JSON 1874–1888 arquivado 20/08 |

---

## Rodada 20/08/2026 (c) ✅ — Vaza Toga 5 + 2 + 3 (IDs atrasados)

A fila reapresentou 4 batches com numeração antiga. **VT4 era duplicata** de 1869–1873 — não mergeado. VT5/VT2/VT3 realocados a partir de **1874**.

| Faixa | Batch | Conteúdo |
|-------|-------|----------|
| **1874–1876** | VT5 (era 1865–1867) | 2.119 CPFs; PET 11228 Dino; sigilo Exército |
| **1877–1882** | VT2 (era 1873–1878) | Certidões GestBio / Dia da Mulher |
| **1883–1888** | VT3 (era 1879–1884) | Fraude exposta (Constantino/Fiuza, Gettr, Zambelli, Palver) |
| — | VT4 (1868–1872) | **Skip** — já publicado como 1869–1873 |

Conexões internas apontam para os IDs reais (VT4 → 1869–1873; VT5 → 1874+). id_1865 continua sendo o PL 2630.

---

## Rodada 20/08/2026 (b) ✅ — Vaza Toga 4 (1869–1873)

Colisão: o batch chegou como **1868–1872**, mas **1868** já era os decretos do MCI. Realocado para **1869–1873**.

---

## Rodada 20/08/2026 (a) ✅ — Fila 1865–1868 (regulação internet)

| ID | Conteúdo |
|----|----------|
| **1865** | Lira arquiva PL 2630/2020 |
| **1866** | STF art. 19 MCI (Temas 987 e 533) |
| **1867** | Lei 15.211/2025 ECA Digital |
| **1868** | Decretos 12.975 e 12.976/2026 |

---

## Pendências abertas

| Item | Prioridade |
|------|------------|
| Formalizar **P13 Porta Giratória** em METHODOLOGY.md (T-254) | Média |
| Formalizar P04b em METHODOLOGY | Média |
| Stubs **725 / 728 / 729** vs registro definitivo 1869–1873 — decidir patch ou arquivar | Média |
| Renomear estudos mislabel `T-1512`/`T-1765`/`T-1766` → faixa T-255+ | Baixa |
| Gap main **1820** (editorial → T-248) | Informativo |
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

- Corpus: `_data/lawfare.json` (**1849** entradas · main até **1888**)
- Unified: `_data/lawfare-unified-corpus.json`
- Sidecar dragão: `_data/dragao-onca.json` (151 · **1763/1764** = CEEE-T / JMEV intactos)
