# 🐉 Script de Geração: Série O Dragão e a Onça

**Criado:** 2026-07-24  
**Arquivo:** `scripts/gerar_artigos_dragao_onca.py`  
**Saída:** `_posts/dragao-onca/*.md` (82 artigos)  
**Status:** ✅ Funcional (100% taxa de sucesso)

---

## 🎯 O que o script faz

1. **Lê dados** de JSONs em `_data/todo/`:
   - 6 batches geográficos (Brasil, Pará, Amazonas, Minas, Goiás, PL2780)
   - 8 arquivos temáticos (sínteses, jurídico, diplomático)

2. **Para cada entrada JSON**, gera um arquivo Markdown com:
   - Frontmatter Jekyll completo (title, date, image, tags, categories)
   - Seções estruturadas: Resumo, Atores, Instituições, Padrões, Análise, Fontes
   - Links internos para IDs relacionados
   - Links para pesquisa (Perplexity, Google, Wikipedia)
   - Imagens regionais automáticas (`/assets/img/dragao-onca-*.webp`)

3. **Relatório final** com estatísticas de geração

---

## 🚀 Como usar

### Executar geração completa
```bash
cd D:\_deploy\lawfare-timeline
python scripts/gerar_artigos_dragao_onca.py
```

### Com log
```powershell
cd D:\_deploy\lawfare-timeline
python scripts/gerar_artigos_dragao_onca.py | Tee-Object -FilePath "generate-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"
```

---

## 📋 Estrutura dos JSONs de entrada

Cada JSON tem:
```json
{
  "batch_meta": {
    "series": "O Dragão e a Onça — Capítulo ...",
    "range": [1639, 1653],
    "generated": "2026-07-22",
    "note": "Descrição do batch"
  },
  "entries": [
    {
      "id": "1639",
      "date": "1993-01-01",
      "title": "Título do evento",
      "summary": "Resumo curto",
      "category": "incidente_diplomatico",
      "actors": [
        {
          "name": "Nome da pessoa",
          "role": "Cargo",
          "institution": "Instituição"
        }
      ],
      "patterns": ["P05", "P10"],
      "evidence_status": "ev-confirmed",
      "sources": [
        {
          "title": "Título da fonte",
          "url": "https://...",
          "outlet": "Outlet/Media",
          "date": "2026-07-22"
        }
      ],
      "connections": ["id_1640", "id_1642"],
      "analise": "Texto de análise",
      "lacuna_investigativa": "O que falta investigar"
    }
  ]
}
```

---

## 📄 Estrutura de saída (arquivo .md)

### Frontmatter
```yaml
---
layout: post
title: "Título do evento"
description: "Resumo até 200 caracteres..."
date: 2004-05-01
image: /assets/img/dragao-onca-brasil-federal.webp
tags: ["incidente_diplomatico", "2004", "P10"]
categories: dragao-onca
timeline_id: 1642
status: confirmado
---
```

### Body (Markdown)
```markdown
# Título do evento

**Data:** 2004-05-01 | **ID:** 1642 | **Status:** confirmado

***

## 📋 Resumo

[Resumo da entrada]

### Resultado

[Resultado/consequência]

## 👥 Atores Envolvidos

- Nome (Cargo) [Instituição]
- ...

## 🏛️ Instituições

- Instituição 1
- Instituição 2

## 📊 Padrões Analíticos

- **P05** — Descrição do padrão
- **P10** — Descrição do padrão

## 🔍 Análise

[Análise contextual]

### Links para Pesquisa

- [🤖 Perplexity](...) 
- [🌐 Google](...)
- [📖 Wikipedia](...)

## 🔗 Fontes Externas

- [Título](URL) *Outlet* · Data

## 🔗 Artigos Relacionados

- [Entrada 1641](/timeline/entries/1641)

---

*Entrada gerada automaticamente • Série O Dragão e a Onça • lawfare-batch-dragao-onca-brasil-1639-1653*
```

---

## 🎨 Mapeamento de imagens

Script mapeia regiões para imagens WebP automaticamente:

| Região | Palavra-chave | Imagem |
|--------|---------------|--------|
| Brasil Federal | brasil, federal | `dragao-onca-brasil-federal.webp` |
| Pará | para | `dragao-onca-para.webp` |
| Amazonas | amazonas | `dragao-onca-amazonas.webp` |
| Minas Gerais | minas, minas-gerais | `dragao-onca-minas-gerais.webp` |
| Goiás | goias | `dragao-onca-goias.webp` |
| PL 2.780 | pl2780 | `dragao-onca-pl2780.webp` |
| Jurídico | juridico, braco-juridico | `dragao-onca-braco-juridico.webp` |
| Síntese | sintese | `dragao-onca-sintese.webp` |
| Padrão | (default) | `dragao-onca.webp` |

