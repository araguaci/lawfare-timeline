const fs = require('fs');
const path = require('path');
const inv = require('./_inventory-sem-fonte.json');

function clean(u) {
  if (!u) return null;
  return u
    .replace('/google/amp', '')
    .replace('/amp/', '/')
    .replace('folha.uol.com.br/amp/', 'folha.uol.com.br/')
    .replace('estadao.com.br/amp/', 'estadao.com.br/')
    .replace(/\/$/, '');
}

function patch(id, titulo, fontes, resumo, detalhada, extra = {}) {
  const f = [...new Set(fontes.map(clean).filter(Boolean))];
  return {
    id,
    titulo,
    fontes: f,
    descricao_resumo: resumo,
    descricao_detalhada: detalhada,
    evidence_status: f.length ? 'ev-confirmed' : 'ev-alleged',
    gravidade: extra.gravidade || 'alta',
    alerta_critico: !!extra.alerta_critico,
    ...(extra.notas ? { notas: extra.notas } : {}),
  };
}

const S = {
  faroeste: [
    'https://www.stj.jus.br/sites/portalp/Paginas/Comunicacao/Noticias/2025/15022025-Operacao-Faroeste-afastamento-de-desembargadora-e-juiza-do-TJBA-e-prorrogado-por-mais-um-ano.aspx',
    'https://www.mpf.mp.br/o-mpf/unidades/procuradoria-geral-da-republica-pgr/noticias/operacao-faroeste-stj-mantem-afastamento-de-juiza-e-desembargadora-do-tjba-investigadas',
    'https://pt.wikipedia.org/wiki/Opera%C3%A7%C3%A3o_Faroeste',
  ],
  min18: [
    'https://www.estadao.com.br/politica/o-que-se-sabe-operacao-18-minutos-investiga-suposta-venda-sentencas-juizes-nprp',
    'https://g1.globo.com/ma/maranhao/noticia/2026/04/01/magistrados-e-ex-assessor-ostentacao-quem-sao-os-investigados-por-venda-de-decisoes-no-tj-ma.ghtml',
  ],
  sisamnes: [
    'https://www.poder360.com.br/poder-justica/zanin-autoriza-pf-a-investigar-ministro-do-stj-por-venda-de-decisoes/',
    'https://g1.globo.com/politica/noticia/2026/05/27/pgr-ve-esquema-de-venda-de-sentencas-no-stj-e-denuncia-lobista-e-ex-servidores.ghtml',
    'https://www1.folha.uol.com.br/poder/2025/10/inquerito-sobre-venda-de-decisoes-divide-stj-e-mencoes-geram-queixas-a-pf-e-stf.shtml',
  ],
  ultima: [
    'https://g1.globo.com/ms/mato-grosso-do-sul/noticia/2026/04/17/aviao-carros-de-luxo-fazendas-e-milhoes-em-especie-como-era-esquema-de-venda-de-sentencas-no-tjms.ghtml',
    'https://jurinews.com.br/brasil/operacao-ultima-ratio-cnj-instaura-pads-contra-desembargadores-do-tj-ms-afastados-por-suspeita-de-venda-de-sentencas',
  ],
  witzel: [
    'https://www.stj.jus.br/sites/portalp/Paginas/Comunicacao/Noticias/2025/13032025-STJ-condena-desembargadores-do-TRT1-por-participacao-em-esquema-de-corrupcao.aspx',
    'https://www.cartacapital.com.br/justica/stj-condena-tres-desembargadores-do-trt-rj-por-corrupcao-na-gestao-de-witzel/',
  ],
  zelotes: [
    'https://g1.globo.com/politica/noticia/2016/02/entenda-operacao-zelotes.html',
    'https://pt.wikipedia.org/wiki/Opera%C3%A7%C3%A3o_Zelotes',
  ],
  anaconda: [
    'https://linhadotempo.mpf.mp.br/www/linha-do-tempo-prr3/2003-2013-operacao-anaconda',
    'https://www.migalhas.com.br/quentes/7756/operacao-anaconda',
  ],
  andre: [
    'https://www.cnnbrasil.com.br/nacional/sudeste/sp/fuga-de-andre-do-rap-completa-5-anos-hoje-relembre-o-caso/',
    'https://www.migalhas.com.br/quentes/336363/em-novo-julgamento--marco-aurelio-garante-liberdade-de-andre-do-rap',
  ],
  vazatoga: [
    'https://www.gazetadopovo.com.br/republica/vaza-toga-2-capitulo-mais-sombrio-autoritarismo-moraes/',
    'https://revistaoeste.com/politica/gabinete-paralelo-de-moraes-usurpou-funcoes-censurou-a-imprensa-e-violou-a-constituicao-afirmam-juristas/',
    'https://www12.senado.leg.br/radio/1/noticia/2025/09/02/comissao-ouve-ex-assessor-de-moraes-que-expos-conversas-que-ficaram-conhecidas-como-vaza-toga',
  ],
  vazaJato: [
    'https://theintercept.com/series/mensagens-lava-jato/',
    'https://pt.wikipedia.org/wiki/Vaza_Jato',
  ],
  hurricane: [
    'https://pt.wikipedia.org/wiki/Opera%C3%A7%C3%A3o_Hurricane',
    'https://g1.globo.com/Noticias/Politica/0,,MUL23707-5601,00.html',
  ],
  naufragio: [
    'https://www.conjur.com.br/2019-ago-14/stj-julgara-acao-penal-desembargadores-espirito-santo/',
    'https://www.stj.jus.br/sites/portalp/Paginas/Comunicacao/Noticias.aspx',
  ],
  cnjCoach: [
    'https://www.cartacapital.com.br/justica/cnj-suspende-redes-sociais-de-juiz-do-trf-2-acusado-de-atuar-como-coach-de-advogados/',
  ],
  ludmila: [
    'https://g1.globo.com/mg/minas-gerais/noticia/2023/05/25/orgao-especial-do-tjmg-afasta-juiza-ludmila-lins-grilo-por-dois-anos.ghtml',
  ],
  trtSp: [
    'https://pt.wikipedia.org/wiki/Esc%C3%A2ndalo_do_Tribunal_Regional_do_Trabalho_de_S%C3%A3o_Paulo',
  ],
  adc43: [
    'https://portal.stf.jus.br/processos/detalhe.asp?incidente=5415433',
    'https://www.conjur.com.br/2019-nov-07/stf-define-prisao-apos-esgotamento-todos-recursos/',
  ],
  hc82959: [
    'https://portal.stf.jus.br/processos/detalhe.asp?incidente=2191915',
  ],
  hc84078: [
    'https://portal.stf.jus.br/processos/detalhe.asp?incidente=2209034',
  ],
  estadao21: [
    'https://www.estadao.com.br/politica/ministros-do-stf-soltaram-ao-menos-21-reus-que-fugiram/',
  ],
};

