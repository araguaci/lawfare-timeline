#!/usr/bin/env python3
"""Pipeline da série: series-nav nos dossiês → timelines condensadas em timeline/.

Ordem de importância canônica: README 0–18 (hub + T-229…T-246).

Uso:
  python scripts/run_series_pipeline.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent

STEPS = [
    ("updater_series_nav.py", "series-nav 0-18 nos dossies HTML"),
    ("generate_timeline_pages.py", "timeline/timeline-*.html a partir dos dossies"),
    ("patch_timeline_index_hrefs.py", "hrefs do timeline/index.html -> timelines"),
]


def main() -> int:
    print(f"ROOT = {ROOT}")
    for name, label in STEPS:
        path = SCRIPTS / name
        if not path.exists():
            print(f"SKIP {name} (ausente)", file=sys.stderr)
            continue
        print(f"\n==> {name} — {label}")
        r = subprocess.run([sys.executable, str(path)], cwd=ROOT)
        if r.returncode != 0:
            print(f"FAIL {name} exit={r.returncode}", file=sys.stderr)
            return r.returncode
    print("\nPipeline OK - dossies + timeline/ sincronizados (0-18)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
