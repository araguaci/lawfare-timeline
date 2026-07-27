# Changelog

Registro de alterações em **fontes** do projeto.  
O build Jekyll gera em `docs/` (`destination: docs`) e **não** é listado aqui.

Formato: data (ISO) → resumo → arquivos de fonte.

---

## 2026-07-27 — Sínteses cross-estadual refeitas (11 UFs)

Após os capítulos **Amapá (T-244)** e **Rio de Janeiro (T-245)**, os quatro artefatos de síntese foram reescritos: KPIs, tabela comparativa, tipologia ampliada (10 mecanismos), alertas, horizontes e `series-nav` (17 dossiês). Correção **RS Day → id_1756** (1760 = CMPort/Vast no RJ). Corpus **T-228→T-245** · **142 posts** · IDs **1639–1762**.

### Fontes (`odragaoeaonca/`)

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Alterado** | `dragao-onca-sintese.html` | Síntese v1 (T-233): 11 UFs, + AP/RJ na tese, KPIs, comparativo, alertas, horizontes (SC/MA candidatos). |
| **Alterado** | `dragao-onca-sintese-final-cross-state.html` | Fechamento T-243: tabela 11 estados; mecanismos 8–10 (captura federal, controle cooperativista, composição infra+gov.); lacunas CADE/GACC. |
| **Alterado** | `artigos/sintese-xarticle.md` | X Article v1: 11 UFs, seções AP/RJ, 10 mecanismos, tweet atualizado. |
| **Alterado** | `artigos/sintese-final-xarticle.md` | X Article T-243: fechamento tipológico 11 estados; links AP/RJ; RS Day 1756. |

### Snapshot pós-síntese

| Track | Last | Próximo |
|-------|------|---------|
| Main | **1762** | **1763** |
| Thematic | **T-245** | **T-246** |
| Posts `dragao-onca` | **142** | — |
| Dossiês HTML | **17** | — |

---

## 2026-07-26 — Amapá T-244 · Rio de Janeiro T-245 · expansão MG/RS

Rodada pós-síntese T-243: backfill **MG** (China paralela CRRC/Midea/BYD), **RS Day** (1756), novos capítulos **AP** e **RJ**. `_data/todo/` esvaziada após merge.

### Fontes

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Criado** | `_posts/dragao-onca/*.md` (+16) | IDs **1749–1762** + temáticos **T-244**, **T-245**. Total pasta: **142 posts**. |
| **Alterado** | `_data/lawfare.json` | +16 assuntos dragao-onca (max ID **1762**). |
| **Alterado** | `_data/claude.ai-corpus-ids-sync.json` | main next **1763** · thematic last **T-245** (next **T-246**). |
| **Arquivado** | `_data/processados/lawfare-batch-dragao-onca-*-1749*.json` etc. | MG 1750–1755, RS Day 1756, AP 1757–1759, RJ 1760–1762, T-244, T-245. |
| **Patch** | `scripts/apply_lawfare_patch.py` | id_1100 (FZA-M-59 — contexto Margem Equatorial). |
| **Criado** | `odragaoeaonca/dragao-onca-amapa.html` | Dossiê Cap. 16 (controle + captura federal). |
| **Criado** | `odragaoeaonca/dragao-onca-rj.html` | Dossiê Cap. 17 (Açu + Castro/Hikvision). |
| **Criado** | `odragaoeaonca/artigos/amapa-xarticle.md` · `rj-xarticle.md` | X Articles T-244 · T-245. |
| **Criado** | `assets/img/dragao-onca-{amapa,rj}.webp` | Heroes regionais. |
| **Alterado** | `scripts/gerar_artigos_dragao_onca.py` | T-244, T-245, mapeamentos AP/RJ, arrays de batch. |
| **Alterado** | `scripts/fix_dragao_onca_hero_images.py` | Faixas 1757–1762, t244, t245. |
| **Alterado** | `scripts/add_dragao_onca_state_tags.py` | Tags `amapa`, `rio-de-janeiro`, overrides T-244/T-245. |
| **Alterado** | `scripts/apply_dragao_onca_og_and_dossier_links.py` | OG T-245; THEMATIC_DOSSIER 244/245. |
| **Alterado** | `odragaoeaonca/index.html` · `README.md` · `CATALAGO.md` | Hub 17 dossiês; cards AP/RJ. |

### Capítulos novos

| T / IDs | Capítulo |
|---------|----------|
| 1749–1756 | MG expandido + RS Day Pequim |
| T-244 · 1757–1759 | Amapá — Amazonbai/açaí, GACC, Chevron/CNPC |
| T-245 · 1760–1762 | RJ — CMPort/Vast, Castro/Hikvision, CNOOC cliente |

### Verificação

- `tools/validate-ids.ps1` → 0 erros
- `bundle exec jekyll build` → **não executado** (pausa editorial mantida)

---

## 2026-07-25 — Conclusão da série O Dragão e a Onça (IDs 1713–1748 · T-236–T-243)

Merge dos capítulos pendentes: diplomático federal, Bahia, São Paulo, Paraná, RS, ES, Goiás retroativo e síntese final cross-state. **Build Jekyll pausado** para revisão editorial antes de `bundle exec jekyll build`.

