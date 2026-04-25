#!/usr/bin/env python3
"""
Adiciona ao lawfare-full.json as novas entradas do lawfare-export-timeline-15abr2026.json
que ainda não estão no arquivo principal.

Entradas a adicionar:
- FPA-2025-001 a FPA-2026-003 (falas polêmicas de autoridades)
- IDs 146-153 (Operação Persona Non Grata + Vaza Toga original)
- IDs 1431-1436 (Dossiê Gilmar Mendes)
"""

import json
from pathlib import Path

BASE = Path(__file__).parent.parent
FULL_JSON = BASE / "_data" / "lawfare-full.json"

print(f"Lendo {FULL_JSON}...")
with open(FULL_JSON, encoding="utf-8") as f:
    data = json.load(f)

max_id = max(item["id"] for item in data["assuntos"])
next_id = max_id + 1
print(f"Último ID existente: {max_id} — próximo ID: {next_id}")

NOVAS_ENTRADAS = [
    # ── FPA: Falas Polêmicas de Autoridades ──────────────────────────────────
    {
        "titulo": "Lula — 'Eu sou um amante da democracia, porque os amantes são mais apaixonados pela amante do que pelas mulheres'",
        "data_evento": "2025-01-08",
        "data_iso": "2025-01-08T12:00:00.000Z",
        "categoria": "indecoro",
        "tags": ["indecoro", "lula", "sexismo", "liberdade de expressão", "gravidade-media"],
        "descricao": "No evento comemorativo do 2º aniversário do 8 de Janeiro, Lula faz declaração sexista improvisada que viraliza imediatamente — ignorada pela imprensa hegemônica. Janja da Silva sinalizou desaprovação ao vivo.",
        "relevancia": "media",
        "impacto_diplomatico": "N/A",
        "tipo_escandalo": "Declaração sexista / indecorosa em contexto público institucional",
        "fontes": [
            "Correio Braziliense, 08/01/2025 — https://www.correiobraziliense.com.br/politica/2025/01/7029830-lula-maridos-sao-mais-apaixonados-pela-amante-do-que-pelas-mulheres.html"
        ],
        "pessoas_envolvidas": ["Luiz Inácio Lula da Silva", "Janja da Silva"],
        "instituicoes_envolvidas": ["Palácio do Planalto", "Presidência da República"],
        "pais": "Brasil",
        "valor_envolvido": "N/A",
        "prioridade": 2,
        "fonte_arquivo": "_posts\\indecoro\\2025-01-08-lula-amante-da-democracia-declaracao-machista.md",
    },
    {
        "titulo": "Barroso admite ter pedido declarações de apoio dos EUA para pressionar militares brasileiros",
        "data_evento": "2025-05-13",
        "data_iso": "2025-05-13T12:00:00.000Z",
        "categoria": "indecoro",
        "tags": ["indecoro", "barroso", "stf", "soberania", "crise-diplomatica", "liberdade de expressão", "gravidade-alta"],
        "descricao": "Em evento do Grupo LIDE em Nova York, Barroso revela voluntariamente que pediu três vezes ao governo americano — incluindo ao Departamento de Estado — apoio para intimidar os militares brasileiros durante o período eleitoral de 2022. Convocado à Comissão de Segurança Pública do Senado.",
        "relevancia": "alta",
        "impacto_diplomatico": "Alto — admissão de interferência estrangeira coordenada por presidente do TSE/STF em período eleitoral",
        "tipo_escandalo": "Interferência estrangeira articulada por ministro do STF — questionamento da imparcialidade do TSE/2022",
        "fontes": [
            "CartaCapital, 13/05/2025 — https://www.cartacapital.com.br/politica/barroso-diz-que-pediu-apoio-dos-eua-para-evitar-um-golpe-de-estado-no-brasil/",
            "Senado Federal, 20/05/2025"
        ],
        "pessoas_envolvidas": ["Luís Roberto Barroso"],
        "instituicoes_envolvidas": ["STF", "TSE", "Departamento de Estado dos EUA", "Senado Federal"],
        "pais": "Brasil",
        "valor_envolvido": "N/A",
        "prioridade": 1,
        "fonte_arquivo": "_posts\\indecoro\\2025-05-13-barroso-admite-ter-pedido-apoio-dos-eua-para-pressionar-militares.md",
    },
    {
        "titulo": "Gilmar Mendes — '200 milhões de juristas palpitando sobre coisas do Supremo'",
        "data_evento": "2025-11-15",
        "data_iso": "2025-11-15T12:00:00.000Z",
        "categoria": "indecoro",
        "tags": ["indecoro", "gilmar-mendes", "stf", "soberania", "decano", "gravidade-alta"],
        "descricao": "Em entrevista sobre o Caso Banco Master, Gilmar Mendes equipara críticos do STF a 'técnicos de futebol leigos', negando legitimidade popular para questionar o tribunal — no contexto de conflito de interesse documentado de três ministros com o banco.",
        "relevancia": "alta",
        "impacto_diplomatico": "N/A",
        "tipo_escandalo": "Deslegitimação da soberania popular — blindagem corporativa do STF — Padrões P3 e P8",
        "fontes": [
            "Revista Oeste, 22/04/2026 — https://revistaoeste.com/politica/gilmar-critica-200-milhoes-de-juristas-com-opinioes-sobre-o-stf/"
        ],
        "pessoas_envolvidas": ["Gilmar Ferreira Mendes"],
        "instituicoes_envolvidas": ["STF", "Grupo Globo"],
        "pais": "Brasil",
        "valor_envolvido": "N/A",
        "prioridade": 1,
        "fonte_arquivo": "_posts\\indecoro\\2025-11-15-gilmar-mendes-200-milhoes-de-juristas-blindagem-do-stf.md",
    },
    {
        "titulo": "Moraes — 'Querem me derrubar faz tempo. Cabeças vão rolar'",
        "data_evento": "2026-02-26",
        "data_iso": "2026-02-26T12:00:00.000Z",
        "categoria": "indecoro",
        "tags": ["indecoro", "alexandre-de-moraes", "stf", "autoritarismo", "lawfare", "gravidade-alta"],
        "descricao": "Durante sessão judicial do STF no julgamento do caso Marielle Franco, após falha técnica, Alexandre de Moraes profere ameaça ao vivo. Contexto: contrato de R$ 129 milhões da esposa advogada com o Banco Master.",
        "relevancia": "alta",
        "impacto_diplomatico": "N/A",
        "tipo_escandalo": "Ameaça institucional em sessão judicial oficial — Padrões P3 e P5",
        "fontes": [
            "Gazeta do Povo, 26/02/2026 — https://www.gazetadopovo.com.br/sem-rodeios/querem-me-derrubar-moraes-causa-polemica-em-fala-no-stf/"
        ],
        "pessoas_envolvidas": ["Alexandre de Moraes"],
        "instituicoes_envolvidas": ["STF"],
        "pais": "Brasil",
        "valor_envolvido": "N/A",
        "prioridade": 1,
        "fonte_arquivo": "_posts\\indecoro\\2026-02-26-moraes-cabecas-vao-rolar-ameaca-em-sessao-judicial.md",
    },
    {
        "titulo": "Lula — 'Na China não deve ter esse problema' — declaração sobre gastos com pets a executivo chinês",
        "data_evento": "2026-03-26",
        "data_iso": "2026-03-26T12:00:00.000Z",
        "categoria": "indecoro",
        "tags": ["indecoro", "lula", "diplomacia", "china", "gravidade-media"],
        "descricao": "Na reinauguração da Caoa em Anápolis com executivo da Changan Automobile presente, Lula insinua que a China não tem problema com gastos com pets — declaração culturalmente inadequada que gerou reação de tutores de animais.",
        "relevancia": "media",
        "impacto_diplomatico": "Médio — insinuação cultural sensível perante representante do principal parceiro comercial do Brasil",
        "tipo_escandalo": "Declaração diplomaticamente inadequada em contexto de negócios bilaterais",
        "fontes": [
            "CNN Brasil, 26/03/2026 — https://www.cnnbrasil.com.br/politica/lula-cita-gastos-com-caes-e-diz-que-na-china-nao-deve-ter-esse-problema/",
            "Acessa.com, 27/03/2026",
            "ND Mais, 26/03/2026"
        ],
        "pessoas_envolvidas": ["Luiz Inácio Lula da Silva", "Zhu Huarong"],
        "instituicoes_envolvidas": ["Presidência da República", "Caoa", "Changan Automobile"],
        "pais": "Brasil",
        "valor_envolvido": "N/A",
        "prioridade": 2,
        "fonte_arquivo": "_posts\\indecoro\\2026-03-26-lula-na-china-nao-deve-ter-esse-problema-sobre-pets.md",
    },
    {
        "titulo": "Gilmar Mendes — 'É preciso ter adultos na sala' — blindagem do STF no Caso Master",
        "data_evento": "2026-04-22",
        "data_iso": "2026-04-22T12:00:00.000Z",
        "categoria": "indecoro",
        "tags": ["indecoro", "gilmar-mendes", "stf", "banco-master", "corrupcao", "gravidade-alta"],
        "descricao": "Em entrevista sobre o Caso Banco Master, Gilmar minimiza os vínculos de ministros com o banco ('Não acho que seja um escândalo do STF') e diz que críticos precisam de 'adultos na sala' — enquanto esposa de Moraes tinha contrato de R$ 129mi, irmãos de Toffoli eram sócios de resort de Vorcaro, e ele próprio viajou em avião da empresa de Vorcaro.",
        "relevancia": "alta",
        "impacto_diplomatico": "N/A",
        "tipo_escandalo": "Blindagem corporativa do STF — minimização de conflitos de interesse documentados — Padrões P3 e P8",
        "fontes": [
            "Revista Oeste, 22/04/2026 — https://revistaoeste.com/politica/gilmar-critica-200-milhoes-de-juristas-com-opinioes-sobre-o-stf/"
        ],
        "pessoas_envolvidas": ["Gilmar Ferreira Mendes"],
        "instituicoes_envolvidas": ["STF", "Banco Master", "Grupo Globo"],
        "pais": "Brasil",
        "valor_envolvido": "N/A",
        "prioridade": 1,
        "fonte_arquivo": "_posts\\indecoro\\2026-04-22-gilmar-mendes-adultos-na-sala-caso-banco-master.md",
    },
    # ── Operação Persona Non Grata ────────────────────────────────────────────
    {
        "titulo": "Detenção de Alexandre Ramagem pelo ICE em Orlando",
        "data_evento": "2026-04-13",
        "data_iso": "2026-04-13T12:00:00.000Z",
        "categoria": "crise-diplomatica",
        "tags": ["crise-diplomatica", "lawfare", "operacoes", "alexandre-de-moraes", "extradição", "PF", "gravidade-alta"],
        "descricao": "Ex-deputado e ex-diretor da ABIN Alexandre Ramagem é detido em Orlando pelo ICE. PF anuncia 'cooperação policial internacional bem-sucedida'. O Notice to Appear usado não menciona crimes brasileiros nem extradição formal — operação usou canal migratório como substituto de extradição judicial.",
        "relevancia": "alta",
        "impacto_diplomatico": "Alto — uso indevido de canal migratório americano contornando o Departamento de Estado",
        "tipo_escandalo": "Uso político transfronteiriço do aparato de segurança pública — Padrões P3 e P7",
        "fontes": [
            "PF nota oficial 13/04/2026",
            "Metrópoles / Samuel Pancher",
            "BBC News Brasil"
        ],
        "pessoas_envolvidas": ["Alexandre Ramagem", "Andrei Rodrigues", "Marcelo Ivo de Carvalho"],
        "instituicoes_envolvidas": ["Polícia Federal", "ICE/DHS", "ABIN"],
        "pais": "Brasil",
        "valor_envolvido": "N/A",
        "prioridade": 1,
        "fonte_arquivo": "_posts\\crise-diplomatica\\2026-04-13-detencao-de-alexandre-ramagem-pelo-ice-em-orlando.md",
    },
    {
        "titulo": "Ramagem liberado pelo ICE após 48h — sem deportação",
        "data_evento": "2026-04-15",
        "data_iso": "2026-04-15T12:00:00.000Z",
        "categoria": "crise-diplomatica",
        "tags": ["crise-diplomatica", "lawfare", "impunidade", "extradição", "alexandre-de-moraes", "gravidade-alta"],
        "descricao": "Alexandre Ramagem é liberado sem fiança 48h após detenção, contrariando a versão da PF de 'cooperação bem-sucedida'. Agradece à 'alta cúpula da administração Trump'. Classifica Andrei Rodrigues de 'vergonha'. Autoridades americanas concluíram que situação migratória era regular — asilo em andamento.",
        "relevancia": "alta",
        "impacto_diplomatico": "Alto — exposição pública do fracasso da operação e início da crise bilateral",
        "tipo_escandalo": "Falha operacional e narrativa falsa de cooperação bem-sucedida",
        "fontes": [
            "Metrópoles",
            "Gazeta do Povo",
            "O Antagonista"
        ],
        "pessoas_envolvidas": ["Alexandre Ramagem", "Paulo Figueiredo", "Eduardo Bolsonaro", "Andrei Rodrigues"],
        "instituicoes_envolvidas": ["ICE/DHS", "Polícia Federal"],
        "pais": "Brasil",
        "valor_envolvido": "N/A",
        "prioridade": 1,
        "fonte_arquivo": "_posts\\crise-diplomatica\\2026-04-15-ramagem-liberado-pelo-ice-apos-48h-sem-deportacao.md",
    },
    {
        "titulo": "EUA iniciam apuração interna sobre papel da PF na detenção de Ramagem",
        "data_evento": "2026-04-17",
        "data_iso": "2026-04-17T12:00:00.000Z",
        "categoria": "crise-diplomatica",
        "tags": ["crise-diplomatica", "lawfare", "operacoes", "PF", "MLAT", "soberania", "gravidade-critica"],
        "descricao": "Autoridades norte-americanas abrem processo formal de apuração para identificar se a PF tentou usar o ICE como mecanismo alternativo à extradição formal, contornando a competência do Departamento de Estado. A distinção deportação migratória (DHS/ICE) × extradição judicial (Dept. de Estado) é juridicamente central.",
        "relevancia": "alta",
        "impacto_diplomatico": "Crítico — investigação americana sobre conduta de agência brasileira em território dos EUA",
        "tipo_escandalo": "Abuso de canal diplomático — deslocamento de competência — Padrão P7",
        "fontes": [
            "Estado de Minas",
            "Gazeta do Povo"
        ],
        "pessoas_envolvidas": ["Marcelo Ivo de Carvalho", "Andrei Rodrigues"],
        "instituicoes_envolvidas": ["ICE/DHS", "Departamento de Estado EUA", "Polícia Federal"],
        "pais": "Brasil",
        "valor_envolvido": "N/A",
        "prioridade": 1,
        "fonte_arquivo": "_posts\\crise-diplomatica\\2026-04-17-eua-inicia-apuracao-sobre-papel-da-pf-na-detencao-de-ramagem.md",
    },
    {
        "titulo": "Delegado Marcelo Ivo de Carvalho expulso dos EUA — persona non grata",
        "data_evento": "2026-04-20",
        "data_iso": "2026-04-20T12:00:00.000Z",
        "categoria": "crise-diplomatica",
        "tags": ["crise-diplomatica", "lawfare", "operacoes", "PF", "soberania", "gravidade-critica"],
        "descricao": "Bureau of Western Hemisphere Affairs exige saída do delegado de ligação da PF no ICE em Miami. Declaração: 'No foreigner gets to game our immigration system to both circumvent formal extradition requests and extend political witch hunts into U.S. territory.' Expulsão compulsória sem comunicação prévia ao Brasil.",
        "relevancia": "alta",
        "impacto_diplomatico": "Crítico — maior incidente diplomático bilateral Brasil-EUA em décadas",
        "tipo_escandalo": "Violação da soberania territorial americana — abuso do canal de cooperação policial — Padrões P3, P6 e P7",
        "fontes": [
            "@WHAAsstSecty (20/04/2026)",
            "@EmbaixadaEUA",
            "Metrópoles",
            "TV Globo",
            "Gazeta do Povo"
        ],
        "pessoas_envolvidas": ["Marcelo Ivo de Carvalho", "Andrei Rodrigues"],
        "instituicoes_envolvidas": ["Bureau of Western Hemisphere Affairs", "Departamento de Estado EUA", "Polícia Federal", "Embaixada EUA no Brasil"],
        "pais": "Brasil",
        "valor_envolvido": "N/A",
        "prioridade": 1,
        "fonte_arquivo": "_posts\\crise-diplomatica\\2026-04-20-delegado-marcelo-ivo-expulso-dos-eua-persona-non-grata.md",
    },
    {
        "titulo": "Silêncio do Itamaraty e da PF após expulsão — padrão de supressão narrativa",
        "data_evento": "2026-04-20",
        "data_iso": "2026-04-20T18:00:00.000Z",
        "categoria": "crise-diplomatica",
        "tags": ["crise-diplomatica", "impunidade", "lawfare", "accountability", "soberania", "gravidade-alta"],
        "descricao": "Após a expulsão compulsória de delegado da PF pelos EUA — o incidente diplomático mais grave em décadas —, nem Itamaraty nem PF emitiram nota pública. Itamaraty: 'não comentaria o caso'. Ausência de prestação de contas — Padrão P6.",
        "relevancia": "alta",
        "impacto_diplomatico": "Alto — silêncio consolida narrativa americana (political witch hunts) como única versão oficial pública",
        "tipo_escandalo": "Falha de accountability institucional — supressão narrativa deliberada — Padrão P6",
        "fontes": [
            "Metrópoles",
            "Gazeta do Povo"
        ],
        "pessoas_envolvidas": ["Andrei Rodrigues"],
        "instituicoes_envolvidas": ["Itamaraty/MRE", "Polícia Federal"],
        "pais": "Brasil",
        "valor_envolvido": "N/A",
        "prioridade": 1,
        "fonte_arquivo": "_posts\\crise-diplomatica\\2026-04-20-silencio-do-itamaraty-e-pf-apos-expulsao-diplomatica.md",
    },
    # ── Antecedentes ──────────────────────────────────────────────────────────
    {
        "titulo": "Delegado Marcelo Ivo mata motociclista dirigindo embriagado com CNH vencida — absolvido 4 anos depois",
        "data_evento": "2016-10-23",
        "data_iso": "2016-10-23T12:00:00.000Z",
        "categoria": "impunidade",
        "tags": ["impunidade", "operacoes", "corporativismo", "PF", "gravidade-critica"],
        "descricao": "Delegado Marcelo Ivo de Carvalho atropela e mata Francisco Lopes da Silva Neto (36 anos) na Rodovia Raposo Tavares em Sorocaba. Viatura PF em uso pessoal. Bafômetro: 0,49 mg/L (acima do limite criminal). CNH vencida há 1 ano e 3 meses. Absolvido em 2020 por 'insuficiência de provas'. Nenhuma consequência disciplinar. Em 2023, nomeado oficial de ligação PF no ICE em Miami.",
        "relevancia": "alta",
        "impacto_diplomatico": "N/A",
        "tipo_escandalo": "Corporativismo institucional — impunidade documentada de servidor público — Padrão P6",
        "fontes": [
            "Jornal Cruzeiro do Sul, 27/10/2016",
            "A Investigação, 17/04/2026",
            "Poder360"
        ],
        "pessoas_envolvidas": ["Marcelo Ivo de Carvalho", "Francisco Lopes da Silva Neto (vítima)", "Verlange Xavier da Silva (viúva)"],
        "instituicoes_envolvidas": ["Polícia Federal", "TJSP"],
        "pais": "Brasil",
        "valor_envolvido": "Pensão viúva: R$ 800/mês",
        "prioridade": 1,
        "fonte_arquivo": "_posts\\impunidade\\2016-10-23-delegado-marcelo-ivo-mata-motociclista-embriagado-cnh-vencida-absolvido.md",
    },
    {
        "titulo": "Moraes ordena monitoramento de cidadã americana Flávia Magalhães — oficialato Miami acionado",
        "data_evento": "2024-01-03",
        "data_iso": "2024-01-03T12:00:00.000Z",
        "categoria": "lawfare",
        "tags": ["lawfare", "alexandre-de-moraes", "soberania", "censura", "liberdade de expressão", "gravidade-critica"],
        "descricao": "Alexandre de Moraes ordena prisão e aciona o Oficialato de Ligação da PF em Miami (DPF Marcelo Ivo) contra Flávia Magalhães — brasileira naturalizada americana desde 2012, em Pompano Beach — por publicações nas redes sociais. Flávia não era ré em nenhum processo. Moraes bloqueou passaporte e a classificou como 'evadida', desconsiderando cidadania americana. Caso fundamentou sanções Magnitsky (out/2025).",
        "relevancia": "alta",
        "impacto_diplomatico": "Crítico — extensão ilegal da jurisdição brasileira sobre cidadã americana em solo americano",
        "tipo_escandalo": "Perseguição transfronteiriça de cidadão estrangeiro por manifestação política — Padrões P1, P3 e P7",
        "fontes": [
            "Gazeta do Povo",
            "A Investigação, 17/04/2026",
            "Paulo Faria (advogado de Flávia)"
        ],
        "pessoas_envolvidas": ["Alexandre de Moraes", "Marcelo Ivo de Carvalho", "Flávia Magalhães (vítima)", "Fábio Mertens"],
        "instituicoes_envolvidas": ["STF", "Polícia Federal", "CGCPI", "ICE/DHS"],
        "pais": "Brasil",
        "valor_envolvido": "N/A",
        "prioridade": 1,
        "fonte_arquivo": "_posts\\lawfare\\2024-01-03-moraes-ordena-monitoramento-de-cidada-americana-flavia-magalhaes.md",
    },
    # ── Vaza Toga Original ────────────────────────────────────────────────────
    {
        "titulo": "Vaza Toga — Folha de S.Paulo publica mensagens internas do TSE/STF",
        "data_evento": "2024-08-01",
        "data_iso": "2024-08-01T12:00:00.000Z",
        "categoria": "vazatoga",
        "tags": ["vazatoga", "alexandre-de-moraes", "stf", "tse", "lawfare", "imprensa", "liberdade de expressão", "gravidade-alta"],
        "descricao": "Folha de S.Paulo (Fábio Serapião e Glenn Greenwald) publica a série 'Vaza Toga': mensagens de WhatsApp de assessores de Moraes revelando uso da estrutura do TSE fora dos ritos formais. Eduardo Tagliaferro identificado como suspeito. Moraes abre inquérito contra ex-assessor e inclui jornalistas no Inq. das Fake News — acumula funções de investigado-indireto, investigador e futuro julgador.",
        "relevancia": "alta",
        "impacto_diplomatico": "N/A",
        "tipo_escandalo": "Abuso de poder institucional — perseguição a jornalistas e fonte — acúmulo de funções incompatíveis — Padrões P2 e P3",
        "fontes": [
            "Folha de S.Paulo / A Investigação — https://www.ainvestigacao.com/p/moraes-e-forcado-a-anular-audiencia",
            "CartaCapital",
            "Revista Oeste"
        ],
        "pessoas_envolvidas": ["Alexandre de Moraes", "Eduardo de Oliveira Tagliaferro", "Fábio Serapião", "Glenn Greenwald"],
        "instituicoes_envolvidas": ["STF", "TSE", "Folha de S.Paulo", "Polícia Federal"],
        "pais": "Brasil",
        "valor_envolvido": "N/A",
        "prioridade": 1,
        "fonte_arquivo": "_posts\\vazatoga\\2024-08-01-vaza-toga-folha-publica-mensagens-internas-tse-stf.md",
    },
    # ── Dossiê Gilmar Mendes ──────────────────────────────────────────────────
    {
        "titulo": "Receita Federal produz relatório com indícios de lavagem de dinheiro contra Gilmar Mendes — auditores são punidos",
        "data_evento": "2018-05-01",
        "data_iso": "2018-05-01T12:00:00.000Z",
        "categoria": "decano",
        "tags": ["gilmar-mendes", "stf", "corrupcao", "impunidade", "receita-federal", "decano", "gravidade-alta"],
        "descricao": "Sistema automatizado da Receita identificou variação patrimonial inexplicada de R$ 700 mil de Gilmar e indícios de lavagem de dinheiro de Guiomar (declarou receber R$ 2,7 mi; escritório Bermudes declarou pagar R$ 40 mil — 70x menos). Gilmar acionou Toffoli; Moraes suspendeu investigações e afastou auditores. Em 2025, PF abriu inquérito contra os 4 servidores — com tornozeleira.",
        "relevancia": "alta",
        "impacto_diplomatico": "N/A",
        "tipo_escandalo": "Corporativismo sistêmico — inversão investigativa — investigadores de ministro tornaram-se investigados — Padrão P2",
        "fontes": [
            "Cruzeiro do Sul",
            "Conjur, 16/05/2018 — https://www.conjur.com.br/2018-mai-16/receita-federal-gilmar-mendes-guiomar-feitosa/",
            "Folha de S.Paulo"
        ],
        "pessoas_envolvidas": ["Gilmar Ferreira Mendes", "Guiomar Feitosa Mendes", "Dias Toffoli", "Alexandre de Moraes"],
        "instituicoes_envolvidas": ["STF", "Receita Federal", "Polícia Federal", "Escritório Sérgio Bermudes"],
        "pais": "Brasil",
        "valor_envolvido": "Variação patrimonial: R$ 700 mil (Gilmar) | Movimentação total casal: R$ 17 milhões+",
        "prioridade": 1,
        "fonte_arquivo": "_posts\\decano\\2018-05-01-receita-federal-relatorio-gilmar-mendes-auditores-punidos.md",
    },
    {
        "titulo": "Gilmar Mendes libera 21 presos da Lava Jato no Rio em 30 dias por decisões monocráticas",
        "data_evento": "2018-07-01",
        "data_iso": "2018-07-01T12:00:00.000Z",
        "categoria": "decano",
        "tags": ["gilmar-mendes", "stf", "impunidade", "lava-jato", "decano", "decisao-judicial", "gravidade-alta"],
        "descricao": "Em 30 dias, Gilmar Mendes concedeu habeas corpus monocráticos determinando a soltura de 21 presos da Lava Jato no Rio. Uma soltura a cada 1,4 dias. Nenhuma decisão passou pelo plenário ou turma do STF. O uso mais extensivo documentado do instrumento monocrático como mecanismo de esvaziamento em massa de operação anticorrupção.",
        "relevancia": "alta",
        "impacto_diplomatico": "N/A",
        "tipo_escandalo": "Uso de poder monocrático para esvaziamento em série de operação anticorrupção — impunidade industrial",
        "fontes": [
            "O Globo — https://oglobo.globo.com/brasil/gilmar-mendes-soltou-21-presos-da-lava-jato-no-rio-em-30-dias-22930512",
            "Gazeta do Povo"
        ],
        "pessoas_envolvidas": ["Gilmar Ferreira Mendes"],
        "instituicoes_envolvidas": ["STF", "Ministério Público Federal"],
        "pais": "Brasil",
        "valor_envolvido": "N/A",
        "prioridade": 1,
        "fonte_arquivo": "_posts\\decano\\2018-07-01-gilmar-mendes-solta-21-presos-lava-jato-rio-em-30-dias.md",
    },
    {
        "titulo": "IDP recebe mais de R$ 7 milhões de empresas com processos no gabinete de Gilmar, parte com cláusula de confidencialidade",
        "data_evento": "2016-12-01",
        "data_iso": "2016-12-01T12:00:00.000Z",
        "categoria": "decano",
        "tags": ["gilmar-mendes", "stf", "corrupcao", "conflito-de-interesse", "idp", "decano", "gravidade-alta"],
        "descricao": "Entre 2011 e 2016, 23 empresas patrocinaram o IDP (instituto de Gilmar) com R$ 7 milhões. Muitos eram ocultos. Souza Cruz pagou R$ 2 mi com cláusula de sigilo; JBS R$ 2 mi; Google R$ 200 mil sem exibição da marca. 300+ processos dessas empresas passaram pelo gabinete de Gilmar. Bradesco concedeu empréstimo de R$ 26 mi a 11,35% ao ano — condição indisponível em 99,92% dos casos — liberado no mesmo dia em que o filho de Gilmar comprou cota por R$ 12 mi.",
        "relevancia": "alta",
        "impacto_diplomatico": "N/A",
        "tipo_escandalo": "Captura institucional — financiamento oculto de instituto como canal de lobby judicial",
        "fontes": [
            "Cruzeiro do Sul — https://www.crusoe.com.br/ed/idp-gilmar-mendes-financiamento/",
            "Conjur, 09/01/2017 — https://www.conjur.com.br/2017-jan-09/empresas-processos-stf-financiam-instituto-gilmar-mendes/",
            "Repórter Brasil"
        ],
        "pessoas_envolvidas": ["Gilmar Ferreira Mendes", "Francisco Mendes (filho)"],
        "instituicoes_envolvidas": ["IDP", "STF", "Bradesco", "JBS", "Souza Cruz", "Google"],
        "pais": "Brasil",
        "valor_envolvido": "R$ 7 milhões+ (2011-2016) | Empréstimo Bradesco: R$ 26 milhões",
        "prioridade": 1,
        "fonte_arquivo": "_posts\\decano\\2016-12-01-idp-recebe-7-milhoes-de-empresas-com-processos-no-gabinete-de-gilmar.md",
    },
    {
        "titulo": "Fórum Jurídico de Lisboa — 'Gilmar Palusa': o maior evento de lobby judicial do planeta",
        "data_evento": "2024-07-01",
        "data_iso": "2024-07-01T12:00:00.000Z",
        "categoria": "decano",
        "tags": ["gilmar-mendes", "stf", "corrupcao", "conflito-de-interesse", "idp", "extravagancia", "decano", "gravidade-alta"],
        "descricao": "O Fórum Jurídico de Lisboa, organizado pelo IDP em parceria com FGV e Universidade de Lisboa, reúne anualmente a cúpula do poder brasileiro com executivos de BTG (5 representantes + jantar reservado), JBS, iFood, Vale, Meta, Bradesco, Google, Amazon, TikTok. Encontros fora de agendas oficiais dos ministros. Custo público: R$ 1,3 milhão em diárias e jatinhos da FAB. Transparência Internacional: 'maior evento de lobby judicial do planeta'.",
        "relevancia": "alta",
        "impacto_diplomatico": "N/A",
        "tipo_escandalo": "Captura institucional — encontros não oficiais entre magistrados e litigantes corporativos em Portugal a custo público",
        "fontes": [
            "Transparência Internacional",
            "Conjur, Julho 2024",
            "O Globo"
        ],
        "pessoas_envolvidas": ["Gilmar Ferreira Mendes"],
        "instituicoes_envolvidas": ["IDP", "STF", "STJ", "TCU", "BTG Pactual", "JBS", "Vale", "Meta", "Bradesco"],
        "pais": "Brasil",
        "valor_envolvido": "Custo público: R$ 1,3 milhão (diárias e jatinhos FAB)",
        "prioridade": 1,
        "fonte_arquivo": "_posts\\decano\\2024-07-01-forum-juridico-de-lisboa-gilmar-palusa-lobby-judicial.md",
    },
    {
        "titulo": "Gilmar anula monocraticamente quebra de sigilo da CPI do Banco Master por duas vezes",
        "data_evento": "2024-05-01",
        "data_iso": "2024-05-01T12:00:00.000Z",
        "categoria": "decano",
        "tags": ["gilmar-mendes", "stf", "banco-master", "decisao-judicial", "impunidade", "decano", "gravidade-alta"],
        "descricao": "CPI do Senado aprovou quebra de sigilo de empresa ligada a Toffoli no Caso Master. Gilmar anulou monocraticamente — e repetiu quando a CPI insistiu. Paralelamente, viajou de Diamantino a Brasília em avião Phenom 300 operado por empresa de Daniel Vorcaro, dono do Banco Master. Afirmou não saber da ligação.",
        "relevancia": "alta",
        "impacto_diplomatico": "N/A",
        "tipo_escandalo": "Conflito de interesse demonstrável — uso do poder monocrático para proteger investigados com vínculo pessoal — Padrão P3",
        "fontes": [
            "Conjur, Maio 2024 — https://www.conjur.com.br/2024-mai-gilmar-anula-cpi-master/",
            "Folha de S.Paulo",
            "O Globo"
        ],
        "pessoas_envolvidas": ["Gilmar Ferreira Mendes", "Daniel Vorcaro", "Dias Toffoli", "Marcos Molina"],
        "instituicoes_envolvidas": ["STF", "Senado Federal", "Banco Master", "FGC", "Marfrig"],
        "pais": "Brasil",
        "valor_envolvido": "Caso Master envolve tentativa de transferência de R$ 330 bilhões ao FGC",
        "prioridade": 1,
        "fonte_arquivo": "_posts\\decano\\2024-05-01-gilmar-anula-quebra-de-sigilo-cpi-banco-master-duas-vezes.md",
    },
    {
        "titulo": "Gilmar suspende monocraticamente lei de impeachment de 1950 e eleva quórum para processar ministro do STF de 41 para 54 votos",
        "data_evento": "2024-12-01",
        "data_iso": "2024-12-01T12:00:00.000Z",
        "categoria": "decano",
        "tags": ["gilmar-mendes", "stf", "impunidade", "decano", "soberania", "decisao-judicial", "gravidade-alta"],
        "descricao": "Gilmar Mendes suspendeu partes da Lei de Impeachment de 1950 elevando de 41 para 54 votos (2/3 do Senado) o quórum para processar ministro do STF. Decisão monocrática, sem plenário. Gilmar foi alvo de 18 pedidos de impeachment entre 2015 e 2020. O caso mais explícito de ministro alterando as regras de seu próprio julgamento.",
        "relevancia": "alta",
        "impacto_diplomatico": "N/A",
        "tipo_escandalo": "Autopreservação institucional — alteração unilateral das regras de responsabilização do STF pelo próprio beneficiário",
        "fontes": [
            "Conjur, Dezembro 2024 — https://www.conjur.com.br/2024-dez-gilmar-suspende-lei-impeachment/",
            "Folha de S.Paulo",
            "O Globo"
        ],
        "pessoas_envolvidas": ["Gilmar Ferreira Mendes"],
        "instituicoes_envolvidas": ["STF", "Senado Federal"],
        "pais": "Brasil",
        "valor_envolvido": "N/A",
        "prioridade": 1,
        "fonte_arquivo": "_posts\\decano\\2024-12-01-gilmar-mendes-suspende-lei-impeachment-eleva-quorum-stf.md",
    },
]