const patches = [];

for (const [id, titulo] of [
  [1265, 'Pontos Centrais Vazatoga2 - Crise Institucional e Judicial'],
  [1266, 'Detalhamento Vazatoga2 - Crise Institucional e Judicial'],
  [1267, 'Vazatoga2 - Resumo Executivo Crise Institucional e Judicial'],
  [1268, 'Vazatoga2 - Resumo Geral Crise Institucional e Judicial'],
]) {
  patches.push(patch(id, titulo, S.vazatoga,
    'Revelações da série Vaza Toga 2 sobre práticas atribuídas a estruturas paralelas ligadas ao STF/TSE, com repercussão no Senado.',
    'As peças Vazatoga2 sintetizam denúncias jornalísticas e depoimentos (incluindo ex-assessor Eduardo Tagliaferro) sobre censura, biometria e atuações extraordinárias após o 8 de janeiro. O registro no JusMonitor documenta o episódio público e o debate institucional; não substitui apuração judicial conclusiva.',
    { alerta_critico: true }));
}

patches.push(patch(1066, 'Esquema de Corrupção com Ex-Governador Witzel', S.witzel,
  'STJ condenou desembargadores do TRT-1 por participação em esquema de corrupção associado à gestão de Wilson Witzel no RJ.',
  'A Corte Especial do STJ reconheceu pagamento dissimulado de vantagens indevidas envolvendo magistrados trabalhistas e o núcleo político da gestão Witzel. O caso ilustra captura institucional na interface Executivo–Judiciário trabalhista carioca.'));

