# Plano — Temática dedicada Vaza Toga
*lawfare-timeline · v2 — reformulado em 2026-08-20 a partir de `export-vazatoga.json`*

**Jornalistas investigativos da série:**
David Ágape e Eli Vieira (A Investigação, em parceria com Michael Shellenberger/Civilization Works e Public) — Vaza Toga 2, 4 e 5. Glenn Greenwald e Fábio Serapião (Folha de S.Paulo) — Vaza Toga 1, origem da série. Edilson Salgueiro, Rachel Díaz e Carlo Cauti (Revista Oeste) — Vaza Toga 3. Fonte primária dos documentos em todas as fases: Eduardo Tagliaferro, ex-chefe da AEED/TSE.

**Origem da série (portal de referência):** https://www.ainvestigacao.com/

**Hub publicado 20/08/2026:** [/vazatoga/](/vazatoga/) (padrão `/dragao-onca/`), capítulos **T-255–T-262** em `_posts/vazatoga/`, artefatos HTML em `vazatoga/vt1–vt5.html`. T-207 permanece ponte INQ 4781; T-255 é o índice de leitura da série consolidada.

---

## 1. Estado real do corpus (fonte: `export-vazatoga.json`, sincronizado por Araguaci)

Total: **42 entradas** rastreadas (`_posts/vazatoga/` + `lawfare.json`), cobrindo o período 2022-08-23 a 2026-05-29. IDs finais **não coincidem** com os que eu propus nos batches desta sessão — foram renumerados no merge para não colidir com 1865-1868 (ocupados por conteúdo de regulação de internet, fora da série). Mapa real:

| Capítulo | Nome | Origem | IDs main (núcleo) | Qtd. total no capítulo |
|---|---|---|---|---|
| 1 | Vaza Toga 1 — Folha/Greenwald e gabinete paralelo | Folha de S.Paulo / Greenwald / Serapião | 1262, 1299, 1303, 1304, 1312, 1316, 1320, 1322, 1405, 1409 + 4 sem ID confirmado | 16 |
| 2 | Vaza Toga 2 — Certidões GestBio e Dia da Mulher | A Investigação / Civilization Works | 1877-1882 | 10 (inclui 4 sínteses redundantes) |
| 3 | Vaza Toga 3 — A fraude exposta | Revista Oeste | 1883-1888 | 6 |
| 4 | Vaza Toga 4 — Empresários e fabricação de provas | A Investigação / Public / Civilization Works | 1869-1873 (+ 1321 desdobramento) | 6 |
| 5 | Vaza Toga 5 — Devassa de CPFs CNJ/STF | A Investigação / Public | 1874-1876 | 3 |
| índice | T-207 · Vaza Toga — Índice Corpus INQ 4781 | — | thematic | 1 |

**Os capítulos 2-5 estão, na prática, fechados** com o conteúdo produzido nesta sessão (batches de 20/08/2026), já renumerado e sincronizado. O capítulo 1 é o único com lacunas reais remanescentes.

## 2. Lacunas remanescentes identificadas no export

### 2.1 Vaza Toga 1 — núcleo original sem ID confirmado (prioridade alta)
Dois posts sobre a publicação original da Folha (01/08/2024) existem como rascunhos duplicados, **nenhum com `id_corpus` atribuído** — um está explicitamente marcado `duplicata_de` do outro. É a origem de toda a série e ainda não tem entrada canônica única no corpus principal. Precisa: (a) escolher a versão correta, (b) atribuir ID novo, (c) descartar a duplicata.

### 2.2 Desdobramentos do caso Tagliaferro sem ID confirmado (prioridade alta)
Quatro eventos processuais relevantes existem como rascunhos sem `id_corpus`:
- 13/11/2025 — 1ª Turma do STF torna Tagliaferro réu por 4 a 0 (complementa id_1320)
- 01/12/2025 — Moraes determina citação por edital alegando paradeiro desconhecido (mesmo fato já registrado como id_1882 nesta sessão — **possível duplicidade a checar**)
- 17/03/2026 — Audiência de instrução realizada sem intimação regular do réu, testemunhos colhidos
- 27/03/2026 — **Moraes reconhece nulidade absoluta e anula todos os depoimentos colhidos na audiência de 17/03** — desfecho que eu não tinha quando produzi id_1882/1888 nesta sessão; é atualização relevante e favorável ao devido processo, deve ser registrada com o mesmo rigor factual dado aos abusos.

