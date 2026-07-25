#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processa _data/todo/*.json e gera artigos Jekyll conforme padrão Chirpy do projeto.

Suporta schemas:
  - instancia_padrao (TEMPLATE-registro-rapido)
  - entries[] (biazucci)
  - assuntos[] (crise diplomatica)
  - lawfare batch (titulo, descricao, id)
  - objeto único (homeschooling)

Uso:
  python scripts/merge_todo_json.py
  python scripts/merge_todo_json.py --dry-run
  python scripts/merge_todo_json.py --force
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

IMAGE_BY_CATEGORY = {
    "operacoes": "/assets/solid/bullseye.svg",
    "escandalos": "/assets/solid/skull.svg",
    "stf": "/assets/solid/gavel.svg",
    "justica": "/assets/solid/hammer.svg",
    "governo": "/assets/solid/sitemap.svg",
    "impunidade": "/assets/solid/handcuffs.svg",
    "lawfare": "/assets/solid/weight-scale.svg",
    "crise-diplomatica": "/assets/solid/globe.svg",
    "bancos": "/assets/solid/landmark.svg",
}


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")[:90]


def yaml_escape(s: str) -> str:
    return s.replace('"', '\\"')


def format_iso(d: str) -> str:
    return f"{(d or '2026-01-01')[:10]}T12:00:00.000Z"


def post_has_id(id_corpus: str) -> bool:
    for p in POSTS.rglob("*.md"):
        try:
            t = p.read_text(encoding="utf-8")
        except OSError:
            continue
        if re.search(rf'^id_corpus:\s*["\']?{re.escape(id_corpus)}["\']?\s*$', t, re.M):
            return True
    return False


def extract_raw_records(data, source: Path) -> list[dict]:
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict) and ("id" in x or "id_display" in x)]
    if isinstance(data, dict):
        if "entries" in data:
            return list(data["entries"])
        if "assuntos" in data:
            return list(data["assuntos"])
        if "id" in data or "id_display" in data:
            return [data]
    return []


def resolve_category(entry: dict) -> str:
    if entry.get("jekyll_categories"):
        c = entry["jekyll_categories"]
        return c[0] if isinstance(c, list) else str(c)

    titulo = (entry.get("titulo") or entry.get("title") or "").lower()
    cat = (entry.get("categoria") or entry.get("category") or "").lower()
    op = (entry.get("operacao_referencia") or "").lower()
    tags = [str(t).lower() for t in entry.get("tags") or []]
    actors = " ".join(
        (a.get("nome") or a.get("name") or str(a))
        for a in (entry.get("atores") or entry.get("actors") or [])
        if isinstance(a, dict)
    ).lower()

    mapping = {
        "captura-institucional": "escandalos",
        "conflito-de-interesses": "escandalos",
        "crise-diplomatica": "crise-diplomatica",
        "judicial": "justica",
        "documentado": "escandalos",
        "operacao": "operacoes",
        "operacoes": "operacoes",
    }
    if cat in mapping:
        return mapping[cat]

    if entry.get("tipo") == "instancia_padrao":
        if "stf" in titulo or "toffoli" in titulo or ("moraes" in actors and "stf" in actors):
            return "stf"
        if "trf" in titulo or "justiça federal" in titulo or titulo.startswith("jf "):
            return "justica"
        if any(k in titulo for k in ("governador", "ministro de minas", "zema", "copasa", "semad")):
            return "governo"
        if "compliance zero" in op or "biomm" in titulo or "cedro" in titulo and "vende" in titulo:
            return "escandalos"
        if "operacao" in op or "operação" in op:
            return "operacoes"
        return "operacoes"

    if "crise-diplomatica" in cat or "crise-diplomatica" in tags:
        return "crise-diplomatica"
    if any(k in cat for k in ("stf", "moraes", "supremo")):
        return "stf"
    if "operacao" in cat or "operacao" in tags:
        return "operacoes"
    if cat == "judicial":
        return "justica"
    return "escandalos"


