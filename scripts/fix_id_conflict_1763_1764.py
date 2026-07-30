#!/usr/bin/env python3
"""Restaura dragao-onca 1763/1764 e realoca batch sigilo Vorcaro para 1775/1776."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAWFARE = ROOT / "_data/lawfare.json"
DRAGAO = ROOT / "_data/dragao-onca.json"
SYNC = ROOT / "_data/claude.ai-corpus-ids-sync.json"
NEW_V, NEW_A = 1775, 1776


def main() -> None:
    lf = json.loads(LAWFARE.read_text(encoding="utf-8"))
    by_id = {a["id"]: a for a in lf["assuntos"] if isinstance(a.get("id"), int)}

    dragao = {
        a["id"]: a
        for a in json.loads(DRAGAO.read_text(encoding="utf-8"))["assuntos"]
    }

    vorcaro = by_id.get(1763)
    alcolumbre = by_id.get(1764)
    dup1774 = by_id.get(1774)

    if not vorcaro or "Vorcaro" not in vorcaro.get("titulo", ""):
        raise SystemExit("1763 não é Vorcaro — abortando")
    if not alcolumbre or "Alcolumbre" not in alcolumbre.get("titulo", ""):
        raise SystemExit("1764 não é Alcolumbre — abortando")

    for rid in (1763, 1764):
        if rid not in dragao:
            raise SystemExit(f"dragao-onca.json sem id {rid}")
        by_id[rid] = dragao[rid].copy()

    if dup1774 and "Vorcaro" in dup1774.get("titulo", ""):
        del by_id[1774]

    if NEW_V in by_id or NEW_A in by_id:
        raise SystemExit("1775/1776 já ocupados")

    v = vorcaro.copy()
    v["id"] = NEW_V
    a = alcolumbre.copy()
    a["id"] = NEW_A
    if a.get("connections"):
        a["connections"] = [
            f"id_{NEW_V}" if c == "id_1763" else c for c in a["connections"]
        ]
    by_id[NEW_V] = v
    by_id[NEW_A] = a

    lf["assuntos"] = sorted(by_id.values(), key=lambda x: x.get("id") or 0)
    lf["total"] = len(lf["assuntos"])
    lf["data_extração"] = "2026-07-29"
    LAWFARE.write_text(json.dumps(lf, ensure_ascii=False, indent=2), encoding="utf-8")

    vorcaro_post = ROOT / "_posts/bancos/2026-07-27-ministerio-da-justica-mantem-sigilo-de-100-anos-sobre-lista-de-visitantes-de-daniel-vorcar.md"
    alc_post = ROOT / "_posts/bancos/2025-09-17-alcolumbre-reafirma-sigilo-de-100-anos-sobre-registros-de-entrada-do-careca-do-inss-no-sen.md"

    vt = vorcaro_post.read_text(encoding="utf-8")
    vt = re.sub(r'id_corpus:\s*"1763"', f'id_corpus: "{NEW_V}"', vt, count=1)
    vorcaro_post.write_text(vt, encoding="utf-8")

    at = alc_post.read_text(encoding="utf-8")
    at = re.sub(r'id_corpus:\s*"1764"', f'id_corpus: "{NEW_A}"', at, count=1)
    at = re.sub(r"id_1763", f"id_{NEW_V}", at)
    alc_post.write_text(at, encoding="utf-8")

    sintese = ROOT / "_posts/estudos/2026-07-27-sintese-estrutural-sigilo-de-100-anos-como-padrao-p10-confirmado-vorcaro-executivo-e-carec.md"
    if sintese.exists():
        st = sintese.read_text(encoding="utf-8")
        st = st.replace("id_1763", f"id_{NEW_V}").replace("id_1764", f"id_{NEW_A}")
        sintese.write_text(st, encoding="utf-8")

    sync = json.loads(SYNC.read_text(encoding="utf-8"))
    main = sync.setdefault("tracks", {}).setdefault("main", {})
    main["last_id"] = NEW_A
    main["next_available"] = NEW_A + 1
    main["last_confirmed"] = NEW_A
    main["last_jekyll_published"] = NEW_A
    SYNC.write_text(json.dumps(sync, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"OK lawfare total {lf['total']} last main {NEW_A}")
    print(f"Restaurados dragao-onca 1763/1764; sigilo -> {NEW_V}/{NEW_A}")


if __name__ == "__main__":
    main()
