#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sincroniza _data/todo/*.json pendentes com artigos Jekyll e corpus.

Detecta automaticamente:
  - Arquivos T-NNN*.json ou tipo analise_estrutural -> estudos (thematic track)
  - Demais JSON com id numerico -> posts timeline (main track)

Uso:
  python scripts/sync_todo_current.py
  python scripts/sync_todo_current.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODO = ROOT / "_data" / "todo"
PROC = ROOT / "_data" / "processados"
POSTS = ROOT / "_posts"
LAWFARE = ROOT / "_data" / "lawfare.json"
UNIFIED = ROOT / "_data" / "lawfare-unified-corpus.json"
SYNC = ROOT / "_data" / "claude.ai-corpus-ids-sync.json"

IMAGE_BY_CATEGORY = {
    "operacoes": "/assets/solid/bullseye.svg",
    "escandalos": "/assets/solid/skull.svg",
    "stf": "/assets/solid/gavel.svg",
    "justica": "/assets/solid/hammer.svg",
    "bancos": "/assets/solid/landmark.svg",
    "lawfare": "/assets/solid/weight-scale.svg",
    "crise-diplomatica": "/assets/solid/globe.svg",
}


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")[:90]


def yaml_escape(s: str) -> str:
    return s.replace('"', '\\"').replace("\n", " ")


def format_iso(d: str) -> str:
    return f"{(d or '2026-01-01')[:10]}T12:00:00.000Z"


def thematic_id_from_file(path: Path, data: dict) -> int | None:
    m = re.search(r"T-(\d+)", path.stem, re.I)
    if m:
        return int(m.group(1))
    eid = data.get("id")
    tipo = (data.get("tipo") or "").lower()
    if tipo in ("analise_estrutural", "lacuna_investigativa") and isinstance(eid, int) and eid >= 100:
        return eid
    return None


def resolve_category(entry: dict) -> str:
    cat = (entry.get("category") or entry.get("categoria") or entry.get("tipo") or "").lower()
    title = (entry.get("title") or entry.get("titulo") or "").lower()
    tags = [str(t).lower() for t in entry.get("tags") or entry.get("padroes_ativados") or []]

    mapping = {
        "operacao_policial": "operacoes",
        "operacao": "operacoes",
        "operacoes": "operacoes",
        "perseguicao_processual": "stf",
        "judicial": "justica",
        "crise-diplomatica": "crise-diplomatica",
        "censura-digital": "lawfare",
    }
    if cat in mapping:
        return mapping[cat]
    if "operacao" in cat or "operacao" in tags:
        return "operacoes"
    if "moraes" in title or "stf" in title or "calunia" in title:
        return "stf"
    if "pcc" in title or "cv" in title or "garimpo" in title:
        return "operacoes"
    if "master" in title or "vorcaro" in title:
        return "bancos"
    return "escandalos"


def build_tags(entry: dict, category: str) -> list[str]:
    tags: list[str] = []
    for src in (entry.get("padroes_ativados"), entry.get("patterns"), entry.get("tags")):
        if src:
            tags.extend(str(x) for x in src)
    if entry.get("slug"):
        tags.append(entry["slug"][:40])
    if category not in tags:
        tags.insert(0, category)
    return list(dict.fromkeys(tags))[:12]


def parse_actors(raw_actors) -> list[str]:
    out: list[str] = []
    for a in raw_actors or []:
        if isinstance(a, dict):
            n = a.get("name") or a.get("nome", "")
            r = a.get("role") or a.get("papel", "")
            out.append(f"{n} ({r})" if r else n)
        else:
            out.append(str(a))
    return out


def parse_fontes(entry: dict) -> list[dict]:
    fontes: list[dict] = []
    ev = entry.get("evidencia_primaria") or {}
    if ev.get("url_referencia"):
        for url in str(ev["url_referencia"]).split(";"):
            url = url.strip()
            if url:
                fontes.append({"titulo": ev.get("fonte", "Fonte"), "url": url})
    for s in entry.get("sources") or entry.get("fontes") or []:
        if isinstance(s, dict):
            fontes.append({
                "titulo": s.get("title") or s.get("titulo") or s.get("name") or s.get("outlet") or "Fonte",
                "url": s.get("url") or "",
            })
    return fontes


