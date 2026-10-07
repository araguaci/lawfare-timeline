# -*- coding: utf-8 -*-
"""Gera o estudo T-270 Compilado Lawfare (síntese + antologia) a partir de _posts/estudos."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "_posts" / "estudos"
OUT = SRC / "2026-10-06-compilado-lawfare.md"
SITE = "https://lawfare-timeline.vercel.app"

SKIP_SLUGS = {"compilado-lawfare"}

AXES: list[tuple[str, str, tuple[str, ...]]] = [
    (
        "metodo",
        "Método, padrões e como ler",
        (
            "como-ler",
            "padroes-sistemicos",
            "narrativa-vs-evidencia",
            "top30",
            "radar",
            "lacunas",
            "methodology",
            "dashboard",
        ),
    ),
    (
        "stf",
        "STF, INQ 4.781 e a premissa protetora",
        (
            "vaza-toga",
            "inq",
            "moraes",
            "liminar",
            "monocratica",
            "nemo-judex",
            "legitima-defesa",
            "estupidez",
            "criatura",
            "sete-anos",
            "excecao",
            "coaf-moraes",
            "golpe-brasil",
            "democratic-erosion",
            "fachin",
            "gabinete",
        ),
    ),
    (
        "tse",
        "TSE, USAID e seletividade eleitoral",
        (
            "tse-usaid",
            "tse-seletividade",
            "inelegibilidade",
            "cassacao",
            "seletividade-punitiva",
            "video-de-ia",
            "bolsonaro-na-convencao",
            "paywall-eleitoral",
            "p12-b",
            "usaid",
        ),
    ),
    (
        "mineracao",
        "Mineração, rejeito e terras raras",
        (
            "rejeito",
            "lama",
            "minerio",
            "minerios",
            "terras-raras",
            "serra-curral",
            "brumadinho",
            "cade",
        ),
    ),
    (
        "pcc",
        "PCC, crime organizado e vetor transnacional",
        (
            "pcc",
            "cv-",
            "crime-organizado",
            "ofac",
            "yakuza",
            "mafia",
            "funk",
            "ouro-ilegal",
            "amazonia",
            "gafilat",
            "europol",
            "terrorista",
            "gi-toc",
            "delegada",
            "infiltracao",
        ),
    ),
    (
        "p11",
        "Extração P11, penduricalhos e máquina de gastos",
        (
            "p11",
            "penduricalho",
            "custeio",
            "gastos",
            "extravagancia",
            "prisao-economica",
            "estatais",
            "paris",
            "loop-extracao",
            "viagens-gastos",
        ),
    ),
    (
        "bancos",
        "Bancos, Vorcaro, Master, INSS e carbono",
        (
            "vorcaro",
            "master",
            "inss",
            "farra",
            "americanas",
            "carbono",
            "sigilo-de-100",
            "banco",
            "biomm",
        ),
    ),
    (
        "justica",
        "Justiça seletiva, HC, foro e dosimetria",
        (
            "justicawatch",
            "duplo-padrao",
            "habeas",
            "hc-seletivo",
            "foro-privilegiado",
            "dosimetria",
            "indenizacao",
            "dois-pesos",
            "estado-como-reu",
            "delacao",
            "weaponizacao",
            "erro-judiciario",
        ),
    ),
    (
        "narrativa",
        "Captura cultural, SPLC, P04 e mapa de conexões",
        (
            "splc",
            "p04",
            "mcd",
            "conexoes-documentadas",
            "direita-permitida",
            "sleeping",
            "porta-giratoria",
            "p13",
        ),
    ),
    (
        "saude",
        "Saúde, pandemia e Operação Sepse",
        (
            "pandemia",
            "sepse",
            "parasitas",
            "hmap",
            "uti",
            "covid",
        ),
    ),
    (
        "historia",
        "Precedentes históricos e República",
        (
            "republica",
            "precedentes",
            "mensalao",
            "ap-470",
            "1891",
        ),
    ),
    (
        "outros",
        "Outros recortes (patrimônio, cartórios, sorteio, dados)",
        (
            "salles",
            "cartorio",
            "sorteio",
            "reforma-tributaria",
            "escalada",
            "protecao-tecnica",
            "p10-promovido",
        ),
    ),
]


def parse_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    raw, body = parts[1], parts[2]
    meta: dict = {}
    key = None
    buf: list[str] = []
    for line in raw.splitlines():
        if re.match(r"^[A-Za-z0-9_]+:", line):
            if key is not None:
                meta[key] = "\n".join(buf).strip().strip("\"'")
            key, _, rest = line.partition(":")
            key = key.strip()
            buf = [rest.strip()]
        elif key is not None:
            buf.append(line.strip())
    if key is not None:
        meta[key] = "\n".join(buf).strip().strip("\"'")
    return meta, body.lstrip("\n")


def slug_from_name(name: str) -> str:
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", name[:-3])


def permalink_of(meta: dict, name: str) -> str:
    perm = (meta.get("permalink") or "").strip()
    if perm:
        return perm if perm.endswith("/") else perm + "/"
    return f"/posts/{slug_from_name(name)}/"


def classify(name: str, title: str, desc: str, corpus: str, tags: str) -> str:
    """Classifica por arquivo/título primeiro; tags P0x sozinhas não decidem o eixo."""
    low_id = f"{name} {title} {corpus}".lower()
    low_all = f"{low_id} {desc}".lower()
    if "pcc" in low_id or "narco" in low_id or "yakuza" in low_id or "europol" in low_id:
        return "pcc"
    if "splc" in low_id or "mcd-" in low_id or "p04-pela" in low_id:
        return "narrativa"
    if "rejeito" in low_id or "terras-raras" in low_id or "loop-da-lama" in low_id:
        return "mineracao"
    if "tse" in low_id or "usaid" in low_id or "p12-b" in low_id:
        return "tse"
    if "sepse" in low_id or "parasitas" in low_id or "pandemia" in low_id:
        return "saude"
    if "precedentes-republica" in low_id or "mensalao" in low_id or "ap-470" in low_id:
        return "historia"
    if "como-ler" in low_id or "padroes-sistemicos" in low_id or "narrativa-vs" in low_id:
        return "metodo"
    for axis_id, _label, keys in AXES:
        if axis_id == "outros":
            continue
        if any(k in low_all for k in keys):
            return axis_id
    return "outros"


def rewrite_links(md: str) -> str:
    def abs_internal(match: re.Match) -> str:
        href = match.group(1)
        if href.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)
        if href.startswith("/"):
            return f"]({SITE}{href})"
        return match.group(0)

    return re.sub(r"\]\(([^)]+)\)", abs_internal, md)


def demote_headings(md: str, n: int = 2) -> str:
    prefix = "#" * n

    def repl(match: re.Match) -> str:
        hashes, rest = match.group(1), match.group(2)
        extra = min(6, len(hashes) + n)
        return f"{'#' * extra}{rest}"

    return re.sub(r"^(#{1,6})(\s+.*)$", repl, md, flags=re.M)


def load_posts() -> list[dict]:
    posts = []
    for path in sorted(SRC.glob("*.md")):
        slug = slug_from_name(path.name)
        if slug in SKIP_SLUGS:
            continue
        text = path.read_text(encoding="utf-8")
        meta, body = parse_front_matter(text)
        title = meta.get("title") or slug
        corpus = meta.get("id_corpus") or ""
        desc = re.sub(r"\s+", " ", meta.get("description") or "")
        perm = permalink_of(meta, path.name)
        posts.append(
            {
                "path": path,
                "slug": slug,
                "title": title,
                "id": corpus,
                "description": desc,
                "permalink": perm,
                "url": f"{SITE}{perm}",
                "axis": classify(path.name, title, desc, corpus, meta.get("tags") or ""),
                "body": body,
                "date": meta.get("date") or path.name[:10],
            }
        )
    return posts


def catalog_md(posts: list[dict]) -> str:
    lines = [
        "## 📚 Catálogo dos estudos",
        "",
        f"Este compilado reúne **{len(posts)} estudos** publicados em `_posts/estudos`. "
        "Cada título aponta para a página canônica no site. As fontes primárias de cada peça "
        "permanecem no texto integral (Parte B) e nas notas originais.",
        "",
    ]
    by_axis: dict[str, list[dict]] = {a[0]: [] for a in AXES}
    for p in posts:
        by_axis.setdefault(p["axis"], []).append(p)
    for axis_id, label, _ in AXES:
        items = by_axis.get(axis_id) or []
        if not items:
            continue
        lines.append(f"### {label}")
        lines.append("")
        for p in items:
            ident = f"`{p['id']}` · " if p["id"] else ""
            desc = f" — {p['description']}" if p["description"] else ""
            if len(desc) > 180:
                desc = desc[:177] + "…"
            lines.append(f"- {ident}[{p['title']}]({p['url']}){desc}")
        lines.append("")
    return "\n".join(lines)


def anthology_md(posts: list[dict]) -> str:
    chunks = [
        "# Parte B — Antologia integral",
        "",
        "Os textos abaixo são os estudos originais, com front matter removido. "
        "Links internos foram reescritos para URL absoluta do site. "
        "A peça canônica de cada capítulo continua sendo a página individual — "
        "use o link no cabeçalho do capítulo se for citar.",
        "",
    ]
    order = {a[0]: i for i, a in enumerate(AXES)}
    posts_sorted = sorted(posts, key=lambda p: (order.get(p["axis"], 99), p["date"], p["title"]))
    current = None
    for p in posts_sorted:
        if p["axis"] != current:
            current = p["axis"]
            label = next(lbl for aid, lbl, _ in AXES if aid == current)
            chunks.append(f"# {label}")
            chunks.append("")
        ident = f"{p['id']} · " if p["id"] else ""
        chunks.append(f"# {ident}{p['title']}")
        chunks.append("")
        chunks.append(f"*Canônico:* [{p['url']}]({p['url']})")
        chunks.append("")
        body = rewrite_links(p["body"])
        # Evita H1 do post original competir com o título do capítulo.
        body = re.sub(r"^# ", "## ", body, count=1, flags=re.M)
        chunks.append(body.rstrip())
        chunks.append("")
        chunks.append("***")
        chunks.append("")
    return "\n".join(chunks)


def synthesis_md(posts: list[dict]) -> str:
    n = len(posts)
    return f"""# Parte A — Síntese do compilado

