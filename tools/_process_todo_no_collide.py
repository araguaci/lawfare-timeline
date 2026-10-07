# -*- coding: utf-8 -*-
"""Prepara a fila 06/10/2026: arquiva duplicata, realoca lock, numera T-271/T-272."""
from __future__ import annotations

import json
import re
import shutil
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODO = ROOT / "_data" / "todo"
LOCK = ROOT / "_data" / "lock"
PROC = ROOT / "_data" / "processados"

LOCK_ORDER = [
    "lawfare-batch-impedimento-stf-master-1918-1921.json",
    "lawfare-batch-crise-stf-master-1922-1926.json",
    "lawfare-batch-gilmar-alcolumbre-motta-castro-1927-1932.json",
    "lawfare-batch-patrocinios-iter-darkhorse-1933-1936.json",
    "lawfare-batch-rpps-delacoes-1937-1938.json",
    "lawfare-batch-rioprevidencia-dino-1939-1940.json",
    "lawfare-batch-rioprevidencia-individuos-1941-1942.json",
    "lawfare-batch-cedae-castro-busca-apreensao-1943-1944.json",
    "lawfare-batch-coronel-pcc-visto-embaixadora-PENDENTE_SYNC.json",
]


def remap_num(n: int) -> int:
    if 1918 <= n <= 1944:
        return n + 25
    return n


def remap_text(val):
    if isinstance(val, str):
        def repl(m):
            old = int(m.group(1))
            return f"id_{remap_num(old)}"
        return re.sub(r"id_(\d+)", repl, val)
    if isinstance(val, list):
        return [remap_text(x) for x in val]
    return val


def remap_item(item: dict, pending_ids: list[int] | None = None) -> dict:
    out = deepcopy(item)
    raw = out.get("id")
    if raw in ("__PENDENTE_SYNC__",) or (isinstance(raw, str) and "PENDENTE" in str(raw).upper()):
        if not pending_ids:
            raise SystemExit("sem ID pendente disponível")
        out["id"] = pending_ids.pop(0)
    else:
        try:
            old = int(raw)
        except (TypeError, ValueError):
            old = None
        if old is not None:
            out["id"] = remap_num(old)
    for key in (
        "connections",
        "lacuna_investigativa",
        "analise",
        "summary",
        "descricao",
        "resumo",
        "ponto_de_inflexao",
    ):
        if key in out:
            out[key] = remap_text(out[key])
    return out


def load_entries(raw):
    if isinstance(raw, list):
        return raw, None
    for key in ("entries", "entradas", "assuntos", "main"):
        if isinstance(raw.get(key), list):
            return raw[key], key
    return [], None