def normalize_main_entry(entry: dict, source: str) -> dict | None:
    eid = entry.get("id")
    if eid is None:
        return None

    title = entry.get("title") or entry.get("titulo", "")
    if not title:
        return None

    jdate = (
        entry.get("date")
        or entry.get("data_evento")
        or entry.get("data_registro")
        or entry.get("jekyll_date")
        or ""
    )[:10]

    ev = entry.get("evidencia_primaria") or {}
    resumo = (
        entry.get("summary")
        or entry.get("descricao")
        or ev.get("descricao")
        or entry.get("resumo")
        or ""
    )

    cat = resolve_category(entry)
    slug = entry.get("slug") or slugify(title)
    fname_md = entry.get("jekyll_filename") or f"{jdate}-{slugify(title)}.md"
    if not fname_md.endswith(".md"):
        fname_md += ".md"

    lacunas = entry.get("lacuna_investigativa") or entry.get("evidentiary_caveat") or ""
    if isinstance(lacunas, str):
        lacunas_list = [lacunas] if lacunas else []
    else:
        lacunas_list = list(lacunas)

    return {
        "id_corpus": str(int(eid)),
        "jekyll_filename": fname_md,
        "jekyll_date": jdate,
        "jekyll_categories": [cat],
        "jekyll_tags": build_tags(entry, cat),
        "jekyll_permalink": f"/posts/{Path(fname_md).stem}/",
        "titulo": title,
        "resumo": resumo,
        "categoria": entry.get("category") or entry.get("categoria") or entry.get("tipo") or cat,
        "pais": entry.get("pais", "Brasil"),
        "atores": parse_actors(entry.get("actors") or entry.get("atores")),
        "instituicoes": entry.get("institutions") or entry.get("instituicoes") or [],
        "fontes_verificadas": parse_fontes(entry),
        "_analise": entry.get("analise") or entry.get("observacao_analitica") or "",
        "_result": entry.get("result") or "",
        "_legal": entry.get("legal_basis") or entry.get("legal_refs") or [],
        "_lacunas": lacunas_list,
        "_open_questions": entry.get("open_questions") or [],
        "_cadeia": entry.get("cadeia_logica") or "",
        "_nota_correcao": entry.get("nota_correcao_midiatica"),
        "_source": source,
    }


def render_timeline_post(u: dict) -> str:
    category = u["jekyll_categories"][0]
    tags = u.get("jekyll_tags") or []
    title = u["titulo"]
    resumo = u["resumo"]
    desc = yaml_escape((resumo[:157] + "...") if len(resumo) > 157 else resumo)
    image = IMAGE_BY_CATEGORY.get(category, "/assets/solid/circle-exclamation.svg")
    fm_tags = json.dumps(tags, ensure_ascii=False)

    parts = [
        "- &nbsp;",
        "{:toc .large-only}",
        "",
        f"# {title}",
        "",
        "***",
        "",
        "## Resumo",
        "",
        resumo,
        "",
        "***",
        "",
        "## Metadados do corpus",
        "",
        "| Campo | Valor |",
        "| --- | --- |",
        f"| `id_corpus` | **{u.get('id_corpus', '')}** |",
        f"| Categoria analitica | {u.get('categoria', '-') } |",
        "",
    ]
    if u.get("conflito_nota"):
        parts.extend([f"> **Nota de conflito ID:** {u['conflito_nota']}", ""])
    if u.get("_cadeia"):
        parts.extend(["## Cadeia logica", "", u["_cadeia"], ""])
    if u.get("atores"):
        parts.extend(["### Atores", ""] + [f"- {a}" for a in u["atores"]] + [""])
    if u.get("instituicoes"):
        parts.extend(["### Instituicoes", ""] + [f"- {i}" for i in u["instituicoes"]] + [""])
    if u.get("_result"):
        parts.extend(["## Resultado documentado", "", u["_result"], ""])
    if u.get("_analise") and u["_analise"] != resumo:
        parts.extend(["## Analise", "", u["_analise"], ""])
    if u.get("_legal"):
        parts.extend(["## Base legal", ""] + [f"- {lb}" for lb in u["_legal"]] + [""])
    nc = u.get("_nota_correcao")
    if nc:
        parts.extend([
            "## Nota de correcao midiatica",
            "",
            f"**Alegacao:** {nc.get('alegacao_circulando', '')}",
            "",
            f"**Correcao:** {nc.get('correcao', '')}",
            "",
        ])
    lacunas = u.get("_lacunas") or []
    if lacunas:
        parts.extend(["## Lacunas investigativas", ""] + [f"- {x}" for x in lacunas] + [""])
    oq = u.get("_open_questions") or []
    if oq:
        parts.extend(["## Questoes em aberto", ""] + [f"- {x}" for x in oq] + [""])
    fontes = u.get("fontes_verificadas") or []
    if fontes:
        parts.extend(["## Fontes verificaveis", ""])
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
permalink: {u.get('jekyll_permalink', '')}
id_corpus: "{u.get('id_corpus', '')}"
corpus_unificado: true
source_data: "{u.get('_source', '')}"
---