Este volume não inventa dossiê novo. Organiza os **{n} estudos** já publicados na categoria `estudos` em uma leitura contínua e, na Parte B, devolve o texto integral de cada um, com [links para a página canônica]({SITE}/estudos/) e para as fontes que o estudo original já citava.

A regra do corpus vale aqui: o que não fecha, não sobe. [T-208]({SITE}/posts/narrativa-vs-evidencia-corpus-bridge/) é a trava. Selos `ev-confirmed`, `ev-contested`, `ev-alleged` e `ev-inference` continuam no texto de origem.

## Como ler este livro

Há três camadas no projeto, descritas no [guia sem jargão]({SITE}/posts/como-ler-o-lawfare-timeline-guia-para-o-leitor-brasileiro/):

1. **Linha do tempo** — eventos com data, fonte e ID.
2. **Estudos** — cruzamentos que nomeiam um mecanismo.
3. **Padrões (P01–P13)** — só entram no catálogo quando o mesmo mecanismo aparece em três ou mais casos independentes.

Este compilado é a camada 2 inteira, lida como livro. O [dashboard mestre]({SITE}/posts/padroes-sistemicos-dashboard/) é o mapa dos padrões. O [radar de lacunas]({SITE}/posts/top30-alertas-criticos-operacoes-sem-dossie/) (T-196) é o que ainda não tem dossiê.

