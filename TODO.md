# Próximos passos · lawfare-timeline

**Atualizado:** 2026-05-28 (sync sessão claude.ai — merge 1572-1576 + corpus map v1.1.0)

---

## Snapshot

| Track | Last ID | Próximo | Status |
| --- | ---: | ---: | --- |
| Main (timeline) | 1576 | 1577 | Merge 1572–1576 concluído (Flávio/Trump) |
| Thematic (estudos T) | 209 | 210 | T-207 confirmado · T-208/T-209 reserved |
| Fila editorial Q2 | — | — | Rodada T-208+ pendente |

---

## Rodada T-205–T-207 ✅ (29/05/2026)

| ID | Dossiê | Registry |
| --- | --- | --- |
| T-205 | [Duplo padrão judicial](/posts/2026-05-29-duplo-padrao-judicial-corpus-bridge/) | T-143 |
| T-206 | [SPLC modelo Brasil](/posts/2026-05-29-splc-modelo-brasil-corpus-bridge/) | T-129 |
| T-207 | [Vaza Toga INQ 4781](/posts/2026-05-29-vaza-toga-corpus-bridge/) | T-108 |

**Artefatos HTML restantes sem ID:** narrativa-vs-evidencia · justicawatch-brasil → T-208/T-209

---

## Rodada T-202–T-204 ✅ (29/05/2026)

| ID | Dossiê | Status |
| --- | --- | --- |
| T-202 | [Delegada × PCC SP](/posts/2026-05-29-delegada-pcc-infiltracao-institucional-sp/) | ✅ |
| T-203 | [Zelotes CARF](/posts/2026-05-29-operacao-zelotes-carf-captura-fiscal/) | ✅ |
| T-204 | [Gastos Paris cluster](/posts/2026-05-29-gastos-paris-cluster-extravagancia-janja/) | ✅ |

---

## Rodada editorial T-191–T-201 ✅ (28/05/2026)

| ID | Dossiê | Status |
| --- | --- | --- |
| T-191 | Custeio P11 | ✅ |
| T-192 | Vorcaro triângulo | ✅ |
| T-193 | Viagens sigilo | ✅ |
| T-194 | Índice cluster P11 | ✅ |
| T-195 | CPI × PCC eleitoral | ✅ |
| T-196 | Radar Top 30 lacunas | ✅ |
| T-197 | Operação Rejeito 1552–1571 | ✅ |
| T-198 | COAF × Moraes | ✅ |
| T-199 | Lojas Americanas | ✅ |
| T-200 | Estatais rombo P11 | ✅ |
| T-201 | PCC transnacional OFAC/EUA/luso | ✅ |

**Resultado:** 0 alertas críticos (score ≥ 40) · 200+ posts excluídos por cobertura

---

## Prioridade 1 — Próxima rodada (T-208+)

| # | Candidato | Escopo |
| ---: | --- | --- |
| 1 | **T-208** | Narrativa vs Evidência → estudo Jekyll (artefato HTML existe) |
| 2 | **T-209** | JustiçaWatch Brasil → estudo Jekyll + integrar em `/data/justicawatch/` |

Radar vivo: [T-196](/posts/2026-05-28-top30-alertas-criticos-operacoes-sem-dossie/) · [relatorio-top30-sem-estudo.md](/docs/relatorio-top30-sem-estudo.md)

**Comandos:** `python tools/sync_corpus_ids.py` · `python tools/rank_ops_sem_estudo.py`

---

## Prioridade 2 — Publicações pendentes

- [ ] Publicar **T-192** Vorcaro: `_posts/estudos/2026-05-28-vorcaro-triangulo-carbono-mineracao-banco.md` + gosurf.site
- [ ] Extrair **9 posts P11 cluster** de `jekyll-posts-p11-cluster.tar.gz` → `_posts/governo/` e `_posts/escandalos/`
- [ ] Formalizar **P04b** como subcategoria em `METHODOLOGY-v2.2.md`

---

## Prioridade 3 — Infraestrutura

- [ ] Faixa **1449–1510** em `_data/` (`batch_file_only`) — merge linear futuro
- [ ] IPFS/archive.org — espelhamento fora-jurisdição (pendente recorrente)
- [ ] Integrar JustiçaWatch em `/data/justicawatch/` no repositório
- [ ] Recuperação shadowban **@araguaci**

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

| Destino | Arquivo |
| --- | --- |
| `_posts/governo/` | timeline-167 · 170 · 172 · 174 · 175 · 176 · 177 · 178 |
| `_posts/escandalos/` | novo-orcamento-secreto-stf-suspende-repasses |

⚠️ Checar antes de sobrescrever: `timeline-172` (desfile Janja) pode já existir em disco.

### Ação 3 — Formalizar T-208 e T-209

Criar estudos Jekyll para os 2 artefatos HTML `reserved`:

| ID | Artefato | Slug alvo |
| --- | --- | --- |
| T-208 | `narrativa-vs-evidencia.html` | `2026-05-28-narrativa-vs-evidencia-corpus-bridge` |
| T-209 | `justicawatch-brasil.html` | `2026-05-28-justicawatch-brasil-corpus-bridge` |

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
- Portal: https://lawfare-timeline.vercel.app/

