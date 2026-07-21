#!/usr/bin/env python3
"""Patch claude.ai-corpus-ids-sync.json: T-224 + historical_precedents track."""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYNC = ROOT / "_data" / "claude.ai-corpus-ids-sync.json"
PREC = ROOT / "_data" / "precedentes-republica.json"

data = json.loads(SYNC.read_text(encoding="utf-8"))
prec = json.loads(PREC.read_text(encoding="utf-8"))
prec_ids = [e["id"] for e in prec["entradas"]]
today = date.today().isoformat()

thematic = data["tracks"]["thematic"]
entries = thematic["entries"]
by_id = {e["id"]: e for e in entries}

t224 = {
    "id": 224,
    "status": "confirmed",
    "topic": "Precedentes República 1891–1930 — sidecar PREC-* (T-224)",
    "artifact": "2026-07-19-precedentes-republica-1891-1930",
    "notes": "Estudo Jekyll _posts/estudos/2026-07-19-precedentes-republica-1891-1930.md · sidecar _data/precedentes-republica.json",
}
if 224 in by_id:
    by_id[224].update(t224)
else:
    entries.append(t224)
entries.sort(key=lambda e: e["id"])
thematic["entries"] = entries
thematic["last_id"] = 224
thematic["next_available"] = 225

data["tracks"]["historical_precedents"] = {
    "description": "Sidecar pre-1990 — namespace PREC-AAAA-NN (não mesclado em lawfare.json)",
    "id_format": "PREC-AAAA-NN",
    "source_file": "_data/precedentes-republica.json",
    "periodo": "1890-1930",
    "total": len(prec_ids),
    "last_id": prec_ids[-1],
    "index_thematic": "T-224",
    "entries": prec_ids,
    "status": "confirmed",
    "last_sync": today,
}

sync = data["sync_status"]
sync["thematic_track_last_sync"] = today
sync["ids_confirmed_total"]["thematic_track"] = 224
note = f"T-224 Precedentes República 1891-1930 publicado ({today}) — sidecar historical_precedents"
if note not in sync.get("open_items", []):
    sync.setdefault("open_items", []).append(note)
lawfare_note = "lawfare.json last_id=1628; próximo ID livre=1629"
open_items = sync.get("open_items", [])
sync["open_items"] = [x for x in open_items if not x.startswith("lawfare.json last_id=")]
sync["open_items"].append(lawfare_note)

SYNC.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Patched {SYNC.name}: thematic last_id=224, historical_precedents={len(prec_ids)} entries")
