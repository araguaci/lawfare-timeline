# Próximos passos · lawfare-timeline

**Atualizado:** 2026-07-18 (batch 1620 + T-222/T-223 + posts 1577–1578)

---

## Snapshot


| Track                | Last ID | Próximo | Status                                        |
| -------------------- | ------- | ------- | --------------------------------------------- |
| Main (timeline)      | 1624    | 1625    | Gap 0707–0718 + Consulado HK (1623)         |
| Thematic (estudos T) | 223     | 224     | T-223 P12-B assimetria analítica eleitoral    |
| Fila editorial       | —       | —       | `_data/todo/` — consulado HK pendente sync    |
| Posts 404 resolvidos | 12      | —       | ✅ permalink + 1 post criado (ID 160)     |


---

## Manutenção Jekyll — 404s resolvidos ✅ (29/05/2026)


| URL corrigida                                                                       | Ação                                                |
| ----------------------------------------------------------------------------------- | --------------------------------------------------- |
| `/posts/duplo-padrao-judicial-corpus-bridge/`                                       | Arquivo existia — resolução automática via `:title` |
| `/posts/splc-modelo-brasil-corpus-bridge/`                                          | Arquivo existia — resolução automática via `:title` |
| `/posts/vaza-toga-corpus-bridge/`                                                   | Arquivo existia — resolução automática via `:title` |
| `/posts/1997-01-01-escandalo-da-venda-da-companhia-vale-do-rio-doce/`               | `permalink` explícito adicionado                    |
| `/posts/2025-07-30-eua-aplicam-sancoes-a-alexandre-de-moraes-usando-lei-magnitsky/` | `permalink` explícito adicionado                    |
| `/posts/2025-08-20-silas-malafaia-tem-mensagens-vazadas-na-imprensa/`               | `permalink` explícito adicionado                    |
| `/posts/2018-03-01-operacao-descarte/`                                              | `permalink` explícito adicionado                    |
| `/posts/2020-03-03-operacao-ultimo-lance/`                                          | `permalink` explícito adicionado                    |
| `/posts/2003-07-01-operacao-banestado/`                                             | `permalink` explícito adicionado                    |
| `/posts/2003-10-30-operacao-anaconda/`                                              | `permalink` explícito adicionado                    |
| `/posts/2007-05-17-operacao-navalha/`                                               | `permalink` explícito adicionado                    |
| `/posts/2026-04-13-moraes-abre-inquerito-contra-pre-candidato...`                   | **Post criado** (corpus entry ID 160)               |


> **Causa raiz:** tema Chirpy usa `permalink: /posts/:title/` — `:title` extrai slug sem a data do filename. Links internos apontavam para URLs com data prefixada. Solução: `permalink` explícito no front matter.

---

## Rodada T-205–T-207 ✅ (29/05/2026)


| ID    | Dossiê                                                               | URL canônica                                                       |
| ----- | -------------------------------------------------------------------- | ------------------------------------------------------------------ |
| T-205 | [Duplo padrão judicial](/posts/duplo-padrao-judicial-corpus-bridge/) | `_posts/estudos/2026-05-29-duplo-padrao-judicial-corpus-bridge.md` |
| T-206 | [SPLC modelo Brasil](/posts/splc-modelo-brasil-corpus-bridge/)       | `_posts/estudos/2026-05-29-splc-modelo-brasil-corpus-bridge.md`    |
| T-207 | [Vaza Toga INQ 4781](/posts/vaza-toga-corpus-bridge/)                | `_posts/estudos/2026-05-29-vaza-toga-corpus-bridge.md`             |


**Artefatos HTML restantes sem ID:** narrativa-vs-evidencia · justicawatch-brasil → T-208/T-209

---

## Rodada T-202–T-204 ✅ (29/05/2026)


| ID    | Dossiê                                                                              | Status |
| ----- | ----------------------------------------------------------------------------------- | ------ |
| T-202 | [Delegada × PCC SP](/posts/2026-05-29-delegada-pcc-infiltracao-institucional-sp/)   | ✅      |
| T-203 | [Zelotes CARF](/posts/2026-05-29-operacao-zelotes-carf-captura-fiscal/)             | ✅      |
| T-204 | [Gastos Paris cluster](/posts/2026-05-29-gastos-paris-cluster-extravagancia-janja/) | ✅      |


---

## Rodada editorial T-191–T-201 ✅ (28/05/2026)


