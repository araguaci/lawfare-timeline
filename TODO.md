# Próximos passos · lawfare-timeline

**Atualizado:** 2026-09-10 (T-267 minérios / terras raras)

> Espelho: `docs/TODO.md` · Notas: `_data/processados/todo.md` · Legado: `docs/TODO-LEGACY.md`

---

## Snapshot

| Track | Last | Próximo | Validação |
|-------|------|---------|-----------|
| Main | **1912** | **1913** | lawfare.json **1873** entradas · sem IDs duplicados |
| Thematic | **T-267** | **T-268** | sync 100–267 contínuo |
| Dragão e a Onça | **1770** / **T-246** | — | `dragao-onca.json` **151** |
| Fila `_data/todo/` | staging HTML/MD | — | JSON 1910–1912 arquivado 10/09 |

---

## Rodada 10/09/2026 (c) ✅ — T-267 minérios / terras raras

Estudo temático do extrato `_data/minerios-terras-raras.json` (**80 IDs**). Hero do X Article `118 DIAS`. Próximo temático: **T-268**.

| ID | Post |
|----|------|
| **T-267** | `_posts/estudos/2026-09-10-minerios-terras-raras-dois-mercados.md` |

---

## Rodada 10/09/2026 (b) ✅ — Fachin / Temer / Projeto Topázio

| Faixa | Batch | Conteúdo |
|-------|-------|----------|
| **1910** | `fachin-pf-temer-topazio` | Fachin suspende Mendonça/Dino sobre a PF e tira Moraes do INQ 4.781 |
| **1911** | mesmo lote | Temer pede «serenidade» após aconselhar Moraes em privado (URLs Metrópoles/247 inseridas no merge) |
| **1912** | mesmo lote | Extração forense Gmais confirma «Projeto Topázio» (elo Nikolas/Vorcaro) |

IDs 1910–1912 estavam livres. Sem realocação.

---

## Rodada 10/09/2026 ✅ — Crise Moraes / Mendonça / INQ 4781

| Faixa | Batch | Conteúdo |
|-------|-------|----------|
| **1905–1908** | `crise-moraes-mendonca-inq4781` | Sigilo do relatório Master; Moraes encaminha Fachin via 4.781; PF aponta risco de nulidade; relatório de inteligência prévio (`ev-alleged`) |
| **1909** | mesmo lote | Nikolas pede prisão de Moraes e os áudios com Vorcaro (P04b) |

IDs pediam 1905–1909 e estavam livres. Sem realocação.

---

## Rodada 01/09/2026 ✅ — Fila com colisão 1889

Dois batches pediam **1889+**. Realocados antes do merge.

| Faixa | Batch | Conteúdo |
|-------|-------|----------|
| **1889–1897** | Radiolão / Machado | Denúncia de inserções, exoneração, PAD, CNJ, plano de mídia 2026 |
| **1898–1904** | INQ 4781 cronologia | Receita 133 contribuintes → ADC 43/44/54 → validação do inquérito → Toffoli/Moro → Reino Unido → bloqueio do X |
| **T-263** | Auditoria MCD-05/2024 | Mapa das Conexões (P04b/P09/P10) |
| **T-264–T-266** | Editoriais do lote INQ | Transparência Internacional/Dallagnol; Estadão «Sete anos de exceção»; Talhari / legítima defesa institucional |

`lawfare-batch-inq4781-cronologia-1889-1898.json` **não** manteve 1889–1898.

---

## Rodada 20/08/2026 (c) ✅ — Vaza Toga 5 + 2 + 3 (IDs atrasados)

A fila reapresentou 4 batches com numeração antiga. **VT4 era duplicata** de 1869–1873 — não mergeado. VT5/VT2/VT3 realocados a partir de **1874**.

| Faixa | Batch | Conteúdo |
|-------|-------|----------|
| **1874–1876** | VT5 (era 1865–1867) | 2.119 CPFs; PET 11228 Dino; sigilo Exército |
| **1877–1882** | VT2 (era 1873–1878) | Certidões GestBio / Dia da Mulher |
| **1883–1888** | VT3 (era 1879–1884) | Fraude exposta (Constantino/Fiuza, Gettr, Zambelli, Palver) |
| — | VT4 (1868–1872) | **Skip** — já publicado como **1869–1873** |

---

## Pendências abertas

| Item | Prioridade |
|------|------------|
| **1899** sem `fontes_verificadas` (ADC 43/44/54 — `ev-contested` no lote) | Alta |
| **1907** / **1908** `ev-alleged` (fonte única / coluna) — corroborar | Alta |
| Formalizar **P13 Porta Giratória** em METHODOLOGY.md (T-254) | Média |
| Formalizar P04b em METHODOLOGY | Média |
| Stubs **725 / 728 / 729** vs registro definitivo 1869–1873 — decidir patch ou arquivar | Média |
| Staging `todo/p13-porta-giratoria.html` + HTML Radiolão/INQ/MCD + `prompt-tratamento-pdfs-mensalao.md` | Baixa |
| `/tags/p10/` em produção lista 1 post — colisão `p10`/`P10` (plugin local; falta deploy) | Média |
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

- Corpus: `_data/lawfare.json` (**1873** entradas · main até **1912**)
- Unified: `_data/lawfare-unified-corpus.json`
- Sidecar dragão: `_data/dragao-onca.json` (151 · **1763/1764** = CEEE-T / JMEV intactos)
