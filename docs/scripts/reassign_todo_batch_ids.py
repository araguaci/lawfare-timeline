#!/usr/bin/env python3
"""Realoca IDs em batches _data/todo/ para sequência livre em lawfare.json."""
from __future__ import annotations

import json
import re
import shutil
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODO = ROOT / "_data" / "todo"
HOLD = TODO / "_hold"
LAWFARE = ROOT / "_data" / "lawfare.json"
SYNC = ROOT / "_data" / "claude.ai-corpus-ids-sync.json"

# Ordem de merge (arquivo relativo a TODO ou HOLD)
MERGE_ORDER: list[tuple[str, list[int] | None]] = [
    ("lawfare-batch-radiolao-machado-1889-1897.json", [1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897]),
    ("lawfare-batch-auditoria-mapa-conexoes-T263.json", None),
    ("lawfare-batch-inq4781-cronologia-1889-1898.json", None),
]


def occupied_ids() -> set[int]:
    lf = json.loads(LAWFARE.read_text(encoding="utf-8"))
    return {a["id"] for a in lf.get("assuntos", []) if isinstance(a.get("id"), int)}


def next_free(start: int, taken: set[int]) -> int:
    n = start
    while n in taken:
        n += 1
    return n


def is_pending_id(val) -> bool:
    if val == "__PENDENTE_SYNC__":
        return True
    return isinstance(val, str) and "PENDENTE" in val.upper()


def occupied_thematic() -> set[int]:
    sync = json.loads(SYNC.read_text(encoding="utf-8"))
    entries = sync.get("tracks", {}).get("thematic", {}).get("entries", [])
    return {int(e["id"]) for e in entries if isinstance(e.get("id"), int)}


def parse_thematic_num(val) -> int | None:
    if isinstance(val, str):
        m = re.match(r"^T-(\d+)$", val.strip(), re.I)
        if m:
            return int(m.group(1))
    return None


def coerce_main_id(val):
    if isinstance(val, int):
        return val
    if isinstance(val, str) and val.isdigit():
        return int(val)
    return val


def batch_slices(raw: dict | list) -> tuple[list[dict], list[dict], dict | list]:
    """Retorna (main_items, thematic_items, raw) para escrita."""
    if isinstance(raw, list):
        return raw, [], raw
    if not isinstance(raw, dict):
        return [], [], raw
    main: list[dict] = []
    thematic: list[dict] = []
    if isinstance(raw.get("main"), list):
        main.extend(raw["main"])
    if isinstance(raw.get("entries"), list):
        main.extend(raw["entries"])
    if isinstance(raw.get("entries_main"), list):
        main.extend(raw["entries_main"])
    if isinstance(raw.get("entradas"), list):
        main.extend(raw["entradas"])
    if isinstance(raw.get("assuntos"), list):
        for item in raw["assuntos"]:
            if not isinstance(item, dict):
                continue
            if item.get("id") is None and item.get("id_corpus"):
                item["id"] = item["id_corpus"]
            if parse_thematic_num(item.get("id") or item.get("id_corpus")) is not None:
                thematic.append(item)
            else:
                main.append(item)
    if isinstance(raw.get("entry"), dict):
        main.append(raw["entry"])
    if isinstance(raw.get("thematic"), list):
        thematic.extend(raw["thematic"])
    if isinstance(raw.get("entries_thematic"), list):
        thematic.extend(raw["entries_thematic"])
    if isinstance(raw.get("thematic_entries"), list):
        thematic.extend(raw["thematic_entries"])
    return main, thematic, raw


def load_items(path: Path) -> list[dict]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    main, thematic, _ = batch_slices(raw)
    return main + thematic


def save_items(path: Path, items: list[dict], original: dict | list) -> None:
    if isinstance(original, list):
        path.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return
    if isinstance(original, dict) and "entry" in original:
        out = deepcopy(original)
        out["entry"] = items[0] if len(items) == 1 else items
        path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return
    if isinstance(original, dict) and (
        "entries" in original or "entradas" in original or "assuntos" in original
    ):
        out = deepcopy(original)
        if "assuntos" in original:
            out["assuntos"] = items
        else:
            key = "entries" if "entries" in original else "entradas"
            out[key] = items
        path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return
    if isinstance(original, dict) and ("main" in original or "thematic" in original):
        out = deepcopy(original)
        n_main = len(original.get("main") or [])
        n_th = len(original.get("thematic") or [])
        if n_main:
            out["main"] = items[:n_main]
        if n_th:
            out["thematic"] = items[n_main : n_main + n_th]
        path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return
    path.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def remap_connections(text: str, mapping: dict[int, int]) -> str:
    def repl(m: re.Match) -> str:
        old = int(m.group(1))
        new = mapping.get(old, old)
        return f"id_{new}"

    return re.sub(r"id_(\d+)", repl, text)


