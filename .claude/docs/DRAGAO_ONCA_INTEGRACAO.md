# 🐉 Integração: O Dragão e a Onça com o Site Jekyll

**Data:** 2026-07-24  
**Status:** ✅ Implementado  
**Componentes:** Tab + Layout + Featured Category

---

## 📋 O que foi criado

### 1. **Tab de Navegação**
📁 `_tabs/dragao-onca.md`

```yaml
title: O Dragão e a Onça
layout: dragao-onca
icon: fas fa-dragon
redirect: /categories/dragao-onca/
order: 1
```

- **Função:** Adiciona item no menu principal (sidebar)
- **Posição:** `order: 1` = primeira aba (depois do Home)
- **Ícone:** Dragão (FontAwesome `fas fa-dragon`)
- **Rota:** `/categories/dragao-onca/`

### 2. **Layout Customizado**
📁 `_layouts/dragao-onca.html`

**Seções:**
1. **Descrição da série** — a partir de `_featured_categories/dragao-onca.md`
2. **🏛️ Capítulos Temáticos** — cards dos 7 temáticos (T228–T235)
   - Sínteses estruturadas por região
   - Padrões analíticos incluídos
   - Links para cada capítulo
3. **📅 Timeline Completa** — todas as entradas (1639–1712)
   - Organizadas por ano
   - Com ID, resumo compacto
   - Data formatada
4. **🔗 Categorias Relacionadas** — links para:
   - Crise Diplomática
   - Operações
   - Lawfare
   - Escândalos

**Estilo:**
- Cards com hover effect
- Timeline visual com anos destacados
- Badges de identificação
- Responsive (desktop, tablet, mobile)

### 3. **Categoria Featured**
📁 `_featured_categories/dragao-onca.md`

```yaml
layout: dragao-onca
type: category
title: O Dragão e a Onça 🐉
slug: dragao-onca
sidebar: true
description: [descrição longa da série]
```

- **Função:** Metadados e descrição da série
- **Exibição:** No topo da página de categoria
- **Sidebar:** Ativada (`true`)

---

## 🔗 Como funciona a navegação

```
Menu Principal (Sidebar)
    ├── Home
    ├── O Dragão e a Onça  ← NOVO
    │   ├── Descrição
    │   ├── 7 Capítulos Temáticos
    │   └── 74 Artigos Timeline
    ├── Crise Diplomática
    ├── Operações
    └── ...
```

**URL:** `https://lawfare-timeline.vercel.app/categories/dragao-onca/`

---

## 📊 Estrutura de dados

### Artigos da série
- **Total:** 82 (74 batch + 8 temáticos)
- **Localização:** `_posts/dragao-onca/`
- **Naming:** `YYYY-MM-DD-id[NUM]-[slug].md` ou `YYYY-MM-DD-t[NUM]-[slug].md`
- **Frontmatter:**
  ```yaml
  categories: dragao-onca
  timeline_id: [numero]
  tags: [categoria, ano, padroes]
  image: /assets/img/dragao-onca-[region].webp
  ```

### Padrões de conexão
- **Batch entries:** Campo `connections` (links bidirecionais)
- **Temáticos:** Campo `connects_to_main_ids` (links para 13–15 IDs cada)

### Imagens
- 9 WebP regionais (`dragao-onca-*.webp`)
- 1 padrão (`dragao-onca.webp`)
- Localização: `assets/img/`

---

## 🎯 Fluxo de visitação

### Caminho 1: Exploração Linear
1. Usuário clica em "O Dragão e a Onça" no menu
2. Vê descrição e 7 capítulos temáticos (sínteses)
3. Clica em um capítulo (ex: "Brasil Federal")
4. Lê a síntese (temático)
5. Vê links para 15 IDs relacionados
6. Clica em um ID → artigo específico
7. Lê o artigo com fontes, atores, padrões
8. Usa links internos para explorar mais

### Caminho 2: Timeline
1. Usuário acessa a série
2. Desce para "📅 Timeline Completa"
3. Explora por ano (1993→2026)
4. Clica em um artigo
5. Lê e segue links relacionados

### Caminho 3: Contexto
1. Usuário lê artigo de "Crise Diplomática"
2. Nota que está relacionado à série "Dragão e Onça"
3. Clica no link relacionado
4. Explora a série completa

---

## 🔄 Ciclos de atualização

### Quando gerar novos artigos
```bash
cd D:\_deploy\lawfare-timeline
python scripts/gerar_artigos_dragao_onca.py
```

**Resultado:**
- Atualiza/cria arquivos em `_posts/dragao-onca/`
- Mantém estrutura de nomes
- Preserva frontmatter Jekyll
- Gera 100% dos artigos

