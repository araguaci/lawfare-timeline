# Scripts · lawfare-timeline

Pipeline de geração, merge e exportação do corpus. **Editar sempre em `scripts/`** — cópias em `docs/scripts/` são artefato de build Jekyll.

**Requisitos:** Python 3.10+ (stdlib na maioria). Exceções: `pipeline_tse_farmaceutico.py` e `lawfare_timeline_farma_2022.py` exigem `pandas`.

---

## Fluxo editorial recomendado

Ordem típica após receber JSON em `_data/todo/`:

```bash
# 1. Simular publicação (lista posts que seriam criados)
python scripts/sync_todo_current.py --dry-run

# 2. Publicar: _posts/ + lawfare.json + sync JSON + arquivar todo
python scripts/sync_todo_current.py

# 3. Atualizar mapa de IDs e HTML de status
python tools/sync_corpus_ids.py

# 4. Validar integridade do corpus
pwsh -File tools/validate-ids.ps1 -Verbose
```

Verificação cruzada antes do merge:

```bash
python tools/verify_todo_posts.py
```

---

## Sync e merge (`_data/todo/`)

### `sync_todo_current.py` — **script principal**

Publica JSON pendentes em `_data/todo/` como posts Jekyll e atualiza o corpus.

| Entrada | Destino |
|---------|---------|
| `T-NNN*.json` ou `analise_estrutural` | `_posts/estudos/` (track temático) |
| `entries[]` com ID numérico | `_posts/<categoria>/` (track main) |
| Batches mistos (ex.: `1620` + `T-222`) | Roteamento por item |

Também atualiza `lawfare.json`, `lawfare-unified-corpus.json`, `claude.ai-corpus-ids-sync.json` e move JSON processados para `_data/processados/`.

```bash
python scripts/sync_todo_current.py --dry-run
python scripts/sync_todo_current.py
```

**Exemplo:** batch `lawfare-batch-1620-t222-t223-lacunas.json` gera 1 post timeline + 2 estudos e arquiva o arquivo.

---

### `merge_todo_pending.py` — conflitos de ID (legado)

Resolve renumeracao de batches antigos com colisão de faixas:

| Origem | Destino |
|--------|---------|
| Biomm 1481–1500 | 1527–1546 |
| Zema 185–188 | 1547–1550 |
| Homeschooling | 1551 |
| Thematic 189 | 190 |

```bash
python scripts/merge_todo_pending.py --dry-run
python scripts/merge_todo_pending.py
```

> Preferir `sync_todo_current.py` para fila editorial atual. Usar `merge_todo_pending.py` apenas para batches históricos documentados.

---

### `merge_todo_batches.py` — merge por regras de faixa

Merge de batches todo em `lawfare.json` + posts, com regras fixas (Biazucci 1511–1513, crise 1514–1524, Ramagem 1525–1526).

```bash
python scripts/merge_todo_batches.py --dry-run
python scripts/merge_todo_batches.py
python scripts/merge_todo_batches.py --force-posts    # sobrescreve posts existentes
python scripts/merge_todo_batches.py --skip-xarticles # pula conversão X Article
```

---

### `merge_todo_json.py` — merge genérico multi-schema

Processa qualquer JSON em `_data/todo/` com schemas variados (`instancia_padrao`, `entries[]`, `assuntos[]`, objeto único).

```bash
python scripts/merge_todo_json.py --dry-run
python scripts/merge_todo_json.py
python scripts/merge_todo_json.py --force   # sobrescreve posts existentes
```

---

### `sync_todo_batches.py` / `sync_new_todo_batches.py` — batches pontuais

Scripts **one-shot** para rodadas editoriais específicas (IDs a partir de 1577; Sepse T-210–T-214; decano Gilmar Mendes). Não são genéricos — ler cabeçalho do arquivo antes de executar.

```bash
python scripts/sync_todo_batches.py --dry-run
python scripts/sync_todo_batches.py

python scripts/sync_new_todo_batches.py
```

---

## Geração de posts

### `gerar_posts_unified_corpus.py`

Gera posts a partir de `_data/lawfare-unified-corpus.json` (respeita `jekyll_filename`, conexões P01–P12).

```bash
# Apenas arquivos ausentes em _posts/
python scripts/gerar_posts_unified_corpus.py

# Regenerar tudo (cuidado: sobrescreve)
python scripts/gerar_posts_unified_corpus.py --force
```

---

### `gerar_posts_from_lawfare.py` — legado Mare Liberum

Gera posts a partir de `_data/lawfare-mare-liberum-timeline.json` (não usa `lawfare.json` principal).

```bash
python scripts/gerar_posts_from_lawfare.py
```

---

### `gerar_posts_timeline_124_145.py`

Batch histórico: `_data/lawfare-timeline-124-145.json` → `_posts/`.

```bash
python scripts/gerar_posts_timeline_124_145.py
```

---

### `gerar_penduricalhos_de_json.py`

Posts categoria `penduricalhos` + entradas em `lawfare.json` a partir de `tools/penduricalhos-novos-eventos-*.json`.

```bash
python scripts/gerar_penduricalhos_de_json.py
```

---

### `gerar_artigos.py`

Gera Markdown a partir de JSON com campos `data`, `acao`, `descricao_completa`, `violacao`, `envolvidos`, `fontes`.

```bash
python scripts/gerar_artigos.py _data/meu-batch-eventos.json
```

---

### `crise-diplomatica-AJUSTADA.py`

