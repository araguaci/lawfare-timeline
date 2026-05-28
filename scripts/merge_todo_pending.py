#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Resolve conflitos de ID nos batches _data/todo e publica posts Jekyll.

Renumeracao:
  Biomm 1481-1500 -> 1527-1546 (1481-1500 reservados PCC/Ndrangheta)
  Zema 185-188     -> 1547-1550 (185-188 reservados thematic/Dosimetria)
  Homeschooling    -> 1551      (1425 ocupado por Mare Liberum)
  Direita Permitida thematic 189 -> 190 (T-189 = Reforma Tributaria)

Uso: python scripts/merge_todo_pending.py [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODO = ROOT / "_data" / "todo"
PROC = ROOT / "_data" / "processados"
POSTS = ROOT / "_posts"
SYNC = ROOT / "_data" / "claude.ai-corpus-ids-sync.json"

BIOMM_MAP = {old: 1527 + (old - 1481) for old in range(1481, 1501)}
ZEMA_MAP = {185: 1547, 186: 1548, 187: 1549, 188: 1550}
HOMESCHOOL_ID = 1551
LAST_MAIN_ID = 1551
NEXT_MAIN_ID = 1552

IMAGE_BY_CATEGORY = {
    "escandalos": "/assets/solid/skull.svg",
    "bancos": "/assets/solid/landmark.svg",
    "operacoes": "/assets/solid/bullseye.svg",
    "governo": "/assets/solid/sitemap.svg",
    "justica": "/assets/solid/hammer.svg",
    "lawfare": "/assets/solid/weight-scale.svg",
}


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")[:90]


def yaml_escape(s: str) -> str:
    return s.replace('"', '\\"')


def resolve_category(entry: dict) -> str:
    cat = (entry.get("categoria") or entry.get("category") or "").lower()
    tags = [str(t).lower() for t in entry.get("tags") or []]
    mapping = {
        "captura-institucional": "escandalos",
        "conflito-de-interesses": "escandalos",
        "operacao": "operacoes",
        "operacoes": "operacoes",
        "judicial": "justica",
        "documentado": "escandalos",
    }
    if cat in mapping:
        return mapping[cat]
    if "operacao-rejeito" in tags or "operacao" in cat:
        return "operacoes"
    if "zema" in tags or "mineracao" in tags:
        return "escandalos"
    if "homeschooling" in tags or cat == "judicial":
        return "justica"
    if any(k in cat for k in ("banco", "master", "biomm")):
        return "escandalos"
    return "escandalos"


def format_iso(d: str) -> str:
    return f"{(d or '2026-01-01')[:10]}T12:00:00.000Z"


def normalize_biomm(raw: dict, new_id: int) -> dict:
    old_id = raw["id"]
    title = raw["titulo"]
    jdate = raw["data_evento"]
    cat = resolve_category(raw)
    fname = f"{jdate}-{slugify(title)}.md"
    note = f"Renumerado de {old_id} (faixa 1481-1500 reservada PCC/Ndrangheta)."
    return {
        "id_corpus": str(new_id),
        "id_original": old_id,
        "conflito_nota": note,
        "jekyll_filename": fname,
        "jekyll_date": jdate,
        "jekyll_categories": [cat],
        "jekyll_tags": (raw.get("tags") or [])[:12],
        "jekyll_permalink": f"/posts/{Path(fname).stem}/",
        "titulo": title,
        "resumo": raw.get("descricao", ""),
        "categoria": raw.get("categoria", cat),
        "pais": raw.get("pais", "Brasil"),
        "atores": raw.get("pessoas_envolvidas") or [],
        "instituicoes": raw.get("instituicoes_envolvidas") or [],
        "fontes": raw.get("fontes") or [],
    }


def normalize_zema(raw: dict, new_id: int) -> dict:
    old_id = raw["id"]
    title = raw["title"]
    jdate = str(raw.get("date", ""))[:10]
    cat = resolve_category(raw)
    fname = f"{jdate}-{slugify(title)}.md"
    note = f"Renumerado de {old_id} (thematic 185-188 = Dosimetria)."
    actors = raw.get("actors") or []
    if actors and isinstance(actors[0], str):
        people = actors
    else:
        people = [f"{a.get('name', a)}" for a in actors if isinstance(a, dict)]
    return {
        "id_corpus": str(new_id),
        "id_original": old_id,
        "conflito_nota": note,
        "jekyll_filename": fname,
        "jekyll_date": jdate,
        "jekyll_categories": [cat],
        "jekyll_tags": (raw.get("tags") or [])[:12],
        "jekyll_permalink": f"/posts/{Path(fname).stem}/",
        "titulo": title,
        "resumo": raw.get("summary", ""),
        "categoria": cat,
        "pais": "Brasil",
        "atores": people,
        "instituicoes": [],
        "fontes": raw.get("sources") or [],
        "_analise": raw.get("analytical_note", ""),
        "_patterns": raw.get("patterns") or [],
    }


def normalize_homeschool(raw: dict) -> dict:
    title = raw["title"]
    jdate = raw["date"]
    cat = "justica"
    fname = f"{jdate}-{slugify(title)}.md"
    note = "Renumerado de 1425 (1425 = Mare Liberum Galeao no corpus)."
    actors = []
    for a in raw.get("actors") or []:
        if isinstance(a, dict):
            actors.append(f"{a.get('name', '')} ({a.get('role', '')})".strip(" ()"))
    sources = raw.get("sources") or []
    fontes = [s.get("url", s) if isinstance(s, dict) else s for s in sources]
    return {
        "id_corpus": str(HOMESCHOOL_ID),
        "id_original": raw["id"],
        "conflito_nota": note,
        "jekyll_filename": fname,
        "jekyll_date": jdate,
        "jekyll_categories": [cat],
        "jekyll_tags": (raw.get("tags") or [])[:12],
        "jekyll_permalink": f"/posts/{Path(fname).stem}/",
        "titulo": title,
        "resumo": raw.get("summary", ""),
        "categoria": cat,
        "pais": "Brasil",
        "atores": actors,
        "instituicoes": [],
        "fontes": fontes,
        "_legal": (raw.get("legal_analysis") or {}).get("notas") or [],
    }


def render_post(u: dict) -> str:
    cats = u.get("jekyll_categories") or ["lawfare"]
    category = cats[0]
    tags = u.get("jekyll_tags") or []
    title = u["titulo"]
    resumo = u["resumo"]
    desc = yaml_escape((resumo[:157] + "…") if len(resumo) > 157 else resumo)
    image = IMAGE_BY_CATEGORY.get(category, "/assets/solid/circle-exclamation.svg")
    fm_tags = json.dumps(tags, ensure_ascii=False)
    perm = u.get("jekyll_permalink") or f"/posts/{Path(u['jekyll_filename']).stem}/"

    parts = [
        "- &nbsp;",
        "{:toc .large-only}",
        "",
        f"# {title}",
        "",
        "***",
        "",
        "## 🧭 Resumo",
        "",
        resumo,
        "",
        "***",
        "",
        "## 🏷️ Metadados do corpus",
        "",
        "| Campo | Valor |",
        "| --- | --- |",
        f"| `id_corpus` | **{u.get('id_corpus', '')}** |",
        f"| Categoria analítica | {u.get('categoria', '—')} |",
        f"| País / âmbito | {u.get('pais', '—')} |",
        "",
    ]
    if u.get("conflito_nota"):
        parts.extend([f"> **Nota de conflito ID:** {u['conflito_nota']}", ""])
    if u.get("atores"):
        parts.extend(["### Atores", ""] + [f"- {a}" for a in u["atores"]] + [""])
    if u.get("instituicoes"):
        parts.extend(["### Instituições", ""] + [f"- {i}" for i in u["instituicoes"]] + [""])
    if u.get("_analise"):
        parts.extend(["## Análise", "", u["_analise"], ""])
    if u.get("_patterns"):
        parts.extend(["## Padrões", ""] + [f"- {p}" for p in u["_patterns"]] + [""])
    if u.get("_legal"):
        parts.extend(["## Notas jurídicas", ""] + [f"- {x}" for x in u["_legal"]] + [""])
    fontes = u.get("fontes") or []
    if fontes:
        parts.extend(["## 📚 Fontes verificáveis", ""])
        for i, f in enumerate(fontes, 1):
            url = f if isinstance(f, str) else f.get("url", "")
            if url:
                parts.append(f"{i}. {url}")
        parts.append("")

    fm = f"""---
title: "{yaml_escape(title)}"
description: "{desc}"
date: {format_iso(u.get('jekyll_date', ''))}
image:
  path: "{image}"
tags: {fm_tags}
categories: {category}
permalink: {perm}
id_corpus: "{u.get('id_corpus', '')}"
corpus_unificado: true
---

"""
    return fm + "\n".join(parts)


def load_entries() -> list[dict]:
    entries: list[dict] = []

    biomm_path = TODO / "lawfare-1481-1500-merged.json"
    if biomm_path.is_file():
        biomm = json.loads(biomm_path.read_text(encoding="utf-8"))
        for raw in biomm:
            new_id = BIOMM_MAP[raw["id"]]
            entries.append(normalize_biomm(raw, new_id))

    zema_path = TODO / "ids-185-188-zema-mineracao.json"
    if zema_path.is_file():
        zema = json.loads(zema_path.read_text(encoding="utf-8"))
        for raw in zema:
            new_id = ZEMA_MAP[raw["id"]]
            entries.append(normalize_zema(raw, new_id))

    hs_path = TODO / "entry_1425_homeschooling_jales.json"
    if hs_path.is_file():
        hs = json.loads(hs_path.read_text(encoding="utf-8"))
        entries.append(normalize_homeschool(hs))

    return entries


def write_posts(entries: list[dict], dry_run: bool) -> int:
    n = 0
    for u in entries:
        cat = u["jekyll_categories"][0]
        target = POSTS / cat / u["jekyll_filename"]
        if dry_run:
            print(f"  [dry-run] {target.relative_to(ROOT)}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render_post(u), encoding="utf-8")
            print(f"  OK {target.relative_to(ROOT)}")
        n += 1
    return n


def renumber_json_files(dry_run: bool) -> None:
    biomm_src = TODO / "lawfare-1481-1500-merged.json"
    if biomm_src.is_file():
        data = json.loads(biomm_src.read_text(encoding="utf-8"))
        out = []
        for raw in data:
            old = raw["id"]
            new = BIOMM_MAP[old]
            item = dict(raw)
            item["id_original"] = old
            item["id"] = new
            item["conflito_nota"] = f"Renumerado de {old} (1481-1500 = PCC/Ndrangheta)."
            out.append(item)
        dst = PROC / "lawfare-1527-1546-biomm-renumerado.json"
        if not dry_run:
            PROC.mkdir(parents=True, exist_ok=True)
            dst.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"  JSON {dst.relative_to(ROOT)}")

    zema_src = TODO / "ids-185-188-zema-mineracao.json"
    if zema_src.is_file():
        data = json.loads(zema_src.read_text(encoding="utf-8"))
        out = []
        for raw in data:
            old = raw["id"]
            new = ZEMA_MAP[old]
            item = dict(raw)
            item["id_original"] = old
            item["id"] = new
            item["conflito_nota"] = f"Renumerado de {old} (thematic 185-188 = Dosimetria)."
            out.append(item)
        dst = PROC / "zema-1547-1550-renumerado.json"
        if not dry_run:
            dst.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"  JSON {dst.relative_to(ROOT)}")

    hs_src = TODO / "entry_1425_homeschooling_jales.json"
    if hs_src.is_file():
        data = json.loads(hs_src.read_text(encoding="utf-8"))
        data["id_original"] = data["id"]
        data["id"] = HOMESCHOOL_ID
        data["conflito_nota"] = "Renumerado de 1425 (1425 = Mare Liberum)."
        dst = PROC / "entry-1551-homeschooling-jales.json"
        if not dry_run:
            dst.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"  JSON {dst.relative_to(ROOT)}")

    direita_src = TODO / "lawfare-189-direita-permitida.json"
    if direita_src.is_file():
        data = json.loads(direita_src.read_text(encoding="utf-8"))
        if isinstance(data, list) and data:
            data[0]["id_original"] = data[0].get("id")
            data[0]["id"] = 190
            data[0]["id_display"] = "T-190"
            data[0]["conflito_nota"] = "Renumerado de 189 (T-189 = Reforma Tributaria)."
        dst = PROC / "thematic-190-direita-permitida.json"
        if not dry_run:
            dst.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"  JSON {dst.relative_to(ROOT)}")


