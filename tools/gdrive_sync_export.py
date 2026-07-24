#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exporta _data/claude.ai-corpus-ids-sync.json para Google Drive.

Chamado automaticamente por sync_corpus_ids.py e sync_todo_current.py após
atualizar o arquivo de sync. Também pode ser executado manualmente:

  python tools/gdrive_sync_export.py
  python tools/gdrive_sync_export.py --dry-run

Configuração (prioridade):
  1. Variável de ambiente LAWFARE_GDRIVE_SYNC_DIR (pasta de destino)
  2. _data/gdrive-sync-export.json (dest_dir, subfolder, enabled)
  3. Detecção automática de Google Drive / Meu Drive no Windows
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYNC = ROOT / "_data" / "claude.ai-corpus-ids-sync.json"
CONFIG = ROOT / "_data" / "gdrive-sync-export.json"
CONFIG_EXAMPLE = ROOT / "_data" / "gdrive-sync-export.example.json"

GDRIVE_ROOT_CANDIDATES = (
    lambda: Path(os.environ.get("LAWFARE_GDRIVE_ROOT", "")),
    lambda: Path.home() / "Google Drive",
    lambda: Path.home() / "My Drive",
    lambda: Path("G:/My Drive"),
    lambda: Path("G:/Meu Drive"),
    lambda: Path("D:/Google Drive"),
    lambda: Path("D:/Meu Drive"),
)


def load_config() -> dict:
    path = CONFIG if CONFIG.is_file() else CONFIG_EXAMPLE
    if not path.is_file():
        return {"enabled": True, "dest_dir": "", "subfolder": "lawfare-timeline"}
    return json.loads(path.read_text(encoding="utf-8"))


def _valid_dir(p: Path) -> bool:
    if not p or not str(p).strip():
        return False
    try:
        resolved = p.resolve()
    except OSError:
        return False
    if resolved == ROOT.resolve():
        return False
    return p.is_dir()


def detect_gdrive_root() -> Path | None:
    for factory in GDRIVE_ROOT_CANDIDATES:
        try:
            p = factory()
        except (OSError, TypeError):
            continue
        if _valid_dir(p):
            return p
    return None


def resolve_dest_dir(config: dict) -> Path | None:
    env_dir = os.environ.get("LAWFARE_GDRIVE_SYNC_DIR", "").strip()
    if env_dir:
        return Path(env_dir)

    dest = (config.get("dest_dir") or "").strip()
    if dest:
        return Path(dest)

    root = detect_gdrive_root()
    if not root:
        return None

    subfolder = (config.get("subfolder") or "").strip()
    return root / subfolder if subfolder else root


def export_sync_to_gdrive(*, dry_run: bool = False, quiet: bool = False) -> bool:
    config = load_config()
    if not config.get("enabled", True):
        if not quiet:
            print("gdrive export: desabilitado em gdrive-sync-export.json")
        return False

    if not SYNC.is_file():
        if not quiet:
            print(f"gdrive export: arquivo ausente — {SYNC}")
        return False

    dest_dir = resolve_dest_dir(config)
    if dest_dir is None:
        if not quiet:
            print(
                "gdrive export: destino não configurado (Google Drive não detectado). "
                "Defina LAWFARE_GDRIVE_SYNC_DIR ou dest_dir em "
                f"_data/{CONFIG.name}."
            )
        return False

    try:
        dest_resolved = dest_dir.resolve()
    except OSError:
        dest_resolved = dest_dir
    if dest_resolved == ROOT.resolve():
        if not quiet:
            print("gdrive export: destino não pode ser a raiz do repositório.")
        return False

    filename = config.get("dest_filename") or "claude.ai-corpus-ids-sync.json"
    dest_file = dest_dir / filename

    if dry_run:
        print(f"gdrive export [dry-run]: {SYNC} -> {dest_file}")
        return True

    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SYNC, dest_file)
    except OSError as exc:
        print(f"gdrive export ERRO: {exc}", file=sys.stderr)
        return False

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    meta = {
        "exported_at": stamp,
        "source": str(SYNC.relative_to(ROOT)).replace("\\", "/"),
        "dest": str(dest_file),
        "main_last_id": _peek_main_last_id(),
    }
    meta_path = dest_dir / f"{filename}.export-meta.json"
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if not quiet:
        print(f"gdrive export OK: {dest_file}")
    return True


def _peek_main_last_id() -> int | None:
    try:
        data = json.loads(SYNC.read_text(encoding="utf-8"))
        main = data.get("tracks", {}).get("main", {})
        return main.get("last_id") or main.get("last_confirmed")
    except (OSError, json.JSONDecodeError):
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Exporta claude.ai-corpus-ids-sync.json para Google Drive")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Retorna código 1 se export falhar (padrão: 0 quando Drive não configurado)",
    )
    args = ap.parse_args()
    ok = export_sync_to_gdrive(dry_run=args.dry_run, quiet=args.quiet)
    if ok:
        return 0
    config = load_config()
    dest_missing = resolve_dest_dir(config) is None and not args.dry_run
    if dest_missing and not args.strict:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