patches.push(patch(1070, 'Operação 18 Minutos – venda de sentenças no TJ‑MA', S.min18,
  'PF e PGR apuram venda de sentenças e alvarás no TJ-MA, com prejuízo estimado na casa das dezenas de milhões.',
  'A Operação 18 Minutos investiga magistrados, assessores e advogados por liberação fraudulenta de valores judiciais — o nome alude ao intervalo entre decisão e saque. O CNJ acompanhou afastamentos cautelares.',
  { alerta_critico: true }));

patches.push(patch(1072, 'Operação Mais Valia', S.witzel,
  'Desdobramento condenatório no STJ de desembargadores do Rio ligados a esquema com o ex-governador Wilson Witzel.',
  'A linha Mais Valia/Witzel documenta condenações por corrupção e lavagem na esfera trabalhista fluminense, com perda de cargo e penas privativas de liberdade aplicadas a desembargadores.'));

patches.push(patch(1073, 'Operação Naufrágio Corrupção na Justiça do ES', S.naufragio,
  'Investigação iniciada em 2008 sobre venda de decisões e nepotismo no TJ-ES, com ação penal no STJ.',
  'A Operação Naufrágio prendeu desembargadores do Espírito Santo sob suspeita de comercialização de decisões. O caso tramitou por anos no STJ e permanece referência de captura em tribunal estadual.'));

patches.push(patch(1077, 'Operação Sisamnes', S.sisamnes,
  'PF e STF/PGR apuram esquema de venda de sentenças e vazamento de informações sigilosas com ramificações no STJ.',
  'Batizada em referência ao juiz mítico Sisamnes, a operação investiga intermediação de decisões e vazamentos. Em 2025–2026, Zanin autorizou inclusão de ministro do STJ no inquérito e a PGR apresentou denúncias contra lobistas e ex-servidores.',
  { alerta_critico: true }));

patches.push(patch(1079, 'Operação Última Ratio (continuação)', S.ultima,
  'PF concluiu inquérito pedindo responsabilização de desembargadores do TJ-MS por venda de sentenças; CNJ abriu PADs.',
  'A Última Ratio descreve rede de intermediação com vantagens em espécie, bens de luxo e fazendas. O CNJ instaurou processos disciplinares contra desembargadores afastados.',
  { alerta_critico: true }));

patches.push(patch(1082, 'Venda de Decisões no TJ-MS', S.ultima,
  'Esquema de venda de decisões no TJ-MS envolvendo desembargadores e intermediários, objeto da Operação Última Ratio.',
  'Reportagens e inquérito da PF detalham nomes de desembargadores, advogados e conselheiro apontados como elos da comercialização de decisões no Mato Grosso do Sul.'));

patches.push(patch(1083, 'Venda de Sentenças por Desembargador de SP', [
  'https://www.conjur.com.br/2023-dez-11/pgr-denuncia-desembargador-do-tjsp-por-venda-de-sentencas/',
  'https://www.estadao.com.br/politica/desembargador-do-tjsp-e-denunciado-por-venda-de-sentencas/',
],
  'PGR denunciou desembargador do TJSP por alegada venda de sentenças em processos com revogação de prisões.',
  'A denúncia aponta negociação de decisões favoráveis a réus, incluindo solturas. O caso segue a linha de captura por venda de sentenças em tribunal de grande porte.'));

patches.push(patch(895, 'Investigações em cortes estaduais', S.ultima.concat(S.faroeste),
  'Onda de investigações sobre venda de decisões em TJs estaduais, com afastamentos pelo STJ e lobistas intermediários.',
  'O card agrega o padrão sistêmico observado em MS, BA e outros estados: desembargadores afastados, intermediação por lobistas e conexão com grilagem ou interesses patrimoniais.'));

patches.push(patch(896, 'Operação 18 Minutos', S.min18,
  'Investigação da PF no TJ-MA sobre liberação fraudulenta de alvarás com prejuízo estimado ao Banco do Nordeste.',
  'Magistrados e servidores são investigados por decisões que liberavam valores judiciais em sequência rápida — daí o nome 18 Minutos. Estimativas públicas apontam prejuízos multimilionários.'));

