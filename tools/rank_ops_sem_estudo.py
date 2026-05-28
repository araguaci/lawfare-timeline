#!/usr/bin/env python3
"""Identifica top operações/escândalos sem estudo aprofundado."""
from __future__ import annotations

import json
import re
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "_posts"
OUT_PATHS = [
    ROOT / "_data" / "relatorio-top30-sem-estudo.md",
    ROOT / "docs" / "relatorio-top30-sem-estudo.md",
    ROOT / "artigos" / "relatorio-top30-sem-estudo.md",
]

STUDY_DIRS = ["estudos"]
OP_DIRS = ["operacoes", "escandalos", "bancos", "governo", "stf", "lawfare", "crise-diplomatica"]

# estudo slug/title keywords -> cobre operação
STUDY_COVERAGE = [
    ("compliance zero", ["compliance-zero", "compliance zero", "banco master"]),
    ("carbono oculto", ["carbono-oculto", "carbono oculto"]),
    ("narco fluxo", ["narco-fluxo", "narco fluxo", "choquei"]),
    ("greenwashing", ["greenwashing", "operacao-greenwashing"]),
    ("biomm", ["biomm", "pochmann", "fundo cartago"]),
    ("mare liberum", ["mare-liberum", "mare liberum"]),
    ("pcc", ["pcc-fluxo", "pcc portugal", "ndrangheta", "mafia italiana"]),
    ("crise diplomatica", ["crise-diplomatica", "crise diplomatica"]),
    ("reforma tributaria", ["reforma-tributaria", "captura-regulatoria"]),
    ("direita permitida", ["direita-permitida"]),
    ("biazucci", ["biazucci"]),
    ("inss", ["inss", "sem-desconto", "hydra"]),
    ("dosimetria", ["dosimetria", "lei-15402"]),
    ("faixa tropical", ["faixa-tropical"]),
    ("oliver ortiz", ["oliver-ortiz"]),
    ("penduricalhos", ["penduricalhos", "supersalarios"]),
    ("pandemia", ["pandemia-capturada"]),
    ("jbs", ["jbs-leviata"]),
    ("republica capturada", ["republica-capturada"]),
    ("emaranhamento", ["emaranhamento-operacoes"]),
    ("rejeito", ["rejeito", "serra-do-curral", "terceiro-manuscrito", "parcours", "poeira-vermelha"]),
    ("tank", ["operacao-tank", "tank-pr"]),
    ("sem desconto", ["sem-desconto", "inss"]),
    ("hydra", ["hydra", "inss"]),
    ("vaza toga", ["vazatoga", "vaza-toga"]),
    ("lava jato", ["lava-jato", "lava jato"]),
    ("satiagraha", ["satiagraha"]),
    ("castelo de areia", ["castelo-de-areia"]),
    ("custeio p11", ["custeio-administrativo", "timeline-178", "p11 orçament"]),
    ("vorcaro t192", ["vorcaro", "timeline-132", "carbono-ficticio", "creditos-de-carbono"]),
    ("sigilo gastos t193", ["timeline-177", "viagens-federais-sob-sigilo", "timeline-167", "cartao-corporativo"]),
    ("cluster p11 t194", ["timeline-174", "timeline-176", "novo-orcamento-secreto", "orcamento-secreto"]),
    ("cpi pcc t195", ["cpi-crime-organizado-mapeamento", "pcc-infiltracao-eleitoral"]),
    ("rejeito t197", ["operacao-rejeito", "serra-curral", "terceiro-manuscrito", "poeira-vermelha", "parcours-serra"]),
    ("coaf moraes t198", ["coaf-e-acao-de-moraes", "acumulacao-funcoes-moraes", "alexandre-de-moraes-solicita-novos-relatorios"]),
    ("americanas t199", ["fraude-contabil-das-lojas-americanas", "lojas-americanas"]),
    ("estatais t200", ["estatais-federais-registram-rombo", "estatais-federais"]),
    ("pcc transnacional t201", ["ofac-sanciona-diego-carmo", "eua-indicia-18-brasileiros", "cimeira-luso-brasileira"]),
    ("delegada pcc t202", ["delegada-empossada-com-governador", "flavio-dino-reintegra-candidata-delegada"]),
    ("zelotes t203", ["operacao-zelotes"]),
    ("paris cluster t204", ["olimpiadas-de-paris", "janjapalooza", "desfile-janja-em-paris"]),
    ("duplo padrao t205", ["duplo-padrao-ocupacoes-do-plenario", "timeline-1483"]),
    ("splc t206", ["splc-modelo-brasil"]),
    ("vaza toga t207", ["vazatoga", "vaza-toga", "tagliaferro", "gabinete-paralelo"]),
]

