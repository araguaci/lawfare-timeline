---
id_corpus: "T-217"
thematic_track: true
title: "Seletividade Punitiva — TSE: Casos Isolados (Atualizado)"
description: "Dois casos documentados no corpus tocam o tema sem constituir estudo comparativo: (1) TSE pune 14 canais do YouTube por narrativas pro-voto impresso em 2021."
date: 2026-06-29T12:00:00-03:00
image:
  path: "/assets/solid/book-open.svg"
tags: ["estudo", "p04", "tse", "lawfare"]
categories: lawfare
mermaid: false
pin: false
permalink: /posts/2026-06-29-seletividade-punitiva-tse-casos-isolados/
source_data: "T-195-seletividade-punitiva-tse-lacuna.json"
---

# LAWFARE

**Lawfare** é o uso estratégico do sistema legal para fins políticos, sob aparência de legalidade e seletividade.

*4 min leitura · [Ver original](https://lawfare-timeline.vercel.app/posts/2026-06-29-seletividade-punitiva-tse-casos-isolados/)*

---

Este registro documenta uma lacuna metodológica real, não um achado: a tese de "seletividade punitiva institucional por facção política" — recorrente no debate público sobre o TSE e sobre órgãos de controle interno do Legislativo — não tem, até a data desta atualização, um estudo comparativo consolidado que a sustente como padrão sistêmico verificável.

Diferente da maioria das entradas do corpus, este registro não conclui um caso — ele declara, com transparência, o que falta para concluí-lo, e agora precisa exatamente **onde** essa falta pode ser preenchida.

## O que existe, de fato

Dois casos isolados tocam o tema, sem constituir comparação sistemática entre si:

**TSE × 14 canais do YouTube (2021)** — o TSE puniu 14 canais por veicular narrativas pró-voto impresso. O registro disponível é uma referência curta a uma matéria do Aos Fatos, sem dados de contraparte (não há, na mesma fonte, levantamento de canais favoráveis à posição oposta que tenham sido tratados de forma diferente).

**Conselho de Ética da Câmara — ocupação do plenário, 2016 vs. 2025/2026** — este é o caso com evidência mais forte de comparação direta: em maio de 2026, o Conselho suspendeu por 60 dias os mandatos de Van Hattem, Pollon e Zé Trovão por ocupação do plenário (05/08/2025), e o próprio registro do corpus contrasta esse episódio com a impunidade de uma ocupação similar promovida pela esquerda em 2016. **Importante**: este caso é do Conselho de Ética da Câmara, não do TSE — citá-lo como prova de seletividade do TSE seria erro de atribuição institucional.

## Atualização de 18/07/2026 — infraestrutura de dados localizada

Uma verificação adicional identificou que os insumos necessários **não são inexistentes** — são **infraestrutura pública já disponível, mas não extraída, cruzada nem testada estatisticamente**:

| Insumo necessário | Status anterior (29/06/2026) | Status atualizado (18/07/2026) |
|---|---|---|
| Base de dados TSE com tempo médio de tramitação de AIJE/AIRC | "não localizado em fonte pública" | **Localizado**: [Estatística Processual do TSE](https://www.tse.jus.br/transparencia-e-prestacao-de-contas/estatistica-processual) — consultas paramétricas 2007–2021 sobre a base SADP/PJe, "sem interferência humana" |
| Classificação de processos por partido/coligação do representado | "não localizado" | **Parcialmente localizável**: cruzamento manual necessário entre a Estatística Processual (não classifica por partido nativamente) e o [Repositório de Dados Eleitorais](https://dadosabertos.tse.jus.br/) (que tem candidato → partido → coligação) |
| API pública de metadados processuais de qualquer tribunal, incluindo Justiça Eleitoral | não mencionado | **Localizado**: [CNJ DataJud](https://www.cnj.jus.br/sistemas/datajud/) — API pública, metadados de processos de todos os tribunais brasileiros |
| Teste estatístico de diferença entre grupos | "não localizado" | Metodologicamente definível agora que os dois insumos anteriores têm fonte identificada — falta apenas a execução |

**O que isso muda, e o que não muda**: a classificação evidencial deste item **permanece `ev-alleged`** — nenhum dado foi de fato extraído, cruzado ou testado nesta atualização. O que mudou é que a lacuna deixou de ser "nenhuma fonte pública existe" e passou a ser "as fontes existem, a extração e o cruzamento não foram feitos". Essa é uma lacuna tratável, não estrutural — e por isso este registro agora se desdobra num projeto público próprio (ver abaixo) em vez de permanecer apenas como nota de metodologia.

## Origem deste registro

Este item nasceu de uma tentativa inicial de formalizar um "ID 180 — TSE seletividade punitiva" identificado em sync de sessão anterior. A verificação revelou que o ID 180 real do corpus trata de tema correlato mas distinto — seletividade em inelegibilidade e cassação (padrões P02/P03), já confirmado e publicado separadamente. Este registro (T-217) preserva especificamente a lacuna da tese "velocidade/rigor de julgamento por facção", que é diferente e permanece aberta.

## Padrões aplicáveis

**P04 — Arma midiática**: a repetição anedótica de uma tese sem dado estruturado é, em si, um padrão de circulação de narrativa que merece registro — não pela veracidade da tese, mas pela forma como ela se propaga sem verificação.

## Lacuna investigativa (campo central deste registro)

Falta, integralmente:
1. **Extração estruturada** do dataset de tramitação processual do TSE por partido/coligação (fonte identificada: Estatística Processual TSE + DataJud + Repositório de Dados Eleitorais — cruzamento não executado)
2. **Metodologia de comparação estatística** validada (teste a definir — ver projeto público abaixo)
3. **Levantamento sistemático** (não anedótico) de casos de ocupação de plenário no Conselho de Ética e seus desfechos ao longo do tempo, não apenas o par 2016/2025-2026 — nenhuma fonte consolidada localizada até esta atualização

## Conexões

`timeline-1483` (duplo padrão — Conselho de Ética) · `ID 180` (seletividade em inelegibilidade/cassação — tema correlato, já confirmado) · `alem-da-toga.html` · `paradoxo-constitucional.html` · **novo**: `tseletivometro` (projeto público de extração de dados — ver repositório)

---

Licença CC0 1.0 — domínio público. Parte do corpus lawfare-timeline. Esta entrada documenta uma lacuna, não uma conclusão — produção futura é bem-vinda caso surjam fontes primárias estruturadas.
