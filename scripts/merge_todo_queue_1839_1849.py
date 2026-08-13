#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merge pending _data/todo batches 1839-1849 + T-251 into corpus and posts."""
from __future__ import annotations

import json
import re
import shutil
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODO = ROOT / "_data" / "todo"
PROC = ROOT / "_data" / "processados"
POSTS = ROOT / "_posts"
LAWFARE = ROOT / "_data" / "lawfare.json"
SYNC = ROOT / "_data" / "claude.ai-corpus-ids-sync.json"

IMAGE_BY_CATEGORY = {
    "penduricalhos": "/assets/solid/gift.svg",
    "stf": "/assets/solid/gavel.svg",
    "escandalos": "/assets/solid/skull.svg",
    "crise-diplomatica": "/assets/solid/globe.svg",
    "bancos": "/assets/solid/landmark.svg",
    "lawfare": "/assets/solid/weight-scale.svg",
    "justica": "/assets/solid/hammer.svg",
    "estudos": "/assets/solid/book-open.svg",
}

BATCH_FILES = [
    "lawfare-batch-janja-telegram-eua-1839-1841.json",
    "lawfare-batch-cnj-penduricalhos-retroativos-1842.json",
    "lawfare-batch-moraes-master-convergencia-1843-1849.json",
]


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")[:90]


def yaml_escape(s: str) -> str:
    return s.replace('"', '\\"')


def resolve_category(entry: dict) -> str:
    eid = int(entry.get("id") or 0)
    title = (entry.get("title") or entry.get("titulo") or "").lower()
    cat = (entry.get("category") or entry.get("categoria") or "").lower()
    if eid == 1842 or "penduricalho" in title or "ats" in title or "quinquênio" in title:
        return "penduricalhos"
    if eid == 1841 or "visto" in title or "itamaraty" in title or "incidente_diplomatico" in cat:
        return "crise-diplomatica"
    if eid == 1839:
        return "escandalos"
    if "banco master" in title or eid in (1843,):
        return "bancos" if "contrato" in title else "stf"
    if eid in (1840, 1843, 1844, 1845, 1846, 1847, 1848, 1849) or "moraes" in title or "toffoli" in title or "gilmar" in title:
        return "stf"
    if "chokepoint" in cat or "abuso" in cat:
        return "stf"
    return "escandalos"


def actors_people(raw) -> list[str]:
    out = []
    for a in raw or []:
        if isinstance(a, dict):
            name = a.get("name") or a.get("nome") or ""
            role = a.get("role") or a.get("papel") or ""
            if name:
                out.append(f"{name} ({role})" if role else name)
        elif a:
            out.append(str(a))
    return out


def fontes_urls(raw) -> list[str]:
    urls = []
    for s in raw or []:
        if isinstance(s, dict) and s.get("url"):
            urls.append(s["url"])
        elif isinstance(s, str) and s.startswith("http"):
            urls.append(s)
    return urls


def fontes_md(raw) -> str:
    lines = []
    for i, s in enumerate(raw or [], 1):
        if isinstance(s, dict):
            title = s.get("title") or s.get("titulo") or "Fonte"
            url = s.get("url") or ""
            if url:
                lines.append(f"{i}. [{title}]({url})")
            else:
                lines.append(f"{i}. {title}")
        else:
            lines.append(f"{i}. {s}")
    return "\n".join(lines) if lines else "_Sem fontes registradas_"