# Atribui IDs sequenciais
for i, entrada in enumerate(NOVAS_ENTRADAS):
    entrada["id"] = next_id + i

print(f"\nAdicionando {len(NOVAS_ENTRADAS)} novas entradas...")
for e in NOVAS_ENTRADAS:
    titulo_curto = e["titulo"][:70] + "..." if len(e["titulo"]) > 70 else e["titulo"]
    print(f"  [{e['id']}] {e['categoria'].upper()} | {titulo_curto}")

data["assuntos"].extend(NOVAS_ENTRADAS)

# Atualiza metadados
data["total"] = len(data["assuntos"])
data["data_extração"] = "2026-04-24"
data["periodo"] = "1855-01-01 a 2026-04-24"
data["fonte_original"] = (
    "D:\\_deploy\\lawfare-timeline\\_posts + "
    "_data\\lawfare-timeline-124-145.json + "
    "_data\\lawfare-export-timeline-15abr2026.json"
)
data["nota"] = (
    "Extraído de _posts (scripts/extrair_posts_para_json.py) e mesclado com "
    "lawfare-timeline-124-145.json e lawfare-export-timeline-15abr2026.json. "
    "Atualizado em 2026-04-24 com 20 novas entradas: "
    "FPA (falas polêmicas), Operação Persona Non Grata, Vaza Toga original e Dossiê Gilmar Mendes."
)

print(f"\nTotal de entradas após atualização: {data['total']}")
print(f"Escrevendo {FULL_JSON}...")

with open(FULL_JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✓ lawfare-full.json atualizado com sucesso!")
print(f"  IDs adicionados: {next_id} → {next_id + len(NOVAS_ENTRADAS) - 1}")