## Tese em uma página

A falha institucional brasileira documentada nestes estudos **não é um bug ocasional**. É desenho recorrente: o mesmo tipo de manobra reaparece sob nome novo de operação, de inquérito ou de acordo. O [dossiê de padrões]({SITE}/posts/padroes-sistemicos-dashboard/) formula isso assim: a falha estrutural não é vício do sistema — é o seu design principal.

Três eixos se cruzam o tempo todo:

- **Poder sem colegiado imediato.** Liminar monocrática, relatoria acumulada, inquérito sem mérito que dura anos. Ver [Anatomia da liminar]({SITE}/posts/anatomia-liminar-monocratica-stf-poder-individual-sem-controle/), [T-221]({SITE}/posts/2026-06-16-nemo-judex-in-causa-propria-formalizado-por-orgao-de-estado-a-preliminar-da-dpu-na-ap-2782/) e [T-266]({SITE}/posts/2026-08-24-refutacao-juridica-da-tese-de-legitima-defesa-institucional-como-fundamento-para-autotutel/).
- **Narrativa no lugar do caso.** P04 e P04b: o fato some, ou vira «só um lado». Vale para esquerda e direita — [T-227]({SITE}/posts/2026-07-20-p04-pela-direita-narco-soberania-eleitoral-e-diplomacia-das-sombras-como-espelhos-estrutur/) e o [modelo SPLC]({SITE}/posts/splc-modelo-brasil/).
- **Dinheiro público como veículo.** P05 e P11: INSS, FGC, estatais, penduricalho, rejeito que é ativo num regulador e «não-ativo» noutro. [P11 expandido]({SITE}/posts/p11-expandido-loop-extracao-perpetua-economia-politica-brasil/), [T-268]({SITE}/posts/2026-06-12-o-loop-da-lama-rejeito-como-ativo-bilionario-perante-o-cade-passivo-inexistente-perante-a-/), [T-219]({SITE}/posts/2026-03-28-farra-do-inss-rede-completa-conafer-careca-do-inss-nucleo-politico-e-o-nucleo-internaciona/).

