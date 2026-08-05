#!/usr/bin/env python3
"""Corrige last_id/next_available do track temático (T-NNN, não main)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYNC = ROOT / "_data/claude.ai-corpus-ids-sync.json"

sync = json.loads(SYNC.read_text(encoding="utf-8"))
th = sync.setdefault("tracks", {}).setdefault("thematic", {})
entries = th.get("entries", [])
# Remove entradas temáticas espúrias (IDs main >= 1000 tratados como T-NNN)
entries = [e for e in entries if int(e.get("id", 0)) < 1000]
th["entries"] = entries
if entries:
    last = max(int(e["id"]) for e in entries)
    th["last_id"] = last
    th["next_available"] = last + 1
SYNC.write_text(json.dumps(sync, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"thematic last_id={th.get('last_id')} next={th.get('next_available')} ({len(entries)} entries)")
