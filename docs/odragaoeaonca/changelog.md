# Changelog — O Dragão e a Onça

Registro de alterações em **fontes** do subsite/submódulo `odragaoeaonca/`.  
Não inclui espelhos em `docs/odragaoeaonca/` (artefato de build Jekyll no repositório principal).

Formato: data (ISO) → resumo → arquivos de fonte.

---

## 2026-07-27 (l) — series-nav 0–18 + pipeline timeline/

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Atualizado** | `scripts/updater_series_nav.py` | Sequência 0–18 (+ SC T-246); fallback RJ sem `<main>`. |
| **Atualizado** | `scripts/generate_timeline_pages.py` | Cap. 18 SC; extrator `.tlitem`; 18 timelines. |
| **Criado** | `scripts/run_series_pipeline.py` | Orquestra: series-nav → generate → patch index. |
| **Atualizado** | `scripts/patch_timeline_index_hrefs.py` | Href SC + contagens 0–18 / T-246. |
| **Regenerado** | 18× `dragao-onca-*.html` series-nav | Cards 0–18; `is-current` por capítulo. |
| **Gerado** | `timeline/timeline-santa-catarina.html` | Condensado IDs 1764–1770. |
| **Atualizado** | `timeline/index.html` · `index.html` | Card/chip SC; link Timeline; aliases `#sc`/`#t-246`. |

Uso: `python scripts/run_series_pipeline.py`

---

## 2026-07-27 (k) — Docs: Santa Catarina (T-246) no índice da série

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Atualizado** | `README.md` | Cap. 18: paths X Article + hero; tese T-243–246; calendário dia 18; corpus ~150 / IDs→1770. |
| **Atualizado** | `CATALAGO.md` | Índice #18 + prompt hero SC; UF SC; pendência hero fechada. |
| **Atualizado** | `promo/x-posts-promocao.md` | Hub/corpus; B17 dossiê SC; C15 X Article; calendário dia 16. |

---

## 2026-07-27 (j) — X Article Santa Catarina (T-246)

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Criado** | `artigos/santa-catarina-xarticle.md` | X Article: Alesc×JMEV, cortejo duplo SC/ES sem fábrica; ferrovias exploratórias; GACC/frango como controle. |
| **Criado** | `public/dragao-onca-santa-catarina.webp` | Hero share card (~1024×600, 5:2). |

Fonte: `dragao-onca-santa-catarina.html` · IDs 1764–1770 · T-246.

---

## 2026-07-27 (i) — Fix cards do timeline hub (âncoras aninhadas)

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Corrigido** | `timeline/index.html` | Cards 0–17: `div.card` + `a.card-main` + `#âncora` no topo — remove `<a>` dentro de `<a>` que quebrava layout/clique. |

---

## 2026-07-27 (h) — Timelines condensadas + hub reordenado

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Criado** | `scripts/generate_timeline_pages.py` | Extrai KPIs + eventos dos dossiês → `timeline/timeline-*.html`. |
| **Gerado** | 17× `timeline/timeline-*.html` | Capítulos 1–17 (Federal→RJ), series-nav ordem de importância. |
| **Reescrito** | `index.html` | Ordem 1–17 + âncoras; links Dossiê + Timeline por card. |
| **Atualizado** | `timeline/index.html` | Cards apontam às timelines condensadas. |

---

## 2026-07-27 (g) — Timeline hub: ordem de importância + âncoras

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Reescrito** | `timeline/index.html` | 18 artefatos (0–17); índice inteligente sticky; âncoras `#federal`…`#rj`; aliases UF/T-ID; links dossiês + X Articles. |

---

## 2026-07-27 (f) — Hub Jekyll: ordem de importância nos Capítulos Temáticos

A página `/dragao-onca/` (layout Chirpy) passou a listar os 18 posts **T-228→T-245** na mesma ordem de leitura deste README (0 Hub → 17 T-245), em vez de data decrescente.

| Ação | Arquivo (repositório principal) | Descrição |
|------|----------------------------------|-----------|
| **Criado** | `_data/dragao_onca_thematic_order.yml` | Lista `timeline_id` 229, 236, 238, 228… 245. |
| **Alterado** | `_layouts/dragao-onca.html` | Seção **Capítulos Temáticos** usa ordem de importância; timeline cronológica inalterada. |

Detalhes de tags `p0x` e build: [`changelog.md`](../changelog.md) (entrada 2026-07-27).

---

