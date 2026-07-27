#!/usr/bin/env python3
"""Exporta corpus Dragão e a Onça para _data/dragao-onca.json (schema lawfare.json)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
LAWFARE = ROOT / "_data" / "lawfare.json"
POSTS_DIR = ROOT / "_posts" / "dragao-onca"
THEMATIC_ORDER = ROOT / "_data" / "dragao_onca_thematic_order.yml"
DEFAULT_OUT = ROOT / "_data" / "dragao-onca.json"


def load_yaml(path: Path) -> dict:
    if not path.exists() or yaml is None:
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def is_dragao_assunto(item: dict) -> bool:
    cat = (item.get("categoria") or "").lower()
    path = (item.get("fonte_arquivo") or "").replace("\\", "/").lower()
    return cat == "dragao-onca" or "/dragao-onca/" in path or path.startswith("_posts/dragao-onca/")


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


def extract_patterns(body: str) -> list[str]:
    found: set[str] = set()
    for p in re.findall(r"\*\*Padr(?:ões|ão):\*\*\s*([^\n·]+)", body, re.I):
        for m in re.findall(r"P\d{2}b?", p, re.I):
            found.add(m.lower())
    sec = re.search(
        r"##\s*[^\n]*Padrões Analíticos[^\n]*\n(.*?)(?=\n## |\Z)", body, re.S | re.I
    )
    if sec:
        for p in re.findall(r"-\s*\*\*(P\d{2}b?)\*\*", sec.group(1), re.I):
            found.add(p.lower())
    return sorted(found)


def post_to_assunto(path: Path, track: str) -> dict | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    fm, body = parse_frontmatter(text)
    if not fm:
        return None

    titulo = fm.get("title") or path.stem
    descricao = (fm.get("description") or "")[:500]
    date_raw = str(fm.get("date") or "2026-01-01")
    data_evento = date_raw[:10] if len(date_raw) >= 10 else "2026-01-01"
    tags = fm.get("tags") or []
    if isinstance(tags, str):
        tags = [tags]
    tags = [str(t) for t in tags]
    patterns = extract_patterns(body)
    for p in patterns:
        if p not in tags:
            tags.append(p)
    if "dragao-onca" not in tags:
        tags.insert(0, "dragao-onca")

    timeline_id = fm.get("timeline_id")
    entry_id = int(timeline_id) if timeline_id is not None else None

    rel = path.relative_to(ROOT).as_posix()
    assunto = {
        "titulo": titulo,
        "data_evento": data_evento,
        "data_iso": f"{data_evento}T12:00:00.000Z",
        "categoria": "dragao-onca",
        "tags": tags[:12],
        "descricao": descricao,
        "relevancia": "alta",
        "impacto_diplomatico": "N/A",
        "tipo_escandalo": "N/A",
        "fontes": ["N/A"],
        "pessoas_envolvidas": [],
        "instituicoes_envolvidas": [],
        "pais": "Brasil",
        "valor_envolvido": "N/A",
        "prioridade": 1,
        "fonte_arquivo": rel.replace("/", "\\"),
        "track": track,
    }

    if track == "main" and entry_id is None:
        m = re.search(r"id(\d{4})", path.stem, re.I)
        entry_id = int(m.group(1)) if m else None

    if entry_id is not None:
        assunto["id"] = entry_id

    if track == "thematic" and entry_id is not None:
        assunto["thematic_id"] = f"T-{entry_id}"

    status = fm.get("status")
    if status:
        assunto["status"] = status

    return assunto


def load_main_from_lawfare() -> list[dict]:
    data = json.loads(LAWFARE.read_text(encoding="utf-8"))
    items = [dict(a) for a in data.get("assuntos", []) if is_dragao_assunto(a)]
    for a in items:
        a["track"] = "main"
        if "thematic_id" in a:
            del a["thematic_id"]
    return sorted(items, key=lambda x: x.get("id", 0))


def load_thematic_from_posts(existing_main_ids: set[int]) -> list[dict]:
    thematic: list[dict] = []
    for path in sorted(POSTS_DIR.glob("2026-07-24-t*.md")):
        item = post_to_assunto(path, track="thematic")
        if not item or "id" not in item:
            continue
        if item["id"] in existing_main_ids:
            continue
        thematic.append(item)
    return thematic


def sort_thematic(items: list[dict], order: list[int]) -> list[dict]:
    rank = {tid: i for i, tid in enumerate(order)}
    return sorted(items, key=lambda x: rank.get(x.get("id"), 999))


def build_export() -> dict:
    main = load_main_from_lawfare()
    main_ids = {a["id"] for a in main if "id" in a}
    thematic = load_thematic_from_posts(main_ids)

    order_cfg = load_yaml(THEMATIC_ORDER)
    thematic_order = order_cfg.get("ids") or []
    thematic = sort_thematic(thematic, thematic_order)

    assuntos = main + thematic
    datas = [a["data_evento"] for a in assuntos if a.get("data_evento") and a["data_evento"] != "0001-01-01"]
    periodo = f"{min(datas)} a {max(datas)}" if datas else "N/A"

    main_ids_list = sorted(main_ids)
    thematic_ids = sorted(a["id"] for a in thematic if "id" in a)

    return {
        "serie": "O Dragão e a Onça",
        "assuntos": assuntos,
        "total": len(assuntos),
        "total_main": len(main),
        "total_thematic": len(thematic),
        "data_extracao": datetime.now().strftime("%Y-%m-%d"),
        "periodo": periodo,
        "fonte_original": f"{LAWFARE.relative_to(ROOT)} + {POSTS_DIR.relative_to(ROOT)}/",
        "id_ranges": {
            "main": {
                "min": min(main_ids_list) if main_ids_list else None,
                "max": max(main_ids_list) if main_ids_list else None,
                "next": max(main_ids_list) + 1 if main_ids_list else 1639,
            },
            "thematic": {
                "min": min(thematic_ids) if thematic_ids else None,
                "max": max(thematic_ids) if thematic_ids else None,
                "next": max(thematic_ids) + 1 if thematic_ids else 228,
                "prefix": "T-",
            },
        },
        "thematic_order": thematic_order,
        "nota": (
            f"Exportado de lawfare.json ({len(main)} entradas main, IDs "
            f"{main_ids_list[0] if main_ids_list else '?'}-{main_ids_list[-1] if main_ids_list else '?'}) "
            f"+ {len(thematic)} capítulos temáticos (T-{thematic_ids[0] if thematic_ids else '?'}"
            f"→T-{thematic_ids[-1] if thematic_ids else '?'}). "
            "Campo track: main | thematic. IDs originais preservados."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", "-o", default=str(DEFAULT_OUT.relative_to(ROOT)))
    parser.add_argument("--compact", action="store_true", help="JSON sem indentação")
    args = parser.parse_args()

    if not LAWFARE.exists():
        print(f"Erro: {LAWFARE} não encontrado.", file=sys.stderr)
        return 1

    out_path = ROOT / args.output
    payload = build_export()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=None if args.compact else 2)

    print(
        f"Exportados {payload['total']} assuntos "
        f"(main={payload['total_main']}, thematic={payload['total_thematic']}) -> {out_path}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