---

<details>
<summary>Arquivo legado — links e rascunhos sociais</summary>

## TODOs (ícones)

- drone.svg > plane-departure
- reflect.svg > sun
- thermometer-low.svg > thermometer-half
- laser-pointer.svg >  bolt-lightning 

----

Prezado @PastorMalafaia, agora que o senhor faz parte da grade de vítimas, lhe apresento um portal com a linha de tempo de eventos que estão em curso no Brasil, baseado em analises da investigação do cientista de dados @leonardodias, que cedeu imagens de seu famoso artigo "lawfare", ele tem um projeto chamado "Guerra da Informação" que estuda este cenário. 

O portal usa as investigações dos jornalistas investigativos @david_agape_ e @EliVieiraJr, inspirado no projeto "Guerra da Informação" para criar uma área com linhas de tempo de vários episódios de falhas sistêmicas e escândalos no Brasil usando várias ferramentas de IA e diversos programas em python.

Incluo na conversa algumas pessoas cujo trabalho e opinião valorizo muito. Forte abraço. 🤝

## Aplicações

-🤐🕵️‍♂️ Censura no Brasil (2019-2025) 🌐
🔗 https://tinyurl.com/abusosupremo

Brasil e Big Techs: Impacto da Seção 301
🔗 https://tinyurl.com/brasil-x-bigtechs

- COAF e Ação de Moraes: Desafios nas Investigações Criminais
🔗 https://tinyurl.com/coaf-investigacoes

- https://tinyurl.com/abusosupremo
- https://tinyurl.com/lawfare-5w
- https://tinyurl.com/guiana-crime-transnacional
- https://tinyurl.com/crime-transnacionalNC
- https://tinyurl.com/crime-transnacional
- https://tinyurl.com/usaid-felipe-neto-mapa
- https://tinyurl.com/usaid-felipe-neto
- https://tinyurl.com/crise-diplomatica-stf-x-eua
- https://tinyurl.com/crise-diplomatica-resumo
- https://tinyurl.com/governanca-criminal
- https://tinyurl.com/vazatoga-mapa
- https://tinyurl.com/vazatoga2
- https://tinyurl.com/linhadetempo-impunes
- https://tinyurl.com/linhadetempo-jus
- https://tinyurl.com/linhadetempo-fin
- https://tinyurl.com/linhadetempo-gov
- https://tinyurl.com/linhadetempo-dossie
- https://tinyurl.com/linhadetempo-violador
- https://tinyurl.com/linhadetempo-tse
- https://tinyurl.com/linhadetempo-stf
- https://tinyurl.com/linhadetempo-lawfare
- https://tinyurl.com/crise-diplomatica
- https://tinyurl.com/supersalarios-ia
- https://tinyurl.com/privilegio-ia

## Lawfare

-🏛️ Lawfare - O Quê, Porquê, Quem, Onde, Quando
🔗 https://tinyurl.com/lawfare-5w

- 💥 Governança Criminal, 26% do BR vive sob regras de facções
🔗 https://tinyurl.com/governanca-criminal

## Linhas de Tempo Montadas:

-🏛️ Resumo Crise diplomática Brasil-EUA 📜
🔗 https://tinyurl.com/crise-diplomatica-stf-x-eua

-🧭 Linha do Tempo Crise diplomática Brasil-EUA 
🔗 https://tinyurl.com/crise-diplomatica

-📜 Interferências Judiciais Sistêmicas no Brasil
🔗 https://tinyurl.com/linhadetempo-lawfare

-✒️ STF no Contexto Político Brasileiro (2018-2025) ⚖️
🔗 https://tinyurl.com/linhadetempo-stf

-🌐 Parceria entre o Tribunal Superior Eleitoral (TSE) e USAID ⚖️
🔗 https://tinyurl.com/linhadetempo-tse

-📝 Ações do Violador de Direitos Humanos 💥
🔗 https://tinyurl.com/linhadetempo-dossie

-💰 Escândalos Políticos no Brasil
🔗 https://tinyurl.com/linhadetempo-gov

-🏛️ Escândalos Financeiros no Brasil (1995-2025)
🔗 https://tinyurl.com/linhadetempo-fin

-⚖️ Casos de Corrupção no Sistema Judiciário Brasileiro
🔗 https://tinyurl.com/linhadetempo-jus

-⛓️ Decisões Judiciais Beneficiando Criminosos no Brasil 💥
🔗 https://tinyurl.com/linhadetempo-impunes

- 🎭 Felipe Neto e Instituto Vero com ONGs estrangeiras (Open Society, Ford, EUA)
👉 https://tinyurl.com/usaid-felipe-neto
🔗 https://tinyurl.com/usaid-felipe-neto-mapa

Mapa Mental