def load_entries(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get("assuntos") or data.get("entries") or data.get("items") or [data]
    return []


def to_assunto(entry: dict, category: str, source_file: str) -> dict:
    eid = int(entry["id"])
    title = (entry.get("title") or entry.get("titulo") or "").strip()
    date = str(entry.get("date") or entry.get("data_evento") or "2026-01-01")[:10]
    summary = (entry.get("summary") or entry.get("descricao") or entry.get("resumo") or "").strip()
    people = actors_people(entry.get("actors") or entry.get("pessoas_envolvidas"))
    inst = entry.get("institutions") or entry.get("instituicoes") or entry.get("instituicoes_envolvidas") or []
    tags = [category]
    for p in entry.get("patterns") or []:
        tags.append(str(p))
    if entry.get("evidence_status"):
        tags.append(entry["evidence_status"])
    tags = list(dict.fromkeys(tags))[:10]
    assunto = {
        "titulo": title,
        "data_evento": date,
        "data_iso": f"{date}T12:00:00Z",
        "categoria": category,
        "tags": tags,
        "descricao": summary,
        "relevancia": "alta",
        "impacto_diplomatico": "N/A",
        "tipo_escandalo": entry.get("category") or "N/A",
        "fontes": fontes_urls(entry.get("sources") or entry.get("fontes")) or ["N/A"],
        "pessoas_envolvidas": people,
        "instituicoes_envolvidas": list(inst),
        "pais": "Brasil",
        "valor_envolvido": "N/A",
        "prioridade": 1,
        "fonte_arquivo": f"_data\\\\todo\\\\{source_file}",
        "id": eid,
        "evidence_status": entry.get("evidence_status"),
        "status": entry.get("status"),
        "analise": entry.get("analise"),
        "lacuna_investigativa": entry.get("lacuna_investigativa"),
        "result": entry.get("result"),
        "connections": entry.get("connections") or [],
        "patterns": entry.get("patterns") or [],
        "legal_basis": entry.get("legal_basis") or [],
    }
    if entry.get("ponto_de_inflexao"):
        assunto["ponto_de_inflexao"] = entry["ponto_de_inflexao"]
    return assunto


def render_post(entry: dict, category: str, source_file: str) -> tuple[str, Path]:
    eid = int(entry["id"])
    title = (entry.get("title") or entry.get("titulo") or "").strip()
    date = str(entry.get("date") or entry.get("data_evento") or "2026-01-01")[:10]
    summary = (entry.get("summary") or entry.get("descricao") or "").strip()
    desc = yaml_escape((summary[:157] + "…") if len(summary) > 157 else summary)
    tags = [category] + [str(p) for p in (entry.get("patterns") or [])]
    tags = list(dict.fromkeys(tags))[:10]
    slug = slugify(title)
    fname = f"{date}-{slug}.md"
    image = IMAGE_BY_CATEGORY.get(category, "/assets/solid/circle-exclamation.svg")
    people = actors_people(entry.get("actors") or entry.get("pessoas_envolvidas"))
    inst = entry.get("institutions") or entry.get("instituicoes") or []
    result = entry.get("result") or ""
    analise = entry.get("analise") or ""
    lacuna = entry.get("lacuna_investigativa") or ""
    legal = entry.get("legal_basis") or []
    conns = entry.get("connections") or []

    body = f"""---
title: "{yaml_escape(title)}"
description: "{desc}"
date: {date}T12:00:00.000Z
image:
  path: "{image}"
tags: {json.dumps(tags, ensure_ascii=False)}
categories: {category}
permalink: /posts/{Path(fname).stem}/
id_corpus: "{eid}"
corpus_unificado: true
source_data: "{source_file}"
---

- &nbsp;
{{:toc .large-only}}

# {title}

***

## Resumo

{summary}

***

## Metadados do corpus

| Campo | Valor |
| --- | --- |
| `id_corpus` | **{eid}** |
| Categoria analitica | {entry.get('category') or category} |
| Evidencia | {entry.get('evidence_status') or 'N/A'} |
| Status | {entry.get('status') or 'N/A'} |

### Atores

{chr(10).join(f'- {p}' for p in people) if people else '- _N/A_'}

### Instituicoes

{chr(10).join(f'- {i}' for i in inst) if inst else '- _N/A_'}

## Resultado documentado

{result or '_N/A_'}

## Analise

{analise or '_N/A_'}

## Base legal

{chr(10).join(f'- {x}' for x in legal) if legal else '- _N/A_'}

## Conexoes

{chr(10).join(f'- {c}' for c in conns) if conns else '- _N/A_'}

## Lacunas investigativas

{lacuna or '_N/A_'}

## Fontes verificaveis

{fontes_md(entry.get('sources') or entry.get('fontes'))}
"""
    out_dir = POSTS / category
    out_dir.mkdir(parents=True, exist_ok=True)
    return body, out_dir / fname


def render_thematic(t: dict) -> tuple[str, Path]:
    tid = t["id"]
    title = f"{tid} · {t.get('topic') or t.get('titulo')}"
    date = str(t.get("date") or "2026-08-12")[:10]
    summary = (t.get("summary") or "").strip()
    desc = yaml_escape((summary[:157] + "…") if len(summary) > 157 else summary)
    tags = ["estudos"] + [str(p) for p in (t.get("patterns") or [])]
    tags = list(dict.fromkeys(tags))[:10]
    slug = slugify(title)
    fname = f"{date}-{slug}.md"
    body = f"""---
title: "{yaml_escape(title)}"
description: "{desc}"
date: {date}T12:00:00.000Z
image:
  path: "/assets/solid/book-open.svg"
tags: {json.dumps(tags, ensure_ascii=False)}
categories: estudos
permalink: /posts/{Path(fname).stem}/
id_corpus: "{tid}"
corpus_unificado: true
source_data: "lawfare-thematic-T251-convergencia-stf-master-familia.json"
---

- &nbsp;
{{:toc .large-only}}

# {title}

***

## Resumo

{summary}

***

## Análise estrutural

{t.get('analise_estrutural') or '_N/A_'}

## Lacunas investigativas

{t.get('lacuna_investigativa') or '_N/A_'}

## Conexões

{chr(10).join(f'- {c}' for c in (t.get('connections') or [])) or '- _N/A_'}

## Notas

{t.get('notes') or '_N/A_'}
"""
    out_dir = POSTS / "estudos"
    out_dir.mkdir(parents=True, exist_ok=True)
    return body, out_dir / fname


def main() -> int:
    lawfare = json.loads(LAWFARE.read_text(encoding="utf-8"))
    assuntos = lawfare.get("assuntos") or []
    existing = {a.get("id") for a in assuntos}
    created_posts = []
    merged_ids = []

    for fname in BATCH_FILES:
        path = TODO / fname
        if not path.is_file():
            print(f"SKIP missing {fname}")
            continue
        for entry in load_entries(path):
            eid = int(entry["id"])
            if eid in existing:
                print(f"SKIP already in corpus: {eid}")
                continue
            category = resolve_category(entry)
            assunto = to_assunto(entry, category, fname)
            assuntos.append(assunto)
            existing.add(eid)
            merged_ids.append(eid)
            body, out_path = render_post(entry, category, fname)
            out_path.write_text(body, encoding="utf-8")
            created_posts.append(str(out_path.relative_to(ROOT)))
            print(f"OK {eid} -> {category}/{out_path.name}")

    # Thematic T-251
    thematic_path = TODO / "lawfare-thematic-T251-convergencia-stf-master-familia.json"
    if thematic_path.is_file():
        t = json.loads(thematic_path.read_text(encoding="utf-8"))
        tid = t.get("id")
        # thematic stays as estudo post; also append lightweight assunto if numeric-less
        body, out_path = render_thematic(t)
        if not out_path.exists():
            out_path.write_text(body, encoding="utf-8")
            created_posts.append(str(out_path.relative_to(ROOT)))
            print(f"OK {tid} -> estudos/{out_path.name}")
        else:
            print(f"SKIP thematic post exists: {out_path.name}")

    assuntos.sort(key=lambda a: (a.get("data_evento") or "", a.get("id") or 0))
    lawfare["assuntos"] = assuntos
    if "data_extração" in lawfare:
        lawfare["data_extração"] = "2026-08-12"
    LAWFARE.write_text(json.dumps(lawfare, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"lawfare.json atualizado; novos IDs: {merged_ids}")

    # sync file hint
    if SYNC.exists():
        try:
            sync = json.loads(SYNC.read_text(encoding="utf-8"))
            if isinstance(sync, dict):
                sync["last_main_id"] = max(merged_ids) if merged_ids else sync.get("last_main_id")
                sync["next_available"] = (max(merged_ids) + 1) if merged_ids else sync.get("next_available")
                sync["updated"] = "2026-08-12"
                SYNC.write_text(json.dumps(sync, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as exc:
            print(f"Aviso sync: {exc}")

    PROC.mkdir(parents=True, exist_ok=True)
    for fname in BATCH_FILES + ["lawfare-thematic-T251-convergencia-stf-master-familia.json"]:
        src = TODO / fname
        if src.is_file():
            dst = PROC / fname
            shutil.move(str(src), str(dst))
            print(f"Arquivado: todo/{fname} -> processados/{fname}")

    print(f"Posts criados: {len(created_posts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
