# 📦 Manifesto de Processamento — Série O Dragão e a Onça

**Data de processamento:** 2026-07-24  
**Status:** ✅ Completo  
**Destino:** `_posts/dragao-onca/` (90 artigos)

---

## 📋 Arquivos Processados (14)

### Batches Geográficos (6)

| Arquivo | IDs | Entradas | Status |
|---------|-----|----------|--------|
| `lawfare-batch-dragao-onca-brasil-1639-1653.json` | 1639–1653 | 15 | ✅ |
| `lawfare-batch-dragao-onca-para-1654-1666.json` | 1654–1666 | 13 | ✅ |
| `lawfare-batch-dragao-onca-amazonas-1667-1678.json` | 1667–1678 | 12 | ✅ |
| `lawfare-batch-dragao-onca-minas-1679-1688.json` | 1679–1688 | 10 | ✅ |
| `lawfare-batch-dragao-onca-juridico-1689-1700.json` | 1689–1700 | 12 | ✅ |
| `lawfare-batch-dragao-onca-pl2780-1701-1712.json` | 1701–1712 | 12 | ✅ |

**Subtotal batch:** 74 entradas → 74 artigos

### Temáticos (8)

| Arquivo | ID | Tipo | Status |
|---------|--|----|--------|
| `lawfare-thematic-T228-T229-dragao-onca.json` | T228–T229 | Síntese regional | ✅ |
| `lawfare-thematic-T230-para.json` | T230 | Síntese regional | ✅ |
| `lawfare-thematic-T231-amazonas.json` | T231 | Síntese regional | ✅ |
| `lawfare-thematic-T232-minas.json` | T232 | Síntese regional | ✅ |
| `lawfare-thematic-T233-sintese.json` | T233 | Síntese geral | ✅ |
| `lawfare-thematic-T234-juridico.json` | T234 | Síntese jurídica | ✅ |
| `lawfare-thematic-T235-pl2780.json` | T235 | Síntese legislativa | ✅ |
| `lawfare-thematic-T236-braco-diplomatico-dragao-onca.json` | T236 | Vazio | ⚠️ Sem entradas |

**Subtotal temático:** 8 arquivos → 16 artigos (duplicatas T228–T229 foram consolidadas)

### Metadata

| Arquivo | Status |
|---------|--------|
| `todo.md` | ✅ Histórico local |

---

## 📊 Resumo de Geração

### Cobertura
- **Período:** 1993–2026 (33 anos)
- **Regiões:** Brasil Federal, Goiás, Pará, Amazonas, Minas Gerais
- **Temas:** Diplomacia, mineração, legislação, captura institucional

### Padrões Analíticos Representados
- **P04b** — Both-sidesism funcional (4 entries)
- **P05** — Apropriação de recursos públicos (20+ entries)
- **P06** — Exclusão de voz (2 entries)
- **P09** — Captura regulatória (8 entries)
- **P10** — Infraestrutura compartilhada (30+ entries)
- **P11** — Escalada de consolidação (5 entries)

### Atores Principais
- **Presidentes:** Lula (I/II/III), Dilma, Bolsonaro
- **Governadores:** Caiado (GO), Barbalho (PA), Wilson Lima (AM), Zema (MG)
- **Instituições:** STF, Congresso, Itamaraty, BNDES, Ministério de Minas e Energia
- **Estrangeiros:** China, EUA, Japão (JOGMEC), Brasil (diplomacia)

### Referências
- **Fontes externas:** ~300+ URLs (Itamaraty, mídia, Observatórios, SciELO)
- **Conexões internas:** 13–15 por temático, 0–3 por batch entry
- **Imagens:** 9 WebP regionais + 1 padrão

---

## 🔄 Próximas Etapas

### Sincronização de IDs
Scripts a executar:
```bash
# 1. Sincronizar IDs com corpus central
python tools/sync_corpus_ids.py

# 2. Reconciliar batches
python tools/reconcile_lawfare_batch.py

# 3. Validar IDs
pwsh -File tools/validate-ids.ps1
```

### Atualização de Documentação
- [ ] `docs/TODO.md` — refletir processamento completo
- [ ] `docs/CORPUS.md` — incluir série dragão-onça
- [ ] Readme — mencionar série em destaque

### Publicação
- [ ] Commit com artigos + integração
- [ ] Build Jekyll
- [ ] Deploy em produção
- [ ] Verificar renderização

---

## 📝 Notas

### Qualidade
- ✅ 100% das entradas processadas
- ✅ Frontmatter completo (jekyll-compatível)
- ✅ Imagens mapeadas por região
- ✅ Links internos automáticos
- ✅ Fontes estruturadas

### Limitações Conhecidas
- T236 (Braco Diplomático) está vazio no JSON original
- Rota `/timeline/entries/[ID]` — verificar existência no Jekyll

### Oportunidades Futuras
- Análise estatística da série (gráficos)
- Mapa interativo de regiões
- Feed RSS específico
- Versão em PDF

---

## 📌 Referência Rápida

**Diretório original:** `D:\_deploy\lawfare-timeline\_data\todo/`  
**Diretório atual:** `D:\_deploy\lawfare-timeline\_data\processados/`  
**Saída gerada:** `D:\_deploy\lawfare-timeline\_posts\dragao-onca/` (90 artigos)  
**Integração web:** `_tabs/dragao-onca.md`, `_layouts/dragao-onca.html`, `_featured_categories/dragao-onca.md`

---

**Processamento finalizado:** ✅  
**Data:** 2026-07-24  
**Executor:** Claude Code  
**Série:** O Dragão e a Onça