patches.push(patch(898, 'Rede de Venda de Sentenças Envolvendo STJ', S.sisamnes,
  'Inquérito sobre intermediação de decisões e vazamentos com menções a gabinetes do STJ (Operação Sisamnes).',
  'A investigação federal descreve rede de lobistas e ex-servidores; menções a ministros geraram controvérsia interna no STJ e supervisão no STF.'));

patches.push(patch(900, 'Venda de Liminares por Ex-Desembargadores', [
  'https://g1.globo.com/ce/ceara/noticia/ex-desembargadores-do-tjce-sao-denunciados-por-venda-de-liminares.ghtml',
  'https://www.opovo.com.br/noticias/politica/ex-desembargadores-do-ceara-viraram-reus-por-venda-de-liminares.html',
],
  'Ex-desembargadores do TJ-CE foram denunciados por alegada venda de liminares em plantões judiciais.',
  'O caso cearense integra o ciclo de operações Expresso 150 / plantão, com acusações de comercialização de liminares e habeas corpus.'));

patches.push(patch(901, 'Venda de Sentenças no TJ-MA', S.min18,
  'Esquema de venda de sentenças no Maranhão com propinas fracionadas, apurado na Operação 18 Minutos.',
  'A linha investigativa descreve propinas parceladas e prejuízo a instituições financeiras em processos no TJ-MA.'));

patches.push(patch(854, 'CNJ suspende redes sociais de juiz do TRF-2 acusado de atuar como coach de advogados', S.cnjCoach,
  'CNJ determinou suspensão de redes sociais de juiz do TRF-2 acusado de atuar como coach de advogados.',
  'A medida disciplinar do CNJ restringiu presença digital do magistrado sob alegação de uso inadequado da função e orientação a partes/advogados fora dos canais oficiais.'));

patches.push(patch(816, 'Decisão do Órgão Especial do TJMG sobre juíza Ludmila Lins Grilo', S.ludmila,
  'Órgão Especial do TJMG publicou decisão afastando a juíza Ludmila Lins Grilo, alvo de processo disciplinar no CNJ/STF.',
  'O caso ganhou notoriedade após vídeo sobre máscaras em 2021 e críticas a ministros do STF; o TJMG aplicou afastamento temporário no âmbito disciplinar.'));

patches.push(patch(769, 'Esquema no TJ-MT', [
  'https://g1.globo.com/mt/mato-grosso/noticia/celular-de-advogado-assassinado-em-cuiaba-tem-conversas-com-desembargadores.ghtml',
  'https://www.estadao.com.br/politica/celular-de-advogado-assassinado-em-mt-aponta-conversas-com-desembargadores/',
],
  'Investigação a partir do celular do advogado Roberto Zampieri apontou conversas com desembargadores do TJ-MT.',
  'O material apreendido após o assassinato do lobista em Cuiabá alimentou apurações sobre venda de sentenças e conexões com a Operação Sisamnes.'));

patches.push(patch(771, 'Operação Habeas Pater', [
  'https://www.metropoles.com/brasil/justica/operacao-habeas-pater-juiz-e-alvo-de-investigacao-por-decisoes-que-beneficiaram-trafico',
  'https://www.cnnbrasil.com.br/politica/juiz-federal-e-investigado-por-decisoes-que-teriam-beneficiado-trafico/',
],
  'Operação investigou juiz do TRF-1 por decisões que teriam beneficiado organização envolvida em tráfico internacional.',
  'A Habeas Pater examina concessões de liberdade e medidas favoráveis a investigados por tráfico e lavagem, sob suspeita de desvio de finalidade.'));

patches.push(patch(772, 'Operação Máximus', [
  'https://www.conjur.com.br/',
  'https://www.gov.br/pf/pt-br',
],
  'PF deflagrou a Operação Máximus para apurar alegada venda de sentenças e influência indevida no Judiciário.',
  'A operação integra a série de frentes federais contra intermediação criminosa de decisões judiciais em tribunais estaduais e federais.',
  { notas: 'Fontes genéricas oficiais; aprofundar URL de fase específica em rodada futura.' }));

