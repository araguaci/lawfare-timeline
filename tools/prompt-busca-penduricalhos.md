# Prompt de Busca — Categoria Penduricalhos
**Projeto:** lawfare-timeline  
**Propósito:** Manter a timeline atualizada com eventos recentes de penduricalhos institucionais  
**Retorno esperado:** JSON estruturado pronto para montagem de artigos  
**Última entrada na timeline:** 2025-07-01  
**Próximo período a cobrir:** 2025-07-02 até hoje  
**Última revisão:** 2026-05-11

---

## CONTEXTO ANALÍTICO

"Penduricalhos" são benefícios extras (auxílios, indenizações, bônus, licenças convertidas em pagamento, viagens custeadas pelo erário, moradia oficial, veículos oficiais, passagens aéreas, supersalários acima do teto constitucional de R$ 46.366,19) concedidos a:

- **Magistrados** (juízes federais e estaduais, desembargadores, ministros do STF/STJ/TST/TSE/STM)
- **Membros do MP** (promotores, procuradores do MPF/MPE/MPDFT/MPM)
- **Conselheiros** (TCU, TCEs, CNJ, CNMP)
- **Outras autoridades** (delegados de carreira, defensores públicos, servidores de cargos DAS-6)

**Critério de inclusão:** O evento deve demonstrar auto-benefício institucional com recursos públicos, violação do teto constitucional, opacidade na concessão, ou contraste gritante com indicadores de serviço público (50% da população brasileira sem acesso a esgoto tratado; 35 milhões sem água potável).

---

## PROMPT PARA BUSCA EM IA (Perplexity / ChatGPT / Gemini)

Copie e cole o bloco abaixo na ferramenta de busca de sua preferência:

```
Busque notícias e dados publicados entre 2025-07-02 e 2026-05-11 sobre penduricalhos, supersalários, benefícios extraordinários e vantagens indevidas concedidas a magistrados, promotores, procuradores, conselheiros de tribunais de contas e autoridades públicas brasileiras. A última entrada já registrada na timeline é de 2025-07-01 (supersalários no judiciário crescem 49,3% em 2024). Não repetir eventos já cobertos.

Foco específico:
1. Pagamentos acima do teto constitucional (atualmente R$ 46.366,19)
2. Auxílios (moradia, alimentação, transporte, creche, saúde) em valores que superam o teto quando somados ao salário base
3. Indenizações por férias não gozadas, licenças-prêmio convertidas em dinheiro
4. Uso de aviões da FAB, carros oficiais ou seguranças pessoais fora de situações de risco documentado
5. Bônus por acúmulo de processos, gratificações por "produtividade" ou "disponibilidade"
6. Benefícios aprovados em sessões sigilosas ou sem publicidade adequada
7. Decisões do CNJ, CNMP, TCU ou STF sobre penduricalhos
8. Projetos de lei (PL) ou medidas provisórias que criem ou ampliem penduricalhos
9. Sentenças judiciais que anulem cortes de penduricalhos
10. Dados do Portal da Transparência sobre remunerações acima do teto

Para cada evento encontrado, forneça:
- Data exata ou período
- Nome(s) do(s) beneficiado(s) quando público
- Instituição envolvida
- Valor monetário quando disponível
- URL da fonte primária (portal oficial, veículo jornalístico confiável)
- Contexto: qual penduricalho específico, como foi aprovado, se há contestação

Formate a resposta seguindo o JSON schema fornecido abaixo.
```

---

## JSON SCHEMA DE RETORNO

O retorno deve seguir exatamente este schema para integração direta na timeline:

