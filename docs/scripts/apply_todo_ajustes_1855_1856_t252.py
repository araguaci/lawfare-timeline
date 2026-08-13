#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aplica ajustes da fila todo: patch 1855, novo 1856, rewrite T-252."""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from merge_todo_queue_1850_1855 import (  # noqa: E402
    BATCH_MAIN,
    BATCH_THEMATIC,
    LAWFARE,
    POSTS,
    PROC,
    TODO,
    actors_people,
    build_corpus_index,
    connections_md,
    linkify_inline,
    render_post,
    render_thematic,
    rewrite_connections_in_posts,
    slugify,
    to_assunto,
    yaml_escape,
)

# Override category rules for this pass
def resolve_category(entry: dict) -> str:
    eid = int(entry.get("id") or 0)
    title = (entry.get("title") or "").lower()
    cat = (entry.get("category") or "").lower()
    if eid == 1856 or ("moraes" in title and "fonte" in title):
        return "stf"
    if eid == 1855 or "rede interrompida" in title or "seletividade plataforma" in title:
        return "justica"
    if eid == 1854 or ("janja" in title and "negado" not in title):
        return "escandalos"
    if eid in (1850, 1851, 1852, 1853):
        return "lawfare"
    if "chokepoint_judicial" in cat:
        return "justica"
    return "escandalos"


def find_post_by_id(cid: str) -> Path | None:
    for p in POSTS.rglob("*.md"):
        t = p.read_text(encoding="utf-8", errors="replace")
        if re.search(rf'id_corpus:\s*"{re.escape(cid)}"\s*$', t, re.M):
            return p
    return None