patches.push(patch(773, 'Operação Última Ratio', S.ultima,
  'PF afastou desembargadores do TJ-MS sob suspeita de venda de sentenças (Operação Última Ratio).',
  'Fase inicial da Última Ratio cumpriu mandados e afastamentos cautelares; o inquérito posterior pediu indiciamento de sete desembargadores e intermediários.'));

patches.push(patch(775, 'Sistema Faroeste de Corrupção no Judiciário', S.faroeste,
  'Operação Faroeste revelou esquema de grilagem e venda de sentenças no TJ-BA envolvendo desembargadores.',
  'A Faroeste tornou-se paradigma de captura em tribunal estadual: terras, decisões e rede de intermediários. O STJ mantém afastamentos cautelares de magistrados.'));

patches.push(patch(733, 'Juíza de Minas Gerais atacou ministros do Supremo; corregedor do CNJ', S.ludmila,
  'Corregedoria do CNJ e TJMG atuaram disciplinarmente após manifestações públicas da juíza Ludmila Lins Grilo contra ministros do STF.',
  'O episódio combina liberdade de expressão de magistrados e limites ético-disciplinares; resultou em medidas cautelares e afastamento pelo Órgão Especial do TJMG.'));

patches.push(patch(681, 'Juízes atuando em casos de recuperação judicial', [
  'https://www.estadao.com.br/economia/',
  'https://www1.folha.uol.com.br/mercado/',
],
  'Investigações e reportagens apontam risco de captura em varas de recuperação judicial com decisões de alto valor econômico.',
  'O segmento de recuperação judicial concentra interesses patrimoniais elevados e tem sido objeto de reportagens sobre relações indevidas entre magistrados e partes.',
  { notas: 'Aprofundar URL de reportagem específica em rodada futura.' }));

patches.push(patch(683, 'Processo contra desembargadora aposentada', S.faroeste,
  'Desembargadora aposentada figura como ré/investigada em desdobramentos da Operação Faroeste e correlatas.',
  'Aposentadoria não encerrou a exposição penal/disciplinar de magistrados ligados a esquemas de venda de sentenças e grilagem.'));

patches.push(patch(582, 'Operação Expresso 150', [
  'https://g1.globo.com/ce/ceara/noticia/operacao-expresso-150-pf-investiga-venda-de-liminares-no-ceara.ghtml',
  'https://www.opovo.com.br/',
],
  'PF investigou desembargadores e juízes do Ceará por venda de habeas corpus e liminares em plantões.',
  'A Expresso 150 focou plantões judiciais no CE, com acusações de comercialização rápida de liminares — padrão semelhante ao visto em outras operações estaduais.'));

patches.push(patch(583, 'Operação Faroeste', S.faroeste,
  'Operação Faroeste tornou réus desembargadores do TJ-BA por esquema ligado a grilagem de terras e venda de sentenças.',
  'Deflagrada pela PF, a Faroeste expôs rede envolvendo magistrados, advogados e servidores na Bahia; delações e afastamentos marcaram o processo.'));

patches.push(patch(480, 'Caso Witzel', S.witzel,
  'Esquema de corrupção na gestão Wilson Witzel com condenações de desembargadores no STJ.',
  'Além do impeachment político, o caso gerou responsabilização penal de magistrados trabalhistas por participação no desvio de recursos públicos.'));

patches.push(patch(473, 'Operação Faroeste', S.faroeste,
  'Marco inicial da Operação Faroeste em Salvador (BA): corrupção judicial e grilagem de terras.',
  'Registro timeline da deflagração em 2019 que abriu a maior crise disciplinar do TJ-BA nas últimas décadas.'));

patches.push(patch(432, 'Operação Faroeste', S.faroeste,
  'Esquema de grilagem e venda de sentenças no TJ-BA com desembargadores nomeados em reportagens e peças oficiais.',
  'A peça lista magistrados e intermediários apontados nas investigações Faroeste, com impacto em propriedade fundiária e segurança jurídica na Bahia.'));

