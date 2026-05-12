#!/usr/bin/env python3
"""
Extrai posts Markdown (_posts/<categoria>/**/*.md) para JSON alinhado ao schema
descrito em METHODOLOGY.md (seção 4), com campos extras em meta para dashboards.

Uso:
  python tools/extract_md_to_methodology_json.py penduricalhos
  python tools/extract_md_to_methodology_json.py lawfare --output _data/export-lawfare.json
  python tools/extract_md_to_methodology_json.py --all --output _data/export-todos.json

Requer: pip install pyyaml
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    raise SystemExit("Instale PyYAML: pip install pyyaml")

REPO_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = REPO_ROOT / "_posts"

# METHODOLOGY §3 — categorias analíticas (valor do campo categoria no JSON)
CATEGORIAS_ANALITICAS = frozenset(
    {
        "lawfare",
        "perseguicao-institucional",
        "captura-institucional",
        "interferencia-externa",
        "registro-analitico",
    }
)

# Pasta/tags Jekyll → categoria analítica (heurística documentável)
MAPA_CATEGORIA_SITE_PARA_ANALITICA: dict[str, str] = {
    "lawfare": "lawfare",
    "stf": "lawfare",
    "tse": "lawfare",
    "justica": "lawfare",
    "vazatoga": "captura-institucional",
    "penduricalhos": "captura-institucional",
    "extravagancia": "captura-institucional",
    "impunidade": "lawfare",
    "indecoro": "lawfare",
    "operacoes": "perseguicao-institucional",
    "escandalos": "captura-institucional",
    "bancos": "captura-institucional",
    "crise-diplomatica": "interferencia-externa",
    "decano": "registro-analitico",
    "dossie": "registro-analitico",
    "estudos": "registro-analitico",
}


def strip_html(text: str) -> str:
    if not text:
        return ""
    t = re.sub(r"<[^>]+>", " ", text)
    t = unescape(t)
    t = re.sub(r"\{:[^}]*\}", "", t)
    return re.sub(r"\s+", " ", t).strip()


def parse_frontmatter(content: str) -> tuple[dict[str, Any] | None, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return None, content
    try:
        fm = yaml.safe_load(match.group(1))
        body = match.group(2).strip()
        return (fm if isinstance(fm, dict) else {}), body
    except yaml.YAMLError:
        return None, content


def slug_from_filename(filepath: Path) -> str:
    name = filepath.stem
    m = re.match(r"^\d{4}-\d{2}-\d{2}-?(.*)$", name)
    return m.group(1) if m and m.group(1) else name


def data_evento_from_file_or_fm(filepath: Path, fm: dict[str, Any]) -> tuple[str, str]:
    date_val = fm.get("date")
    if date_val:
        if hasattr(date_val, "strftime"):
            de = date_val.strftime("%Y-%m-%d")
            return de, f"{de}T00:00:00.000Z"
        if isinstance(date_val, str):
            try:
                dt = datetime.fromisoformat(date_val.replace("Z", "+00:00"))
                de = dt.strftime("%Y-%m-%d")
                return de, f"{de}T00:00:00.000Z"
            except ValueError:
                if len(date_val) >= 10:
                    de = date_val[:10]
                    return de, f"{de}T00:00:00.000Z"
    m = re.match(r"^(\d{4}-\d{2}-\d{2})", filepath.stem)
    if m:
        de = m.group(1)
        return de, f"{de}T00:00:00.000Z"
    return "", ""


def categoria_site(fm: dict[str, Any], filepath: Path, filtro_cli: str | None) -> str:
    cats = fm.get("categories")
    if isinstance(cats, str) and cats.strip():
        return cats.strip()
    if isinstance(cats, list) and cats:
        return str(cats[0]).strip()
    rel = filepath.relative_to(POSTS_DIR)
    parts = rel.parts
    if len(parts) > 1:
        return parts[0]
    return filtro_cli or "estudos"


def categoria_analitica(site_cat: str) -> str:
    k = site_cat.lower().replace(" ", "-")
    return MAPA_CATEGORIA_SITE_PARA_ANALITICA.get(k, "lawfare")


def infer_relevancia(tags: list[str]) -> str:
    tl = [t.lower() if isinstance(t, str) else "" for t in tags]
    if any("gravidade-alta" in x or "gravidadealta" in x for x in tl):
        return "alta"
    if any("gravidade-baixa" in x or "gravidadebaixa" in x for x in tl):
        return "baixa"
    return "media"


def extract_section(body: str, heading: str) -> str | None:
    """Trecho após ## heading até o próximo ## ou fim."""
    esc = re.escape(heading)
    m = re.search(rf"^##\s+{esc}\s*\n(.+?)(?=^##\s|\Z)", body, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else None


def parse_detalhes_penduricalhos(section: str) -> dict[str, Any]:
    """Parseia lista '- **Campo**: valor' e sublistas indentadas."""
    out: dict[str, Any] = {}
    lines = section.splitlines()
    current_key: str | None = None
    list_keys = frozenset({"envolvidos", "consequências", "consequencias", "categorias", "fontes"})
    key_pattern = re.compile(r"^-\s*\*\*([^*]+)\*\*:\s*(.*)$")

    def append_subitem(key: str, raw_line: str) -> None:
        raw = raw_line.strip()
        link_m = re.search(r"\[([^\]]*)\]\((https?://[^)\s]+)\)", raw)
        if not isinstance(out[key], list):
            out[key] = []
        if link_m:
            out[key].append({"texto": strip_html(link_m.group(1)), "url": link_m.group(2)})
        else:
            out[key].append(strip_html(raw))

    for line in lines:
        m = key_pattern.match(line.rstrip())
        if m:
            label = m.group(1).strip().lower().replace(" ", "_")
            if label == "consequências":
                label = "consequencias"
            rest = m.group(2).strip()
            current_key = label
            if label in list_keys and not rest:
                out[label] = []
            elif rest:
                out[label] = strip_html(rest)
            else:
                out[label] = ""
            continue

        sub = re.match(r"^\s{2,}-\s+(.+)$", line)
        if sub and current_key in list_keys:
            append_subitem(current_key, sub.group(1))

    return out


def normalize_detalhes_keys(d: dict[str, Any]) -> dict[str, Any]:
    key_map = {
        "descrição": "descricao",
        "decisão": "decisao",
        "beneficiado": "beneficiado",
        "departamento": "departamento",
        "consequencias": "consequencias",
        "consequências": "consequencias",
    }
    out: dict[str, Any] = {}
    for k, v in d.items():
        nk = key_map.get(k, k)
        out[nk] = v
    return out


def urls_from_markdown(text: str) -> list[str]:
    seen: set[str] = set()
    urls = []
    for m in re.finditer(r"\((https?://[^)\s]+)\)", text):
        u = m.group(1).rstrip(").,;")
        if u not in seen and "google.com/search" not in u and "wikipedia.org/w/index.php?search" not in u:
            seen.add(u)
            urls.append(u)
    return urls


def extract_fontes_verificaveis(body: str) -> list[str]:
    sec = extract_section(body, "📚 Fontes verificáveis") or extract_section(body, "Fontes verificáveis")
    if sec:
        return urls_from_markdown(sec)
    return []


def extract_markdown_h3_block(body: str, heading_text: str) -> str | None:
    m = re.search(
        rf"^###\s+{re.escape(heading_text)}\s*\n(.+?)(?=^###\s|^##\s|\Z)",
        body,
        re.MULTILINE | re.DOTALL,
    )
    return m.group(1).strip() if m else None


def extract_atores_instituicoes(body: str) -> tuple[list[str], list[str]]:
    atores: list[str] = []
    insts: list[str] = []
    for heading, target in (
        ("Atores", atores),
        ("Instituições", insts),
        ("Instituicoes", insts),
    ):
        sec = extract_markdown_h3_block(body, heading)
        if sec:
            for line in sec.splitlines():
                b = re.match(r"^[-*]\s+(.+)$", line.strip())
                if b:
                    target.append(strip_html(b.group(1)))
    return atores, insts


def build_entrada(
    filepath: Path,
    fm: dict[str, Any],
    body: str,
    idx: int,
    filtro_cli: str | None,
) -> dict[str, Any]:
    titulo = fm.get("title") or ""
    if not isinstance(titulo, str):
        titulo = str(titulo)
    titulo = titulo.strip()

    data_evento, data_iso = data_evento_from_file_or_fm(filepath, fm)
    site_cat = categoria_site(fm, filepath, filtro_cli)
    cat_an = categoria_analitica(site_cat)
    if cat_an not in CATEGORIAS_ANALITICAS:
        cat_an = "lawfare"

    tags = fm.get("tags") or []
    if isinstance(tags, str):
        tags = [tags] if tags else []
    tags = [str(t).strip() for t in tags if t is not None]

    descricao_fm = fm.get("description") or ""
    if isinstance(descricao_fm, str):
        descricao_fm = strip_html(descricao_fm.strip())

    detalhes_sec = extract_section(body, "Detalhes")
    detalhes: dict[str, Any] = {}
    if detalhes_sec:
        detalhes = normalize_detalhes_keys(parse_detalhes_penduricalhos(detalhes_sec))

    corpo_txt = detalhes.get("corpo") or ""
    descricao = corpo_txt or descricao_fm
    resumo_sec = extract_section(body, "🧭 Resumo") or extract_section(body, "Resumo")
    if resumo_sec and len(descricao) < 80:
        first_para = resumo_sec.split("***")[0].strip()
        descricao = strip_html(first_para) or descricao

    fontes: list[str] = []
    raw_fontes = detalhes.get("fontes")
    if isinstance(raw_fontes, list):
        for item in raw_fontes:
            if isinstance(item, dict) and item.get("url"):
                fontes.append(item["url"])
            elif isinstance(item, str) and item.startswith("http"):
                fontes.append(item)
            elif isinstance(item, str):
                fontes.extend(urls_from_markdown(item))
    fontes.extend(extract_fontes_verificaveis(body))
    ref_sec = extract_section(body, "Referências") or extract_section(body, "Fontes")
    if ref_sec:
        fontes.extend(urls_from_markdown(ref_sec))
    seen_f: set[str] = set()
    fontes_unique = []
    for u in fontes:
        if u not in seen_f and "perplexity.ai" not in u:
            seen_f.add(u)
            fontes_unique.append(u)

    pessoas: list[str] = []
    instituicoes: list[str] = []

    juiz = detalhes.get("juiz")
    if juiz and str(juiz).strip() and str(juiz).strip().upper() != "N/A":
        pessoas.append(str(juiz).strip())

    benef = detalhes.get("beneficiado")
    if benef and str(benef).strip() and "N/A" not in str(benef).upper():
        pessoas.append(str(benef).strip())

    envolv = detalhes.get("envolvidos")
    if isinstance(envolv, list):
        for e in envolv:
            if isinstance(e, str):
                if any(x in e for x in ("Tribunal", "STF", "TJ", "MP", "CNJ", "CNMP", "Ministério", "Ministerio")):
                    instituicoes.append(e)
                else:
                    pessoas.append(e)

    dept = detalhes.get("departamento")
    if dept:
        instituicoes.append(str(dept))

    a2, i2 = extract_atores_instituicoes(body)
    pessoas.extend(a2)
    instituicoes.extend(i2)

    def dedupe(lst: list[str]) -> list[str]:
        s: set[str] = set()
        out = []
        for x in lst:
            x = x.strip()
            if x and x.lower() not in s:
                s.add(x.lower())
                out.append(x)
        return out

    pessoas = dedupe(pessoas)
    instituicoes = dedupe(instituicoes)

    meta_extra: dict[str, Any] = {
        "tipo": "evento",
        "subtipo": site_cat,
        "entradas_relacionadas": [],
        "periodo_coberto": "",
        "vetor_correcao_disponivel": True,
        "observacao": "",
        "fonte_arquivo": str(filepath.relative_to(REPO_ROOT)).replace("\\", "/"),
        "slug": slug_from_filename(filepath),
        "categoria_jekyll": site_cat,
        "detalhes_extraidos": detalhes if detalhes else None,
    }

    article_id = fm.get("article_id") or fm.get("id_corpus")
    if article_id is not None:
        meta_extra["article_id"] = article_id

    contraste_const = extract_section(body, "Contraste constitucional")
    contraste_soc = extract_section(body, "Contraste social")
    if contraste_const:
        meta_extra["contraste_constitucional"] = strip_html(contraste_const.split("\n\n")[0][:2000])
    if contraste_soc:
        meta_extra["contraste_social_texto"] = strip_html(contraste_soc.split("\n\n")[0][:2000])

    valor = detalhes.get("valor")
    if valor:
        meta_extra["valor_mencionado"] = str(valor)

    prioridade = 2
    pr = fm.get("prioridade")
    if isinstance(pr, int):
        prioridade = max(1, min(3, pr))
    elif idx <= 10:
        prioridade = 1

    return {
        "id": idx,
        "titulo": titulo,
        "data_evento": data_evento,
        "data_iso": data_iso,
        "categoria": cat_an,
        "tags": tags,
        "descricao": descricao,
        "pessoas_envolvidas": pessoas,
        "instituicoes_envolvidas": instituicoes,
        "fontes": fontes_unique,
        "relevancia": infer_relevancia(tags),
        "prioridade": prioridade,
        "meta": meta_extra,
    }


def iter_markdown_files(categoria: str | None, all_posts: bool) -> list[Path]:
    if all_posts:
        return sorted(POSTS_DIR.rglob("*.md"))
    if not categoria:
        raise SystemExit("Informe CATEGORIA (ex.: penduricalhos) ou use --all.")
    sub = POSTS_DIR / categoria
    if sub.is_dir():
        return sorted(sub.rglob("*.md"))
    hits = [p for p in POSTS_DIR.rglob("*.md") if categoria_site({}, p, categoria) == categoria]
    return sorted(hits)


def main() -> None:
    ap = argparse.ArgumentParser(description="Exporta Markdown (_posts) para JSON (METHODOLOGY.md).")
    ap.add_argument(
        "categoria",
        nargs="?",
        help="Nome da pasta em _posts/ (ex.: penduricalhos, lawfare) ou categoria no front matter.",
    )
    ap.add_argument("--all", action="store_true", help="Processar todos os .md em _posts/.")
    ap.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Arquivo JSON de saída (padrão: _data/export-<categoria>.json ou export-todos.json).",
    )
    args = ap.parse_args()

    paths = iter_markdown_files(args.categoria, args.all)
    filtro = args.categoria if not args.all else None

    entradas: list[dict[str, Any]] = []
    for path in paths:
        try:
            content = path.read_text(encoding="utf-8")
        except OSError as e:
            print(f"[skip] {path}: {e}")
            continue
        fm, body = parse_frontmatter(content)
        if fm is None:
            print(f"[skip] sem front matter: {path}")
            continue
        entradas.append(build_entrada(path, fm, body, len(entradas) + 1, filtro))

    out_path = args.output
    if out_path is None:
        tag = "todos" if args.all else (args.categoria or "todos")
        out_path = REPO_ROOT / "_data" / f"export-{tag}-methodology.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "meta": {
            "descricao": "Exportação gerada por tools/extract_md_to_methodology_json.py conforme METHODOLOGY.md §4",
            "methodology_ref": "METHODOLOGY.md v2.0",
            "exportado_em": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "filtro_categoria_cli": filtro,
            "processar_todos": args.all,
            "total_entradas": len(entradas),
            "raiz_repositorio": str(REPO_ROOT),
        },
        "entradas": entradas,
    }

    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Escrito {out_path} ({len(entradas)} entradas).")


if __name__ == "__main__":
    main()
