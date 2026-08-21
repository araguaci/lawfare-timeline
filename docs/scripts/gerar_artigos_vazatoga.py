#!/usr/bin/env python3
"""Gera posts temáticos T-255–T-262 da série Vaza Toga."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "_posts" / "vazatoga"
IMG = "/assets/img/vazatoga.jpg"

FRONT = """\
---
layout: post
title: "{title}"
description: "{desc}"
date: 2026-08-20T12:00:00.000Z
image:
  path: "{img}"
tags: {tags}
categories: vazatoga
timeline_id: {tid}
id_corpus: "T-{tid}"
thematic_track: true
status: confirmed
mermaid: false
pin: false
---

- &nbsp;
{{:toc .large-only}}

"""


def write_post(tid: int, slug: str, title: str, desc: str, tags: list[str], body: str) -> Path:
    tags_yaml = "[" + ", ".join(f'"{t}"' for t in tags) + "]"
    fm = FRONT.format(title=title.replace('"', '\\"'), desc=desc.replace('"', '\\"'), img=IMG, tags=tags_yaml, tid=tid)
    path = POSTS / f"2026-08-20-t-{tid}-{slug}.md"
    path.write_text(fm + body.strip() + "\n", encoding="utf-8", newline="\n")
    print(path.relative_to(ROOT))
    return path


def main() -> None:
    POSTS.mkdir(parents=True, exist_ok=True)

    write_post(
        255,
        "vaza-toga-sintese-geral",
        "T-255 · Vaza Toga — síntese geral (2022–2026)",
        "Índice da série: Folha/Greenwald (VT1) → Ágape/Vieira/Shellenberger (VT2, 4, 5) → Revista Oeste (VT3). Gabinete paralelo de Moraes, INQ 4781 e cinco capítulos documentados.",
        ["vazatoga", "estudo", "inq4781", "p03", "p04", "alexandre-de-moraes"],
        r'''
# T-255 · Vaza Toga — síntese geral

**ID:** T-255 | **Série:** Vaza Toga | **Suplanta como índice de leitura:** [T-207](/posts/2026-05-29-vaza-toga-corpus-bridge/)

> Vaza Toga é a série de reportagens iniciada em agosto/2024 pela Folha de S.Paulo com Glenn Greenwald e Fábio Serapião, e continuada principalmente por David Ágape, Eli Vieira e Michael Shellenberger/Civilization Works. Baseia-se em mensagens, áudios e documentos de WhatsApp de assessores do ministro Alexandre de Moraes (STF/TSE), especialmente Eduardo Tagliaferro (ex-chefe da AEED/TSE) e Airton Vieira.

Portal de referência: [ainvestigacao.com](https://www.ainvestigacao.com/). Artefato HTML deste capítulo: [vt1-censura-criticos.html](/vazatoga/vt1-censura-criticos.html). Hub: [/vazatoga/](/vazatoga/).

## O que a série documenta

Não era a Assessoria Especial de Enfrentamento à Desinformação (AEED/TSE) identificando problemas por conta própria. O pedido partia do ministro — via o juiz auxiliar Airton Vieira — para Eduardo Tagliaferro, que montava relatório mesmo quando não encontrava conteúdo incriminador. A cadeia de comando é: Moraes → Vieira → Tagliaferro → relatório formal produzido a posteriori.

A definição de "desinformação" era elástica o bastante para enquadrar opinião contrária ao STF ou ao governo, inclusive posts antigos ou já apagados. Nenhum dos alvos documentados nesta fase teve acesso ao relatório que fundamentou a medida antes de ela ser executada.

## Cronologia condensada

| Data | Capítulo | Evento | Corpus |
| --- | --- | --- | --- |
| 23–29/08/2022 | VT4 | Busca contra empresários; relatório Shor com metadados posteriores à operação | [1869](/posts/2022-08-23-moraes-ordena-busca-e-apreensao-contra-empresarios-bolsonaristas-em-5-estados-com-base-em-/), [1870](/posts/2022-08-27-fabricacao-retroativa-de-provas-infiltrado-colaboradora-informal-e-delegado-produzem-relat/) |
| 30/10–01/12/2022 | VT3 | Palver/DX, PM-BA, Constantino/Fiuza, Gettr, Zambelli | [1883](/posts/2022-11-22-gabinete-paralelo-ordena-bloqueio-dos-colunistas-rodrigo-constantino-e-guilherme-fiuza-por/)–[1887](/posts/2022-10-30-instituto-democracia-em-xeque-e-palver-monitoram-termos-ligados-as-eleicoes-de-2022-a-pedi/) |
| 13/01–08/03/2023 | VT2 | Grupo "Audiências de Custódia", 1.398 certidões GestBio, Dia da Mulher | [1877](/posts/2023-01-13-kusahara-cria-grupo-audiencias-de-custodia-e-monta-sistema-de-1398-certidoes-usando-gestbi/)–[1880](/posts/2023-01-19-caso-ana-priscila-silva-de-azevedo-prisao-preventiva-determinada-por-moraes-antes-de-qualq/) |
| 20/04–05/12/2023 | VT5 | PET 11228 (Dino); extração de 2.119 CPFs e ofício-circular nacional | [1874](/posts/2023-12-05-gabinete-de-moraes-ordena-extracao-de-2119-cpfs-de-processos-do-8-de-janeiro-e-determina-v/), [1875](/posts/2023-04-20-cpf-de-flavio-dino-entao-ministro-da-justica-extraido-para-a-varredura-via-pet-11228-sigil/) |
| Ago/2024 | VT1 | Folha publica as primeiras mensagens (Greenwald/Serapião) | [timeline Folha](/posts/vaza-toga-folha-publica-mensagens-internas-tse-stf/) |
| 15/08/2025 | VT1 | Série ganha escala; gabinete paralelo nomeado | [1262](/posts/vaza-toga-expoe-gabinete-paralelo-de-alexandre-de-moraes/) |
| 02/09/2025 | VT1 | Tagliaferro depõe no Senado | [1303](/posts/eduardo-tagliaferro-depoe-no-senado-sobre-operacoes-paralelas-do-gabinete-de-moraes/) |
| 27/03/2026 | VT1 | Moraes anula audiência de instrução (nulidade absoluta) | [T-261](/posts/2026-08-20-t-261-vaza-toga-desdobramentos-tagliaferro/) |

## Mapa dos capítulos temáticos

| ID | Capítulo | Origem jornalística | Núcleo main |
| --- | --- | --- | --- |
| [T-256](/posts/2026-08-20-t-256-vaza-toga-2-certidoes-positivas/) | VT2 — Certidões positivas | A Investigação / Civilization Works | 1877–1882 |
| [T-257](/posts/2026-08-20-t-257-vaza-toga-3-cacando-jornalistas/) | VT3 — Caçando jornalistas | Revista Oeste (Edilson Salgueiro, Rachel Díaz, Carlo Cauti) | 1883–1888 |
| [T-258](/posts/2026-08-20-t-258-vaza-toga-4-fabricacao-de-provas/) | VT4 — Fabricação de provas | A Investigação / Public | 1869–1873 |
| [T-259](/posts/2026-08-20-t-259-vaza-toga-5-purga-institucional/) | VT5 — Purga institucional | A Investigação / Public | 1874–1876 |
| [T-260](/posts/2026-08-20-t-260-vaza-toga-padrao-salomao/) | Padrão Salomão | transversal | CNJ em VT4 e VT5 |
| [T-261](/posts/2026-08-20-t-261-vaza-toga-desdobramentos-tagliaferro/) | Caso Tagliaferro | Folha + desdobramentos | 1303, 1320, 1405, 1409, 1882 |
| [T-262](/posts/2026-08-20-t-262-vaza-toga-padroes-p10b/) | Padrões + P10-B | transversal | Palver, GestBio, DX |

T-207 permanece como ponte histórica do INQ 4781 (categoria estudos). Este T-255 é o índice de leitura da série consolidada após os capítulos 2–5.

## Padrões recorrentes

**P02** — a fonte que revela o mecanismo vira alvo do mesmo mecanismo. **P03** — centralização de detenção, prova e punição num único gabinete. **P04** — "desinformação" como categoria expansiva. **P10** — GestBio, Palver e Instituto Democracia em Xeque como infraestrutura reutilizável (proposta **P10-B** em T-262).

## Fontes

Folha de S.Paulo · A Investigação · Civilization Works · Public · Revista Oeste · Gazeta do Povo · depoimento ao Senado (02/09/2025)

*Dossiê T-255 · hub [/vazatoga/](/vazatoga/) · CC0 · lawfare-timeline*
''',
    )

    write_post(
        256,
        "vaza-toga-2-certidoes-positivas",
        "T-256 · Vaza Toga 2 — Certidões positivas (GestBio / Dia da Mulher)",
        "Como um documento nunca mostrado à defesa, nunca juntado aos autos, decidiu quem saía da prisão depois do 8 de Janeiro — usando o banco biométrico do eleitorado.",
        ["vazatoga", "certidoes", "gestbio", "8-de-janeiro", "p03", "p10", "ev-confirmed"],
        r'''
# T-256 · Vaza Toga 2 — Certidões positivas

**ID:** T-256 | **Main:** 1877–1882 | **HTML:** [vt2-certidoes-positivas.html](/vazatoga/vt2-certidoes-positivas.html)

Jornalistas: David Ágape e Eli Vieira, em parceria com Michael Shellenberger (Civilization Works).

## O mecanismo

Em 13/01/2023, às 14h12 — cinco dias após os atos —, Cristina Yukiko Kusahara criou o grupo de WhatsApp "Audiências de Custódia". Primeira mensagem de serviço: *Temos 1.200 pessoas custodiadas […] Não podemos nos dar ao luxo de ficar filosofando […] É prioridade do Ministro.* Dois dias antes, Alexandre de Moraes já havia centralizado em suas mãos toda decisão de detenção: juízes de primeira instância só checavam a legalidade formal, sem poder de soltura.

As "certidões" cruzavam nomes de detidos com o **GestBio** — banco biométrico do TSE — e com histórico em redes sociais. Qualquer conteúdo crítico ao STF ou ao PT podia gerar rótulo "positivo". Nunca compartilhadas com a defesa. Nunca juntadas aos autos.

> "A PGR pediu LP para eles, mas o Min não quer soltar sem antes a gente ver nas redes se tem alguma coisa."
>
> — Cristina Kusahara, 13/02/2023, sobre um lote de 20 casos em que a própria PGR já recomendara soltura

## Escala (13–17/01/2023)

| Momento | Certidões |
| --- | --- |
| 13/01 (noite) | ~200 |
| 14/01 (fim do dia) | 405 |
| 16/01 (manhã) | 853 / 1.398 |
| 16/01 (noite) | 1.225 |
| 17/01 (final) | **1.398** |

Tagliaferro registrou que "muitos perfis foram excluídos ou removeram um período de publicação": certidão negativa podia refletir só a capacidade de apagar histórico.

## O "show do Dia da Mulher"

Em 08/03/2023 o STF anunciou 149 solturas. No mesmo dia, às 12h51, Tagliaferro enviou 17 nomes com PDF — mulheres que **não** entrariam na soltura celebrada. O tribunal nunca publicou a lista oficial das 149 nem os critérios.

## Dois casos, duas lições

**Vildete da Silva Guardia, 74 anos** — certidão "positiva" às 16h53 de 13/01; às 16h56 corrigida ("era outra pessoa"). Erro de 3 minutos. Permaneceu presa mais 21 dias. Condenada a 11 anos e 11 meses. [1879](/posts/2023-01-13-caso-vildete-da-silva-guardia-erro-de-identidade-em-certidao-corrigido-em-3-minutos-mas-pr/)

**Ana Priscila Silva de Azevedo** — contraexemplo: em 19/01 Airton Vieira registra que ela "já está presa por preventiva do Ministro" *antes* de qualquer certidão positiva. A certidão veio depois. Impede a generalização de que toda prisão mantida se explica pela certidão. [1880](/posts/2023-01-19-caso-ana-priscila-silva-de-azevedo-prisao-preventiva-determinada-por-moraes-antes-de-qualq/)

## Vácuo de responsabilização

Novo (CNJ/Barroso), CPI proposta por Esperidião Amin, impeachment de Marcel Van Hattem, ocupação da mesa do Senado, representação no CNJ contra Airton Vieira e Marco Vargas: nenhuma via prosperou. O CNJ arquivou sob o argumento de que a conduta "remetia ao próprio ministro" — e o CNJ não tem jurisdição sobre ministro do STF. [1881](/posts/2025-08-01-todas-as-tentativas-de-responsabilizacao-institucional-contra-o-sistema-de-certidoes-fraca/)

## Padrões

- **P03** — centralização de toda decisão de detenção numa pessoa
- **P04** — gesto público (Dia da Mulher) coexistindo com triagem oculta
- **P06** — cinco vias de responsabilização, nenhuma prospera
- **P10** — GestBio, criado para fins eleitorais, redirecionado à triagem penal

## Âncoras

- [1877 · Kusahara cria o grupo](/posts/2023-01-13-kusahara-cria-grupo-audiencias-de-custodia-e-monta-sistema-de-1398-certidoes-usando-gestbi/)
- [1878 · Dia da Mulher](/posts/2023-03-08-show-do-dia-da-mulher-moraes-anuncia-soltura-de-149-presas-em-08032023-enquanto-gabinete-f/)

*T-256 · Vaza Toga 2/5 · CC0*
''',
    )

    write_post(
        257,
        "vaza-toga-3-cacando-jornalistas",
        "T-257 · Vaza Toga 3 — Caçando jornalistas (A fraude exposta)",
        "Revista Oeste: o gabinete paralelo deixa de mirar só manifestantes do 8 de Janeiro e passa a mirar colunistas, caminhoneiros e deputadas eleitas. Frase-símbolo: «use sua criatividade».",
        ["vazatoga", "censura", "liberdade de expressão", "p02", "p04", "ev-confirmed"],
        r'''
# T-257 · Vaza Toga 3 — Caçando jornalistas

**ID:** T-257 | **Main:** 1883–1888 | **HTML:** [vt3-cacando-jornalistas.html](/vazatoga/vt3-cacando-jornalistas.html)

Origem: Revista Oeste, "A fraude exposta" (Ed. 285) — Edilson Salgueiro, Rachel Díaz, Carlo Cauti.

## A imprensa como alvo direto

Em 22/11/2022 Airton Vieira compartilhou vídeo de Rodrigo Constantino (Gazeta do Povo) criticando o TSE e determinou bloqueio com multa. Tagliaferro pediu orientação sobre como *justificar* o relatório — a ordem veio antes da justificativa técnica. [1883](/posts/2022-11-22-gabinete-paralelo-ordena-bloqueio-dos-colunistas-rodrigo-constantino-e-guilherme-fiuza-por/)

Em 27/12 o mesmo grupo discutiu Guilherme Fiuza. Tagliaferro enviou relatório ("esse não precisou de muito para se comprometer"); Vargas classificou os posts como "golpistas"; a conclusão foi "vamos mandar bala". Bloqueios executados em 30/12/2022 (Constantino) e 02/01/2023 (Fiuza) no INQ 4.781/DF.

Contra a rede Gettr, o alvo era Allan dos Santos, então nos EUA. Quando Tagliaferro perguntou o que reportar sem conteúdo incriminador, recebeu a instrução que virou símbolo do método:

> "Use sua criatividade."
>
> — Airton Vieira [1885](/posts/2022-12-01-gabinete-paralelo-avanca-contra-o-gettr-para-calar-allan-dos-santos-frase-use-sua-criativi/)

Carla Zambelli foi monitorada antes da diplomação; o bloqueio de conta **não está confirmado** nas fontes disponíveis (`ev-contested`). [1886](/posts/2022-12-01-gabinete-paralelo-monitora-carla-zambelli-e-discute-bloqueio-de-conta-antes-de-sua-diploma/)

## Caminhoneiros

Entre 01 e 08/11/2022 o gabinete pediu ao tenente-coronel José Luiz Santos Silva (PM-BA) identificação de placas e mapeamento de "financiadores". Grupos de Telegram caíram em menos de 10 minutos — Tagliaferro confirmou: "Cumpridos!" Não há registro público de base legal para essa solicitação a oficial de PM estadual por assessores do TSE. [1884](/posts/2022-11-01-gabinete-paralelo-aciona-tenente-coronel-da-pm-ba-para-identificar-e-multar-caminhoneiros-/)

## Infraestrutura privada

**Instituto Democracia em Xeque** coordenou com a AEED termos de busca ("urna eletrônica", "voto impresso") e celebrou a vitória de Lula em 30/10/2022 como "vitória contra a desinformação". **Palver** forneceu volume de menções em grupos; hoje opera comercialmente para Folha, Lupa e CNN Brasil — a mesma ferramenta, sem transparência em 2022. [1887](/posts/2022-10-30-instituto-democracia-em-xeque-e-palver-monitoram-termos-ligados-as-eleicoes-de-2022-a-pedi/)

A Revista Oeste relata mais de um ano sem receita publicitária no YouTube; a causalidade com a cobertura do STF **não está documentada** — só o fato da desmonetização.

## Por que saiu em 2025

Em 28/08/2025 Tagliaferro relatou que um veículo internacional vinha adiando a publicação. A identificação do veículo (comentada como CNN) **não vem de fonte primária** — `ev-alleged`. [1888](/posts/2025-08-28-tagliaferro-relata-publicamente-que-veiculo-internacional-postergou-por-meses-a-publicacao/)

## Padrões

- **P02** — crítica vira gatilho de investigação
- **P04** — "use sua criatividade" como manual para gerar enquadramento
- **P10-B** (candidato) — Palver e Democracia em Xeque: vigilância política terceirizada

*T-257 · Vaza Toga 3/5 · CC0*
''',
    )

    write_post(
        258,
        "vaza-toga-4-fabricacao-de-provas",
        "T-258 · Vaza Toga 4 — Fabricação de provas (empresários / relatório Shor)",
        "A operação de 23/08/2022 contra empresários bolsonaristas não teve prova real por trás: teve prova fabricada depois, com metadados que a perícia forense desmontou.",
        ["vazatoga", "empresarios-bolsonaristas", "p01", "p03", "p04", "ev-confirmed"],
        r'''
# T-258 · Vaza Toga 4 — Fabricação de provas

**ID:** T-258 | **Main:** 1869–1873 | **HTML:** [vt4-fabricacao-de-provas.html](/vazatoga/vt4-fabricacao-de-provas.html)

Jornalistas: David Ágape e Eli Vieira, com Public (Michael Shellenberger) e Civilization Works.

## A operação

Em 23/08/2022 — dez dias antes do primeiro debate presidencial — a PF cumpriu mandados em cinco estados contra Luciano Hang, Meyer Nigri (Tecnisa), José Koury, Nelson Piquet, Flávio Rocha e Afrânio Barreira: bloqueio de contas e perfis. A única base fática pública era uma reportagem do Metrópoles (17/08/2022) sobre o grupo "Empresários & Política". [1869](/posts/2022-08-23-moraes-ordena-busca-e-apreensao-contra-empresarios-bolsonaristas-em-5-estados-com-base-em-/)

## A cadeia de fabricação

Airton Vieira (ordena) → Tagliaferro (executa) → Letícia Sallorenzo (intermedeia) → Lucas Mesquita (infiltra) → delegado Shor (assina).

Em 27/08/2022, à 1h da manhã — quatro dias *depois* da operação —, Sallorenzo enviou prints e exportação integral do grupo, obtidos por infiltrado identificado como o jornalista Lucas Mesquita. Objetivo declarado: "sossegar o amigo" (Moraes). Sem cadeia de custódia formal.

O relatório que sustentava a operação está datado de **19/08/2022** — antes da própria busca (23/08). Perícia independente contratada por A Investigação (revelada em 08/10/2025) apurou metadados de criação em **29/08/2022**, o dia em que Moraes levantou o sigilo. [1870](/posts/2022-08-27-fabricacao-retroativa-de-provas-infiltrado-colaboradora-informal-e-delegado-produzem-relat/)

> "Sossegar o amigo."

Áudio posterior de Sallorenzo admitindo ter denunciado os empresários: [1321](/posts/audio-revela-colaboradora-informal-do-tse-admitindo-ter-denunciado-empresarios/).

## Efeito colateral: juiz Melek

O mesmo fluxo levantou dados sobre Marlos Melek, juiz do Trabalho no grupo. Um ano depois o CNJ o afastou cautelarmente por 9 meses — por reagir com emoji. O relator Luis Felipe Salomão registrou que a conduta era "de menor importância". Em junho de 2024, censura (sanção mais branda) e retorno. [1871](/posts/2023-09-01-cnj-afasta-juiz-marlos-melek-por-participar-do-mesmo-grupo-de-whatsapp-alvo-da-operacao-de/)

## Desfecho seletivo

| Alvo | Desfecho |
| --- | --- |
| 6 dos 8 empresários | Arquivados ~1 ano depois, sem provas reconhecidas pelo relator |
| Meyer Nigri | Mantido |
| Luciano Hang | Redes bloqueadas por mais de 2 anos; liberadas em set/2024 |
| Queixa de Sallorenzo contra jornalistas da série | Arquivada por Moraes em jan/2026 por falta de indícios [1873](/posts/2026-01-26-moraes-arquiva-acao-criminal-de-leticia-sallorenzo-contra-jornalistas-da-vaza-toga-por-fal/) |

O mesmo relator que concentra o chokepoint arquivou a ação contra os jornalistas que revelaram o caso — contraexemplo obrigatório. [1872](/posts/2023-06-01-desfecho-seletivo-do-caso-moraes-arquiva-a-maioria-apos-posse-de-lula-mantem-hang-e-nigri-/)

## Padrões

- **P01** — prova formal produzida a posteriori para preencher decisão já tomada
- **P03** — operação sem lastro investigativo prévio documentado
- **P10** — mesma arquitetura informal reaplicada de alvos do 8/1 para empresários

*T-258 · Vaza Toga 4/5 · CC0*
''',
    )

    write_post(
        259,
        "vaza-toga-5-purga-institucional",
        "T-259 · Vaza Toga 5 — Purga institucional (2.119 CPFs / PET 11228)",
        "A vigilância informal se formaliza: 2.119 CPFs extraídos e cruzados contra o funcionalismo do Judiciário — inclusive um futuro colega de banca no STF.",
        ["vazatoga", "cnj", "stf", "8-de-janeiro", "p02", "p03", "p10", "ev-confirmed"],
        r'''
# T-259 · Vaza Toga 5 — Purga institucional

**ID:** T-259 | **Main:** 1874–1876 | **HTML:** [vt5-purga-institucional.html](/vazatoga/vt5-purga-institucional.html)

Jornalistas: David Ágape e Eli Vieira, com Public (Michael Shellenberger). Revelado em agosto/2026.

## A devassa

O pedido original do CNJ (corregedor Luis Felipe Salomão) era limitado: informações sobre integrantes do Judiciário nos processos do 8 de Janeiro. O gabinete de Moraes ampliou unilateralmente.

Em 05/12/2023 ordenou extração de todos os CPFs de ações penais, inquéritos e 124 petições: **2.119 CPFs** distintos — 1.355 ocorrências como "investigado", 2.452 como "requerido", 12 como "réu". **711** pessoas apareciam exclusivamente como "requeridas", sem status de investigado ou réu. [1874](/posts/2023-12-05-gabinete-de-moraes-ordena-extracao-de-2119-cpfs-de-processos-do-8-de-janeiro-e-determina-v/)

Em 15/12/2023 ofício-circular assinado "de ordem" por Cristina Kusahara foi a todos os tribunais do país, prazo de 15 dias, inclusive para resultado negativo. A lista incluía nomes de três inquéritos sigilosos (4930, 4939, 4948).

## O caso Dino

Flávio Dino, então ministro da Justiça, entra na lista via PET 11228 sigilosa (20/04/2023, notícia-crime por omissão diante do 8 de Janeiro).

| Data | Evento |
| --- | --- |
| 27/11/2023 | Lula indica Dino ao STF |
| 05/12/2023 | Gabinete ordena extração — inclui o CPF de Dino |
| 13/12/2023 | Senado aprova a indicação |
| 15/12/2023 | Lista distribuída aos tribunais |
| 22/02/2024 | Dino toma posse — colega de Moraes no STF |

A PET 11228 não teve desfecho público até a reportagem — nem recebimento, nem arquivamento, nem conversão em inquérito. Petição similar (PET 10829) foi arquivada em curto prazo com decisão pública. [1875](/posts/2023-04-20-cpf-de-flavio-dino-entao-ministro-da-justica-extraido-para-a-varredura-via-pet-11228-sigil/)

## A réplica no Exército

Em março/2025 a CMRI julgou recurso LAI sobre militares punidos pelo Comando Militar do Planalto. O Comando confirmou 4 inquéritos e 4 PADs (2 com punição) e recusou os nomes citando sigilo de inquérito sob relatoria de Moraes. A mesma opacidade se propagou do Judiciário às Forças Armadas. [1876](/posts/2025-03-01-sigilo-do-stf-vira-barreira-institucional-exercito-nega-nomes-de-militares-punidos-pelo-8-/)

## Padrões

- **P02** — futuro ministro do STF sob checagem funcional sem desfecho público
- **P03** — sigilo de um processo vira controle de informação em outra esfera
- **P10** — um mecanismo de sigilo a montante blinda decisões a jusante

*T-259 · Vaza Toga 5/5 · CC0*
''',
    )

    write_post(
        260,
        "vaza-toga-padrao-salomao",
        "T-260 · O padrão Salomão — seletividade da Corregedoria nos cinco capítulos",
        "Luis Felipe Salomão aparece na série como autor do pedido restrito que o gabinete de Moraes ampliou (VT5) e como relator que classificou emoji de Melek como «de menor importância» (VT4).",
        ["vazatoga", "cnj", "estudo", "p03", "p06", "ev-confirmed"],
        r'''
# T-260 · O padrão Salomão

**ID:** T-260 | **Transversal:** VT4 (Melek) + VT5 (devassa de CPFs)

Luis Felipe Salomão, então Corregedor Nacional de Justiça, não é o operador do gabinete paralelo. O que a série documenta é **seletividade de escopo** na Corregedoria quando o alvo está perto do STF e **ampliação unilateral** quando o pedido sai do gabinete de Moraes.

## Dois atos, dois pesos

Em Vaza Toga 4, o CNJ afastou o juiz Marlos Melek por 9 meses por reagir com emoji num grupo de WhatsApp. O próprio Salomão registrou nos autos que a conduta era "de menor importância". A cautelar durou quase um ano; a sanção final foi censura. [1871](/posts/2023-09-01-cnj-afasta-juiz-marlos-melek-por-participar-do-mesmo-grupo-de-whatsapp-alvo-da-operacao-de/)

Em Vaza Toga 5, o pedido da Corregedoria era só informações sobre *integrantes do Judiciário* nos autos do 8 de Janeiro. O gabinete de Moraes transformou isso em extração nacional de 2.119 CPFs, ofício a todos os tribunais e inclusão de pessoas que jamais foram rés. [1874](/posts/2023-12-05-gabinete-de-moraes-ordena-extracao-de-2119-cpfs-de-processos-do-8-de-janeiro-e-determina-v/)

O CNJ não reverteu a ampliação. Quando a cadeia de comando das certidões apontou para o próprio ministro (Airton Vieira / Marco Vargas), o CNJ arquivou por incompetência. [1881](/posts/2025-08-01-todas-as-tentativas-de-responsabilizacao-institucional-contra-o-sistema-de-certidoes-fraca/)

## Leitura estrutural

Não é necessário atribuir dolo pessoal a Salomão para registrar o padrão: a Corregedoria é **rigorosa na periferia do sistema** (juiz do Trabalho num grupo de empresários) e **opaca no centro** (ministro do STF cujo gabinete executa a varredura). P03 (chokepoint) e P06 (exaustão institucional) descrevem o desenho, não a biografia.

Lacuna: não há, nas fontes da série, decisão da Corregedoria que confronte a extração de CPFs de 711 pessoas sem status de investigado. Essa ausência é o dado.

## Conexões

- [T-258 · Fabricação de provas](/posts/2026-08-20-t-258-vaza-toga-4-fabricacao-de-provas/)
- [T-259 · Purga institucional](/posts/2026-08-20-t-259-vaza-toga-5-purga-institucional/)
- [T-256 · Certidões / CNJ](/posts/2026-08-20-t-256-vaza-toga-2-certidoes-positivas/)

*T-260 · CC0*
''',
    )

    write_post(
        261,
        "vaza-toga-desdobramentos-tagliaferro",
        "T-261 · Desdobramentos Tagliaferro — da revelação à nulidade de 27/03/2026",
        "Cronologia processual do ex-chefe da AEED/TSE: Senado, réu na 1ª Turma, citação por edital, audiência sem intimação, nulidade absoluta reconhecida por Moraes e destituição dos advogados.",
        ["vazatoga", "tagliaferro", "stf", "p01", "p02", "p03", "ev-confirmed"],
        r'''
# T-261 · Desdobramentos do caso Tagliaferro

**ID:** T-261 | **HTML origem:** [vt1-censura-criticos.html](/vazatoga/vt1-censura-criticos.html)

Eduardo Tagliaferro é a fonte primária documental das cinco fases. Este capítulo registra o que o Estado fez com a fonte — inclusive o momento em que o próprio relator anulou a instrução.

## Linha do tempo

| Data | Evento | Corpus |
| --- | --- | --- |
| Ago/2024 | Folha publica mensagens do celular de Tagliaferro | [Folha](/posts/vaza-toga-folha-publica-mensagens-internas-tse-stf/) |
| 02/09/2025 | Depõe no Senado; confirma legitimidade do material | [1303](/posts/eduardo-tagliaferro-depoe-no-senado-sobre-operacoes-paralelas-do-gabinete-de-moraes/) |
| 02/09/2025 | Senado envia relatório a EUA e organismos internacionais | [1304](/posts/senado-decide-enviar-relatorio-sobre-vaza-toga-aos-eua-e-organismos-internacionais/) |
| 25/10/2025 | Queixa-crime de Sallorenzo contra Ágape e Vieira | [1312](/posts/jornalistas-david-agape-e-eli-vieira-sao-alvo-de-queixa-crime-no-stf-por-revelacoes-da-vaza-toga/) |
| 09–13/11/2025 | 1ª Turma torna Tagliaferro réu por 4 a 0 | [1320](/posts/stf-forma-maioria-para-tornar-eduardo-tagliaferro-reu-por-revelacoes-da-vaza-toga/), [1ª Turma](/posts/1-turma-do-stf-torna-tagliaferro-reu-por-4-a-0/) |
| 01/12/2025 – 02/03/2026 | Citação por edital com paradeiro "incerto" apesar de Senado e Itália | [1882](/posts/2026-03-02-tagliaferro-citado-por-edital-com-paradeiro-incerto-apesar-de-comparecimentos-publicos-aud/), [edital 01/12](/posts/moraes-determina-citacao-por-edital-alegando-paradeiro-desconhecido-contradicao-com-pedido-de-extradicao-anterior/) |
| 17/03/2026 | Audiência de instrução sem intimação regular da defesa | [audiência](/posts/audiencia-de-instrucao-realizada-sem-intimacao-regular-do-reu-testemunhos-colhidos-sem-contraditorio/) |
| **27/03/2026** | **Moraes reconhece nulidade absoluta e anula os depoimentos** | [nulidade](/posts/moraes-reconhece-nulidade-absoluta-da-audiencia-anula-todos-os-depoimentos-colhidos/) |
| 02–13/04/2026 | Defesa representa à OAB; Moraes destitui advogados e nomeia DPU | [1405](/posts/defesa-protocola-representacao-a-oab-denunciando-acusacao-de-abandono-de-causa/), [1409](/posts/moraes-destitui-advogados-constituidos-e-nomeia-defensoria-publica-sub-padrao-substituicao-compulsoria-de-defesa-tecnica/) |

A citação por edital de 01/12/2025 e o registro [1882](/posts/2026-03-02-tagliaferro-citado-por-edital-com-paradeiro-incerto-apesar-de-comparecimentos-publicos-aud/) descrevem o mesmo fato em datas diferentes (determinação vs. cumprimento). Não são dois eventos independentes.

## O contraexemplo de 27/03/2026

O relator anulou a instrução colhida sem contraditório. Registrado com o mesmo peso dos abusos: o processo também se corrigiu neste ponto. Não há, nas fontes disponíveis, decisão pública de mérito da ação penal. A cronologia mostra oscilação, não desfecho.

## Padrões

- **P02** — denunciante vira réu no tribunal que denunciou
- **P01** — nulidade reconhecida depois da audiência irregular
- **P03** — juíza auxiliar do próprio gabinete preside a instrução contra a fonte

*T-261 · CC0*
''',
    )

    write_post(
        262,
        "vaza-toga-padroes-p10b",
        "T-262 · Padrões P01–P12 na Vaza Toga e proposta P10-B",
        "Cinco âncoras de infraestrutura compartilhada (Palver, GestBio, certidões, Democracia em Xeque, Sallorenzo) sustentam a proposta de P10-B: terceirização privada de vigilância política.",
        ["vazatoga", "estudo", "p10", "p01", "p02", "p03", "p04", "ev-inference"],
        r'''
# T-262 · Padrões da série e proposta P10-B

**ID:** T-262 | **Tipo:** análise estrutural (`ev-inference` na promoção de P10-B; âncoras em `ev-confirmed`)

## Padrões já formalizados, aplicados à série

| Padrão | Onde aparece |
| --- | --- |
| **P01** | Relatório Shor datado antes da operação que pretensamente fundamenta (VT4); nulidade da audiência Tagliaferro (VT1) |
| **P02** | Fonte vira réu; colunistas viram alvo; Dino na lista de CPFs |
| **P03** | Centralização de detenção (VT2); relator investiga a fonte (VT1); sigilo vira escudo no Exército (VT5) |
| **P04** | "Desinformação" elástica; "use sua criatividade"; Dia da Mulher vs. 17 excluídas |
| **P06** | Cinco vias de responsabilização das certidões, nenhuma prospera |
| **P10** | GestBio (eleitoral → penal); Palver e DX (monitoramento → produto comercial) |

## Cinco âncoras para P10-B

P10 descreve infraestrutura de serviço compartilhada. **P10-B** (proposta, não formalizada em METHODOLOGY.md) nomeia o recorte *privado*: empresas e institutos que entregam vigilância política ao gabinete e depois operam no mercado legítimo, sem que a fase 2022 tenha transparência equivalente.

1. **Palver** — volume de menções em grupos em 2022; hoje Folha, Lupa, CNN. [1887](/posts/2022-10-30-instituto-democracia-em-xeque-e-palver-monitoram-termos-ligados-as-eleicoes-de-2022-a-pedi/)
2. **GestBio** — biometria eleitoral cruzada com redes para certidão positiva. [1877](/posts/2023-01-13-kusahara-cria-grupo-audiencias-de-custodia-e-monta-sistema-de-1398-certidoes-usando-gestbi/)
3. **Certidões AEED** — documento extra-autos que decide soltura. [1877](/posts/2023-01-13-kusahara-cria-grupo-audiencias-de-custodia-e-monta-sistema-de-1398-certidoes-usando-gestbi/), [1878](/posts/2023-03-08-show-do-dia-da-mulher-moraes-anuncia-soltura-de-149-presas-em-08032023-enquanto-gabinete-f/)
4. **Instituto Democracia em Xeque** — termos de busca com a AEED; celebração eleitoral em 30/10/2022. [1887](/posts/2022-10-30-instituto-democracia-em-xeque-e-palver-monitoram-termos-ligados-as-eleicoes-de-2022-a-pedi/)
5. **Sallorenzo / firehosing** — colaboradora informal, infiltrado, entrega sem custódia ("sossegar o amigo"). [1870](/posts/2022-08-27-fabricacao-retroativa-de-provas-infiltrado-colaboradora-informal-e-delegado-produzem-relat/), [1888](/posts/2025-08-28-tagliaferro-relata-publicamente-que-veiculo-internacional-postergou-por-meses-a-publicacao/)

Cinco âncoras em capítulos distintos satisfazem o critério mínimo de promoção (3+). A formalização em METHODOLOGY.md permanece decisão editorial — este T-262 só documenta as âncoras já no corpus.

## O que ainda não está no corpus

Vínculos financeiros completos DX/Itaú/USAID (só parciais via 1887). Contraexemplo de quarentena ou controle que *tenha bloqueado* o uso de Palver/GestBio. Desfecho de mérito da ação penal contra Tagliaferro.

## Leitura

- [T-255 · Síntese](/posts/2026-08-20-t-255-vaza-toga-sintese-geral/)
- [T-222 · P10 promovido a padrão](/posts/2026-07-16-p10-promovido-a-padrao-autonomo-infraestrutura-de-servico-compartilhada-com-dois-nos-verif/)

*T-262 · CC0*
''',
    )


if __name__ == "__main__":
    main()
