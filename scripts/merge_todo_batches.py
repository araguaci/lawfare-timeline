#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Merge _data/todo/*.json batches into lawfare.json and lawfare-unified-corpus.json,
then emit Chirpy posts under _posts/<categoria>/.

Regras de ID (alinhado a gosurf.site):
  - Biazucci: 1511-1513 (batch lawfare-1511-1513-biazucci.json)
  - Crise diplomática: 1514-1524 (batch lawfare-1512-1524; pula 1512-1513 do batch crise)
  - Eventos Ramagem ICE/delegado (crise 1512-1513 originais) -> 1525-1526
  - ID 1521: data_evento corrigida para data_iso (2025-07-08)

Uso:
  python scripts/merge_todo_batches.py
  python scripts/merge_todo_batches.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODO = ROOT / "_data" / "todo"
LAWFARE = ROOT / "_data" / "lawfare.json"
UNIFIED = ROOT / "_data" / "lawfare-unified-corpus.json"
SYNC = ROOT / "_data" / "claude.ai-corpus-ids-sync.json"
POSTS = ROOT / "_posts"
GOSURF = Path(r"D:\ai-projects\gosurf.site")

IMAGE_BY_CATEGORY = {
    "lawfare": "/assets/solid/weight-scale.svg",
    "stf": "/assets/solid/gavel.svg",
    "escandalos": "/assets/solid/skull.svg",
    "justica": "/assets/solid/hammer.svg",
    "impunidade": "/assets/solid/handcuffs.svg",
    "crise-diplomatica": "/assets/solid/globe.svg",
    "operacoes": "/assets/solid/bullseye.svg",
    "bancos": "/assets/solid/landmark.svg",
}

GOSURF_DOSSIERS = {
    range(1511, 1514): "biazucci-erro-judiciario-cidh",
    range(1514, 1525): "crise-diplomatica-brasil-eua-2025-2026",
    range(1525, 1527): "crise-diplomatica-brasil-eua-2025-2026",
}


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")[:90]


def yaml_escape(s: str) -> str:
    return s.replace('"', '\\"')


def pick_image(category: str) -> str:
    return IMAGE_BY_CATEGORY.get(category, "/assets/solid/circle-exclamation.svg")


def dossier_for_id(eid: int) -> str | None:
    for rng, slug in GOSURF_DOSSIERS.items():
        if eid in rng:
            return slug
    return None


def format_iso(d: str) -> str:
    return f"{(d or '2026-01-01')[:10]}T12:00:00.000Z"


def actors_list(raw: list) -> tuple[list[str], list[str]]:
    people, inst = [], []
    for a in raw or []:
        if isinstance(a, dict):
            name = a.get("name") or a.get("nome", "")
            role = a.get("role") or a.get("papel", "")
            inst_name = a.get("institution") or a.get("instituicao", "")
            if name:
                people.append(f"{name} ({role})" if role else name)
            if inst_name and inst_name not in inst:
                inst.append(inst_name)
        elif isinstance(a, str):
            people.append(a)
    return people, inst


def sources_unified(raw: list) -> list[dict]:
    out = []
    for s in raw or []:
        if isinstance(s, dict):
            out.append(
                {
                    "url": s.get("url", ""),
                    "titulo": s.get("title") or s.get("titulo", "Fonte"),
                    "veiculo": s.get("outlet") or s.get("veiculo", ""),
                    "data": s.get("date") or s.get("data", ""),
                }
            )
        elif isinstance(s, str):
            out.append({"url": s, "titulo": "Fonte", "veiculo": "", "data": ""})
    return out


