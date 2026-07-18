#!/usr/bin/env python3
"""Exporta timeline de eventos relacionados a Bolsonaro (família e governo)."""
from __future__ import annotations

import json
import re
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAWFARE = ROOT / "_data" / "lawfare.json"
POSTS = ROOT / "_posts"
OUT = ROOT / "_data" / "export-bolsonaro-timeline.json"

PATTERN = re.compile(r"bolsonaro", re.I)
FAMILY = re.compile(
    r"\b(jair|flavio|flávio|eduardo|carlos|michelle|renan)\s+bolsonaro\b|"
    r"\bgoverno[- ]bolsonaro\b|"
    r"\bfam[ií]lia bolsonaro\b|"
    r"\bbolsonaro\b",
    re.I,
)


def slug_from_path(path: str) -> str:
    stem = Path(path.replace("\\", "/")).stem
    parts = stem.split("-", 3)
    return parts[3] if len(parts) > 3 and parts[0].isdigit() else stem


def classify_actor(text: str) -> str:
    t = text.lower()
    if re.search(r"\bjair\b|\bpresidente bolsonaro\b", t):
        return "jair-bolsonaro"
    if "flávio" in t or "flavio" in t:
        return "flavio-bolsonaro"
    if "eduardo" in t:
        return "eduardo-bolsonaro"
    if "carlos" in t:
        return "carlos-bolsonaro"
    if "michelle" in t:
        return "michelle-bolsonaro"
    if "governo bolsonaro" in t or "governo-bolsonaro" in t:
        return "governo-bolsonaro"
    return "bolsonaro-familia"


