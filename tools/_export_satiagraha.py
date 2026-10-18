# -*- coding: utf-8 -*-
"""Exporta o que o repositório tem sobre Operação Satiagraha, com fontes."""
from __future__ import annotations

import json
import re
from datetime import date, datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_data" / "export-satiagraha.json"
PAT = re.compile(r"satiagraha|satyagraha", re.I)
SKIP_URL = re.compile(
    r"google\.com/search|perplexity\.ai|wikipedia\.org/w/index\.php\?search|"
    r"fonts\.googleapis|fonts\.gstatic|gosurf\.site/counter"
)


def clean_url(u: str) -> str:
    return u.rstrip(").,];\"'")


def is_real_url(u: str) -> bool:
    if not u or not u.startswith("http"):
        return False
    if u in ("N/A", "n/a"):
        return False
    if SKIP_URL.search(u):
        return False
    return True


def norm_fontes(raw) -> list[dict]:
    out: list[dict] = []
    seen: set[str] = set()
    if raw is None:
        return out
    if isinstance(raw, str):
        raw = [raw]
    for item in raw:
        if isinstance(item, dict):
            url = clean_url(str(item.get("url") or item.get("href") or ""))
            titulo = item.get("titulo") or item.get("title") or item.get("texto") or url
        else:
            url = clean_url(str(item))
            titulo = url
        if url in ("N/A", "n/a", ""):
            continue
        if url.startswith("http") and not is_real_url(url):
            continue
        key = url or str(titulo)
        if key in seen:
            continue
        seen.add(key)
        rec = {"titulo": titulo, "url": url} if url.startswith("http") else {"titulo": str(titulo)}
        out.append(rec)
    return out


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def strip_tags(html: str) -> str:
    txt = re.sub(r"<br\s*/?>", "\n", html, flags=re.I)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = re.sub(r"&nbsp;", " ", txt)
    txt = re.sub(r"&mdash;", "—", txt)
    txt = re.sub(r"&emdash;", "—", txt)
    txt = re.sub(r"&amp;", "&", txt)
    txt = re.sub(r"\s+", " ", txt)
    return txt.strip()


def parse_satiagraha_html(path: Path) -> dict:
    html = path.read_text(encoding="utf-8")
    cronologia = []
    for m in re.finditer(
        r'<div class="tl-item"[^>]*>.*?class="tl-date">(?P<data>.*?)</span>.*?'
        r'class="tl-badge[^"]*">(?P<fase>.*?)</span>.*?'
        r'class="tl-title">(?P<titulo>.*?)</span>.*?'
        r'<div class="tl-body">(?P<body>.*?)</div>\s*</div>',
        html,
        re.S,
    ):
        body_html = m.group("body")
        paras = [strip_tags(p) for p in re.findall(r"<p>(.*?)</p>", body_html, re.S)]
        quotes = [strip_tags(q) for q in re.findall(r'class="highlight">(.*?)</div>', body_html, re.S)]
        cronologia.append(
            {
                "data": strip_tags(m.group("data")),
                "fase": strip_tags(m.group("fase")),
                "titulo": strip_tags(m.group("titulo")),
                "texto": paras,
                "citacoes_internas": quotes,
            }
        )
    personagens = []
    for m in re.finditer(
        r'<div class="node-card[^"]*">.*?<div class="node-id">(?P<nid>.*?)</div>.*?'
        r'<div class="node-name">(?P<nome>.*?)</div>.*?'
        r'<div class="node-role">(?P<papel>.*?)</div>.*?'
        r'<div class="node-tags">(?P<tags>.*?)</div>.*?'
        r'<div class="node-detail">(?P<detalhe>.*?)</div>',
        html,
        re.S,
    ):
        tags = [strip_tags(t) for t in re.findall(r'class="node-tag">(.*?)</span>', m.group("tags"), re.S)]
        personagens.append(
            {
                "id_interno": strip_tags(m.group("nid")),
                "nome": strip_tags(m.group("nome")),
                "papel": strip_tags(m.group("papel")),
                "marcadores": tags,
                "detalhe": strip_tags(m.group("detalhe")),
            }
        )
    crimes = []
    for m in re.finditer(
        r'<div class="crime-title">(?P<t>.*?)</div>\s*<div class="crime-desc">(?P<d>.*?)</div>',
        html,
        re.S,
    ):
        crimes.append({"titulo": strip_tags(m.group("t")), "descricao": strip_tags(m.group("d"))})
    rodape = re.search(r'<span>FONTES:\s*(.*?)</span>', html)
    fontes_rodape = []
    if rodape:
        fontes_rodape = [x.strip() for x in strip_tags(rodape.group(1)).split("·") if x.strip()]
    return {
        "arquivo": "artigos/satiagraha.html",
        "espelho_docs": "docs/artigos/satiagraha.html",
        "titulo": "Mapa Mental — Operação Satiagraha & Gilmar Mendes",
        "periodo": "2004–2015",
        "nota_fontes": (
            "O HTML não embute URLs nas fichas. O rodapé cita veículos sem link. "
            "As URLs verificáveis estão nos posts e no export de 15/04/2026."
        ),
        "fontes_citadas_no_rodape": fontes_rodape,
        "cronologia": cronologia,
        "personagens": personagens,
        "crimes_investigados": crimes,
    }