def main() -> int:
    main_path = TODO / "lawfare-batch-lei15487-anpd-discord-1850-1855.json"
    thematic_path = TODO / "lawfare-thematic-T252-escalada-anonimizacao-criptografia.json"
    if not main_path.is_file() or not thematic_path.is_file():
        print("ERRO: faltam batches na fila todo/")
        return 1

    entries = json.loads(main_path.read_text(encoding="utf-8"))
    by_todo = {int(e["id"]): e for e in entries}
    lawfare = json.loads(LAWFARE.read_text(encoding="utf-8"))
    assuntos = lawfare.get("assuntos") or []
    by_assunto = {a["id"]: a for a in assuntos if isinstance(a.get("id"), int)}

    touched: list[Path] = []

    # --- 1855 patch ---
    e1855 = by_todo[1855]
    # enrich connections
    conns = list(e1855.get("connections") or [])
    for extra in ("id_1850", "id_1854"):
        if extra not in conns and extra.replace("id_", "") not in [
            str(c).replace("id_", "") for c in conns
        ]:
            pass  # keep as in batch
    cat1855 = resolve_category(e1855)
    assunto1855 = to_assunto(e1855, cat1855, main_path.name)
    if 1855 in by_assunto:
        # preserve id position; replace fields
        old = by_assunto[1855]
        old.clear()
        old.update(assunto1855)
        print("PATCH lawfare 1855")
    else:
        assuntos.append(assunto1855)
        print("ADD lawfare 1855")

    old_post = find_post_by_id("1855")
    idx = build_corpus_index()
    # provisional permalink for new slug
    date = str(e1855["date"])[:10]
    fname = f"{date}-{slugify(e1855['title'])}.md"
    permalink = f"/posts/{Path(fname).stem}/"
    idx["1855"] = {"title": e1855["title"], "permalink": permalink, "path": ""}
    idx["id_1855"] = idx["1855"]

    body, out_path, _ = render_post(e1855, cat1855, main_path.name, idx)
    # force category via local resolve (render_post uses its own resolve - monkeypatch by rewriting)
    # render_post already used imported resolve_category from module — override body categories
    body = body.replace("categories: escandalos", f"categories: {cat1855}")
    body = body.replace("categories: justica", f"categories: {cat1855}")
    # Re-render with patched resolve: call render after injecting
    # Simpler: write with our resolve by temporarily patching module
    import merge_todo_queue_1850_1855 as m

    m.resolve_category = resolve_category
    body, out_path, _ = m.render_post(e1855, cat1855, main_path.name, idx)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(body, encoding="utf-8")
    touched.append(out_path)
    print(f"WRITE post 1855 -> {out_path.relative_to(ROOT)}")
    if old_post and old_post.resolve() != out_path.resolve():
        old_post.unlink()
        print(f"REMOVE old 1855 post {old_post.relative_to(ROOT)}")

    # --- 1856 new ---
    e1856 = by_todo[1856]
    conns6 = list(e1856.get("connections") or [])
    if "id_1849" not in conns6 and "1849" not in conns6:
        conns6.append("id_1849")
        e1856["connections"] = conns6
    cat1856 = resolve_category(e1856)
    if 1856 in by_assunto:
        print("SKIP 1856 already in corpus")
    else:
        assuntos.append(to_assunto(e1856, cat1856, main_path.name))
        print("ADD lawfare 1856")

    date6 = str(e1856["date"])[:10]
    fname6 = f"{date6}-{slugify(e1856['title'])}.md"
    per6 = f"/posts/{Path(fname6).stem}/"
    idx["1856"] = {"title": e1856["title"], "permalink": per6, "path": ""}
    idx["id_1856"] = idx["1856"]
    # refresh 1849 in idx
    idx = build_corpus_index()
    idx["1855"] = {
        "title": e1855["title"],
        "permalink": f"/posts/{out_path.stem}/",
        "path": str(out_path),
    }
    idx["id_1855"] = idx["1855"]
    idx["1856"] = {"title": e1856["title"], "permalink": per6, "path": ""}
    idx["id_1856"] = idx["1856"]

    body6, out6, _ = m.render_post(e1856, cat1856, main_path.name, idx)
    if not out6.exists():
        out6.write_text(body6, encoding="utf-8")
        touched.append(out6)
        print(f"WRITE post 1856 -> {out6.relative_to(ROOT)}")
    else:
        out6.write_text(body6, encoding="utf-8")
        touched.append(out6)
        print(f"OVERWRITE post 1856 -> {out6.relative_to(ROOT)}")

    # Cross-link 1849 -> 1856 in connections if missing
    p1849 = find_post_by_id("1849")
    if p1849:
        t = p1849.read_text(encoding="utf-8")
        if "id_1856" not in t and "1856" not in t.split("## Conex")[-1][:800]:
            link = (
                f"- [id_1856 — {e1856['title'][:80]}…]({per6})\n"
                if len(e1856["title"]) > 80
                else f"- [id_1856 — {e1856['title']}]({per6})\n"
            )
            if "## Conexoes" in t or "## Conexões" in t:
                t2 = re.sub(
                    r"(## Conexoe[s]?[^\n]*\n)",
                    r"\1\n" + link,
                    t,
                    count=1,
                    flags=re.I,
                )
                if t2 != t:
                    p1849.write_text(t2, encoding="utf-8")
                    print("LINK 1849 -> 1856")
            else:
                p1849.write_text(
                    t.rstrip() + "\n\n## Conexoes\n\n" + link, encoding="utf-8"
                )
                print("ADD Conexoes 1849 -> 1856")

    # --- T-252 rewrite ---
    t = json.loads(thematic_path.read_text(encoding="utf-8"))
    idx = build_corpus_index()
    # ensure 1855/1856 in idx
    idx["1855"] = {
        "title": e1855["title"],
        "permalink": f"/posts/{out_path.stem}/",
        "path": str(out_path),
    }
    idx["id_1855"] = idx["1855"]
    idx["1856"] = {
        "title": e1856["title"],
        "permalink": per6,
        "path": str(out6),
    }
    idx["id_1856"] = idx["1856"]

    body_t, out_t = m.render_thematic(t, idx, thematic_path.name)
    # Prefer keep existing T-252 path if present
    old_t = find_post_by_id("T-252")
    if old_t:
        # If slug/title changed, write new and remove old
        if old_t.resolve() != out_t.resolve():
            out_t.write_text(body_t, encoding="utf-8")
            touched.append(out_t)
            old_t.unlink()
            print(f"REWRITE T-252 new slug; removed {old_t.name}")
        else:
            out_t.write_text(body_t, encoding="utf-8")
            touched.append(out_t)
            print("REWRITE T-252 in place")
    else:
        out_t.write_text(body_t, encoding="utf-8")
        touched.append(out_t)
        print(f"WRITE T-252 -> {out_t.name}")

    # Also update xarticle note? skip

    idx = build_corpus_index()
    rewrite_connections_in_posts(touched, idx)

    # Fix H1 if linkify corrupted (headings skipped in newer linkify)
    for p in touched:
        text = p.read_text(encoding="utf-8")
        end = text.find("\n---", 3)
        fm = text[: end + 4]
        body = text[end + 4 :]
        title_m = re.search(r'title:\s*"((?:\\.|[^"\\])*)"', fm)
        if title_m:
            title = title_m.group(1).replace('\\"', '"')
            body2 = re.sub(
                r"^#\s*\[[^\]]+\]\([^)]+\).*$",
                f"# {title}",
                body,
                count=1,
                flags=re.M,
            )
            if body2 != body:
                p.write_text(fm + body2, encoding="utf-8")

    assuntos.sort(key=lambda a: (a.get("data_evento") or "", a.get("id") or 0))
    lawfare["assuntos"] = assuntos
    if "data_extração" in lawfare:
        lawfare["data_extração"] = "2026-08-13"
    LAWFARE.write_text(json.dumps(lawfare, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"lawfare.json max={max(a['id'] for a in assuntos if isinstance(a.get('id'), int))}")

    # Archive: overwrite processados with adjusted versions
    PROC.mkdir(parents=True, exist_ok=True)
    for src in (main_path, thematic_path):
        dst = PROC / src.name
        shutil.copy2(src, dst)
        src.unlink()
        print(f"Arquivado (ajuste): {src.name} -> processados/")

    print("OK ajustes aplicados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
