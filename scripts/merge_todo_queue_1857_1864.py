#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Merge fila _data/todo/ 1857–1864 + T-253/T-254, evitando colisão de IDs.

Colisões resolvidas ANTES do merge:
  - Main 1857 aparece 3× (revisões do mesmo filtro X) → canônico: 1857(2)
  - Temático T-253 aparece 2× → AP 470 permanece T-253; P13 Porta Giratória → T-254
  - 1858–1864 e T-253/T-254 estão livres em lawfare.json / registry (last main 1856, last T 252)
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from merge_todo_queue_1850_1855 import (  # noqa: E402
    LAWFARE,
    POSTS,
    PROC,
    TODO,
    actors_people,
    build_corpus_index,
    connections_md as _connections_md,
    link_for_ref,
    linkify_inline,
    render_post as _render_post,
    render_thematic as _render_thematic,
    rewrite_connections_in_posts,
    slugify,
    to_assunto,
    yaml_escape,
)

CANON_1857 = "lawfare-batch-x-filtro-eleitoral-1857(2).json"
SUPERSEDED_1857 = [
    "lawfare-batch-x-filtro-eleitoral-1857.json",
    "lawfare-batch-x-filtro-eleitoral-1857(1).json",
]
FILE_1858 = "lawfare-batch-mendonca-itercast-1858.json"
FILE_1859 = "lawfare-batch-baptista-junior-1859-1860.json"
FILE_1861 = "lawfare-batch-p13-porta-giratoria-1861-1864.json"
FILE_T253 = "lawfare-thematic-T253-ap470-padrao-evidencial-lula.json"
FILE_T254_SRC = "lawfare-thematic-T253-p13-porta-giratoria.json"
FILE_T254_DST = "lawfare-thematic-T254-p13-porta-giratoria.json"

MAIN_RANGE = set(range(1857, 1865))
THEMATIC_IDS = {253, 254}


def occupied_main() -> set[int]:
    lf = json.loads(LAWFARE.read_text(encoding="utf-8"))
    return {a["id"] for a in lf.get("assuntos", []) if isinstance(a.get("id"), int)}


def extract_items(raw) -> list[dict]:
    if isinstance(raw, list):
        return raw
    if not isinstance(raw, dict):
        return []
    items: list[dict] = []
    for key in ("entries", "entradas", "assuntos", "main"):
        if isinstance(raw.get(key), list):
            items.extend(raw[key])
    if isinstance(raw.get("entry"), dict):
        items.append(raw["entry"])
    return items


def corpus_ref(val) -> str | None:
    s = str(val).strip()
    if re.match(r"^(?:id_)?\d+$", s, re.I):
        return s
    if re.match(r"^T-?\d+$", s, re.I):
        return s
    return None


def connections_md(conns: list, idx: dict) -> str:
    if not conns:
        return "- _N/A_"
    lines = []
    extras = []
    for c in conns:
        ref = corpus_ref(c)
        if ref:
            lines.append(f"- {link_for_ref(ref, idx)}")
        else:
            extras.append(f"- {c}")
    if extras:
        lines.append("")
        lines.append("### Notas de conexão (não-ID)")
        lines.extend(extras)
    return "\n".join(lines) if lines else "- _N/A_"


def resolve_category(entry: dict) -> str:
    eid = int(entry.get("id") or 0)
    title = (entry.get("title") or "").lower()
    if eid == 1857 or "electionfilter" in title or "filtro eleitoral" in title:
        return "tse"
    if eid == 1858 or "mendonça" in title or "mendonca" in title:
        return "stf"
    if eid == 1862 or "campos neto" in title or "nubank" in title:
        return "bancos"
    if eid in (1859, 1860, 1861, 1863, 1864):
        return "escandalos"
    return "escandalos"


def render_post(entry, category, source_file, idx):
    import merge_todo_queue_1850_1855 as m

    orig = m.connections_md
    m.connections_md = connections_md
    try:
        return _render_post(entry, category, source_file, idx)
    finally:
        m.connections_md = orig


def render_thematic(t, idx, source_file, cluster_label: str, next_note: str):
    import merge_todo_queue_1850_1855 as m

    orig = m.connections_md
    m.connections_md = connections_md
    try:
        body, path = _render_thematic(t, idx, source_file)
    finally:
        m.connections_md = orig
    # Replace hardcoded T-252 cluster heading / next-id note
    body = re.sub(
        r"### Cluster Lei 15\.487 / ANPD / Discord \(main track\)",
        f"### {cluster_label}",
        body,
        count=1,
    )
    body = re.sub(
        r"Thematic id T-\d+ — próximo livre após merge: T-\d+\. Main track deste cluster: 1850–1855\.",
        next_note,
        body,
        count=1,
    )
    return body, path


