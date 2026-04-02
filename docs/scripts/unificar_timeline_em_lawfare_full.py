#!/usr/bin/env python3
"""
Mescla lawfare-timeline-124-145.json em _data/lawfare-full.json
com a mesma estrutura de `assuntos` (titulo, data_evento, categoria, etc.).

- Novos registros recebem ids sequenciais após o maior id existente (não
  reutilizam 124–145 da timeline, pois já existem em lawfare-full).
- O id da timeline fica em tags como `timeline-124`.
- Remove entradas anteriores geradas por este script (fonte_arquivo com
  `timeline-{n}-` no nome) antes de inserir de novo (reexecução idempotente).
"""

from __future__ import annotations

import importlib.util
import json
import re
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TIMELINE_PATH = ROOT / "_data" / "lawfare-timeline-124-145.json"
FULL_PATH = ROOT / "_data" / "lawfare-full.json"

TIMELINE_FILE_RE = re.compile(r"timeline-\d+-", re.I)


def _load_gen():
    spec = importlib.util.spec_from_file_location(
        "gerar_timeline",
        ROOT / "scripts" / "gerar_posts_timeline_124_145.py",
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


def fonte_arquivo_rel(item: dict, folder: str, gen) -> str:
    date_str = item.get("date") or "1970-01-01"
    tid = item.get("id")
    slug = gen.slugify(item.get("title", ""))
    fname = f"{date_str}-timeline-{tid}-{slug}.md"
    return f"_posts\\{folder}\\{fname}".replace("/", "\\")


def valores_resumo(values: dict) -> str:
    if not values:
        return "N/A"
    parts = []
    for k, v in list(values.items())[:6]:
        parts.append(f"{k}: {v}")
    return " | ".join(parts)[:500]


def relevancia(item: dict) -> str:
    cat = item.get("category") or ""
    sub = item.get("subcategory") or ""
    values = item.get("values") or {}
    blob = json.dumps(values, default=str)
    if cat == "operacao_policial" and sub in (
        "crime_organizado",
        "crime_ambiental",
        "crime_financeiro",
        "sonegação_fiscal",
        "sonegacao_fiscal",
    ):
        return "alta"
    if "bilh" in blob.lower() or "000.000.000" in blob:
        return "alta"
    return "media"


def fontes_lista(sources: list) -> list[str]:
    out = []
    for s in sources or []:
        title = (s.get("title") or "").strip()
        url = (s.get("url") or "").strip()
        outlet = (s.get("outlet") or "").strip()
        if outlet and title:
            out.append(f"{outlet}: {title} — {url}")
        elif title:
            out.append(f"{title} — {url}")
        elif url:
            out.append(url)
    return out if out else ["N/A"]


def pessoas(actors: list) -> list[str]:
    names = []
    for a in actors or []:
        n = (a.get("name") or "").strip()
        if n:
            names.append(n)
    return names if names else ["N/A"]


def timeline_to_assunto(item: dict, new_id: int, gen) -> dict:
    folder = gen.resolve_folder(item)
    tid = item.get("id")
    date_str = item.get("date") or "1970-01-01"
    if len(date_str) == 10:
        data_iso = f"{date_str}T12:00:00.000Z"
    else:
        data_iso = date_str

    title = (item.get("title") or "").strip()
    summary = (item.get("summary") or "").strip()
    notes = (item.get("notes") or "").strip()
    descricao = summary if len(summary) >= 400 else (summary + ("\n\n" + notes if notes else ""))[:4000]

    impacto, tipo_esc = gen.impacto_e_tipo(item)
    tags = list(gen.norm_tags(item, folder))
    tags.append(f"timeline-{tid}")
    tags.append("lawfare-timeline-json")

    return {
        "titulo": title,
        "data_evento": date_str,
        "data_iso": data_iso,
        "categoria": folder,
        "tags": tags,
        "descricao": descricao,
        "relevancia": relevancia(item),
        "impacto_diplomatico": impacto,
        "tipo_escandalo": tipo_esc,
        "fontes": fontes_lista(item.get("sources")),
        "pessoas_envolvidas": pessoas(item.get("actors")),
        "instituicoes_envolvidas": list(item.get("institutions") or []) or ["N/A"],
        "pais": "Brasil",
        "valor_envolvido": valores_resumo(item.get("values") or {}),
        "prioridade": 2,
        "fonte_arquivo": fonte_arquivo_rel(item, folder, gen),
        "id": new_id,
    }


def is_timeline_merge(entry: dict) -> bool:
    fa = entry.get("fonte_arquivo") or ""
    tgs = entry.get("tags") or []
    if TIMELINE_FILE_RE.search(fa.replace("/", "\\")):
        return True
    if "lawfare-timeline-json" in tgs:
        return True
    return False


def main() -> None:
    gen = _load_gen()
    timeline = json.loads(TIMELINE_PATH.read_text(encoding="utf-8"))
    full = json.loads(FULL_PATH.read_text(encoding="utf-8"))

    assuntos: list = full.get("assuntos") or []
    assuntos = [a for a in assuntos if not is_timeline_merge(a)]

    max_id = max((a.get("id") or 0) for a in assuntos) if assuntos else 0
    next_id = max_id + 1

    novos = []
    for item in timeline:
        novos.append(timeline_to_assunto(item, next_id, gen))
        next_id += 1

    full["assuntos"] = assuntos + novos
    full["total"] = len(full["assuntos"])
    full["data_extração"] = date.today().isoformat()
    full["periodo"] = (
        f"1855-01-01 a {datetime.now().strftime('%Y-%m-%d')}"
    )
    full["fonte_original"] = str(ROOT / "_posts") + " + " + str(TIMELINE_PATH.relative_to(ROOT))
    full["nota"] = (
        "Extraído de _posts (scripts/extrair_posts_para_json.py) "
        "e mesclado com lawfare-timeline-124-145.json (scripts/unificar_timeline_em_lawfare_full.py)."
    )

    FULL_PATH.write_text(
        json.dumps(full, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"lawfare-full.json: {len(assuntos)} + {len(novos)} = {full['total']} assuntos")
    print(f"Novos ids: {max_id + 1} … {next_id - 1}")


if __name__ == "__main__":
    main()
