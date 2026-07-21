#!/usr/bin/env python3
"""Merge batch entries into lawfare.json when posts already exist (no Jekyll rewrite)."""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from sync_todo_current import normalize_main_entry, to_lawfare_assunto  # noqa: E402

LAWFARE = ROOT / "_data" / "lawfare.json"
BATCH = ROOT / "_data" / "processados" / "lawfare-batch-1631-1635-varredura-jul2026.json"


def main() -> int:
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    lf = json.loads(LAWFARE.read_text(encoding="utf-8"))
    assuntos = lf.get("assuntos", [])
    existing = {a["id"] for a in assuntos if a.get("id")}

    added = []
    for item in batch.get("entries", []):
        mid = int(item["id"])
        if mid in existing:
            print(f"  SKIP {mid} — ja em lawfare.json")
            continue
        u = normalize_main_entry(item, BATCH.name)
        if not u:
            print(f"  ERRO normalizar {mid}")
            return 1
        assuntos.append(to_lawfare_assunto(u, u["jekyll_categories"][0]))
        added.append(mid)

    if not added:
        print("Nada a reconciliar.")
        return 0

    assuntos.sort(key=lambda x: x.get("id") or 0)
    lf["assuntos"] = assuntos
    lf["total"] = len(assuntos)
    lf["data_extração"] = date.today().isoformat()
    datas = [a["data_evento"] for a in assuntos if a.get("data_evento") and a["data_evento"] != "0001-01-01"]
    if datas:
        lf["periodo"] = f"{min(datas)} a {max(datas)}"
    LAWFARE.write_text(json.dumps(lf, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"lawfare.json: +{len(added)} IDs {added} (total {len(assuntos)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
