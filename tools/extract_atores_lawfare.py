#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrai entradas de atores específicos de lawfare.json."""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAWFARE = ROOT / "_data" / "lawfare.json"
OUT = ROOT / "_data" / "atores-gilmar-mendes-carmen-lucia.json"

ACTORS = {
    "Gilmar Mendes": {
        "aliases": [r"Gilmar Mendes", r"\bGilmar\b"],
        "instituicao": "STF",
        "papel": "Ministro do STF",
    },
    "Cármen Lúcia": {
        "aliases": [r"C[aá]rmen L[uú]cia", r"Carmen Lucia"],
        "instituicao": "STF",
        "papel": "Ministra do STF",
    },
}


def matches_actor(text: str | None, patterns: list[str]) -> bool:
    if not text:
        return False
    return any(re.search(p, str(text), re.I) for p in patterns)


def entry_hits(entry: dict, patterns: list[str]) -> list[str]:
    fields: list[str] = []
    for field in ("titulo", "descricao"):
        if matches_actor(entry.get(field), patterns):
            fields.append(field)
    for pessoa in entry.get("pessoas_envolvidas") or []:
        if matches_actor(pessoa, patterns):
            fields.append("pessoas_envolvidas")
            break
    return sorted(set(fields))


def main() -> None:
    data = json.loads(LAWFARE.read_text(encoding="utf-8"))
    assuntos = data.get("assuntos", [])

    result = {
        "_meta": {
            "gerado_em": date.today().isoformat(),
            "fonte": "_data/lawfare.json",
            "total_assuntos_corpus": len(assuntos),
            "proposito": "Verificar se os nós Gilmar Mendes e Cármen Lúcia já têm entradas no corpus",
        },
        "atores": {},
    }

    for name, cfg in ACTORS.items():
        patterns = cfg["aliases"]
        hits = []
        for entry in assuntos:
            hit_fields = entry_hits(entry, patterns)
            if not hit_fields:
                continue
            hits.append(
                {
                    "id": entry.get("id"),
                    "data_evento": entry.get("data_evento"),
                    "titulo": entry.get("titulo"),
                    "categoria": entry.get("categoria"),
                    "tags": entry.get("tags", []),
                    "pessoas_envolvidas": entry.get("pessoas_envolvidas", []),
                    "instituicoes_envolvidas": entry.get("instituicoes_envolvidas", []),
                    "fonte_arquivo": entry.get("fonte_arquivo"),
                    "match_em": hit_fields,
                }
            )
        hits.sort(key=lambda x: (x.get("data_evento") or "", x.get("id") or 0))
        ids = sorted(h["id"] for h in hits if h.get("id") is not None)
        result["atores"][name] = {
            "instituicao": cfg["instituicao"],
            "papel": cfg["papel"],
            "tem_entradas": len(hits) > 0,
            "total_entradas": len(hits),
            "id_corpus_min": min(ids) if ids else None,
            "id_corpus_max": max(ids) if ids else None,
            "ids_corpus": ids,
            "entradas": hits,
        }

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for name, actor in result["atores"].items():
        print(
            f"{name}: {actor['total_entradas']} entradas "
            f"(ids {actor['id_corpus_min']}–{actor['id_corpus_max']})"
        )
    print(f"Escrito: {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