## 2026-07-27 (e) — Sínteses refeitas (11 UFs)

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Reescrito** | `dragao-onca-sintese.html` | v1 T-233: 11 UFs, KPIs, comparativo AP/RJ, alertas, horizontes SC/MA. |
| **Reescrito** | `dragao-onca-sintese-final-cross-state.html` | T-243: 10 mecanismos; tabela 11 estados; RS Day **1756**; lacunas CADE/GACC. |
| **Reescrito** | `artigos/sintese-xarticle.md` · `sintese-final-xarticle.md` | X Articles alinhados; tweet 11 estados / 10 mecanismos. |

Corpus referenciado: **T-228→T-245** · **142 posts** · **17 dossiês HTML**.

---

## 2026-07-27 (d) — Hero RJ (T-245)

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Criado** | `public/dragao-onca-rj.webp` | Hero 1024×600 — Açu + vigilância. |
| **Atualizado** | `public/dragao-onca-rj.webp` | Capa web exportada do hero. |
| **Atualizado** | `README.md` · `CATALAGO.md` | Path hero RJ; pendência fechada. |

---

## 2026-07-27 (c) — README alinhado aos 18 artigos

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Atualizado** | `README.md` | Ordem 0–17; índice X Articles completo; promo RS + RJ; calendário ~18 dias; corpus T-228→T-245 / 17 HTML + 18 X Articles; ponte `CATALAGO.md`. |

---

## 2026-07-27 (b) — Catálogo completo + prompts hero

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Reescrito** | `CATALAGO.md` | 18 entradas por ordem de importância; prompts completos (base + capítulo) para todos; atalho UFs; pendências hero RJ/MG/RS. |

---

## 2026-07-27 (a) — X Article Amapá (T-244) + hero

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Atualizado** | `artigos/amapa-xarticle.md` | X Article Cap. 16: Amazonbai 15 mil t, GACC pendente, Chevron/CNPC R$582,2mi; URL vercel; contraste Bahia. |
| **Criado** | `public/dragao-onca-amapa.webp` | Hero share card X (1024×600, wide 5:2). |
| **Atualizado** | `README.md` | Hero path no índice X Articles. |

---

## 2026-07-26 (h) — Capítulo Rio de Janeiro T-245 + IDs 1760–1762

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Processado** | batches RJ 1760–1762 + T-245 | CMPort/Vast, Castro/Hikvision, CNOOC/PetroChina |
| **Criado** | `dragao-onca-rj.html` | Dossiê Cap. 17 (OG tags + conteúdo editorial) |
| **Criado** | `artigos/rj-xarticle.md` | X Article T-245 |
| **Sync** | lawfare.json · claude.ai-corpus-ids-sync.json | main **1762** (next 1763) · thematic **245** (next 246) |

---

## 2026-07-26 (g) — Capítulo Amapá T-244 + IDs 1757–1759

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Processado** | batches amapa + T-244 | Amazonbai/açaí (1757–1758), Chevron/CNPC (1759), capítulo controle |
| **Patch** | `patch-id1100-margem-equatorial-fza59.json` | Correção parser id_1100 (FZA-M-59 — contexto Margem Equatorial) |
| **Criado** | `dragao-onca-amapa.html` | Dossiê interativo Cap. 16 |
| **Criado** | `artigos/amapa-xarticle.md` | X Article T-244 |
| **Sync** | lawfare.json · claude.ai-corpus-ids-sync.json | main **1759** (next 1760) · thematic **244** (next 245) |

---

## 2026-07-26 (f) — X Article T-243 (síntese final)

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Criado** | `artigos/sintese-final-xarticle.md` | Fechamento tipológico 8 mecanismos; releitura MG/RS; confirma/enfraquece/contraria. |
| **Criado** | `public/dragao-onca-sintese-final.webp` | Hero share card X (1024×600, wide 5:2). |
| **Atualizado** | `README.md` · `dragao-onca-sintese-final-cross-state.html` | Índice X Article; lacuna T-243 fechada. |

---

## 2026-07-26 (e) — Síntese final T-243: releitura MG + RS

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Atualizado** | `dragao-onca-sintese-final-cross-state.html` | KPIs, correções metodológicas, tabela, tipologias 6–7 (CEEE-T; vitrine+China), tese, lacunas, mapa com links; alinhado à síntese v1 26/jul. |
| **Atualizado** | `scripts/updater_series_nav.py` | Card MG: “Sigma + China paralela”. |

