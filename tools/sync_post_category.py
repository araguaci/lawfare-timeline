#!/usr/bin/env python3
"""Sincroniza categoria/tags/fonte_arquivo de posts Jekyll para lawfare.json e unified."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAWFARE = ROOT / "_data" / "lawfare.json"
UNIFIED = ROOT / "_data" / "lawfare-unified-corpus.json"

POSTS = [
    "2026-06-15-moraes-nega-adiamento-do-julgamento-de-eduardo-bolsonaro-dpu-arguira-quorum-incompleto-e-v.md",
    "2026-06-16-moraes-nega-todas-as-diligencias-requeridas-pela-defesa-de-flavio-bolsonaro-no-inquerito-d.md",
    "2026-06-16-primeira-turma-condena-eduardo-bolsonaro-a-4-anos-e-2-meses-por-coacao-no-curso-do-process.md",
    "2026-06-26-pf-conclui-inquerito-e-aponta-calunia-de-flavio-bolsonaro-contra-lula-dez-diligencias-da-d.md",
    "2026-06-29-pf-conclui-relatorio-apontando-indicios-de-calunia-por-flavio-bolsonaro-moraes-da-15-dias-.md",
    "2026-07-03-moraes-prorroga-domiciliar-de-bolsonaro-por-prazo-indeterminado-e-ordena-apreensao-de-10-a.md",
    "2026-07-07-moraes-determina-interrogatorio-de-flavio-bolsonaro-pela-pf-em-10-dias-pre-candidato-presi.md",
]


def parse_fm(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    fm: dict = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key, val = key.strip(), val.strip()
        if key == "tags":
            fm[key] = json.loads(val.replace("'", '"'))
        else:
            fm[key] = val.strip('"')
    return fm


def main() -> None:
    lf = json.loads(LAWFARE.read_text(encoding="utf-8"))
    uni = json.loads(UNIFIED.read_text(encoding="utf-8"))
    by_id = {a["id"]: a for a in lf["assuntos"]}
    by_corpus = {e["id_corpus"]: e for e in uni["entradas"]}

    for fname in POSTS:
        path = ROOT / "_posts" / "lawfare" / fname
        if not path.is_file():
            print(f"MISSING {path}")
            continue
        fm = parse_fm(path.read_text(encoding="utf-8"))
        cid = fm.get("id_corpus")
        if not cid:
            print(f"skip (sem id_corpus): {fname}")
            continue
        cat = fm.get("categories", "lawfare")
        tags = fm.get("tags") or [cat]
        rel = str(path.relative_to(ROOT)).replace("/", "\\")
        aid = int(cid)

        if aid in by_id:
            by_id[aid]["categoria"] = cat
            by_id[aid]["tags"] = tags
            by_id[aid]["fonte_arquivo"] = rel
            print(f"lawfare.json {aid} -> {cat} | {rel}")

        if cid in by_corpus:
            entry = by_corpus[cid]
            entry["jekyll_categories"] = [cat]
            entry["jekyll_tags"] = tags
            entry["jekyll_filename"] = fname
            if fm.get("permalink"):
                entry["jekyll_permalink"] = fm["permalink"]
            entry["categoria"] = cat
            print(f"unified {cid} -> {cat}")

    LAWFARE.write_text(json.dumps(lf, ensure_ascii=False, indent=2), encoding="utf-8")
    UNIFIED.write_text(json.dumps(uni, ensure_ascii=False, indent=2), encoding="utf-8")
    print("OK")


if __name__ == "__main__":
    main()
