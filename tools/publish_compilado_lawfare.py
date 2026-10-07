# -*- coding: utf-8 -*-
"""Publica T-270 em docs/ e gera EPUB."""
from __future__ import annotations

import html
import re
import subprocess
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / "_posts" / "estudos" / "2026-10-06-compilado-lawfare.md"
TPL = (
    ROOT
    / "docs"
    / "posts"
    / "2026-09-13-a-criatura-e-o-consenso-teoria-da-estupidez"
    / "index.html"
)
OUT_HTML_DIR = ROOT / "docs" / "posts" / "2026-10-06-compilado-lawfare"
ESTUDOS = ROOT / "docs" / "estudos" / "index.html"
CAT = ROOT / "docs" / "categories" / "estudos" / "index.html"
FEED = ROOT / "docs" / "feed.xml"
SITEMAP = ROOT / "docs" / "sitemap.xml"
EPUB = ROOT / "artigos" / "T-270-compilado-lawfare.epub"
EPUB_DOCS = ROOT / "docs" / "assets" / "ebook" / "compilado-lawfare.epub"
EPUB_ASSETS = ROOT / "assets" / "ebook" / "compilado-lawfare.epub"

TITLE = "T-270 · Compilado Lawfare — síntese e antologia dos estudos"
DESC = (
    "Livro dos estudos: síntese por eixos (STF, TSE, mineração, PCC, P11, Master) "
    "e texto integral dos 128 dossiês, com links canônicos e fontes."
)
PERM = "/posts/2026-10-06-compilado-lawfare/"
URL = "https://lawfare-timeline.vercel.app" + PERM
IMG = "/assets/img/estudos/padroes_sistemicos_dashboard_hero_xarticle.webp"
TS = "1791333600"
DATE_ISO = "2026-10-06T21:40:00-03:00"
DATE_BR = "06/10/2026"
OLD_TITLE = "T-269 · A criatura e o consenso — teoria da estupidez, Moraes 2021–2026"
OLD_DESC = (
    "O mesmo Moraes: apoio partidário em 2021, recusa editorial em 2026. "
    "Bonhoeffer: o poder precisa da estupidez alheia. A criatura já não cabe no consenso."
)
OLD_PERM = "/posts/2026-09-13-a-criatura-e-o-consenso-teoria-da-estupidez/"
OLD_IMG = "/assets/img/a-criatura-e-o-consenso-teoria-da-estupidez-xarticle-hero.png"


def body_markdown() -> str:
    text = MD.read_text(encoding="utf-8")
    return text.split("---", 2)[2].lstrip("\n")