def parse_post_frontmatter(path: Path) -> dict | None:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fm = text[3:end]
    data: dict = {}
    for line in fm.splitlines():
        if line.startswith("title:"):
            data["title"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("date:"):
            data["date"] = line.split(":", 1)[1].strip()[:10]
        elif line.startswith("description:"):
            val = line.split(":", 1)[1].strip().strip('"')
            if val and val != ">":
                data["description"] = val
        elif line.startswith("categories:"):
            data["categories"] = line.split(":", 1)[1].strip()
        elif line.startswith('id_corpus:'):
            data["id_corpus"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("permalink:"):
            data["permalink"] = line.split(":", 1)[1].strip()
    stem = path.stem
    if not data.get("date") and len(stem) >= 10 and stem[:4].isdigit():
        data["date"] = stem[:10]
    return data


def entry_from_lawfare(a: dict) -> dict:
    titulo = a.get("titulo") or ""
    desc = a.get("descricao") or titulo
    arquivo = (a.get("fonte_arquivo") or "").replace("\\", "/")
    return {
        "id_corpus": a.get("id"),
        "data_evento": a.get("data_evento") or "",
        "data_iso": a.get("data_iso") or "",
        "titulo": titulo,
        "descricao": desc,
        "categoria": a.get("categoria") or "",
        "tags": a.get("tags") or [],
        "ator_principal": classify_actor(titulo + " " + desc),
        "pessoas_envolvidas": a.get("pessoas_envolvidas") or [],
        "instituicoes_envolvidas": a.get("instituicoes_envolvidas") or [],
        "fontes": a.get("fontes") or [],
        "fonte_arquivo": arquivo,
        "slug": slug_from_path(arquivo) if arquivo else "",
        "permalink": f"/posts/{slug_from_path(arquivo)}/" if arquivo else "",
        "origem": "lawfare.json",
    }


def entry_from_post(path: Path, fm: dict) -> dict:
    rel = str(path.relative_to(ROOT)).replace("\\", "/")
    slug = slug_from_path(rel)
    title = fm.get("title") or slug
    desc = fm.get("description") or title
    return {
        "id_corpus": fm.get("id_corpus"),
        "data_evento": fm.get("date") or "",
        "data_iso": f"{(fm.get('date') or '')[:10]}T12:00:00.000Z" if fm.get("date") else "",
        "titulo": title,
        "descricao": desc,
        "categoria": (fm.get("categories") or path.parent.name).strip(),
        "tags": [],
        "ator_principal": classify_actor(title + " " + desc + " " + rel),
        "pessoas_envolvidas": [],
        "instituicoes_envolvidas": [],
        "fontes": [],
        "fonte_arquivo": rel,
        "slug": slug,
        "permalink": fm.get("permalink") or f"/posts/{slug}/",
        "origem": "jekyll_post",
    }


def normalize_title(t: str) -> str:
    return re.sub(r"\s+", " ", (t or "").strip().lower())[:120]


def dedupe_key(e: dict) -> str:
    if e.get("id_corpus") not in (None, "", "null"):
        return f"id:{e['id_corpus']}"
    d = e.get("data_evento") or ""
    return f"day:{d}|{normalize_title(e.get('titulo', ''))}"


def main() -> None:
    lf = json.loads(LAWFARE.read_text(encoding="utf-8"))
    by_key: dict[str, dict] = {}

    for a in lf.get("assuntos", []):
        blob = " ".join([
            str(a.get("titulo", "")),
            str(a.get("descricao", "")),
            " ".join(a.get("tags") or []),
            " ".join(a.get("pessoas_envolvidas") or []),
            str(a.get("fonte_arquivo", "")),
        ])
        if PATTERN.search(blob):
            e = entry_from_lawfare(a)
            if (e.get("descricao") or "").strip() in (">", ""):
                e["descricao"] = e.get("titulo") or ""
            key = dedupe_key(e)
            prev = by_key.get(key)
            if prev is None or (prev["origem"] == "jekyll_post" and len(e.get("descricao", "")) > len(prev.get("descricao", ""))):
                by_key[key] = e
            continue

    for md in POSTS.rglob("*.md"):
        rel = str(md.relative_to(ROOT)).replace("\\", "/")
        name_hit = PATTERN.search(md.name) or PATTERN.search(rel)
        fm = parse_post_frontmatter(md)
        if not fm and not name_hit:
            continue
        blob = " ".join([
            md.name,
            rel,
            str((fm or {}).get("title", "")),
            str((fm or {}).get("description", "")),
        ])
        if not (name_hit or PATTERN.search(blob)):
            continue
        if not fm:
            fm = {"title": md.stem, "date": md.stem[:10] if md.stem[:4].isdigit() else ""}
        e = entry_from_post(md, fm)
        if (e.get("descricao") or "").strip() in (">", ""):
            e["descricao"] = e.get("titulo") or ""
        key = dedupe_key(e)
        prev = by_key.get(key)
        if prev is None:
            by_key[key] = e
        elif prev["origem"] == "lawfare.json" and e.get("data_evento") and not prev.get("data_evento"):
            by_key[key] = e

    entradas = [
        e for e in by_key.values()
        if e.get("data_evento") not in ("", "0001-01-01")
    ]

    # Segunda passagem: mesmo evento em IDs distintos (ex.: lawfare + stf)
    merged: dict[str, dict] = {}
    for e in entradas:
        key = f"{e.get('data_evento')}|{normalize_title(e.get('titulo', ''))}"
        prev = merged.get(key)
        if prev is None:
            merged[key] = e
            continue
        score = lambda x: (
            (1 if x.get("id_corpus") else 0),
            len(x.get("descricao") or ""),
            1 if x.get("origem") == "lawfare.json" else 0,
        )
        if score(e) > score(prev):
            merged[key] = e

    entradas = sorted(
        merged.values(),
        key=lambda x: (x.get("data_evento") or "9999", str(x.get("id_corpus") or "")),
    )

    datas = [e["data_evento"] for e in entradas if e.get("data_evento") and e["data_evento"] != "0001-01-01"]
    atores: dict[str, int] = {}
    for e in entradas:
        a = e.get("ator_principal") or "bolsonaro-familia"
        atores[a] = atores.get(a, 0) + 1

    out = {
        "meta": {
            "descricao": "Timeline de eventos relacionados a Jair Bolsonaro, família e governo (2019–2026)",
            "methodology_ref": "METHODOLOGY.md v2.3",
            "exportado_em": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "gerado_por": "tools/export_bolsonaro_timeline.py",
            "filtro": "bolsonaro (titulo, descricao, tags, pessoas, filename)",
            "total_entradas": len(entradas),
            "periodo": f"{min(datas)} a {max(datas)}" if datas else "",
            "distribuicao_atores": atores,
            "license": "CC0 1.0",
        },
        "entradas": entradas,
    }

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {len(entradas)} entradas -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
