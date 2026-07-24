# Instrução de Sincronização de IDs — Projeto lawfare-timeline
**Atualizado:** 2026-05-12  
**Script de validação:** `tools/validate-ids.ps1` (executar após qualquer merge)

---

## TL;DR — O que você DEVE saber antes de gerar IDs

| Variável | Valor atual | Fonte |
|---|---|---|
| Último ID confirmado em `lawfare.json` | **1448** | `lawfare.json` (fonte de verdade) |
| Próximo ID para NOVOS eventos main track | **1512** | (1449–1511 já reservados — ver abaixo) |
| Último ID temático confirmado | **188** | `claude.ai-corpus-ids-sync.json` |
| Próximo ID temático disponível | **189** | thematic track |

---

## 1. Dois sistemas de ID — não confundir

### 1A. `lawfare.json` — fonte de verdade do main track

Arquivo: `_data/lawfare.json`  
Estrutura: `{ "assuntos": [...], "total": 1448 }`

- IDs **sequenciais inteiros 1–1448**, sem gaps, sem duplicatas.
- Cada entrada representa um **evento histórico real** (decisão judicial, operação policial, escândalo institucional, etc.).
- Este arquivo é a **única fonte canônica** para o main track. Se um ID não existe aqui, não está no corpus principal.
- Último ID: **1448** — "TJMG Paga Acima Do Teto A Um Terço Dos Magistrados Em 2026" (2026-05-09)

### 1B. `posts-extraidos.json` — snapshot de _posts/ (IDs posicionais, NÃO usar para ID tracking)

Arquivo: `_data/posts-extraidos.json`  
Gerado por: `python scripts/extrair_posts_para_json.py`

- Contém **1509 artigos** extraídos de toda a pasta `_posts/` recursivamente.
- IDs atribuídos **positionally** (i+1 pela ordem alfabética dos arquivos `.md`).
- **Estes IDs NÃO correspondem aos IDs de `lawfare.json`**.  
  Exemplo: post na posição 1509 no arquivo extraído pode ser o ID 1448 em `lawfare.json`.
- Usado para: inventário de conteúdo publicado, não para geração de novos IDs.
- Delta: 1509 (posts) − 1448 (lawfare.json) = **61 artigos em `_posts/` sem entrada correspondente em `lawfare.json`** (incluem artigos temáticos, penduricalhos recentes, conteúdo auxiliar).

---

## 2. Faixas de ID reservadas — main track

```
[1–1448]      confirmed    lawfare.json (fonte de verdade)
[1449–1511]   batch_file_only  NÃO em lawfare.json — apenas em _data/ batch files
[1512+]       disponível   próximo ID livre para NOVOS eventos
```

### O que é `batch_file_only` (IDs 1449–1511)?

Entradas que foram **criadas em sessões anteriores** e salvas em arquivos separados em `_data/`, mas **ainda não foram mescladas em `lawfare.json`**. Elas existem e têm IDs atribuídos, mas lawfare.json ainda não as contém.

Conteúdo dos slots 1449–1511:
- **1449–1480**: gap potencial — 32 slots não atribuídos ainda (seriam necessários para um merge linear futuro)
- **1481–1496**: Bloco PCC/ʼNdrangheta — crime organizado transnacional (`_data/lawfare-1481-1496-pcc-ndrangheta.json`)
- **1497–1505**: PCC novos — Narco Fluxo, Carbono Oculto/Genial, Hezbollah, FARC, Yakuza, Antimáfia, CPI (`_data/pcc-novas-entradas-1497-1510.json`)
- **1506–1510**: não atribuídos
- **1511**: Erro judiciário — STJ nega indenização ao dentista preso 210 dias (`_data/lawfare-1481.json` reatribuído)

> **Decisão pendente:** o gap 1449–1480 precisa ser preenchido antes de qualquer merge das entradas PCC em `lawfare.json`. Alternativa: formalizar PCC como sub-corpus separado e não mesclar.

### Quando gerar novos IDs para eventos main track

Use **1512** como próximo disponível. Não use 1449–1511 — já reservados.

---

## 3. Thematic track — namespace separado

Arquivo de referência: `_data/claude.ai-corpus-ids-sync.json` (seção `tracks.thematic`)

- IDs **100–188** confirmados (89 entradas).
- Representam **artigos de análise, artefatos HTML, estudos temáticos** publicados em gosurf.site.
- **Namespace completamente separado do main track** — a colisão numérica com IDs de `lawfare.json` é intencional e esperada (ex: thematic ID 166 = artigo Benedito Gonçalves; main ID 166 = evento diferente em lawfare.json).
- Próximo ID temático disponível: **189**

IDs temáticos pendentes (pending, não confirmados):
- **180** — TSE seletividade punitiva (pronto para publicação)
- **189–196** — Operação Travessia (série de 6–9 entradas, planejado)

---

## 4. `lawfare-unified-corpus.json` — corpus consolidado para Jekyll