| ID    | Dossiê                          | Status |
| ----- | ------------------------------- | ------ |
| T-191 | Custeio P11                     | ✅      |
| T-192 | Vorcaro triângulo               | ✅      |
| T-193 | Viagens sigilo                  | ✅      |
| T-194 | Índice cluster P11              | ✅      |
| T-195 | CPI × PCC eleitoral             | ✅      |
| T-196 | Radar Top 30 lacunas            | ✅      |
| T-197 | Operação Rejeito 1552–1571      | ✅      |
| T-198 | COAF × Moraes                   | ✅      |
| T-199 | Lojas Americanas                | ✅      |
| T-200 | Estatais rombo P11              | ✅      |
| T-201 | PCC transnacional OFAC/EUA/luso | ✅      |


**Resultado:** 0 alertas críticos (score ≥ 40) · 200+ posts excluídos por cobertura

---

## Rodada T-208–T-209 ✅ (29/05/2026)


| ID    | Dossiê                                                                 | URL canônica                                                        |
| ----- | ---------------------------------------------------------------------- | ------------------------------------------------------------------- |
| T-208 | [Narrativa vs Evidência](/posts/narrativa-vs-evidencia-corpus-bridge/) | `_posts/estudos/2026-05-28-narrativa-vs-evidencia-corpus-bridge.md` |
| T-209 | [JustiçaWatch Brasil](/posts/justicawatch-brasil-corpus-bridge/)       | `_posts/estudos/2026-05-28-justicawatch-brasil-corpus-bridge.md`    |


---

## Rodada T-210–T-218 ✅ (jun/2026)


| ID    | Dossiê                         | Tema principal                          |
| ----- | ------------------------------ | --------------------------------------- |
| T-210 | Operação Parasitas / Sepse     | Cluster HMAP GO                         |
| T-211 | Sepse 2ª fase                  | PF/MPF rede lavagem                     |
| T-212 | Sepse UTI superfaturada        | Repasse 10% OS                          |
| T-213 | CGU irregularidades OS         | Fixação competência                     |
| T-214 | Status Sepse                   | Sem denúncia formal                     |
| T-215 | Vorcaro STF 2ª Turma           | Prisão familiares                       |
| T-216 | TSE × USAID                    | Parceria / censura seletiva             |
| T-217 | Seletividade punitiva          | Lacuna metodológica TSE/Câmara          |
| T-218 | Ouro ilegal P08                | Amazônia PCC/CV/Venezuela               |


---

## Rodada T-219–T-220 + batch 1609–1611 ✅ (09/07/2026)


| ID / faixa | Dossiê / evento                                                              | Status |
| ---------- | ---------------------------------------------------------------------------- | ------ |
| T-219      | Farra do INSS — rede Conafer/Careca/CPMI                                     | ✅      |
| T-220      | Convergência PCC-OFAC × rede Arpar × INSS                                    | ✅      |
| 1609       | OFAC sanciona Shimada/Victory Trading (PCC)                                  | ✅      |
| 1610       | PF diverge publicamente da avaliação OFAC                                    | ✅      |
| 1611       | Victory × Wave Intermediações (rede Arpar) — ev-alleged, fonte única         | ✅      |


JSON arquivados → `_data/processados/` · `_data/todo/` vazio (exceto `todo.md` notas)

---

## Bucha + Consulado HK ✅ (18/07/2026)

| Item | Resultado |
|------|-----------|
| **Bucha** | Lacuna fechada — sem dia 11/08 verificável → `_data/processados/lacuna-bucha-fundacao-1831.json` |
| **1623** | Consulado HK — P02, ev-contested, fontes Metrópoles (Corregedor/CPADIS) |
| **P13** | Arquivado — N=1; caso usa P02 existente |

Faixa **1621–1624** (batch gap + merge): 1621 Moraes/Milei · 1622 Hawala · 1623 Consulado · 1624 revisão criminal Bolsonaro

---

## Correção IDs 1520/176 ✅ (18/07/2026)

| Ação | Detalhe |
|------|---------|
| **1520** | Restaurado ao post P04b imprensa (`2026-05-28-imprensa-brasileira-...`) |
| **1621** | Revisão criminal Bolsonaro — post canônico `_posts/stf/2026-05-08-bolsonaro-revisao-criminal-...` |
| Removido | Duplicata `_posts/lawfare/2026-05-08-bolsonaro-protocola-revisao-criminal-...` |
| Script | `tools/fix_id_1520_176.py` |

---

## Rodada 1620 + T-222/T-223 + posts 1577–1578 ✅ (18/07/2026)


