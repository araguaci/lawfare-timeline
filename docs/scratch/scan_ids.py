#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "_posts"

timeline_ids = []
t_studies = {}

for p in POSTS.rglob("*.md"):
    t = p.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"^timeline_id:\s*(\d+)\s*$", t, re.M):
        timeline_ids.append(int(m.group(1)))
    for m in re.finditer(r'^id_corpus:\s*["\']?(T-\d+)["\']?\s*$', t, re.M):
        tid = int(m.group(1)[2:])
        t_studies[tid] = p.relative_to(ROOT).as_posix()

print("timeline_id max:", max(timeline_ids) if timeline_ids else None)
print("timeline_id count:", len(timeline_ids))
print(">=1570:", sorted(set(x for x in timeline_ids if x >= 1570)))
print("T-studies:", dict(sorted(t_studies.items())))
