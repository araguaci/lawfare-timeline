#!/usr/bin/env python3
"""
parse_tinyurls.py
Extrai pares (tinyurl, url_original) do TinyURLs.html e filtra
os relacionados ao projeto lawfare-timeline.
"""
import sys, io, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from pathlib import Path

HTML = Path("C:/Users/aragu/OneDrive/\u00c1rea de Trabalho/TinyURLs.html")
html = HTML.read_text(encoding="utf-8", errors="replace")

# Cada item: id="TINYURL" ... alt="ORIGINAL_URL logo"
# Extrair por item via split em li data-v-...
items_raw = re.split(r'<li data-v-[^>]+class="tu-url-stack-item', html)

pairs = []
for chunk in items_raw[1:]:  # pular antes do primeiro item
    tiny = re.search(r'id="(https://tinyurl\.com/[^"]+)"', chunk)
    orig = re.search(r'alt="(https?://[^"]+) logo"', chunk)
    # alternativa: data-test-id="url-stack-item-original-url" href="..."
    orig_b = re.search(r'data-test-id="url-stack-item-original-url"[^>]*href="(https?://[^"]+)"', chunk)
    orig_c = re.search(r'href="(https?://[^"]+)"[^>]*data-test-id="url-stack-item-original-url"', chunk)
    # titulo/label
    title = re.search(r'class="tu-url-stack-item__label[^"]*"[^>]*>([^<]+)<', chunk)
    title_b = re.search(r'data-test-id="url-stack-item-title"[^>]*>([^<]+)<', chunk)

    t = tiny.group(1) if tiny else None
    o = (orig_b and orig_b.group(1)) or (orig_c and orig_c.group(1)) or (orig and orig.group(1)) or None
    lbl = (title_b and title_b.group(1).strip()) or (title and title.group(1).strip()) or ""

    if t:
        pairs.append({"tiny": t, "url": o or "", "label": lbl})

print(f"Total pares extraídos: {len(pairs)}")

# Palavras-chave do projeto
KEYWORDS = [
    "lawfare", "lawfare-timeline", "vercel.app",
    "gosurf.site", "araguaci",
    "claude.ai", "cursor", "jekyll", "chirpy",
    "moraes", "stf", "pcc", "ndrangheta", "lava.jato",
    "archive.org", "wayback",
    "github.com/araguaci",
]

related = []
for p in pairs:
    url_lower = p["url"].lower()
    label_lower = p["label"].lower()
    for kw in KEYWORDS:
        if kw in url_lower or kw in label_lower:
            related.append(p)
            break

print(f"Relacionados ao lawfare-timeline: {len(related)}\n")
for r in related:
    print(f"  {r['tiny']}")
    print(f"    URL: {r['url']}")
    if r["label"]:
        print(f"    Label: {r['label']}")
    print()

# Salvar resultado
out = Path("D:/_deploy/lawfare-timeline/_data/tinyurls_related.json")
out.write_text(json.dumps(related, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Salvo em: {out}")
