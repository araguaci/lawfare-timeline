#!/usr/bin/env python3
"""Repara no lawfare.json os campos estragados pelo extrator antigo.

- descricao igual a ">", "|", ">-", "|-" (ou vazia): relida do front matter do post;
  sem description, usa o resumo do corpo;
- fontes sem nenhum link http (["N/A"], vazio ou só nomes de órgãos): relidas das
  seções de fontes/referências do post e, na falta delas, dos links do corpo.

Só toca nesses dois campos e só quando o post (fonte_arquivo) existe.

Uso:
  python scripts/reparar_descricao_fontes.py           # simulação com contagens
  python scripts/reparar_descricao_fontes.py --apply   # grava
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "_data" / "lawfare.json"
sys.path.insert(0, str(ROOT / "scripts"))
from lawfare_post_parser import extract_fontes, is_block_marker, parse_front_matter  # noqa: E402


def _load_extractor():
    spec = importlib.util.spec_from_file_location(
        "extrair_posts", ROOT / "scripts" / "extrair_posts_para_json.py"
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


def bad_descricao(value) -> bool:
    return not isinstance(value, str) or not value.strip() or is_block_marker(value)


def has_http(fontes) -> bool:
    return isinstance(fontes, list) and any(str(f).startswith("http") for f in fontes)


def counts(assuntos: list[dict]) -> tuple[int, int]:
    return (
        sum(1 for e in assuntos if bad_descricao(e.get("descricao"))),
        sum(1 for e in assuntos if not has_http(e.get("fontes"))),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="grava lawfare.json")
    args = parser.parse_args()

    extractor = _load_extractor()
    data = json.loads(CANON.read_text(encoding="utf-8"))
    assuntos: list[dict] = data["assuntos"]
    antes = counts(assuntos)

    fixed_desc = fixed_fontes = sem_post = 0
    for entry in assuntos:
        need_desc = bad_descricao(entry.get("descricao"))
        need_fontes = not has_http(entry.get("fontes"))
        if not (need_desc or need_fontes):
            continue
        rel = str(entry.get("fonte_arquivo") or "").replace("\\", "/")
        path = ROOT / rel
        if not rel or rel == "N/A" or not path.is_file():
            sem_post += 1
            continue
        front, body = parse_front_matter(path.read_text(encoding="utf-8", errors="replace"))
        if need_desc:
            desc = front.get("description") or front.get("descricao")
            if bad_descricao(desc):
                desc = extractor.extract_from_body(body).get("resumo", "")[:300]
            if not bad_descricao(desc):
                entry["descricao"] = desc[:500] + ("..." if len(desc) > 500 else "")
                fixed_desc += 1
        if need_fontes:
            urls = extract_fontes(body)
            if urls:
                # nomes de órgãos já registrados (ex.: "PF; CGU") ficam depois dos links
                extras = [f for f in entry.get("fontes") or [] if f and f != "N/A"]
                entry["fontes"] = urls + [f for f in extras if not any(u in f for u in urls)]
                fixed_fontes += 1

    depois = counts(assuntos)
    print(f"eventos: {len(assuntos)}")
    print(f"descricao inválida: {antes[0]} -> {depois[0]}  (reparadas {fixed_desc})")
    print(f"sem fonte http:     {antes[1]} -> {depois[1]}  (reparadas {fixed_fontes})")
    print(f"pendentes sem post: {sem_post}")
    if not args.apply:
        print("simulação: nada gravado (use --apply)")
        return

    data["data_extração"] = date.today().isoformat()
    data["nota"] = (
        f"Reparo de descricao ({fixed_desc}) e fontes ({fixed_fontes}) "
        "com scripts/reparar_descricao_fontes.py"
    )
    CANON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8", newline="\r\n")
    print(f"gravado: {CANON.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