def md_urls(text: str) -> list[str]:
    urls = re.findall(r"https?://[^\s\)\]\>\"']+", text)
    return [clean_url(u) for u in urls if is_real_url(clean_url(u))]


def main() -> None:
    lf = load_json(ROOT / "_data" / "lawfare.json")
    hist = load_json(ROOT / "_data" / "lawfare-export-timeline-15abr2026.json")
    if isinstance(hist, dict):
        hist_items = hist.get("entradas") or hist.get("assuntos") or hist.get("timeline") or []
        if not hist_items:
            for v in hist.values():
                if isinstance(v, list) and v and isinstance(v[0], dict) and "titulo" in v[0]:
                    hist_items = v
                    break
    else:
        hist_items = hist

    principais = []
    mencoes = []
    for a in lf["assuntos"]:
        blob = json.dumps(a, ensure_ascii=False)
        if not PAT.search(blob):
            titulo = a.get("titulo") or ""
            if titulo not in (
                "Operação Satiagraha",
                "Caso Daniel Dantas - Opportunity",
                "Escândalo Daniel Dantas",
                "Habeas Corpus para Daniel Dantas",
            ):
                continue
        rec = {
            "id_corpus": a.get("id"),
            "titulo": a.get("titulo"),
            "data_evento": a.get("data_evento"),
            "categoria": a.get("categoria"),
            "descricao": a.get("descricao"),
            "tags": a.get("tags") or [],
            "pessoas_envolvidas": a.get("pessoas_envolvidas") or [],
            "instituicoes_envolvidas": a.get("instituicoes_envolvidas") or [],
            "fonte_arquivo": a.get("fonte_arquivo"),
            "fontes": norm_fontes(a.get("fontes")),
            "origem": "_data/lawfare.json",
        }
        if a.get("id") in (281, 291, 292) or (a.get("titulo") or "").lower().startswith("operação satiagraha"):
            principais.append(rec)
        elif PAT.search(a.get("titulo") or "") or PAT.search((a.get("descricao") or "")[:200]):
            if "paralelo" in (a.get("descricao") or "").lower() or "mare liberum" in (a.get("titulo") or "").lower():
                rec["papel"] = "mencao_comparativa"
                mencoes.append(rec)
            else:
                principais.append(rec)
        else:
            rec["papel"] = "mencao_comparativa"
            mencoes.append(rec)

    posts = [
        ROOT / "_posts" / "operacoes" / "2008-07-08-operacao-satiagraha.md",
        ROOT / "_posts" / "bancos" / "2008-07-08-caso-daniel-dantas-opportunity.md",
        ROOT / "_posts" / "decano" / "2008-07-01-habeas-corpus-para-daniel-dantas.md",
        ROOT / "_posts" / "decano" / "2026-07-21-gilmar-mendes-dossie-itens-mais-graves.md",
        ROOT / "_posts" / "estudos" / "2026-04-02-emaranhamento-operacoes.md",
    ]
    posts_export = []
    for p in posts:
        if not p.is_file():
            continue
        text = p.read_text(encoding="utf-8")
        if p.name != "2008-07-08-operacao-satiagraha.md" and not PAT.search(text):
            continue
        posts_export.append(
            {
                "arquivo": str(p.relative_to(ROOT)).replace("\\", "/"),
                "titulo": (re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', text, re.M) or [None, p.stem])[1],
                "fontes": norm_fontes(md_urls(text)),
            }
        )

    hc = load_json(ROOT / "_data" / "processados" / "gilmar-mendes-hc.json")
    hc_entry = None
    for year, items in hc.items():
        if not isinstance(items, list):
            continue
        for it in items:
            if PAT.search(json.dumps(it, ensure_ascii=False)):
                hc_entry = {
                    "titulo": it.get("titulo"),
                    "data": it.get("data"),
                    "descricao": it.get("descricao"),
                    "envolvidos": it.get("envolvidos"),
                    "fontes": norm_fontes(it.get("fonte")),
                    "origem": "_data/processados/gilmar-mendes-hc.json",
                }

    historico = []
    for it in hist_items:
        if not isinstance(it, dict):
            continue
        if not PAT.search(json.dumps(it, ensure_ascii=False)):
            continue
        fontes = norm_fontes(it.get("fontes"))
        titulo_l = (it.get("titulo") or "").lower()
        eh_ficha = (
            it.get("id") in (1425, 1426)
            or "satiagraha" in titulo_l
            or ("dantas" in titulo_l and ("habeas" in titulo_l or "opportunity" in titulo_l or "prot" in titulo_l))
        )
        if not eh_ficha:
            continue
        historico.append(
            {
                "id_no_export_15abr2026": it.get("id"),
                "titulo": it.get("titulo"),
                "data_evento": it.get("data_evento"),
                "descricao": it.get("descricao"),
                "pessoas_envolvidas": it.get("pessoas_envolvidas"),
                "instituicoes_envolvidas": it.get("instituicoes_envolvidas"),
                "fontes": fontes,
                "nota": (
                    "Estes IDs (1425/1426) foram reutilizados depois em Mare Liberum no lawfare.json atual. "
                    "A ficha Satiagraha com URLs Conjur/O Globo/G1 sobrevive só neste export histórico."
                ),
                "origem": "_data/lawfare-export-timeline-15abr2026.json",
            }
        )

    dossie = parse_satiagraha_html(ROOT / "artigos" / "satiagraha.html")

    catalog: dict[str, dict] = {}

    def add_fonte(f: dict, onde: str) -> None:
        url = f.get("url") or f.get("titulo")
        if not url:
            return
        rec = catalog.setdefault(url, {"titulo": f.get("titulo") or url, "url": f.get("url"), "aparece_em": []})
        if onde not in rec["aparece_em"]:
            rec["aparece_em"].append(onde)

    for rec in principais + mencoes:
        for f in rec.get("fontes") or []:
            add_fonte(f, f"lawfare.json#{rec.get('id_corpus')}")
    for rec in posts_export:
        for f in rec.get("fontes") or []:
            add_fonte(f, rec["arquivo"])
    if hc_entry:
        for f in hc_entry.get("fontes") or []:
            add_fonte(f, "gilmar-mendes-hc.json")
    for rec in historico:
        for f in rec.get("fontes") or []:
            add_fonte(f, f"export-15abr2026#{rec.get('id_no_export_15abr2026')}")

    # fontes dos posts dedicados aplicadas à ficha 292 (corpus tem N/A)
    post_op = next((p for p in posts_export if "operacao-satiagraha" in p["arquivo"]), None)
    if post_op:
        for rec in principais:
            if rec.get("id_corpus") == 292 and not rec["fontes"]:
                rec["fontes"] = post_op["fontes"]
                rec["fontes_origem"] = post_op["arquivo"]
    if hc_entry:
        principais.append(
            {
                "id_corpus": None,
                "titulo": hc_entry["titulo"],
                "data_evento": hc_entry["data"],
                "categoria": "decano",
                "descricao": hc_entry["descricao"],
                "pessoas_envolvidas": hc_entry["envolvidos"],
                "fontes": hc_entry["fontes"],
                "origem": hc_entry["origem"],
                "fonte_arquivo": "_posts/decano/2008-07-01-habeas-corpus-para-daniel-dantas.md",
            }
        )

    payload = {
        "meta": {
            "titulo": "Export Operação Satiagraha",
            "gerado_em": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "data_local": date.today().isoformat(),
            "escopo": (
                "Tudo que o repositório lawfare-timeline já contém sobre a Operação Satiagraha "
                "e o eixo Dantas/Opportunity/HC Gilmar, com as fontes que existem no projeto. "
                "Não inventa URLs. Menções comparativas (Mare Liberum etc.) vão à parte."
            ),
            "totais": {
                "entradas_principais": len(principais),
                "entradas_historicas_com_url": len(historico),
                "mencoes_comparativas": len(mencoes),
                "posts": len(posts_export),
                "eventos_dossie_html": len(dossie["cronologia"]),
                "fontes_unicas_com_url": sum(1 for v in catalog.values() if v.get("url")),
            },
        },
        "fontes_catalogo": sorted(catalog.values(), key=lambda x: (x.get("url") or x.get("titulo") or "")),
        "entradas_principais": principais,
        "entradas_historicas_15abr2026": historico,
        "dossie_html": dossie,
        "posts": posts_export,
        "mencoes_comparativas": mencoes,
        "arquivos_do_projeto": [
            "_posts/operacoes/2008-07-08-operacao-satiagraha.md",
            "_posts/bancos/2008-07-08-caso-daniel-dantas-opportunity.md",
            "_posts/decano/2008-07-01-habeas-corpus-para-daniel-dantas.md",
            "_posts/decano/2026-07-21-gilmar-mendes-dossie-itens-mais-graves.md",
            "artigos/satiagraha.html",
            "docs/artigos/satiagraha.html",
            "docs/posts/operacao-satiagraha/index.html",
            "docs/posts/caso-daniel-dantas-opportunity/index.html",
            "docs/posts/2008-07-01-habeas-corpus-para-daniel-dantas/index.html",
            "docs/tags/satiagraha/index.html",
            "_data/lawfare.json (id 281, 291, 292)",
            "_data/lawfare-export-timeline-15abr2026.json (fichas 1425/1426 históricas)",
            "_data/processados/gilmar-mendes-hc.json",
            "_data/export-operacoes-methodology.json",
            "_data/operacoes-policiais.md",
        ],
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK {OUT} fontes={payload['meta']['totais']}")


if __name__ == "__main__":
    main()
