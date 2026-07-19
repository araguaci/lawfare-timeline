#!/usr/bin/env python3
"""Corrige conflito IDs 1520/176 — revisão criminal Bolsonaro vs P04b imprensa."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LF = ROOT / "_data" / "lawfare.json"
UNI = ROOT / "_data" / "lawfare-unified-corpus.json"
SYNC = ROOT / "_data" / "claude.ai-corpus-ids-sync.json"
DUP = ROOT / "_posts" / "lawfare" / (
    "2026-05-08-bolsonaro-protocola-revisao-criminal-erro-judiciario-"
    "delacao-nao-voluntaria-e-negativa-de-.md"
)


def fix_lawfare() -> None:
    data = json.loads(LF.read_text(encoding="utf-8"))
    assuntos = data["assuntos"]
    for i, a in enumerate(assuntos):
        if a.get("id") == 1520:
            assuntos[i] = {
                "titulo": (
                    "Imprensa brasileira enquadra designação terrorista de PCC/CV "
                    "como 'questão de soberania' — P04b documentado"
                ),
                "data_evento": "2026-05-28",
                "data_iso": "2026-05-28T18:00:00-03:00",
                "categoria": "lawfare",
                "tags": [
                    "lawfare", "pcc", "crime-organizado", "censura",
                    "soberania", "stf", "p04b", "p04",
                ],
                "descricao": (
                    "Cobertura dominante em 28/05/2026 enquadra designação SDGT de PCC/CV "
                    "como soberania, não pelos fatos documentados. Instância P04b."
                ),
                "relevancia": "alta",
                "impacto_diplomatico": "alto",
                "tipo_escandalo": "mecanismo_sistemico",
                "fontes": [
                    "https://www.riotimesonline.com/brazil-scrambles-to-block-u-s-terror-label-for-its-gangs/"
                ],
                "pessoas_envolvidas": [],
                "instituicoes_envolvidas": ["Mídia brasileira"],
                "pais": "Brasil",
                "valor_envolvido": "N/A",
                "prioridade": 1,
                "fonte_arquivo": (
                    "_posts\\lawfare\\2026-05-28-imprensa-brasileira-enquadra-"
                    "designacao-terrorista-pcc-cv-como-questao-de-soberania-p04b.md"
                ),
                "id": 1520,
                "meta": {
                    "observacao": (
                        "Corrigido 2026-07-18: ID 1520 restaurado ao post P04b; "
                        "revisão criminal renumerada para 1621."
                    )
                },
            }
            break

    if not any(a.get("id") == 1621 for a in assuntos):
        assuntos.append({
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
                "Defesa de Bolsonaro protocola revisão criminal após Lei 15.402/2026, "
                "alegando erro judiciário, competência do plenário, delação não voluntária "
                "e cerceamento de defesa."
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
            "id": 1621,
            "meta": {
                "observacao": (
                    "Renumerado 2026-07-18: ex id_corpus 176/1520 duplicado; "
                    "post lawfare/ duplicado removido."
                )
            },
        })

    data["assuntos"] = assuntos
    data["total"] = len(assuntos)
    data["data_extração"] = "2026-07-18"
    LF.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"lawfare.json: {data['total']} entradas")


def fix_unified() -> None:
    data = json.loads(UNI.read_text(encoding="utf-8"))
    entradas = data.get("entradas", [])
    imprensa = {
        "id_corpus": "1520",
        "id_original": 1520,
        "conflito_nota": "Restaurado 2026-07-18: batch 1513-1520 canônico P04b imprensa.",
        "jekyll_filename": (
            "2026-05-28-imprensa-brasileira-enquadra-designacao-terrorista-pcc-cv-"
            "como-questao-de-soberania-p04b.md"
        ),
        "jekyll_date": "2026-05-28",
        "jekyll_categories": ["lawfare"],
        "jekyll_tags": ["lawfare", "pcc", "crime-organizado", "censura", "soberania", "stf", "p04b"],
        "jekyll_permalink": "/posts/imprensa-brasileira-enquadra-designacao-terrorista-pcc-cv-como-questao-de-soberania-p04b/",
        "titulo": (
            "Imprensa brasileira enquadra designação terrorista de PCC/CV "
            "como 'questão de soberania' — P04b documentado"
        ),
        "categoria": "lawfare",
        "resumo": "Instância datada P04b — enquadramento 'soberania' domina cobertura em 28/05/2026.",
        "fontes_verificadas": [{
            "url": "https://www.riotimesonline.com/brazil-scrambles-to-block-u-s-terror-label-for-its-gangs/",
            "titulo": "Brazil Scrambles to Block U.S. Terror Label for Its Gangs",
            "veiculo": "Rio Times Online",
            "data": "2026-03-11",
        }],
        "padroes": ["P04b", "P04"],
        "conexoes": ["id_1518", "id_1512"],
        "verificado": True,
        "status_publicacao": "coberto_por_artigo",
    }
    revisao = {
        "id_corpus": "1621",
        "id_original": None,
        "conflito_nota": "Renumerado 2026-07-18: ex 176/188/1520 duplicado revisão criminal Bolsonaro.",
        "jekyll_filename": "2026-05-08-bolsonaro-revisao-criminal-stf-dosimetria-erro-judiciario.md",
        "jekyll_date": "2026-05-08",
        "jekyll_categories": ["stf"],
        "jekyll_tags": [
            "bolsonaro", "revisao-criminal", "lei-dosimetria", "stf",
            "mauro-cid", "erro-judiciario", "8-janeiro",
        ],
        "jekyll_permalink": "/posts/bolsonaro-revisao-criminal-stf-dosimetria-erro-judiciario/",
        "titulo": (
            "Bolsonaro protocola Revisão Criminal no STF — "
            "Alega 'erro judiciário' e cerceamento de defesa"
        ),
        "categoria": "stf",
        "resumo": (
            "Pedido de revisão criminal após Lei 15.402/2026; tramita na 2ª Turma."
        ),
        "fontes_verificadas": [{
            "url": "https://www.hojeemdia.com.br/politica/bolsonaro-entra-com-revis-o-criminal-no-stf-para-anular-condenac-o-apos-dosimetria-ser-promulgada-1.1116332",
            "titulo": "Bolsonaro entra com revisão criminal no STF após Dosimetria ser promulgada",
            "veiculo": "Hoje em Dia",
            "data": "2026-05-08",
        }],
        "atores": ["Jair Bolsonaro", "Mauro Cid"],
        "instituicoes": ["STF — 2ª Turma"],
        "conexoes": ["id_185", "id_186", "id_187"],
        "verificado": True,
        "status_publicacao": "coberto_por_artigo",
    }

    out: list[dict] = []
    seen: set[str] = set()
    for e in entradas:
        cid = str(e.get("id_corpus", ""))
        if cid in ("1520", "188") and "revisao-criminal" in (e.get("jekyll_filename") or ""):
            continue
        if cid == "1520" and "imprensa-brasileira" not in (e.get("jekyll_filename") or ""):
            continue
        if cid == "188":
            continue
        out.append(e)
        seen.add(cid)

    if "1520" not in seen:
        out.append(imprensa)
    if "1621" not in seen:
        out.append(revisao)

    out.sort(key=lambda x: int(x.get("id_corpus") or 0))
    data["entradas"] = out
    UNI.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"lawfare-unified-corpus.json: {len(out)} entradas")


def fix_sync() -> None:
    data = json.loads(SYNC.read_text(encoding="utf-8"))
    main = data["tracks"]["main"]
    main["last_id"] = 1621
    main["next_available"] = 1622
    main["last_confirmed"] = 1621
    main["last_jekyll_published"] = 1621

    resolutions = data.setdefault("id_conflict_resolutions", {})
    resolutions["1520_176_revisao_criminal_2026-07-18"] = {
        "issue": "Duplicata revisão criminal Bolsonaro (08/05/2026) com id_corpus 176 e 1520",
        "resolution": {
            "1520": "Restaurado ao post P04b imprensa (batch 1513-1520 canônico)",
            "1621": "Revisão criminal — post canônico _posts/stf/2026-05-08-bolsonaro-revisao-criminal-...",
            "removed": "_posts/lawfare/2026-05-08-bolsonaro-protocola-revisao-criminal-... (duplicata)",
        },
    }

    notes = data.setdefault("sync_status", {}).setdefault("notes", [])
    notes.append(
        "Correção 2026-07-18: ID 1520→P04b imprensa; revisão criminal Bolsonaro→1621; duplicata lawfare/ removida."
    )
    notes.append("lawfare.json last_id=1621; próximo ID livre=1622")

    SYNC.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("sync JSON atualizado: main last=1621 next=1622")


def main() -> None:
    if DUP.is_file():
        DUP.unlink()
        print(f"removido: {DUP.relative_to(ROOT)}")
    fix_lawfare()
    fix_unified()
    fix_sync()


if __name__ == "__main__":
    main()