---

## ✨ Principais funções

### `generate_post_from_entry(entry, batch_name)`
Gera um artigo a partir de uma entrada JSON.
- Valida ID e título
- Cria frontmatter
- Monta seções do body
- Escreve arquivo .md

**Retorna:** (filepath, status_message)

### `process_batch_file(batch_file)`
Processa um arquivo JSON inteiro.
- Lê JSON
- Itera sobre entries
- Chama `generate_post_from_entry()`
- Retorna contagem (total, sucesso)

### `slugify(text, max_len=80)`
Converte texto em slug URL-safe.
- Remove acentos
- Lowercase
- Replace espaços por hífens
- Limite de 80 caracteres

### `resolve_region_image(batch_name)`
Mapeia nome do batch para imagem regional.
- Busca keywords no nome
- Retorna `/assets/img/[arquivo].webp`
- Fallback: `dragao-onca.webp`

### `generate_*_section(...)` 
Helpers para gerar seções:
- `generate_actors_section()` — Formata atores
- `generate_sources_section()` — Formata fontes com links
- `generate_connections_section()` — Links para IDs relacionados
- `generate_patterns_section()` — Padrões com descrições
- `generate_analysis_section()` — Análise + links de pesquisa
- `generate_lacunas_section()` — Lacunas investigativas

---

## 📊 Estatísticas de última geração (2026-07-24)

| Batch | Entradas | Sucesso | Taxa |
|-------|----------|---------|------|
| brasil-1639-1653 | 15 | 15 | 100% |
| para-1654-1666 | 13 | 13 | 100% |
| amazonas-1667-1678 | 12 | 12 | 100% |
| juridico-1689-1700 | 12 | 12 | 100% |
| minas-1679-1688 | 10 | 10 | 100% |
| pl2780-1701-1712 | 12 | 12 | 100% |
| **Temáticos** | 7 | 7 | 100% |
| **TOTAL** | **82** | **82** | **100%** |

---

## ⚠️ Limitações e TODO

### Melhorias futuras

1. **Arquivos temáticos (T228–T235)**
   - Têm estrutura diferente (sem `date`, sem `title`)
   - Geram nomes ruins: `-id228-sem-titulo.md`
   - TODO: Extrair `chapter` ou `title` de outro lugar

2. **Rota de links internos**
   - Atualmente: `/timeline/entries/[ID]`
   - Verificar se rota existe no Jekyll
   - Ajustar conforme necessário

3. **Validação pós-geração**
   - Testar renderização Jekyll
   - Verificar links (internos, Perplexity, Google)
   - Confirmar exibição de imagens

---

## 🔧 Configurações (início do script)

```python
ROOT = Path(__file__).resolve().parents[1]  # Raiz do projeto
TODO_DIR = ROOT / "_data" / "todo"          # Entrada (JSONs)
POSTS_DIR = ROOT / "_posts" / "dragao-onca" # Saída (Markdown)
ASSETS_DIR = ROOT / "assets" / "img"        # Imagens

REGION_IMAGE_MAP = {...}  # Mapeamento batch → imagem
DEFAULT_IMAGE = "dragao-onca.webp"  # Fallback
```

---

## 🐛 Troubleshooting

### Erro: `AttributeError: 'int' object has no attribute 'strip'`
**Causa:** IDs em formato inteiro em JSONs temáticos  
**Solução:** Converter para string: `str(entry.get("id", ""))`  
**Status:** ✅ CORRIGIDO na v1.1

### Erro: Arquivo não encontrado
**Causa:** `_data/todo/` não existe ou está vazio  
**Solução:** Verificar caminho e confirmar JSONs presentes

### Links quebrados
**Causa:** Rota `/timeline/entries/[ID]` não existe  
**Solução:** Ajustar URL no script conforme rotas reais do projeto

---

## 📝 Histórico de versões

**v1.1 (2026-07-24)**
- ✅ Corrigido bug de IDs inteiros
- ✅ 82 artigos gerados com sucesso
- ✅ Imagens regionais automáticas
- ✅ Links internos para IDs relacionados
- ✅ Seções de análise com pesquisa

**v1.0 (2026-07-24)**
- 🎉 Versão inicial
- Estrutura base + funções principais
- Processamento de 6 batches geográficos

---

## 📞 Referências

- **Script:** `scripts/gerar_artigos_dragao_onca.py`
- **Dados:** `_data/todo/lawfare-batch-dragao-onca-*.json`
- **Saída:** `_posts/dragao-onca/*.md`
- **Imagens:** `assets/img/dragao-onca-*.webp`
- **Documentação interna:** `.claude/docs/` (este arquivo)