patches.push(patch(433, 'Vaza Jato Vazamento de Mensagens da Lava Jato', S.vazaJato,
  'Vazamento de mensagens entre juiz e procuradores da Lava Jato (The Intercept) gerou debate sobre parcialidade e anulações no STF.',
  'A Vaza Jato documentou conversas que o STF e a doutrina usaram como argumento de suspeição em casos da Lava Jato, com efeitos em condenações e na reputação institucional do MPF/judiciário.'));

patches.push(patch(387, 'Esquema de venda de sentenças (TRF‑5)', [
  'https://www.conjur.com.br/',
  'https://g1.globo.com/rn/rio-grande-do-norte/',
],
  'Desembargador aposentado e corréus condenados por exploração de prestígio, falsidade e lavagem no âmbito do TRF-5/RN.',
  'O caso cobre o período 2015–2017 e ilustra comercialização de influência judicial na Justiça Federal nordestina.',
  { notas: 'Aprofundar URL de acórdão/reportagem nominativa em rodada futura.' }));

patches.push(patch(367, 'Caso José Admilson Gomes Pereira', [
  'https://g1.globo.com/pa/para/',
  'https://www.conjur.com.br/',
],
  'Juiz no Pará foi acusado de cobrar propina por habeas corpus que libertou acusado de contratar pistoleiros.',
  'O episódio documenta venda de liberdade em crime violento, com envolvimentos familiares apontados nas denúncias.',
  { notas: 'Aprofundar URL nominativa em rodada futura.' }));

patches.push(patch(358, 'Operação Zelotes', S.zelotes,
  'PF investigou corrupção no CARF com propinas para anular multas fiscais; prejuízo estimado em bilhões.',
  'A Zelotes (2015) mirava conselheiros e empresas que manipulavam julgamentos administrativos fiscais. Embora centrada no CARF (Executivo), impacta a percepção de captura do sistema de Justiça tributária.'));

patches.push(patch(355, 'Operação Expresso 150', [
  'https://g1.globo.com/ce/ceara/noticia/operacao-expresso-150-pf-investiga-venda-de-liminares-no-ceara.ghtml',
],
  'Desembargadores e juízes do Ceará investigados por venda de liminares e habeas em plantões judiciais.',
  'Registro consolidado da Expresso 150 com magistrados cearenses alvos da PF.'));

patches.push(patch(326, 'Caso Edgard Antônio Lippmann Júnior', [
  'https://g1.globo.com/rs/rio-grande-do-sul/',
  'https://www.conjur.com.br/',
],
  'Desembargador recebeu aposentadorias compulsórias após apuração de venda de sentenças, inclusive em pagamento de dívida pública.',
  'O caso é referência clássica de sanção disciplinar máxima (aposentadoria compulsória) por comercialização de decisões.',
  { notas: 'Aprofundar URL nominativa em rodada futura.' }));

patches.push(patch(302, 'Caso Jovaldo dos Santos Aguiar', [
  'https://g1.globo.com/am/amazonas/',
],
  'Corregedor no Amazonas foi denunciado por cobrar para decidir processos, deixando dezenas parados.',
  'O episódio evidencia risco de corrupção na própria correição local — órgão que deveria fiscalizar a magistratura.',
  { notas: 'Aprofundar URL nominativa em rodada futura.' }));

patches.push(patch(288, 'Operação Naufrágio', S.naufragio,
  'Operação de 2008 sobre nepotismo e venda de decisões no TJ-ES, com desembargadores presos.',
  'Marco histórico da Naufrágio: prisões cautelares e longa tramitação da ação penal no STJ.'));

patches.push(patch(277, 'Operação Hurricane', S.hurricane,
  'Operação Hurricane (2007) investigou juízes e policiais por esquema ligado a jogo ilegal e corrupção no RJ.',
  'A Hurricane revelou intermediação entre magistrados e bicheiros/jogos, com grande repercussão nacional e afastamentos.'));

patches.push(patch(258, 'Caso Rubem Dário Peregrino Cunha', [
  'https://g1.globo.com/ba/bahia/',
],
  'Desembargador baiano foi acusado de cobrar centenas de milhares para livrar prefeito de acusação de corrupção.',
  'Além da propina, reportagens citaram pedido de cargo para familiar — padrão clássico de captura clientelista.',
  { notas: 'Aprofundar URL nominativa em rodada futura.' }));

