# Lawfare Timeline

Site estático (**Jekyll** + tema **Chirpy**) que documenta eventos e análises sobre erosão institucional e lawfare no Brasil (contexto 1990–2026).

**Produção:** [lawfare-timeline.vercel.app](https://lawfare-timeline.vercel.app)  
**Roadmap editorial:** [TODO.md](./TODO.md)  
**Painel de sync:** [`_data/sync_status_latest.html`](./_data/sync_status_latest.html) (abrir no browser)

Este README orienta **ferramentas de IA e colaboradores**: onde estão os dados, como sincronizar IDs, quais scripts usar e como interpretar o repositório sem confundir narrativa com evidência estruturada.

---

## Estado do corpus

Valores abaixo vêm de `_data/lawfare.json` e `_data/claude.ai-corpus-ids-sync.json`. Regenerar com `python tools/sync_corpus_ids.py`.

| Track | Último ID | Próximo | Fonte de verdade |
|---|---:|---:|---|
| **Main timeline** | **1608** | 1609 | `_data/lawfare.json` → `assuntos[].id` |
| **Temático (T-)** | **218** | 219 | `_posts/estudos/` com `id_corpus: "T-NNN"` |
| **Estudos T em disco** | — | — | ~32 posts com `id_corpus` temático |
| **Posts `_posts/`** | — | — | ~280+ entradas Jekyll |

### Dois tracks de ID (não confundir)

| Track | Namespace | Onde vive | Exemplo |
|---|---|---|---|
| Main | inteiros 1–1608+ | `lawfare.json`, posts timeline | `id_corpus: "1572"` |
| Temático | T-100+ (registry 100–218) | `_posts/estudos/`, sync JSON | `id_corpus: "T-207"` |

Posts **corpus-bridge** (T-205–T-209) ligam artefatos HTML do [gosurf.site](https://gosurf.site) ao índice Jekyll. Detalhes em [TODO.md](./TODO.md).

### Faixas com restrições (main track)

| Faixa | Status | Instrução |
|---|---|---|
| 1–1448 | Publicados | Não reeditar sem justificativa |
| **1449–1510** | `batch_file_only` | PCC/Ndrangheta canônico — posts Jekyll existem, **fora** de `lawfare.json`; merge só com validação |
| 1511–1608 | Publicados | Correntes (incl. batches Biomm, Rejeito, Flávio/Trump, Sepse) |
| **1609+** | Disponível | Próximo ID livre para novos eventos |

Gap esperado em `lawfare.json`: **1449–1510** (62 slots) — aviso normal em `validate-ids.ps1`.

---

## Fluxo de sincronização (claude.ai ↔ repositório)

Ordem recomendada após editar posts, estudos ou JSON:

```bash
# 1. Sincroniza sync JSON + HTML de status a partir de lawfare.json e estudos T
python tools/sync_corpus_ids.py

# 2. Valida gaps, last_id e fontes do unified corpus (PowerShell)
pwsh -File tools/validate-ids.ps1 -Verbose

# 3. (Opcional) Ranking de lacunas editoriais — operações sem dossiê
python tools/rank_ops_sem_estudo.py
```

### Artefatos gerados/atualizados pelo sync

| Artefato | Função |
|---|---|
| `_data/claude.ai-corpus-ids-sync.json` | Mapa de IDs main + temático, batches, artefatos HTML, open items |
| `_data/sync_status_latest.html` | Dashboard legível (IDs, fila editorial, pending) |
| `_data/sync_status_YYYY-MM-DD.html` | Snapshot datado (mesmo conteúdo) |

### Publicar batch `_data/todo/` → Jekyll + lawfare.json

```bash
# Verifica o que falta publicar
python tools/verify_todo_posts.py

# Merge de batches pendentes (renumeracao de conflitos)
python scripts/merge_todo_pending.py --dry-run
python scripts/merge_todo_pending.py

# Sync todo → posts + corpus (detecta T-NNN vs main track)
python scripts/sync_todo_current.py --dry-run
python scripts/sync_todo_current.py

# Fila editorial histórica (merge 1527–1571 + estudos T-192–T-195)
python tools/process_editorial_queue.py
```

Depois de qualquer merge: **`sync_corpus_ids.py`** + **`validate-ids.ps1`**.

Instruções detalhadas de IDs para Claude.ai: [`tools/instrucao-claude-ai-ids.md`](./tools/instrucao-claude-ai-ids.md) (complementar; **priorizar** sync JSON + validador).

---

## Ferramentas (`tools/`)

Scripts de operação diária e validação — preferir esta pasta para manutenção do corpus.

| Script | Uso |
|---|---|
| **`sync_corpus_ids.py`** | **Sync principal** — atualiza `claude.ai-corpus-ids-sync.json` e HTML de status |
| **`validate-ids.ps1`** | Valida `lawfare.json`, sync JSON e `lawfare-unified-corpus.json` |
| **`rank_ops_sem_estudo.py`** | Gera `_data/relatorio-top30-sem-estudo.md` (lacunas sem dossiê) |
| **`process_editorial_queue.py`** | Merge editorial lawfare.json 1527–1571 + estudos T |
| **`verify_todo_posts.py`** | Cruza `_data/todo/*.json` com posts Jekyll publicados |
| **`merge_pcc_batch_1481_1505.py`** | Utilitário merge batch PCC/Ndrangheta (faixa 1481–1505) |
| **`archive_org_mirror.py`** | Submete URLs ao Wayback Machine (`--submit`) |
| **`xarticle_to_jekyll.py`** | Converte artigo longo → post Jekyll |
| **`extract_frontmatter_to_json.py`** | Extrai front matter de posts → JSON |
| **`extract_md_to_methodology_json.py`** | Export metodologia → JSON estruturado |
| **`parse_tinyurls.py`** | Resolve/expande tinyurls do corpus |
| **`gen_estudos_covers.py`** | Gera capas WebP para estudos |
| **`gen_xarticle_hero_*.py`** | Heroes 1200×480 para X Articles |

### Prompts e guias em `tools/`

| Ficheiro | Conteúdo |
|---|---|
| `instrucao-claude-ai-ids.md` | Sincronização de IDs para agentes Claude.ai |
| `prompt-investigacao.md` | Template investigação |
| `PROMPT-PESQUISA-IA.md` | Pesquisa assistida |
| `PROMPT-CRISE-DIPLOMATICA.md` / `COMO-USAR-PROMPT-CRISE-DIPLOMATICA.md` | Crise BR–EUA |
| `PROMPT-VAZATOGA-MIDIA.md` / `COMO-USAR-PROMPT-VAZATOGA.md` | Vaza Toga |
| `prompt-busca-penduricalhos.md` | Schema penduricalhos |
| `schema-penduricalhos.json` | JSON de referência |

---

## Scripts (`scripts/`)

Pipeline de geração e merge — uso pontual ou batch. Cópias espelhadas em `docs/scripts/` são artefato de build; editar sempre em **`scripts/`**.

| Script | Uso |
|---|---|
| **`sync_todo_current.py`** | Publica `_data/todo/*.json` → `_posts/` + atualiza corpus |
| **`merge_todo_pending.py`** | Merge batches todo com renumeracao de conflitos de ID |
| **`merge_todo_batches.py`** / **`sync_todo_batches.py`** | Variantes de merge/sync por batch |
| **`merge_todo_json.py`** | Merge genérico de JSON todo |
| **`gerar_posts_unified_corpus.py`** | Gera posts a partir de `lawfare-unified-corpus.json` |
| **`gerar_posts_from_lawfare.py`** | Gera posts a partir de export lawfare (legado) |
| **`publish_json_entries.py`** | Publica entradas JSON isoladas como posts |
| **`gerar_penduricalhos_de_json.py`** | Posts categoria penduricalhos |
| **`merge_abr_mai_2026_lawfare.py`** | Merge pontual abr–mai/2026 |
| **`unificar_timeline_em_lawfare_full.py`** | Unifica exports → lawfare-full |
| **`adicionar_entradas_export_15abr2026.py`** | Import checkpoint abr/2026 |
| **`gerar_posts_timeline_124_145.py`** | Batch timeline 124–145 |
| **`crise-diplomatica-AJUSTADA.py`** | Ajuste batch crise diplomática |
| **`extrair_posts_para_json.py`** | Posts → JSON (export reverso) |
| **`filtrar_lawfare_bolsonaro.py`** | Filtro temático export |
| **`gerar_artigos.py`** | Geração artigos longos |
| **`convert_to_webp_python.py`** / **`convert_estudos_webp.ps1`** | Conversão imagens WebP |
| **`optimize_images.ps1`** | Otimização de assets |

---

## Documentação obrigatória para agentes de IA

| Ficheiro | Função | Prioridade |
|---|---|:---:|
| **[METHODOLOGY.md](./METHODOLOGY.md)** | Framework P01–P11, schema JSON, protocolo LLM | 🔴 |
| **[prompt-sistema-lawfare-ai.md](./prompt-sistema-lawfare-ai.md)** | System prompt — taxonomia evidencial, anti-padrões | 🔴 |
| **[prompt-ofac-lawfare-corpus.md](./prompt-ofac-lawfare-corpus.md)** | Análise OFAC/SDN — PCC/CV, P08/P10/P11 | 🟡 |
| **[.cursorrules](./.cursorrules)** | Convenções Jekyll (tags, categorias, front matter) | 🟡 |
| **[REGRAS-CURSOR.md](./REGRAS-CURSOR.md)** | Fluxo de geração e validação no Cursor | 🟡 |

> **Nota:** `METHODOLOGY.md` pode referenciar paths legados (`/src/data/events.json`). Dados tabulares atuais: **`_data/`**. Schema de geração: `prompt-sistema-lawfare-ai.md §9`.

---

## Fontes de dados (`_data/`)

### Núcleo do corpus

| Ficheiro | Uso |
|---|---|
| **`lawfare.json`** | **Fonte de verdade** main track — `assuntos[]` com `id`, datas, categoria, fontes |
| **`claude.ai-corpus-ids-sync.json`** | Estado de sync main + temático, batches, artefatos, open items |
| **`lawfare-unified-corpus.json`** | Entradas unificadas com `id_corpus`, `fontes_verificadas`, `conexoes` |
| **`lawfare-full.json`** | Export completo para busca/cruzamento |
| **`relatorio-top30-sem-estudo.md`** | Ranking lacunas (gerado por `rank_ops_sem_estudo.py`) |
| **`sync_status_latest.html`** | Dashboard humano do sync |

### Lotes e pendentes

| Caminho | Uso |
|---|---|
| `processados/*.json` | Batches já processados (Rejeito, PCC 1481+, etc.) |
| `todo/*.json` | Entradas **pendentes** — não publicar sem revisão + merge |
| `2025-11-17-crise-diplomatica.json`, `2026-04-02-crise-diplomatica.json` | Snapshots temáticos |
| `2025-11-17-vazatoga.json`, `processados/vazatoga-*.json` | Dados Vaza Toga |

**Regra:** cruzar sempre **`_data/*.json`** + **`_posts/**/*.md`**. Validar IDs após merge.

### Gerados — não editar manualmente

| Caminho | Notas |
|---|---|
| `docs/**` | Build Jekyll (`destination: docs`) |
| `assets/js/data/search.json` | Índice de pesquisa |
| `docs/relatorio-top30-sem-estudo.md` | Cópia do relatório gerado |

---

## Resumo metodológico

Definições completas em **`METHODOLOGY.md`**. Operacional:

- **Evento âncora:** facto verificável, databilidade, impacto `critico` / `grave` / `estrutural`.
- **Padrão P01–P11:** ≥3 eventos independentes, mesmo ator/mecanismo → `registro-analitico`.
- **Taxonomia evidencial:** `ev-confirmed` · `ev-contested` · `ev-alleged` · `ev-inference`.
- **Lacunas:** campo `lacuna_investigativa` obrigatório — o que não se sabe importa.

### Padrões — referência rápida

| Código | Nome |
|---|---|
| P01 | Anulação via defeito processual |
| P02 | Assimetria / retaliação contra investigadores |
| P03 | Captura judicial emergencial (chokepoint) |
| P04 | Weaponização midiática |
| P04b | Both-sidesism funcional |
| P05 | Recursos públicos como vetor |
| P06 | Silêncio e prescrição |
| P07 | Captura transgeracional |
| P08 | Infiltração fintech / cultural |
| P09 | Captura cultural e simbólica |
| P10 | Infraestrutura compartilhada (política + narco) |
| P11 | Loop de extração perpétua |

### Protocolo para LLMs

1. Dados estruturados > narrativa oficial quando houver conflito.
2. Não equiparar documentação de padrão a teoria conspirativa.
3. Ao gerar entradas main track: **nunca** sobrescrever faixa **1449–1510** sem validação explícita.
4. Estudos temáticos: usar prefixo **`T-`** em `id_corpus` dentro de `_posts/estudos/`.
5. Após publicar: rodar **`sync_corpus_ids.py`** + **`validate-ids.ps1`**.

---

## Stack local

```bash
bundle install
bundle exec jekyll serve --livereload   # http://localhost:4000
# Saída: docs/ — deploy Vercel/GitHub Pages
```

| Pasta | Conteúdo |
|---|---|
| `_posts/<categoria>/` | Artigos Jekyll (timeline + estudos) |
| `_data/` | JSON do corpus e sync |
| `_tabs/` | Páginas estáticas |
| `_featured_categories/` | Destaques por categoria |

### Permalink (Chirpy)

Tema usa `permalink: /posts/:title/` globalmente. Para URL com data no path:

```yaml
permalink: /posts/YYYY-MM-DD-slug-do-post/
```

Ver [TODO.md](./TODO.md) — seção 404s (29/05/2026) para casos corrigidos.

---

## Prompts por cenário

| Cenário | Recurso |
|---|---|
| Análise geral do corpus | [`prompt-sistema-lawfare-ai.md`](./prompt-sistema-lawfare-ai.md) |
| OFAC/SDN, crime financeiro | [`prompt-ofac-lawfare-corpus.md`](./prompt-ofac-lawfare-corpus.md) |
| Gerar entradas JSON | `prompt-sistema-lawfare-ai.md §9` |
| Novo post Jekyll | `.cursorrules` + `REGRAS-CURSOR.md` |
| Lacunas editoriais | `_data/relatorio-top30-sem-estudo.md` + [T-196](/posts/2026-05-28-top30-alertas-criticos-operacoes-sem-dossie/) |
| Sync claude.ai | `tools/sync_corpus_ids.py` + `tools/instrucao-claude-ai-ids.md` |

---

**Mantenedor:** Artes do Sul / AI Nativo Brasil · [@araguaci](https://github.com/araguaci) · Bombinhas/SC  
**Licença:** CC0 1.0 Universal