### Publicação
```bash
# Build local
bundle exec jekyll build

# Deploy (Vercel)
git add .
git commit -m "feat: dragao-onca series + artigos"
git push origin main
```

---

## ✨ Recursos especiais

### 1. **Padrões Analíticos Coloridos**
Cada artigo mostra padrões P04b–P11 com:
- Título do padrão
- Descrição breve
- Contexto da entrada

### 2. **Links para Pesquisa**
Cada artigo tem seção "🔍 Análise" com:
- [🤖 Perplexity](https://www.perplexity.ai/)
- [🌐 Google](https://www.google.com/)
- [📖 Wikipedia](https://pt.wikipedia.org/)

### 3. **Referências Internas Automáticas**
Seção "🔗 Artigos Relacionados" lista:
- IDs da série (campo `connections`)
- IDs principais (campo `connects_to_main_ids`)
- Links para `/timeline/entries/[ID]`

### 4. **Fontes Estruturadas**
Seção "🔗 Fontes Externas" com:
- Título da fonte
- URL clicável
- Outlet (mídia/instituição)
- Data da publicação

---

## 📱 Responsividade

### Desktop
- Cards lado a lado (2 colunas)
- Timeline expandida
- Sidebar fixo

### Tablet
- Cards empilhados (1 coluna)
- Timeline normal
- Sidebar colapsável

### Mobile
- Cards full-width
- Timeline compacta
- Menu responsivo

---

## 🔐 SEO & Meta tags

Cada artigo inclui:
- `<title>` — Título do evento
- `<meta description>` — Resumo até 200 chars
- `<meta image>` — Asset regional
- `<meta tags>` — Categoria, ano, padrões
- `og:image` — Social preview
- `canonical` — URL canônica

**Slug:** URL-friendly, sem acentos

---

## 🚀 Próximos passos (opcional)

1. **Adicionar mapa interativo**
   - Regiões (GO, PA, AM, MG)
   - Timeline visual
   - Hover mostra artigos

2. **Criar página de análise**
   - Estatísticas (entradas por ano)
   - Padrões mais comuns
   - Atores mais frequentes
   - Cronograma visual

3. **Gráfico de conexões**
   - D3.js ou similar
   - Nós = IDs
   - Edges = conexões
   - Filtro por padrão/região

4. **Feed RSS específico**
   - `/feed-dragao-onca.xml`
   - Apenas artigos da série
   - Últimas publicações

5. **Versão em PDF**
   - Série completa
   - Índice navegável
   - Fontes incluídas

---

## 📞 Troubleshooting

### Série não aparece no menu
- ✅ Verificar `_tabs/dragao-onca.md` existe
- ✅ Verificar `order: 1` está correto
- ✅ Rodar `bundle exec jekyll build`
- ✅ Limpar cache do navegador

### Artigos não carregam
- ✅ Verificar arquivos em `_posts/dragao-onca/`
- ✅ Verificar frontmatter: `categories: dragao-onca`
- ✅ Verificar encoding UTF-8

### Imagens não aparecem
- ✅ Verificar `assets/img/dragao-onca-*.webp` existe
- ✅ Verificar path no frontmatter: `/assets/img/dragao-onca-*.webp`
- ✅ Verificar permissões de arquivo

### Links internos quebrados
- ✅ Verificar rota: `/timeline/entries/[ID]`
- ✅ Ajustar URL se necessário
- ✅ Testar em navegador

---

## 📊 Estatísticas pós-integração

| Métrica | Valor |
|---------|-------|
| Artigos na série | 82 |
| Capítulos temáticos | 7 |
| Entradas batch | 74 |
| Período coberto | 1993–2026 (33 anos) |
| Padrões únicos | 6 (P04b, P05, P06, P09, P10, P11) |
| Regiões abrangidas | 5 (GO, PA, AM, MG, BR federal) |
| Fontes externas | ~300+ |

---

## 🎓 Referência rápida

**Encontrar série no site:**
- URL: `/categories/dragao-onca/`
- Menu: "O Dragão e a Onça" (1ª aba)
- Ícone: 🐉

**Regenerar artigos:**
```bash
python scripts/gerar_artigos_dragao_onca.py
```

**Atualizar descrição:**
- Editar: `_featured_categories/dragao-onca.md`

**Ajustar layout:**
- Editar: `_layouts/dragao-onca.html`

**Mudar ordem no menu:**
- Editar: `_tabs/dragao-onca.md` → `order: [numero]`

---

**Integração completa:** ✅  
**Artigos gerados:** 82 ✅  
**Link no menu:** ✅  
**Pronto para publicar:** ✅
