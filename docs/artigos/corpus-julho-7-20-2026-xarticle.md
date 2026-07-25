# Depois do interrogatório de Flávio: 12 IDs, três colisões resolvidas e um sidecar de 1891

Entre **7 e 20 de julho de 2026**, o LAWFARE Timeline não só registrou eventos — **fechou arquitetura**. Duas lacunas metodológicas abertas desde abril (P06-B e P10 autônomo), quatro colisões de ID no pipeline editorial, um track histórico pre-1990 sem tocar no main track, e a faixa **1620–1628** consolidada com validação **0 erros**.

O ponto de partida é político: em **07/07**, Alexandre de Moraes determinou interrogatório de Flávio Bolsonaro pela PF em dez dias — pré-candidato presidencial a cinco meses da eleição (**ID 1618**). O corpus já carregava o cluster Bolsonaro (1613–1617) e o estudo **T-221** (*nemo judex* formalizado pela DPU na AP 2782). O que veio depois foi infraestrutura: sincronizar o que estava certo no dossiê mas errado no tracking.

## Main track 1609–1628 — o que entrou

### Narco-financeiro e INSS (09/07)

| ID | Evento |
|----|--------|
| 1609 | OFAC sanciona Shimada/Victory Trading (PCC) |
| 1610 | PF diverge publicamente da avaliação OFAC |
| 1611 | Victory × Wave Intermediações — rede Arpar, ev-alleged |

Estudos **T-219** (Farra INSS) e **T-220** (convergência PCC-OFAC × Arpar × INSS) fecham o eixo transnacional que o dashboard v3.3 já mapeava como P10.

### Lawfare contemporâneo (16–19/07)

| ID | Evento | Padrão |
|----|--------|--------|
| 1620 | Auditorias KPMG/PwC/EY/Crowe — pareceres sem ressalvas Master/Reag | P10 |
| 1621 | Moraes/Milei — visitas domiciliar Bolsonaro | — |
| 1622 | Operação Hawala (PCC/CV/TCP) | — |
| 1623 | Consulado HK / Valler — ev-contested | P02 |
| 1624 | Revisão criminal Bolsonaro (ex-colisão 1520/176) | — |
| 1625 | CPI Crime Organizado — encerra sem relatório | **P06-B** |
| 1626 | Vácuo sucessão RJ — Couto interino pós-renúncia Castro | P03 |
| 1627 | Fux nega Ruas como governador interino (ADI 7942) | P03 |
| 1628 | USTR recomenda +25% citando Pix, desmatamento, STF/plataformas | — |

Próximo ID main livre: **1629**. Track temático: **T-225**.

## Taxonomia — o que o repositório decidiu

### P06-B formalizado

Prescrição parlamentar não é acidente processual. CPI/CPMI que termina sem relatório aprovado é **mecanismo regimental**. Três âncoras:

- CPMI Banestado (2004) — texto nunca votado
- CPMI INSS (28/03/2026) — relatório Gaspar, 4.340 páginas, rejeitado 19×12
- CPI Crime Organizado (14/04/2026) — rejeitado 6×4, zero encaminhamento formal

Duas das três são de **2026** e convergem no cluster Master/Vorcaro/Arpar. O achado fica no ar; a instituição não consolida.

### P10 autônomo vs P11 substrato

Pergunta encerrada no dashboard desde abril, mas ainda pendente em notas de sessão:

- **P10** = infraestrutura de *serviço* (lavagem jurídico-financeira compartilhada)
- **P11** = arquitetura macroeconômica (Selic + desindustrialização + captura de fluxo)

Estudos **T-222** (P10 promovido) e **T-223** (P12-B assimetria analítica eleitoral) fecham a rodada temática.

### P13 arquivado

Consulado Hong Kong reclassificado como **P02** — N=1 insuficiente para padrão autônomo.

> A falha estrutural não é um vício do sistema — é o design principal.
> — Matriz de Indulgência Sistêmica v3.3

## Colisões resolvidas — por que importa

| Batch propôs | Ocupado por | Resolvido |
|--------------|-------------|-----------|
| 1609 USTR | OFAC Shimada 1609 | → **1628** |
| 1624 CPI CO | Bolsonaro revisão 1624 | → **1625** |
| 1577/1580 RJ | ADPF Cremesp / Virgílio | → **1626–1627** |
| 1520/176 | Post P04b imprensa | 1520 restaurado; Bolsonaro → **1624** |

Colisão de ID não é bug de planilha. É sinal de fila editorial acelerada sem gate de namespace. O pipeline agora exige batch com `id` numérico explícito antes de merge.

## Sidecar histórico — T-224 (19/07)

Decisão editorial: **não** consumir main 1629–1641 para eventos de 1890–1930.

- Sidecar `_data/precedentes-republica.json` — **14 entradas** `PREC-AAAA-NN`
- Track `historical_precedents` registrado no sync
- Estudo **T-224** como índice editorial

Lacuna crítica fechada: **PREC-1891-14** documenta que Castilhos foi deposto 14 meses (nov/1891–jan/1893), retornou por acordo com Floriano Peixoto para barrar Silveira Martins, foi reeleito sem concorrentes, e a Guerra da Degola começou **uma semana** após posse contestada. Isso corrige a leitura de PREC-1891-01 e PREC-1895-04, que tratavam permanência como contínua. Fontes reforçadas com **CPDOC/FGV**.

Paralelos estruturais mapeados: Encilhamento → P05/P11; Comissão Verificadora → P06-B; restrição HC 1926 → P03; retorno Castilhos → P03.

## Integridade e ferramentas

- `padroes-sistemicos-dashboard.html` → **v3.3** (espelhado em `docs/`)
- `METHODOLOGY.md` → **v2.4** (P06-B, P10/P11)
- `scripts/sync_todo_current.py` — batches mistos main + T-XXX
- `validate-ids.ps1` → **0 erros** (gaps permanentes 1449–1480, 1506–1510 aceitos)
- Lacuna **Bucha 1831** fechada — sem lastro verificável para 11/08
- `_data/export-bolsonaro-timeline.json` — 152 entradas deduplicadas

## Snapshot final (20/07/2026)

| Track | Last | Próximo |
|-------|------|---------|
| Main | 1628 | 1629 |
| Thematic | T-224 | T-225 |
| Historical | PREC-1930-07 | — |

## Onde ler

- Timeline: [lawfare-timeline.vercel.app](https://lawfare-timeline.vercel.app)
- Dashboard v3.3: [gosurf.site/padroes-sistemicos-dashboard](https://gosurf.site/padroes-sistemicos-dashboard)
- T-224 Precedentes República: `/posts/2026-07-19-precedentes-republica-1891-1930/`
- T-222 P10 autônomo · T-223 P12-B assimetria eleitoral

*Dossiê completo, links de posts individuais e JSON sidecar no primeiro reply.*
