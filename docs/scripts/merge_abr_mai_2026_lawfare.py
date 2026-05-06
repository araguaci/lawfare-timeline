#!/usr/bin/env python3
"""Acrescenta em lawfare.json posts de _posts com 2026-04-*.md e 2026-05-*.md ainda ausentes."""
from __future__ import annotations

import importlib.util
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "_data" / "lawfare.json"


def _load_extractor():
    spec = importlib.util.spec_from_file_location(
        "extrair_posts", ROOT / "scripts" / "extrair_posts_para_json.py"
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


def norm_key(p: str) -> str:
    return p.replace("/", "\\")


def main() -> None:
    mod = _load_extractor()
    data = json.loads(FULL.read_text(encoding="utf-8"))
    assuntos: list = data["assuntos"]
    existing = {norm_key(a.get("fonte_arquivo") or "") for a in assuntos}
    posts_dir = ROOT / "_posts"

    candidates = sorted(
        list(posts_dir.glob("**/2026-04-*.md")) + list(posts_dir.glob("**/2026-05-*.md")),
        key=lambda p: str(p),
    )
    to_add = [
        p
        for p in candidates
        if norm_key(str(p.relative_to(ROOT))) not in existing
    ]

    def sort_key(fp: Path):
        txt = fp.read_text(encoding="utf-8", errors="replace")
        front, _ = mod.parse_front_matter(txt)
        de, _ = mod.extract_date(front, fp)
        return (de, str(fp))

    novos = []
    for fp in sorted(to_add, key=sort_key):
        item = mod.process_post(fp, ROOT, posts_dir)
        if item:
            novos.append(item)

    max_id = max((a.get("id") or 0) for a in assuntos) if assuntos else 0
    for i, item in enumerate(novos):
        item["id"] = max_id + 1 + i

    assuntos.extend(novos)
    data["assuntos"] = assuntos
    data["total"] = len(assuntos)
    data["data_extração"] = date.today().isoformat()

    datas = [
        a["data_evento"]
        for a in assuntos
        if a.get("data_evento") and a["data_evento"] != "0001-01-01"
    ]
    if datas:
        data["periodo"] = f"{min(datas)} a {max(datas)}"

    n = len(novos)
    data["nota"] = (
        "Extraído automaticamente de _posts por scripts/extrair_posts_para_json.py. "
        f"Atualizado em {date.today().isoformat()}: inclusão de {n} entradas novas de abril e maio/2026 "
        "(ausentes do JSON). Maio/2026: entradas só se existirem _posts/.../2026-05-*.md."
    )

    FULL.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Adicionados: {n} (ids {max_id + 1} … {max_id + n})")
    print(f"Total: {data['total']}")


if __name__ == "__main__":
    main()
