#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merge _data/todo batches 1850-1855 + T-252; linkify connections; archive."""
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

BATCH_MAIN = "lawfare-batch-lei15487-anpd-discord-1850-1855.json"
BATCH_THEMATIC = "lawfare-thematic-T252-escalada-anonimizacao-criptografia.json"

IMAGE_BY_CATEGORY = {
    "lawfare": "/assets/solid/weight-scale.svg",
    "escandalos": "/assets/solid/skull.svg",
    "justica": "/assets/solid/hammer.svg",
    "estudos": "/assets/solid/book-open.svg",
    "stf": "/assets/solid/gavel.svg",
    "crise-diplomatica": "/assets/solid/globe.svg",
}


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")[:90]


def yaml_escape(s: str) -> str:
    return s.replace('"', '\\"')


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


def resolve_category(entry: dict) -> str:
    eid = int(entry.get("id") or 0)
    title = (entry.get("title") or "").lower()
    cat = (entry.get("category") or "").lower()
    if eid == 1855 or "chokepoint_judicial" in cat:
        return "justica"
    if eid == 1854 or ("janja" in title and "indefer" not in title and "negado" not in title):
        return "escandalos"
    if eid in (1850, 1851, 1852, 1853) or "anpd" in title or "lei 15.487" in title or "vpn" in title or "ronda virtual" in title:
        return "lawfare"
    if "mecanismo" in cat or "ato_legislativo" in cat:
        return "lawfare"
    return "escandalos"


def build_corpus_index() -> dict[str, dict]:
    """Map id_corpus -> {title, permalink, path} from all posts."""
    idx: dict[str, dict] = {}
    for p in POSTS.rglob("*.md"):
        text = p.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        if end < 0:
            continue
        fm = text[3:end]
        idm = re.search(r'id_corpus:\s*"([^"]+)"', fm) or re.search(
            r"id_corpus:\s*'([^']+)'", fm
        )
        if not idm:
            idm = re.search(r"id_corpus:\s*(\S+)", fm)
        if not idm:
            continue
        cid = idm.group(1).strip().strip("\"'")
        pm = re.search(r'permalink:\s*"([^"]+)"', fm) or re.search(
            r"permalink:\s*(\S+)", fm
        )
        title_m = re.search(r'title:\s*"((?:\\.|[^"\\])*)"', fm)
        permalink = (pm.group(1).strip().strip("\"'") if pm else f"/posts/{p.stem}/")
        if not permalink.endswith("/"):
            permalink += "/"
        title = title_m.group(1).replace('\\"', '"') if title_m else p.stem
        idx[cid] = {"title": title, "permalink": permalink, "path": str(p)}
        # also index bare numeric / T- forms
        if cid.startswith("T-"):
            idx[cid.upper()] = idx[cid]
        elif cid.isdigit():
            idx[f"id_{cid}"] = idx[cid]
    return idx


def short_title(title: str, maxlen: int = 90) -> str:
    title = re.sub(r"^T-\d+\s*[·\-—]\s*", "", title).strip()
    if len(title) <= maxlen:
        return title
    return title[: maxlen - 1] + "…"


def link_for_ref(ref: str, idx: dict[str, dict], pending_titles: dict[str, str] | None = None) -> str:
    """Turn id_1850 / 1850 / T-252 into markdown link."""
    pending_titles = pending_titles or {}
    raw = ref.strip()
    # already a markdown link
    if raw.startswith("[") and "](" in raw:
        return raw

    key = raw
    m = re.match(r"^(?:id_)?(\d+)$", raw, re.I)
    tm = re.match(r"^T-?(\d+)$", raw, re.I)
    if m:
        key = m.group(1)
        label_prefix = f"id_{key}"
    elif tm:
        key = f"T-{tm.group(1)}"
        label_prefix = key
    elif raw.startswith("id_"):
        key = raw[3:]
        label_prefix = raw
    else:
        label_prefix = raw

    meta = idx.get(key) or idx.get(raw) or idx.get(f"id_{key}")
    if meta:
        return f"[{label_prefix} — {short_title(meta['title'])}]({meta['permalink']})"

    # pending (same batch, not yet on disk when first pass)
    if key in pending_titles:
        title = pending_titles[key]
        slug_date_hint = ""  # permalink filled on second pass
        return f"[{label_prefix} — {short_title(title)}]({slug_date_hint})"

    return f"`{raw}`"


