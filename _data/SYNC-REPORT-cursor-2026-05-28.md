# SYNC REPORT — lawfare-timeline
**Gerado:** 2026-05-28  
**Sessão:** claude.ai → Cursor.ai handoff  
**Repositório:** https://github.com/araguaci/lawfare-timeline  
**Site ao vivo:** https://lawfare-timeline.vercel.app (75 páginas confirmadas)

---

## 1. ESTADO ATUAL DOS TRACKS

### Main track — lawfare.json

| Faixa | Status | Ação necessária |
|-------|--------|-----------------|
| 1–1526 | ✅ confirmed em lawfare.json | nenhuma |
| 1449–1510 | ⚠️ batch_file_only (_data/) | NÃO tocar — PCC namespace protegido (1481-1500) |
| 1527–1551 | 🟡 jekyll_published, merge pendente | `merge_todo_pending.py` → `validate-ids.ps1` |
| 1552–1571 | 🟡 jekyll_published, merge pendente | idem — após 1527-1551 |
| 1572–1576 | 🔴 produced, não commitado | copiar para `_data/todo/` → merge após 1527-1571 |
| 1577+ | disponível após merge | próximo ID livre |

**Comando de merge (sequência obrigatória):**
```bash
# 1. Mover batches para todo/ se ainda não estiverem
cp lawfare-batch-rejeito-1552-1571.json _data/todo/
cp lawfare-batch-flavio-trump-1572-1576.json _data/todo/

# 2. Rodar merge
python scripts/merge_todo_pending.py

# 3. Validar — deve retornar STATUS: OK
pwsh -File tools/validate-ids.ps1 -Verbose

# 4. Atualizar sync: last_id=1576, next_available=1577
```

### Thematic track

| ID | Status | Tópico |
|----|--------|--------|
| 100–191 | ✅ confirmed/published | corpus completo |
| 192 | 🟡 produced | Vorcaro triângulo carbono–mineração–banco |
| 193–195 | 🔴 pending | fila editorial (ver seção 4) |
| 196 | ✅ confirmed | Radar Top 30 (T-196) |
| 197–201 | 🟠 reserved | 5 artefatos deployed sem ID (ver seção 5) |

---

## 2. ARQUIVOS A COMMITAR (desta sessão)

### Copiar para `_data/todo/` e mergear:
```
lawfare-batch-rejeito-1552-1571.json      ← 20 entradas Op. Rejeito
lawfare-batch-flavio-trump-1572-1576.json ← 5 entradas Flávio/Trump/Escudo
```

### Copiar para `_posts/estudos/`:
```
_posts/estudos/2026-05-28-t192-vorcaro-triangulo-carbono-mineracao-banco.md
```
Criar o `.md` com frontmatter:
```yaml
---
layout: post
title: "T-192 · Família Vorcaro — Triângulo Carbono–Mineração–Banco"
date: 2026-05-28 00:00:00 -0300
description: "Um único núcleo familiar articula carbono fictício (R$ 45,5 bi em UECs), mineração ilegal (Tamisa/Serra do Curral, 3D Minerals/ANM) e banco liquidado (Master, R$ 12,2 bi). Dossiê de fechamento do triângulo — P08+P11+P03+P04+P09."
categories: [estudos]
tags:
  - p08
  - p11
  - p03
  - vorcaro
  - banco-master
  - carbono-oculto
  - operacao-rejeito
  - compliance-zero
  - serra-do-curral
  - tamisa
  - 3d-minerals
  - alliance-participacoes
  - greenwashing
author: araguaci
id_corpus: 192
padroes_ativados: ["P08", "P11", "P03", "P04", "P09"]
corpus_refs:
  - { id: 119, descricao: "Carbono Oculto — mecanismo greenwashing base" }
  - { id: 114, descricao: "Banco Master — T-192 fecha o triângulo que T-114 abre" }
  - { id: 1558, descricao: "Caio Seabra/ANM — captura do leilão 3D Minerals" }
  - { id: 1566, descricao: "Viviane Barci — proteção jurídica no STF" }
  - { id: 1571, descricao: "3º manuscrito — blendagem mineral análoga à lavagem via UECs" }
  - { id: 191, descricao: "T-191 P11 orçamentário — T-192 é a face privada do mesmo padrão" }
status_investigativo: confirmado
licenca: "CC0 1.0"
---
```
O conteúdo HTML do dossiê está em `t192-vorcaro-triangulo-carbono-mineracao-banco.html` 
(produzido nesta sessão). Adaptar para markdown ou linkar como artefato gosurf.site.

