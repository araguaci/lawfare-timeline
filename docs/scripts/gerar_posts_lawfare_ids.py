#!/usr/bin/env python3
"""Gera posts Jekyll a partir de entradas em lawfare.json (instancia_padrao ou assuntos)."""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from sync_todo_current import POSTS, LAWFARE, render_timeline_post

IMAGE_BY_CATEGORY = {
    "crise-diplomatica": "/assets/solid/globe.svg",
    "lawfare": "/assets/solid/weight-scale.svg",
    "escandalos": "/assets/solid/skull.svg",
    "operacoes": "/assets/solid/bullseye.svg",
}


def slugify(text: str, max_len: int = 90) -> str:
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")[:max_len]


def resolve_category(raw: dict) -> str:
    op = (raw.get("operacao_referencia") or "").lower()
    slug = (raw.get("slug") or "").lower()
    titulo = (raw.get("titulo") or "").lower()
    if any(k in op for k in ("geopolítica", "geopolitica", "brasil–eua", "brasil-eua")):
        return "crise-diplomatica"
    if "compliance zero" in op and "elei" in op:
        return "lawfare"
    if any(k in titulo or k in slug for k in ("trump", "escudo das américas", "escudo das americas", "casa branca")):
        return "crise-diplomatica"
    if raw.get("tipo") == "instancia_padrao":
        return "operacoes"
    return "escandalos"


def build_tags(raw: dict, category: str) -> list[str]:
    tags: list[str] = [category]
    for src in (raw.get("padroes_ativados"), raw.get("patterns"), raw.get("tags")):
        if src:
            for x in src:
                t = str(x).lower()
                if t not in tags:
                    tags.append(t)
    slug = raw.get("slug")
    if slug and slug not in tags:
        tags.append(slug[:40])
    return tags[:10]


def evidence_status(raw: dict) -> str:
    ev = raw.get("evidencia_primaria") or {}
    cls = (ev.get("classificacao") or "").lower()
    if cls == "primária" or cls == "primaria":
        return "ev-confirmed"
    if cls == "secundária" or cls == "secundaria":
        return "ev-alleged"
    return "ev-confirmed" if raw.get("status") == "confirmado" else ""


def instancia_to_post(raw: dict) -> dict:
    eid = int(raw["id"])
    title = raw.get("titulo", "")
    jdate = (raw.get("data_evento") or raw.get("data_registro") or "2026-01-01")[:10]
    slug = raw.get("slug") or slugify(title)
    fname = f"{jdate}-{slug}.md"
    cat = resolve_category(raw)
    ev = raw.get("evidencia_primaria") or {}

    actors: list[str] = []
    for a in raw.get("atores") or []:
        if isinstance(a, dict):
            n = a.get("nome") or a.get("name", "")
            fn = a.get("funcao_estrutural") or a.get("role", "")
            cargo = a.get("cargo_na_epoca") or a.get("cargo", "")
            bit = fn or cargo
            actors.append(f"{n} ({bit})" if bit else n)

    fontes = []
    if ev.get("url_referencia"):
        fontes.append({"titulo": ev.get("fonte") or title[:80], "url": ev["url_referencia"]})

    conns = [
        f"id_{c['id_ref']} — {c.get('descricao', '').strip()}"
        for c in (raw.get("conexoes_corpus") or [])
        if c.get("id_ref") is not None
    ]

    return {
        "id_corpus": str(eid),
        "jekyll_filename": fname,
        "jekyll_date": jdate,
        "jekyll_categories": [cat],
        "jekyll_tags": build_tags(raw, cat),
        "jekyll_permalink": f"/posts/{Path(fname).stem}/",
        "titulo": title,
        "resumo": ev.get("descricao") or raw.get("observacao_analitica") or "",
        "categoria": raw.get("tipo") or cat,
        "atores": actors,
        "instituicoes": [],
        "fontes_verificadas": fontes,
        "_analise": raw.get("observacao_analitica", ""),
        "_cadeia": raw.get("cadeia_logica", ""),
        "_connections": conns,
        "_evidence_status": evidence_status(raw),
        "_operacao": raw.get("operacao_referencia", ""),
        "_lacunas": [],
        "_source": f"lawfare.json id_{eid}",
    }


def load_entries(ids: list[int]) -> list[dict]:
    data = json.loads(LAWFARE.read_text(encoding="utf-8"))
    by_id = {a.get("id"): a for a in data.get("assuntos") or [] if a.get("id") is not None}
    missing = [i for i in ids if i not in by_id]
    if missing:
        raise SystemExit(f"IDs ausentes em lawfare.json: {missing}")
    return [by_id[i] for i in ids]


def update_fonte_arquivo(ids: list[int], paths: dict[int, Path]) -> None:
    data = json.loads(LAWFARE.read_text(encoding="utf-8"))
    for item in data.get("assuntos") or []:
        eid = item.get("id")
        if eid in paths:
            rel = str(paths[eid].relative_to(ROOT)).replace("/", "\\")
            item["fonte_arquivo"] = rel
    LAWFARE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", type=int, nargs="+", help="IDs main track em lawfare.json")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    written: dict[int, Path] = {}
    for raw in load_entries(args.ids):
        u = instancia_to_post(raw)
        cat = u["jekyll_categories"][0]
        folder = POSTS / cat
        target = folder / u["jekyll_filename"]
        content = render_timeline_post(u)

        if args.dry_run:
            print(f"  [dry-run] {target.relative_to(ROOT)}")
            continue

        folder.mkdir(parents=True, exist_ok=True)
        if target.is_file():
            print(f"  SKIP (exists) {target.relative_to(ROOT)}")
        else:
            target.write_text(content, encoding="utf-8")
            print(f"  OK {target.relative_to(ROOT)}")
        written[int(u["id_corpus"])] = target

    if written and not args.dry_run:
        update_fonte_arquivo(list(written.keys()), written)
        print(f"  lawfare.json fonte_arquivo atualizado para {len(written)} ID(s)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
