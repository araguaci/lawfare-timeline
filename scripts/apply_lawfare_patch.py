#!/usr/bin/env python3
"""Aplica patches pontuais em lawfare.json (ex.: correção parser id_1100)."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAWFARE = ROOT / "_data" / "lawfare.json"
TODO = ROOT / "_data" / "todo"
PROC = ROOT / "_data" / "processados"


def apply_patch(patch_path: Path) -> bool:
    patch = json.loads(patch_path.read_text(encoding="utf-8"))
    target_id = patch.get("patch_target_id")
    fields = patch.get("campos_corrigidos") or {}
    if target_id is None or not fields:
        print(f"SKIP {patch_path.name}: patch inválido")
        return False

    lf = json.loads(LAWFARE.read_text(encoding="utf-8"))
    items = lf.get("assuntos") or []
    idx = next((i for i, a in enumerate(items) if a.get("id") == target_id), None)
    if idx is None:
        print(f"SKIP {patch_path.name}: id {target_id} não encontrado")
        return False

    item = items[idx]
    mapping = {
        "titulo": "titulo",
        "descricao": "descricao",
        "pessoas_envolvidas": "pessoas_envolvidas",
        "instituicoes_envolvidas": "instituicoes_envolvidas",
        "fontes": "fontes",
        "connections": "connections",
        "nota_metodologica": "nota_metodologica",
        "analise": "analise",
        "lacuna_investigativa": "lacuna_investigativa",
    }
    for src, dst in mapping.items():
        if src in fields:
            item[dst] = fields[src]
    if fields.get("evidence_status"):
        tags = list(item.get("tags") or [])
        if fields["evidence_status"] not in tags:
            tags.append(fields["evidence_status"])
        item["tags"] = tags
    if patch.get("descricao_bug"):
        item["nota_correcao_parser"] = patch["descricao_bug"]

    items[idx] = item
    lf["assuntos"] = items
    LAWFARE.write_text(json.dumps(lf, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PROC.mkdir(parents=True, exist_ok=True)
    dst = PROC / patch_path.name
    if patch_path.exists():
        shutil.move(str(patch_path), str(dst))
    print(f"PATCHED id_{target_id} <- {patch_path.name}")
    return True


def main() -> None:
    patches = sorted(TODO.glob("patch-*.json"))
    if not patches:
        print("Nenhum patch em _data/todo/")
        return
    ok = sum(apply_patch(p) for p in patches)
    print(f"Total aplicados: {ok}/{len(patches)}")


if __name__ == "__main__":
    main()