def linkify_inline(text: str, idx: dict[str, dict]) -> str:
    """Linkify id_N / T-N outside headings and existing markdown links."""
    if not text:
        return text

    def repl_id(m: re.Match) -> str:
        return link_for_ref(m.group(0), idx)

    lines = text.splitlines(keepends=True)
    out: list[str] = []
    for line in lines:
        # Never rewrite AT / titles / front-matter-like keys
        if re.match(r"^#{1,6}\s", line) or line.startswith("id_corpus:"):
            out.append(line)
            continue
        parts = re.split(r"(\[[^\]]+\]\([^)]+\))", line)
        buf = []
        for part in parts:
            if part.startswith("[") and "](" in part:
                buf.append(part)
                continue
            part = re.sub(r"\bid_\d+\b", repl_id, part)
            part = re.sub(r"\bT-\d+\b", repl_id, part)
            buf.append(part)
        out.append("".join(buf))
    return "".join(out)


def connections_md(conns: list, idx: dict[str, dict]) -> str:
    if not conns:
        return "- _N/A_"
    lines = []
    for c in conns:
        lines.append(f"- {link_for_ref(str(c), idx)}")
    return "\n".join(lines)


def to_assunto(entry: dict, category: str, source_file: str) -> dict:
    eid = int(entry["id"])
    title = (entry.get("title") or "").strip()
    date = str(entry.get("date") or "2026-01-01")[:10]
    summary = (entry.get("summary") or "").strip()
    people = actors_people(entry.get("actors"))
    inst = entry.get("institutions") or []
    tags = [category]
    for p in entry.get("patterns") or []:
        tags.append(str(p).lower() if str(p).startswith("P") else str(p))
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
        "fontes": fontes_urls(entry.get("sources")) or ["N/A"],
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


def render_post(entry: dict, category: str, source_file: str, idx: dict[str, dict]) -> tuple[str, Path, str]:
    eid = int(entry["id"])
    title = (entry.get("title") or "").strip()
    date = str(entry.get("date") or "2026-01-01")[:10]
    summary = (entry.get("summary") or "").strip()
    desc = yaml_escape((summary[:157] + "…") if len(summary) > 157 else summary)
    tags = [category] + [
        str(p).lower() if str(p).upper().startswith("P") else str(p)
        for p in (entry.get("patterns") or [])
    ]
    if entry.get("evidence_status"):
        tags.append(entry["evidence_status"])
    tags = list(dict.fromkeys(tags))[:10]
    slug = slugify(title)
    fname = f"{date}-{slug}.md"
    permalink = f"/posts/{Path(fname).stem}/"
    image = IMAGE_BY_CATEGORY.get(category, "/assets/solid/circle-exclamation.svg")
    people = actors_people(entry.get("actors"))
    inst = entry.get("institutions") or []
    result = linkify_inline(entry.get("result") or "", idx)
    analise = linkify_inline(entry.get("analise") or "", idx)
    lacuna = linkify_inline(entry.get("lacuna_investigativa") or "", idx)
    legal = entry.get("legal_basis") or []
    conns = entry.get("connections") or []
    # enrich with related 1839 for Janja cluster
    if eid == 1854 and "1839" not in [str(c).replace("id_", "") for c in conns]:
        conns = list(conns) + ["id_1839"]

    body = f"""---
title: "{yaml_escape(title)}"
description: "{desc}"
date: {date}T12:00:00.000Z
image:
  path: "{image}"
tags: {json.dumps(tags, ensure_ascii=False)}
categories: {category}
permalink: {permalink}
id_corpus: "{eid}"
corpus_unificado: true
source_data: "{source_file}"
---

- &nbsp;
{{:toc .large-only}}

# {title}

***

## Resumo

{linkify_inline(summary, idx)}

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

{connections_md(conns, idx)}

## Lacunas investigativas

{lacuna or '_N/A_'}

## Fontes verificaveis

{fontes_md(entry.get('sources'))}
"""
    out_dir = POSTS / category
    out_dir.mkdir(parents=True, exist_ok=True)
    return body, out_dir / fname, permalink


