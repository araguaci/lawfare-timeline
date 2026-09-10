# -*- coding: utf-8 -*-
"""Extrai de _data/lawfare.json as entradas sobre minérios e terras raras."""
from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"d:\ai-projects\lawfare-timeline")
SRC = ROOT / "_data" / "lawfare.json"
OUT = ROOT / "_data" / "minerios-terras-raras.json"

TERM_PATTERNS = [
    (r"terras?\s+raras?", "terras-raras"),
    (r"rare\s+earth", "terras-raras"),
    (r"min[eé]rios?", "minerio"),
    (r"minera[cç][aã]o", "mineracao"),
    (r"mineradora", "mineradora"),
    (r"mineroduto", "mineroduto"),
    (r"minerais?\s+cr[ií]ticos?", "minerais-criticos"),
    (r"ativo\s+miner", "ativo-minerario"),
    (r"licenciamento\s+mineral", "licenciamento-mineral"),
    (r"processos?\s+miner", "processo-minerario"),
    (r"pol[ií]tica\s+nacional\s+de\s+miner", "politica-mineral"),
    (r"l[ií]tio", "litio"),
    (r"ni[oó]bio", "niobio"),
    (r"grafite", "grafite"),
    (r"garimpo|garimpeir", "garimpo"),
    (r"opera[cç][aã]o\s+rejeito", "operacao-rejeito"),
    (r"top[aá]zio", "topazio"),
    (r"serra do curral", "serra-do-curral"),
    (r"serra verde", "serra-verde"),
    (r"projeto top", "projeto-topazio"),
    (r"\bgmais\b", "gmais"),
    (r"\banm\b", "anm"),
    (r"cassiterita", "cassiterita"),
    (r"t[aâ]ntalo|tantalita", "tantalo"),
    (r"bauxita", "bauxita"),
    (r"sigma lithium", "sigma-lithium"),
    (r"vale do l[ií]tio", "vale-do-litio"),
    (r"minera[cç][aã]o taboca", "taboca"),
    (r"cedro minera", "cedro-mineracao"),
    (r"poeira vermelha", "poeira-vermelha"),
    (r"usa rare earth", "usa-rare-earth"),
    (r"jogmec", "jogmec"),
    (r"\bfgam\b", "fgam"),
    (r"\bcmbc\b", "cmbc"),
    (r"pnmce", "pnmce"),
    (r"pl\s*2\.?780", "pl-2780"),
    (r"norsk hydro", "norsk-hydro"),
    (r"\bfeam\b", "feam"),
    (r"diamante negro|garimpo ilegal|minera[cç][aã]o ilegal", "garimpo-ilegal"),
    (r"certificado mineral", "certificado-mineral"),
    (r"atividade mineral", "atividade-mineral"),
    (r"direitos minerais", "direitos-minerais"),
    (r"mina-jangada|mina jangada|mina pela ema|grota do cirilo", "mina"),
]

COMPILED = [(re.compile(p, re.I), label) for p, label in TERM_PATTERNS]

# Stubs e cluster Rejeito / Serra do Curral
FORCE_INCLUDE = set(range(1547, 1551)) | set(range(1552, 1572)) | {
    33,
    430,
    649,
    1193,
    1575,
    1607,
    1653,
    1655,
    1657,
    1658,
    1659,
    1669,
    1708,
    1909,
    1912,
}

# Tema principal não é minério / terras raras
EXCLUDE = {
    1492,  # cocaína em caminhão de minério
    1551,  # stub homeschooling (vizinho numérico do cluster Rejeito)
    1713,  # memorandos Fazenda
    1718,  # WAICO / IA
    1722,  # PPP ponte Salvador
    1751,  # biotecnologia
    1754,  # Midea eletrodomésticos
    1757,  # açaí (caso-controle)
}

CORE = {
    "terras-raras",
    "minerio",
    "mineracao",
    "mineradora",
    "mineroduto",
    "minerais-criticos",
    "ativo-minerario",
    "licenciamento-mineral",
    "processo-minerario",
    "politica-mineral",
    "litio",
    "niobio",
    "grafite",
    "garimpo",
    "operacao-rejeito",
    "topazio",
    "serra-do-curral",
    "serra-verde",
    "projeto-topazio",
    "gmais",
    "anm",
    "cassiterita",
    "tantalo",
    "bauxita",
    "sigma-lithium",
    "vale-do-litio",
    "taboca",
    "cedro-mineracao",
    "poeira-vermelha",
    "usa-rare-earth",
    "jogmec",
    "fgam",
    "cmbc",
    "pnmce",
    "pl-2780",
    "norsk-hydro",
    "feam",
    "garimpo-ilegal",
    "certificado-mineral",
    "atividade-mineral",
    "direitos-minerais",
    "mina",
}


