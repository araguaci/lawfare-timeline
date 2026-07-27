"""Insere crédito 'Desenvolvido por Artes do Sul' nos rodapés dos artefatos."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

FILES = sorted(ROOT.glob("dragao-onca-*.html")) + [
    ROOT / "index.html",
    ROOT / "odragaoeaonca.html",
]

CREDIT = (
    '  <div class="footdev">Desenvolvido por '
    '<a href="https://www.artesdosul.com/" target="_blank" rel="noopener">Artes do Sul</a>'
    "</div>"
)

CSS = """
.footdev{font-size:11px;color:var(--text2);margin-top:10px;font-family:var(--mono)}
.footdev a{color:var(--jaguar2,var(--gold,var(--gr2,#e8b23d)));text-decoration:none}
.footdev a:hover{color:#fff;text-decoration:underline}
""".strip()

FLINK = (
    '    <a href="https://www.artesdosul.com/" target="_blank" rel="noopener">'
    "✦ Artes do Sul</a>"
)


def ensure_css(text: str) -> str:
    if ".footdev{" in text:
        return text
    if ".series-nav{" in text:
        return text.replace(".series-nav{", CSS + "\n.series-nav{", 1)
    if "</style>" in text:
        return text.replace("</style>", CSS + "\n</style>", 1)
    return text


def ensure_credit(text: str) -> str:
    if "artesdosul.com" in text and "Desenvolvido por" in text:
        return text
    if "artesdosul.com" in text and "footdev" in text:
        return text

    # style A: flinks + fmeta
    if 'class="flinks"' in text:
        if "artesdosul.com" not in text:
            text = re.sub(
                r'(<div class="flinks">\s*)',
                r"\1" + FLINK + "\n",
                text,
                count=1,
            )
        if "Desenvolvido por" not in text:
            text = text.replace("</footer>", CREDIT + "\n</footer>", 1)
        return text

    # style B: footcc0 / footnote
    if 'class="footcc0"' in text or 'class="footnote"' in text:
        if "Desenvolvido por" not in text:
            text = text.replace("</footer>", CREDIT + "\n</footer>", 1)
        return text

    # style C: .foot (hub/index)
    if 'class="foot"' in text:
        if "artesdosul.com" not in text:
            text = re.sub(
                r'(<div class="foot">)(.*?)(</div>\s*</footer>)',
                r'\1\2 · Desenvolvido por <a href="https://www.artesdosul.com/" target="_blank" rel="noopener">Artes do Sul</a>\3',
                text,
                count=1,
                flags=re.DOTALL,
            )
        return text

    # fallback
    if "</footer>" in text and "artesdosul.com" not in text:
        text = text.replace("</footer>", CREDIT + "\n</footer>", 1)
    return text


def main() -> None:
    for path in FILES:
        if not path.exists():
            print(f"SKIP missing {path.name}")
            continue
        original = path.read_text(encoding="utf-8")
        updated = ensure_css(original)
        updated = ensure_credit(updated)
        if updated == original:
            print(f"OK  {path.name} (já tinha ou sem footer)")
        else:
            path.write_text(updated, encoding="utf-8", newline="\n")
            print(f"UPD {path.name}")


if __name__ == "__main__":
    main()