| ID / faixa | Conteúdo | Status |
| ---------- | -------- | ------ |
| 1620 | Auditorias KPMG/PwC/EY/Crowe — pareceres sem ressalvas Master/Reag | ✅ |
| T-222 | P10 promovido a padrão autônomo (infraestrutura de serviço) | ✅ |
| T-223 | P12-B instanciado — assimetria de capacidade analítica eleitoral | ✅ |
| 1577 | Moraes proíbe Cremesp requisitar prontuários aborto legal (ADPF 1141) | ✅ post Jekyll |
| 1578 | STF suspende resolução CFM aborto após 22 semanas (ADPF 1141) | ✅ post Jekyll |


JSON arquivados → `_data/processados/` · `_data/todo/` pendente: consulado HK (`__PENDENTE_SYNC__`)

---

## Rodada 1613–1618 + T-221 ✅ (09/07/2026)


| ID / faixa | Conteúdo | Status |
| ---------- | -------- | ------ |
| 1613 | Moraes nega adiamento julgamento Eduardo (quórum DPU) | ✅ |
| 1614 | Condenação Eduardo Bolsonaro 4a2m (tarifaço) | ✅ |
| 1615 | Moraes nega diligências Flávio (calúnia) | ✅ |
| 1616 | PF conclui indícios calúnia Flávio | ✅ |
| 1617 | Prorrogação domiciliar Bolsonaro + apreensão aparelhos | ✅ |
| 1618 | Interrogatório Flávio pela PF (10 dias) | ✅ |
| T-221 | Nemo judex formalizado — preliminar DPU AP 2782 | ✅ |


---

## IDs 1513–1520 — Designação Terrorista PCC/CV ✅ (29/05/2026)


| ID   | Data       | Post                                                                                |
| ---- | ---------- | ----------------------------------------------------------------------------------- |
| 1513 | 2025-11-08 | `crise-diplomatica/2025-11-08-promotor-gakiya-sinaliza-designacao-terrorista...`    |
| 1514 | 2026-03-07 | `crise-diplomatica/2026-03-07-trump-lanca-escudo-das-americas...`                   |
| 1515 | 2026-03-11 | `crise-diplomatica/2026-03-11-brasil-rejeita-pedido-formal-dos-eua...`              |
| 1516 | 2026-03-11 | `crise-diplomatica/2026-03-11-chanceler-mauro-vieira-telefona-a-rubio...`           |
| 1517 | 2026-05-01 | `crise-diplomatica/2026-05-01-flavio-bolsonaro-visita-trump-na-casa-branca...`      |
| 1518 | 2026-05-28 | `crise-diplomatica/2026-05-28-departamento-de-estado-designa-pcc-e-cv-como-sdgt...` |
| 1519 | 2026-06-05 | `crise-diplomatica/2026-06-05-fto-entra-em-vigor...`                                |
| 1520 | 2026-05-28 | `lawfare/2026-05-28-imprensa-brasileira-enquadra-designacao-terrorista-pcc-cv...`   |


JSON movido → `_data/processados/lawfare-1513-1520-designacao-terrorista-diplomatica.json`

---

## Prioridade 1 ✅ · Prioridade 2 ✅ (29/05/2026)


| Tarefa                                            | Status |
| ------------------------------------------------- | ------ |
| T-208 Narrativa vs Evidência                      | ✅      |
| T-209 JustiçaWatch Brasil + `_data/justicawatch/` | ✅      |
| IDs 1513–1520 posts Jekyll criados                | ✅      |
| T-192 Vorcaro triângulo publicado                 | ✅      |
| 9 posts P11 cluster extraídos                     | ✅      |
| P04b formalizado METHODOLOGY.md v2.2              | ✅      |
| JSON 1513–1520 movido para processados            | ✅      |


---

## Prioridade 3 — Infraestrutura (29/05/2026)

| Tarefa | Status |
| --- | --- |
| Faixa **1481–1505** (PCC/ʼNdrangheta) → merge em `lawfare.json` | ✅ 29/05/2026 |
| Gaps **1449–1480** e **1506–1510** declarados permanentes | ✅ aceito |
| IPFS/archive.org — espelhamento fora-jurisdição | ✅ script criado |
| Recuperação shadowban **@araguaci** | ⏳ externo |

**Resultado merge:** `lawfare.json` 1514 → **1539 entradas** · script: `tools/merge_pcc_batch_1481_1505.py`
**Gaps permanentes aceitos:** 1449–1480 (32 IDs sem conteúdo) · 1506–1510 (5 IDs sem conteúdo)

