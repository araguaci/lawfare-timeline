#!/usr/bin/env python3
"""Leitura de posts Jekyll compartilhada pelos extratores do lawfare.json.

Corrige dois defeitos do parser linha a linha antigo:
  - escalares YAML em bloco (`description: >`, `|`, `>-`, `|-`) eram lidos como o
    texto literal ">";
  - `fontes` só era lida da seção "## Referências"; agora vale qualquer seção de
    fontes/referências e, na falta dela, os links do corpo. Links de busca gerados
    automaticamente (Perplexity, Google, busca da Wikipedia) não contam como fonte.

Uso como módulo:
    from lawfare_post_parser import parse_front_matter, extract_fontes
"""
from __future__ import annotations

import datetime as dt
import re

try:
    import yaml
except ImportError:  # parser de reserva cobre os casos do acervo
    yaml = None

FRONT_RE = re.compile(r"^﻿?---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)(.*)$", re.DOTALL)
BLOCK_MARKERS = {">", "|", ">-", "|-", ">+", "|+"}
SECTION_RE = re.compile(
    r"^(#{2,3})\s*[^\n]*?\b(fontes?|refer[êe]ncias)\b[^\n]*$", re.IGNORECASE | re.MULTILINE
)
HEADING_RE = re.compile(r"^(#{1,3})\s", re.MULTILINE)
URL_RE = re.compile(r"https?://[^\s<>\"'\)\]]+")
NOT_SOURCE = re.compile(
    r"perplexity\.ai|google\.[a-z.]+/search|bing\.com/search|duckduckgo\.com/\?|"
    r"wikipedia\.org/w/index\.php\?search|[?&]search=|x\.com/search|twitter\.com/search|"
    r"lawfare\.site|lawfare-timeline|araguaci\.github\.io|"
    r"\.(?:png|jpe?g|gif|webp|svg)(?:\?|$)",
    re.IGNORECASE,
)


def is_block_marker(value) -> bool:
    return isinstance(value, str) and value.strip() in BLOCK_MARKERS


def _plain(value):
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()
    if isinstance(value, list):
        return [_plain(v) for v in value]
    if isinstance(value, dict):
        return {str(k).lower(): _plain(v) for k, v in value.items()}
    return value


def _fallback_yaml(fm: str) -> dict:
    """Parser mínimo para front matter que o PyYAML rejeita."""
    front: dict = {}
    lines = fm.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1
        if not line.strip() or line.lstrip().startswith("#") or line[:1] in (" ", "\t"):
            continue
        key, sep, val = line.partition(":")
        if not sep:
            continue
        key, val = key.strip().lower(), val.strip()
        if val in BLOCK_MARKERS:
            block = []
            while i < len(lines) and (not lines[i].strip() or lines[i][:1] in (" ", "\t")):
                block.append(lines[i].strip())
                i += 1
            joiner = "\n" if val.startswith("|") else " "
            val = joiner.join(b for b in block if b).strip()
        elif val[:1] in ("'", '"') and val[-1:] == val[:1]:
            val = val[1:-1].replace('\\"', '"')
        elif val.startswith("["):
            val = re.findall(r"['\"]([^'\"]+)['\"]", val) or [
                v.strip() for v in val.strip("[]").split(",") if v.strip()
            ]
        front[key] = val
    return front


def parse_front_matter(content: str) -> tuple[dict, str]:
    """Retorna (front matter com chaves minúsculas e datas em ISO, corpo)."""
    match = FRONT_RE.match(content)
    if not match:
        return {}, content
    fm, body = match.groups()
    front = None
    if yaml is not None:
        try:
            loaded = yaml.safe_load(fm)
            if isinstance(loaded, dict):
                front = _plain(loaded)
        except yaml.YAMLError:
            front = None
    if front is None:
        front = _fallback_yaml(fm)
    for key, val in front.items():
        if isinstance(val, str):
            front[key] = val.strip()
    return front, body


def _urls(text: str) -> list[str]:
    out = []
    for url in URL_RE.findall(text):
        url = url.rstrip(".,;:!?*_")
        if not NOT_SOURCE.search(url) and url not in out:
            out.append(url)
    return out


def extract_fontes(body: str) -> list[str]:
    """Links das seções de fontes/referências; sem elas, os links do corpo."""
    found: list[str] = []
    for m in SECTION_RE.finditer(body):
        level = len(m.group(1))
        start = m.end()
        end = len(body)
        for h in HEADING_RE.finditer(body, start):
            if len(h.group(1)) <= level:
                end = h.start()
                break
        for url in _urls(body[start:end]):
            if url not in found:
                found.append(url)
    return found or _urls(body)
