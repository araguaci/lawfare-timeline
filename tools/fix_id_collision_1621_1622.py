#!/usr/bin/env python3
"""Resolve colisões 1621–1623 após merge simultâneo de batches gap + consulado."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LF = ROOT / "_data" / "lawfare.json"
UNI = ROOT / "_data" / "lawfare-unified-corpus.json"
SYNC = ROOT / "_data" / "claude.ai-corpus-ids-sync.json"
REVISAO_POST = ROOT / "_posts/stf/2026-05-08-bolsonaro-revisao-criminal-stf-dosimetria-erro-judiciario.md"


def fix_lawfare() -> None:
    data = json.loads(LF.read_text(encoding="utf-8"))
    assuntos = data["assuntos"]

    # Remove duplicate 1622 consulado (keep Hawala as 1622)
    seen: dict[int, dict] = {}
    out: list[dict] = []
    for a in assuntos:
        aid = a.get("id")
        if aid is None:
            out.append(a)
            continue
        titulo = (a.get("titulo") or "").lower()
        if aid == 1622 and "consulado" in titulo and "hong kong" in titulo:
            continue  # drop duplicate; 1623 is canonical
        if aid in seen:
            prev = seen[aid]
            prev_t = (prev.get("titulo") or "").lower()
            if aid == 1622 and "hawala" not in prev_t and "hawala" in titulo:
                out = [x for x in out if x.get("id") != 1622]
                seen[aid] = a
                out.append(a)
            continue
        seen[aid] = a
        out.append(a)

    # Re-add revisão criminal as 1624 if missing
    if not any(a.get("id") == 1624 for a in out):
        out.append({
            "titulo": (
                "Bolsonaro protocola Revisão Criminal no STF — "
                "Alega 'erro judiciário' e cerceamento de defesa"
            ),
            "data_evento": "2026-05-08",
            "data_iso": "2026-05-08T12:00:00.000Z",
            "categoria": "stf",
            "tags": [
                "bolsonaro", "revisao-criminal", "lei-dosimetria", "stf",
                "mauro-cid", "erro-judiciario", "8-janeiro",
            ],
            "descricao": (
                "Defesa de Bolsonaro protocola revisão criminal após Lei 15.402/2026."
            ),
            "relevancia": "alta",
            "impacto_diplomatico": "N/A",
            "tipo_escandalo": "lawfare",
            "fontes": [
                "https://www.hojeemdia.com.br/politica/bolsonaro-entra-com-revis-o-criminal-no-stf-para-anular-condenac-o-apos-dosimetria-ser-promulgada-1.1116332"
            ],
            "pessoas_envolvidas": ["Jair Bolsonaro", "Mauro Cid"],
            "instituicoes_envolvidas": ["STF — 2ª Turma"],
            "pais": "Brasil",
            "valor_envolvido": "N/A",
            "prioridade": 1,
            "fonte_arquivo": (
                "_posts\\stf\\2026-05-08-bolsonaro-revisao-criminal-stf-dosimetria-erro-judiciario.md"
            ),
            "id": 1624,
            "meta": {
                "observacao": (
                    "Renumerado 2026-07-18: ex-1621 (colisão com Moraes/Milei batch gap); "
                    "antes 1520/176."
                )
            },
        })

    out.sort(key=lambda x: x.get("id") or 0)
    data["assuntos"] = out
    data["total"] = len(out)
    data["data_extração"] = "2026-07-18"
    LF.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"lawfare.json: {len(out)} entradas, ids 1621-1624 OK")


def fix_unified() -> None:
    data = json.loads(UNI.read_text(encoding="utf-8"))
    entradas = data.get("entradas", [])
    out: list[dict] = []
    seen: set[str] = set()
    for e in entradas:
        cid = str(e.get("id_corpus", ""))
        fn = e.get("jekyll_filename") or ""
        if cid == "1622" and "consulado" in fn.lower():
            continue
        if cid == "1621" and "revisao-criminal" in fn.lower():
            e = {**e, "id_corpus": "1624", "conflito_nota": "Renumerado 1621→1624 (colisão Moraes/Milei)."}
            cid = "1624"
        if cid in seen:
            continue
        seen.add(cid)
        out.append(e)
    if "1624" not in seen:
        out.append({
            "id_corpus": "1624",
            "jekyll_filename": "2026-05-08-bolsonaro-revisao-criminal-stf-dosimetria-erro-judiciario.md",
            "jekyll_date": "2026-05-08",
            "jekyll_categories": ["stf"],
            "jekyll_permalink": "/posts/bolsonaro-revisao-criminal-stf-dosimetria-erro-judiciario/",
            "titulo": "Bolsonaro protocola Revisão Criminal no STF",
            "verificado": True,
            "status_publicacao": "coberto_por_artigo",
        })
    out.sort(key=lambda x: int(x.get("id_corpus") or 0))
    data["entradas"] = out
    UNI.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"unified: {len(out)} entradas")


def fix_posts() -> None:
    if REVISAO_POST.is_file():
        t = REVISAO_POST.read_text(encoding="utf-8")
        t = t.replace('id_corpus: "1621"', 'id_corpus: "1624"')
        t = t.replace("| `id_corpus` | **1621** |", "| `id_corpus` | **1624** |")
        REVISAO_POST.write_text(t, encoding="utf-8")
        print("post revisão criminal → 1624")
    for p in ROOT.glob("_posts/**/*.md"):
        t = p.read_text(encoding="utf-8", errors="replace")
        if "`id_corpus` 1621)" in t and "revisao-criminal" in t:
            p.write_text(t.replace("`id_corpus` 1621)", "`id_corpus` 1624)"), encoding="utf-8")


def fix_sync() -> None:
    data = json.loads(SYNC.read_text(encoding="utf-8"))
    main = data["tracks"]["main"]
    main["last_id"] = 1624
    main["next_available"] = 1625
    main["last_confirmed"] = 1624
    notes = data.setdefault("sync_status", {}).setdefault("notes", [])
    notes.append(
        "Merge gap 0707-0718: 1621 Moraes/Milei, 1622 Hawala, 1623 Consulado HK (P02); "
        "revisão criminal Bolsonaro→1624."
    )
    data.setdefault("id_conflict_resolutions", {})["1621_revisao_vs_milei_2026-07-18"] = {
        "issue": "1621 atribuído tanto à revisão criminal quanto ao batch Moraes/Milei",
        "resolution": "1621=Moraes/Milei; revisão criminal→1624",
    }
    SYNC.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("sync: last=1624 next=1625")


def main() -> None:
    fix_lawfare()
    fix_unified()
    fix_posts()
    fix_sync()


if __name__ == "__main__":
    main()