### Fontes

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Criado** | `_posts/dragao-onca/*.md` (+43) | 36 main (1713–1748) + 7 temáticos (T236–T241, T243). Total pasta: **125 posts**. |
| **Alterado** | `_data/lawfare.json` | +36 assuntos dragao-onca (total categoria: **110**, max ID **1748**). |
| **Alterado** | `_data/claude.ai-corpus-ids-sync.json` | main next **1749**, thematic last **T-243**. |
| **Arquivado** | `_data/processados/lawfare-batch-dragao-onca-*-1713-1748.json` | 7 batches main track. |
| **Arquivado** | `_data/processados/lawfare-thematic-T236–T243*.json` | 7 capítulos temáticos. |
| **Alterado** | `scripts/gerar_artigos_dragao_onca.py` | Suporte `assuntos`, temáticos soltos, síntese T-243, merge lawfare + sync + archive. |
| **Alterado** | `scripts/add_dragao_onca_state_tags.py` | Tags bahia, parana, rio-grande-do-sul, espirito-santo; overrides T236–T243. |
| **Alterado** | `_layouts/dragao-onca.html` | Badges de estado na timeline (+4 UFs). |
| **Corrigido** | `_posts/dragao-onca/2026-07-24-t228-o-dragao-e-a-onca-goias.md` | Front matter YAML (`layout: post`). |
| **Alterado** | `TODO.md` | Snapshot main **1748**, thematic **T-243**, fila todo vazia. |

### Capítulos temáticos (ordem)

| T | Capítulo |
|---|----------|
| T-228 | Goiás |
| T-229 | Brasil federal |
| T-230 | Pará |
| T-231 | Amazonas |
| T-232 | Minas Gerais |
| T-233 | Síntese comparativa (v1) |
| T-234 | Braço jurídico |
| T-235 | PL 2.780/2024 |
| T-236 | Braço diplomático |
| T-237 | Bahia |
| T-238 | São Paulo |
| T-239 | Paraná |
| T-240 | Rio Grande do Sul |
| T-241 | Espírito Santo |
| T-243 | Síntese final cross-state |

### Verificação (sem build)

- `python scripts/validate_dragao_onca_yaml.py` → OK (125 arquivos)
- T-243: correção metodológica e escopo atualizados (Goiás T-228 + 1740–1748)
- `_data/todo/` esvaziada (batches arquivados em `processados/`)
- `bundle exec jekyll build` → **não executado** (pausa solicitada)

---

## 2026-07-25 (b) — T-242, imagens hero e xarticles (itens 1–3)

### Fontes

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Criado** | `_posts/dragao-onca/2026-07-24-t242-dragao-onca-ranking-cebc.md` | Capítulo ranking CEBC 2007-2025 (T-242). Total pasta: **126 posts**. |
| **Criado** | `assets/img/dragao-onca-{bahia,sao-paulo,parana,rio-grande-do-sul,espirito-santo,ranking-cebc}.webp` | Heroes regionais (26 posts + capítulos temáticos atualizados). |
| **Criado** | `scripts/fix_dragao_onca_hero_images.py` | Atualiza `image:` por faixa ID e capítulo temático. |
| **Criado** | `odragaoeaonca/artigos/parana-xarticle.md` | X Article Cap. 12 (TCP/CMPort). |
| **Criado** | `odragaoeaonca/artigos/rs-es-ranking-xarticle.md` | X Article RS/ES + ranking CEBC. |
| **Alterado** | `_data/claude.ai-corpus-ids-sync.json` | Entrada T-242; thematic last **243**. |
| **Alterado** | `_posts/dragao-onca/2026-07-24-t243-sintese-final-cross-state.md` | T-242 integrado; lacuna removida. |

---

### Fontes

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Criado** | `.cursor/rules/odragaoeaonca-paths.mdc` | Regra: xarticles, heroes e HTML em `odragaoeaonca/`; proíbe salvar em `docs/odragaoeaonca/`. |

---

## 2026-07-24 — Links internos e títulos nos capítulos temáticos Dragão e a Onça

Links de artigos relacionados passam de `/timeline/entries/{id}` para `/posts/{slug}/` (permalink Jekyll). Capítulos `2026-07-24-t*` exibem o **título real** do post no texto do link, não `Entrada {id}`.

### Fontes

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Alterado** | `_posts/dragao-onca/*.md` (61 arquivos) | URLs `/timeline/entries/` → `/posts/{slug}/`. |
| **Alterado** | `_posts/dragao-onca/2026-07-24-t*.md` (6 arquivos) | Labels dos links: título do artigo destino (t229, t230, t231, t232, t234, t235). |
| **Alterado** | `scripts/gerar_artigos_dragao_onca.py` | `build_post_index()` (slug + título), `post_url_for_timeline_id()`, `post_title_for_timeline_id()`, `yaml_escape()` nos títulos/descrições, filtro de tags vazias, `extract_year()` com fallback. |
| **Criado** | `scripts/fix_dragao_onca_post_links.py` | Corrige URLs e labels de links em lote. |
| **Alterado** | `scripts/fix_dragao_onca_yaml_titles.py` | Modos `--tags`, `--rebuild-titles`; skip de títulos já escapados. |