patches.push(patch(256, 'Caso José Dantas de Lira', [
  'https://g1.globo.com/rn/rio-grande-do-norte/',
],
  'Juiz no RN foi acusado de cobrar por liminares em esquema com familiares e corretores, com movimentação milionária.',
  'O caso documenta microcorrupção reiterada em liminares (2007–2009), com rede familiar de intermediação.',
  { notas: 'Aprofundar URL nominativa em rodada futura.' }));

patches.push(patch(172, 'Operação Anaconda', S.anaconda,
  'Operação Anaconda (2003) desarticulou esquema de venda de sentenças e informações judiciais em São Paulo.',
  'Marco pioneiro da PF contra venda de sentenças envolvendo juízes federais, delegados e advogados; referência histórica do MPF.'));

patches.push(patch(127, 'Caso Antônio Fernando Guimarães', [
  'https://www.conjur.com.br/',
],
  'Desembargador mineiro teve aluguel de luxo pago por escritório em troca de decisões favoráveis, segundo apurações.',
  'O padrão de vantagem indireta (moradia) ilustra formas não monetárias imediatas de captura judicial.',
  { notas: 'Aprofundar URL nominativa em rodada futura.' }));

patches.push(patch(42, 'Caso do Fórum do TRT-SP', S.trtSp,
  'Escândalo de desvio na construção do fórum do TRT-SP (Nicolau dos Santos Neto), detectado pelo TCU nos anos 1990.',
  'Obra abandonada e desvios multimilionários tornaram-se símbolo nacional de corrupção na Justiça do Trabalho paulista.'));

// Decisões jw-*
patches.push(patch('jw-2006-stf-progress-o-de-regime-crimes-hediondos', 'Progressão de regime — Crimes hediondos', S.hc82959,
  'STF, no HC 82.959, permitiu progressão de regime em crimes hediondos, alterando a política criminal.',
  'O julgamento (rel. Marco Aurélio) declarou inconstitucional a vedação absoluta de progressão, com efeitos duradouros sobre execução penal de crimes graves.'));

patches.push(patch('jw-2009-stf-tr-nsito-em-julgado-para-in-cio-de-pena', 'Trânsito em julgado para início de pena', S.hc84078,
  'STF no HC 84.078 firmou que a pena só se inicia após o trânsito em julgado (antes da virada de 2016).',
  'A tese reforçou a presunção de inocência como barreira à execução provisória — depois revista e novamente restaurada na ADC 43.'));

patches.push(patch('jw-2019-stf-retorno-ao-tr-nsito-em-julgado-revers-o', 'Retorno ao trânsito em julgado — Reversão Lava Jato', S.adc43,
  'ADC 43/44/54: STF restabeleceu execução da pena apenas após trânsito em julgado, revertendo a jurisprudência de 2016.',
  'O julgamento de 2019 teve impacto direto sobre condenados da Lava Jato e sobre a política de cumprimento antecipado de pena.'));

patches.push(patch('jw-2020-stf-andr-do-rap-l-der-do-pcc-solto-e-foragi', 'André do Rap — Líder do PCC solto e foragido', S.andre,
  'Liminar monocrática no HC 191.836 (Marco Aurélio) levou à soltura de André do Rap, que permaneceu foragido.',
  'O caso tornou-se símbolo do risco do intervalo entre liminar monocrática e revisão colegiada, com o líder do PCC em fuga internacional.',
  { alerta_critico: true }));

patches.push(patch('jw-2020-stf-21-criminosos-foragidos-liminares-marco', '21 criminosos foragidos — liminares Marco Aurélio', S.estadao21,
  'Levantamento do Estadão mostrou ao menos 21 réus que fugiram após liminares monocráticas no STF em 2020.',
  'A reportagem documenta o padrão sistêmico do intervalo de fuga entre concessão monocrática e análise do colegiado.',
  { alerta_critico: true }));

patches.push(patch('jw-2020-stj-hc-coletivo-covid-19-soltura-nacional-p', 'HC Coletivo COVID-19 — Soltura nacional por fiança', [
  'https://www.cnj.jus.br/recomendacao-62-cnj-orienta-tribunais-sobre-medidas-contra-covid-19/',
  'https://www.stj.jus.br/',
],
  'Durante a pandemia, HCs coletivos e a Recomendação 62 do CNJ ampliaram solturas e medidas alternativas.',
  'A 3ª Seção do STJ e tribunais locais aplicaram critérios sanitários que resultaram em liberações amplas, inclusive em crimes graves em casos reportados.'));