def biazucci_to_unified(entry: dict) -> dict:
    cats = entry.get("jekyll_categories") or ["justica"]
    category = cats[0]
    eid = entry["id"]
    title = entry.get("title") or entry.get("titulo", "")
    summary = entry.get("summary") or entry.get("descricao", "")
    jdate = entry.get("jekyll_date") or entry.get("date", "")
    fname = entry.get("jekyll_filename") or f"{jdate}-{slugify(title)}.md"
    people, inst = actors_list(entry.get("actors") or [])
    inst.extend(entry.get("institutions") or [])
    inst = list(dict.fromkeys(inst))
    slug = dossier_for_id(eid)
    gosurf = [{"slug": slug, "url": f"https://gosurf.site/{slug}"}] if slug else []
    conns = []
    for c in entry.get("connections") or []:
        m = re.search(r"\d+", str(c))
        if m:
            conns.append(f"id_{m.group()}")
    return {
        "id_corpus": str(eid),
        "id_original": eid,
        "conflito_nota": None,
        "jekyll_filename": fname,
        "jekyll_layout": "post",
        "jekyll_date": jdate,
        "jekyll_categories": cats,
        "jekyll_tags": entry.get("tags") or list(dict.fromkeys(cats + (entry.get("patterns") or [])))[:12],
        "jekyll_permalink": entry.get("jekyll_permalink") or f"/posts/{Path(fname).stem}/",
        "titulo": title,
        "data": jdate,
        "categoria": entry.get("category") or category,
        "resumo": summary,
        "fontes_verificadas": sources_unified(entry.get("sources") or []),
        "padroes": entry.get("patterns") or [],
        "atores": people,
        "instituicoes": inst,
        "artigos_gosurf": gosurf,
        "conexoes": conns,
        "dimensao_global": eid >= 1514,
        "pais": "Brasil",
        "verificado": True,
        "status_publicacao": "coberto_por_artigo",
        "_analise": entry.get("analise", ""),
        "_result": entry.get("result", ""),
        "_legal": entry.get("legal_basis") or [],
        "_lacunas": entry.get("lacuna_investigativa") or [],
    }


def crise_to_unified(a: dict, *, reassign_id: int | None = None) -> dict:
    eid = reassign_id if reassign_id is not None else a["id"]
    cat = a.get("categoria", "crise-diplomatica")
    jdate = a["data_evento"]
    if eid == 1521 and a.get("data_iso"):
        jdate = a["data_iso"][:10]
    title = a["titulo"]
    fname = f"{jdate}-{slugify(title)}.md"
    slug = dossier_for_id(eid)
    note = None
    if reassign_id:
        note = f"Renumerado de {a['id']} (conflito Biazucci 1511-1513)."
    return {
        "id_corpus": str(eid),
        "id_original": eid,
        "conflito_nota": note,
        "jekyll_filename": fname,
        "jekyll_layout": "post",
        "jekyll_date": jdate,
        "jekyll_categories": [cat],
        "jekyll_tags": (a.get("tags") or [])[:12],
        "jekyll_permalink": f"/posts/{Path(fname).stem}/",
        "titulo": title,
        "data": jdate,
        "categoria": cat,
        "resumo": a.get("descricao", ""),
        "fontes_verificadas": sources_unified(a.get("fontes") or []),
        "padroes": [],
        "atores": a.get("pessoas_envolvidas") or [],
        "instituicoes": a.get("instituicoes_envolvidas") or [],
        "artigos_gosurf": [{"slug": slug, "url": f"https://gosurf.site/{slug}"}] if slug else [],
        "conexoes": [],
        "dimensao_global": a.get("pais", "") in ("Global", "EUA"),
        "pais": a.get("pais", "Brasil"),
        "verificado": True,
        "status_publicacao": "coberto_por_artigo",
        "_impacto": a.get("impacto_diplomatico", "N/A"),
        "_tipo": a.get("tipo_escandalo", "N/A"),
    }


def to_lawfare_assunto(u: dict, category: str) -> dict:
    rel = POSTS / category / u["jekyll_filename"]
    fonte = str(rel.relative_to(ROOT)).replace("/", "\\")
    tags = u.get("jekyll_tags") or [category]
    return {
        "titulo": u["titulo"],
        "data_evento": u["jekyll_date"],
        "data_iso": format_iso(u["jekyll_date"]),
        "categoria": category,
        "tags": tags if isinstance(tags, list) else [tags],
        "descricao": u["resumo"],
        "relevancia": "alta",
        "impacto_diplomatico": u.get("_impacto", "N/A"),
        "tipo_escandalo": u.get("_tipo", "N/A"),
        "fontes": [f.get("url") for f in u.get("fontes_verificadas") or [] if f.get("url")],
        "pessoas_envolvidas": u.get("atores") or [],
        "instituicoes_envolvidas": u.get("instituicoes") or [],
        "pais": u.get("pais", "Brasil"),
        "valor_envolvido": "N/A",
        "prioridade": 1,
        "fonte_arquivo": fonte,
        "id": int(u["id_corpus"]),
    }


