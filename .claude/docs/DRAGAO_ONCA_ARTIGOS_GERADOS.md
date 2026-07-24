# 🐉 Série O Dragão e a Onça — Artigos Gerados

**Data de geração:** 2026-07-24  
**Total de artigos:** 82  
**Taxa de sucesso:** 100%  
**Localização:** `_posts/dragao-onca/`

---

## 📊 Resumo por Batch

| Batch | Região/Tema | Entradas | IDs | Status |
|-------|-------------|----------|-----|--------|
| brasil-federal | Brasil (Federal) | 15 | 1639–1653 | ✅ Gerado |
| para | Pará | 13 | 1654–1666 | ✅ Gerado |
| amazonas | Amazonas | 12 | 1667–1678 | ✅ Gerado |
| juridico | Jurídico/PL2780 | 12 | 1689–1700 | ✅ Gerado |
| minas | Minas Gerais | 10 | 1679–1688 | ✅ Gerado |
| pl2780 | PL 2.780 (Minerais Críticos) | 12 | 1701–1712 | ✅ Gerado |
| **Temáticos** | Sínteses regionais | 7 | T228–T235 | ⚠️ Parcial |
| **Vazio** | Braco Diplomático | 0 | T236 | — |

---

## ✨ Recursos Incluídos em Cada Artigo

### Frontmatter
```yaml
layout: post
title: [do JSON]
description: [resumo de até 200 chars]
date: [YYYY-MM-DD]
image: /assets/img/dragao-onca-[region].webp
tags: [category, year, patterns]
categories: dragao-onca
timeline_id: [ID numérico]
status: [confirmado/draft/etc]
```

### Seções do Body

1. **Título e Metadados** — Data, ID, Status
2. **📋 Resumo** — Resumo da entrada
3. **Resultado** — Consequências/impacto (quando disponível)
4. **👥 Atores Envolvidos** — Lista formatada de atores com roles e instituições
5. **🏛️ Instituições** — Órgãos públicos/privados envolvidos
6. **⚖️ Base Jurídica** — Instrumentos legais (quando aplicável)
7. **📊 Padrões Analíticos** — Padrões P04b–P11 com descrições
8. **❓ Lacunas Investigativas** — Pontos não confirmados
9. **🔍 Análise** — Interpretação contextual
   - Links para Perplexity, Google, Wikipedia
10. **🔗 Fontes Externas** — URLs com outlet + data
11. **🔗 Artigos Relacionados** — IDs conectados (`connections` do JSON)

---

## 📁 Estrutura de Arquivos

```
_posts/dragao-onca/
├── YYYY-MM-DD-id[NUM]-[slug].md     (Batch entries: 1639–1712)
├── -id[T-NUM]-[slug].md              (Temáticos: T228–T235)
└── ...
```

### Exemplo de Nome
- `2004-05-01-id1642-lula-visita-a-china-criacao-da-cosban-comissao-sino-brasileira-de-alto-nivel-de.md`

---

## 🎨 Imagens (Assets)

Cada artigo referencia uma imagem regional automaticamente:

| Região | Imagem |
|--------|--------|
| Brasil (Federal) | `dragao-onca-brasil-federal.webp` |
| Pará | `dragao-onca-para.webp` |
| Amazonas | `dragao-onca-amazonas.webp` |
| Minas Gerais | `dragao-onca-minas-gerais.webp` |
| Goiás | `dragao-onca-goias.webp` |
| PL 2.780 | `dragao-onca-pl2780.webp` |
| Jurídico | `dragao-onca-braco-juridico.webp` |
| Síntese | `dragao-onca-sintese.webp` |
| Padrão | `dragao-onca.webp` |

Todas em: `assets/img/dragao-onca-*.webp`

---

## 🔗 Referências Internas

Cada artigo inclui seção **"Artigos Relacionados"** que lista IDs conectados:

```markdown
## 🔗 Artigos Relacionados

Entradas conectadas nesta série:

- [Entrada 1641](/timeline/entries/1641)
- [Entrada 1642](/timeline/entries/1642)
```

**Padrão de URL:** `/timeline/entries/[ID]`

---

## ⚠️ Observações e Próximos Passos

### Melhorias Futuras

1. **Arquivos temáticos (T228–T235)**
   - Têm estrutura diferente (sem `date`, sem `title`)
   - Atualmente geram nomes de arquivo ruins: `-id228-sem-titulo.md`
   - Recomendação: Revisar JSONs temáticos e melhorar script para extrair `chapter` ou `title`

2. **Links internos**
   - URLs para IDs relacionados usam padrão `/timeline/entries/[ID]`
   - Confirmar se essa rota existe no projeto Jekyll
   - Alternativa: ajustar para `/dragao-onca/entries/[ID]`

3. **Validação visual**
   - Testar renderização em navegador
   - Verificar exibição de imagens
   - Confirmar funcionamento dos links (Perplexity, Google, Wikipedia, internos)

4. **Integração com site**
   - Rodar `jekyll build` para confirmar geração de HTML
   - Publicar em staging/produção
   - Atualizar navegação principal para linkificar série

### Script de Geração

**Localização:** `scripts/gerar_artigos_dragao_onca.py`

**Como executar:**
```bash
cd D:\_deploy\lawfare-timeline
python scripts/gerar_artigos_dragao_onca.py
```

**Saída:** Gera/atualiza todos os arquivos `.md` em `_posts/dragao-onca/`

---

## 📈 Estatísticas

- **Total de entradas processadas:** 82
- **Taxa de sucesso:** 100%
- **Palavras-chave por artigo:** ~150–300 (resumo)
- **Padrões analíticos:** ~1–3 por entrada
- **Fontes externas:** ~1–5 por entrada
- **Referências internas (conexões):** 0–3 por entrada

---

## 🔍 Exemplo de Artigo Completo

Ver: `_posts/dragao-onca/2004-05-01-id1642-lula-visita-a-china-criacao-da-cosban-comissao-sino-brasileira-de-alto-nivel-de.md`

**Destaques:**
- Frontmatter estruturado
- Resumo + Resultado
- Atores com roles e instituições
- Padrão analítico (P10) com explicação
- Análise contextual
- Fonte externa (Itamaraty)
- Referência interna (ID 1641)
- Links para pesquisa

---

## 🛠️ Troubleshooting

### Problema: Artigos temáticos com nomes ruins
**Causa:** JSONs temáticos não têm `date` ou `title`  
**Solução:** Revisar estrutura dos JSONs ou melhorar lógica de fallback

### Problema: Links internos quebrados
**Causa:** Rota `/timeline/entries/[ID]` não existe  
**Solução:** Ajustar URL no script ou criar rota no Jekyll

### Problema: Imagens não aparecem
**Causa:** Assets não estão em `assets/img/`  
**Solução:** Confirmar que arquivos `.webp` existem e são acessíveis

---

## 📞 Suporte

Para regenerar artigos, executar script e verificar logs:

```powershell
cd D:\_deploy\lawfare-timeline
python scripts/gerar_artigos_dragao_onca.py 2>&1 | Tee-Object -FilePath "logs/gerar_artigos_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
```

---

**Gerado por:** Claude Code  
**Série:** O Dragão e a Onça  
**Período:** 1639–1712 (74 entries) + T228–T235 (7 temáticos) + 1 vazio