"""
    return fm + "\n".join(parts)


def study_title(data: dict) -> str:
    return data.get("titulo") or data.get("title") or ""


def study_date(data: dict) -> str:
    return (data.get("data_registro") or data.get("data_evento") or data.get("date") or "2026-01-01")[:10]


def render_estudos_post(data: dict, tid: int) -> tuple[str, str]:
    short_title = study_title(data)
    slug = data.get("slug") or slugify(short_title)
    slug = re.sub(r"^revisar-t\d+-", "", slug, flags=re.I)
    jdate = study_date(data)
    fname = f"{jdate}-{slug}.md"
    title = f"T-{tid} · {short_title.split('—')[0].strip()}" if "—" in short_title else f"T-{tid} · {short_title[:70]}"
    ev = data.get("evidencia_primaria") or {}
    resumo = (
        ev.get("descricao")
        or data.get("summary")
        or (data.get("analise") or "")[:400]
    )
    desc = yaml_escape((resumo[:157] + "...") if len(resumo) > 157 else resumo)
    padroes = data.get("padroes_ativados") or data.get("patterns") or []
    tags = ["estudo", "lawfare"] + [str(p).lower() for p in padroes]
    if data.get("slug"):
        tags.append(data["slug"][:35])
    tags = list(dict.fromkeys(tags))[:12]
    fm_tags = json.dumps(tags, ensure_ascii=False)

    parts = [
        "- &nbsp;",
        "{:toc .large-only}",
        "",
        f"# {title}",
        "",
        resumo[:800] + ("..." if len(resumo) > 800 else ""),
        "",
    ]
    if data.get("cadeia_logica"):
        parts.extend(["## Cadeia logica", "", data["cadeia_logica"], ""])
    correcoes = data.get("correcoes_fonte_secundaria") or []
    if correcoes:
        parts.extend(["## Correcoes de fonte secundaria", "", "| Item | Citado | Correto |", "| --- | --- | --- |"])
        for c in correcoes:
            parts.append(
                f"| {c.get('item', '-')} | {c.get('citado_incorretamente_como', '-')} | {c.get('correto', '-')} |"
            )
        parts.append("")
    if data.get("analise"):
        parts.extend(["## Analise", "", data["analise"], ""])
    if data.get("lacuna_investigativa"):
        parts.extend(["## Lacuna investigativa", "", data["lacuna_investigativa"], ""])
    pats = data.get("patterns_cruzados") or padroes
    if pats:
        parts.extend(["## Padroes", ""])
        if pats and isinstance(pats[0], dict):
            for p in pats:
                parts.append(f"- **{p.get('id', '')}** — {p.get('descricao', '')}")
        else:
            parts.extend([f"- {p}" for p in pats])
        parts.append("")
    conns = data.get("connections") or []
    if conns:
        parts.extend(["## Conexoes", ""] + [f"- {c}" for c in conns] + [""])
    fonte_lines: list[str] = []
    url = ev.get("url_referencia", "")
    if url:
        for u in str(url).split(";"):
            u = u.strip()
            if u:
                fonte_lines.append(f"- [{ev.get('fonte', 'Fonte')}]({u})")
    for s in data.get("sources") or data.get("fontes") or []:
        if isinstance(s, dict) and s.get("url"):
            tit = s.get("title") or s.get("titulo") or s.get("outlet") or "Fonte"
            fonte_lines.append(f"- [{tit}]({s['url']})")
    if fonte_lines:
        parts.extend(["## Fontes", ""] + fonte_lines + [""])
    parts.append(f"*Dossie T-{tid} · CC0 · lawfare-timeline*")

    fm = f"""---