def render_chirpy_post(u: dict) -> str:
    cats = u.get("jekyll_categories") or ["lawfare"]
    category = cats[0] if isinstance(cats, list) else str(cats)
    tags = u.get("jekyll_tags") or []
    title = u["titulo"]
    resumo = u["resumo"]
    desc = yaml_escape((resumo[:157] + "…") if len(resumo) > 157 else resumo)
    image = pick_image(category)
    date_iso = format_iso(u.get("jekyll_date") or u.get("data", ""))
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

    if u.get("_result"):
        parts.extend(["## Resultado documentado", "", u["_result"], ""])
    if u.get("_analise"):
        parts.extend(["## Análise", "", u["_analise"], ""])
    if u.get("_legal"):
        parts.extend(["## Base legal", ""] + [f"- {lb}" for lb in u["_legal"]] + [""])
    lacunas = u.get("_lacunas") or []
    if lacunas:
        parts.extend(["## Lacunas investigativas", ""] + [f"- {x}" for x in lacunas] + [""])

    gosurf = u.get("artigos_gosurf") or []
    if gosurf:
        parts.extend(["## 📎 Dossiê Gosurf", ""])
        for g in gosurf:
            parts.append(f"- [{g['slug']}]({g['url']})")
        parts.append("")

    fontes = u.get("fontes_verificadas") or []
    if fontes:
        parts.extend(["## 📚 Fontes verificáveis", ""])
        for i, f in enumerate(fontes, 1):
            url = f.get("url", "")
            tit = f.get("titulo", "Fonte")
            if url:
                parts.append(f"{i}. [{tit}]({url})")
            else:
                parts.append(f"{i}. {tit}")
        parts.append("")

    fm = f"""---
title: "{yaml_escape(title)}"
description: "{desc}"
date: {date_iso}
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


def load_batches() -> list[dict]:
    entries: list[dict] = []

    bz_path = TODO / "lawfare-1511-1513-biazucci.json"
    if bz_path.is_file():
        bz = json.loads(bz_path.read_text(encoding="utf-8"))
        for e in bz.get("entries") or []:
            entries.append(biazucci_to_unified(e))

    dip_path = TODO / "lawfare-1512-1524-crise-diplomatica.json"
    if dip_path.is_file():
        dip = json.loads(dip_path.read_text(encoding="utf-8"))
        for a in dip.get("assuntos") or []:
            aid = a["id"]
            if aid in (1512, 1513):
                entries.append(crise_to_unified(a, reassign_id=aid + 13))
            elif aid >= 1514:
                entries.append(crise_to_unified(a))

    return entries


def merge_unified(new_entries: list[dict], dry_run: bool) -> int:
    data = json.loads(UNIFIED.read_text(encoding="utf-8"))
    existing: dict[str, dict] = {}
    for e in data.get("entradas") or []:
        k = str(e.get("id_corpus", ""))
        if k:
            existing[k] = e

    added = updated = 0
    for u in new_entries:
        k = u["id_corpus"]
        clean = {kk: vv for kk, vv in u.items() if not kk.startswith("_")}
        if k in existing:
            existing[k].update(clean)
            updated += 1
        else:
            existing[k] = clean
            added += 1

    data["entradas"] = sorted(existing.values(), key=lambda x: int(x.get("id_corpus") or 0))
    if not dry_run:
        UNIFIED.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"unified-corpus: +{added} novos, ~{updated} atualizados")
    return added + updated


def merge_lawfare(new_entries: list[dict], dry_run: bool) -> int:
    data = json.loads(LAWFARE.read_text(encoding="utf-8"))
    assuntos: list = data.get("assuntos") or []
    by_id = {a.get("id"): a for a in assuntos if a.get("id")}

    n = 0
    for u in new_entries:
        eid = int(u["id_corpus"])
        cats = u.get("jekyll_categories") or ["lawfare"]
        cat = cats[0]
        item = to_lawfare_assunto(u, cat)
        if eid in by_id:
            by_id[eid].update(item)
        else:
            assuntos.append(item)
            by_id[eid] = item
        n += 1

    assuntos.sort(key=lambda a: a.get("id") or 0)
    data["assuntos"] = assuntos
    data["total"] = len(assuntos)
    data["data_extração"] = date.today().isoformat()
    datas = [a["data_evento"] for a in assuntos if a.get("data_evento") and a["data_evento"] != "0001-01-01"]
    if datas:
        data["periodo"] = f"{min(datas)} a {max(datas)}"
    data["nota"] = (
        f"Merge todo batches {date.today().isoformat()}: IDs 1511-1526 "
        "(Biazucci 1511-1513, crise 1514-1524, Ramagem 1525-1526)."
    )
    if not dry_run:
        LAWFARE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"lawfare.json: {n} entradas mergeadas (total {len(assuntos)})")
    return n


def write_posts(new_entries: list[dict], dry_run: bool, force: bool) -> int:
    n = 0
    for u in new_entries:
        cats = u.get("jekyll_categories") or ["lawfare"]
        category = cats[0]
        target = POSTS / category / u["jekyll_filename"]
        if target.is_file() and not force:
            print(f"  skip (exists): {target.relative_to(ROOT)}")
            continue
        content = render_chirpy_post(u)
        if dry_run:
            print(f"  [dry-run] {target.relative_to(ROOT)}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            print(f"  OK {target.relative_to(ROOT)}")
        n += 1
    return n


def update_sync(last_id: int, dry_run: bool) -> None:
    if not SYNC.is_file():
        return
    data = json.loads(SYNC.read_text(encoding="utf-8"))
    tracks = data.setdefault("tracks", {})
    main = tracks.setdefault("main", {})
    main["last_id"] = last_id
    main["next_available"] = last_id + 1
    batches = main.setdefault("confirmed_batches", [])
    batches.append(
        {
            "range": [1511, last_id],
            "status": "confirmed",
            "notes": f"Merge todo batches {date.today().isoformat()}. Biazucci 1511-1513; crise 1514-1524; Ramagem 1525-1526.",
        }
    )
    sync = data.setdefault("sync_status", {})
    sync["main_track_last_sync"] = date.today().isoformat()
    sync["ids_confirmed_total"] = {
        "main_track": f"{last_id} (lawfare.json + unified-corpus)",
        "thematic_track": tracks.get("thematic", {}).get("last_id", 188),
    }
    open_items = sync.setdefault("open_items", [])
    note = "MERGE PCC batch 1449-1510 ainda pendente"
    if note not in open_items:
        open_items.append(note)
    if not dry_run:
        SYNC.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"sync: last_id={last_id}, next={last_id + 1}")


def copy_xarticles(dry_run: bool) -> list[str]:
    """Copia xarticles gosurf -> _posts/estudos/*-xarticle.md"""
    slugs = [
        "biazucci-erro-judiciario-cidh",
        "crise-diplomatica-brasil-eua-2025-2026",
        "reforma-tributaria-captura-regulatoria",
        "direita-permitida-dossie",
        "biomm-insider-operacao-completa",
    ]
    estudos = POSTS / "estudos"
    copied = []
    for slug in slugs:
        src = GOSURF / "artigos" / f"{slug}-xarticle.md"
        if not src.is_file():
            print(f"  xarticle ausente: {src.name}")
            continue
        dst = estudos / f"{slug}-xarticle.md"
        if dry_run:
            print(f"  [dry-run] copy {src.name}")
        else:
            estudos.mkdir(parents=True, exist_ok=True)
            dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"  copy {dst.name}")
        copied.append(slug)
    return copied


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force-posts", action="store_true", help="Sobrescreve posts existentes")
    ap.add_argument("--skip-xarticles", action="store_true")
    args = ap.parse_args()

    entries = load_batches()
    if not entries:
        print("Nenhuma entrada carregada dos batches todo.", file=sys.stderr)
        return 1

    print(f"Carregadas {len(entries)} entradas (IDs {entries[0]['id_corpus']}–{entries[-1]['id_corpus']})")
    merge_unified(entries, args.dry_run)
    merge_lawfare(entries, args.dry_run)
    n_posts = write_posts(entries, args.dry_run, args.force_posts)
    print(f"Posts: {n_posts} escritos")
    update_sync(1526, args.dry_run)

    if not args.skip_xarticles:
        print("Xarticles gosurf -> estudos:")
        copy_xarticles(args.dry_run)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