def build_tags(entry: dict, category: str) -> list[str]:
    tags: list[str] = []
    for src in (entry.get("padroes_ativados"), entry.get("patterns"), entry.get("tags")):
        if src:
            tags.extend(str(x) for x in src)
    if entry.get("slug"):
        tags.append(entry["slug"])
    if entry.get("operacao_referencia"):
        tags.append(slugify(entry["operacao_referencia"])[:40])
    if category not in tags:
        tags.insert(0, category)
    return list(dict.fromkeys(tags))[:12]


def normalize_entry(raw: dict, source: Path) -> dict | None:
    eid = raw.get("id_display") or raw.get("id")
    if eid is None:
        return None

    # instancia_padrao
    if raw.get("tipo") == "instancia_padrao" or raw.get("evidencia_primaria"):
        title = raw.get("titulo", "")
        jdate = raw.get("data_evento") or raw.get("jekyll_date") or raw.get("date", "")
        ev = raw.get("evidencia_primaria") or {}
        resumo = ev.get("descricao") or raw.get("observacao_analitica") or ""
        cat = resolve_category(raw)
        slug = raw.get("slug") or slugify(title)
        fname = raw.get("jekyll_filename") or f"{str(jdate)[:10]}-{slug}.md"
        if not fname.endswith(".md"):
            fname += ".md"
        actors = []
        for a in raw.get("atores") or []:
            if isinstance(a, dict):
                n = a.get("nome") or a.get("name", "")
                fn = a.get("funcao_estrutural") or a.get("role", "")
                actors.append(f"{n} ({fn})" if fn else n)
            else:
                actors.append(str(a))
        fontes = []
        if ev.get("url_referencia"):
            fontes.append({"titulo": ev.get("fonte", "Fonte"), "url": ev["url_referencia"]})
        elif ev.get("fonte"):
            fontes.append({"titulo": ev["fonte"], "url": ""})
        conexoes = [
            f"ID {c.get('id_ref')}: {c.get('descricao', '')}"
            for c in (raw.get("conexoes_corpus") or [])
        ]
        return {
            "id_corpus": str(eid),
            "jekyll_filename": fname,
            "jekyll_date": str(jdate)[:10],
            "jekyll_categories": [cat],
            "jekyll_tags": build_tags(raw, cat),
            "jekyll_permalink": raw.get("jekyll_permalink") or f"/posts/{Path(fname).stem}/",
            "titulo": title,
            "resumo": resumo,
            "categoria": raw.get("tipo") or cat,
            "pais": "Brasil",
            "atores": actors,
            "instituicoes": [],
            "fontes_verificadas": fontes,
            "_analise": raw.get("observacao_analitica", ""),
            "_cadeia": raw.get("cadeia_logica", ""),
            "_operacao": raw.get("operacao_referencia", ""),
            "_conexoes": conexoes,
            "_lacunas": [],
            "conflito_nota": raw.get("conflito_nota"),
            "_source": source.name,
        }

    # biazucci-style entries
    if raw.get("summary") and raw.get("title") and raw.get("actors"):
        title = raw.get("title", "")
        jdate = raw.get("jekyll_date") or raw.get("date", "")
        cat = resolve_category(raw)
        fname = raw.get("jekyll_filename") or f"{str(jdate)[:10]}-{slugify(title)}.md"
        people, inst = [], []
        for a in raw.get("actors") or []:
            if isinstance(a, dict):
                n = a.get("name") or a.get("nome", "")
                r = a.get("role") or a.get("papel", "")
                i = a.get("institution") or a.get("instituicao", "")
                if n:
                    people.append(f"{n} ({r})" if r else n)
                if i:
                    inst.append(i)
        inst.extend(raw.get("institutions") or [])
        fontes = []
        for s in raw.get("sources") or []:
            if isinstance(s, dict):
                fontes.append({"titulo": s.get("title", "Fonte"), "url": s.get("url", "")})
            else:
                fontes.append({"titulo": "Fonte", "url": str(s)})
        return {
            "id_corpus": str(eid),
            "jekyll_filename": fname,
            "jekyll_date": str(jdate)[:10],
            "jekyll_categories": raw.get("jekyll_categories") or [cat],
            "jekyll_tags": build_tags(raw, cat),
            "jekyll_permalink": raw.get("jekyll_permalink") or f"/posts/{Path(fname).stem}/",
            "titulo": title,
            "resumo": raw.get("summary", ""),
            "categoria": raw.get("category") or cat,
            "pais": "Brasil",
            "atores": people,
            "instituicoes": list(dict.fromkeys(inst)),
            "fontes_verificadas": fontes,
            "_analise": raw.get("analise", ""),
            "_result": raw.get("result", ""),
            "_legal": raw.get("legal_basis") or [],
            "_lacunas": raw.get("lacuna_investigativa") or [],
            "conflito_nota": raw.get("conflito_nota"),
            "_source": source.name,
        }

    # lawfare assuntos / zema / biomm batch
    title = raw.get("titulo") or raw.get("title", "")
    if not title:
        return None
    jdate = (
        raw.get("jekyll_date")
        or raw.get("data_evento")
        or raw.get("date")
        or raw.get("data_registro")
        or ""
    )
    cat = resolve_category(raw)
    fname = raw.get("jekyll_filename") or f"{str(jdate)[:10]}-{slugify(title)}.md"
    if not fname.endswith(".md"):
        fname += ".md"
    resumo = raw.get("descricao") or raw.get("summary") or raw.get("resumo", "")
    people = raw.get("pessoas_envolvidas") or []
    if not people:
        for a in raw.get("actors") or raw.get("atores") or []:
            people.append(a if isinstance(a, str) else a.get("name") or a.get("nome", ""))
    inst = raw.get("instituicoes_envolvidas") or raw.get("institutions") or []
    fontes_raw = raw.get("fontes") or raw.get("sources") or []
    fontes = []
    for f in fontes_raw:
        if isinstance(f, dict):
            fontes.append({"titulo": f.get("title") or f.get("titulo", "Fonte"), "url": f.get("url", "")})
        elif f:
            fontes.append({"titulo": "Fonte", "url": str(f)})
    return {
        "id_corpus": str(eid),
        "jekyll_filename": fname,
        "jekyll_date": str(jdate)[:10],
        "jekyll_categories": raw.get("jekyll_categories") or [cat],
        "jekyll_tags": build_tags(raw, cat),
        "jekyll_permalink": raw.get("jekyll_permalink") or f"/posts/{Path(fname).stem}/",
        "titulo": title,
        "resumo": resumo,
        "categoria": raw.get("categoria") or raw.get("category") or cat,
        "pais": raw.get("pais", "Brasil"),
        "atores": people,
        "instituicoes": inst,
        "fontes_verificadas": fontes,
        "_analise": raw.get("analytical_note") or raw.get("observacao_analitica", ""),
        "_legal": raw.get("legal_refs") or raw.get("legal_basis") or [],
        "_lacunas": [],
        "conflito_nota": raw.get("conflito_nota"),
        "_source": source.name,
    }