# id_corpus temático → fragmentos de slug cobertos explicitamente
THEMATIC_SLUG_FRAGMENTS: dict[str, list[str]] = {
    "T-191": ["timeline-178", "custeio-administrativo-federal"],
    "T-192": ["timeline-132", "vorcaro", "carbono-ficticio", "creditos-de-carbono"],
    "T-193": ["timeline-177", "timeline-167", "viagens-federais", "cartao-corporativo"],
    "T-194": [
        "timeline-178",
        "timeline-177",
        "timeline-167",
        "timeline-174",
        "timeline-176",
        "novo-orcamento-secreto",
    ],
    "T-195": ["cpi-crime-organizado", "pcc-infiltracao-eleitoral"],
    "T-197": [
        "operacao-rejeito",
        "serra-curral",
        "terceiro-manuscrito",
        "poeira-vermelha",
        "parcours-serra",
        "teixeira-celular",
        "feam-tac",
        "toffoli-sigilo",
        "trf6-soltura",
        "viviane-barci-defesa-kallas",
        "pad-teixeira",
        "kallas-vorcaro-desinvestimento",
    ],
    "T-198": [
        "coaf-e-acao-de-moraes",
        "acumulacao-funcoes-moraes",
        "alexandre-de-moraes-solicita-novos-relatorios",
        "moraes-suspende-lei-dosimetria",
        "sequestro-pauta-dosimetria",
    ],
    "T-199": ["fraude-contabil-das-lojas-americanas", "lojas-americanas"],
    "T-200": ["estatais-federais-registram-rombo", "estatais-federais"],
    "T-201": [
        "ofac-sanciona-diego-carmo",
        "eua-indicia-18-brasileiros-pcc",
        "cimeira-luso-brasileira",
    ],
    "T-202": ["delegada-empossada-com-governador", "flavio-dino-reintegra-candidata-delegada"],
    "T-203": ["operacao-zelotes"],
    "T-204": [
        "olimpiadas-de-paris",
        "janjapalooza-festival",
        "desfile-janja-em-paris",
        "timeline-170",
        "timeline-171",
        "timeline-172",
    ],
    "T-205": ["timeline-1483", "duplo-padrao-ocupacoes-do-plenario"],
    "T-206": ["splc-modelo-brasil"],
    "T-207": [
        "vaza-toga",
        "vazatoga",
        "tagliaferro",
        "gabinete-paralelo",
        "inq-4781",
        "jornalistas-david-agape",
    ],
}


def slugify(t: str) -> str:
    t = unicodedata.normalize("NFD", t).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[-\s]+", "-", re.sub(r"[^\w\s-]", "", t.lower())).strip("-")[:80]


def post_url(path: str, fm: dict) -> str:
    """URL pública alinhada ao Chirpy: permalink explícito ou /posts/:basename/."""
    permalink = fm.get("permalink", "").strip()
    if permalink:
        return permalink if permalink.startswith("/") else f"/{permalink}"
    stem = Path(path).stem
    return f"/posts/{stem}/"


