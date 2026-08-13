#!/usr/bin/env python3
"""Normalize JustiçaWatch / decisões sidecar into JusMonitor-shaped cards.

Reads justicawatch-brasil.json (T-209) from this folder or sibling path and
writes decisoes-seed.json suitable for jusmonitor.vercel.app/data/decisoes-source.json.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANDIDATES = [
    HERE / "justicewatch" / "justicawatch-brasil.json",
    HERE / "justicawatch-brasil.json",
]


def main() -> None:
    src = next((p for p in CANDIDATES if p.exists()), None)
    if not src:
        raise SystemExit("justicawatch-brasil.json not found — place under _data/justicewatch/")
    data = json.loads(src.read_text(encoding="utf-8"))
    out = HERE / "justicewatch" / "decisoes-seed.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    # Pass-through: JusMonitor build-unified normalizes casos[] → cards
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK wrote {out} ({len(data.get('casos', []))} casos)")


if __name__ == "__main__":
    main()
