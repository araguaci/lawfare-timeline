#!/usr/bin/env python3
"""Exporta posts da série Vaza Toga 1–5 para _data/export-vazatoga.json.

Fonte primária: `_posts/` (pasta vazatoga + posts relacionados).
Enriquece com `lawfare.json` quando há `id_corpus` ou `fonte_arquivo` coincidente.
IDs do export-vazatoga-methodology.json (posicionais 1…N) NÃO são reutilizados.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
LAWFARE = ROOT / "_data" / "lawfare.json"
POSTS_DIR = ROOT / "_posts"
DEFAULT_OUT = ROOT / "_data" / "export-vazatoga.json"

CAPITULOS = {
    1: {
        "nome": "Vaza Toga 1 — Folha/Greenwald e gabinete paralelo",
        "nucleo": "Série Folha (ago/2024); gabinete paralelo; Tagliaferro como fonte; INQ 4781",
        "origem": "Folha de S.Paulo / Glenn Greenwald / Fábio Serapião",
    },
    2: {
        "nome": "Vaza Toga 2 — Certidões GestBio e Dia da Mulher",
        "nucleo": "Grupo Audiências de Custódia; 1.398 certidões; GestBio; arquivos do 8 de janeiro",
        "origem": "A Investigação / Civilization Works (ago/2025)",
        "ids_main": list(range(1877, 1883)),
    },
    3: {
        "nome": "Vaza Toga 3 — A fraude exposta",
        "nucleo": "Constantino/Fiuza; PM-BA; Gettr/Allan; Zambelli; Palver; atraso de veículo internacional",
        "origem": "Revista Oeste",
        "ids_main": list(range(1883, 1889)),
    },
    4: {
        "nome": "Vaza Toga 4 — Empresários e fabricação de provas",
        "nucleo": "Busca 23/08/2022; relatório Shor; Melek; Hang/Nigri; Sallorenzo vs jornalistas",
        "origem": "A Investigação / Public / Civilization Works",
        "ids_main": list(range(1869, 1874)),
    },
    5: {
        "nome": "Vaza Toga 5 — Devassa de CPFs CNJ/STF",
        "nucleo": "2.119 CPFs; PET 11228 (Dino); sigilo do Exército",
        "origem": "A Investigação / Public (ago/2026)",
        "ids_main": list(range(1874, 1877)),
    },
}

# Posts de síntese/dossiê com tag vazatoga mas sem capítulo 1–5 próprio.
EXCLUDE_STEMS = {
    "2026-04-22-golpe-brasil-analise-evidencial",
    "2026-07-21-alexandre-de-moraes-dossie-itens-mais-graves",
}

DUPLICATA_FOLHA = {
    "2024-08-01-vaza-toga-folha-de-spaulo-publica-mensagens-internas-do-tsestf": (
        "_posts/vazatoga/2024-08-01-vaza-toga-folha-publica-mensagens-internas-tse-stf.md"
    ),
}

SOURCE_CAPITULO = {
    "vazatoga2": 2,
    "vazatoga3": 3,
    "vazatoga4": 4,
    "vazatoga5": 5,
}

ID_CAPITULO = {}
for cap, spec in CAPITULOS.items():
    for i in spec.get("ids_main") or []:
        ID_CAPITULO[i] = cap

# Stems sem source_data/id de batch — classificação editorial.
STEM_CAPITULO: dict[str, tuple[int, str]] = {
    # VT1 — publicação original e desdobramentos da fonte / INQ 4781
    "2024-08-01-vaza-toga-folha-de-spaulo-publica-mensagens-internas-do-tsestf": (1, "nucleo"),
    "2024-08-01-vaza-toga-folha-publica-mensagens-internas-tse-stf": (1, "nucleo"),
    "2025-08-15-vaza-toga-expoe-gabinete-paralelo-de-alexandre-de-moraes": (1, "nucleo"),
    "2025-09-02-eduardo-tagliaferro-depoe-no-senado-sobre-operacoes-paralelas-do-gabinete-de-moraes": (
        1,
        "desdobramento",
    ),
    "2025-09-02-senado-decide-enviar-relatorio-sobre-vaza-toga-aos-eua-e-organismos-internacionais": (
        1,
        "desdobramento",
    ),
    "2025-11-09-stf-forma-maioria-para-tornar-eduardo-tagliaferro-reu-por-revelacoes-da-vaza-toga": (
        1,
        "desdobramento",
    ),
    "2025-11-13-1-turma-do-stf-torna-tagliaferro-reu-por-4-a-0": (1, "desdobramento"),
    "2025-12-01-moraes-determina-citacao-por-edital-alegando-paradeiro-desconhecido-contradicao-com-pedido-de-extradicao-anterior": (
        1,
        "desdobramento",
    ),
    "2026-03-17-audiencia-de-instrucao-realizada-sem-intimacao-regular-do-reu-testemunhos-colhidos-sem-contraditorio": (
        1,
        "desdobramento",
    ),
    "2026-03-27-moraes-reconhece-nulidade-absoluta-da-audiencia-anula-todos-os-depoimentos-colhidos": (
        1,
        "desdobramento",
    ),
    "2026-04-02-defesa-protocola-representacao-a-oab-denunciando-acusacao-de-abandono-de-causa": (
        1,
        "desdobramento",
    ),
    "2026-04-13-moraes-destitui-advogados-constituidos-e-nomeia-defensoria-publica-sub-padrao-substituicao-compulsoria-de-defesa-tecnica": (
        1,
        "desdobramento",
    ),
    "2025-10-25-jornalistas-david-agape-e-eli-vieira-sao-alvo-de-queixa-crime-no-stf-por-revelacoes-da-vaza-toga": (
        1,
        "desdobramento",
    ),
    "2025-10-30-moraes-encaminha-acao-contra-jornalistas-da-vaza-toga-a-pgr-para-analise": (
        1,
        "desdobramento",
    ),
    "2025-11-12-david-agape-denuncia-tentativa-de-criminalizar-jornalismo-investigativo-atraves-do-stf": (
        1,
        "desdobramento",
    ),
    "2026-05-29-vaza-toga-corpus-bridge": (0, "indice"),
    "2025-08-25-crise-brasil-eua-inq-4781-vaza-toga-e-sancoes": (1, "transversal"),
    # VT2 — resumos da série certidões / 8 de janeiro
    "2025-08-17-pontos-centrais": (2, "sintese"),
    "2025-08-17-resumo-detalhado-dos-arquivos-do-8-de-janeiro": (2, "sintese"),
    "2025-08-17-resumo-executivo": (2, "sintese"),
    "2025-08-17-resumo-geral-dos-arquivos-do-8-de-janeiro": (2, "sintese"),
    # VT4 — áudio Sallorenzo (mesmo núcleo empresários; id 1321)
    "2025-11-12-audio-revela-colaboradora-informal-do-tse-admitindo-ter-denunciado-empresarios": (
        4,
        "desdobramento",
    ),
}

PAPEL_POR_SOURCE = {
    2: "nucleo",
    3: "nucleo",
    4: "nucleo",
    5: "nucleo",
}


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm_raw, body = parts[1], parts[2]
    if yaml:
        fm = yaml.safe_load(fm_raw) or {}
    else:
        fm = {}
    return fm, body


def as_list(val) -> list[str]:
    if val is None:
        return []
    if isinstance(val, list):
        return [str(x) for x in val if x is not None and str(x).strip()]
    if isinstance(val, str):
        return [val] if val.strip() else []
    return [str(val)]


def as_str(val) -> str:
    if val is None:
        return ""
    if isinstance(val, list):
        return str(val[0]) if val else ""
    return str(val)


def norm_path(p: str) -> str:
    return p.replace("\\", "/").strip().lstrip("./")


def permalink_from(fm: dict, path: Path) -> str:
    pl = as_str(fm.get("permalink")).strip()
    if pl:
        return pl if pl.endswith("/") else pl + "/"
    return f"/posts/{path.stem}/"


def parse_id_corpus(raw) -> tuple[int | None, str | None, str]:
    """Retorna (id_int, thematic_id, track)."""
    s = as_str(raw).strip()
    if not s:
        return None, None, "post"
    if s.upper().startswith("T-"):
        num = re.sub(r"[^\d]", "", s)
        tid = s.upper() if s.upper().startswith("T-") else f"T-{num}"
        return (int(num) if num else None), tid, "thematic"
    if s.isdigit():
        return int(s), None, "main"
    m = re.search(r"(\d+)", s)
    if m:
        return int(m.group(1)), None, "main"
    return None, None, "post"


def extract_section_items(body: str, headings: tuple[str, ...]) -> list[str]:
    for heading in headings:
        pat = rf"###\s*{heading}\s*\n(.*?)(?=\n### |\n## |\Z)"
        m = re.search(pat, body, re.S | re.I)
        if not m:
            continue
        items = []
        for line in m.group(1).splitlines():
            line = line.strip()
            if line.startswith("- "):
                items.append(line[2:].strip())
        if items:
            return items
    return []


def extract_fontes_body(body: str) -> list[str]:
    sec = re.search(
        r"##\s*[^\n]*Fontes[^\n]*\n(.*?)(?=\n## |\Z)", body, re.S | re.I
    )
    if not sec:
        return []
    urls = re.findall(r"\((https?://[^)]+)\)", sec.group(1))
    return list(dict.fromkeys(urls))


def source_capitulo(source_data: str) -> int | None:
    s = (source_data or "").lower()
    for key, cap in SOURCE_CAPITULO.items():
        if key in s:
            return cap
    return None


def classify(stem: str, source_data: str, id_int: int | None) -> tuple[int, str]:
    cap = source_capitulo(source_data)
    if cap is not None:
        return cap, PAPEL_POR_SOURCE[cap]
    if id_int is not None and id_int in ID_CAPITULO:
        c = ID_CAPITULO[id_int]
        return c, PAPEL_POR_SOURCE[c]
    if stem in STEM_CAPITULO:
        return STEM_CAPITULO[stem]
    return 1, "desdobramento"


def load_lawfare_indexes() -> tuple[dict[int, dict], dict[str, dict]]:
    data = json.loads(LAWFARE.read_text(encoding="utf-8"))
    by_id: dict[int, dict] = {}
    by_file: dict[str, dict] = {}
    for a in data.get("assuntos", []):
        aid = a.get("id")
        if isinstance(aid, int):
            by_id[aid] = a
        fa = norm_path(str(a.get("fonte_arquivo") or ""))
        if fa:
            by_file[fa.lower()] = a
            by_file[Path(fa).name.lower()] = a
    return by_id, by_file


def is_related_post(path: Path, fm: dict) -> bool:
    if path.stem in EXCLUDE_STEMS:
        return False
    rel = path.relative_to(ROOT).as_posix()
    if "/vazatoga/" in rel or path.stem in STEM_CAPITULO:
        return True
    title = as_str(fm.get("title")).lower()
    src = as_str(fm.get("source_data")).lower()
    title_vt = "vaza toga" in title or "vazatoga" in title
    src_vt = "vazatoga" in src
    return bool(title_vt or src_vt)


def post_to_entry(
    path: Path,
    fm: dict,
    body: str,
    by_id: dict[int, dict],
    by_file: dict[str, dict],
) -> dict | None:
    if path.stem in EXCLUDE_STEMS:
        return None
    if not is_related_post(path, fm):
        return None

    rel = path.relative_to(ROOT).as_posix()
    titulo = as_str(fm.get("title")) or path.stem
    descricao = as_str(fm.get("description"))
    date_raw = as_str(fm.get("date") or "2026-01-01")
    data_evento = date_raw[:10] if len(date_raw) >= 10 else "2026-01-01"
    tags = as_list(fm.get("tags"))
    categoria = as_str(fm.get("categories")) or path.parent.name
    source_data = as_str(fm.get("source_data"))
    permalink = permalink_from(fm, path)

    id_int, thematic_id, track = parse_id_corpus(fm.get("id_corpus"))

    lf = None
    if id_int is not None and track == "main":
        lf = by_id.get(id_int)
    if lf is None:
        lf = by_file.get(rel.lower()) or by_file.get(path.name.lower())
    if lf is not None and id_int is None and isinstance(lf.get("id"), int):
        id_int = lf["id"]
        track = "main"

    cap, papel = classify(path.stem, source_data, id_int if track == "main" else None)
    if track == "thematic":
        papel = "indice"
        cap = 0

    pessoas = extract_section_items(body, ("Atores", "Pessoas"))
    instituicoes = extract_section_items(body, ("Instituicoes", "Instituições", "Instituicoes"))
    fontes = extract_fontes_body(body)

    if lf:
        if not descricao:
            descricao = as_str(lf.get("descricao"))
        if not pessoas:
            pessoas = as_list(lf.get("pessoas_envolvidas"))
        if not instituicoes:
            instituicoes = as_list(lf.get("instituicoes_envolvidas"))
        if not fontes:
            fontes = [f for f in as_list(lf.get("fontes")) if f and f != "N/A"]
        if not tags:
            tags = as_list(lf.get("tags"))

    cap_nome = (
        "Índice / transversal"
        if cap == 0
        else CAPITULOS[cap]["nome"]
    )

    entry: dict = {
        "titulo": titulo,
        "data_evento": data_evento,
        "data_iso": f"{data_evento}T12:00:00.000Z",
        "capitulo": cap,
        "capitulo_nome": cap_nome,
        "papel": papel,
        "categoria": categoria,
        "tags": tags,
        "descricao": descricao,
        "permalink": permalink,
        "fonte_arquivo": rel.replace("/", "\\"),
        "source_data": source_data or None,
        "track": track,
        "pessoas_envolvidas": pessoas,
        "instituicoes_envolvidas": instituicoes,
        "fontes": fontes,
        "pais": "Brasil",
    }

    if thematic_id:
        entry["thematic_id"] = thematic_id
        entry["id_corpus"] = thematic_id
    elif id_int is not None:
        entry["id"] = id_int
        entry["id_corpus"] = str(id_int)
    else:
        entry["id_corpus"] = None

    if lf:
        for k in ("relevancia", "prioridade", "tipo_escandalo", "impacto_diplomatico"):
            if lf.get(k) is not None:
                entry[k] = lf[k]

    dup = DUPLICATA_FOLHA.get(path.stem)
    if dup:
        entry["duplicata_de"] = dup.replace("/", "\\")

    return entry


def collect_posts() -> list[Path]:
    files = list(POSTS_DIR.rglob("*.md"))
    return sorted(files)


def build_export() -> dict:
    by_id, by_file = load_lawfare_indexes()
    assuntos: list[dict] = []

    for path in collect_posts():
        text = path.read_text(encoding="utf-8", errors="replace")
        fm, body = parse_frontmatter(text)
        entry = post_to_entry(path, fm, body, by_id, by_file)
        if entry:
            assuntos.append(entry)

    assuntos.sort(
        key=lambda a: (
            a.get("capitulo") if a.get("capitulo") != 0 else 9,
            a.get("data_evento") or "",
            a.get("id") or 0,
            a.get("fonte_arquivo") or "",
        )
    )

    por_capitulo = {str(i): 0 for i in range(0, 6)}
    for a in assuntos:
        por_capitulo[str(a.get("capitulo", 0))] += 1

    datas = [a["data_evento"] for a in assuntos if a.get("data_evento")]
    periodo = f"{min(datas)} a {max(datas)}" if datas else "N/A"

    ids_main = sorted(a["id"] for a in assuntos if a.get("track") == "main" and "id" in a)

    return {
        "serie": "Vaza Toga",
        "capitulos": {
            str(k): {kk: vv for kk, vv in v.items() if kk != "ids_main"}
            | ({"ids_main": v["ids_main"]} if "ids_main" in v else {})
            for k, v in CAPITULOS.items()
        },
        "assuntos": assuntos,
        "total": len(assuntos),
        "por_capitulo": {
            "indice_transversal": por_capitulo["0"],
            "1": por_capitulo["1"],
            "2": por_capitulo["2"],
            "3": por_capitulo["3"],
            "4": por_capitulo["4"],
            "5": por_capitulo["5"],
        },
        "data_extracao": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "periodo": periodo,
        "fonte_original": "_posts/ + _data/lawfare.json",
        "id_ranges": {
            "vt2": {"min": 1877, "max": 1882},
            "vt3": {"min": 1883, "max": 1888},
            "vt4": {"min": 1869, "max": 1873},
            "vt5": {"min": 1874, "max": 1876},
            "vt1_legado": [1262, 1299, 1303, 1304, 1312, 1316, 1320, 1321, 1322, 1405, 1409],
        },
        "ids_main": ids_main,
        "nota": (
            "Exportado a partir de _posts/ (pasta vazatoga + posts cujo título trata da série). "
            "Campo id / id_corpus = ID do corpus (lawfare.json); T-207 no track temático. "
            "Não usa IDs posicionais de export-vazatoga-methodology.json. "
            "1865–1868 (regulação de internet) não pertencem à série. "
            "Os dois posts Folha de 2024-08-01 descrevem o mesmo evento; o arquivo "
            "…do-tsestf.md está marcado como duplicata_de."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", "-o", default=str(DEFAULT_OUT.relative_to(ROOT)))
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()

    if yaml is None:
        print("Erro: PyYAML é necessário (pip install pyyaml).", file=sys.stderr)
        return 1
    if not LAWFARE.exists():
        print(f"Erro: {LAWFARE} não encontrado.", file=sys.stderr)
        return 1

    out_path = ROOT / args.output
    payload = build_export()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=None if args.compact else 2)
        f.write("\n")

    pc = payload["por_capitulo"]
    print(
        f"Exportados {payload['total']} assuntos "
        f"(VT1={pc['1']}, VT2={pc['2']}, VT3={pc['3']}, VT4={pc['4']}, VT5={pc['5']}, "
        f"indice={pc['indice_transversal']}) -> {out_path}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