### Copiar para `_posts/governo/` e `_posts/escandalos/`:
Descompactar `jekyll-posts-p11-cluster.tar.gz`:
```bash
tar -xzf jekyll-posts-p11-cluster.tar.gz -C _posts/ --strip-components=1
```
**9 posts incluídos:**
```
_posts/governo/2023-01-01-timeline-167-cartao-corporativo-da-presidencia-99-dos-r-555-mil.md
_posts/governo/2024-01-01-timeline-177-viagens-federais-sob-sigilo-r-405-milhoes-em-2024.md
_posts/governo/2024-04-01-timeline-176-camara-dos-deputados-diarias-disparam-78-em-2025-r.md
_posts/governo/2024-07-01-timeline-175-gilmarpalooza-lisboa-buenos-aires-r-1-mi-em-recurs.md
_posts/governo/2024-07-26-timeline-170-olimpiadas-de-paris-r-235-mil-em-viagem-de-4-dias.md
_posts/governo/2025-01-01-timeline-178-custeio-administrativo-federal-r-324-bilhoes-no-1o.md
_posts/governo/2025-06-01-timeline-172-desfile-janja-em-paris-r-344-mil-pela-apex-para-ev.md
_posts/governo/2025-08-08-timeline-174-tst-30-lexus-es-300h-a-r-3465-mil-cada-r-1039-mi-s.md
_posts/escandalos/2025-01-01-novo-orcamento-secreto-stf-suspende-repasses-de-r-4-2-bilhoes-em-emendas-parlamentares.md
```
⚠️ Verificar conflito: `timeline-172` (desfile Janja) pode já existir. Checar antes de sobrescrever.

### Substituir `_data/claude.ai-corpus-ids-sync.json`:
Copiar o arquivo `claude.ai-corpus-ids-sync.json` desta sessão para `_data/`.  
Este é o arquivo que contém todas as atualizações desta sessão.

---

## 3. DECISÃO DE ID — T-192 (registrar no commit message)

```
DECISÃO: T-192 = Vorcaro triângulo carbono–mineração–banco
         T-193 = Rejeito/Serra do Curral dossiê consolidado (anterior pending_notes[192])

Motivo: T-192 produzido com qualidade alta. Rejeito já coberto pelos 20 batches
        1552-1571 — dossiê consolidado T-193 a produzir na próxima sessão.
```

---

## 4. FILA EDITORIAL THEMATIC — por prioridade

| Prioridade | ID | Tópico | Score/Urgência |
|-----------|-----|--------|----------------|
| 🔴 1 | T-193 | Rejeito/Serra do Curral — dossiê consolidado | Alta — bases nos batches 1552-1571 |
| 🔴 2 | T-180 | TSE seletividade punitiva | Open item mais antigo |
| 🟠 3 | T-194 | PCC transnacional + EUA + Escudo das Américas | Score combinado 154 |
| 🟠 4 | T-195 | Máquina de Gastos P11 — 6 posts sem estudo | Score combinado 374,8 |

---

## 5. IDs RESERVADOS — FORMALIZAR (197–201)

Estes artefatos estão deployed mas sem thematic_id no sync anterior. Esta sessão reservou IDs:

| ID | Arquivo | Ação |
|----|---------|------|
| 197 | splc-modelo-brasil.html | Adicionar `id_corpus: 197` no frontmatter do post correspondente |
| 198 | duplo-padrao-judicial.html | Idem |
| 199 | narrativa-vs-evidencia.html | Idem |
| 200 | vaza-toga.html | Idem |
| 201 | justicawatch-brasil.html | Idem |

---

## 6. ITENS RECORRENTES — OPEN ITEMS

| Item | Status | Notas |
|------|--------|-------|
| Formalizar P04b em METHODOLOGY-v2.2.md | 🔴 pendente | Subcategoria both-sidesism funcional |
| Espelhamento IPFS/archive.org | 🔴 pendente recorrente | Prioridade de resiliência |
| JustiçaWatch em /data/justicawatch/ | 🟠 pendente | JSON dinâmico + integração Jekyll |
| Shadowban @araguaci | 🟠 em andamento | Verificar shadowban.yuzurisa.com |

---

## 7. VALIDAÇÃO PÓS-COMMIT

```bash
# Após todos os commits:
python tools/sync_corpus_ids.py
pwsh -File tools/validate-ids.ps1 -Verbose

# Resultado esperado:
# STATUS: OK  (zero erros)
# STATUS: AVISO  (apenas batch_file_only — esperado)

# Verificar site ao vivo:
# https://lawfare-timeline.vercel.app/posts/t192-vorcaro-triangulo-carbono-mineracao-banco/
# https://lawfare-timeline.vercel.app/posts/custeio-administrativo-federal-p11/
```

---

## 8. ESTADO FINAL ESPERADO APÓS COMMIT

```
lawfare.json:         last_id = 1576
thematic:             last_id = 196, last_produced = 192
next_available main:  1577
next_available thematic: 197
_data/todo/:          VAZIO (após merge)
_posts/:              +9 governo/escandalos + +1 estudos (T-192)
```

---

*Sync report gerado por claude.ai — sessão 2026-05-28*  
*Arquivo sync completo: `_data/claude.ai-corpus-ids-sync.json`*  
*CC0 1.0 Universal — Domínio Público Total*