def blob_of(a: dict) -> str:
    return " ".join(
        [
            str(a.get("titulo") or ""),
            str(a.get("descricao") or ""),
            str(a.get("analise") or ""),
            str(a.get("impacto_diplomatico") or ""),
            str(a.get("tipo_escandalo") or ""),
            str(a.get("categoria") or ""),
            " ".join(str(t) for t in (a.get("tags") or [])),
            " ".join(str(x) for x in (a.get("pessoas_envolvidas") or [])),
            " ".join(str(x) for x in (a.get("instituicoes_envolvidas") or [])),
        ]
    )


def match_labels(text: str) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for rx, label in COMPILED:
        if rx.search(text) and label not in seen:
            seen.add(label)
            found.append(label)
    return found


def cluster_of(aid: int, labels: list[str], titulo: str) -> str:
    if aid == 1909 or (aid == 1912):
        return "topazio-vorcaro" if aid == 1909 else "operacao-rejeito-serra-curral"
    if aid in set(range(1547, 1551)) | set(range(1552, 1572)) or "operacao-rejeito" in labels or "serra-do-curral" in labels:
        return "operacao-rejeito-serra-curral"
    if aid in {33, 430, 649, 1607} or "garimpo" in labels or "garimpo-ilegal" in labels:
        return "garimpo-ouro-ilegal"
    if aid in range(1667, 1675) or "taboca" in labels:
        return "taboca-amazonas"
    if aid in {1655, 1657, 1658, 1659}:
        return "para-vale-hydro"
    if aid in {1575, 1653, 1714, 1715, 1716, 1717} or "usa-rare-earth" in labels:
        return "minerais-criticos-geopolitica"
    if aid in range(1696, 1713) or "pl-2780" in labels or "pnmce" in labels:
        return "pl-2780-minerais-criticos"
    if aid in range(1740, 1749) or "jogmec" in labels or aid == 1193:
        return "terras-raras-goias-diplomacia"
    if aid in range(1679, 1685) or aid == 1750 or "litio" in labels or "sigma-lithium" in labels:
        return "litio-minas-gerais"
    if "terras-raras" in labels:
        return "terras-raras"
    return "mineracao-outros"


def main() -> None:
    data = json.loads(SRC.read_text(encoding="utf-8"))
    assuntos = data.get("assuntos", [])

    extracted: list[dict] = []
    index: list[dict] = []

    for a in assuntos:
        aid = a.get("id")
        if aid in EXCLUDE:
            continue
        text = blob_of(a)
        labels = match_labels(text)
        forced = aid in FORCE_INCLUDE
        if not forced and not any(lb in CORE for lb in labels):
            continue

        item = deepcopy(a)
        extracted.append(item)
        index.append(
            {
                "id": aid,
                "titulo": a.get("titulo") or "",
                "data_evento": a.get("data_evento") or "",
                "categoria": a.get("categoria") or "",
                "labels": labels,
                "cluster": cluster_of(aid, labels, a.get("titulo") or ""),
                "incompleto": not (a.get("titulo") or "").strip(),
            }
        )

    extracted.sort(key=lambda x: (str(x.get("data_evento") or "9999"), x.get("id") or 0))
    index.sort(key=lambda x: (x["data_evento"] or "9999", x["id"] or 0))

    clusters: dict[str, list[int]] = {}
    for row in index:
        clusters.setdefault(row["cluster"], []).append(row["id"])

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out = {
        "meta": {
            "fonte": "_data/lawfare.json",
            "gerado_em": now,
            "criterio": (
                "Assuntos do corpus principal com relação a minérios, mineração, "
                "terras raras, minerais críticos, lítio, nióbio, garimpo, "
                "Operação Rejeito / Serra do Curral e Projeto Topázio. "
                "Campos originais preservados; rótulos de match só em indice."
            ),
            "total_corpus": len(assuntos),
            "total_extraidas": len(extracted),
            "ids": [e.get("id") for e in extracted],
            "ids_incompletos": [r["id"] for r in index if r["incompleto"]],
            "clusters": clusters,
        },
        "indice": index,
        "assuntos": extracted,
    }

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"extraidas={len(extracted)} arquivo={OUT}")
    for row in index:
        flag = " [STUB]" if row["incompleto"] else ""
        print(f"{row['id']}\t{row['data_evento']}\t{row['cluster']}\t{row['titulo'][:80]}{flag}")


if __name__ == "__main__":
    main()