### Archive.org — espelhamento

Script criado: `tools/archive_org_mirror.py` — **1.663 URLs** identificadas.

```bash
# dry-run (lista URLs, sem envio)
python tools/archive_org_mirror.py

# envio completo (~83 min, ~1663 URLs × 3s)
python tools/archive_org_mirror.py --submit

# retomar (pula URLs já arquivadas)
python tools/archive_org_mirror.py --submit --skip-archived
```

Log: `_data/archive_org_log.json`

Radar vivo: [T-196](/posts/2026-05-28-top30-alertas-criticos-operacoes-sem-dossie/) · [relatorio-top30-sem-estudo.md](/docs/relatorio-top30-sem-estudo.md)

**Comandos:** `python tools/sync_corpus_ids.py` · `python tools/rank_ops_sem_estudo.py`

---

## Relatório Cursor.ai — Recomendações de Continuidade (2026-05-28)

> Estado pós-sync com sessão claude.ai. Executar nesta ordem.

### Estado atual confirmado

```
lawfare.json      last_id = 1576  (total = 1514 entradas)
thematic          last_id = 209   (207 confirmed · 208/209 reserved)
_data/todo/       T-191.json · T-192.json · T-199-americanas.json
_posts/estudos/   T-180 … T-207 publicados (15 estudos em disco)
```

### Ação 1 — Publicar T-192 Vorcaro `[alta prioridade]`

Criar `_posts/estudos/2026-05-28-vorcaro-triangulo-carbono-mineracao-banco.md` com frontmatter:

```yaml
---
layout: post
title: "T-192 · Família Vorcaro — Triângulo Carbono–Mineração–Banco"
date: 2026-05-28 00:00:00 -0300
description: >
  Um único núcleo familiar articula carbono fictício (R$ 45,5 bi em UECs),
  mineração ilegal (Tamisa/Serra do Curral, 3D Minerals/ANM) e banco liquidado
  (Master, R$ 12,2 bi). Fechamento do triângulo — P08+P11+P03+P04+P09.
categories: [estudos]
tags: [p08, p11, p03, vorcaro, banco-master, carbono-oculto, operacao-rejeito,
       compliance-zero, serra-do-curral, tamisa, 3d-minerals, greenwashing]
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

Conteúdo: adaptar `t192-vorcaro-triangulo-carbono-mineracao-banco.html` (em `_data/todo/`) para markdown ou linkar como artefato gosurf.site.

### Ação 2 — Extrair posts P11 cluster `[alta prioridade]`

Localizar `jekyll-posts-p11-cluster.tar.gz` (produzido na sessão claude.ai) e extrair:

```bash
tar -xzf jekyll-posts-p11-cluster.tar.gz -C _posts/ --strip-components=1
```

**9 posts incluídos:**


| Destino              | Arquivo                                                |
| -------------------- | ------------------------------------------------------ |
| `_posts/governo/`    | timeline-167 · 170 · 172 · 174 · 175 · 176 · 177 · 178 |
| `_posts/escandalos/` | novo-orcamento-secreto-stf-suspende-repasses           |


⚠️ Checar antes de sobrescrever: `timeline-172` (desfile Janja) pode já existir em disco.

### Ação 3 — Formalizar T-208 e T-209

Criar estudos Jekyll para os 2 artefatos HTML `reserved`:


| ID    | Artefato                      | Slug alvo                                         |
| ----- | ----------------------------- | ------------------------------------------------- |
| T-208 | `narrativa-vs-evidencia.html` | `2026-05-28-narrativa-vs-evidencia-corpus-bridge` |
| T-209 | `justicawatch-brasil.html`    | `2026-05-28-justicawatch-brasil-corpus-bridge`    |


Padrão de frontmatter: seguir T-205/T-206/T-207 como modelo (`_posts/estudos/2026-05-29-*-corpus-bridge.md`).

### Ação 4 — Formalizar P04b em METHODOLOGY-v2.2.md

Adicionar subcategoria em `METHODOLOGY-v2_2.md`:

```markdown
#### P04b — Both-sidesism funcional
Falsa-equivalência operada por veículos mainstream como mecanismo de proteção
a atores sob investigação. Distinto de P04 (weaponização direta): P04b neutraliza
cobertura crítica sem produzir conteúdo ofensivo — apenas dilui o sinal.
Casos: [T-184, ...].
```

### Ação 5 — Mover T-191 e T-192 JSON de `_data/todo/` para `_data/processados/`

```bash
mv _data/todo/T-191-custeio-administrativo-federal-p11.json _data/processados/
mv _data/todo/T-192-vorcaro-triangulo-carbono-mineracao-banco.json _data/processados/
# manter T-199-americanas.json em todo/ até publicação do estudo
```

### Validação pós-commit

```bash
python tools/sync_corpus_ids.py
pwsh -File tools/validate-ids.ps1 -Verbose
# Resultado esperado: STATUS: OK (zero erros)
# STATUS: AVISO apenas para faixa 1449-1510 batch_file_only — esperado
```

### Namespace protegido — NÃO tocar

```
_data/ faixa 1449–1510  →  PCC/Ndrangheta canônico (1481-1500)
                            merge linear somente com validação explícita