```json
{
  "meta": {
    "prompt_versao": "1.0",
    "data_busca": "2026-05-11",
    "periodo_coberto": "2025-07-02/2026-05-11",
    "total_eventos": 0,
    "fonte_busca": "perplexity|chatgpt|gemini|manual"
  },
  "assuntos": [
    {
      "id": null,
      "titulo": "Título factual em português, sem adjetivos valorativos",
      "data_evento": "YYYY-MM-DD",
      "data_iso": "YYYY-MM-DDT00:00:00.000Z",
      "categoria": "penduricalhos",
      "tags": [
        "magistrado|promotor|procurador|conselheiro|autoridade",
        "supersalario|auxilio|indenizacao|bonus|viagem|veiculo|seguranca",
        "stf|stj|tst|tse|trf|tj|mpf|mpe|tcu|tce|cnj|cnmp",
        "estado-uf"
      ],
      "descricao": "Descrição factual: data, local, cargo do beneficiado, tipo de penduricalho, valor, quem concedeu. Sem julgamento de valor.",
      "relevancia": "alta|media|baixa",
      "impacto_diplomatico": "N/A",
      "tipo_escandalo": "supersalario|penduricalho|nepotismo|viagem-publica|uso-indevido-erario|fundo-especial|licenca-remunerada",
      "fontes": [
        "https://url-fonte-primaria.com.br/artigo"
      ],
      "pessoas_envolvidas": [
        "Nome Completo (cargo, instituição)"
      ],
      "instituicoes_envolvidas": [
        "Nome da Instituição"
      ],
      "pais": "Brasil",
      "valor_envolvido": "R$ 0.000,00 ou N/A se não divulgado",
      "prioridade": 1,
      "fonte_arquivo": "_posts/penduricalhos/YYYY-MM-DD-slug-do-titulo.md",
      "contraste_social": {
        "indicador": "descrição do indicador de desigualdade para contextualização",
        "dado": "valor ou percentual do indicador",
        "fonte_indicador": "IBGE|FGV|SNIS|OMS|IPEA"
      },
      "vetor_correcao": {
        "disponivel": true,
        "mecanismo": "CNJ|CNMP|TCU|TCE|MPF|ação popular|CPI|legislação",
        "status": "pendente|em_andamento|arquivado|sem_previsao"
      },
      "artigo": {
        "front_matter": {
          "layout": "post",
          "title": "Título Para o Artigo",
          "categories": "penduricalhos",
          "image_path": "/assets/solid/gift.svg",
          "article_id": "YYYYMMDD",
          "description": "YYYY-MM-DD-Local-tipo-beneficio",
          "tags": ["tag1", "tag2"]
        },
        "corpo": {
          "heading": "Título Completo - Subtítulo Descritivo - Tipo de Evento",
          "detalhes": {
            "ano": "YYYY",
            "data": "YYYY-MM-DD",
            "descricao": "Descrição expandida do evento",
            "decisao": "Tipo de concessão ou aprovação",
            "beneficiado": "Nome ou grupo beneficiado",
            "departamento": "Instituição que concedeu",
            "local": "Cidade/Estado",
            "valor": "R$ 0.000,00"
          },
          "envolvidos": ["Nome (cargo)"],
          "consequencias": ["consequência documentada 1", "consequência documentada 2"],
          "subcategorias": ["penduricalho", "tipo-especifico"],
          "fontes_formatadas": [
            "[Título da Fonte](https://url)"
          ],
          "contraste_constitucional": "Contexto sobre teto constitucional e violação",
          "contraste_social": "Contexto sobre desigualdade: saneamento, renda, acesso a serviços públicos"
        }
      }
    }
  ]
}
```

---

## REGRAS DE PREENCHIMENTO

### Campo `titulo`
- Factual, sem adjetivos: **"Auxílio-Moradia Para Desembargador TJ-SP — R$ 4.500 Mensais"** ✓
- Não use: "Escândalo do Auxílio" ou "Roubalheira no Judiciário" ✗

### Campo `relevancia`
| Valor | Critério |
|-------|----------|
| `alta` | Valor > R$ 50 mil/mês, ou afeta > 100 beneficiados, ou há decisão do CNJ/STF sobre o caso |
| `media` | Valor entre R$ 10–50 mil/mês, ou caso individual de cargo alto (ministro, desembargador) |
| `baixa` | Dados estatísticos, estudos, casos de menor valor monetário ou impacto restrito |

### Campo `prioridade`
| Valor | Critério |
|-------|----------|
| `1` | Evento com fonte verificada, valor documentado, beneficiado identificado |
| `2` | Dado estatístico agregado, relatório institucional, sem beneficiado nominal |
| `3` | Referência doutrinária, estudo acadêmico, contexto histórico |