---

## 2026-07-24 — Correção YAML em `_posts/dragao-onca/`

Build Jekyll falhava com `did not find expected key` em 16 posts: aspas duplas internas no campo `title` do front matter sem escape. Tags de ano vazias (`""`) em capítulos temáticos geravam aviso `Empty slug generated for ''`.

### Fontes

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Alterado** | `_posts/dragao-onca/*.md` (16 títulos + 15 tags) | Escape `\"` em títulos com citações; tag `"2026"` no lugar de `""`. |
| **Alterado** | `scripts/gerar_artigos_dragao_onca.py` | Prevenção na geração (ver entrada acima). |
| **Criado** | `scripts/fix_dragao_onca_yaml_titles.py` | Correção pontual de títulos e tags vazias. |
| **Criado** | `scripts/validate_dragao_onca_yaml.py` | Valida front matter YAML dos 90 posts da pasta. |

### Verificação

- `python scripts/validate_dragao_onca_yaml.py` → OK (90 arquivos)
- `bundle exec jekyll build` → concluído sem erros de YAML

---

## 2026-07-24 — Cards sem colisão + timeline estilo /timeline/

Ajuste visual da página `/dragao-onca/`: capítulos com card idêntico à home (sem texto sobre a imagem) e lista cronológica no padrão `#archives` de `/timeline/`.

### Fontes

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Alterado** | `_includes/post-card.html` | Imagem envolvida em `.preview-img.shimmer` + `loading="lazy"` (aspect-ratio/object-fit). |
| **Alterado** | `_layouts/dragao-onca.html` | Capítulos em `#post-list`; timeline com `#archives` (ano, nó, data, título, descrição, badge de estado). |
| **Alterado** | `_includes/refactor-content.html` | Evita double-wrap de `.preview-img` na home. |
| **Alterado** | `_sass/addon/commons.scss` | `width: 100%` da preview também em `.post-list`. |
| **Alterado** | `_sass/layout/home.scss` | `overflow: hidden`, `min-width: 0` nas colunas do card (anti-colisão). |
| **Alterado** | `_sass/layout/archives.scss` | Descrição multilinha + padding; linha do tempo acompanha a altura do item. |

---

## 2026-07-24 — Tags de estado nos artigos Dragão e a Onça

Incluída tag relativa ao estado (ou âmbito federal) no front matter de todos os 82 posts em `_posts/dragao-onca/`.

### Convenção de tags

| Tag | Escopo |
|-----|--------|
| `goias` | Capítulo / entradas Goiás |
| `para` | Capítulo / entradas Pará |
| `amazonas` | Capítulo / entradas Amazonas |
| `minas-gerais` | Capítulo / entradas Minas Gerais |
| `sao-paulo` | Entradas Doria/SP (Sinovac, escritório Xangai) |
| `brasil-federal` | Linha federal, braço jurídico e PL 2.780/2024 |

A síntese comparativa (`t233`) recebe as tags dos quatro estados + `brasil-federal`.

### Fontes

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Alterado** | `_posts/dragao-onca/*.md` (82 arquivos) | Tag de estado adicionada em `tags` (máx. 10). |
| **Criado** | `scripts/add_dragao_onca_state_tags.py` | Script idempotente: mapeia estado por imagem do capítulo, overrides por ID/arquivo. |

### Mapeamento (resumo)

- Imagem do capítulo → tag padrão (`dragao-onca-para.webp` → `para`, etc.).
- Overrides: IDs 1648–1650 → `sao-paulo`; ID 1710 (Serra Verde) → `goias`.
- Temáticos T228–T235 → tag do respectivo capítulo.

---

## 2026-07-24 — Cards da série Dragão e a Onça alinhados à home

A página da série (`/dragao-onca/`, layout `dragao-onca`) passa a usar o mesmo card horizontal da home: um por linha, texto à esquerda, imagem à direita (`flex-md-row-reverse`).

### Fontes

| Ação | Arquivo | Descrição |
|------|---------|-----------|
| **Criado** | `_includes/post-card.html` | Include do card horizontal reutilizável (imagem, título, descrição, data, categorias, `timeline_id`, pin). |
| **Alterado** | `_layouts/dragao-onca.html` | Capítulos temáticos e timeline passam a listar via `{% include post-card.html %}` em `.post-list` (remove grid `col-lg-6` e lista de arquivo com thumbnail). |
| **Alterado** | `_layouts/home.html` | Lista da home passa a usar o mesmo include `post-card.html`. |
| **Alterado** | `_sass/layout/home.scss` | Estilos de card de `#post-list` também aplicam a `.post-list` (reuso fora da home). |

### Portabilidade (projeto completo)

Ao levar para o repositório com ~3000 entradas, copiar apenas as fontes acima e regenerar o site (`jekyll build` → `docs/`).

### Fora do escopo deste changelog

- Saída gerada em `docs/` (HTML/CSS compilados).
- Posts, assets de conteúdo e dados.
