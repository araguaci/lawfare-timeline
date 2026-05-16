---
title: "PALANTIR × SOBERANIA DIGITAL — Diagnóstico Crítico Brasil 2025–2026"
description: PALANTIR × SOBERANIA DIGITAL — Diagnóstico Crítico Brasil 2025–2026
date: 2026-05-04T12:00:00-03:00
image:
  path: "/assets/img/estudos/soberania_ameacada_hero.webp"
tags: ["brasa", "soberania"]
categories: estudos
mermaid: false
pin: false
---

- &nbsp;
{:toc .large-only}

O FNDE opera desde 2024 com software da **Palantir** (Foundry e AIP), articulado pelo **Serpro** sobre **AWS**, sem licitação específica para a empresa americana. O paradoxo é brutal: a autarquia que distribui recursos da educação nacional — com dados de **menores**, municípios e vulnerabilidade territorial — repousa numa camada jurídica sujeita ao **CLOUD Act** (2018), que permite ao governo dos EUA exigir dados de fornecedores americanos **onde quer que os servidores estejam**.

Este texto sintetiza o dossiê “Palantir × Soberania Digital” (atualizado maio/2026): vínculo histórico com a **CIA** via **In-Q-Tel**, encadeamento contratual, vetores de risco pontuados, encaixe em LGPD/ECA e comparativo internacional. A tese não é conspiratória: é **estrutural**. Quem define o risco não é só “quem opera o painel no Brasil”, mas **qual lei pode compelir o fornecedor**.

## Palantir e CIA — o vínculo não é anedótico

Logo após a fundação, a Palantir recebeu cerca de **US$ 2 milhões** do **In-Q-Tel**, braço de venture capital da CIA. Reportagens e documentação pública descrevem **co-desenvolvimento** do software com analistas de agências de inteligência durante anos — financiamento aliado a construção técnica, não a um cheque passivo.

Hoje a empresa atende uma fatia relevante da **comunidade de inteligência e defesa ocidental** (CIA, NSA, FBI, Pentágono e outros clientes públicos nos EUA e aliados). Em 2025, sob o governo Trump, circulam valores bilionários ligados a contratos federais, **Projeto Maven** (IA para drones) e iniciativas como **ImmigrationOS** (vigilância migratória). O CEO **Alex Karp** e a própria empresa publicaram alinhamento explícito com a “república tecnológica” americana. No outro lado do Atlântico, **divisões da DGSI** na França teriam **proibido internamente** o uso do software por risco estrutural de espionagem — sinal de que o debate não é “só político”, é de **arquitetura de dados**.

O **In-Q-Tel**, fundado em 1999 pela CIA, existe para fechar o fosso entre **Silicon Valley** e **segurança nacional**; em décadas apoiou centenas de empresas. Autodeclaração de independência não apaga o desenho institucional: **aprovação e missão** convergem para capacidades de coleta e alcance.

## O contrato FNDE — quatro camadas e um atalho de mercado

O encadeamento documentado no dossiê segue quatro níveis:

1. **Serpro** — estatal de TI que deveria ser vetor de soberança, mas figura como **intermediária**, inclusive com presença na **AWS**.
2. **Amazon Web Services / Marketplace** — infraestrutura estadunidense; a Palantir entra como **serviço adicional** no ecossistema, **sem licitação dedicada** à plataforma.
3. **Palantir Foundry + AIP** — em uso desde 2024; o Relatório de Gestão do FNDE (1º semestre de 2025) chegou a **confirmar** Foundry e AIP antes de sumir do site público, segundo o próprio painel.
4. **FNDE** — autarquia do **MEC**, repasses bilionários, dados de escolas e alunos cruzados com indicadores socioeconômicos e territoriais.

Em evento no FNDE, referência citada no dossiê: gerência de Cloud do Serpro teria declarado que o Serpro **viabiliza** o acesso do FNDE a ferramentas da AWS e da Palantir. Isso importa para **transparência** e para **rastreabilidade decisória**: quem assina o que, com qual base legal e qual concorrência.

## Defesa oficial e por que “servidor no Brasil” não fecha o caso

