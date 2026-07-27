#!/usr/bin/env python3
"""Sincroniza tags p01–p12/p04b com padrões declarados no corpo dos posts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "_posts"
MAX_TAGS = 10

PAT_INLINE = re.compile(r"\*\*Padr(?:ões|ão):\*\*\s*([^\n·]+)", re.I)
PAT_BULLET = re.compile(r"-\s*\*\*(P\d{2}b?)\*\*", re.I)
PAT_BOLD = re.compile(r"\*\*(P\d{2}b?)\*\*", re.I)
PAT_SECTION = re.compile(
    r"##\s*[^\n]*Padrões Analíticos[^\n]*\n(.*?)(?=\n## |\Z)", re.S | re.I
)
PAT_SECTION_SISTEMICOS = re.compile(
    r"#{2,3}\s*[^\n]*Padrões sistêmicos[^\n]*\n(.*?)(?=\n#{2,3} |\n## |\Z)",
    re.S | re.I,
)
PAT_PATTERN_TAG = re.compile(r"^p\d{2}b?$", re.I)
PAT_LEGACY_TAG = re.compile(r"^padr[aã]o-0?(\d+)(b?)$", re.I)


def normalize_existing_tag(tag: str) -> str:
    t = tag.strip()
    m = PAT_LEGACY_TAG.match(t)
    if m:
        num = m.group(1)
        if len(num) == 1:
            num = num.zfill(2)
        return f"p{num}{m.group(2).lower()}"
    tl = t.lower()
    if re.fullmatch(r"p\d{2}b", tl):
        return tl
    if re.fullmatch(r"p\d{2}-b", tl):
        return tl
    m = re.fullmatch(r"P(\d{2})-B", t)
    if m:
        return f"p{m.group(1)}-b"
    m = re.fullmatch(r"P(\d{2})b", t, re.I)
    if m:
        return f"p{m.group(1)}b"
    m = re.fullmatch(r"P(\d{2})", t, re.I)
    if m:
        return f"p{m.group(1)}"
    if re.fullmatch(r"p\d{2}", tl):
        return tl
    return t


def norm_pat(raw: str) -> str:
    m = re.fullmatch(r"P(\d{2})(b?)", raw.strip(), re.I)
    if not m:
        return raw.lower()
    return f"p{m.group(1)}{m.group(2).lower()}"


def parse_frontmatter(text: str) -> tuple[str | None, str | None, str | None]:
    if not text.startswith("---"):
        return None, None, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, None, text
    return parts[0], parts[1], parts[2]


def parse_tags_line(fm: str) -> tuple[list[str], re.Match[str] | None]:
    m = re.search(r"^tags:\s*(\[[^\]]*\])\s*$", fm, re.M)
    if not m:
        m = re.search(r"^tags:\s*(\[[\s\S]*?\])\s*$", fm, re.M)
    if not m:
        return [], None
    raw = m.group(1)
    tags = [a or b for a, b in re.findall(r'"([^"]+)"|\'([^\']+)\'', raw)]
    return tags, m


def _patterns_from_chunk(chunk: str) -> set[str]:
    found: set[str] = set()
    for p in PAT_BULLET.findall(chunk):
        found.add(norm_pat(p))
    for line in chunk.splitlines():
        for p in PAT_BOLD.findall(line):
            found.add(norm_pat(p))
    return found


def extract_patterns(body: str) -> set[str]:
    found: set[str] = set()

    for line in body.splitlines()[:40]:
        if "**Padrões:**" in line or "**Padrão:**" in line:
            for p in re.findall(r"P\d{2}b?", line, re.I):
                found.add(norm_pat(p))

    m = PAT_INLINE.search(body)
    if m:
        for p in re.findall(r"P\d{2}b?", m.group(1), re.I):
            found.add(norm_pat(p))

    for pat in (PAT_SECTION, PAT_SECTION_SISTEMICOS):
        sec = pat.search(body)
        if sec:
            found |= _patterns_from_chunk(sec.group(1))

    return found


def normalize_tags_in_file(path: Path, dry_run: bool) -> dict | None:
    text = path.read_text(encoding="utf-8")
    _, fm, body = parse_frontmatter(text)
    if fm is None or body is None:
        return None

    existing, m_tags = parse_tags_line(fm)
    if m_tags is None:
        return None

    new_tags: list[str] = []
    seen: set[str] = set()
    fixes: list[tuple[str, str]] = []
    for tag in existing:
        nt = normalize_existing_tag(tag)
        if tag != nt:
            fixes.append((tag, nt))
        if nt in seen:
            continue
        seen.add(nt)
        new_tags.append(nt)

    if not fixes:
        return None

    new_raw = format_tags(new_tags, m_tags.group(1))
    rel = path.relative_to(ROOT)
    change = {"path": rel, "casing_fixes": fixes, "before": existing, "after": new_tags}

    if not dry_run:
        new_fm = fm[: m_tags.start(1)] + new_raw + fm[m_tags.end(1) :]
        path.write_text("---" + new_fm + "---" + body, encoding="utf-8")

    return change


def is_pattern_tag(tag: str) -> bool:
    tl = tag.lower()
    return bool(re.fullmatch(r"p\d{2}b?", tl) or re.fullmatch(r"p\d{2}-b", tl))


def merge_tags(existing: list[str], patterns: set[str]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()
    for tag in existing:
        nt = normalize_existing_tag(tag)
        if nt in seen:
            continue
        seen.add(nt)
        normalized.append(nt)

    pattern_tags = sorted(patterns)
    non_pattern = [t for t in normalized if not is_pattern_tag(t)]
    current_patterns = [t for t in normalized if is_pattern_tag(t)]

    merged_patterns = sorted(set(current_patterns) | patterns)
    result = non_pattern + merged_patterns

    if len(result) > MAX_TAGS:
        # Prioriza todos os padrões declarados; trunca tags temáticas
        keep_non = MAX_TAGS - len(merged_patterns)
        if keep_non < 0:
            result = merged_patterns[:MAX_TAGS]
        else:
            result = non_pattern[:keep_non] + merged_patterns

    return result


def format_tags(tags: list[str], original_raw: str) -> str:
    if "'" in original_raw and '"' not in original_raw:
        inner = ", ".join(f"'{t}'" for t in tags)
    else:
        inner = ", ".join(f'"{t}"' for t in tags)
    return f"[{inner}]"


def process_file(path: Path, dry_run: bool) -> dict | None:
    text = path.read_text(encoding="utf-8")
    _, fm, body = parse_frontmatter(text)
    if fm is None or body is None:
        return None

    patterns = extract_patterns(body)
    if not patterns:
        return None

    existing, m_tags = parse_tags_line(fm)
    if m_tags is None:
        return {"path": path, "error": "no tags line"}

    normalized_existing = [normalize_existing_tag(t) for t in existing]
    current_pattern_tags = {t for t in normalized_existing if is_pattern_tag(t)}
    missing = sorted(patterns - current_pattern_tags)
    casing_fixes = [
        (a, b)
        for a, b in zip(existing, normalized_existing)
        if a != b
    ]

    new_tags = merge_tags(existing, patterns)
    new_raw = format_tags(new_tags, m_tags.group(1))
    old_raw = m_tags.group(1)

    if new_raw == old_raw and not missing and not casing_fixes:
        return None

    rel = path.relative_to(ROOT)
    change = {
        "path": rel,
        "patterns": sorted(patterns),
        "before": existing,
        "after": new_tags,
        "missing": missing,
        "casing_fixes": casing_fixes,
        "truncated": len(new_tags) >= MAX_TAGS and len(set(new_tags)) < len(
            [t for t in existing if not is_pattern_tag(normalize_existing_tag(t))]
        )
        + len(patterns),
    }

    if not dry_run:
        new_fm = fm[: m_tags.start(1)] + new_raw + fm[m_tags.end(1) :]
        path.write_text("---" + new_fm + "---" + body, encoding="utf-8")

    return change


def audit(posts_dir: Path) -> tuple[int, int, list[dict]]:
    gaps: list[dict] = []
    total_with_patterns = 0
    for md in sorted(posts_dir.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        _, fm, body = parse_frontmatter(text)
        if fm is None:
            continue
        patterns = extract_patterns(body)
        if not patterns:
            continue
        total_with_patterns += 1
        existing, _ = parse_tags_line(fm)
        tag_pats = {normalize_existing_tag(t) for t in existing if is_pattern_tag(normalize_existing_tag(t))}
        missing = sorted(patterns - tag_pats)
        if missing:
            gaps.append(
                {
                    "path": str(md.relative_to(ROOT)),
                    "patterns": sorted(patterns),
                    "tags": sorted(tag_pats),
                    "missing": missing,
                }
            )
    return total_with_patterns, len(gaps), gaps


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Só reporta alterações")
    parser.add_argument("--apply", action="store_true", help="Aplica alterações nos arquivos")
    parser.add_argument("--audit-only", action="store_true", help="Só executa auditoria de gaps")
    parser.add_argument("--normalize-casing", action="store_true", help="Normaliza tags P0x legadas")
    args = parser.parse_args()

    if args.normalize_casing:
        dry_run = not args.apply
        changes: list[dict] = []
        for md in sorted(POSTS.rglob("*.md")):
            result = normalize_tags_in_file(md, dry_run=dry_run)
            if result:
                changes.append(result)
        mode = "DRY-RUN" if dry_run else "APPLIED"
        print(f"{mode} normalize: {len(changes)} arquivo(s)")
        for c in changes:
            print(f"{c['path']}: {c['casing_fixes']}")
        return 0

    if args.audit_only or (not args.apply and not args.dry_run):
        total, gap_count, gaps = audit(POSTS)
        print(f"Posts com padrões no corpo: {total}")
        print(f"Posts com tags faltando: {gap_count}")
        for g in gaps:
            print(f"{g['path']}")
            print(f"  body: {g['patterns']}")
            print(f"  tags: {g['tags']}")
            print(f"  MISSING: {g['missing']}")
        return 0 if gap_count == 0 else 1

    dry_run = args.dry_run
    changes: list[dict] = []
    errors: list[dict] = []

    for md in sorted(POSTS.rglob("*.md")):
        result = process_file(md, dry_run=dry_run)
        if result is None:
            continue
        if "error" in result:
            errors.append(result)
        else:
            changes.append(result)

    mode = "DRY-RUN" if dry_run else "APPLIED"
    print(f"{mode}: {len(changes)} arquivo(s) alterado(s)")
    for c in changes:
        print(f"{c['path']}")
        if c.get("missing"):
            print(f"  + missing: {c['missing']}")
        if c.get("casing_fixes"):
            print(f"  ~ casing: {c['casing_fixes']}")
        print(f"  before ({len(c['before'])}): {c['before']}")
        print(f"  after  ({len(c['after'])}): {c['after']}")

    if errors:
        print(f"ERRORS: {len(errors)}")
        for e in errors:
            print(f"  {e['path']}: {e['error']}")

    if not dry_run:
        total, gap_count, _ = audit(POSTS)
        print(f"\nPós-sync: {total} posts com padrões, {gap_count} gaps restantes")

    return 0


if __name__ == "__main__":
    sys.exit(main())
