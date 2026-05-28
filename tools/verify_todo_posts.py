#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica se registros em _data/todo/*.json têm artigos Jekyll publicados."""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODO = ROOT / "_data" / "todo"
POSTS = ROOT / "_posts"
REPORT = ROOT / "docs" / "relatorio-verificacao-todo-jekyll.md"

STATUS_OK = "publicado"
STATUS_PARTIAL = "parcial"
STATUS_CONFLICT = "conflito_id"
STATUS_MISSING = "ausente"


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")[:90]


def tokenize(text: str) -> set[str]:
    return {t for t in re.split(r"[^\w]+", slugify(text)) if len(t) >= 4}


def title_similarity(a: str, b: str) -> float:
    ta, tb = tokenize(a), tokenize(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    out: dict[str, str] = {}
    for line in block.splitlines():
        m = re.match(r'^(\w[\w-]*):\s*(.+)$', line.strip())
        if m:
            val = m.group(2).strip().strip('"').strip("'")
            out[m.group(1)] = val
    return out


def extract_records(data, source_file: Path) -> list[tuple[Path, dict]]:
    records: list[tuple[Path, dict]] = []

    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and ("id" in item or "id_display" in item):
                records.append((source_file, item))
        return records

    if isinstance(data, dict):
        if "entries" in data:
            for item in data["entries"]:
                records.append((source_file, item))
            return records
        if "assuntos" in data:
            for item in data["assuntos"]:
                records.append((source_file, item))
            return records
        if "id" in data or "id_display" in data:
            records.append((source_file, data))
    return records


def get_record_id(rec: dict):
    if rec.get("id_display"):
        return rec["id_display"]
    return rec.get("id")


def expected_filename(rec: dict) -> str | None:
    jf = rec.get("jekyll_filename")
    if jf:
        return jf if jf.endswith(".md") else f"{jf}.md"
    title = rec.get("title") or rec.get("titulo", "")
    d = (
        rec.get("jekyll_date")
        or rec.get("date")
        or rec.get("data_evento")
        or rec.get("data_registro")
        or ""
    )
    d = str(d)[:10] if d else ""
    if title and d:
        return f"{d}-{slugify(title)}.md"
    return None


def record_slug_hints(rec: dict) -> set[str]:
    hints: set[str] = set()
    for key in ("slug", "jekyll_filename"):
        val = rec.get(key)
        if val:
            hints.add(slugify(str(Path(str(val)).stem)))
    title = rec.get("title") or rec.get("titulo", "")
    if title:
        hints.add(slugify(title))
    exp = expected_filename(rec)
    if exp:
        hints.add(Path(exp).stem)
    return {h for h in hints if len(h) >= 8}


def build_post_index() -> tuple[list[dict], dict[str, list[dict]]]:
    posts: list[dict] = []
    by_id: dict[str, list[dict]] = defaultdict(list)

    for p in POSTS.rglob("*.md"):
        rel = p.relative_to(ROOT).as_posix()
        try:
            text = p.read_text(encoding="utf-8")
        except OSError:
            continue
        fm = parse_frontmatter(text)
        title = fm.get("title", "")
        posts.append(
            {
                "path": rel,
                "filename": p.name,
                "stem": p.stem,
                "title": title,
                "category": fm.get("categories", ""),
                "id_corpus": fm.get("id_corpus", ""),
            }
        )
        if fm.get("id_corpus"):
            by_id[fm["id_corpus"]].append(posts[-1])

    return posts, by_id


def score_post(rec: dict, post: dict) -> tuple[float, str]:
    title = rec.get("title") or rec.get("titulo", "")
    exp = expected_filename(rec)
    hints = record_slug_hints(rec)
    stem = post["stem"]
    reasons: list[str] = []
    score = 0.0

    if exp and post["filename"] == exp:
        return 1.0, "jekyll_filename_exato"

    if exp and stem == Path(exp).stem:
        return 0.98, "filename_stem_exato"

    for hint in hints:
        if hint and (hint in stem or stem in hint):
            score = max(score, 0.92)
            reasons.append("slug_parcial")

    sim = title_similarity(title, post["title"])
    if sim >= 0.35:
        score = max(score, 0.55 + sim)
        reasons.append(f"titulo_sim={sim:.2f}")

    rid = get_record_id(rec)
    if rid is not None and post["id_corpus"] == str(rid):
        if sim >= 0.25 or any(h in stem for h in hints):
            score = max(score, 0.85)
            reasons.append("id_corpus+titulo")
        else:
            score = max(score, 0.15)
            reasons.append("id_corpus_apenas")

    return score, "+".join(reasons) if reasons else "—"


def classify(score: float, method: str) -> str:
    if score >= 0.8:
        return STATUS_OK
    if "id_corpus_apenas" in method and score < 0.5:
        return STATUS_CONFLICT
    if score >= 0.45:
        return STATUS_PARTIAL
    return STATUS_MISSING


def find_best_match(rec: dict, posts: list[dict], by_id: dict[str, list[dict]]) -> dict:
    candidates: list[tuple[float, str, dict]] = []

    for post in posts:
        score, method = score_post(rec, post)
        if score >= 0.15:
            candidates.append((score, method, post))

    rid = get_record_id(rec)
    if rid is not None and str(rid) in by_id:
        for post in by_id[str(rid)]:
            score, method = score_post(rec, post)
            candidates.append((score, method, post))

    if not candidates:
        return {
            "status": STATUS_MISSING,
            "post_path": None,
            "match_method": None,
            "match_score": 0.0,
            "expected": expected_filename(rec),
        }

    candidates.sort(key=lambda x: x[0], reverse=True)
    score, method, post = candidates[0]
    status = classify(score, method)

    return {
        "status": status,
        "post_path": post["path"],
        "match_method": method,
        "match_score": round(score, 3),
        "expected": expected_filename(rec),
    }


def collect_results() -> list[dict]:
    posts, by_id = build_post_index()
    results: list[dict] = []

    for jf in sorted(TODO.glob("*.json")):
        try:
            data = json.loads(jf.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            results.append({"source_file": jf.name, "error": str(exc), "status": STATUS_MISSING})
            continue

        for src, rec in extract_records(data, jf):
            match = find_best_match(rec, posts, by_id)
            rid = get_record_id(rec)
            title = rec.get("title") or rec.get("titulo") or rec.get("slug") or "—"
            results.append(
                {
                    "source_file": jf.name,
                    "id": rid,
                    "title": title,
                    **match,
                }
            )

    return results


def status_icon(status: str) -> str:
    return {
        STATUS_OK: "✅",
        STATUS_PARTIAL: "🟡",
        STATUS_CONFLICT: "⚠️",
        STATUS_MISSING: "❌",
    }.get(status, "❓")


def render_markdown(rows: list[dict]) -> str:
    data_rows = [r for r in rows if "error" not in r]
    errors = [r for r in rows if "error" in r]

    ok = [r for r in data_rows if r["status"] == STATUS_OK]
    partial = [r for r in data_rows if r["status"] == STATUS_PARTIAL]
    conflict = [r for r in data_rows if r["status"] == STATUS_CONFLICT]
    missing = [r for r in data_rows if r["status"] == STATUS_MISSING]

    by_file: dict[str, list[dict]] = defaultdict(list)
    for r in data_rows:
        by_file[r["source_file"]].append(r)

    lines = [
        "# Relatório de verificação — `_data/todo` × artigos Jekyll",
        "",
        f"**Gerado em:** {date.today().isoformat()}  ",
        "**Escopo:** todos os registros em `_data/todo/*.json` cruzados com `_posts/**/*.md`",
        "",
        "## Resumo executivo",
        "",
        "| Métrica | Valor |",
        "| --- | ---: |",
        f"| Arquivos JSON analisados | {len(list(TODO.glob('*.json')))} |",
        f"| Registros extraídos | {len(data_rows)} |",
        f"| ✅ Publicados (post timeline correspondente) | **{len(ok)}** |",
        f"| 🟡 Parciais (dossiê/estudo, sem post 1:1) | **{len(partial)}** |",
        f"| ⚠️ Conflito de ID (`id_corpus` reutilizado) | **{len(conflict)}** |",
        f"| ❌ Ausentes | **{len(missing)}** |",
        "",
        "## Legenda de status",
        "",
        "| Status | Significado |",
        "| --- | --- |",
        "| ✅ `publicado` | Post Jekyll encontrado com correspondência forte (filename, slug ou título) |",
        "| 🟡 `parcial` | Conteúdo coberto por estudo/dossiê agregado, mas sem post individual esperado |",
        "| ⚠️ `conflito_id` | Existe post com o mesmo `id_corpus`, porém conteúdo diferente (colisão de IDs) |",
        "| ❌ `ausente` | Nenhum post correspondente encontrado |",
        "",
        "## Critérios de correspondência",
        "",
        "Prioridade de matching (score composto):",
        "",
        "1. `jekyll_filename` exato",
        "2. stem de arquivo (`YYYY-MM-DD-slug`)",
        "3. slug parcial (ex.: `reforma-tributaria-captura-regulatoria`)",
        "4. similaridade de tokens no título",
        "5. `id_corpus` — só conta como match forte se o título/slug também convergir",
        "",
        "## Resultado por arquivo JSON",
        "",
    ]

    for fname in sorted(by_file):
        items = by_file[fname]
        counts = {s: sum(1 for i in items if i["status"] == s) for s in (STATUS_OK, STATUS_PARTIAL, STATUS_CONFLICT, STATUS_MISSING)}
        lines.extend(
            [
                f"### `{fname}`",
                "",
                f"- Registros: **{len(items)}**",
                f"- ✅ {counts[STATUS_OK]} · 🟡 {counts[STATUS_PARTIAL]} · ⚠️ {counts[STATUS_CONFLICT]} · ❌ {counts[STATUS_MISSING]}",
                "",
                "| ID | Status | Título | Post / esperado | Score | Método |",
                "| ---: | --- | --- | --- | ---: | --- |",
            ]
        )
        for r in sorted(items, key=lambda x: str(x["id"])):
            icon = status_icon(r["status"])
            post = r["post_path"] or r["expected"] or "—"
            title = r["title"].replace("|", "\\|")[:65]
            score = r.get("match_score", 0)
            method = r.get("match_method") or "—"
            lines.append(
                f"| {r['id']} | {icon} {r['status']} | {title} | `{post}` | {score:.2f} | {method} |"
            )
        lines.append("")

    def section(title: str, items: list[dict]) -> None:
        if not items:
            return
        lines.extend([f"## {title}", ""])
        lines.extend(
            [
                "| Arquivo | ID | Status | Post / esperado |",
                "| --- | ---: | --- | --- |",
            ]
        )
        for r in sorted(items, key=lambda x: (x["source_file"], str(x["id"]))):
            post = r["post_path"] or r["expected"] or "—"
            title_txt = r["title"].replace("|", "\\|")[:60]
            lines.append(
                f"| `{r['source_file']}` | {r['id']} | {status_icon(r['status'])} {r['status']} | `{post}` — {title_txt} |"
            )
        lines.append("")

    section("Registros ausentes", missing)
    section("Conflitos de ID detectados", conflict)
    section("Cobertura parcial (estudos/dossiês)", partial)
    section("Registros publicados", ok)

    if errors:
        lines.extend(["## Erros de leitura", ""])
        for e in errors:
            lines.append(f"- `{e['source_file']}`: {e['error']}")
        lines.append("")

    lines.extend(
        [
            "## Observações importantes",
            "",
            "### Colisão IDs 1481–1500",
            "",
            "Os batches `lawfare-1481-1494.json` e `lawfare-1481-1500-merged.json` descrevem eventos **Biomm/Banco Master**, mas os IDs 1481–1500 já estão atribuídos no site a entradas da **linha PCC/Ndrangheta**. Não há posts timeline 1:1 para o batch Biomm; existe cobertura agregada em `_posts/estudos/2026-05-21-biomm-insider-operacao-completa.md`.",
            "",
            "### Colisão IDs 1512–1513",
            "",
            "No batch `lawfare-1512-1524-crise-diplomatica.json`, os IDs 1512–1513 descrevem Ramagem/ICE, mas `id_corpus` 1512–1513 no site apontam para **Biazucci**. Após merge (`scripts/merge_todo_batches.py`), Ramagem/ICE foram renumerados para **1525–1526** — posts publicados em `_posts/crise-diplomatica/`.",
            "",
            "### Entradas temáticas T-189",
            "",
            "- `thematic-189-reforma-tributaria-captura.json` → estudo publicado em `_posts/estudos/2026-05-26-reforma-tributaria-captura-regulatoria.md` (sem `id_corpus` no frontmatter).",
            "- `lawfare-189-direita-permitida.json` → estudo publicado em `_posts/estudos/2026-05-22-direita-permitida-dossie.md`.",
            "",
            "### Batches já mergeados",
            "",
            "- `lawfare-1511-1513-biazucci.json` → 3 posts em `_posts/impunidade/`",
            "- `lawfare-1512-1524-crise-diplomatica.json` → IDs 1514–1524 + 1525–1526 publicados",
            "",
            "---",
            "",
            "*Relatório gerado por `tools/verify_todo_posts.py`. Reexecute após novos merges ou publicações.*",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    rows = collect_results()
    md = render_markdown(rows)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(md, encoding="utf-8")

    data_rows = [r for r in rows if "error" not in r]
    ok = sum(1 for r in data_rows if r["status"] == STATUS_OK)
    missing = sum(1 for r in data_rows if r["status"] == STATUS_MISSING)
    conflict = sum(1 for r in data_rows if r["status"] == STATUS_CONFLICT)
    partial = sum(1 for r in data_rows if r["status"] == STATUS_PARTIAL)

    print(f"Relatório: {REPORT}")
    print(f"Publicados: {ok} | Parciais: {partial} | Conflitos: {conflict} | Ausentes: {missing}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