O FNDE e órgãos ligados costumam alegar **hospedagem no Brasil**, **operação por servidores** e **dados públicos ou publicáveis**. Cada ponto merece resposta:

- **CLOUD Act**: lei americana pode obrigar empresas dos EUA a entregar dados **independentemente da geolocalização física** do armazenamento. Precedentes e debates europeus já trataram esse tema como **incompatibilidade estrutural** com certos níveis de proteção — a Suíça, no argumento do dossiê, chegou a conclusão dura em auditoria militar.
- **“Só servidores brasileiros”**: sem **auditoria independente**, logs de acesso, inventário de tratamentos e limitação contratual verificável, a frase não substitui evidência.
- **Dados “públicos”**: **correlação** (educação + mobilidade + vulnerabilidade) produz **inferência sensível** sobre pessoas, inclusive crianças — LGPD e ECA não dispensam proteção só porque a fonte original parece aberta.

## Vetores de risco — soberania e licitação

**Soberania**

- **CLOUD Act / acesso extraterritorial** — severidade crítica (score indicativo 9,5/10 no painel).
- **Ausência de licitação específica** para Palantir, via Serpro–AWS — crítico (~9,0).
- **Lock-in** em plataforma proprietária — alto (~8,5).
- **Contradição com política de Nuvem de Governo / soberança digital** — alto (~8,0).
- **Dados estratégicos nacionais** (padrões territoriais, investimento educacional) — alto (~7,8).

**Dados e privacidade**

- **Menores e ECA** — crítico (~9,2).
- **LGPD art. 33** — transferência internacional e risco via exposição compulsória — crítico (~8,8).
- **Inferência sensível por cruzamento de bases** — alto (~8,0).
- **Ausência de RIPD publicado** (art. 38 LGPD) — alto (~7,5).
- **Remoção do relatório de gestão** que citava Palantir — indicício de opacidade; possível tensão com **LAI** — alto (~7,0).

**Infraestrutura**

- **Interrupção unilateral** de serviço por fornecedor estrangeiro — crítico (~8,5).
- **Código fechado** sem auditoria de backdoors — alto (~8,0).
- **Dupla dependência AWS + Palantir** sob o mesmo arcabouço jurídico EUA — alto (~7,5).
- **Sem plano de saída** documentado — alto (~7,0).

**Geopolítico**

- **Inteligência competitiva** a partir de malha educacional/territorial — crítico (~8,8).
- **Alinhamento declarado da empresa com agenda do governo americano** em contexto de tensão bilateral — crítico (~8,5).
- **Precedente para replicação** em outros órgãos — alto (~8,0).
- **Pressão diplomática** mediada por acesso a dados — alto (~7,8).

## Análise jurídica brasileira — LGPD, ECA, CF e licitações

**LGPD (Lei 13.709/2018)** — Dados de crianças e correlações socioeconômicas podem configurar **sensíveis**; falta de base legal clara e publicada é problema. **Art. 33**: não há “nível adequado” genérico para EUA no mesmo sentido europeu; o risco **Cloud Act** é argumento central. **Art. 38**: tratamento de alto risco pede **RIPD**; o dossiê afirma que **não há RIPD publicado** para este fluxo.

**ECA (Lei 8.069/1990)** — Proteção integral e intimidade: encaminhar fluxos de menores para ecossistema com **DNA de inteligência estrangeira** é colisão frontal com a doutrina de proteção, sob leitura defendida no painel.

**CF/88 e EC 115/2022** — Privacidade e proteção de dados como direitos fundamentais reforçam o campo normativo de exigência de **proporcionalidade e transparência**.

**LAI** — Tirar do ar documento que confirmava fornecedor sensível, após reportagem, merece **apuração** sobre transparência ativa.

**Lei 14.133/2021** — Contratação por “carona” em marketplace, sem discussão explícita de **risco soberano** para dados de menores e repasse federal, é convite a **controle do TCU** e revisão judicial.

> O Exército suíço, segundo o relatório citado no dossiê, tratou a Palantir como **estruturalmente incompatível** com soberania — não como risco operacional gerenciável com servidores locais. O argumento paralleliza com o Brasil: a questão é **lei aplicável ao fornecedor**, não só bandeira no datacenter.