def render_post(u: dict) -> str:
    category = u["jekyll_categories"][0]
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
    ]
    if u.get("_operacao"):
        parts.append(f"| Operação | {u['_operacao']} |")
    parts.extend(["", ""])

    if u.get("conflito_nota"):
        parts.extend([f"> **Nota de conflito ID:** {u['conflito_nota']}", ""])

    if u.get("_cadeia"):
        parts.extend(["## Cadeia lógica", "", u["_cadeia"], ""])

    if u.get("atores"):
        parts.extend(["### Atores", ""] + [f"- {a}" for a in u["atores"]] + [""])
    if u.get("instituicoes"):
        parts.extend(["### Instituições", ""] + [f"- {i}" for i in u["instituicoes"]] + [""])

    if u.get("_result"):
        parts.extend(["## Resultado documentado", "", u["_result"], ""])
    if u.get("_analise") and u["_analise"] != resumo:
        parts.extend(["## Análise", "", u["_analise"], ""])
    if u.get("_legal"):
        parts.extend(["## Base legal / referências normativas", ""] + [f"- {lb}" for lb in u["_legal"]] + [""])
    if u.get("_conexoes"):
        parts.extend(["## Conexões no corpus", ""] + [f"- {c}" for c in u["_conexoes"]] + [""])
    lacunas = u.get("_lacunas") or []
    if lacunas:
        parts.extend(["## Lacunas investigativas", ""] + [f"- {x}" for x in lacunas] + [""])

    fontes = u.get("fontes_verificadas") or []
    if fontes:
        parts.extend(["## 📚 Fontes verificáveis", ""])
        for i, f in enumerate(fontes, 1):
            url = f.get("url", "")
            tit = f.get("titulo", "Fonte")
            if url:
                parts.append(f"{i}. [{tit}]({url})")
            elif tit:
                parts.append(f"{i}. {tit}")
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
source_data: "{u.get('_source', '')}"
---