---

## 2026-07-26 (d) — Síntese v1: releitura MG + RS

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Atualizado** | `dragao-onca-sintese.html` | Tese/KPIs/quadro/gráficos/alertas: MG deixa “sem China” (CRRC/Midea/BYD ~R$1,4bi+); RS com CEEE-T R$2,67bi + derrota GWM; soma ~R$81bi; links ao dossiê RS dedicado. |
| **Atualizado** | `artigos/sintese-xarticle.md` | Mesma releitura MG/RS no X Article da síntese. |

---

## 2026-07-26 (c) — Dossiê RS (T-240) no shell da série

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Reescrito** | `dragao-onca-rio-grande-do-sul.html` | Cap. 13 mobile-first: shell Bahia, scroll-spy, KPIs, simetria, series-nav, `#gotop`, copyAll, safe-area; CEEE-T + GWM 1735–1737. |
| **Atualizado** | `scripts/updater_series_nav.py` | Insere RS como ordem 10; renumera RS/ES→15. |
| **Atualizado** | `index.html` · `README.md` | Card RS aponta ao dossiê dedicado. |

---

## 2026-07-26 (b) — Referência de qualidade de artefato

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Criado** | `docs/qualidade-artefato-referencia.md` | Benchmark Bahia (T-237); ranking por função; checklist 12 critérios; recomendações A/B/C; prompts completo e de auditoria para artefatos ≥ qualidade Bahia. |

---

## 2026-07-26 (a) — X Article RS · ES · Ranking CEBC

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Atualizado** | `artigos/rs-es-ranking-xarticle.md` | X Article T-240–242: par de controle GWM, logística vs diplomacia, ranking CEBC US$85,5bi / 355 projetos. |
| **Criado** | `public/dragao-onca-rs-es-ranking.webp` | Hero share card X (1024×600, composição wide 5:2). |

---

## 2026-07-25 (k) — X Article Paraná

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Atualizado** | `artigos/parana-xarticle.md` | X Article T-239: CMPort 90%, acordos gêmeos APPA/MPor (3–5/nov/2025), contraste SP, nota anti-confirmation-bias. |
| **Criado** | `public/dragao-onca-parana.webp` | Hero share card X (1024×600, composição wide 5:2). |

---

## 2026-07-25 (j) — X Article síntese v1

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Atualizado** | `artigos/sintese-xarticle.md` | X Article T-233 alinhado à síntese de 9 UFs: confirma / enfraquece / contraria; KPIs CEBC; ponte T-243. |
| **Criado** | `public/dragao-onca-sintese.webp` | Hero share card X (1024×600, composição wide 5:2). |

---