def render_thematic(t: dict, idx: dict[str, dict], source_file: str) -> tuple[str, Path]:
    tid = str(t["id"])
    if not tid.startswith("T-"):
        tid = f"T-{tid}"
    topic = (t.get("title") or t.get("topic") or t.get("titulo") or "").strip()
    title = f"{tid} · {topic}" if not topic.startswith("T-") else topic
    date = str(t.get("date") or "2026-08-13")[:10]
    summary = (t.get("summary") or "").strip()
    desc = yaml_escape((summary[:157] + "…") if len(summary) > 157 else summary)
    tags = ["estudos"] + [
        str(p).lower() if str(p).upper().startswith("P") else str(p)
        for p in (t.get("patterns") or [])
    ]
    if t.get("evidence_status"):
        tags.append(t["evidence_status"])
    tags = list(dict.fromkeys(tags))[:10]
    slug = slugify(f"{tid}-{topic}")
    fname = f"{date}-{slug}.md"
    permalink = f"/posts/{Path(fname).stem}/"
    analise = linkify_inline(t.get("analise") or "", idx)
    lacuna = linkify_inline(t.get("lacuna_investigativa") or "", idx)
    inflexao = linkify_inline(t.get("ponto_de_inflexao") or "", idx)
    conns = t.get("connections") or []

    body = f"""---
title: "{yaml_escape(title)}"
description: "{desc}"
date: {date}T12:00:00.000Z
image:
  path: "/assets/solid/book-open.svg"
tags: {json.dumps(tags, ensure_ascii=False)}
categories: estudos
permalink: {permalink}
id_corpus: "{tid}"
corpus_unificado: true
source_data: "{source_file}"
---

- &nbsp;
{{:toc .large-only}}

# {title}

***

## Resumo

{linkify_inline(summary, idx)}

***

## Análise estrutural

{analise or '_N/A_'}

## Ponto de inflexão

{inflexao or '_N/A_'}

## Lacunas investigativas

{lacuna or '_N/A_'}

## Conexões

### Cluster Lei 15.487 / ANPD / Discord (main track)

{connections_md(conns, idx)}

## Notas

Thematic id {tid} — próximo livre após merge: T-253. Main track deste cluster: 1850–1855.
"""
    out_dir = POSTS / "estudos"
    out_dir.mkdir(parents=True, exist_ok=True)
    return body, out_dir / fname


def rewrite_connections_in_posts(paths: list[Path], idx: dict[str, dict]) -> None:
    """Second pass: ensure Conexoes section uses full permalinks after all posts exist."""
    for path in paths:
        text = path.read_text(encoding="utf-8")
        # Fix empty permalink placeholders and bare `id_N` leftovers in Conexoes
        def fix_line(m: re.Match) -> str:
            line = m.group(0)
            # `- [id_1850 — title]()` or `- \`id_1850\``
            bare = re.match(r"^-\s+`((?:id_)?\d+|T-\d+)`\s*$", line)
            if bare:
                return f"- {link_for_ref(bare.group(1), idx)}"
            empty_link = re.match(
                r"^-\s+\[((?:id_)?\d+|T-\d+)\s*[—\-].*?\]\(\)\s*$", line
            )
            if empty_link:
                return f"- {link_for_ref(empty_link.group(1), idx)}"
            # `[id_1850]()` style
            def fill(mm: re.Match) -> str:
                return link_for_ref(mm.group(1), idx)

            line2 = re.sub(
                r"\[((?:id_)?\d+|T-\d+)[^\]]*\]\(\)",
                fill,
                line,
            )
            return line2

        text2 = re.sub(r"^- .+$", fix_line, text, flags=re.M)
        # Also linkify remaining bare id_/T- outside links in body (not front matter)
        if text2.startswith("---"):
            end = text2.find("\n---", 3)
            fm, body = text2[: end + 4], text2[end + 4 :]
            body = linkify_inline(body, idx)
            # avoid double-wrapping already linked tokens: linkify_inline already skips markdown links
            text2 = fm + body
        if text2 != text:
            path.write_text(text2, encoding="utf-8")


