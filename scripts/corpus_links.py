#!/usr/bin/env python3
"""Índice id_corpus → título/URL e formatação de links para seções Conexões."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "_posts"
LAWFARE = ROOT / "_data" / "lawfare.json"

# Referências compostas (intervalos, clusters) → destino canônico
SPECIAL_REFS: dict[str, dict[str, str]] = {
    "1552_a_1571": {
        "url": "/posts/operacao-rejeito-serra-curral-manuscritos/",
        "title": "Operação Rejeito — cluster 1552–1571 (T-197)",
    },
    "1400-1448": {
        "url": "/posts/farra-do-inss-rede-completa-conafer-careca-do-inss-nucleo-politico-e-o-nucleo-internaciona/",
        "title": "CPI / Farra do INSS — cluster 1400–1448",
    },
}

CONN_LINE = re.compile(
    r"^(-\s*)(?:id_(T\d+|\d+(?:_a_\d+)?|\d+-\d+)|T-(\d+))(.*)$",
    re.MULTILINE,
)
EMOJI_LEAD = re.compile(
    r"^[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0000FE0F\U0000200D\s]+"
)


def slug_from_stem(stem: str) -> str:
    m = re.match(r"^\d{4}-\d{2}-\d{2}-(.+)$", stem)
    return m.group(1) if m else stem


def clean_title(title: str, max_len: int = 72) -> str:
    t = EMOJI_LEAD.sub("", title).strip()
    if len(t) > max_len:
        return t[: max_len - 1].rstrip() + "…"
    return t


def extract_fm_field(text: str, field: str) -> str | None:
    m = re.search(rf'^{field}:\s*"(.*)"\s*$', text, re.M)
    if m:
        return m.group(1).replace('\\"', '"')
    m = re.search(rf"^{field}:\s*'(.*)'\s*$", text, re.M)
    if m:
        return m.group(1)
    m = re.search(rf"^{field}:\s*(\S+)\s*$", text, re.M)
    return m.group(1) if m else None


def post_url_from_stem(stem: str, permalink: str | None) -> str:
    if permalink:
        return permalink if permalink.endswith("/") else permalink + "/"
    return f"/posts/{slug_from_stem(stem)}/"


def build_thematic_index() -> dict[str, dict[str, str]]:
    index: dict[str, dict[str, str]] = {}
    for path in sorted(POSTS.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        cid = extract_fm_field(text, "id_corpus")
        if not cid or not cid.startswith("T-"):
            continue
        title = extract_fm_field(text, "title") or path.stem
        perm = extract_fm_field(text, "permalink")
        index[cid] = {
            "title": title,
            "url": post_url_from_stem(path.stem, perm),
        }
    return index


def build_corpus_index() -> dict[str, dict[str, str]]:
    index: dict[str, dict[str, str]] = {}

    for path in sorted(POSTS.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        cid = extract_fm_field(text, "id_corpus")
        if not cid or cid.startswith("T-"):
            continue
        if not cid.isdigit():
            continue
        title = extract_fm_field(text, "title") or path.stem
        perm = extract_fm_field(text, "permalink")
        index[cid] = {
            "title": title,
            "url": post_url_from_stem(path.stem, perm),
        }

    if LAWFARE.is_file():
        data = json.loads(LAWFARE.read_text(encoding="utf-8"))
        for item in data.get("assuntos") or []:
            cid = str(item.get("id", ""))
            if not cid.isdigit() or cid in index:
                continue
            title = item.get("titulo") or f"Entrada {cid}"
            fa = (item.get("fonte_arquivo") or "").replace("\\", "/")
            if fa:
                stem = Path(fa).stem
                index[cid] = {
                    "title": title,
                    "url": post_url_from_stem(stem, None),
                }

    return index


def link_label(nid: str, meta: dict[str, str], *, thematic: bool = False) -> str:
    title = clean_title(meta["title"])
    if thematic:
        title = re.sub(rf"^{re.escape(nid)}\s*[·\-—]\s*", "", title, flags=re.I).strip()
    return f"{nid} · {title}"


def format_connection(
    raw: str,
    index: dict[str, dict[str, str]],
    thematic: dict[str, dict[str, str]] | None = None,
) -> str:
    """Converte 'id_1772 — nota' ou 'id_T191' em markdown com link."""
    thematic = thematic or {}
    s = raw.strip()

    m_t = re.match(r"^id_T(\d+)$", s, re.I)
    if m_t:
        tid = f"T-{m_t.group(1)}"
        meta = thematic.get(tid)
        if meta:
            return f"[{link_label(tid, meta, thematic=True)}]({meta['url']})"
        return raw

    m_t2 = re.match(r"^T-(\d+)$", s)
    if m_t2:
        tid = f"T-{m_t2.group(1)}"
        meta = thematic.get(tid)
        if meta:
            return f"[{link_label(tid, meta, thematic=True)}]({meta['url']})"
        return raw

    m = re.match(r"^id_(\d+(?:_a_\d+)?|\d+-\d+)(.*)$", s)
    if not m:
        return raw
    ref_key, suffix = m.group(1), m.group(2).rstrip()

    special = SPECIAL_REFS.get(ref_key)
    if special:
        label = special["title"]
        if ref_key[0].isdigit() and "·" not in label and "_" in ref_key:
            label = f"{ref_key.replace('_a_', '–')} · {label}"
        return f"[{label}]({special['url']}){suffix}"

    primary_id = ref_key.split("_a_")[0].split("-")[0]
    meta = index.get(primary_id)
    if not meta:
        return raw
    return f"[{link_label(primary_id, meta)}]({meta['url']}){suffix}"


def fix_conexoes_section(
    text: str,
    index: dict[str, dict[str, str]],
    thematic: dict[str, dict[str, str]] | None = None,
) -> tuple[str, int]:
    """Substitui linhas `- id_NNN` na seção ## Conexoes por links markdown."""
    if thematic is None:
        thematic = build_thematic_index()
    m = re.search(r"^## Conex[^\n]*\n", text, re.M | re.I)
    if not m:
        return text, 0

    start = m.end()
    rest = text[start:]
    end_m = re.search(r"^## ", rest, re.M)
    section_end = start + (end_m.start() if end_m else len(rest))
    section = text[start:section_end]
    count = 0

    def repl(line_m: re.Match) -> str:
        nonlocal count
        prefix = line_m.group(1)
        ref_t = line_m.group(2)
        ref_main = line_m.group(3)
        tail = line_m.group(4)
        if ref_t:
            raw = f"id_{ref_t}{tail}"
        elif ref_main:
            raw = f"T-{ref_main}{tail}"
        else:
            return line_m.group(0)
        formatted = format_connection(raw.strip(), index, thematic)
        if formatted == raw.strip():
            return line_m.group(0)
        count += 1
        return f"{prefix}{formatted}"

    new_section = CONN_LINE.sub(repl, section)
    if new_section == section:
        return text, 0
    return text[:start] + new_section + text[section_end:], count
