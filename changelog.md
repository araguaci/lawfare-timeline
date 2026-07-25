# Changelog

Registro de alterações em **fontes** do projeto.  
O build Jekyll gera em `docs/` (`destination: docs`) e **não** é listado aqui.

Formato: data (ISO) → resumo → arquivos de fonte.

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