Gera posts Jekyll para categoria crise diplomática a partir de JSON (`assuntos[]` ou array direto).

```bash
python scripts/crise-diplomatica-AJUSTADA.py _data/export-crise-diplomatica.json
python scripts/crise-diplomatica-AJUSTADA.py _data/batch.json --output-dir crise-diplomatica
```

---

### `publish_json_entries.py` — legado hardcoded

Publica listas fixas de arquivos (`entries-153-158.json`, `lawfare-1441-1447.json`, etc.). Editar o array `files` no script antes de rodar.

```bash
python scripts/publish_json_entries.py
```

---

## Exportação e filtros (JSON / posts)

### `extrair_posts_para_json.py`

Export reverso: `_posts/` → JSON estruturado (front matter + corpo).

```bash
python scripts/extrair_posts_para_json.py
python scripts/extrair_posts_para_json.py --output _data/posts-extraidos.json
python scripts/extrair_posts_para_json.py --posts-dir _posts/lawfare --limit 50
python scripts/extrair_posts_para_json.py --no-pretty
```

---

### `filtrar_lawfare_bolsonaro.py`

Extrai subset temático de `lawfare.json` (lawfare, dossiê, vaza toga + keywords Bolsonaro).

```bash
python scripts/filtrar_lawfare_bolsonaro.py
python scripts/filtrar_lawfare_bolsonaro.py \
  --input _data/lawfare.json \
  --output _data/lawfare-ataques-bolsonaro-apoiadores.json
```

**Alternativa atualizada:** timeline deduplicada em `_data/export-bolsonaro-timeline.json` via `python tools/export_bolsonaro_timeline.py`.

---

## Merge pontual em `lawfare.json`

Scripts one-shot para checkpoints históricos — usar só se o caso se aplicar.

| Script | Função |
|--------|--------|
| `merge_abr_mai_2026_lawfare.py` | Insere posts `2026-04-*` e `2026-05-*` ausentes em `lawfare.json` |
| `unificar_timeline_em_lawfare_full.py` | Mescla `lawfare-timeline-124-145.json` em `lawfare-full.json` |
| `adicionar_entradas_export_15abr2026.py` | Import checkpoint abr/2026 (FPA, Persona Non Grata, Gilmar) |

```bash
python scripts/merge_abr_mai_2026_lawfare.py
python scripts/unificar_timeline_em_lawfare_full.py
python scripts/adicionar_entradas_export_15abr2026.py
```

---

## Dados eleitorais / farmacêutico

Análise externa (não altera o site Jekyll). Requer CSVs do TSE e Receita Federal.

### `pipeline_tse_farmaceutico.py`

```bash
python scripts/pipeline_tse_farmaceutico.py \
  --receitas receitas_candidatos_2022_BRASIL.csv \
  --estabelecimentos Estabelecimentos0.csv \
  --ano 2022 \
  --saida ranking_partidos_farma_2022.csv
```

### `lawfare_timeline_farma_2022.py`

Notebook-style: editar caminhos `ARQUIVO_RECEITAS_TSE` e `ARQUIVO_EMPRESAS_RF` no topo do arquivo e executar.

```bash
python scripts/lawfare_timeline_farma_2022.py
```

---

## Imagens (PowerShell / Python)

| Script | Uso |
|--------|-----|
| `optimize_images.ps1` | Otimiza pasta `assets/img` (resize, compress, WebP) |
| `convert_to_webp.ps1` | Converte uma imagem |
| `convert_to_webp_python.py` | Fallback Python (Pillow) |
| `convert_estudos_webp.ps1` | Capas em `assets/img/estudos` |

```powershell
# Otimizar todas as imagens (dry-run)
.\scripts\optimize_images.ps1 -DryRun

# Otimizar com qualidade customizada
.\scripts\optimize_images.ps1 -Path assets\img -Quality 82

# Converter uma imagem
.\scripts\convert_to_webp.ps1 -ImagePath assets\img\lawfare-timeline.png -Quality 80

# Capas dos estudos
.\scripts\convert_estudos_webp.ps1
.\scripts\convert_estudos_webp.ps1 -Force -Quality 82 -IncludeArtigosHero
```

```bash
python scripts/convert_to_webp_python.py assets/img/exemplo.png 80
```

Guia detalhado: [`optimize_images.md`](./optimize_images.md).

---

## Referência rápida

| Objetivo | Comando |
|----------|---------|
| Publicar fila `_data/todo/` | `python scripts/sync_todo_current.py` |
| Validar IDs pós-merge | `pwsh -File tools/validate-ids.ps1` |
| Sync mapa de IDs | `python tools/sync_corpus_ids.py` |
| Posts → JSON | `python scripts/extrair_posts_para_json.py` |
| Timeline Bolsonaro | `python tools/export_bolsonaro_timeline.py` |
| Gerar posts unified | `python scripts/gerar_posts_unified_corpus.py` |
| Otimizar imagens | `.\scripts\optimize_images.ps1` |

---

## Relacionados

- Ferramentas diárias: [`tools/`](../tools/) e tabela em [`README.md`](../README.md)
- Metodologia e schema: [`METHODOLOGY.md`](../METHODOLOGY.md)
- Fila editorial: [`TODO.md`](../TODO.md) · notas em [`_data/todo/todo.md`](../_data/todo/todo.md)
- Sync de IDs para agentes: [`tools/instrucao-claude-ai-ids.md`](../tools/instrucao-claude-ai-ids.md)

*Atualizado: 2026-07-18*
