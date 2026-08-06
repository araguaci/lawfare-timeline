# LAWFARE Timeline: o arquivo que a manchete esquece

Um caso vira manchete por três dias e some. Um número de R$ 86 bilhões aparece uma vez e nunca é atualizado. Um habeas corpus monocrático parece detalhe técnico — até você ver o sexto, o sexagésimo, o seiscentos.

O [LAWFARE Timeline](https://lawfare-timeline.vercel.app/) existe para tornar **visível o padrão**. Não é blog de opinião. É um corpus documentado de erosão institucional no Brasil — decisões, operações, escândalos financeiros, crise diplomática, censura, penduricalhos — com fonte, data e selo de evidência em cada entrada.

Em agosto de 2026 o arquivo passa de **1.838 IDs** na linha do tempo principal, **T-250** no eixo temático, cerca de **2.000 posts** publicados e uma série inteira sobre soberania mineral (*O Dragão e a Onça*). Domínio público onde couber (CC0). Sem paywall de narrativa.

## O que o projeto é — e o que não é

**É:** documentação sistemática. Evento âncora precisa ser verificável, datável e relevante para um padrão institucional. Três casos independentes com o mesmo mecanismo viram padrão nomeado (P01–P12). Estudos cruzam entradas. Dossiês HTML abrem o mapa interativo.

**Não é:** partido, assessoria, “lado A versus lado B”. Manipulação de narrativa aparece documentada à esquerda e à direita — o código **P04b** existe exatamente para isso. Se um artigo aqui não tiver fonte clicável, desconfie dele também.

> O corpus não pede concordância. Pede rastreabilidade: data, ator, documento, padrão.

## Três camadas (como o site funciona)

**1. Linha do tempo** — eventos pontuais: decisão, prisão, liquidação bancária, sanção diplomática. Pastas por tema (`stf`, `bancos`, `crise-diplomatica`, `impunidade`…). Cada card pode carregar `id_corpus` sequencial.

**2. Estudos** — análises que respondem “por que isso se repete?”. Exemplos recentes: [T-250 · dois pesos, duas medidas](https://lawfare-timeline.vercel.app/posts/2026-08-05-dois-pesos-duas-medidas-erro-judiciario-indenizacao-assimetrica/), [T-249 · sorteio eletrônico e imparcialidade](https://lawfare-timeline.vercel.app/posts/2026-08-04-sorteio-correto-resultado-sensivel-quando-a-distribuicao-aleatoria-nao-resolve-o-conflito-/), [P11 expandido — loop de extração](https://lawfare-timeline.vercel.app/posts/p11-expandido-loop-extracao-perpetua-economia-politica-brasil/).

**3. Padrões sistêmicos** — só entram na matriz se o mecanismo se repetir. Em uma frase:

- **P01** — o processo cai por defeito formal, não porque o fato não aconteceu
- **P02** — quem denuncia vira réu; o investigado vira “vítima”
- **P03** — um ministro do STF, sozinho, destrava ou trava tudo
- **P04 / P04b** — a cobertura decide o que “aconteceu”, ou dilui o fato como “só um lado”
- **P05** — dinheiro público vira veículo do esquema que deveria fiscalizar
- **P06** — o caso envelhece até prescrever
- **P07** — a rede de proteção atravessa gerações e governos
- **P08** — crime organizado lava em escala via fintech/cripto
- **P09** — quem denuncia perde prestígio cultural
- **P10** — política e crime compartilham infraestrutura de serviço
- **P11** — juros, dívida e austeridade se realimentam sem coordenação explícita

Metodologia aberta: [METHODOLOGY.md](https://github.com/araguaci/lawfare-timeline/blob/main/METHODOLOGY.md).

## O que o arquivo cobre (amostra do mapa)

Não dá para resumir 2.000 posts. Dá para mostrar a amplitude:

**Justiça e lawfare** — liminar monocrática, HC seletivo, foro privilegiado, Vaza Toga, COAF × acumulação de funções, seletividade TSE.

**Dinheiro** — Banco Master, Vorcaro, Mare Liberum (R$ 86,6 bi em DIs irregulares), Americanas sem condenação equivalente ao estrago, penduricalhos acima do teto, P11 de custeio federal.

**Crime organizado** — designação FTO/SDGT de PCC e CV pelos EUA, OFAC, lavagem, drones no RJ, infiltrção institucional.

**Diplomacia** — crise Brasil–EUA 2025–2026, Magnitsky, vistos, Seção 301, rebaixamentos bilaterais.

**Soberania mineral** — série *[O Dragão e a Onça](https://lawfare-timeline.vercel.app/odragaoeaonca/)*: governadores como operadores reais de contratos com China, EUA, Japão e capital ocidental — Goiás, Pará, Amazonas, Minas, Bahia, SP, PR, RS, SC, RJ, Amapá.

**Assimetria cotidiana** — o dossiê de hoje: cidadão preso por erro do Estado ouve “risco normal”; magistradas erram o aeroporto e recebem indenização. [T-250](https://lawfare-timeline.vercel.app/posts/2026-08-05-dois-pesos-duas-medidas-erro-judiciario-indenizacao-assimetrica/).

## Cinco portas de entrada (se você tem quinze minutos)

1. **[Como ler o Lawfare Timeline](https://lawfare-timeline.vercel.app/posts/2026-07-21-como-ler-o-lawfare-timeline-guia-para-o-leitor-brasileiro/)** — guia sem jargão, por perfil de leitor
2. **[Vaza Toga — resumo executivo](https://lawfare-timeline.vercel.app/posts/resumo-executivo/)** — gabinete paralelo no WhatsApp
3. **[Anatomia da liminar monocrática](https://lawfare-timeline.vercel.app/posts/anatomia-liminar-monocratica-stf-poder-individual-sem-controle/)** — poder individual sem freio
4. **[T-1512 · Designação terrorista PCC/CV](https://lawfare-timeline.vercel.app/posts/designacao-terrorista-pcc-cv/)** — FTO/SDGT + [P04b na cobertura](https://lawfare-timeline.vercel.app/posts/imprensa-brasileira-enquadra-designacao-terrorista-pcc-cv-como-questao-de-soberania-p04b/)
5. **[O Dragão e a Onça](https://lawfare-timeline.vercel.app/odragaoeaonca/)** — soberania mineral estado a estado

Índice por categoria: [lawfare-timeline.vercel.app/categories/](https://lawfare-timeline.vercel.app/categories/)

## Como a evidência é marcada

Cada fato sério carrega selo. Não é decoração:

- `ev-confirmed` — duas ou mais fontes independentes
- `ev-contested` — fontes divergem sobre o fato central
- `ev-alleged` — alegação relevante, ainda sem confirmação cruzada
- `ev-inference` — leitura estrutural *separada* do fato bruto

Quando o texto choca, o primeiro gesto certo é abrir a fonte — não compartilhar o título.

## Por que isso importa agora

2026 não é ano “qualquer”. Há eleição, sanções internacionais ativas, STF no centro do debate público, facções designadas como terroristas no exterior, e um volume de decisões que a memória de feed não segura.

Arquivo sem método vira panfleto. Método sem arquivo vira paper que ninguém lê. O projeto tenta os dois: **volume rastreável + padrões nomeados**.

Se você investiga, litiga, cobre política ou só quer entender por que o mesmo filme se repete com elenco diferente — o site é ferramenta, não culto.

## Números de estado (ago/2026)

- Site: [lawfare-timeline.vercel.app](https://lawfare-timeline.vercel.app/)
- Main track: último ID **1838** · próximo **1839**
- Temático: até **T-250**
- Posts Jekyll: ~**2.000**
- Série Dragão e a Onça: hub + dossiês HTML + X Articles regionais
- Licença dos dossiês abertos: **CC0** onde indicado

## Fontes e repositório

- Site de produção: [https://lawfare-timeline.vercel.app/](https://lawfare-timeline.vercel.app/)
- GitHub: [araguaci/lawfare-timeline](https://github.com/araguaci/lawfare-timeline)
- Metodologia: [METHODOLOGY.md](https://github.com/araguaci/lawfare-timeline/blob/main/METHODOLOGY.md)
- Hub mineral: [odragaoeaonca](https://lawfare-timeline.vercel.app/odragaoeaonca/)
- Guia do leitor: [Como ler](https://lawfare-timeline.vercel.app/posts/2026-07-21-como-ler-o-lawfare-timeline-guia-para-o-leitor-brasileiro/)

*LAWFARE Timeline — na guerra silenciosa que destrói democracias. Arquivo, não manchete.*