def apply_id_map(item: dict, id_map: dict[int, int]) -> None:
    old = coerce_main_id(item.get("id"))
    if isinstance(item.get("id"), str) and parse_thematic_num(item.get("id")) is not None:
        pass
    elif isinstance(old, int) and old in id_map:
        item["id"] = id_map[old]
    elif old == "__PENDENTE_SYNC__":
        pass
    for key in ("connections", "lacuna_investigativa", "analise", "summary", "descricao", "resumo"):
        val = item.get(key)
        if isinstance(val, str):
            item[key] = remap_connections(val, id_map)
        elif isinstance(val, list):
            item[key] = [
                remap_connections(v, id_map) if isinstance(v, str) else v for v in val
            ]


def main() -> None:
    sync = json.loads(SYNC.read_text(encoding="utf-8"))
    cursor = int(sync.get("tracks", {}).get("main", {}).get("next_available", 1827))
    th_cursor = int(sync.get("tracks", {}).get("thematic", {}).get("next_available", 249))
    taken = occupied_ids()
    th_taken = occupied_thematic()
    log: list[str] = []

    for rel, fixed_ids in MERGE_ORDER:
        path = TODO / rel if not rel.startswith("_hold/") else ROOT / "_data" / "todo" / rel
        if not path.exists():
            log.append(f"SKIP ausente: {rel}")
            continue

        raw = json.loads(path.read_text(encoding="utf-8"))
        main_items, thematic_items, _ = batch_slices(raw)
        items = main_items + thematic_items
        if not items:
            log.append(f"SKIP vazio: {rel}")
            continue

        id_map: dict[int, int] = {}
        leftover_thematic: list[dict] = []
        if fixed_ids is not None:
            if len(fixed_ids) != len(main_items):
                raise SystemExit(f"{rel}: esperado {len(fixed_ids)} main, tem {len(main_items)}")
            for item, nid in zip(main_items, fixed_ids):
                old = coerce_main_id(item.get("id"))
                if isinstance(old, int) and old != nid:
                    id_map[old] = nid
                item["id"] = nid
                taken.add(nid)
            cursor = max(cursor, max(fixed_ids) + 1)
        else:
            kept_main: list[dict] = []
            for item in main_items:
                cat = (
                    item.get("category")
                    or item.get("categoria")
                    or item.get("tipo")
                    or ""
                ).lower()
                old = coerce_main_id(item.get("id"))
                if cat == "analise_editorial" and parse_thematic_num(item.get("id")) is None:
                    new_t = th_cursor
                    while new_t in th_taken:
                        new_t += 1
                    item["id"] = f"T-{new_t}"
                    th_taken.add(new_t)
                    th_cursor = new_t + 1
                    leftover_thematic.append(item)
                    continue
                if is_pending_id(old):
                    nid = next_free(cursor, taken)
                    item["id"] = nid
                    taken.add(nid)
                    cursor = nid + 1
                    kept_main.append(item)
                    continue
                if not isinstance(old, int):
                    kept_main.append(item)
                    continue
                if old in taken:
                    nid = next_free(cursor, taken)
                    id_map[old] = nid
                    item["id"] = nid
                    taken.add(nid)
                    cursor = nid + 1
                else:
                    item["id"] = old
                    taken.add(old)
                    cursor = max(cursor, old + 1)
                kept_main.append(item)
            main_items[:] = kept_main
            thematic_items.extend(leftover_thematic)
            items[:] = main_items + thematic_items

        assigned_this_file = {
            parse_thematic_num(it.get("id"))
            for it in leftover_thematic
        } if fixed_ids is None else set()
        for item in thematic_items:
            old_t = parse_thematic_num(item.get("id"))
            if old_t is None:
                continue
            if old_t in assigned_this_file:
                continue
            if old_t in th_taken:
                new_t = th_cursor
                while new_t in th_taken:
                    new_t += 1
                if old_t != new_t:
                    id_map[old_t] = new_t  # só conexões id_NNN; T remapped abaixo
                item["id"] = f"T-{new_t}"
                th_taken.add(new_t)
                th_cursor = new_t + 1
            else:
                item["id"] = f"T-{old_t}"
                th_taken.add(old_t)
                th_cursor = max(th_cursor, old_t + 1)

        for item in items:
            apply_id_map(item, id_map)

        save_items(path, items, raw)
        new_ids = [item.get("id") for item in items]
        log.append(f"OK {path.name}: IDs {new_ids}")

        # batches em _hold passam para todo/ após realocação
        if rel.startswith("_hold/"):
            dest = TODO / path.name
            if not dest.exists():
                shutil.copy2(path, dest)
                log.append(f"  -> copiado para _data/todo/{path.name}")

    # T-247: flatten entry para sync temático
    t247 = TODO / "lawfare-thematic-T247-dedo-na-balanca-t2-video-ia.json"
    if t247.exists():
        data = json.loads(t247.read_text(encoding="utf-8"))
        if isinstance(data.get("entry"), dict) and "summary" not in data:
            entry = data["entry"]
            merged = {**entry, "_meta": data.get("_meta"), "_source_file": t247.name}
            t247.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            log.append("OK T-247: entry flatten para sync temático")

    print("\n".join(log))
    print(f"\nPróximo ID livre sugerido: {cursor}")


if __name__ == "__main__":
    main()