def parse_fm(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    block = text[3:end]
    out: dict = {}
    for line in block.splitlines():
        m = re.match(r"^(\w[\w-]*):\s*(.+)$", line.strip())
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return out


def load_posts(subdirs: list[str]) -> list[dict]:
    items = []
    for d in subdirs:
        for p in (POSTS / d).glob("*.md") if (POSTS / d).is_dir() else []:
            text = p.read_text(encoding="utf-8", errors="replace")
            fm = parse_fm(text)
            body = text[text.find("\n---", 3) + 4 :] if text.startswith("---") else text
            items.append(
                {
                    "path": p.relative_to(ROOT).as_posix(),
                    "category": d,
                    "title": fm.get("title", p.stem),
                    "tags": fm.get("tags", ""),
                    "id_corpus": fm.get("id_corpus", ""),
                    "date": fm.get("date", "")[:10],
                    "body": body.lower(),
                    "slug": p.stem,
                    "url": post_url(p.name, fm),
                }
            )
    return items


def study_text_blob(studies: list[dict]) -> str:
    return " ".join(s["title"].lower() + " " + s["slug"] + " " + s["body"][:3000] for s in studies)


def linked_post_slugs(studies: list[dict]) -> set[str]:
    slugs: set[str] = set()
    for s in studies:
        for m in re.finditer(r"/posts/([^/)#\s]+)/", s["body"]):
            slugs.add(m.group(1))
    return slugs


def thematic_coverage(item: dict, studies: list[dict]) -> tuple[bool, str]:
    slug = item["slug"]
    for study in studies:
        tid = (study.get("id_corpus") or "").strip()
        if not tid.startswith("T-"):
            continue
        frags = THEMATIC_SLUG_FRAGMENTS.get(tid, [])
        if any(f in slug for f in frags):
            return True, tid
    return False, ""


def has_study(item: dict, blob: str, linked: set[str], studies: list[dict]) -> tuple[bool, str]:
    if item["slug"] in linked:
        return True, "link-estudo"
    ok, by = thematic_coverage(item, studies)
    if ok:
        return True, by
    title = item["title"].lower()
    slug = item["slug"]
    combined = f"{title} {slug} {item['body'][:2000]}"

    def has_kw(text: str, kw: str) -> bool:
        if kw in slug or kw.replace(" ", "-") in slug:
            return True
        return bool(re.search(rf"\b{re.escape(kw)}\b", text))

    for label, kws in STUDY_COVERAGE:
        if any(has_kw(combined, k) for k in kws):
            if any(has_kw(blob, k) for k in kws):
                return True, label

    return False, ""


def score(item: dict) -> float:
    s = 0.0
    text = (item["title"] + " " + item["body"][:4000]).lower()
    tags = item["tags"].lower()

    # padrões sistêmicos
    for p in ["p11", "p08", "p07", "p06", "p05", "p03", "p01"]:
        if p.upper() in tags or p in text:
            s += {"p11": 12, "p08": 10, "p07": 9, "p06": 8, "p05": 7, "p03": 6, "p01": 5}.get(p, 3)

    # valores monetários
    for m in re.finditer(r"r\$\s*([\d.,]+)\s*(bi|milh|mil|mi|tril)", text):
        val, unit = m.group(1), m.group(2)
        num = float(val.replace(".", "").replace(",", "."))
        if "tril" in unit:
            s += 25
        elif "bi" in unit:
            s += min(20, num * 2)
        elif "mi" in unit or "milh" in unit:
            s += min(12, num / 100)

    keywords = {
        "sigilo": 8,
        "stf": 6,
        "toffoli": 6,
        "moraes": 5,
        "preso": 4,
        "preventiva": 4,
        "lavagem": 7,
        "pcc": 8,
        "ndrangheta": 7,
        "fgc": 8,
        "rombo": 7,
        "captura": 5,
        "fraude": 6,
        "bilh": 5,
        "desmantela": 6,
        "rejeito": 9,
        "compliance zero": 9,
        "carbono oculto": 9,
        "inss": 8,
        "anm": 5,
        "cvm": 4,
        "vorcaro": 6,
        "mineracao": 5,
        "serra do curral": 8,
        "manuscrito": 7,
    }
    for kw, pts in keywords.items():
        if kw in text:
            s += pts

    if item["category"] == "operacoes":
        s += 3
    if item["category"] == "escandalos":
        s += 2

    # recência
    if item["date"] >= "2025-01-01":
        s += 4
    if item["date"] >= "2026-01-01":
        s += 3

    return round(s, 1)


def main():
    studies = load_posts(STUDY_DIRS)
    ops = load_posts(OP_DIRS)
    blob = study_text_blob(studies)
    linked = linked_post_slugs(studies)
    today = date.today().isoformat()

    excluded_recent: list[dict] = []
    ranked = []
    for item in ops:
        covered, by = has_study(item, blob, linked, studies)
        if covered:
            excluded_recent.append({**item, "score": score(item), "covered_by": by})
            continue
        ranked.append({**item, "score": score(item), "covered_by": by})

    ranked.sort(key=lambda x: x["score"], reverse=True)
    excluded_recent.sort(key=lambda x: x["score"], reverse=True)
    top = ranked[:30]

    lines = [
        "# Top 30 — Operações e escândalos sem estudo aprofundado",
        "",
        f"**Gerado em:** {today}  ",
        "**Critério:** posts em `operacoes/`, `escandalos/` e afins **sem** dossiê correspondente em `estudos/`  ",
        "**Score:** padrões P01–P11, valores R$, keywords institucionais, recência",
        "",
        "## Cobertura temática recente (excluídos do ranking)",
        "",
        "Episódios cobertos por estudos **T-191–T-207** (mai/2026):",
        "",
        "| Estudo | Escopo |",
        "| --- | --- |",
        "| [T-191](/posts/2026-05-27-custeio-administrativo-federal-p11/) | Custeio federal P11 · timeline 178 |",
        "| [T-192](/posts/2026-05-28-vorcaro-triangulo-carbono-mineracao-banco/) | Vorcaro / carbono fictício · timeline 132 |",
        "| [T-193](/posts/2026-05-28-viagens-gastos-sigilo-complemento-p11/) | Viagens sigilo · cartão corporativo |",
        "| [T-194](/posts/2026-05-28-maquina-gastos-p11-indice-cluster/) | Índice cluster P11 (178, 177, 167, 174, 176, orçamento secreto) |",
        "| [T-195](/posts/2026-05-28-cpi-crime-organizado-pcc-infiltracao-eleitoral/) | CPI CO × PCC eleitoral |",
        "| [T-197](/posts/2026-05-28-operacao-rejeito-serra-curral-manuscritos/) | Operação Rejeito cluster 1552–1571 |",
        "| [T-198](/posts/2026-05-28-coaf-moraes-acumulacao-funcoes-dosimetria/) | COAF × Moraes · acumulação dosimetria |",
        "| [T-199](/posts/2026-05-28-fraude-lojas-americanas-risco-sacado/) | Fraude Lojas Americanas · risco sacado |",
        "| [T-200](/posts/2026-05-28-estatais-rombo-p11-complemento/) | Estatais rombo P11 · complemento cluster |",
        "| [T-201](/posts/2026-05-28-pcc-transnacional-ofac-eua-luso/) | PCC transnacional OFAC/EUA/luso |",
        "| [T-202](/posts/2026-05-29-delegada-pcc-infiltracao-institucional-sp/) | Delegada × PCC SP |",
        "| [T-203](/posts/2026-05-29-operacao-zelotes-carf-captura-fiscal/) | Operação Zelotes CARF |",
        "| [T-204](/posts/2026-05-29-gastos-paris-cluster-extravagancia-janja/) | Gastos Paris cluster |",
        "| [T-205](/posts/2026-05-29-duplo-padrao-judicial-corpus-bridge/) | Duplo padrão judicial · T-143 |",
        "| [T-206](/posts/2026-05-29-splc-modelo-brasil-corpus-bridge/) | SPLC modelo Brasil · T-129 |",
        "| [T-207](/posts/2026-05-29-vaza-toga-corpus-bridge/) | Vaza Toga INQ 4781 · T-108 |",
        "",
    ]
    if excluded_recent:
        lines.append(f"**{len(excluded_recent)}** posts timeline excluídos por cobertura (top scores entre excluídos):")
        lines.append("")
        for x in excluded_recent[:12]:
            lines.append(
                f"- {x['covered_by']} · score {x['score']} — [{x['title'][:60]}]({x['url']})"
            )
        lines.append("")

    lines.extend(["## Alertas críticos (score ≥ 40)", ""])

    critical = [x for x in top if x["score"] >= 40]
    for c in critical:
        lines.append(f"- **🔴 ID {c['id_corpus'] or '—'} · score {c['score']}** — [{c['title'][:70]}]({c['url']})")

    lines.extend(["", "## Ranking completo", "", "| # | Score | ID | Categoria | Título | Post |", "| ---: | ---: | --- | --- | --- | --- |"])

    for i, r in enumerate(top, 1):
        url = r["url"]
        title = r["title"].replace("|", "\\|")[:65]
        alert = "🔴" if r["score"] >= 40 else ("🟠" if r["score"] >= 25 else "🟡")
        lines.append(
            f"| {i} | {alert} {r['score']} | {r['id_corpus'] or '—'} | {r['category']} | {title} | [link]({url}) |"
        )

    lines.extend(
        [
            "",
            "## Legenda",
            "",
            "| Alerta | Score |",
            "| --- | --- |",
            "| 🔴 Crítico | ≥ 40 |",
            "| 🟠 Alto | 25–39 |",
            "| 🟡 Médio | < 25 |",
            "",
            "## Estudos existentes (referência de cobertura)",
            "",
            f"Total em `estudos/`: **{len(studies)}** artigos analisados como base de exclusão.",
            "",
            "Radar consolidado: [T-196 Top 30 lacunas](/posts/2026-05-28-top30-alertas-criticos-operacoes-sem-dossie/).",
            "",
            "---",
            "",
            "*Gerado por `tools/rank_ops_sem_estudo.py`*",
        ]
    )

    text = "\n".join(lines)
    for out in OUT_PATHS:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")

    print(json.dumps([{"rank": i + 1, "score": t["score"], "id": t["id_corpus"], "title": t["title"], "path": t["path"]} for i, t in enumerate(top)], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