def main() -> None:
    PROC.mkdir(parents=True, exist_ok=True)
    staging = TODO / "_staging"
    staging.mkdir(exist_ok=True)

    # 1) Duplicata 1943-1959 = já mergeado 1926-1942
    dup = TODO / "lawfare-batch-1943-1959.json"
    if dup.is_file():
        note = PROC / "lawfare-batch-1943-1959.DUPLICATA-1926-1942.md"
        note.write_text(
            "Arquivado sem merge em 2026-10-06.\n"
            "Conteúdo idêntico ao lote já em lawfare.json como 1926–1942 "
            "(óbitos 8/1, bloqueios P05, Madame Satã).\n"
            "Os IDs 1943–1959 deste arquivo NÃO foram usados.\n",
            encoding="utf-8",
        )
        shutil.move(str(dup), str(PROC / "lawfare-batch-1943-1959.json"))
        print("archive duplicata 1943-1959 -> processados/")

    # 2) Lock -> todo com +25 (1918-1944)
    pending = [1970, 1971]
    for name in LOCK_ORDER:
        src = LOCK / name
        if not src.is_file():
            print("SKIP lock ausente", name)
            continue
        raw = json.loads(src.read_text(encoding="utf-8"))
        items, key = load_entries(raw)
        if "PENDENTE" in name:
            items = [remap_item(it, pending) for it in items]
        else:
            items = [remap_item(it) for it in items]
        if key is None:
            out = items
        else:
            out = deepcopy(raw)
            out[key] = items
            meta = out.setdefault("_meta", {}) if isinstance(out, dict) else {}
            if isinstance(meta, dict):
                meta["renumerado_em"] = "2026-10-06"
                meta["nota_renumeracao"] = (
                    "IDs 1918-1944 realocados +25 → 1943-1969 para não colidir "
                    "com Brumadinho 1918-1925 e mortalidade 8/1 1926-1942. "
                    "PENDENTE_SYNC → 1970-1971."
                )
        dest_name = name.replace("1918-1921", "1943-1946").replace(
            "1922-1926", "1947-1951"
        ).replace("1927-1932", "1952-1957").replace("1933-1936", "1958-1961").replace(
            "1937-1938", "1962-1963"
        ).replace("1939-1940", "1964-1965").replace("1941-1942", "1966-1967").replace(
            "1943-1944", "1968-1969"
        ).replace("-PENDENTE_SYNC", "-1970-1971")
        dest = TODO / dest_name
        dest.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        shutil.move(str(src), str(PROC / f"lock-orig-{name}"))
        print(f"lock {name} -> todo/{dest_name}")

    # 3) Gilmarpalooza → 1972
    gpath = TODO / "entrada-pendente-gilmarpalooza.json"
    if gpath.is_file():
        raw = json.loads(gpath.read_text(encoding="utf-8"))
        items, key = load_entries(raw)
        for it in items:
            it["id"] = 1972
            it["connections"] = ["id_1941", "id_1942", "id_1601", "id_1958"]
        raw[key] = items
        raw.setdefault("_meta", {})["renumerado_em"] = "2026-10-06"
        raw["_meta"]["id_final"] = 1972
        gpath.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("gilmarpalooza -> 1972")

    # 4) Comparação P05 → 1973 (não usa faixa duplicata 1950-1959)
    cpath = TODO / "lawfare-entrada-1960-comparacao-p05.json"
    if cpath.is_file():
        raw = json.loads(cpath.read_text(encoding="utf-8"))
        items, key = load_entries(raw)
        for it in items:
            it["id"] = 1973
            it["connections"] = [
                "id_1925",
                "id_1929",
                "id_1930",
                "id_1931",
                "id_1933",
                "id_1934",
                "id_1941",
                "id_1942",
            ]
        raw[key] = items
        raw.setdefault("_meta", {})["renumerado_em"] = "2026-10-06"
        raw["_meta"]["id_final"] = 1973
        raw["_meta"]["nota_renumeracao"] = (
            "1960 evitado: a faixa 1943-1959 era duplicata de 1926-1942. "
            "Comparação P05 recebe 1973; conexões apontam aos IDs já mergeados."
        )
        dest = TODO / "lawfare-entrada-1973-comparacao-p05.json"
        dest.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cpath.unlink()
        print("comparacao P05 1960 -> 1973")

    # 5) Temáticos: T-270 HTML = Sete de Onze → T-271; T-271 HTML = Sob Medida → T-272
    t271 = {
        "id": 271,
        "tipo": "analise_estrutural",
        "titulo": "Sete de Onze: o retrato estrutural do STF na crise Banco Master",
        "slug": "sete-de-onze-stf-banco-master",
        "data_registro": "2026-09-17",
        "summary": (
            "Sete dos onze ministros do STF com vínculo documentado a Daniel Vorcaro/"
            "Banco Master. Nenhuma autodeclaração espontânea de impedimento. "
            "Síntese do eixo Judiciário federal; o eixo Rio (Castro/Rioprevidência/Cedae) "
            "foi desmembrado para T-272."
        ),
        "analise": (
            "Nenhuma entrada isolada prova captura sistêmica; a soma prova. "
            "7/11 ministros com vínculo documentado; 0 autodeclarações espontâneas; "
            "R$ 3,4 bi+ citados (confirmados + alegados). "
            "A delação de Vorcaro foi encerrada pela PGR em 02/07/2026 (id_1963). "
            "Mendonça detém o HD pericial do celular de Vorcaro; Dino propôs tratamento "
            "sistemático dos vínculos (id_1965). Artefato HTML original em "
            "_data/todo/_staging/t271-sete-de-onze.html (antes rotulado T-270; "
            "T-270 ficou o Compilado Lawfare)."
        ),
        "padroes_ativados": ["P02", "P03", "P05", "P07", "P10"],
        "connections": ["id_1843", "id_1846", "id_1963", "id_1965"],
        "fontes": [
            {"titulo": "Corpus lawfare-timeline 1843–1969", "url": "https://lawfare-timeline.vercel.app/estudos/"}
        ],
        "lacuna_investigativa": (
            "Conteúdo integral do HD pericial sob Mendonça não público. "
            "Tratamento colegiado dos 7 vínculos ainda não formalizado."
        ),
    }
    t272 = {
        "id": 272,
        "tipo": "analise_estrutural",
        "titulo": "Sob Medida: captura relâmpago do Rioprevidência e da Cedae",
        "slug": "sob-medida-rioprevidencia-cedae",
        "data_registro": "2026-09-17",
        "summary": (
            "Substituição de cúpula em três meses; nomeação no mesmo dia do pedido "
            "de credenciamento do Master. Busca e apreensão contra Cláudio Castro "
            "(11/09/2026); PGR fala em coautoria. Contraponto processual a T-271."
        ),
        "analise": (
            "Diferente do STF (T-271), aqui a trilha é administrativa: 3 dias entre "
            "encontro presencial e primeiro aporte (dez/2024); Rioprevidência R$3 bi+ "
            "(>25% do patrimônio); Cedae prejuízo estimado R$222,1 mi (id_1968); "
            "8 encontros Castro–Vorcaro em 1 ano; busca e apreensão (id_1969). "
            "Artefato HTML original em _data/todo/_staging/t272-sob-medida-rioprevidencia-cedae.html."
        ),
        "padroes_ativados": ["P05", "P07"],
        "connections": ["id_1964", "id_1966", "id_1968", "id_1969"],
        "fontes": [
            {"titulo": "Jornal de Brasília — auditoria Cedae", "url": "https://jornaldebrasilia.com.br/noticias/economia/auditoria-da-cedae-aponta-articulacao-para-aportes-conjuntos-com-rioprevidencia-no-banco-master/"}
        ],
        "lacuna_investigativa": (
            "Nomes dos executivos da Cedae responsáveis pela mudança de política "
            "ainda não individualizados nas fontes públicas."
        ),
    }
    (TODO / "thematic-T271-sete-de-onze.json").write_text(
        json.dumps(t271, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (TODO / "thematic-T272-sob-medida-rioprevidencia-cedae.json").write_text(
        json.dumps(t272, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    for src, dest in (
        (TODO / "t270-sete-de-onze.html", staging / "t271-sete-de-onze.html"),
        (TODO / "t271-sob-medida-rioprevidencia-cedae.html", staging / "t272-sob-medida-rioprevidencia-cedae.html"),
    ):
        if src.is_file():
            shutil.move(str(src), str(dest))
    for name in (
        "compass_artifact_wf-f0a7ae6e-6414-5aa6-aeb8-e68f78dd467f_text_markdown.md",
        "lawfare-timeline-entradas-ois-draft.md",
        "notas-clubes-militares.html",
        "prompt-tratamento-pdfs-mensalao.md",
        "thread-vazatoga-diploma-impunidade.md",
    ):
        src = TODO / name
        if src.is_file():
            shutil.move(str(src), str(staging / name))
            print("staging", name)

    print("prep ok")


if __name__ == "__main__":
    main()
