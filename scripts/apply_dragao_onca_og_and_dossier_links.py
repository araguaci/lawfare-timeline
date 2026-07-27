#!/usr/bin/env python3
"""OG tags em dossiês HTML + links dossiê nos capítulos temáticos T-*.md."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_DIR = ROOT / "odragaoeaonca"
POSTS_DIR = ROOT / "_posts" / "dragao-onca"
BASE_URL = "https://gosurf.site"
IMAGE_BASE = "https://gosurf.site"

# slug HTML (sem .html) → imagem og (gosurf.site)
IMAGE_BY_SLUG = {
    "dragao-onca-amazonas": "dragao-onca-amazonas.webp",
    "dragao-onca-bahia": "dragao-onca-bahia.webp",
    "dragao-onca-braco-diplomatico": "dragao-onca-brasil-federal.webp",
    "dragao-onca-braco-juridico": "dragao-onca-braco-juridico.webp",
    "dragao-onca-brasil-federal": "dragao-onca-brasil-federal.webp",
    "dragao-onca-goias": "dragao-onca-goias.webp",
    "dragao-onca-minas-gerais": "dragao-onca-minas-gerais.webp",
    "dragao-onca-para": "dragao-onca-para.webp",
    "dragao-onca-parana": "dragao-onca-parana.webp",
    "dragao-onca-pl2780": "dragao-onca-pl2780.webp",
    "dragao-onca-rio-grande-do-sul": "dragao-onca-rio-grande-do-sul.webp",
    "dragao-onca-rs-es-ranking-nacional": "dragao-onca-rs-es.webp",
    "dragao-onca-sao-paulo": "dragao-onca-sp.webp",
    "dragao-onca-sintese": "dragao-onca-sintese.webp",
    "dragao-onca-sintese-final-cross-state": "dragao-onca-sintese.webp",
    "dragao-onca-amapa": "dragao-onca-amapa.webp",
    "dragao-onca-rj": "dragao-onca-rj.webp",
}

# og:url pode diferir do nome do arquivo (legado gosurf)
URL_SLUG_OVERRIDE = {
    "dragao-onca-rs-es-ranking-nacional": "dragao-onca-rs-es-ranking",
    "dragao-onca-sintese-final-cross-state": "dragao-onca-sintese-final",
}

# timeline_id → (slug, rótulo link)
THEMATIC_DOSSIER = {
    228: ("dragao-onca-goias", "Capítulo Goiás — pivô China→EUA/Japão"),
    229: ("dragao-onca-brasil-federal", "Capítulo Brasil (Federal)"),
    230: ("dragao-onca-para", "Capítulo Pará"),
    231: ("dragao-onca-amazonas", "Capítulo Amazonas"),
    232: ("dragao-onca-minas-gerais", "Capítulo Minas Gerais"),
    233: ("dragao-onca-sintese", "Síntese comparativa (5 UFs)"),
    234: ("dragao-onca-braco-juridico", "Braço Jurídico"),
    235: ("dragao-onca-pl2780", "PL 2.780/2024 — Minerais Críticos"),
    236: ("dragao-onca-braco-diplomatico", "Braço Diplomático"),
    237: ("dragao-onca-bahia", "Capítulo Bahia"),
    238: ("dragao-onca-sao-paulo", "Capítulo São Paulo"),
    239: ("dragao-onca-parana", "Capítulo Paraná"),
    240: ("dragao-onca-rio-grande-do-sul", "Capítulo Rio Grande do Sul"),
    241: ("dragao-onca-rs-es-ranking-nacional", "Capítulo Espírito Santo (dossiê RS·ES·Ranking)"),
    242: ("dragao-onca-rs-es-ranking-nacional", "Ranking CEBC 2007-2025"),
    243: ("dragao-onca-sintese-final-cross-state", "Síntese final cross-state (T-243)"),
    244: ("dragao-onca-amapa", "Capítulo Amapá — caso controle + petróleo federal"),
    245: ("dragao-onca-rj", "Capítulo Rio de Janeiro — Porto do Açu + governador-negociador"),
}

OG_TWITTER_DESC = {
    "dragao-onca-amazonas": "Taboca, ZFM e contaminação Waimiri-Atroari — timeline verificável.",
    "dragao-onca-braco-diplomatico": "WAICO, Serra Verde e alinhamento assimétrico Pequim–Washington.",
    "dragao-onca-braco-juridico": "Marco temporal, PL da Devastação e ADI 7919 — arco jurídico da série.",
    "dragao-onca-brasil-federal": "Parceria Estratégica e caso Doria–Sinovac — pano de fundo federal.",
    "dragao-onca-goias": "Caiado, Serra Verde e pivô EUA/Japão em terras raras.",
    "dragao-onca-minas-gerais": "Sigma Lithium e capital chinês paralelo: CRRC, Midea, BYD.",
    "dragao-onca-para": "Ferrovia CCCC/Vale, COP30 e custo ambiental no Pará.",
    "dragao-onca-pl2780": "Política Nacional de Minerais Críticos — elo legislativo da série.",
    "dragao-onca-sintese": "Soberania na conta do governador — síntese dos cinco primeiros capítulos.",
    "dragao-onca-rio-grande-do-sul": "RS Day, BYD/GWM e derrota logística — par de controle RS×ES.",
    "dragao-onca-amapa": "Açaí Amazonbai, GACC e CNPC/Chevron na Margem Equatorial — três arquiteturas.",
    "dragao-onca-rj": "CMPort no Porto do Açu, Castro × Hikvision/Dahua — infraestrutura + governador.",
}


def extract_meta(html: str, name: str) -> str:
    m = re.search(rf'<meta name="{name}" content="([^"]*)"', html)
    return m.group(1) if m else ""


def extract_title(html: str) -> str:
    m = re.search(r"<title>([^<]+)</title>", html)
    return m.group(1).strip() if m else ""


def og_title_from_page(title: str) -> str:
    t = re.sub(r"\s*\|\s*lawfare-timeline\s*$", "", title, flags=re.I)
    t = re.sub(r"\s*\|\s*República Sequestrada\s*$", "", t, flags=re.I)
    return t.strip()


def og_description(desc: str, max_len: int = 160) -> str:
    d = desc.strip()
    if len(d) <= max_len:
        return d
    cut = d[: max_len - 1].rsplit(" ", 1)[0]
    return cut + "…"


def build_og_block(slug: str, og_title: str, page_desc: str) -> str:
    url_slug = URL_SLUG_OVERRIDE.get(slug, slug)
    img = IMAGE_BY_SLUG.get(slug, "dragao-onca.webp")
    og_desc = og_description(page_desc, 155)
    tw_desc = OG_TWITTER_DESC.get(slug, og_description(page_desc, 120))
    og_short_title = og_title_from_page(og_title)
    return f"""
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE_URL}/{url_slug}">
<meta property="og:title" content="{og_short_title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:image" content="{IMAGE_BASE}/{img}">
<meta property="og:locale" content="pt_BR">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_short_title}">
<meta name="twitter:description" content="{tw_desc}">
"""


def inject_og_tags(html_path: Path) -> bool:
    html = html_path.read_text(encoding="utf-8")
    if "property=\"og:type\"" in html or "property='og:type'" in html:
        # Normalizar RS se ainda aponta vercel
        if "odragaoeaonca.vercel.app" in html and html_path.stem == "dragao-onca-rio-grande-do-sul":
            slug = html_path.stem
            desc = extract_meta(html, "description")
            title = extract_title(html)
            block = build_og_block(slug, title, desc).strip()
            html = re.sub(
                r"<link rel=\"canonical\"[^>]*>\s*<meta property=\"og:type\"[^>]*>.*?"
                r"<meta name=\"twitter:description\" content=\"[^\"]*\">",
                block,
                html,
                count=1,
                flags=re.S,
            )
            html_path.write_text(html, encoding="utf-8")
            print(f"  normalized OG: {html_path.name}")
            return True
        return False

    slug = html_path.stem
    desc = extract_meta(html, "description")
    title = extract_title(html)
    if not desc or not title:
        print(f"  SKIP (sem title/desc): {html_path.name}")
        return False

    block = build_og_block(slug, title, desc)
    # Inserir após meta description, antes de <style> ou <link
    new_html, n = re.subn(
        r'(<meta name="description" content="[^"]*">)\s*\n',
        r"\1\n" + block,
        html,
        count=1,
    )
    if n == 0:
        print(f"  SKIP (anchor não encontrado): {html_path.name}")
        return False
    html_path.write_text(new_html, encoding="utf-8")
    print(f"  +OG: {html_path.name}")
    return True


def dossier_callout(slug: str, label: str) -> str:
    url_slug = URL_SLUG_OVERRIDE.get(slug, slug)
    url = f"{BASE_URL}/{url_slug}"
    return (
        "\n\n> **Link para dossiê completo:** "
        f"[{label}]({url})\n\n"
        "***\n"
    )


def inject_dossier_link(md_path: Path) -> bool:
    text = md_path.read_text(encoding="utf-8")
    if "Link para dossiê completo:" in text:
        return False
    m = re.search(r"^timeline_id:\s*(\d+)\s*$", text, re.M)
    if not m:
        return False
    tid = int(m.group(1))
    if tid not in THEMATIC_DOSSIER:
        return False
    slug, label = THEMATIC_DOSSIER[tid]
    block = dossier_callout(slug, label)

    # Após bloco inicial (H1 + linha meta **Data:** ... ***)
    pattern = (
        r"(# .+\n\n\*\*Data:\*\*[^\n]*\n\n\*\*\*\n)"
    )
    new_text, n = re.subn(pattern, r"\1" + block + "\n", text, count=1)
    if n == 0:
        # fallback: após primeiro ***
        new_text, n = re.subn(r"(\*\*\*\n)", r"\1" + block + "\n", text, count=1)
    if n == 0:
        print(f"  SKIP md anchor: {md_path.name}")
        return False
    md_path.write_text(new_text, encoding="utf-8")
    print(f"  +link: {md_path.name}")
    return True


def main() -> None:
    print("=== OG tags (odragaoeaonca/*.html) ===")
    og_count = 0
    for path in sorted(HTML_DIR.glob("dragao-onca*.html")):
        if inject_og_tags(path):
            og_count += 1
    print(f"HTML atualizados: {og_count}")

    print("\n=== Links dossiê (2026-07-24-t*.md) ===")
    link_count = 0
    for path in sorted(POSTS_DIR.glob("2026-07-24-t*.md")):
        if inject_dossier_link(path):
            link_count += 1
    print(f"Posts atualizados: {link_count}")


if __name__ == "__main__":
    main()