### Campo `tags` (máximo 10, todas em minúsculas)
Combine sempre: **[cargo] + [tipo-penduricalho] + [instituição] + [UF]**

Exemplos de tags válidas:
`magistrado`, `promotor`, `procurador`, `desembargador`, `ministro-stf`  
`supersalario`, `auxilio-moradia`, `auxilio-alimentacao`, `auxilio-creche`, `auxilio-transporte`  
`indenizacao-ferias`, `licenca-premio`, `bonus-produtividade`, `dezembrada`  
`voo-fab`, `carro-oficial`, `seguranca-pessoal`, `viagem-exterior`  
`stf`, `stj`, `tst`, `tse`, `stm`, `trf1`...`trf6`, `tj-sp`...`tj-am`  
`mpf`, `mpe`, `mpdft`, `tcu`, `tce-sp`...`tce-am`, `cnj`, `cnmp`  
`sp`, `rj`, `mg`, `rs`, `pr`, `ba`, `pe`, `ce`, `go`, `df`...

### Campo `contraste_social`
Sempre inclua quando o valor for > R$ 20 mil. Indicadores disponíveis:
- **Saneamento:** "47,4% dos brasileiros sem acesso a esgoto tratado (SNIS 2023)"
- **Água:** "35 milhões de brasileiros sem acesso à água potável (SNIS 2023)"
- **Bolsa Família:** "Benefício médio do Bolsa Família: R$ 681/mês (MDS 2024)"
- **Salário mínimo:** "Salário mínimo em 2025: R$ 1.518/mês"
- **Saúde:** "SUS gasta R$ 2.000/habitante/ano (Ministério da Saúde 2024)"
- **Educação pública:** "Gasto por aluno/ano no ensino fundamental público: R$ 8.700 (INEP 2023)"

### Campo `vetor_correcao`
- `disponivel: true` → existe mecanismo ativo capaz de reverter o benefício
- `disponivel: false` → sem mecanismo operacional disponível (captura sistêmica)

---

## FONTES PRIMÁRIAS PARA MONITORAR

### Portais Oficiais
- Portal da Transparência: `portaldatransparencia.gov.br`
- CNJ — Estatísticas Judiciárias: `cnj.jus.br/pesquisas-judiciarias`
- CNMP — Dados Abertos: `cnmp.mp.br/portal/dados-abertos`
- TCU — Fiscalizações: `tcu.gov.br`
- Diário da Justiça eletrônico de cada tribunal

### Veículos Jornalísticos (investigativos)
- Agência Pública, Piauí, The Intercept Brasil
- Folha de S.Paulo (Dados), O Globo (investigações)
- G1/Globo, UOL, Estado de S.Paulo
- Congresso em Foco, Metrópoles

### Organizações da Sociedade Civil
- Transparência Brasil: `transparencia.org.br`
- JOTA: `jota.info`
- Movimento Voto Consciente

---

## EXEMPLO DE SAÍDA VÁLIDA