def main() -> int:
    main_path = TODO / BATCH_MAIN
    thematic_path = TODO / BATCH_THEMATIC
    if not main_path.is_file():
        print(f"ERRO: falta {main_path}")
        return 1

    entries = json.loads(main_path.read_text(encoding="utf-8"))
    lawfare = json.loads(LAWFARE.read_text(encoding="utf-8"))
    assuntos = lawfare.get("assuntos") or []
    existing = {a.get("id") for a in assuntos}

    idx = build_corpus_index()
    # seed pending titles for intra-batch links before write
    pending_titles = {str(e["id"]): e["title"] for e in entries}
    for eid, title in pending_titles.items():
        # provisional permalink will be set after render
        pass

    created: list[Path] = []
    merged_ids: list[int] = []

    # First pass: compute permalinks for batch
    planned: list[tuple[dict, str, str, Path]] = []
    for entry in entries:
        eid = int(entry["id"])
        if eid in existing:
            print(f"SKIP already in corpus: {eid}")
            continue
        category = resolve_category(entry)
        date = str(entry.get("date") or "2026-01-01")[:10]
        slug = slugify(entry["title"])
        fname = f"{date}-{slug}.md"
        permalink = f"/posts/{Path(fname).stem}/"
        idx[str(eid)] = {
            "title": entry["title"],
            "permalink": permalink,
            "path": str(POSTS / category / fname),
        }
        idx[f"id_{eid}"] = idx[str(eid)]
        planned.append((entry, category, permalink, POSTS / category / fname))

    for entry, category, permalink, out_path in planned:
        eid = int(entry["id"])
        assunto = to_assunto(entry, category, BATCH_MAIN)
        assuntos.append(assunto)
        existing.add(eid)
        merged_ids.append(eid)
        body, out_path2, _ = render_post(entry, category, BATCH_MAIN, idx)
        out_path2.write_text(body, encoding="utf-8")
        created.append(out_path2)
        print(f"OK {eid} -> {category}/{out_path2.name}")

    # Thematic T-252
    if thematic_path.is_file():
        t = json.loads(thematic_path.read_text(encoding="utf-8"))
        tid = str(t.get("id") or "T-252")
        if not tid.startswith("T-"):
            tid = f"T-{tid}"
        date = str(t.get("date") or "2026-08-13")[:10]
        topic = t.get("title") or ""
        slug = slugify(f"{tid}-{topic}")
        fname = f"{date}-{slug}.md"
        permalink = f"/posts/{Path(fname).stem}/"
        idx[tid] = {"title": f"{tid} · {topic}", "permalink": permalink, "path": str(POSTS / "estudos" / fname)}
        body, out_path = render_thematic(t, idx, BATCH_THEMATIC)
        if out_path.exists():
            print(f"SKIP thematic exists: {out_path.name}")
        else:
            out_path.write_text(body, encoding="utf-8")
            created.append(out_path)
            print(f"OK {tid} -> estudos/{out_path.name}")

    # Second pass linkify with complete index
    idx = build_corpus_index()
    rewrite_connections_in_posts(created, idx)

    assuntos.sort(key=lambda a: (a.get("data_evento") or "", a.get("id") or 0))
    lawfare["assuntos"] = assuntos
    if "data_extração" in lawfare:
        lawfare["data_extração"] = "2026-08-13"
    LAWFARE.write_text(json.dumps(lawfare, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"lawfare.json +{len(merged_ids)} IDs: {merged_ids}")

    PROC.mkdir(parents=True, exist_ok=True)
    for fname in (BATCH_MAIN, BATCH_THEMATIC):
        src = TODO / fname
        if src.is_file():
            dst = PROC / fname
            shutil.move(str(src), str(dst))
            print(f"Arquivado: todo/{fname} -> processados/{fname}")

    print(f"Posts criados/atualizados: {len(created)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