O [T-269]({SITE}/posts/2026-09-13-a-criatura-e-o-consenso-teoria-da-estupidez/) fecha o arco político-editorial: o mesmo Alexandre de Moraes que recebeu licença partidária em 2021 («defesa da democracia») vira objeto de recusa editorial em setembro de 2026. O [INQ 4.781]({SITE}/posts/crise-brasil-eua-inq-4781-vaza-toga-e-sancoes/) segue aberto. O consenso, não.

## Os padrões, em uma frase cada

Síntese operacional a partir do [dashboard]({SITE}/posts/padroes-sistemicos-dashboard/) e das promoções posteriores ([T-222]({SITE}/posts/2026-07-16-p10-promovido-a-padrao-autonomo-infraestrutura-de-servico-compartilhada-com-dois-nos-verif/), [T-223]({SITE}/posts/2026-07-16-p12-b-instanciado-como-assimetria-de-capacidade-analitica-camada-oficial-aberta-tse-camada/), [T-254]({SITE}/posts/2026-08-18-t-254-p13-porta-giratoria/)):

| Código | Mecanismo |
|---|---|
| P01 | O processo cai por defeito formal, sem enfrentar o mérito |
| P02 | Quem investiga ou denuncia vira alvo |
| P03 | Um ministro, sozinho, trava ou destrava o caso |
| P04 / P04b | A cobertura decide o que «aconteceu», ou dilui o fato em opinionismo |
| P05 | Recurso público mistura-se ao esquema que deveria fiscalizar |
| P06 / P06-B | O caso envelhece até prescrever; CPI/CPMI acaba sem relatório |
| P07 | A rede atravessa gerações e trocas de governo |
| P08 | Fintech, cripto e ouro irregular como trilho de lavagem |
| P09 | Legitimidade cultural como escudo («defesa da democracia», narcoestética) |
| P10 | Política e crime organizado compartilham prestador de serviço |
| P11 | Loop macro: juro, dívida, transferência e extração que se realimentam |
| P12 / P12-B | Assimetria de capacidade analítica / paywall de dado eleitoral |
| P13 | Porta giratória: autoridade pública vira capital relacional privado |

