# O corpus fechou duas lacunas que estavam abertas desde abril: P06-B e P10

Hoje (18/07/2026) o LAWFARE Timeline não ganhou um escândalo novo. Ganhou **sincronização metodológica** — duas decisões analíticas que já existiam no dossiê, mas ainda apareciam como pendências no tracking.

A primeira: **P06-B**, prescrição parlamentar. CPI e CPMI que terminam sem relatório aprovado não é acidente processual. É mecanismo regimental. O levantamento do *Congresso em Foco* aponta **8 comissões desde 2004**. Três âncoras fecham a formalização:

- CPMI do Banestado (dez/2004) — texto nunca votado
- CPMI do INSS (28/03/2026) — relatório Gaspar, 4.340 páginas, 216+ indiciados, rejeitado 19×12
- CPI do Crime Organizado (14/04/2026) — relatório rejeitado 6×4, zero encaminhamento formal

Duas das três são de **2026** e convergem no mesmo cluster: Banco Master, Vorcaro, rede Arpar. O achado fica no ar como documento de relator; a instituição brasileira não consolida. Em parte dos casos, quem age é vetor externo (OFAC). Isso também é dado.

A segunda: **P10 autônomo vs P11 substrato**. Pergunta encerrada desde abril no dashboard, mas ainda registrada como aberta em notas de sessão. Definição consolidada:

- **P10** = infraestrutura de *serviço* (quem presta lavagem jurídico-financeira compartilhada)
- **P11** = arquitetura macroeconômica (Selic + desindustrialização + captura de fluxo)

Não competem. Um é o operador; o outro é o incentivo que o alimenta.

> A falha estrutural não é um vício do sistema — é o design principal.
> — Matriz de Indulgência Sistêmica v3.3

## O que entrou no repositório hoje

### Taxonomia e dashboard

- `padroes-sistemicos-dashboard.html` atualizado para **v3.3** (espelhado em `docs/`)
- Post `_posts/estudos/2026-04-17-padroes-sistemicos-dashboard.md` alinhado
- `METHODOLOGY.md` → **v2.4** com linha P06-B e nota P10/P11
- Proposta **P13 arquivada**: Consulado Hong Kong reclassificado como **P02** (N=1 insuficiente)

### Main track 1620–1625

| ID | Evento |
|----|--------|
| 1620 | Auditorias Master/Reag sem ressalvas (P10) |
| 1621 | Moraes/Milei — visitas domiciliar Bolsonaro |
| 1622 | Operação Hawala (PCC/CV/TCP) |
| 1623 | Consulado HK / Valler — **P02**, ev-contested |
| 1624 | Revisão criminal Bolsonaro (ex-colisão 1520/176/1621) |
| 1625 | CPI Crime Organizado — encerra sem relatório (**P06-B**) |

Próximo ID main: **1626**. Track temático: **T-224**.

### Correções de integridade

- Colisão **1520/176** resolvida: post canônico da revisão criminal → **1624**
- Colisão **1621** (Moraes/Milei vs Bolsonaro) desfeita
- Duplicata **1622** (consulado + Hawala) removida
- `fontes_verificadas` do ID 1624 corrigido no unified corpus
- Validação `validate-ids.ps1`: **0 erros**, STATUS AVISO (gaps permanentes 1449–1480 e 1506–1510)

### Pipeline e ferramentas

- `scripts/sync_todo_current.py` — batches mistos main + T-XXX
- `_data/export-bolsonaro-timeline.json` — 152 entradas deduplicadas
- `scripts/README.md` documentado
- Lacuna **Bucha 1831** fechada (sem lastro verificável para 11/08)

## Onde ler

- Dashboard interativo: [gosurf.site/padroes-sistemicos-dashboard](https://gosurf.site/padroes-sistemicos-dashboard)
- Timeline: [lawfare-timeline.vercel.app](https://lawfare-timeline.vercel.app)
- Post resumo dos padrões: `/posts/padroes-sistemicos-dashboard/`

*Dossiê completo e links de posts individuais no primeiro reply.*