id_corpus: "T-{tid}"
thematic_track: true
title: "{yaml_escape(title)}"
description: "{desc}"
date: {jdate}T12:00:00-03:00
image:
  path: "/assets/solid/book-open.svg"
tags: {fm_tags}
categories: estudos
mermaid: false
pin: false
permalink: /posts/{Path(fname).stem}/
source_data: "{data.get('_source_file', '')}"
---

"""
    return fm + "\n".join(parts), fname


def to_lawfare_assunto(u: dict, category: str) -> dict:
    rel = POSTS / category / u["jekyll_filename"]
    fonte = str(rel.relative_to(ROOT)).replace("/", "\\")
    tags = u.get("jekyll_tags") or [category]
    fontes = [f.get("url") for f in u.get("fontes_verificadas") or [] if f.get("url")]
    return {
        "titulo": u["titulo"],
        "data_evento": u["jekyll_date"],
        "data_iso": format_iso(u["jekyll_date"]),
        "categoria": category,
        "tags": tags if isinstance(tags, list) else [tags],
        "descricao": u["resumo"],
        "relevancia": "alta",
        "impacto_diplomatico": "N/A",
        "tipo_escandalo": u.get("categoria", "N/A"),
        "fontes": fontes,
        "pessoas_envolvidas": u.get("atores") or [],
        "instituicoes_envolvidas": u.get("instituicoes") or [],
        "pais": u.get("pais", "Brasil"),
        "valor_envolvido": "N/A",
        "prioridade": 1,
        "fonte_arquivo": fonte,
        "id": int(u["id_corpus"]),
    }


def load_todo_files() -> list[Path]:
    return sorted(TODO.glob("*.json"))


def process_all(dry_run: bool) -> tuple[list[dict], list[tuple[int, str, str]], list[str]]:
    main_entries: list[dict] = []
    thematic: list[tuple[int, str, str]] = []
    archived: list[str] = []

    for fpath in load_todo_files():
        try:
            data = json.loads(fpath.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"ERRO {fpath.name}: {exc}")
            continue

        tid = thematic_id_from_file(fpath, data)
        if tid is not None:
            data["_source_file"] = fpath.name
            content, md_fname = render_estudos_post(data, tid)
            target = POSTS / "estudos" / md_fname
            if dry_run:
                print(f"  [dry-run] T-{tid}: {target.relative_to(ROOT)}")
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
                print(f"  OK {target.relative_to(ROOT)}")
            thematic.append((tid, fpath.name, md_fname))
            archived.append(fpath.name)
            continue

        if isinstance(data, dict) and isinstance(data.get("entries"), list):
            items = data["entries"]
        elif isinstance(data, list):
            items = data
        else:
            items = [data]
        for item in items:
            u = normalize_main_entry(item, fpath.name)
            if not u:
                continue
            main_entries.append(u)
            target = POSTS / u["jekyll_categories"][0] / u["jekyll_filename"]
            if dry_run:
                print(f"  [dry-run] ID {u['id_corpus']}: {target.relative_to(ROOT)}")
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(render_timeline_post(u), encoding="utf-8")
                print(f"  OK {target.relative_to(ROOT)}")
        archived.append(fpath.name)

    return main_entries, thematic, archived


def update_lawfare(entries: list[dict], dry_run: bool) -> None:
    if not entries or dry_run:
        return
    lf_data = json.loads(LAWFARE.read_text(encoding="utf-8"))
    assuntos = lf_data.get("assuntos", [])
    new_ids = {int(u["id_corpus"]) for u in entries}
    assuntos = [a for a in assuntos if a.get("id") not in new_ids]
    for u in entries:
        assuntos.append(to_lawfare_assunto(u, u["jekyll_categories"][0]))
    assuntos.sort(key=lambda x: x.get("id") or 0)
    lf_data["assuntos"] = assuntos
    lf_data["total"] = len(assuntos)
    lf_data["data_extração"] = date.today().isoformat()
    datas = [a["data_evento"] for a in assuntos if a.get("data_evento") and a["data_evento"] != "0001-01-01"]
    if datas:
        lf_data["periodo"] = f"{min(datas)} a {max(datas)}"
    LAWFARE.write_text(json.dumps(lf_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"lawfare.json: +{len(entries)} assuntos (total {len(assuntos)})")


def update_unified(entries: list[dict], dry_run: bool) -> None:
    if not entries or dry_run or not UNIFIED.is_file():
        return
    uni_data = json.loads(UNIFIED.read_text(encoding="utf-8"))
    entradas = uni_data.get("entradas", [])
    new_ids = {int(u["id_corpus"]) for u in entries}
    entradas = [e for e in entradas if int(e.get("id_corpus", 0)) not in new_ids]
    for u in entries:
        clean = {k: v for k, v in u.items() if not k.startswith("_")}
        clean["verificado"] = True
        clean["status_publicacao"] = "coberto_por_artigo"
        clean["id_corpus"] = u["id_corpus"]
        entradas.append(clean)
    entradas.sort(key=lambda x: int(x.get("id_corpus") or 0))
    uni_data["entradas"] = entradas
    UNIFIED.write_text(json.dumps(uni_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"lawfare-unified-corpus.json: +{len(entries)} entradas")


def update_sync(main_entries: list[dict], thematic: list[tuple[int, str, str]], dry_run: bool) -> None:
    if dry_run or not SYNC.is_file():
        return
    sync_data = json.loads(SYNC.read_text(encoding="utf-8"))
    batch_note = f"Merge todo {date.today().isoformat()}"

    if main_entries:
        new_ids = [int(u["id_corpus"]) for u in main_entries]
        last_main = max(new_ids)
        main = sync_data.setdefault("tracks", {}).setdefault("main", {})
        main["last_id"] = last_main
        main["next_available"] = last_main + 1
        main["last_confirmed"] = last_main
        main["last_jekyll_published"] = last_main
        main.setdefault("confirmed_batches", []).append({
            "range": [min(new_ids), last_main],
            "status": "confirmed",
            "notes": f"{batch_note}: main IDs {min(new_ids)}-{last_main}.",
        })

    if thematic:
        last_t = max(t[0] for t in thematic)
        thematic_track = sync_data.setdefault("tracks", {}).setdefault("thematic", {})
        thematic_track["last_id"] = last_t
        thematic_track["next_available"] = last_t + 1
        entries = thematic_track.setdefault("entries", [])
        existing_ids = {int(e["id"]) for e in entries}
        for tid, fname, md_fname in thematic:
            note = f"Estudo Jekyll _posts/estudos/{md_fname}"
            if tid in existing_ids:
                for e in entries:
                    if int(e["id"]) == tid:
                        e.update({"status": "confirmed", "artifact": md_fname, "notes": note})
            else:
                entries.append({
                    "id": tid,
                    "status": "confirmed",
                    "topic": f"T-{tid} ({fname})",
                    "artifact": md_fname,
                    "notes": note,
                })
        entries.sort(key=lambda x: int(x["id"]))

    sync_status = sync_data.setdefault("sync_status", {})
    sync_status["main_track_last_sync"] = date.today().isoformat()
    sync_status["thematic_track_last_sync"] = date.today().isoformat()
    if main_entries:
        sync_status.setdefault("ids_confirmed_total", {})["main_track"] = (
            f"{max(int(u['id_corpus']) for u in main_entries)} (Jekyll + lawfare.json)"
        )
    if thematic:
        sync_status.setdefault("ids_confirmed_total", {})["thematic_track"] = max(t[0] for t in thematic)

    SYNC.write_text(json.dumps(sync_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("claude.ai-corpus-ids-sync.json atualizado.")


def archive_files(fnames: list[str], dry_run: bool) -> None:
    PROC.mkdir(parents=True, exist_ok=True)
    for fname in fnames:
        src = TODO / fname
        if not src.is_file():
            continue
        dst = PROC / fname
        if dry_run:
            print(f"  [dry-run] archive {fname}")
            continue
        if dst.is_file():
            src.unlink()
        else:
            shutil.move(str(src), str(dst))
        print(f"  archive -> processados/{fname}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    files = load_todo_files()
    if not files:
        print("Nenhum JSON em _data/todo/")
        return 0

    print(f"=== Processando {len(files)} arquivo(s) em _data/todo/ ===")
    main_entries, thematic, archived = process_all(args.dry_run)

    update_lawfare(main_entries, args.dry_run)
    update_unified(main_entries, args.dry_run)
    update_sync(main_entries, thematic, args.dry_run)

    print("\n=== Arquivar JSON processados ===")
    archive_files(list(dict.fromkeys(archived)), args.dry_run)

    print(f"\nConcluido: {len(main_entries)} posts timeline, {len(thematic)} estudos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
