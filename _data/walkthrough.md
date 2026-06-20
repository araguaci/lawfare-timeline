# Walkthrough — Sincronização dos Batches do Todo Realizada

Todas as 18 entradas dos 3 batches do diretório `_data/todo/` foram sincronizadas com sucesso, sem duplicatas, renumeradas a partir de `1577` e com todas as referências internas atualizadas.

## Mudanças Realizadas

1. **Geração de Posts Jekyll:** Foram criados 18 arquivos Markdown sob as respectivas pastas de categorias em `_posts/`:
   * **`_posts/escandalos/`** (7 posts)
   * **`_posts/crise-diplomatica/`** (6 posts)
   * **`_posts/lawfare/`** (5 posts)
2. **Correção de Referências Cruzadas:** Varremos o conteúdo dos novos posts para atualizar referências aos IDs antigos que mudaram de posição para evitar links quebrados:
   * Em `2025-01-20-trump-assina-eo-14157-...md`, as referências aos IDs `1533` e `1535` foram corrigidas para `1585` e `1587`.
   * Em `2006-07-14-jose-serra-endossa-bornhausen-...md`, a referência ao ID `1529` foi corrigida para `1581`.
3. **Integração no Banco de Dados:**
   * `_data/lawfare.json` foi atualizado com as 18 novas entradas ordenadas pelo ID, elevando o total para **1557** assuntos cadastrados (excluindo os slots vazios correspondentes aos gaps permanentes).
   * `_data/lawfare-unified-corpus.json` recebeu as 18 novas entradas estruturadas com referências de fontes verificáveis.
4. **Atualização do claude.ai-corpus-ids-sync.json:**
   * O track `main` foi atualizado para registrar a faixa `[1577, 1594]` sob `confirmed_batches`.
   * A propriedade `next_available` foi definida para `1595`.
5. **Arquivamento:** Os arquivos processados foram movidos de `_data/todo/` para `_data/processados/`:
   * `lawfare-1525-1531-pt-pcc-p04b-retroativo.json`
   * `lawfare-1532-1537-contexto-fto-internacional.json`
   * `lawfare-1572-1576-bloqueio-internet.json`
   * `lawfare-consolidado-1518-1572.json`

---

## Mapeamento de IDs Sincronizados

A tabela abaixo apresenta a renomeação efetuada para evitar conflitos:

| ID Original | Novo ID | Data Evento | Categoria | Título do Post |
| :---: | :---: | :---: | :---: | :--- |
| **1525** | **1577** | 2006-05-02 | `escandalos` | Alckmin responsabiliza Lula pelo crescimento do PCC — contexto eleitoral 2006 |
| **1526** | **1578** | 2006-07-13 | `escandalos` | Bornhausen (PFL) afirma que PT pode estar 'manuseando' ações do PCC em São Paulo |
| **1527** | **1579** | 2006-07-14 | `escandalos` | José Serra endossa Bornhausen e afirma ver 'indícios de elo entre PT e PCC' |
| **1528** | **1580** | 2006-09-05 | `escandalos` | Senador Arthur Virgílio (PSDB) culpa Lula pelos ataques do PCC e pela porosidade das fronteiras |
| **1529** | **1581** | 2011-01-01 | `crise-diplomatica` | WikiLeaks revela: Serra pediu cooperação americana de inteligência contra o PCC sem informar governo federal |
| **1530** | **1582** | 2014-11-30 | `escandalos` | Aécio Neves afirma ter perdido eleição de 2014 para 'organização criminosa', não para partido político |
| **1531** | **1583** | 2016-03-01 | `escandalos` | Reinaldo Azevedo (Veja) publica coluna 'O PCC, o PT e as eleições' — enquadramento de equivalência |
| **1532** | **1584** | 2025-01-20 | `crise-diplomatica` | Trump assina EO 14157 — cartéis internacionais como FTO/SDGT: arquitetura jurídica |
| **1533** | **1585** | 2025-02-20 | `crise-diplomatica` | State Department designa 8 organizações criminosas latino-americanas como FTO/SDGT |
| **1534** | **1586** | 2025-07-11 | `crise-diplomatica` | Ovidio Guzmán (filho de El Chapo) se declara culpado em Chicago com forfeiture de US$ 80 mi |
| **1535** | **1587** | 2025-06-25 | `crise-diplomatica` | FinCEN designa CIBanco, Intercam e Vector como 'primary money laundering concern' |
| **1536** | **1588** | 2026-03-10 | `escandalos` | Pesquisa FBSP/Datafolha 'Medo do Crime e Eleições 2026' — 41,2% convivem com facções no bairro |
| **1537** | **1589** | 2025-02-05 | `crise-diplomatica` | Memorando Pam Bondi 'Total Elimination of Cartels and TCOs' — doutrina DOJ |
| **1572** | **1590** | 2025-06-01 | `lawfare` | Estudo técnico documenta ~46.000 sites bloqueados na internet brasileira, maioria sob sigilo |
| **1573** | **1591** | 2025-06-01 | `lawfare` | 18.000 domínios bloqueados têm potencial de derrubar 250 milhões de domínios colateralmente |
| **1574** | **1592** | 2025-06-01 | `lawfare` | Aderência das operadoras às ordens de bloqueio varia entre 3% e 90% — apenas 15% cumpridas |
| **1575** | **1593** | 2025-06-01 | `lawfare` | Anatel confirma: não avalia nem monitora domínios bloqueados por convênio com Ministério da Fazenda |
| **1576** | **1594** | 2026-06-15 | `escandalos` | Relato técnico de bloqueio seletivo por horário e conteúdo nas operadoras brasileiras — ano eleitoral |

---

## Resultados da Validação

Foram executadas as ferramentas de sincronia e testes de integridade do repositório:
1. `python tools/sync_corpus_ids.py`
   * **Resultado:** `sync OK: main last=1594 next=1595; thematic last=209 next=210`
2. `pwsh -File tools/validate-ids.ps1`
   * **Resultado:** Sem erros (`STATUS: AVISO` devido apenas aos gaps canônicos aceitos `1449-1480` e `1506-1510`).