https://mermaid.live/edit#pako:eNqNV8tu4zYU_RVCGBQJJollJ3Ec7TyOM0gxDyN2UqDIhpZoh41EqqSUySQI0H_oD7ToYtABZjXtZrb6k35JD6kXlbrTBnlKl-TlOeeee_PghTJiXuAlXEQJTa8EIUrKbGvrlMU8ZeQNyyT5hpwJnfEsx--XTMntbRNnvgiZSJGxO7x4yRSNy2eEjLOcFh-K3ySJGHG2qt939yNbb9-83K7fTWSypBkjxS9YrLlYSZWUm9URM6pCpjjVJJQJmS9Oe4v5tN16FefFRxFySlhCWMw4Fv_JNBn4g0EP3w7q0FMuqIlLmEAmuAVTAslML8ZNMudchzIgEyZ0riiQuOTF75rMZFx8yniIlMrIzlaaTHWmqFgzrqSut3qbMkHmMuQse09OZS4imnEpNNmaS4Q1RxJyMX82OPT3fN83N0DG_fbdCbPg4Hl_v-cf9dy3UwDH72hESWRyuBi3y86f9Y-aHf1-D59Yud8GdLGQK47fGzov5uOzk79--nkync3m7ZpxKrkkUA5XRia3QBxEajdZUXwxu2qjg1sLXXmjw4YDqSIHjXZtTbIl8dbC-m_Z1hnUZLT6qHQWYmfKm_VQDEDPU8USSRaKL3NBY8g0MhJ2eDhnueBGxCbnQc8fddSD-68Z0g6MCv9DsY2QUqQGYHlEAQh3smuwhpTJVpMUssRNpCJT6DiT3fwmMqZLPCsrjScpRBnyjD5liJKQJikV14YHvkZEi8U5bq2xk4q487TCkCsLv6pxqMrNRQjXsDdB0THDSCQV9gOXt1xnVNeUTEsGdyfX9JbV67vKtqoMsGXIlqyqgRsCMbuF04Zb-Qd1PZjMNsWZmu8c0fcD8p1UN_papppouVRYfM1CumZJG7jv9_xjlP0_YMNBAqVNXshYgzXlMOwP7OYl5OyuIsOg_yqPqZPQfvfOw6BCh1x5r_HTgP5jbmDVuwkFm55z6cMyPuKVu8qqNkoAUHyENdZDtXOoI9s-LncQkMU7nsHxUEsxGHuh6D2PCYqc0JBpLUmqwGHM1obTdvFgaBfPaGwP0kRQMk7offGHQK2aLFoX6jiQLaCgrSlThM-fNoLnHQNxfQJY4eQB8A1z3faWaZRTBRQ28NHv2_jGg2rqrJl10UBeZ2hjasVU3TlsM6C4nXZaiLOqvM1YFL_GXDPyQ66KTxEP6VOvLJcsWIKNJqpsGrrtVZ1Dp-Wh7SmW0FXldRF2SI0TuKiOq94WSlQwEzbIkFBZS936lmAKXLqaqCzJmBaqAM5n-GO1y9RRlxweU20yk5ktcdcmXnEstWaGT4gexa87vneWdCwPVKE3dhQ1Z4ioGZXmGPiwi3XdfCubp5s6fd2QHfDa4k1V8XnXLUIzoFDUGIxqk3IutNUWHipjZGX3uvKeertnkEZ94wGIeXI-hM3WyFoUHyj5tlaHm4AzIVmeDW2pubt5spJrubk_oPnROKMmyBS6BnjttJNunoyqGcWMapAz7IZH5ZoG5U1m0LaImGbFZ7QhC8Sq03vT4ssytoNQM72hwENqmATZ3fqug05YGJecG119rYxLuzBR5UjCzbi0ON1pXabph1WLaTIyN23wqDGwmtdkjuZUfEzcWpwpNB6UUGalHFaaMzDS0tEh26ylAYLjGb9vdPs_hoAppjwbDFthOcj72hhwmccCRbnkVZCR_7q1p9bkr4S3460Vj7wgUznb8RKGg82f3oMd073smiXsyguMhKm6Mf3kEWtQHN9LmdTLlMzX116worHGX3mKeYydcLpWtA3BuMPUBMNa5gV9v39oN_GCB-_OC3YP9w6PRkejg9GB3-8fj4bDHe-9CTvaGwwOhsPB8THe7PvDxx3v3p7r742ODo7djx2PRcZ_Xpf_lNj_TR7_BowhKAk

---

-⚖️ Linhas de Tempo da Guerra Silenciosa contra a Nação ⚔️
🔗 https://lawfare-timeline.vercel.app/

---

## 🤖 Ferramentas de Analise IA:

- ✨ Raio-X da Corrupção - Painel da Corrupção
🔗 https://tinyurl.com/ia-raio-x

- ✨ Soberania do Brasil - Análise Estratégica
🔗 https://tinyurl.com/soberania-ia

- ✨ A Arquitetura do Privilégio
🔗 https://tinyurl.com/privilegio-ia

- ✨ Sistema de Análise de Supersalários
🔗 https://tinyurl.com/supersalarios-ia

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

</details>
