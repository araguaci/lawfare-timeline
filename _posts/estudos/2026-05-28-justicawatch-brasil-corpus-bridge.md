---
id_corpus: "T-209"
thematic_track: true
title: "T-209 · JustiçaWatch Brasil — Índice Corpus"
description: Ponte T-156 — observatório de decisões de alto impacto (2005–2026); HC, progressões, nulidades e alertas, com revisão de 12/09/2026 (P01-B e cautelares).
date: 2026-05-28T12:00:00-03:00
image:
  path: "/assets/solid/gavel.svg"
tags: ["estudo", "justicawatch", "jusmonitor", "impunidade", "p01-B", "p02", "p06", "justica"]
categories: lawfare
mermaid: false
pin: false
---

- &nbsp;
{:toc .large-only}

# T-209 · JustiçaWatch Brasil — índice corpus

Entrada canônica do **registry T-156** no track temático Jekyll. O observatório documenta decisões judiciais brasileiras que resultaram em **soltura, progressão de regime ou arquivamento** em casos de crimes violentos — com dados verificáveis em portais oficiais.

| Camada | Recurso |
| --- | --- |
| **Produto canônico (2026-09-12)** | [jusmonitor.vercel.app](https://jusmonitor.vercel.app) — captura + decisões unificados |
| **Dossiê canônico (DS v1.1)** | [/artigos/t209-justicawatch-brasil.html](/artigos/t209-justicawatch-brasil.html) |
| Artefato HTML (gosurf.site, espelho) | [gosurf.site/jusmonitor](https://gosurf.site/jusmonitor) |
| Redirect legado | [justicawatch-brasil.html](/artigos/justicawatch-brasil.html) → jusmonitor |
| Espelho local | [/artigos/jusmonitor.html](/artigos/jusmonitor.html) |
| Data file | [`_data/justicewatch/justicawatch-brasil.json`](/_data/justicewatch/justicawatch-brasil.json) |
| Extract decisões | [`_data/extract_decisoes.py`](/_data/extract_decisoes.py) |
| Registry | T-156 · pages.json slug `jusmonitor` · domínio canônico `jusmonitor.vercel.app` |

> Conheça as decisões. Exija prestação de contas. Apresentação de casos não implica culpa do magistrado — registra impacto público verificável.

## Indicadores agregados (fontes oficiais)

| Indicador | Valor | Contexto |
| --- | ---: | --- |
| HC traficantes STJ (Seif) | 9.166 | 2024 — dossiê parlamentar; metodologia própria |
| HC/RHC tráfico STJ (ConJur) | 10.127 | 2024 até 26/dez — 49,1% de 20.114 concessões ([1808](/posts/2024-12-26-stj-concede-10127-hcsrhcs-a-acusados-de-trafico-em-2024-quase-metade-de-todas-as-concessoe/)) |
| Privilegiado no STJ | 1.578 | 2024 — HCs para aplicar o art. 33, §4º (ConJur) |
| HC tráfico STF | 577 | 2024 |
| Taxa reincidência BR | 42% | DEPEN/INFOPEN |
| População carcerária | 834k | SENAPPEN |
| Foragidos via HC Marco Aurélio | 21+ | Levantamento Estadão 2020 |
| Casos-âncora no JSON | 17 | Revisão 2026-09-12 (11 até 06/08 + P01-B + cautelares 2026) |

## Casos-âncora (2006–2026)

Revisão de **12/09/2026**: a edição de 06/08/2026 tinha 11 âncoras (até 2025). Entraram o lote P01-B (1804–1809) e as cautelares de 2026 (1798–1799). O caso 2023 (695 kg) foi enriquecido com Itaguaí / 2ª Turma (1806). Os números 9.166 e 10.127 ficam lado a lado.

| Ano | Tribunal | Caso | Tipo |
| ---: | --- | --- | --- |
| 2006 | STF | Progressão regime — crimes hediondos (HC 82.959) | HC coletivo 6×5 |
| 2009 | STF | Trânsito em julgado para início de pena | Mudança jurisprudencial |
| 2019 | STF | ADC 43/44/54 — reversão Lava Jato | ADC plenário |
| 2020 | STF | André do Rap — PCC solto e foragido | HC monocrático |
| 2020 | STF | 21 foragidos — liminares Marco Aurélio | Padrão intervalo de fuga |
| 2020 | STJ | HC coletivo COVID-19 — soltura por fiança | Efeito nacional |
| 2021 | TJ-GO | Lázaro Barbosa — progressão vs. laudo periculosidade | Reincidência fatal |
| 2021 | STJ | [EREsp 1.887.511 — quantidade não afasta privilegiado](/posts/2021-06-01-stj-3-secao-fixa-em-eresp-1887511-que-quantidade-de-droga-nao-afasta-por-si-so-trafico-pri/) | Embargos · **1804** |
| 2022 | STJ | Anulação busca pessoal — 122 porções devolvidas | Nulidade processual |
| 2022 | STJ | [311 kg cocaína GO — liberdade unânime](/posts/2022-09-26-stj-mantem-por-unanimidade-liberdade-de-motorista-preso-com-311kg-de-cocaina-em-goias/) | HC · **1805** |
| 2023 | STF | [695 kg Itaguaí — nulidade por fundada suspeita](/posts/2023-06-01-stf-2-turma-anula-apreensao-de-695kg-de-cocaina-no-porto-de-itaguai-por-vicio-de-fundada-s/) | Nulidade · **1806** |
| 2023 | STJ | [Controle — nega privilegiado a 110 kg de maconha](/posts/2023-09-11-caso-de-controle-stj-nega-trafico-privilegiado-a-reu-preso-com-110kg-de-maconha-recurso-do/) | Controle · **1809** |
| 2024 | STJ | [9.166 Seif / 10.127 ConJur — HCs de tráfico](/posts/2024-12-26-stj-concede-10127-hcsrhcs-a-acusados-de-trafico-em-2024-quase-metade-de-todas-as-concessoe/) | Levantamento · **1808** |
| 2024 | STJ | [832 kg cocaína PR–SP — liberdade](/posts/2024-10-30-stj-concede-liberdade-a-motorista-flagrado-com-832kg-de-cocaina-entre-parana-e-sao-paulo/) | HC liminar · **1807** |
| 2025 | STJ | Estupro vulnerável — erro de proibição | Distinguishing Súmula 593 |
| 2026 | TJ-RJ | [Oruam — revoga preventiva; permanece foragido](/posts/2026-07-31-justica-do-rio-revoga-prisao-preventiva-de-oruam-por-tentativa-de-homicidio-mas-rapper-per/) | Cautelar · **1798** |
| 2026 | TJ-SP | [Karen Tanaka / Japa do PCC — revoga tornozeleira](/posts/2026-08-01-justica-de-sp-revoga-tornozeleira-eletronica-de-karen-tanaka-a-japa-do-pcc-suspeita-de-lav/) | Cautelar · **1799** |

Detalhes expandidos, referências e links primários: [artefato completo](/artigos/jusmonitor.html).

## Alertas sistêmicos

| Nível | Alerta |
| --- | --- |
| 🔴 Alto | **Intervalo de fuga** — liminares monocráticas vs. colegiado |
| 🔴 Alto | **Tráfico privilegiado desfigurado** — EREsp 1.887.511; 311 kg (2022) e 832 kg (2024); 1.578 HCs de privilegiado em 2024. Controle: [1809](/posts/2023-09-11-caso-de-controle-stj-nega-trafico-privilegiado-a-reu-preso-com-110kg-de-maconha-recurso-do/) |
| 🔴 Alto | **Ausência de banco nacional de solturas** — BNMP sem reincidência |
| 🟠 Médio | **Cautelares 2026** — Oruam (desclassificação + foragido) e Tanaka (2 anos sem denúncia) |
| 🟠 Médio | Nulidades processuais anulando materialidade incontestável |
| 🟠 Médio | Laudos de periculosidade ignorados em progressões |
| 🟡 Atenção | Súmula 593 (estupro vulnerável) sob pressão de distinguishing |

## Padrões no corpus

**P02** — assimetria: HC coletivo hediondos (2006) vs. rigor seletivo em outros eixos ([T-205](/posts/duplo-padrao-judicial-corpus-bridge/)).

**P06** — prescrição/delonga: trânsito em julgado (2009→2019) como ferramenta de protelação.

**P03** — chokepoint: STF/STJ como terminal de solturas em escala nacional.

**P01-B** — quantidade de droga não afasta privilegiado (EREsp 1.887.511) e se materializa em 311 kg e 832 kg; o [1809](/posts/2023-09-11-caso-de-controle-stj-nega-trafico-privilegiado-a-reu-preso-com-110kg-de-maconha-recurso-do/) impede tratar o padrão como absoluto.

## Integração corpus

| Dossiê | Eixo |
| --- | --- |
| [T-206 SPLC](/posts/splc-modelo-brasil-corpus-bridge/) | Financiamento acadêmico → STF |
| [T-208 Narrativa vs Evidência](/posts/narrativa-vs-evidencia-corpus-bridge/) | Metodologia anti-viés |
| [Assimetria Punitiva](/posts/assimetria-punitiva/) | Zero × Zero |
| [Dosimetria impunidade](/posts/dosimetria-da-impunidade-lei-15402-ep72-tratamento-diferenciado/) | Lei 15.402/EP72 |
| [Foro privilegiado](/posts/foro-privilegiado-jurisdicao-como-escudo-brasil/) | Jurisdição como escudo |
| Cluster P01-B (1804–1809) | Quantidade vs. privilegiado; 9.166 vs 10.127 |
| [1798 Oruam](/posts/2026-07-31-justica-do-rio-revoga-prisao-preventiva-de-oruam-por-tentativa-de-homicidio-mas-rapper-per/) · [1799 Tanaka](/posts/2026-08-01-justica-de-sp-revoga-tornozeleira-eletronica-de-karen-tanaka-a-japa-do-pcc-suspeita-de-lav/) | Cautelares 2026 |

## Fontes primárias

- STF/STJ portais · CNJ painéis · DEPEN/INFOPEN · Dossiê Sen. Jorge Seif
- IPEA Atlas da Violência · Aos Fatos · Gazeta do Povo (série segurança pública)
- Schema JSON canônico: `_data/justicewatch/justicawatch-brasil.json` (`updated`: 2026-09-12)
- Stub legado (não usar como fonte): `_data/justicawatch/justicawatch-brasil.json`

*Dossiê T-209 · registry T-156 · CC0 · lawfare-timeline*