def patch_estudos_frontmatter(dry_run: bool) -> None:
    patches = [
        (
            POSTS / "estudos" / "2026-05-26-reforma-tributaria-captura-regulatoria.md",
            'id_corpus: "T-189"\nthematic_track: true\n',
        ),
        (
            POSTS / "estudos" / "2026-05-22-direita-permitida-dossie.md",
            'id_corpus: "T-190"\nthematic_track: true\n',
        ),
        (
            POSTS / "estudos" / "2026-05-21-biomm-insider-operacao-completa.md",
            'id_corpus: "1527-1546"\nthematic_track: false\n',
        ),
    ]
    for path, insert in patches:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if "id_corpus:" in text:
            continue
        if dry_run:
            print(f"  [dry-run] patch {path.name}")
            continue
        text = text.replace("---\n", f"---\n{insert}", 1)
        path.write_text(text, encoding="utf-8")
        print(f"  patch {path.name}")


def update_sync(dry_run: bool) -> None:
    if not SYNC.is_file():
        return
    data = json.loads(SYNC.read_text(encoding="utf-8"))
    tracks = data.setdefault("tracks", {})
    main = tracks.setdefault("main", {})
    main["last_id"] = LAST_MAIN_ID
    main["next_available"] = NEXT_MAIN_ID
    batches = main.setdefault("confirmed_batches", [])
    batches.append(
        {
            "range": [1527, LAST_MAIN_ID],
            "status": "confirmed",
            "notes": (
                f"Merge todo pending {date.today().isoformat()}: "
                "Biomm 1527-1546 (ex 1481-1500); Zema 1547-1550 (ex 185-188); "
                f"Homeschooling {HOMESCHOOL_ID} (ex 1425)."
            ),
        }
    )

    thematic = tracks.setdefault("thematic", {})
    entries = thematic.setdefault("entries", [])
    for tid, topic, artifact, note in [
        (189, "Reforma Tributaria — captura regulatoria split payment (T-189)", "reforma-tributaria-captura-regulatoria", "Confirmado estudo Jekyll 2026-05-26"),
        (190, "Direita Permitida — gatekeeping oposicionista (T-190)", "direita-permitida-dossie", "Renumerado de 189; T-189 reservado Reforma"),
    ]:
        found = False
        for e in entries:
            if e.get("id") == tid:
                e.update({"status": "confirmed", "topic": topic, "artifact": artifact, "notes": note})
                found = True
                break
        if not found:
            entries.append({"id": tid, "status": "confirmed", "topic": topic, "artifact": artifact, "notes": note})

    thematic["last_id"] = 190
    thematic["next_available"] = 191
    pending = thematic.get("pending") or []
    thematic["pending"] = [p for p in pending if p not in (189, 190)]

    sync = data.setdefault("sync_status", {})
    sync["main_track_last_sync"] = date.today().isoformat()
    sync["thematic_track_last_sync"] = date.today().isoformat()
    sync["ids_confirmed_total"] = {
        "main_track": f"{LAST_MAIN_ID} (lawfare.json + unified-corpus + Jekyll)",
        "thematic_track": 190,
    }
    open_items = sync.setdefault("open_items", [])
    resolved = [
        "MERGE PCC batch 1449-1510 ainda pendente",
        "MERGE PCC batch: IDs 1449–1511 existem apenas em _data/ batch files. Merge em lawfare.json requer preenchimento sequencial 1449–1480 antes de incluir série 1481–1511 — ou aceitar namespace separado definitivamente.",
    ]
    for note in resolved:
        while note in open_items:
            open_items.remove(note)
    new_notes = [
        "Biomm batch publicado como 1527-1546 (1481-1500 = PCC confirmado)",
        "Zema/mineracao publicado como 1547-1550 (185-188 thematic = Dosimetria)",
        f"Homeschooling Jales publicado como {HOMESCHOOL_ID}",
    ]
    for n in new_notes:
        if n not in open_items:
            open_items.append(n)

    data["id_conflict_resolutions"] = {
        "generated": date.today().isoformat(),
        "biomm": {"old_range": "1481-1500", "new_range": "1527-1546", "reason": "1481-1500 PCC/Ndrangheta publicados"},
        "zema": {"old_ids": "185-188", "new_ids": "1547-1550", "reason": "thematic 185-188 Dosimetria"},
        "homeschooling": {"old_id": 1425, "new_id": HOMESCHOOL_ID, "reason": "1425 Mare Liberum Galeao"},
        "direita_permitida": {"old_id": "T-189", "new_id": "T-190", "reason": "T-189 Reforma Tributaria"},
        "pcc_namespace": {"range": "1481-1500", "status": "canonical_pcc_ndrangheta", "do_not_overwrite": True},
    }

    if not dry_run:
        SYNC.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  sync: main last={LAST_MAIN_ID}, thematic last=190")


def archive_todo(dry_run: bool) -> None:
    moved = [
        "lawfare-1481-1500-merged.json",
        "lawfare-1481-1494.json",
        "ids-185-188-zema-mineracao.json",
        "entry_1425_homeschooling_jales.json",
        "lawfare-189-direita-permitida.json",
        "thematic-189-reforma-tributaria-captura.json",
    ]
    for name in moved:
        src = TODO / name
        if not src.is_file():
            continue
        dst = PROC / name
        if dry_run:
            print(f"  [dry-run] archive {name}")
        else:
            shutil.move(str(src), str(dst))
            print(f"  archive -> processados/{name}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    entries = load_entries()
    if not entries:
        print("Nenhuma entrada pendente.", file=sys.stderr)
        return 1

    print(f"Entradas: {len(entries)} (IDs {entries[0]['id_corpus']}–{entries[-1]['id_corpus']})")
    renumber_json_files(args.dry_run)
    n = write_posts(entries, args.dry_run)
    print(f"Posts: {n}")
    patch_estudos_frontmatter(args.dry_run)
    update_sync(args.dry_run)
    archive_todo(args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