Arquivo: `_data/lawfare-unified-corpus.json`  
34 entradas com fontes verificadas (URLs reais), Jekyll-ready.

Distribuição de `id_corpus`:
- **Temáticos (100–999):** 166, 181, 182, 183, 185, 186, 187, 188 — artigos/análises
- **Main batch-only (1000+):** 1481–1505, 1511 — eventos PCC + erro judiciário

Campos Jekyll relevantes: `jekyll_categories`, `jekyll_filename`, `jekyll_date`, `jekyll_permalink`, `fontes_verificadas`.

Categorias válidas do projeto (apenas estas):
```
escandalos | estudos | operacoes | lawfare | stf | justica | bancos |
crise-diplomatica | decano | dossie | extravagancia | governo | impunidade |
indecoro | penduricalhos | tse | vazatoga | sabedoria
```

---

## 5. Regras para geração de novos IDs

### Para eventos no main track (acontecimentos históricos reais):
1. Verificar `last_id` em `lawfare.json` — atualmente **1448**
2. Reservar a partir de **1512** (nunca usar 1449–1511)
3. Atualizar `claude.ai-corpus-ids-sync.json`: `tracks.main.last_id` e `tracks.main.next_available`
4. Se adicionando ao batch PCC (faixa 1449–1511): verificar que o ID específico não foi atribuído

### Para artigos temáticos (análise estrutural, artefatos gosurf.site):
1. Verificar `last_id` em `tracks.thematic` — atualmente **188**
2. Usar **189+**
3. Atualizar `claude.ai-corpus-ids-sync.json`: `tracks.thematic.last_id` e `tracks.thematic.next_available`

### Nunca:
- Usar `posts-extraidos.json` IDs para referenciar entradas de `lawfare.json`
- Reutilizar IDs já marcados como `batch_file_only` sem verificar o arquivo batch específico
- Gerar IDs sem atualizar `claude.ai-corpus-ids-sync.json` e sem rodar `validate-ids.ps1`

---

## 6. Validação após qualquer operação de ID

```powershell
pwsh -File tools/validate-ids.ps1 -Verbose
```

Resultado esperado: **STATUS: OK** (zero erros) ou **STATUS: AVISO** (apenas aviso de batch-only, que é esperado).  
**STATUS: FALHOU** indica conflito real — não prosseguir com merge.

---

## 7. Fluxo de trabalho recomendado

```
Novo evento real  →  ID 1512+  →  adicionar em lawfare.json  →  atualizar sync  →  validar
Novo artigo gosurf →  ID 189+  →  adicionar em thematic entries  →  atualizar sync  →  validar
Merge PCC batch   →  preencher gap 1449-1480 primeiro  →  mesclar em lawfare.json  →  validar
Sync concluído    →  export automático para Google Drive (ver §9)
```

---

## 9. Export para Google Drive (ferramentas externas)

Após `python tools/sync_corpus_ids.py` ou `python scripts/sync_todo_current.py` atualizar
`_data/claude.ai-corpus-ids-sync.json`, o arquivo é copiado automaticamente para Google Drive
via `tools/gdrive_sync_export.py`.

**Configurar destino (uma vez):**

1. Copiar `_data/gdrive-sync-export.example.json` → `_data/gdrive-sync-export.json` (se ainda não existir)
2. Preencher `dest_dir` com o caminho absoluto da pasta no Drive, por exemplo:
   - `G:/Meu Drive/lawfare-timeline`
   - `C:/Users/SEU_USUARIO/Google Drive/lawfare-timeline`
3. Ou definir variável de ambiente (prioridade máxima):
   - `LAWFARE_GDRIVE_SYNC_DIR=G:/Meu Drive/lawfare-timeline`

**Manual:**

```powershell
python tools/gdrive_sync_export.py
python tools/gdrive_sync_export.py --dry-run
```

Se o Drive não estiver montado, o sync local conclui normalmente; apenas o export exibe aviso.

---

## 8. Arquivos de referência no repositório

| Arquivo | Papel |
|---|---|
| `_data/lawfare.json` | Fonte de verdade — main track IDs 1-1448 |
| `_data/claude.ai-corpus-ids-sync.json` | Mapa de sincronização entre tracks e sessões |
| `_data/lawfare-unified-corpus.json` | Corpus consolidado Jekyll-ready (34 entradas) |
| `_data/posts-extraidos.json` | Inventário de _posts/ (IDs posicionais, não usar para tracking) |
| `tools/validate-ids.ps1` | Script de validação — executar após qualquer merge |
| `tools/gdrive_sync_export.py` | Exporta sync JSON para Google Drive (automático após sync) |
| `_data/gdrive-sync-export.json` | Config do destino no Drive |
| `_data/lawfare-1481-1496-pcc-ndrangheta.json` | Batch PCC/ʼNdrangheta (1481-1496, batch_file_only) |
| `_data/pcc-novas-entradas-1497-1510.json` | Batch PCC novos (1497-1505, batch_file_only) |