```

---

## Referências

- Sync: `_data/claude.ai-corpus-ids-sync.json` (schema 1.1.0 · 2026-05-28)
- Design system: `_data/lawfare-design-system-reference.html`
- Portal: [https://lawfare-timeline.vercel.app/](https://lawfare-timeline.vercel.app/)

---

Arquivo legado — links e rascunhos sociais

## TODOs (ícones)

- drone.svg > plane-departure
- reflect.svg > sun
- thermometer-low.svg > thermometer-half
- laser-pointer.svg >  bolt-lightning

---

## Relacionados

- 🤐🕵️‍♂️ Censura no Brasil (2019-2025) 🌐
🔗 [https://tinyurl.com/abusosupremo](https://tinyurl.com/abusosupremo)

- 🌐 Brasil e Big Techs: Impacto da Seção 301
🔗 [https://tinyurl.com/brasil-x-bigtechs](https://tinyurl.com/brasil-x-bigtechs)

### COAF e Ação de Moraes: Desafios nas Investigações Criminais

- [https://tinyurl.com/coaf-investigacoes](https://tinyurl.com/coaf-investigacoes)
- [https://tinyurl.com/abusosupremo](https://tinyurl.com/abusosupremo)
- [https://tinyurl.com/lawfare-5w](https://tinyurl.com/lawfare-5w)
- [https://tinyurl.com/guiana-crime-transnacional](https://tinyurl.com/guiana-crime-transnacional)
- [https://tinyurl.com/crime-transnacionalNC](https://tinyurl.com/crime-transnacionalNC)
- [https://tinyurl.com/crime-transnacional](https://tinyurl.com/crime-transnacional)
- [https://tinyurl.com/usaid-felipe-neto-mapa](https://tinyurl.com/usaid-felipe-neto-mapa)
- [https://tinyurl.com/usaid-felipe-neto](https://tinyurl.com/usaid-felipe-neto)
- [https://tinyurl.com/crise-diplomatica-stf-x-eua](https://tinyurl.com/crise-diplomatica-stf-x-eua)
- [https://tinyurl.com/crise-diplomatica-resumo](https://tinyurl.com/crise-diplomatica-resumo)
- [https://tinyurl.com/governanca-criminal](https://tinyurl.com/governanca-criminal)
- [https://tinyurl.com/vazatoga-mapa](https://tinyurl.com/vazatoga-mapa)
- [https://tinyurl.com/vazatoga2](https://tinyurl.com/vazatoga2)
- [https://tinyurl.com/linhadetempo-impunes](https://tinyurl.com/linhadetempo-impunes)
- [https://tinyurl.com/linhadetempo-jus](https://tinyurl.com/linhadetempo-jus)
- [https://tinyurl.com/linhadetempo-fin](https://tinyurl.com/linhadetempo-fin)
- [https://tinyurl.com/linhadetempo-gov](https://tinyurl.com/linhadetempo-gov)
- [https://tinyurl.com/linhadetempo-dossie](https://tinyurl.com/linhadetempo-dossie)
- [https://tinyurl.com/linhadetempo-violador](https://tinyurl.com/linhadetempo-violador)
- [https://tinyurl.com/linhadetempo-tse](https://tinyurl.com/linhadetempo-tse)
- [https://tinyurl.com/linhadetempo-stf](https://tinyurl.com/linhadetempo-stf)
- [https://tinyurl.com/linhadetempo-lawfare](https://tinyurl.com/linhadetempo-lawfare)
- [https://tinyurl.com/crise-diplomatica](https://tinyurl.com/crise-diplomatica)
- [https://tinyurl.com/supersalarios-ia](https://tinyurl.com/supersalarios-ia)
- [https://tinyurl.com/privilegio-ia](https://tinyurl.com/privilegio-ia)

## Lawfare

-🏛️ Lawfare - O Quê, Porquê, Quem, Onde, Quando
🔗 [https://tinyurl.com/lawfare-5w](https://tinyurl.com/lawfare-5w)

-💥 Governança Criminal, 26% do BR vive sob regras de facções
🔗 [https://tinyurl.com/governanca-criminal](https://tinyurl.com/governanca-criminal)

## Linhas de Tempo Montadas:

-🏛️ Resumo Crise diplomática Brasil-EUA 📜
🔗 [https://tinyurl.com/crise-diplomatica-stf-x-eua](https://tinyurl.com/crise-diplomatica-stf-x-eua)

-🧭 Linha do Tempo Crise diplomática Brasil-EUA 
🔗 [https://tinyurl.com/crise-diplomatica](https://tinyurl.com/crise-diplomatica)

-📜 Interferências Judiciais Sistêmicas no Brasil
🔗 [https://tinyurl.com/linhadetempo-lawfare](https://tinyurl.com/linhadetempo-lawfare)

-✒️ STF no Contexto Político Brasileiro (2018-2025) ⚖️
🔗 [https://tinyurl.com/linhadetempo-stf](https://tinyurl.com/linhadetempo-stf)

-🌐 Parceria entre o Tribunal Superior Eleitoral (TSE) e USAID ⚖️
🔗 [https://tinyurl.com/linhadetempo-tse](https://tinyurl.com/linhadetempo-tse)

-📝 Ações do Violador de Direitos Humanos 💥
🔗 [https://tinyurl.com/linhadetempo-dossie](https://tinyurl.com/linhadetempo-dossie)

-💰 Escândalos Políticos no Brasil
🔗 [https://tinyurl.com/linhadetempo-gov](https://tinyurl.com/linhadetempo-gov)

-🏛️ Escândalos Financeiros no Brasil (1995-2025)
🔗 [https://tinyurl.com/linhadetempo-fin](https://tinyurl.com/linhadetempo-fin)

-⚖️ Casos de Corrupção no Sistema Judiciário Brasileiro
🔗 [https://tinyurl.com/linhadetempo-jus](https://tinyurl.com/linhadetempo-jus)

-⛓️ Decisões Judiciais Beneficiando Criminosos no Brasil 💥
🔗 [https://tinyurl.com/linhadetempo-impunes](https://tinyurl.com/linhadetempo-impunes)

- 🎭 Felipe Neto e Instituto Vero com ONGs estrangeiras (Open Society, Ford, EUA)
👉 [https://tinyurl.com/usaid-felipe-neto](https://tinyurl.com/usaid-felipe-neto)
🔗 [https://tinyurl.com/usaid-felipe-neto-mapa](https://tinyurl.com/usaid-felipe-neto-mapa)
🔗 [Mapa Mental - Felipe Neto & Instituto Vero](https://mermaid.live/view#pako:eNqNV8tu4zYU_RVCGBQJJollJ3Ec7TyOM0gxDyN2UqDIhpZoh41EqqSUySQI0H_oD7ToYtABZjXtZrb6k35JD6kXlbrTBnlKl-TlOeeee_PghTJiXuAlXEQJTa8EIUrKbGvrlMU8ZeQNyyT5hpwJnfEsx--XTMntbRNnvgiZSJGxO7x4yRSNy2eEjLOcFh-K3ySJGHG2qt939yNbb9-83K7fTWSypBkjxS9YrLlYSZWUm9URM6pCpjjVJJQJmS9Oe4v5tN16FefFRxFySlhCWMw4Fv_JNBn4g0EP3w7q0FMuqIlLmEAmuAVTAslML8ZNMudchzIgEyZ0riiQuOTF75rMZFx8yniIlMrIzlaaTHWmqFgzrqSut3qbMkHmMuQse09OZS4imnEpNNmaS4Q1RxJyMX82OPT3fN83N0DG_fbdCbPg4Hl_v-cf9dy3UwDH72hESWRyuBi3y86f9Y-aHf1-D59Yud8GdLGQK47fGzov5uOzk79--nkync3m7ZpxKrkkUA5XRia3QBxEajdZUXwxu2qjg1sLXXmjw4YDqSIHjXZtTbIl8dbC-m_Z1hnUZLT6qHQWYmfKm_VQDEDPU8USSRaKL3NBY8g0MhJ2eDhnueBGxCbnQc8fddSD-68Z0g6MCv9DsY2QUqQGYHlEAQh3smuwhpTJVpMUssRNpCJT6DiT3fwmMqZLPCsrjScpRBnyjD5liJKQJikV14YHvkZEi8U5bq2xk4q487TCkCsLv6pxqMrNRQjXsDdB0THDSCQV9gOXt1xnVNeUTEsGdyfX9JbV67vKtqoMsGXIlqyqgRsCMbuF04Zb-Qd1PZjMNsWZmu8c0fcD8p1UN_papppouVRYfM1CumZJG7jv9_xjlP0_YMNBAqVNXshYgzXlMOwP7OYl5OyuIsOg_yqPqZPQfvfOw6BCh1x5r_HTgP5jbmDVuwkFm55z6cMyPuKVu8qqNkoAUHyENdZDtXOoI9s-LncQkMU7nsHxUEsxGHuh6D2PCYqc0JBpLUmqwGHM1obTdvFgaBfPaGwP0kRQMk7offGHQK2aLFoX6jiQLaCgrSlThM-fNoLnHQNxfQJY4eQB8A1z3faWaZRTBRQ28NHv2_jGg2rqrJl10UBeZ2hjasVU3TlsM6C4nXZaiLOqvM1YFL_GXDPyQ66KTxEP6VOvLJcsWIKNJqpsGrrtVZ1Dp-Wh7SmW0FXldRF2SI0TuKiOq94WSlQwEzbIkFBZS936lmAKXLqaqCzJmBaqAM5n-GO1y9RRlxweU20yk5ktcdcmXnEstWaGT4gexa87vneWdCwPVKE3dhQ1Z4ioGZXmGPiwi3XdfCubp5s6fd2QHfDa4k1V8XnXLUIzoFDUGIxqk3IutNUWHipjZGX3uvKeertnkEZ94wGIeXI-hM3WyFoUHyj5tlaHm4AzIVmeDW2pubt5spJrubk_oPnROKMmyBS6BnjttJNunoyqGcWMapAz7IZH5ZoG5U1m0LaImGbFZ7QhC8Sq03vT4ssytoNQM72hwENqmATZ3fqug05YGJecG119rYxLuzBR5UjCzbi0ON1pXabph1WLaTIyN23wqDGwmtdkjuZUfEzcWpwpNB6UUGalHFaaMzDS0tEh26ylAYLjGb9vdPs_hoAppjwbDFthOcj72hhwmccCRbnkVZCR_7q1p9bkr4S3460Vj7wgUznb8RKGg82f3oMd073smiXsyguMhKm6Mf3kEWtQHN9LmdTLlMzX116worHGX3mKeYydcLpWtA3BuMPUBMNa5gV9v39oN_GCB-_OC3YP9w6PRkejg9GB3-8fj4bDHe-9CTvaGwwOhsPB8THe7PvDxx3v3p7r742ODo7djx2PRcZ_Xpf_lNj_TR7_BowhKAk)

---

-⚖️ Linhas de Tempo da Guerra Silenciosa contra a Nação ⚔️
🔗 [https://lawfare-timeline.vercel.app/](https://lawfare-timeline.vercel.app/)

---

## 🤖 Ferramentas de Analise IA:

- ✨ Raio-X da Corrupção - Painel da Corrupção
🔗 [https://tinyurl.com/ia-raio-x](https://tinyurl.com/ia-raio-x)
- ✨ Raio-X da Corrupção (lawfare-three)
🔗 [https://tinyurl.com/raiox-ia](https://tinyurl.com/raiox-ia)
- ✨ Soberania do Brasil - Análise Estratégica
🔗 [https://tinyurl.com/soberania-ia](https://tinyurl.com/soberania-ia)
- ✨ A Arquitetura do Privilégio
🔗 [https://tinyurl.com/privilegio-ia](https://tinyurl.com/privilegio-ia)
- ✨ Sistema de Análise de Supersalários
🔗 [https://tinyurl.com/supersalarios-ia](https://tinyurl.com/supersalarios-ia)

---

## 📌 Posts lawfare-timeline.vercel.app

- ⚖️ Análise do Voto do Ministro Luiz Fux na AP 2668
🔗 [https://tinyurl.com/voto-do-fux](https://tinyurl.com/voto-do-fux)

---

## 🌊 gosurf.site — Dossiês

- 🗺️ Padrões Sistêmicos — Dashboard
🔗 [https://tinyurl.com/padroes-sistemicos](https://tinyurl.com/padroes-sistemicos)
- ⚓ Mare Liberum
🔗 [https://tinyurl.com/mare-liberum](https://tinyurl.com/mare-liberum)
- 🎖️ Alto Comando — Decadência Moral
🔗 [https://tinyurl.com/decadencia-moral](https://tinyurl.com/decadencia-moral)

---

## 🔗 lawfare-three.vercel.app — Linhas de Tempo Espelhadas

- 🏛️ Linha de Tempo Principal
🔗 [https://tinyurl.com/lawfare-br](https://tinyurl.com/lawfare-br)
- 🤡 Plenário do STF — Indecoro
🔗 [https://tinyurl.com/plenopiti](https://tinyurl.com/plenopiti)
- 👴 Decano — Vida Loka
🔗 [https://tinyurl.com/decano-vidaloka](https://tinyurl.com/decano-vidaloka)
- 💸 Lei do Luxo — Extravagâncias
🔗 [https://tinyurl.com/leideluxo](https://tinyurl.com/leideluxo)
- ⛓️ Impunidade
🔗 [https://tinyurl.com/timeline-impune](https://tinyurl.com/timeline-impune)
- 🎭 Penduricalhos — Farra com o Dinheiro Público
🔗 [https://tinyurl.com/timeline-farra](https://tinyurl.com/timeline-farra)
- 🚔 Operações Policiais
🔗 [https://tinyurl.com/timeline-ope](https://tinyurl.com/timeline-ope)
- 🏦 Escândalos Financeiros
🔗 [https://tinyurl.com/timeline-fin](https://tinyurl.com/timeline-fin)
- ⚖️ Corrupção no Judiciário
🔗 [https://tinyurl.com/timeline-jus](https://tinyurl.com/timeline-jus)
- 💥 Escândalos Políticos
🔗 [https://tinyurl.com/timeline-gov](https://tinyurl.com/timeline-gov)
- 📁 Dossiê do Violador
🔗 [https://tinyurl.com/timeline-dossie](https://tinyurl.com/timeline-dossie)
- 🗳️ TSE — Parceria USAID
🔗 [https://tinyurl.com/timeline-tse](https://tinyurl.com/timeline-tse)
- 🔎 STF — INQ 4781
🔗 [https://tinyurl.com/timeline-4781](https://tinyurl.com/timeline-4781)
- 📜 Interferências Judiciais (lawfare)
🔗 [https://tinyurl.com/timeline-stf](https://tinyurl.com/timeline-stf)

---

## 🔎 Observatório / Investigações

- 🏦 Compliance Zero — Banco Master (Observatório Civil)
🔗 [https://tinyurl.com/compliance-zero](https://tinyurl.com/compliance-zero)
- 🌎 Cronologia de Operações EUA × Crime Organizado
🔗 [https://tinyurl.com/operacoes-eua](https://tinyurl.com/operacoes-eua)
- 📰 Notícia: STF suspende investigação da Receita contra autoridades (EN)
🔗 [https://tinyurl.com/against-revenue-service](https://tinyurl.com/against-revenue-service)

---

## 📚 Outros Projetos Relacionados

- 🧠 Ponerologia — Psicopatas no Poder (PDF)
🔗 [https://tinyurl.com/psicopatas-no-poder](https://tinyurl.com/psicopatas-no-poder)
- 🇧🇷 Pátria Amada Brasil
🔗 [https://tinyurl.com/amadapatria](https://tinyurl.com/amadapatria)
- 📅 1000 Dias de Governo
🔗 [https://tinyurl.com/1000diasgovbr](https://tinyurl.com/1000diasgovbr)
- 🕊️ Stop War For Ever
🔗 [https://tinyurl.com/all-wars-end](https://tinyurl.com/all-wars-end)

--- CC: ---

- @ClaudioLessa
- @pfigueiredo08
- @LeoVilhenaReal
- @fabio_talhari
- @auriverdebrasil
- @TheIncorrupt_
- @Maxcardosobr
- @ProfJoaoCarlosM
- @alertatotal
- @redegni
- @diretopontoblog
- @NamericaToday
- @OliverNoronha
- @george1BR2
- @tdhoratheoffice
- @DanilodeDireita
- @fiscaldofim
- @movadvdireitabr
- @VisaoPatria
- @OdnaldaW2
- @RicardoRoveran
- @jornalbunker
- @OficialVanucci
- @BlogPequi
- @VlogdoLisboa
- @ducavendish
- @pamcosta21
- @RoziSNews
- @CarinaBelome
- @DefecatingB
- @MafinhaBarba
- @arvor_ia
- @oeditorialNews
- @GuerraDaInfor
- @CleberT97506802
- @canalsergio2
- @GringaVidaUsa

