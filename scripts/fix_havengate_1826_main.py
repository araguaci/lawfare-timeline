#!/usr/bin/env python3
"""Promove havengate id 1826 de estudo T-1826 para main track."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from sync_todo_current import normalize_main_entry, render_timeline_post, to_lawfare_assunto

batch = json.loads(
    (ROOT / "_data/processados/lawfare-batch-havengate-calixto-1767-1768.json").read_text(
        encoding="utf-8"
    )
)
item = batch[1].copy()
item["category"] = "mecanismo_sistemico"
u = normalize_main_entry(item, "havengate-fix-1826.json")
if not u or u["id_corpus"] != "1826":
    raise SystemExit("falha ao normalizar 1826")

post = ROOT / "_posts" / u["jekyll_categories"][0] / u["jekyll_filename"]
post.parent.mkdir(parents=True, exist_ok=True)
post.write_text(render_timeline_post(u), encoding="utf-8")

lf = json.loads((ROOT / "_data/lawfare.json").read_text(encoding="utf-8"))
assuntos = [a for a in lf["assuntos"] if a.get("id") != 1826]
assuntos.append(to_lawfare_assunto(u, u["jekyll_categories"][0]))
assuntos.sort(key=lambda x: x.get("id") or 0)
lf["assuntos"] = assuntos
lf["total"] = len(assuntos)
(ROOT / "_data/lawfare.json").write_text(json.dumps(lf, ensure_ascii=False, indent=2), encoding="utf-8")

est = ROOT / "_posts/estudos/2026-05-22-aliado-de-eduardo-bolsonaro-tem-casa-de-r-36-milhoes-no-texas-via-mercury-legacy-trust-mes.md"
if est.exists():
    est.unlink()
print("OK", post.relative_to(ROOT))