## 2026-07-25 (i) — crédito Artes do Sul nos rodapés

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Alterado** | 14× `dragao-onca-*.html` + `index.html` + `odragaoeaonca.html` | Rodapé: **Desenvolvido por [Artes do Sul](https://www.artesdosul.com/)** (link + CSS `.footdev`; nos dossiês com `flinks`, também no grupo de links). |

---

## 2026-07-25 (h) — síntese v1 com novos artefatos

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Alterado** | `dragao-onca-sintese.html` | Tese com nuance (BA, SP, PR, RS/ES, Diplomático); KPIs 9 UFs / ~R$78bi / CEBC; quadro 9 estados; gráficos e alertas atualizados; horizontes marcando entregas 25/jul; ponte para T-243. |

---

## 2026-07-25 (g) — nav scroll-spy nos artefatos novos

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Alterado** | `dragao-onca-sao-paulo.html`, `bahia`, `parana`, `rs-es-ranking-nacional`, `braco-diplomatico`, `sintese-final-cross-state` | Nav deixou de ser tabs (show/hide). Agora mostra todo o conteúdo, destaca a seção ativa via `IntersectionObserver` (padrão MG) e `#gotop` fixo no canto inferior direito. |

---

## 2026-07-25 (f) — series-nav em todos os dossiês

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Alterado** | 8× `dragao-onca-*.html` (GO, BR, PA, AM, MG, síntese v1, PL 2.780, jurídico) | `#serie` atualizado: 15 artefatos na ordem README; `is-current` no capítulo da página. |
| **Criado** | 6× `dragao-onca-*.html` (diplomático, SP, BA, PR, RS/ES/ranking, síntese final) | CSS `series-nav` + seção `#serie` antes do rodapé (mesmo padrão). |

---

## 2026-07-25 (e) — series-nav federal (ordem README)

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Alterado** | `dragao-onca-brasil-federal.html` | `#serie` / `series-nav`: 15 artefatos na ordem de importância do README (0 Hub → 14 T-243); card atual T-229 com `is-current`. |

---

## 2026-07-26 (e) — OG Graph + links dossiê nos capítulos T-*

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Alterado** | `odragaoeaonca/dragao-onca-*.html` | OG/Twitter em 9 dossiês que faltavam; RS normalizado para gosurf.site |
| **Alterado** | `_posts/dragao-onca/2026-07-24-t*.md` | Bloco **Link para dossiê completo:** → gosurf.site (16 capítulos) |
| **Criado** | `scripts/apply_dragao_onca_og_and_dossier_links.py` | Automação reutilizável |

---

| Ação | Descrição |
|------|-----------|
| **Batch** | 8 entradas: GWM critérios ES (1749), MG CRRC/Midea/BYD/Wondfo (1750–1755), RS Day Pequim (1756) |
| **Posts** | +8 em `_posts/dragao-onca/` (134 total) |
| **Sync** | `lawfare.json` + `claude.ai-corpus-ids-sync.json` → last_id **1756** |

---

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Alterado** | `README.md` (repo principal) | Seção série Dragão e a Onça, IDs 1748/T-243, tabelas de artefatos |
| **Criado** | `promo/x-posts-promocao.md` | 32 posts X (hub, corpus, 16 dossiês, 14 X Articles) + calendário 15 dias |

---

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Alterado** | `index.html` | 16 dossiês: eixos transversais → UFs por ranking CEBC → sínteses; badge **25/jul** nos novos artefatos; seção X Articles. |

---

Posts e capítulos temáticos gerados a partir dos batches mergeados; xarticle SP já publicável em `artigos/`.

| Ação | Descrição |
|------|-----------|
| **Repo principal** | 43 posts novos em `_posts/dragao-onca/`, lawfare.json e sync atualizados |
| **HTML** | Dossiês `dragao-onca-*.html` na raiz do submódulo (SP, Bahia, etc.) |
| **X Articles** | `artigos/sao-paulo-xarticle.md` + hero (Cap. 11) |
| **Pendente editorial** | Heroes regionais base (webp); artes dedicadas por UF opcionais; `jekyll build` pausado |
| **X Articles** | `parana-xarticle.md`, `rs-es-ranking-xarticle.md` (+ sao-paulo, bahia existentes) |

---

Artigo longo para X.com a partir do dossiê HTML `dragao-onca-sao-paulo.html` (CRRC, COFCO, variante “mercado”, IDs 1726–1730, T-238).

### Fontes

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Criado** | `artigos/sao-paulo-xarticle.md` | X Article: leilões/concessões, domínio CRRC, terminal COFCO Santos, tese T-238, lacunas, fontes. |
| **Criado** | `public/dragao-onca-sao-paulo.webp` | Capa share card X, 1024×600 px, composição wide 5:2. |
| **Fonte** | `dragao-onca-sao-paulo.html` | Dossiê interativo Cap. 11 (5 entradas + 1 vaga, fev/2024–2026). |

### Publicação X (referência)

- Compositor: **x.com/compose/article**
- Link externo do dossiê no **primeiro reply** (não no tweet principal): `https://gosurf.site/dragao-onca-sao-paulo`

---

## 2026-07-25 — Convenção de caminhos (repositório principal)

Regra Cursor no projeto pai documenta que **esta pasta** (`odragaoeaonca/` na raiz) é a fonte canônica — não `docs/odragaoeaonca/`.

| Ação | Arquivo (repo principal) | Descrição |
|------|--------------------------|-----------|
| **Criado** | `.cursor/rules/odragaoeaonca-paths.mdc` | X Articles, heroes e HTML sempre em `odragaoeaonca/artigos/` e `odragaoeaonca/*.html`. |

---

## Estrutura esperada de `artigos/`

```
artigos/
├── [capitulo]-xarticle.md      # texto para X Articles
└── [capitulo]-xarticle-hero.png # capa 1024×600 (quando gerada)
```

Capítulos com xarticle na pasta (jul/2026): amazonas, bahia, braco-diplomatico, braco-juridico, brasil-federal, goias, minas-gerais, odragaoeaonca (série), **parana**, para, pl2780, **rs-es-ranking**, sao-paulo, sintese.