"""
    return fm + "\n".join(parts)


def write_posts(entries: list[dict], force: bool, dry_run: bool) -> tuple[int, int]:
    written = skipped = 0
    for u in entries:
        kid = u["id_corpus"]
        cat = u["jekyll_categories"][0]
        target = POSTS / cat / u["jekyll_filename"]
        if target.is_file() and not force:
            if post_has_id(kid):
                print(f"  skip (exists): {target.relative_to(ROOT)}")
                skipped += 1
                continue
        if dry_run:
            print(f"  [dry-run] {target.relative_to(ROOT)}")
            written += 1
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_post(u), encoding="utf-8")
        print(f"  OK {target.relative_to(ROOT)}")
        written += 1
    return written, skipped


def update_sync(entries: list[dict], dry_run: bool) -> None:
    if not SYNC.is_file() or not entries:
        return
    ids = [int(u["id_corpus"]) for u in entries if str(u["id_corpus"]).isdigit()]
    if not ids:
        return
    data = json.loads(SYNC.read_text(encoding="utf-8"))
    main = data.setdefault("tracks", {}).setdefault("main", {})
    last = max(ids)
    if last >= main.get("last_id", 0):
        main["last_id"] = last
        main["next_available"] = last + 1
    batches = main.setdefault("confirmed_batches", [])
    note = f"Merge todo {date.today().isoformat()}: IDs {min(ids)}–{last} via merge_todo_json.py"
    batches.append({"range": [min(ids), last], "status": "confirmed", "notes": note})
    sync = data.setdefault("sync_status", {})
    sync["main_track_last_sync"] = date.today().isoformat()
    sync["ids_confirmed_total"] = {
        "main_track": f"{main['last_id']} (Jekyll + lawfare.json)",
        "thematic_track": data.get("tracks", {}).get("thematic", {}).get("last_id", 190),
    }
    if not dry_run:
        SYNC.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  sync: last_id={main['last_id']}, next={main['next_available']}")


def archive_processed(source: Path, all_skipped: bool, dry_run: bool) -> None:
    if all_skipped:
        return
    dst = PROC / source.name
    if dst.is_file():
        return
    if dry_run:
        print(f"  [dry-run] archive {source.name}")
        return
    PROC.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(dst))
    print(f"  archive -> processados/{source.name}")


def process_file(path: Path, force: bool, dry_run: bool) -> tuple[int, int]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"  ERRO {path.name}: {exc}", file=sys.stderr)
        return 0, 0

    entries: list[dict] = []
    for raw in extract_raw_records(data, path):
        u = normalize_entry(raw, path)
        if u:
            entries.append(u)

    if not entries:
        print(f"  {path.name}: nenhum registro reconhecido")
        return 0, 0

    print(f"\n{path.name}: {len(entries)} registros (IDs {entries[0]['id_corpus']}–{entries[-1]['id_corpus']})")
    written, skipped = write_posts(entries, force, dry_run)
    if written and not dry_run:
        update_sync(entries, dry_run=False)
    archive_processed(path, written == 0 and skipped == len(entries), dry_run)
    return written, skipped


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="Sobrescreve posts existentes")
    args = ap.parse_args()

    files = sorted(TODO.glob("*.json"))
    if not files:
        print("Nenhum JSON em _data/todo/", file=sys.stderr)
        return 1

    total_w = total_s = 0
    for f in files:
        w, s = process_file(f, args.force, args.dry_run)
        total_w += w
        total_s += s

    print(f"\nTotal: {total_w} escritos, {total_s} ignorados (já existiam)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