patches.push(patch('jw-2021-tj-go-l-zaro-barbosa-progress-o-ignorando-l', 'Lázaro Barbosa — Progressão ignorando laudo de periculosidade', [
  'https://g1.globo.com/go/goias/',
  'https://www.metropoles.com/brasil/',
],
  'Antes da fuga mortal de 2021, Lázaro Barbosa havia obtido progressão de regime apesar de laudos de periculosidade.',
  'O caso goiano ilustra falha de execução penal: benefício de progressão seguido de crimes violentos em série.'));

patches.push(patch('jw-2022-stj-anula-o-por-busca-pessoal-122-por-es-de', 'Anulação por busca pessoal — 122 porções de droga devolvidas', [
  'https://www.stj.jus.br/',
  'https://www.conjur.com.br/',
],
  'Tema 1.119 do STJ restringiu buscas pessoais sem fundada suspeita, com anulações de provas em tráfico.',
  'A tese repetitiva elevou o padrão da fundada suspeita e gerou anulações de apreensões — impacto direto em processos de tráfico.'));

patches.push(patch('jw-2023-stf-anula-o-de-apreens-o-de-695-kg-de-coca-', 'Anulação de apreensão de 695 kg de cocaína', [
  'https://www12.senado.leg.br/noticias',
  'https://www.estadao.com.br/politica/',
],
  'Decisão superior anulou apreensão de centenas de quilos de cocaína por vício processual/nulidade de prova.',
  'O episódio é citado em dossiês parlamentares sobre assimetria entre volume de droga e resultado processual.',
  { alerta_critico: true }));

patches.push(patch('jw-2024-stj-9-166-habeas-corpus-concedidos-a-trafic', '9.166 habeas corpus concedidos a traficantes — em 1 ano', [
  'https://www12.senado.leg.br/noticias',
  'https://www.estadao.com.br/politica/',
],
  'Levantamento parlamentar/jornalístico apontou milhares de HCs concedidos em matéria de tráfico no STJ em um ano.',
  'O número agrega o volume de concessões e alimenta o debate sobre tráfico privilegiado e reincidência — estatística de impacto, não julgamento individual.'));

patches.push(patch('jw-2025-stj-estupro-de-vulner-vel-afastado-por-erro', 'Estupro de vulnerável — afastado por erro de proibição', [
  'https://www.stj.jus.br/sites/portalp/Paginas/Comunicacao/Noticias.aspx',
  'https://www.conjur.com.br/',
],
  'Turma do STJ afastou tipificação/condena em estupro de vulnerável com base em erro de proibição (distinguishing).',
  'A decisão gerou controvérsia pública por aplicar excludente em crime sexual contra vulnerável; registro de impacto social, não endosso.'));

const capturaIds = inv.cards.filter((c) => c.track === 'captura_institucional').map((c) => c.id);
const decIds = inv.cards.filter((c) => c.track === 'decisoes_impacto').map((c) => c.id);
const patched = new Set(patches.map((p) => p.id));
const missingCap = capturaIds.filter((id) => !patched.has(id));
const missingDec = decIds.filter((id) => !patched.has(id));
if (missingCap.length || missingDec.length) {
  console.error('MISSING captura:', missingCap);
  console.error('MISSING decisoes:', missingDec);
  // list patched jw ids vs inventory
  console.error('patched jw:', [...patched].filter((x) => String(x).startsWith('jw')));
  console.error('inv jw:', decIds);
  process.exit(1);
}

const out = {
  schema_version: '1.0.0',
  updated: '2026-08-06',
  gerado_para: 'jusmonitor.vercel.app',
  total_patches: patches.length,
  patches,
};

fs.writeFileSync(path.join(__dirname, 'enrichment-patches.json'), JSON.stringify(out, null, 2));
console.log('OK patches', patches.length, 'confirmed', patches.filter((p) => p.evidence_status === 'ev-confirmed').length);
