#!/usr/bin/env python3
"""Devolve ao lawfare.json as fichas que só existem no lawfare-full.json de 24/04/2026.

Contexto: os dois JSONs numeraram de forma diferente a partir do id 1403. O
lawfare.json (canônico) manteve 1403–1424 para a leva de abril/2026 (Ramagem/ICE,
Seção 301, Mare Liberum) e perdeu a leva "timeline-124..145" (Carbono Oculto,
Greenwashing, Compliance Zero) e mais 14 fichas do full (entre elas o #1426
"Barroso admite ter pedido declarações de apoio dos EUA").

Este script acha essas fichas por identidade (fonte_arquivo ou título+data),
dá ids novos a partir de max(id)+1 e grava o mapa antigo→novo em
_data/id-remap-full-abr2026.json.

Uso:
  python scripts/recuperar_ids_orfaos_full_abr2026.py           # simulação
  python scripts/recuperar_ids_orfaos_full_abr2026.py --apply   # grava
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "_data" / "lawfare.json"
OLD_FULL = ROOT / "_data" / "lawfare-full.json"
REMAP = ROOT / "_data" / "id-remap-full-abr2026.json"


def fonte_key(entry: dict) -> str:
    raw = str(entry.get("fonte_arquivo") or "").replace("\\", "/").strip("/").lower()
    return "" if raw in ("", "n/a") else raw


def titulo_key(entry: dict) -> tuple[str, str]:
    titulo = unicodedata.normalize("NFKD", str(entry.get("titulo") or ""))
    titulo = titulo.encode("ascii", "ignore").decode().lower()
    return (str(entry.get("data_evento") or "")[:10], re.sub(r"[^a-z0-9]+", "", titulo)[:60])


def is_evento(entry: dict) -> bool:
    data = str(entry.get("data_evento") or "")
    return bool(entry.get("titulo")) and bool(data) and not data.startswith("0001")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="grava lawfare.json e o mapa de ids")
    args = parser.parse_args()

    canon = json.loads(CANON.read_text(encoding="utf-8"))
    assuntos: list[dict] = canon["assuntos"]
    old = json.loads(OLD_FULL.read_text(encoding="utf-8"))["assuntos"]

    known_fontes = {fonte_key(e) for e in assuntos} - {""}
    known_titulos = {titulo_key(e) for e in assuntos}
    next_id = max(e["id"] for e in assuntos if isinstance(e.get("id"), int)) + 1

    recovered: list[dict] = []
    remap: dict[str, int] = {}
    for entry in sorted(old, key=lambda e: e["id"]):
        if not is_evento(entry):
            continue
        if fonte_key(entry) in known_fontes or titulo_key(entry) in known_titulos:
            continue
        new = {**entry, "id": next_id}
        remap[str(entry["id"])] = next_id
        recovered.append(new)
        print(f"  full #{entry['id']:>4} -> #{next_id}  {entry['data_evento']}  {entry['titulo'][:80]}")
        next_id += 1

    print(f"\nfichas recuperadas: {len(recovered)}")
    if not recovered:
        return
    if not args.apply:
        print("simulação: nada gravado (use --apply)")
        return

    canon["assuntos"] = assuntos + recovered
    canon["total"] = len(canon["assuntos"])
    canon["data_extração"] = date.today().isoformat()
    canon["nota"] = (
        f"Recuperação de {len(recovered)} fichas órfãs do lawfare-full.json de 24/04/2026 "
        f"(ids {recovered[0]['id']}–{recovered[-1]['id']}); mapa em {REMAP.name}"
    )
    CANON.write_text(json.dumps(canon, ensure_ascii=False, indent=2), encoding="utf-8", newline="\r\n")
    REMAP.write_text(
        json.dumps(
            {
                "gerado_em": date.today().isoformat(),
                "origem": "_data/lawfare-full.json (24/04/2026)",
                "destino": "_data/lawfare.json",
                "mapa": remap,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"gravado: {CANON.relative_to(ROOT)} e {REMAP.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
