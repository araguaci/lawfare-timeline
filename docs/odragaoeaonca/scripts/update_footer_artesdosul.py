#!/usr/bin/env python3
"""Crédito @artesdosul + contador de visitas (stats.artesdosul.com) nos rodapés."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FILES = (
    sorted(ROOT.glob("dragao-onca-*.html"))
    + [ROOT / "index.html", ROOT / "odragaoeaonca.html"]
    + sorted((ROOT / "timeline").glob("*.html"))
)

CREDIT_HTML = (
    '  <div class="footdev">Desenvolvido por '
    '<a href="https://www.artesdosul.com/" target="_blank" rel="noopener">@artesdosul</a>'
    "</div>\n"
    '  <div id="ads-counter"></div>'
)

SCRIPTS_BLOCK = """
<script defer src="https://stats.artesdosul.com/v.js"
  data-site="Zjt0Xma8E766TTRDfK0L"
  data-key="pk_a9d707d4d64804ab5736f17d85c8674b"></script>
<script defer src="https://stats.artesdosul.com/c.js"
  data-site="Zjt0Xma8E766TTRDfK0L"
  data-key="pk_a9d707d4d64804ab5736f17d85c8674b"
  data-target="#ads-counter"></script>
""".strip()

CSS = """
.footdev{font-size:11px;color:var(--text2);margin-top:10px;font-family:var(--mono)}
.footdev a{color:var(--jaguar2,var(--gold,var(--gr2,#e8b23d)));text-decoration:none}
.footdev a:hover{color:#fff;text-decoration:underline}
#ads-counter{font-family:var(--mono);font-size:11px;color:var(--text2);margin-top:8px;text-align:center}
""".strip()

FLINK = (
    '    <a href="https://www.artesdosul.com/" target="_blank" rel="noopener">'
    "✦ @artesdosul</a>"
)

OLD_CREDIT = re.compile(
    r'<div class="footdev">\s*Desenvolvido por\s*'
    r'<a href="https://www\.artesdosul\.com/"[^>]*>[^<]*</a>\s*</div>\s*',
    re.I,
)
OLD_INLINE = re.compile(
    r'\s*·\s*Desenvolvido por\s*'
    r'<a href="https://www\.artesdosul\.com/"[^>]*>[^<]*</a>',
    re.I,
)
OLD_COUNTER_SCRIPTS = re.compile(
    r'<script[^>]*stats\.artesdosul\.com/v\.js[\s\S]*?</script>\s*'
    r'(?:<div id="ads-counter"></div>\s*)?'
    r'<script[^>]*stats\.artesdosul\.com/c\.js[\s\S]*?</script>\s*',
    re.I,
)
OLD_ADS_DIV = re.compile(r'\s*<div id="ads-counter"></div>\s*', re.I)
OLD_FLINK = re.compile(
    r'\s*<a href="https://www\.artesdosul\.com/"[^>]*>\s*✦\s*(?:Artes do Sul|@artesdosul)\s*</a>\s*',
    re.I,
)


def ensure_css(text: str) -> str:
    if ".footdev{" in text and "#ads-counter{" in text:
        return text
    if ".footdev{" in text and "#ads-counter{" not in text:
        text = text.replace(
            ".footdev a:hover{color:#fff;text-decoration:underline}",
            ".footdev a:hover{color:#fff;text-decoration:underline}\n"
            "#ads-counter{font-family:var(--mono);font-size:11px;color:var(--text2);"
            "margin-top:8px;text-align:center}",
            1,
        )
        if "#ads-counter{" in text:
            return text
    if ".series-nav{" in text:
        return text.replace(".series-nav{", CSS + "\n.series-nav{", 1)
    if "</style>" in text:
        return text.replace("</style>", CSS + "\n</style>", 1)
    return text


def ensure_credit(text: str) -> str:
    text = OLD_CREDIT.sub("", text)
    text = OLD_INLINE.sub("", text)
    text = OLD_ADS_DIV.sub("\n", text)

    # style A: flinks + fmeta
    if 'class="flinks"' in text:
        if "artesdosul.com" not in text or "✦" not in text:
            text = OLD_FLINK.sub("\n", text)
            text = re.sub(
                r'(<div class="flinks">\s*)',
                r"\1" + FLINK + "\n",
                text,
                count=1,
            )
        elif "Artes do Sul" in text:
            text = text.replace(">✦ Artes do Sul</a>", ">✦ @artesdosul</a>")
        if "</footer>" in text:
            text = text.replace("</footer>", CREDIT_HTML + "\n</footer>", 1)
        return text

    # style B: footcc0 / footnote
    if 'class="footcc0"' in text or 'class="footnote"' in text:
        if "</footer>" in text:
            text = text.replace("</footer>", CREDIT_HTML + "\n</footer>", 1)
        return text

    # style C: .foot (hub/index/timeline) — crédito inline + counter no fim do footer
    if 'class="foot"' in text:
        text = re.sub(
            r'(<div class="foot">)(.*?)(</div>\s*</footer>)',
            lambda m: m.group(1)
            + re.sub(
                r'\s*·\s*Desenvolvido por\s*<a[^>]*>[^<]*</a>',
                "",
                m.group(2),
                flags=re.I,
            )
            + ' · Desenvolvido por <a href="https://www.artesdosul.com/" target="_blank" rel="noopener">@artesdosul</a>'
            + '</div>\n  <div id="ads-counter"></div>\n</footer>',
            text,
            count=1,
            flags=re.DOTALL,
        )
        return text

    if "</footer>" in text:
        text = text.replace("</footer>", CREDIT_HTML + "\n</footer>", 1)
    return text


def ensure_counter(text: str) -> str:
    text = OLD_COUNTER_SCRIPTS.sub("", text)
    if "stats.artesdosul.com/v.js" in text and "stats.artesdosul.com/c.js" in text:
        return text
    if "</body>" in text:
        return text.replace("</body>", SCRIPTS_BLOCK + "\n</body>", 1)
    return text + "\n" + SCRIPTS_BLOCK + "\n"


def main() -> None:
    for path in FILES:
        if not path.exists():
            print(f"SKIP missing {path.relative_to(ROOT)}")
            continue
        original = path.read_text(encoding="utf-8")
        updated = ensure_css(original)
        updated = ensure_credit(updated)
        updated = ensure_counter(updated)
        if updated == original:
            print(f"OK  {path.relative_to(ROOT)}")
        else:
            path.write_text(updated, encoding="utf-8", newline="\n")
            print(f"UPD {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