def prepare_queue() -> None:
    """Dedup 1857 + reassign P13 → T-254. Mutates files in todo/."""
    src1857 = TODO / CANON_1857
    if not src1857.is_file():
        raise SystemExit(f"ERRO: falta canônico {CANON_1857}")
    dst1857 = TODO / "lawfare-batch-x-filtro-eleitoral-1857.json"
    # Keep (2) as the named 1857 file for archive consistency
    data1857 = json.loads(src1857.read_text(encoding="utf-8"))
    if dst1857.exists() and dst1857.resolve() != src1857.resolve():
        # original 1857 is superseded; overwrite dest with canonical
        dst1857.write_text(
            json.dumps(data1857, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"CANON 1857 <- {CANON_1857}")
    else:
        shutil.copy2(src1857, dst1857)
        print(f"CANON 1857 copied <- {CANON_1857}")

    src_t254 = TODO / FILE_T254_SRC
    if src_t254.is_file():
        raw = json.loads(src_t254.read_text(encoding="utf-8"))
        if isinstance(raw.get("_meta"), dict):
            raw["_meta"]["reassigned_from"] = "T-253"
            raw["_meta"]["thematic_id"] = "T-254"
            raw["_meta"]["collision_note"] = (
                "T-253 já ocupado na fila por AP 470 (Mensalão). "
                "P13 Porta Giratória realocado para T-254 (próximo livre após T-253)."
            )
        entries = raw.get("entries") or []
        if entries:
            entries[0]["id"] = 254
            entries[0]["thematic_id"] = "T-254"
            title = entries[0].get("title") or ""
            entries[0]["title"] = re.sub(r"^T-253\b", "T-254", title)
        dst = TODO / FILE_T254_DST
        dst.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"REASSIGN {FILE_T254_SRC} -> {FILE_T254_DST} (T-254)")


def load_thematic_entry(path: Path) -> dict:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw.get("entries"), list) and raw["entries"]:
        e = dict(raw["entries"][0])
        tid = e.get("thematic_id") or e.get("id")
        e["id"] = tid if str(tid).startswith("T-") else f"T-{tid}"
        return e
    # top-level thematic (AP 470)
    return raw