def kramdown(md: str) -> str:
    tmp_md = ROOT / "_site_tmp_compilado.md"
    tmp_html = ROOT / "_site_tmp_compilado.html"
    tmp_md.write_text(md, encoding="utf-8")
    proc = subprocess.run(
        ["ruby", str(ROOT / "tools" / "_kramdown_try.rb"), str(tmp_md), str(tmp_html)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    return tmp_html.read_text(encoding="utf-8")


def insert_card() -> None:
    card = f"""
    <article class="estudos-card card h-100 position-relative">
      <div class="estudos-card__media">
          <img
            class="estudos-card__img"
            src="{IMG}"
            alt="{html.escape(TITLE)}"
            loading="lazy"
            width="640"
            height="360"
          >
      </div>
      <div class="card-body d-flex flex-column">
        <h2 class="h6 card-title text-body mb-2">{html.escape(TITLE)}</h2>
        <div class="post-meta small text-muted mt-auto">
          <i class="far fa-calendar fa-fw me-1"></i>
<time data-ts="{TS}" data-df="DD/MM/YYYY">{DATE_BR}</time>
        </div>
      </div>
      <a href="{PERM}" class="stretched-link">
        <span class="visually-hidden">{html.escape(TITLE)}</span>
      </a>
    </article>
"""
    html_txt = ESTUDOS.read_text(encoding="utf-8")
    if "compilado-lawfare" in html_txt:
        print("estudos card already present")
        return
    needle = '<div id="estudos-grid" class="estudos-grid">'
    html_txt = html_txt.replace(needle, needle + "\n" + card, 1)
    ESTUDOS.write_text(html_txt, encoding="utf-8")
    print("inserted estudos card")


def insert_category() -> None:
    txt = CAT.read_text(encoding="utf-8")
    if "compilado-lawfare" in txt:
        print("category already present")
        return
    txt = txt.replace(
        '<span class="lead text-muted ps-2">127</span>',
        '<span class="lead text-muted ps-2">128</span>',
        1,
    )
    item = f"""
      <li class="d-flex justify-content-between px-md-3">
        <a href="{PERM}">{html.escape(TITLE)}</a>
        <span class="dash flex-grow-1"></span>
<time class="text-muted small text-nowrap" data-ts="{TS}" data-df="DD/MM/YYYY">{DATE_BR}</time>
      </li>
"""
    txt = txt.replace('<ul class="content ps-0">', '<ul class="content ps-0">\n' + item, 1)
    CAT.write_text(txt, encoding="utf-8")
    print("inserted category item")


def insert_feed() -> None:
    txt = FEED.read_text(encoding="utf-8")
    if "compilado-lawfare" in txt:
        print("feed already present")
        return
    entry = f"""
  <entry>
    <title>{html.escape(TITLE)}</title>
    <link href="{URL}" rel="alternate" type="text/html" title="{html.escape(TITLE)}" />
    <published>{DATE_ISO}</published>
    <updated>{DATE_ISO}</updated>
    <id>{URL}</id>
    <content src="{URL}" />
    <author><name>lawfare</name></author>
    <category term="estudos" />
    <summary>{html.escape(DESC)}</summary>
  </entry>
"""
    txt = txt.replace("<updated>2026-09-13T12:08:42-03:00</updated>", f"<updated>{DATE_ISO}</updated>", 1)
    txt = txt.replace(
        '<entry>\n    <title>T-269',
        entry + '\n  <entry>\n    <title>T-269',
        1,
    )
    FEED.write_text(txt, encoding="utf-8")
    print("inserted feed entry")


def insert_sitemap() -> None:
    txt = SITEMAP.read_text(encoding="utf-8")
    if "compilado-lawfare" in txt:
        print("sitemap already present")
        return
    block = f"""<url>
<loc>{URL}</loc>
<lastmod>{DATE_ISO}</lastmod>
</url>
"""
    txt = txt.replace(
        "<loc>https://lawfare-timeline.vercel.app/posts/2026-09-13-a-criatura-e-o-consenso-teoria-da-estupidez/</loc>\n<lastmod>2026-09-13T00:30:00-03:00</lastmod>\n</url>\n",
        "<loc>https://lawfare-timeline.vercel.app/posts/2026-09-13-a-criatura-e-o-consenso-teoria-da-estupidez/</loc>\n<lastmod>2026-09-13T00:30:00-03:00</lastmod>\n</url>\n"
        + block,
        1,
    )
    SITEMAP.write_text(txt, encoding="utf-8")
    print("inserted sitemap url")


def write_post_html(body_html: str, words: int) -> None:
    mins = max(1, words // 200)
    page = TPL.read_text(encoding="utf-8")
    repls = [
        (OLD_TITLE, TITLE),
        (OLD_DESC, DESC),
        (OLD_PERM, PERM),
        (OLD_IMG, IMG),
        ("2026-09-13T00:30:00-03:00", DATE_ISO),
        ("1789270200", TS),
        ("13/09/2026", DATE_BR),
        ("1427 palavras", f"{words} palavras"),
        ("<em>7 min</em> de leitura", f"<em>{mins} min</em> de leitura"),
    ]
    for a, b in repls:
        page = page.replace(a, b)
    start = page.find('<div class="content">')
    end = page.find('<div class="post-tail-wrapper text-muted">', start)
    if start < 0 or end < 0:
        raise RuntimeError("content markers not found in template")
    # keep the wrapper close before post-tail
    new_content = (
        '<div class="content">\n\n'
        + body_html
        + '\n\n  </div>\n\n  '
    )
    page = page[:start] + new_content + page[end:]
    tags = """
      <div class="post-tags">
        <i class="fa fa-tags fa-fw me-1"></i>
          <a href="/tags/estudo/" class="post-tag no-text-decoration">estudo</a>
          <a href="/tags/lawfare/" class="post-tag no-text-decoration">lawfare</a>
          <a href="/tags/compilado/" class="post-tag no-text-decoration">compilado</a>
          <a href="/tags/stf/" class="post-tag no-text-decoration">stf</a>
          <a href="/tags/justica/" class="post-tag no-text-decoration">justica</a>
          <a href="/tags/censura/" class="post-tag no-text-decoration">censura</a>
          <a href="/tags/pcc/" class="post-tag no-text-decoration">pcc</a>
          <a href="/tags/mineracao/" class="post-tag no-text-decoration">mineracao</a>
          <a href="/tags/corrupcao/" class="post-tag no-text-decoration">corrupcao</a>
      </div>
"""
    page = re.sub(
        r'<div class="post-tags">.*?</div>',
        tags.strip(),
        page,
        count=1,
        flags=re.S,
    )
    OUT_HTML_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_HTML_DIR / "index.html").write_text(page, encoding="utf-8")
    print(f"wrote {OUT_HTML_DIR / 'index.html'} words={words} mins={mins}")


def split_chapters(md: str) -> list[tuple[str, str]]:
    parts = re.split(r"(?m)^# ", md)
    chapters = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        title, _, rest = part.partition("\n")
        title = title.strip()
        if not title:
            continue
        chapters.append((title, rest.strip()))
    if not chapters:
        chapters = [("Compilado Lawfare", md)]
    return chapters


def md_inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    return text


def chapter_to_xhtml(title: str, body: str) -> str:
    blocks = []
    buf: list[str] = []
    in_code = False
    code_buf: list[str] = []
    in_ul = False

    def flush_p() -> None:
        nonlocal buf
        if buf:
            blocks.append("<p>" + md_inline(" ".join(buf)) + "</p>")
            buf = []

    def flush_ul() -> None:
        nonlocal in_ul
        if in_ul:
            blocks.append("</ul>")
            in_ul = False

    for line in body.splitlines():
        if line.startswith("```"):
            flush_p()
            flush_ul()
            if in_code:
                blocks.append(
                    "<pre><code>" + html.escape("\n".join(code_buf)) + "</code></pre>"
                )
                code_buf = []
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_buf.append(line)
            continue
        if line.startswith("|") and "|" in line[1:]:
            flush_p()
            flush_ul()
            blocks.append("<p>" + md_inline(line) + "</p>")
            continue
        if re.match(r"^#{1,6} ", line):
            flush_p()
            flush_ul()
            hashes, _, rest = line.partition(" ")
            level = min(6, len(hashes) + 1)
            blocks.append(f"<h{level}>{md_inline(rest)}</h{level}>")
            continue
        if line.strip() in {"***", "---"}:
            flush_p()
            flush_ul()
            blocks.append("<hr/>")
            continue
        if re.match(r"^[-*] ", line):
            flush_p()
            if not in_ul:
                blocks.append("<ul>")
                in_ul = True
            blocks.append("<li>" + md_inline(line[2:]) + "</li>")
            continue
        if not line.strip():
            flush_p()
            flush_ul()
            continue
        buf.append(line.strip())
    flush_p()
    flush_ul()
    if in_code:
        blocks.append("<pre><code>" + html.escape("\n".join(code_buf)) + "</code></pre>")
    inner = "\n".join(blocks)
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="pt-BR" lang="pt-BR">
<head>
  <meta charset="utf-8"/>
  <title>{escape(title)}</title>
  <link rel="stylesheet" type="text/css" href="styles.css"/>
</head>
<body>
  <h1>{escape(title)}</h1>
  {inner}
</body>
</html>
"""


def write_epub(md: str) -> None:
    chapters = split_chapters(md)
    # Capítulos demais (antologia) — agrupa eixos + síntese, mantém todos.
    manifest = []
    spine = []
    nav_li = []
    files: dict[str, bytes] = {}
    for i, (title, body) in enumerate(chapters, 1):
        name = f"ch{i:03d}.xhtml"
        files[f"OEBPS/{name}"] = chapter_to_xhtml(title, body).encode("utf-8")
        manifest.append(
            f'<item id="ch{i:03d}" href="{name}" media-type="application/xhtml+xml"/>'
        )
        spine.append(f'<itemref idref="ch{i:03d}"/>')
        nav_li.append(f'<li><a href="{name}">{escape(title)}</a></li>')

    nav = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="pt-BR" lang="pt-BR">
<head><meta charset="utf-8"/><title>Sumário</title>
<link rel="stylesheet" type="text/css" href="styles.css"/></head>
<body>
  <nav epub:type="toc" id="toc"><h1>Sumário</h1><ol>
    {''.join(nav_li)}
  </ol></nav>
</body></html>
"""
    files["OEBPS/nav.xhtml"] = nav.encode("utf-8")
    files["OEBPS/styles.css"] = (
        "body{font-family:Georgia,serif;line-height:1.5;margin:1.2em;}"
        "h1,h2,h3{font-family:sans-serif;line-height:1.25;}"
        "a{color:#1a365d;} code,pre{font-family:Consolas,monospace;font-size:.9em;}"
        "pre{background:#f4f4f4;padding:.8em;overflow-x:auto;} hr{border:0;border-top:1px solid #ccc;}"
        "blockquote{border-left:3px solid #999;margin-left:0;padding-left:1em;color:#333;}"
    ).encode("utf-8")
    opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid" version="3.0" xml:lang="pt-BR">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">urn:uuid:lawfare-t270-compilado</dc:identifier>
    <dc:title>{escape(TITLE)}</dc:title>
    <dc:creator>lawfare-timeline</dc:creator>
    <dc:language>pt-BR</dc:language>
    <dc:date>2026-10-06</dc:date>
    <dc:description>{escape(DESC)}</dc:description>
    <meta property="dcterms:modified">2026-10-06T21:40:00Z</meta>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="css" href="styles.css" media-type="text/css"/>
    {''.join(manifest)}
  </manifest>
  <spine>
    <itemref idref="nav"/>
    {''.join(spine)}
  </spine>
</package>
"""
    files["OEBPS/content.opf"] = opf.encode("utf-8")
    files["META-INF/container.xml"] = (
        '<?xml version="1.0"?>\n'
        '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
        "<rootfiles><rootfile full-path=\"OEBPS/content.opf\" "
        'media-type="application/oebps-package+xml"/></rootfiles></container>'
    ).encode("utf-8")

    for dest in (EPUB, EPUB_DOCS, EPUB_ASSETS):
        dest.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(dest, "w") as zf:
            zf.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
            for name, data in files.items():
                zf.writestr(name, data, compress_type=zipfile.ZIP_DEFLATED)
        print(f"wrote {dest} chapters={len(chapters)} bytes={dest.stat().st_size}")


def patch_markdown_epub_link() -> None:
    text = MD.read_text(encoding="utf-8")
    note = (
        "EPUB para leitura offline: "
        "[T-270 Compilado Lawfare](https://lawfare-timeline.vercel.app/assets/ebook/compilado-lawfare.epub)."
    )
    if "compilado-lawfare.epub" in text:
        return
    text = text.replace(
        "Página da categoria: [https://lawfare-timeline.vercel.app/estudos/](https://lawfare-timeline.vercel.app/estudos/).",
        "Página da categoria: [https://lawfare-timeline.vercel.app/estudos/](https://lawfare-timeline.vercel.app/estudos/). "
        + note,
        1,
    )
    MD.write_text(text, encoding="utf-8")


def main() -> None:
    md = body_markdown()
    words = len(re.findall(r"\w+", md, flags=re.U))
    print("converting markdown via kramdown…")
    body_html = kramdown(md)
    write_post_html(body_html, words)
    insert_card()
    insert_category()
    insert_feed()
    insert_sitemap()
    write_epub(md)
    patch_markdown_epub_link()


if __name__ == "__main__":
    main()