## Precedentes internacionais — o Brasil fora do padrão de reação

| País | Reação resumida | Lição |
|------|-----------------|-------|
| Suíça | Auditorias formais; **rejeição** por incompatibilidade soberana | Auditoria independente é víavel; Brasil não fez equivalente público |
| França | Uso restrito/proibido em frentes da **DGSI** | Até aparelhos de espionagem aliados reconhecem o paradoxo Cloud Act |
| Alemanha | **Tribunal constitucional** limitou uso em polícia federal | Judiciário como freio |
| União Europeia | **GDPR × CLOUD Act**; debates pós-Schrems II | LGPD em sintonia parcial com lógica europeia de transfers |
| Brasil | Contrato ativo FNDE; relatório removido; **sem posicionamento formal** robusto da ANPD/TCU/CGU no recorte do painel | Lacuna institucional documentada até mai/2026 |

## Recomendações — transição em vez de negacionismo

**Imediato (0–30 dias)**

- Restaurar e publicar o **Relatório de Gestão** e a **cadeia documental** do contrato (escopo, bases, logs, subcontratos).
- Publicar **RIPD** e **bases legais** do art. 7º da LGPD por categoria, com foco em menores.
- Acionar formalmente a **ANPD** sobre transferência e tratamento de alto risco.

**Médio prazo (30–180 dias)**

- **Auditoria TCU/CGU** com metodologia inspirada na suíça (pedidos de informação, provas técnicas, governança de acessos).
- **Marco legislativo** para TI de fornecedores com vínculos documentados a inteligência estrangeira em bases sensíveis.
- **Alternativa soberana** (stack aberto, nuvem de governo, portabilidade).

**Longo prazo**

- **Estratégia nacional** de inventário de contratos sujeitos a lei estrangeira competidora com a LGPD e **Avaliação de Impacto à Soberania** para contratos grandes.
- **Diplomacia de dados** com EUA e fóruns multilaterais sobre limites extraterritoriais.

**Rescisão**

O painel lista argumentos fortes para rescisão (CLOUD Act, RIPD, menores, licitação, opacidade), mas também riscos operacionais de **lock-in**. A saída sugerida é **programada (~180 dias)** com documentação imediata, auditoria e plano de migração — não um “big bang” sem contingência.

## Veredicto

**Ameaça à soberania digital: confirmada** no sentido jurídico-institucional usado no dossiê. O vínculo Palantir–inteligência dos EUA é **documentado e persistente**. O FNDE processa camada sensível do Estado (educação, território, infância) via fornecedor **compelível** por lei americana. Alegação de servidores no Brasil **não resolve** o núcleo do problema. A ausência de RIPD, de licitação transparente para a plataforma e de auditoria pública **agrava** a exposição. Em perspectiva comparada, o Brasil aparece **atrasado** nas respostas institucionais que a Europa e a Suíça ensaiaram.

A analogia do próprio painel vale recortar: Estados Unidos não aceitariam espelho complacente de infraestrutura de dados sensíveis hospedada em empresa com DNA de **inteligência estrangeira** sem reação — o recíproco deveria orientar o padrão brasileiro de exigência.

## Fontes

- gov.br/fnde — notícia AIP Bootcamp (mar/2024)
- FNDE — Relatório de Gestão 1º sem 2025 (status: removido do site; citado no dossiê)
- Wikipedia — Palantir Technologies; In-Q-Tel
- CartaCapital — “Cavalo de Troia” (dez/2025)
- The Intercept — NSA e Palantir (2017)
- Brasil 247 — “Hipoteca do futuro” (dez/2025); “Manifesto Palantir” (abr/2026)
- Republik (Suíça) — auditoria Forças Armadas / Palantir (dez/2025)
- American Immigration Council — ImmigrationOS (ago/2025)
- Liberation News — vigilância Palantir (jun/2025)
- Fortune — In-Q-Tel (jul/2025)
- CNBC, CartaCapital, demais veículos citados no painel HTML

*Dossiê completo (interativo): [https://gosurf.site/soberania-ameacada](https://gosurf.site/soberania-ameacada)*
 