def main() -> int:
    occ = occupied_main()
    clash = sorted(MAIN_RANGE & occ)
    if clash:
        print("ERRO: IDs main já ocupados em lawfare.json:", clash)
        return 1
    print(f"OK lawfare.json livre para {min(MAIN_RANGE)}–{max(MAIN_RANGE)} (occupied max={max(occ) if occ else '—'})")

    prepare_queue()

    # --- load main entries ---
    batches: list[tuple[str, list[dict]]] = []
    for fname in (
        "lawfare-batch-x-filtro-eleitoral-1857.json",
        FILE_1858,
        FILE_1859,
        FILE_1861,
    ):
        path = TODO / fname
        if not path.is_file():
            print(f"ERRO: falta {fname}")
            return 1
        items = extract_items(json.loads(path.read_text(encoding="utf-8")))
        batches.append((fname, items))
        ids = [int(i["id"]) for i in items]
        print(f"  {fname}: IDs {ids}")

    all_main: list[tuple[str, dict]] = []
    seen: set[int] = set()
    for fname, items in batches:
        for e in items:
            eid = int(e["id"])
            if eid in seen:
                print(f"ERRO: ID {eid} duplicado na fila após dedup")
                return 1
            if eid in occ:
                print(f"ERRO: ID {eid} colide com lawfare.json")
                return 1
            seen.add(eid)
            all_main.append((fname, e))

    expected = set(range(1857, 1865))
    if seen != expected:
        print(f"ERRO: IDs main esperados {sorted(expected)}, obtidos {sorted(seen)}")
        return 1

    t253 = load_thematic_entry(TODO / FILE_T253)
    t254_path = TODO / FILE_T254_DST
    if not t254_path.is_file():
        print("ERRO: T-254 não gerado")
        return 1
    t254 = load_thematic_entry(t254_path)
    print(f"  thematic: {t253.get('id')} / {t254.get('id')}")

    # --- write posts ---
    import merge_todo_queue_1850_1855 as m

    m.resolve_category = resolve_category
    m.connections_md = connections_md

    lawfare = json.loads(LAWFARE.read_text(encoding="utf-8"))
    assuntos = lawfare.get("assuntos") or []
    by_id = {a["id"]: a for a in assuntos if isinstance(a.get("id"), int)}

    idx = build_corpus_index()
    pending_titles = {str(int(e["id"])): e.get("title") or "" for _, e in all_main}
    pending_titles["T-253"] = t253.get("title") or ""
    pending_titles["T-254"] = t254.get("title") or ""
    idx.update({k: {"title": v, "permalink": "#", "path": ""} for k, v in pending_titles.items()})
    for k, v in list(pending_titles.items()):
        if k.isdigit():
            idx[f"id_{k}"] = idx[k]

    touched: list[Path] = []

    for fname, entry in all_main:
        cat = resolve_category(entry)
        assunto = to_assunto(entry, cat, fname)
        assunto["fonte_arquivo"] = f"_data/processados/{fname}"
        eid = int(entry["id"])
        if eid in by_id:
            by_id[eid].clear()
            by_id[eid].update(assunto)
            print(f"PATCH lawfare {eid}")
        else:
            assuntos.append(assunto)
            print(f"ADD lawfare {eid}")
        date = str(entry["date"])[:10]
        fname_md = f"{date}-{slugify(entry['title'])}.md"
        per = f"/posts/{Path(fname_md).stem}/"
        idx[str(eid)] = {"title": entry["title"], "permalink": per, "path": ""}
        idx[f"id_{eid}"] = idx[str(eid)]

    # refresh index after permalinks known, then write
    for fname, entry in all_main:
        cat = resolve_category(entry)
        body, out_path, per = render_post(entry, cat, fname, idx)
        out_path.write_text(body, encoding="utf-8")
        touched.append(out_path)
        idx[str(int(entry["id"]))] = {
            "title": entry["title"],
            "permalink": per,
            "path": str(out_path),
        }
        idx[f"id_{int(entry['id'])}"] = idx[str(int(entry["id"]))]
        print(f"WRITE post {entry['id']} -> {out_path.relative_to(ROOT)}")

    body253, out253 = render_thematic(
        t253,
        idx,
        FILE_T253,
        "Comparandum evidencial (AP 470 / Mensalão)",
        "Thematic id T-253 — próximo livre após este merge: T-255 (T-254 = P13 Porta Giratória).",
    )
    out253.write_text(body253, encoding="utf-8")
    touched.append(out253)
    idx["T-253"] = {"title": t253.get("title") or "", "permalink": f"/posts/{out253.stem}/", "path": str(out253)}
    print(f"WRITE T-253 -> {out253.relative_to(ROOT)}")

    body254, out254 = render_thematic(
        t254,
        idx,
        FILE_T254_DST,
        "Cluster P13 Porta Giratória (main track 1859–1864)",
        "Thematic id T-254 — próximo livre: T-255. Main track âncoras: 1859–1864. P13 em METHODOLOGY.md permanece proposta até formalização.",
    )
    out254.write_text(body254, encoding="utf-8")
    touched.append(out254)
    idx["T-254"] = {"title": t254.get("title") or "", "permalink": f"/posts/{out254.stem}/", "path": str(out254)}
    print(f"WRITE T-254 -> {out254.relative_to(ROOT)}")

    idx = build_corpus_index()
    rewrite_connections_in_posts(touched, idx)

    assuntos.sort(key=lambda a: (a.get("data_evento") or "", a.get("id") or 0))
    lawfare["assuntos"] = assuntos
    lawfare["total"] = len(assuntos)
    if "data_extração" in lawfare:
        lawfare["data_extração"] = "2026-08-19"
    LAWFARE.write_text(json.dumps(lawfare, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ids = [a["id"] for a in assuntos if isinstance(a.get("id"), int)]
    print(f"lawfare.json total={len(assuntos)} max={max(ids)}")

    PROC.mkdir(parents=True, exist_ok=True)
    to_archive = [
        CANON_1857,
        *SUPERSEDED_1857,
        "lawfare-batch-x-filtro-eleitoral-1857.json",
        FILE_1858,
        FILE_1859,
        FILE_1861,
        FILE_T253,
        FILE_T254_SRC,
        FILE_T254_DST,
    ]
    seen_names: set[str] = set()
    for name in to_archive:
        src = TODO / name
        if not src.is_file() or name in seen_names:
            continue
        seen_names.add(name)
        dst = PROC / name
        shutil.copy2(src, dst)
        src.unlink()
        print(f"Arquivado: {name}")

    print("OK merge 1857–1864 + T-253 + T-254")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