Metodologia: [METHODOLOGY.md](https://github.com/araguaci/lawfare-timeline/blob/main/METHODOLOGY.md).

## Eixo por eixo

### STF e a criatura

O [índice Vaza Toga]({SITE}/posts/vaza-toga-corpus-bridge/) (T-207) ancora o gabinete paralelo e o INQ 4.781. O [Estadão]({SITE}/posts/2025-12-01-o-estado-de-s-paulo-publica-editorial-sete-anos-de-excecao-criticando-manutencao-do-inq-47/) (T-265) marca a rachadura editorial («sete anos de exceção»). A DPU formaliza *nemo judex* na [AP 2782]({SITE}/posts/2026-06-16-nemo-judex-in-causa-propria-formalizado-por-orgao-de-estado-a-preliminar-da-dpu-na-ap-2782/) (T-221). [T-266]({SITE}/posts/2026-08-24-refutacao-juridica-da-tese-de-legitima-defesa-institucional-como-fundamento-para-autotutel/) recusa a tese de «legítima defesa institucional» como autotutela. [T-269]({SITE}/posts/2026-09-13-a-criatura-e-o-consenso-teoria-da-estupidez/) lê a sequência 2021–2026 com Bonhoeffer: o poder precisa da estupidez alheia — slogan no lugar do caso.

Análise evidencial do golpe e erosão: [Quem deu o golpe]({SITE}/posts/golpe-brasil-analise-evidencial/) e [Brazil Democratic Erosion 2026]({SITE}/posts/brazil-democratic-erosion-2026/). COAF e acumulação de funções: [T-198]({SITE}/posts/coaf-moraes-acumulacao-funcoes-dosimetria/).

### TSE e seletividade

[T-216]({SITE}/posts/tse-usaid-parceria-censura-seletiva/) documenta o acordo TSE–USAID e repasses via ONGs. [T-180]({SITE}/posts/tse-seletividade-inelegibilidade-cassacao/) e [T-217]({SITE}/posts/seletividade-punitiva-tse-casos-isolados/) tratam cassação e seletividade punitiva. [T-223]({SITE}/posts/2026-07-16-p12-b-instanciado-como-assimetria-de-capacidade-analitica-camada-oficial-aberta-tse-camada/) instancia P12-B: portal aberto na superfície, assimetria de capacidade por baixo. [T-247]({SITE}/posts/2026-07-25-episodio-video-de-ia-de-bolsonaro-na-convencao-do-pl-detona-disputa-de-competencia-stftse-/) é o episódio de IA na convenção do PL e a disputa de competência STF/TSE.

### Mineração: dois mercados, um loop

[T-197]({SITE}/posts/operacao-rejeito-serra-curral-manuscritos/) consolida Rejeito / Serra do Curral. [T-267]({SITE}/posts/2026-09-10-minerios-terras-raras-dois-mercados/) cruza 80 IDs: 22 presos em setembro de 2025, zero em janeiro de 2026; Serra Verde vendida por US$ 2,8 bi. [T-268]({SITE}/posts/2026-06-12-o-loop-da-lama-rejeito-como-ativo-bilionario-perante-o-cade-passivo-inexistente-perante-a-/) é a contradição CADE/CVM: o mesmo rejeito muda de natureza jurídica conforme o regulador.

### PCC e o trilho compartilhado

O cluster transnacional (WSJ, OFAC, Yakuza, GAFILAT, Europol, GI-TOC) e as pontes domésticas ([T-201]({SITE}/posts/pcc-transnacional-ofac-eua-luso/), [T-195]({SITE}/posts/cpi-crime-organizado-pcc-infiltracao-eleitoral/), [T-202]({SITE}/posts/delegada-pcc-infiltracao-institucional-sp/), [T-218]({SITE}/posts/ouro-ilegal-vetor-p08-amazonia-pcc-cv-venezuela/), [T-220]({SITE}/posts/convergencia-estrutural-vetor-pcc-ofac-rede-arpar-farra-do-inss-via-infraestrutura-finance/)) descrevem o mesmo desenho: facção, porto, ouro, fintech e, quando cabe, dinheiro público. [T-1512]({SITE}/posts/designacao-terrorista-pcc-cv/) registra a designação terrorista e o enquadramento P04b da cobertura. P10 ([T-222]({SITE}/posts/2026-07-16-p10-promovido-a-padrao-autonomo-infraestrutura-de-servico-compartilhada-com-dois-nos-verif/)) é o nome do prestador compartilhado.

### Extração e penduricalho

[P11 expandido]({SITE}/posts/p11-expandido-loop-extracao-perpetua-economia-politica-brasil/), [Prisão econômica]({SITE}/posts/prisao-economica/), [máquina de gastos]({SITE}/posts/maquina-gastos-p11-indice-cluster/) (T-194), [custeio administrativo]({SITE}/posts/custeio-administrativo-federal-p11/) (T-191), [estatais]({SITE}/posts/estatais-rombo-p11-complemento/) (T-200) e [T-226]({SITE}/posts/o-ciclo-do-penduricalho-restricao-burla-e-autolegitimacao-mar-jul2026/) descrevem o loop: restrição, burla, autolegitimação. Paris e viagens entram como cluster de extravagância ([T-204]({SITE}/posts/gastos-paris-cluster-extravagancia-janja/), [T-193]({SITE}/posts/viagens-gastos-sigilo-complemento-p11/)).

### Master, INSS, carbono

[T-192]({SITE}/posts/vorcaro-triangulo-carbono-mineracao-banco/), [T-219]({SITE}/posts/2026-03-28-farra-do-inss-rede-completa-conafer-careca-do-inss-nucleo-politico-e-o-nucleo-internaciona/), [T-215]({SITE}/posts/2026-06-16-2-turma-do-stf-mantem-prisao-de-pai-e-primo-de-daniel-vorcaro-por-31-gilmar-mendes-diverge/), [T-251]({SITE}/posts/2026-08-12-t-251-convergencia-estrutural-stffamiliabanco-master-p02p05p07-aplicados-ao-mesmo-colegiad/) e [T-1765]({SITE}/posts/2026-07-27-sintese-estrutural-sigilo-de-100-anos-como-padrao-p10-confirmado-vorcaro-executivo-e-carec/) cruzam liquidação bancária, família no colegiado, sigilo de 100 anos e o INSS. Americanas ([T-199]({SITE}/posts/fraude-lojas-americanas-risco-sacado/)) e Biomm entram como variação do mesmo trilho financeiro.

### Justiça seletiva

[T-209 JustiçaWatch]({SITE}/posts/justicawatch-brasil-corpus-bridge/), [T-205]({SITE}/posts/duplo-padrao-judicial-corpus-bridge/), [T-250]({SITE}/posts/dois-pesos-duas-medidas-erro-judiciario-indenizacao-assimetrica/), [HC seletivo]({SITE}/posts/hc-seletivo-habeas-corpus-como-privilegio-processual/), [foro privilegiado]({SITE}/posts/foro-privilegiado-jurisdicao-como-escudo-brasil/) e [dosimetria da impunidade]({SITE}/posts/dosimetria-da-impunidade-lei-15402-ep72-tratamento-diferenciado/) medem o privilégio processual. [Estado como réu]({SITE}/posts/estado-como-reu-weaponizacao-processual-contra-cidadaos/) inverte o vetor: o cidadão vira alvo da máquina que deveria protegê-lo.

### Narrativa e SPLC

[SPLC → Brasil]({SITE}/posts/splc-modelo-brasil/) e a [ponte T-206]({SITE}/posts/splc-modelo-brasil-corpus-bridge/) descrevem transferência estrutural de weaponização. [T-263]({SITE}/posts/2026-08-26-auditoria-evidencial-do-mapa-das-conexoes-documentadas-mcd-052024-como-artefato-do-padrao-/) audita o MCD-05/2024 aresta a aresta. [T-190]({SITE}/posts/direita-permitida-dossie/) e [T-227]({SITE}/posts/2026-07-20-p04-pela-direita-narco-soberania-eleitoral-e-diplomacia-das-sombras-como-espelhos-estrutur/) impedem a leitura de um lado só. [T-254]({SITE}/posts/2026-08-18-t-254-p13-porta-giratoria/) promove a porta giratória a padrão.

### Saúde e precedentes

Pandemia capturada e o arco Sepse/Parasitas (T-210 a T-214) mostram P03+P07 em verba de emergência. [T-224]({SITE}/posts/precedentes-republica-1891-1930/) e [República capturada]({SITE}/posts/republica-capturada/) puxam o fio até 1891–1930. [T-253]({SITE}/posts/2010-04-08-t-253-ap-470-mensalao-stf-exige-base-documental-e-probatoria-para-recusar-reiteradamente-a/) (AP 470) é o precedente de recusa reiterada de inclusão no polo passivo.

## O que este compilado não afirma

Não substitui a linha do tempo (os IDs main). Não reabre mérito penal. Não trata selo `ev-alleged` como fato. Não unifica autoria de vídeos, cifras de plateia nem testemunho sem URL. Cada estudo da Parte B traz a sua própria lista do que **não** afirma — respeite essa lista ao citar.

## Referências-mãe (porta de entrada)

- Site: [{SITE}/estudos/]({SITE}/estudos/)
- Guia: [Como ler o Lawfare Timeline]({SITE}/posts/como-ler-o-lawfare-timeline-guia-para-o-leitor-brasileiro/)
- Padrões: [Dashboard mestre]({SITE}/posts/padroes-sistemicos-dashboard/)
- Método: [T-208]({SITE}/posts/narrativa-vs-evidencia-corpus-bridge/) · [METHODOLOGY.md](https://github.com/araguaci/lawfare-timeline/blob/main/METHODOLOGY.md)
- INQ 4.781: [crise Brasil–EUA]({SITE}/posts/crise-brasil-eua-inq-4781-vaza-toga-e-sancoes/)
- JustiçaWatch: [T-209]({SITE}/posts/justicawatch-brasil-corpus-bridge/)

"""


FRONT_MATTER = """---
id_corpus: "T-270"
thematic_track: true
title: "T-270 · Compilado Lawfare — síntese e antologia dos estudos"
description: "Livro dos estudos: síntese por eixos (STF, TSE, mineração, PCC, P11, Master) e texto integral dos 128 dossiês, com links canônicos e fontes."
date: 2026-10-06T21:40:00-03:00
image:
  path: "/assets/img/estudos/padroes_sistemicos_dashboard_hero_xarticle.webp"
tags: [estudo, lawfare, compilado, stf, justica, censura, pcc, mineracao, corrupcao]
categories: estudos
mermaid: false
pin: false
permalink: /posts/2026-10-06-compilado-lawfare/
source_data: "compilado-lawfare-estudos"
---

- &nbsp;
{{:toc .large-only}}

"""


def main() -> None:
    posts = load_posts()
    # FRONT_MATTER uses doubled braces for the Jekyll toc line
    header = FRONT_MATTER.replace("{{:toc .large-only}}", "{:toc .large-only}")
    parts = [
        header,
        "# T-270 · Compilado Lawfare",
        "",
        f"Síntese + antologia de **{len(posts)} estudos**. "
        f"Parte A organiza a leitura. Parte B devolve o texto integral. "
        f"Página da categoria: [{SITE}/estudos/]({SITE}/estudos/).",
        "",
        "***",
        "",
        synthesis_md(posts),
        catalog_md(posts),
        "***",
        "",
        anthology_md(posts),
        "",
        "*Dossiê T-270 · CC0 · lawfare-timeline*",
        "",
    ]
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote {OUT} posts={len(posts)} bytes={OUT.stat().st_size}")


if __name__ == "__main__":
    main()
