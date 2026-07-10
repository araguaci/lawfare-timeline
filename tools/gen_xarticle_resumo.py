#!/usr/bin/env python3
"""Gera X Article resumo de posts desde 2026-05-26."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "_data" / "posts-since-2026-05-26.json").read_text(encoding="utf-8"))
BASE = "https://lawfare-timeline.vercel.app"

SECTIONS = [
    ("lawfare", "Lawfare — STF, Bolsonaro e dosimetria seletiva", (
        "Nove entradas documentam o cluster Moraes/Bolsonaro entre maio e julho/2026: "
        "pedido de inclusão de Jair e Flávio no inquérito Eduardo (ID 1619), condenação "
        "de Eduardo por coação (1614), negativa de diligências a Flávio (1615–1616), "
        "prorrogação indeterminada da domiciliar de Jair (1617) e interrogatório de Flávio "
        "a cinco meses da eleição (1618). O estudo T-221 formaliza a preliminar *nemo judex "
        "in causa propria* arguida pela DPU na AP 2782."
    )),
    ("crise-diplomatica", "Crise diplomática Brasil–EUA", (
        "Designação SDGT imediata e FTO com vigência em 05/06/2026; publicação no Federal "
        "Register criminaliza suporte material a PCC e CV nos EUA. Complementa o dossiê "
        "T-1512 e o estudo macro da escalada bilateral (Magnitsky, Rumble, ICE, vistos)."
    )),
    ("operacoes", "Operações em campo", (
        "Seis episódios: terceiro manuscrito Rejeito (Vale/Gerdau/Trafigura), Infiltrados "
        "(DISE Campinas), Compliance Zero 9ª fase (Jaques Wagner), garimpo CV em Sararé, "
        "sanções OFAC contra Shimada/Victory Trading e divergência pública da PF com o Tesouro dos EUA."
    )),
    ("bancos", "Bancos e ecossistema Vorcaro", (
        "Delação rejeitada citando US$30 mi a Alcolumbre, quebra de sigilo Ciro Nogueira/Hugo Motta, "
        "vínculo da namorada do diretor-geral da PF com escritório do ecossistema Vorcaro."
    )),
    ("escandalos", "Escândalos e infraestrutura", (
        "Bloqueio seletivo documentado em operadoras no ano eleitoral 2026; Victory Trading "
        "(OFAC) recebeu R$ 514,5 mi da Wave Intermediações (rede Arpar)."
    )),
    ("estudos_p11", "Estudos — Cluster P11 (orçamento e captura)", (
        "T-189 (reforma tributária), T-191 (R$ 32,4 bi custeio federal), T-193 (viagens sob sigilo), "
        "T-194 (índice cluster), T-200 (rombo estatais), T-203 (Zelotes/CARF), T-204 (Paris/Janja), "
        "T-199 (Americanas R$ 25,3 bi, zero condenações)."
    )),
    ("estudos_narco", "Estudos — Narco, mineração e vetores transnacionais", (
        "T-192 (triângulo Vorcaro), T-195 (CPI crime organizado), T-197 (Rejeito/manuscritos), "
        "T-201 (PCC transnacional OFAC), T-202 (delegada × PCC), T-218 (ouro ilegal P08), "
        "T-220 (convergência PCC-OFAC × Arpar × INSS)."
    )),
    ("estudos_corpus", "Estudos — Pontes de corpus e índices", (
        "T-180 (TSE seletividade), T-196 (radar top 30 sem dossiê), T-198 (COAF × Moraes), "
        "T-205–T-209 (duplo padrão, SPLC, Vaza Toga, narrativa vs evidência, JustiçaWatch), "
        "T-214 (Sepse), T-215 (prisão Vorcaro 3×1), T-216–T-217 (TSE-USAID, seletividade TSE/Câmara)."
    )),
    ("estudos_outros", "Estudos — Outros", (
        "Caso Biazucci (CIDH), crise diplomática 2025–2026 (estudo), T-1512 (designação terrorista)."
    )),
]

# Map estudos to sub-sections
ESTUDO_MAP = {
    "T-189": "estudos_p11", "T-191": "estudos_p11", "T-193": "estudos_p11",
    "T-194": "estudos_p11", "T-200": "estudos_p11", "T-203": "estudos_p11",
    "T-204": "estudos_p11", "T-199": "estudos_p11",
    "T-192": "estudos_narco", "T-195": "estudos_narco", "T-197": "estudos_narco",
    "T-201": "estudos_narco", "T-202": "estudos_narco", "T-218": "estudos_narco",
    "T-220": "estudos_narco",
    "T-180": "estudos_corpus", "T-196": "estudos_corpus", "T-198": "estudos_corpus",
    "T-205": "estudos_corpus", "T-206": "estudos_corpus", "T-207": "estudos_corpus",
    "T-208": "estudos_corpus", "T-209": "estudos_corpus", "T-214": "estudos_corpus",
    "T-215": "estudos_corpus", "T-216": "estudos_corpus", "T-217": "estudos_corpus",
    "T-221": "estudos_corpus",
}

by_section: dict[str, list] = {s[0]: [] for s in SECTIONS}
for item in DATA["items"]:
    cat = item["cat"]
    tid = item.get("id", "")
    if cat == "estudos":
        key = ESTUDO_MAP.get(tid, "estudos_outros")
        by_section[key].append(item)
    elif cat in by_section:
        by_section[cat].append(item)
    else:
        by_section.setdefault("estudos_outros", []).append(item)


def fmt_entry(it: dict) -> str:
    title = it["title"]
    tid = it.get("id", "")
    if tid and not title.startswith(tid):
        label = f"**{tid}** · {title}"
    elif tid:
        label = f"**{tid}** · {title[len(tid):].lstrip(' ·')}"
    else:
        label = title
    url = BASE + it["url"]
    desc = it.get("desc", "").strip()
    line = f"- [{label}]({url}) — *{it['date']}*"
    if desc:
        line += f"\n  {desc}"
    return line


lines = [
    "# 53 entradas em 6 semanas: o que o LAWFARE Timeline documentou desde 26/05/2026",
    "",
    "Entre 26 de maio e 7 de julho de 2026, o projeto [LAWFARE Timeline](https://lawfare-timeline.vercel.app/) "
    "publicou **53 entradas** — 31 estudos, 9 lawfare, 6 operações, 3 bancos, 2 crise diplomática, 2 escândalos. "
    "Não é acúmulo aleatório: três eixos se repetem com densidade incomum.",
    "",
    "Primeiro, **captura orçamentária sem crime identificável** (P11): R$ 32,4 bilhões em custeio federal, "
    "viagens sob sigilo, estatais em rombo recorde, CARF capturado na Zelotes, Americanas com R$ 25,3 bi "
    "de fraude e zero condenações.",
    "",
    "Segundo, **narco-financeiro transnacional**: designação SDGT/FTO de PCC e CV, sanções OFAC contra "
    "Shimada/Victory Trading, garimpo CV na Amazônia, triângulo Vorcaro-carbono-mineração-banco, "
    "terceiro manuscrito ligando minério ilegal a Vale e Gerdau.",
    "",
    "Terceiro, **lawfare com calendário eleitoral**: cluster Bolsonaro (1613–1619), *nemo judex* formalizado "
    "pela DPU (T-221), COAF acumulando funções com Moraes (T-198), imprensa deslocando FTO para \"soberania\" (P04b).",
    "",
    "> O corpus não pede concordância. Pede rastreabilidade: data, ator, documento, padrão.",
    "> — Metodologia LAWFARE Timeline",
    "",
    "## O mapa em números",
    "",
    f"- **Total:** {DATA['total']} entradas (26/05–07/07/2026)",
    f"- **Estudos:** {DATA['by_cat']['estudos']} (T-180 a T-221, índices e dossiês)",
    f"- **Lawfare:** {DATA['by_cat']['lawfare']} (IDs 1608, 1613–1619)",
    f"- **Operações:** {DATA['by_cat']['operacoes']}",
    f"- **Bancos:** {DATA['by_cat']['bancos']}",
    f"- **Crise diplomática:** {DATA['by_cat']['crise-diplomatica']}",
    f"- **Escândalos:** {DATA['by_cat']['escandalos']}",
    "",
]

for key, title, intro in SECTIONS:
    items = by_section.get(key, [])
    if not items:
        continue
    lines.append(f"## {title}")
    lines.append("")
    lines.append(intro)
    lines.append("")
    for it in items:
        lines.append(fmt_entry(it))
        lines.append("")

lines.extend([
    "## Padrões que atravessam o período",
    "",
    "**P03** — STF/TSE como chokepoint: seletividade em inelegibilidade (T-180), negativa de diligências, "
    "dosimetria acumulada (COAF T-198).",
    "",
    "**P04b** — Enquadramento midiático desloca fatos para soberania: designação PCC/CV, divergência PF vs. Tesouro.",
    "",
    "**P08** — Infiltração em fintechs e ouro ilegal: T-218, OFAC, Victory Trading, BK Bank no corpus maior.",
    "",
    "**P10** — Infraestrutura compartilhada: mesma rede financeira serve cleptocracia e narco (T-220).",
    "",
    "**P11** — Extração via orçamento público sem ilícito individualizado: cluster T-191–T-194, T-200.",
    "",
    "## Como usar este índice",
    "",
    "Cada link aponta para a entrada completa no site, com fontes primárias, tags de padrão e conexões "
    "no grafo do corpus. O radar T-196 mantém ranking vivo das operações ainda sem dossiê — "
    "ferramenta editorial, não lista de culpados.",
    "",
    "## Fontes",
    "",
    "- [LAWFARE Timeline](https://lawfare-timeline.vercel.app/) — corpus aberto, atualizado continuamente",
    "- Entradas individuais linkadas nas seções acima (26/05/2026 – 07/07/2026)",
    "",
    "*Dossiê completo: [https://lawfare-timeline.vercel.app/](https://lawfare-timeline.vercel.app/)*",
])

out = ROOT / "artigos" / "lawfare-timeline-maio-julho-2026-xarticle.md"
out.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {out} ({len(lines)} lines)")
