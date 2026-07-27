"""Converte nav em tabs (show/hide) para scroll-spy estilo Minas Gerais."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

FILES = [
    "dragao-onca-sao-paulo.html",
    "dragao-onca-bahia.html",
    "dragao-onca-parana.html",
    "dragao-onca-rs-es-ranking-nacional.html",
    "dragao-onca-braco-diplomatico.html",
    "dragao-onca-sintese-final-cross-state.html",
]

SCROLL_JS_CORE = """
const links = document.querySelectorAll('.nb');
const sections = document.querySelectorAll('main .sec');
const map = {};
links.forEach(l=>{map[l.dataset.target]=l});
const observer = new IntersectionObserver((entries)=>{
  entries.forEach(entry=>{
    if(entry.isIntersecting){
      links.forEach(l=>l.classList.remove('act'));
      const id = entry.target.id;
      if(map[id]) map[id].classList.add('act');
    }
  });
},{rootMargin:'-30% 0px -60% 0px',threshold:0});
sections.forEach(s=>observer.observe(s));
const gotop = document.getElementById('gotop');
window.addEventListener('scroll',()=>{
  if(gotop) gotop.classList.toggle('show', window.scrollY > 400);
});
if(gotop) gotop.addEventListener('click',()=>{
  window.scrollTo({top:0,behavior:'smooth'});
});
""".strip()

GOTOP_BTN = '<button id="gotop" title="Voltar ao topo" aria-label="Voltar ao topo">↑</button>'

GOTOP_CSS = """
#gotop{position:fixed;right:20px;bottom:20px;z-index:300;width:46px;height:46px;border-radius:50%;background:linear-gradient(135deg,var(--gold,var(--jaguar,#e8b23d)),var(--blue,#4a9eff));color:#0b0f0a;border:none;font-size:18px;font-weight:800;display:flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,0.45);opacity:0;pointer-events:none;transform:translateY(12px);transition:opacity .25s,transform .25s}
#gotop.show{opacity:1;pointer-events:auto;transform:translateY(0)}
#gotop:hover{filter:brightness(1.1)}
""".strip()


def convert(text: str) -> str:
    # html scroll-behavior
    if "scroll-behavior" not in text:
        text = text.replace(
            "*{box-sizing:border-box;margin:0;padding:0}",
            "*{box-sizing:border-box;margin:0;padding:0}\n  html{scroll-behavior:smooth}",
            1,
        )

    # sticky nav
    text = re.sub(
        r"nav\{display:flex;gap:4px;padding:10px 26px;[^}]+\}",
        "nav{display:flex;gap:4px;padding:12px 26px;background:rgba(10,14,18,0.96);border-bottom:2px solid var(--gr-dim,var(--border));box-shadow:0 6px 18px rgba(0,0,0,0.35);overflow-x:auto;flex-wrap:wrap;position:sticky;top:0;z-index:200;backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}",
        text,
        count=1,
    )

    # .nb as link-like
    text = re.sub(
        r"\.nb\{[^}]+\}",
        ".nb{padding:7px 14px;border-radius:6px;border:1px solid var(--border);background:transparent;color:var(--text2);font-family:var(--font);font-size:12px;font-weight:600;cursor:pointer;transition:all .2s;white-space:nowrap;text-decoration:none;display:inline-block}",
        text,
        count=1,
    )
    text = re.sub(
        r"\.nb:hover\{[^}]+\}",
        ".nb:hover{border-color:var(--gold-dim,var(--gr-dim));color:var(--gold,var(--gr2))}",
        text,
        count=1,
    )
    text = re.sub(
        r"\.nb\.act\{[^}]+\}",
        ".nb.act{background:linear-gradient(90deg,rgba(232,196,75,0.2),rgba(62,203,111,0.12));border-color:var(--gold,var(--gr));color:#fff;font-weight:800;box-shadow:0 0 0 1px var(--gold,var(--gr)) inset}",
        text,
        count=1,
    )

    # show all sections
    text = re.sub(
        r"\.sec\{display:none;[^}]*\}\s*\.sec\.act\{display:block\}",
        ".sec{padding:34px 0 12px;border-bottom:1px solid var(--border);scroll-margin-top:70px}\n  .sec:last-of-type{border-bottom:none}",
        text,
        count=1,
    )

    # gotop CSS
    text = re.sub(
        r"\.gotop\{[^}]+\}\s*\.gotop\.vis\{[^}]+\}",
        GOTOP_CSS,
        text,
        count=1,
    )
    if "#gotop{" not in text:
        if ".series-nav{" in text:
            text = text.replace(".series-nav{", GOTOP_CSS + "\n.series-nav{", 1)
        else:
            text = text.replace("</style>", GOTOP_CSS + "\n</style>", 1)

    # buttons → anchors pointing to #sec-xxx (keep existing ids)
    def btn_repl(m: re.Match) -> str:
        sid = m.group(1)
        label = m.group(2)
        # first button may have had act; observer will set act on scroll
        return f'<a class="nb" href="#sec-{sid}" data-target="sec-{sid}">{label}</a>'

    text = re.sub(
        r'<button class="nb(?: act)?" onclick="show\(\'([^\']+)\'\)">([^<]+)</button>',
        btn_repl,
        text,
    )

    # remove act from section divs (all visible now)
    text = re.sub(
        r'(id="sec-[^"]+" class="sec) act(")',
        r"\1\2",
        text,
    )

    # gotop element
    text = re.sub(
        r'<div class="gotop" id="gotop"[^>]*>↑</div>',
        GOTOP_BTN,
        text,
        count=1,
    )
    if 'id="gotop"' not in text:
        text = text.replace("</footer>", "</footer>\n\n" + GOTOP_BTN + "\n", 1)

    COPY_ALL = """
function copyAll(){
  const content = document.querySelector('main').innerText;
  navigator.clipboard.writeText(content).then(() => {
    const btn = document.querySelector('.copy-all-btn');
    btn.textContent = '✓ Copiado!';
    setTimeout(() => { btn.textContent = '⊕ Copiar dossiê completo para IA'; }, 2000);
  });
}
""".strip()

    has_copy = "function copyAll(" in text or "copy-all-btn" in text
    copy_fn = ("\n" + COPY_ALL) if has_copy else ""
    new_script = f"<script>\n{SCROLL_JS_CORE}{copy_fn}\n</script>"

    # replace entire last script before </body> if it has show(
    if "function show(" in text:
        text = re.sub(
            r"<script>[\s\S]*?function show\([\s\S]*?</script>",
            new_script,
            text,
            count=1,
        )
    elif "IntersectionObserver" not in text:
        text = text.replace("</body>", new_script + "\n</body>", 1)

    return text


def main() -> None:
    for name in FILES:
        path = ROOT / name
        original = path.read_text(encoding="utf-8")
        if "function show(" not in original and ".sec{display:none" not in original:
            print(f"SKIP {name}")
            continue
        updated = convert(original)
        issues = []
        if "function show(" in updated:
            issues.append("show() remains")
        if "display:none" in updated and ".sec{display:none" in updated:
            issues.append("sec still hidden")
        if "IntersectionObserver" not in updated:
            issues.append("no observer")
        if 'id="gotop"' not in updated:
            issues.append("no gotop")
        n_links = len(re.findall(r'data-target="sec-', updated))
        n_secs = len(re.findall(r'id="sec-[^"]+" class="sec"', updated))
        path.write_text(updated, encoding="utf-8", newline="\n")
        print(f"{name}: links={n_links} secs={n_secs} issues={issues or ['ok']}")


if __name__ == "__main__":
    main()
