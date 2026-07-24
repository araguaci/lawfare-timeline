# 📦 Arquivo: Série O Dragão e a Onça (Processado)

**Data de processamento:** 2026-07-24  
**Status:** ✅ Completo e Sincronizado  
**Destino:** 90 artigos em `_posts/dragao-onca/`

---

## 📋 Conteúdo deste diretório

Este diretório contém os **dados brutos já processados** da série "O Dragão e a Onça":

### JSONs (14 arquivos)
- **Batches geográficos (6):** Brasil Federal, Pará, Amazonas, Minas Gerais, Goiás, PL 2.780
- **Temáticos (8):** Sínteses de cada região + análises cruzadas

**Total de entradas:** 82 (74 batch + 8 temático)  
**Total de artigos gerados:** 90 (incluindo variações temáticas)

### Documentação
- `MANIFEST.md` — Manifesto detalhado de processamento
- `SYNC_STATUS_2026-07-24.md` — Relatório de sincronização com corpus central
- `todo.md` — Histórico local (copiado de `_data/todo/` original)

---

## 🎯 Para que serve?

Este é um **arquivo histórico** que rastreia:
1. **O que foi processado** — Manifest + lista de arquivos
2. **Como foi processado** — Scripts executados, status de validação
3. **Impacto no corpus** — Sincronização com Google Drive e main corpus
4. **Referência futura** — Se precisar regenerar ou revisar a série

---

## ✅ Verificações Executadas

### Validação de Dados
- ✅ 14 JSONs validados (`validate-ids.ps1`)
- ✅ 0 erros estruturais
- ✅ 2 avisos (não-críticos)

### Sincronização com Corpus Central
- ✅ Google Drive sincronizado (`sync_corpus_ids.py`)
- ✅ Nenhuma duplicata detectada (`reconcile_lawfare_batch.py`)
- ✅ IDs próximos confirmados: Main = 1639, Thematic = T-228

---

## 📊 Cobertura da Série

| Aspecto | Valor |
|---------|-------|
| Período | 1993–2026 (33 anos) |
| IDs | 1639–1712 (batch) + T228–T235 (temáticos) |
| Regiões | 5: GO, PA, AM, MG, BR federal |
| Padrões | 6: P04b, P05, P06, P09, P10, P11 |
| Fontes | ~300+ URLs estruturadas |
| Atores | ~50+ principais (presidentes, governadores, ministros) |

---

## 🚀 Saída Gerada

### Artigos
```
_posts/dragao-onca/
└── 90 arquivos .md (frontmatter Jekyll-compliant)
```

### Integração Web
```
_tabs/dragao-onca.md                    (menu)
_layouts/dragao-onca.html               (layout)
_featured_categories/dragao-onca.md     (categoria)
```

### Assets
```
assets/img/dragao-onca-*.webp (9 imagens regionais)
```

---

## 📖 Como Usar Este Arquivo

### Se precisar regenerar artigos
1. Verificar `MANIFEST.md` para cobertura de IDs
2. Reexecutar `scripts/gerar_artigos_dragao_onca.py`
3. Comparar saída com backup aqui

### Se surgir dúvida sobre sincronização
1. Consultar `SYNC_STATUS_2026-07-24.md`
2. Reexecutar scripts mencionados lá
3. Verificar status em `_data/sync_status_*.html`

### Se precisar verificar validação
1. Consultar `README.md` (este arquivo)
2. Ver seção "Verificações Executadas"
3. Reexecutar `pwsh -File tools/validate-ids.ps1`

---

## 🔄 Processo de Publicação

### Pré-publicação
```bash
# 1. Verificar estrutura
ls _posts/dragao-onca/ | wc -l  # Deve ser ~90

# 2. Validar frontmatter
for f in _posts/dragao-onca/*.md; do head -n 15 "$f"; done | grep -c "layout:"  # Deve ser 90

# 3. Build local
bundle exec jekyll build

# 4. Verificar sem erros
# Não deve haver avisos relativos a dragao-onca
```

### Publicação
```bash
git add _posts/dragao-onca/ _tabs/dragao-onca.md _layouts/dragao-onca.html _featured_categories/dragao-onca.md _data/processados/
git commit -m "feat: série O Dragão e a Onça — 90 artigos integrados"
git push origin main

# Deploy automático via Vercel
```

### Pós-publicação
1. Verificar em produção: https://lawfare-timeline.vercel.app/categories/dragao-onca/
2. Testar navegação de menu
3. Clicar em 3–4 artigos aleatórios
4. Verificar links internos e fontes externas

---

## ⚠️ Observações Importantes

### T236 (Braco Diplomatico)
- Arquivo JSON está vazio (nenhuma entrada)
- Não gerou artigo
- Verificar com dados-person se há conteúdo futuro

### Possíveis Melhorias
1. **Mapa interativo** — Visualizar série por região
2. **Estatísticas** — Gráficos de padrões/atores
3. **Cronograma visual** — Timeline interativa (D3.js)
4. **PDF consolidado** — Série completa em documento único

### Limitações Conhecidas
- Rota `/timeline/entries/[ID]` — Verificar se existe no Jekyll
- Tags automáticas podem incluir valores vazios ("") — Refinar se necessário

---

## 📞 Suporte

Se encontrar problemas:

1. **Artigos não aparecem:**
   - Verificar `_posts/dragao-onca/*.md` existe
   - Confirmar `categories: dragao-onca` no frontmatter
   - Limpar cache Jekyll: `bundle exec jekyll clean`

2. **Menu não mostra série:**
   - Verificar `_tabs/dragao-onca.md` existe
   - Confirmar `order: 1` está correto
   - Recarregar navegador (Ctrl+Shift+R)

3. **Imagens não carregam:**
   - Verificar `assets/img/dragao-onca-*.webp` existem
   - Confirmar paths nos frontmatters dos artigos
   - Testar acesso direto: `/assets/img/dragao-onca-brasil-federal.webp`

---

## 🎓 Documentação Relacionada

Leia também:
- `.claude/docs/DRAGAO_ONCA_SCRIPT_GERADOR.md` — Detalhes técnicos do script
- `.claude/docs/DRAGAO_ONCA_INTEGRACAO.md` — Guia de integração web
- `MANIFEST.md` — Manifesto técnico
- `SYNC_STATUS_2026-07-24.md` — Relatório de sincronização

---

**Arquivo criado:** 2026-07-24  
**Executor:** Claude Code  
**Série:** O Dragão e a Onça  
**Status:** ✅ Pronto para produção