```json
{
  "meta": {
    "prompt_versao": "1.0",
    "data_busca": "2026-05-11",
    "periodo_coberto": "2026-02-10/2026-05-11",
    "total_eventos": 1,
    "fonte_busca": "perplexity"
  },
  "assuntos": [
    {
      "id": null,
      "titulo": "Auxílio-Moradia Para Membros Do CNMP — R$ 10 Mil Mensais Aprovados Em Sessão Administrativa",
      "data_evento": "2026-04-15",
      "data_iso": "2026-04-15T00:00:00.000Z",
      "categoria": "penduricalhos",
      "tags": ["procurador", "auxilio-moradia", "cnmp", "df", "supersalario"],
      "descricao": "Em 15 de abril de 2026, o CNMP aprovou em sessão administrativa o pagamento de auxílio-moradia de R$ 10.000 mensais a membros do Ministério Público lotados no Distrito Federal, mesmo para aqueles com imóvel funcional. O benefício foi aprovado sem publicidade prévia e eleva a remuneração mensal bruta a R$ 56.366,19, acima do teto constitucional.",
      "relevancia": "alta",
      "impacto_diplomatico": "N/A",
      "tipo_escandalo": "penduricalho",
      "fontes": [
        "https://www.transparencia.org.br/blog/cnmp-auxilio-moradia-2026"
      ],
      "pessoas_envolvidas": [],
      "instituicoes_envolvidas": ["CNMP", "Ministério Público"],
      "pais": "Brasil",
      "valor_envolvido": "R$ 10.000,00/mês por membro",
      "prioridade": 1,
      "fonte_arquivo": "_posts/penduricalhos/2026-04-15-auxilio-moradia-membros-cnmp-r10-mil-mensais.md",
      "contraste_social": {
        "indicador": "Brasileiros sem acesso a esgoto tratado",
        "dado": "47,4% da população (SNIS 2023)",
        "fonte_indicador": "SNIS"
      },
      "vetor_correcao": {
        "disponivel": true,
        "mecanismo": "TCU",
        "status": "pendente"
      },
      "artigo": {
        "front_matter": {
          "layout": "post",
          "title": "Auxílio-Moradia Para Membros Do CNMP — R$ 10 Mil Mensais",
          "categories": "penduricalhos",
          "image_path": "/assets/solid/gift.svg",
          "article_id": "20260415",
          "description": "2026-04-15-Brasília-auxilio-moradia-cnmp",
          "tags": ["procurador", "auxilio-moradia", "cnmp", "df"]
        },
        "corpo": {
          "heading": "Auxílio-Moradia Para Membros Do CNMP — R$ 10 Mil Mensais Aprovados Em Sessão Administrativa - Concessão de Penduricalho",
          "detalhes": {
            "ano": "2026",
            "data": "2026-04-15",
            "descricao": "CNMP aprovou auxílio-moradia de R$ 10.000 mensais para membros do MP no DF",
            "decisao": "Aprovação em sessão administrativa do CNMP",
            "beneficiado": "Membros do Ministério Público no Distrito Federal",
            "departamento": "Conselho Nacional do Ministério Público — CNMP",
            "local": "Brasília, DF",
            "valor": "R$ 10.000,00/mês por membro"
          },
          "envolvidos": ["CNMP (concedente)"],
          "consequencias": [
            "Remuneração bruta sobe para R$ 56.366,19, acima do teto constitucional de R$ 46.366,19",
            "Precedente para pleitos em outros ramos do MP"
          ],
          "subcategorias": ["penduricalho", "auxilio-moradia"],
          "fontes_formatadas": [
            "[Transparência Brasil — CNMP Auxílio-Moradia 2026](https://www.transparencia.org.br/blog/cnmp-auxilio-moradia-2026)"
          ],
          "contraste_constitucional": "O teto constitucional fixado pelo art. 37, XI da CF/88 é de R$ 46.366,19 (2025). O benefício aprovado eleva a remuneração bruta em 21,6% acima deste limite.",
          "contraste_social": "No Brasil, 47,4% da população (SNIS 2023) não tem acesso a esgoto tratado. O auxílio-moradia mensal aprovado equivale a 6,5 salários mínimos (R$ 1.518) ou a 14,7 benefícios médios do Bolsa Família (R$ 681)."
        }
      }
    }
  ]
}
```

---

## CHECKLIST DE VALIDAÇÃO ANTES DE INSERIR NA TIMELINE

- [ ] Fonte primária verificável e acessível (URL funcionando)
- [ ] Data precisa ou intervalo delimitado (não "recentemente")
- [ ] Valor monetário documentado ou campo `valor_envolvido: "N/A"` explícito
- [ ] Não duplica entrada existente em `_data/lawfare.json`
- [ ] `categoria` está corretamente definida como `"penduricalhos"`
- [ ] Máximo 10 tags, todas em minúsculas, sem acentos
- [ ] `fonte_arquivo` segue o padrão: `_posts/penduricalhos/YYYY-MM-DD-slug.md`
- [ ] Slug do arquivo: tudo minúsculo, sem acentos, hífens no lugar de espaços
- [ ] Campo `contraste_social` preenchido quando valor > R$ 20 mil
- [ ] `id` definido como `null` (será atribuído ao inserir no JSON principal)
