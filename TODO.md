# Próximos passos · lawfare-timeline

**Atualizado:** 2026-07-25 (série Dragão e a Onça completa · IDs 1639–1748 · T-228–T-243)

> Espelho: `docs/TODO.md` · Notas: `_data/todo/todo.md` · Legado: `docs/TODO-LEGACY.md`

---

## Snapshot

| Track | Last | Próximo | Validação |
|-------|------|---------|-----------|
| Main | **1748** | **1749** | dragao-onca 110 entradas |
| Thematic | **T-243** | **T-244** | síntese final + ranking CEBC T-242 |
| Historical pre-1990 | PREC-1930-07 | — | 14 entradas · T-224 |
| Historical pos-1990 | PREC-1997-05 | — | 1 entrada · sidecar |
| Fila `_data/todo/` | vazio | — | — |

---

## Rodada 25/07/2026 ✅ — Série O Dragão e a Onça (conclusão)

| Faixa | Conteúdo |
|-------|----------|
| **1713–1718** | Braço diplomático federal (WAICO, Serra Verde, G7) |
| **1719–1725** | Bahia — caso de controle (PPP Ponte, Windey) |
| **1726–1730** | São Paulo — variante mercado (CRRC, COFCO) |
| **1731–1734** | Paraná — TCP / CM Port |
| **1735–1737** | Rio Grande do Sul — missão BYD/Huawei (GWM → ES) |
| **1738–1739** | Espírito Santo — fábrica GWM Aracruz |
| **1740–1748** | Goiás retroativo — Caiado, JOGMEC, terras raras |
| **T-236–T-241** | Capítulos temáticos novos |
| **T-243** | Síntese final cross-state |

**126 posts** em `_posts/dragao-onca/` · **build Jekyll pausado** para revisão editorial.

---

## Rodada 25/07/2026 (b) — T-242, heroes, xarticles

| Item | Entrega |
|------|---------|
| **T-242** | Post + JSON CEBC ranking; sync thematic **243** |
| **Heroes** | `dragao-onca-{bahia,sao-paulo,parana,rio-grande-do-sul,espirito-santo,ranking-cebc}.webp` + 26 posts atualizados |
| **X Articles** | `parana-xarticle.md`, `rs-es-ranking-xarticle.md` |
| **Scripts** | `fix_dragao_onca_hero_images.py`; gerador com seção ranking CEBC |


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
| T-242 (ranking CEBC) | Concluído (T-242 publicado) |
| Revisão editorial T-243 vs T-233 | Concluída (T-243 = síntese final) |
| `bundle exec jekyll build` | **Pausado** — aguardando admin lawfare-thematic/ids |
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