### 2.3 Redundância em Vaza Toga 2 (prioridade baixa — limpeza, não conteúdo)
Quatro entradas de síntese (1265-1268: "Pontos Centrais", "Detalhamento", "Resumo Executivo", "Resumo Geral" — todas de 17/08/2025) parecem ser variações do mesmo resumo gerado em lote. Candidatas a consolidação em uma única entrada de síntese ou a arquivamento como rascunhos de trabalho, não entradas finais.

### 2.4 Ainda fora do corpus (gaps já sinalizados em sessões anteriores, confirmados persistentes)
- Rede DX/Itaú/USAID (Instituto Democracia em Xeque) — só parcialmente coberta via id_1887; a investigação completa de vínculos financeiros (Itaú, USAID) não foi aprofundada.
- P10-B (terceirização privada de vigilância política) — proposto, não formalizado. Já tem 5 âncoras disponíveis no corpus atual (Palver em id_1877/1887, GestBio em id_1877, certidões em id_1877/1878, rede DX em id_1887, Sallorenzo/firehosing mencionado em id_1877/1888). Decisão de formalização segue pendente, é editorial.
- 1865-1868 permanecem fora da série por decisão de escopo (regulação de internet) — confirmado, não é lacuna.

## 3. Índice temático já existente — reconciliar, não duplicar

**T-207 "Vaza Toga — Índice Corpus INQ 4781"** (publicado 29/05/2026, categoria `estudos`) já funciona como ponte/índice geral da série, antes mesmo da consolidação desta sessão. A proposta de hub temático (seção 4) não deve recriar esse papel — deve **estender T-207** ou **substituí-lo por uma nova versão consolidada**, já que ele foi escrito antes dos capítulos 2-5 existirem no formato atual. Decisão editorial: atualizar T-207 no lugar, ou aposentá-lo e abrir a série T-255+ como sucessora explícita, linkando de volta.

## 4. Proposta de hub temático — thematic track (T-255+)

Mantida a estrutura de capítulos da sessão anterior, ajustada à numeração real de IDs main confirmada no export:

- **T-255** — Síntese geral: cronologia 2022-2026 (Folha/Greenwald → Ágape/Vieira → Oeste), suplanta ou referencia T-207
- **T-256** — Vaza Toga 2: certidões (id_1877-1882) — GestBio, "Dia da Mulher", Vildete Guardia, Ana Priscila Azevedo
- **T-257** — Vaza Toga 3: A fraude exposta (id_1883-1888) — Constantino/Fiuza, PM-BA, Gettr/Allan, Zambelli, Palver/DX
- **T-258** — Vaza Toga 4: fabricação de provas (id_1869-1873) — Shor, Melek, Hang/Nigri
- **T-259** — Vaza Toga 5: devassa de CPFs (id_1874-1876) — CNJ/Salomão, PET 11228/Dino
- **T-260** — O padrão Salomão: seletividade da Corregedoria através de todos os 5 capítulos
- **T-261** — Os desdobramentos do caso Tagliaferro: da revelação à nulidade reconhecida (27/03/2026) — inclui o contraexemplo de correção processual, não só o abuso
- **T-262** — Síntese de padrões P01-P12 + proposta P10-B, com as 5 âncoras já disponíveis

## 5. Recomendação imediata

1. Resolver 2.1 e 2.2 primeiro — são lacunas de ID, não de apuração; rápidas de fechar e destravam a limpeza do capítulo 1.
2. Checar duplicidade entre "citação por edital" do export (01/12/2025) e id_1882/1888 desta sessão antes de qualquer novo merge.
3. Decidir sobre T-207 (seção 3) antes de abrir T-255 — evita dois índices concorrentes.
4. F2 do plano original (Palver/GestBio/rede DX a fundo) segue como próxima fronteira de apuração real, não de organização.

**SELVA** ou **me surpreenda** resolvem 2.1+2.2 nesta sessão, se preferir não esperar.
