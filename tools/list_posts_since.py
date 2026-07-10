#!/usr/bin/env python3
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "_posts"
cutoff = date(2026, 5, 26)
items = []
for p in sorted(ROOT.rglob("*.md")):
    m = re.search(r"(\d{4}-\d{2}-\d{2})", p.stem)
    if not m:
        continue
    d = date.fromisoformat(m.group(1))
    if d < cutoff:
        continue
    t = p.read_text(encoding="utf-8", errors="replace")
    fm: dict = {}
    fm_m = re.match(r"^---\n(.*?)\n---", t, re.S)
    if fm_m:
        for line in fm_m.group(1).splitlines():
            if line.startswith("title:"):
                fm["title"] = line.split(":", 1)[1].strip().strip('"')
            elif line.startswith("categories:"):
                fm["cat"] = line.split(":", 1)[1].strip()
            elif line.startswith("id_corpus:"):
                fm["id"] = line.split(":", 1)[1].strip().strip('"')
            elif line.startswith("permalink:"):
                fm["url"] = line.split(":", 1)[1].strip()
            elif line.startswith("description:"):
                fm["desc"] = line.split(":", 1)[1].strip().strip('"')[:200]
    items.append({
        "date": str(d),
        "cat": fm.get("cat", p.parent.name),
        "title": fm.get("title", p.stem),
        "id": fm.get("id", ""),
        "url": fm.get("url", f"/posts/{p.stem}/"),
        "path": str(p.relative_to(ROOT.parent)).replace("\\", "/"),
        "desc": fm.get("desc", "")[:180],
    })
items.sort(key=lambda x: (x["date"], x["cat"], x["title"]))
out = {
    "total": len(items),
    "by_cat": {c: sum(1 for i in items if i["cat"] == c) for c in sorted({i["cat"] for i in items})},
    "items": items,
}
out_path = Path(__file__).resolve().parents[1] / "_data" / "posts-since-2026-05-26.json"
out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {out['total']} posts to {out_path}")
