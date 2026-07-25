#!/usr/bin/env python3
"""Valida front matter YAML dos posts dragao-onca."""

from pathlib import Path

try:
    import yaml
except ImportError:
    raise SystemExit("PyYAML not installed")

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "_posts" / "dragao-onca"

failures = []
for path in sorted(POSTS_DIR.glob("*.md")):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        continue
    parts = text.split("---", 2)
    if len(parts) < 3:
        failures.append((path.name, "missing closing ---"))
        continue
    try:
        yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        failures.append((path.name, str(exc)))

if failures:
    for name, err in failures:
        print(f"FAIL: {name}: {err}")
    raise SystemExit(1)

print(f"OK: {len(list(POSTS_DIR.glob('*.md')))} files")
