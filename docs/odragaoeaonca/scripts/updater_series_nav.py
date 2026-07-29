from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

# Ordem de importância resolvida (README 0–18)
ARTIFACTS = [
    ("index.html", "0 · Hub", "Índice da série", "Mapa completo + tese · 19 artefatos · 12 UFs"),
    ("/dragao-onca-brasil-federal.html", "1 · T-229 · Crítico", "🇧🇷 BR Brasil (Federal)", "Pano de fundo 1993–2026 · Doria–Sinovac"),
    ("/dragao-onca-braco-diplomatico.html", "2 · T-236 · Crítico", "🌐 Braço Diplomático", "WAICO + Serra Verde + alinhamento duplo"),
    ("/dragao-onca-sao-paulo.html", "3 · T-238 · Alto", "🇧🇷 SP São Paulo", "Variante “mercado” — CRRC/COFCO"),
    ("/dragao-onca-goias.html", "4 · T-228 · Alto", "🇧🇷 GO Goiás", "Pivô China→EUA/Japão, terras raras"),
    ("/dragao-onca-minas-gerais.html", "5 · T-232 · Alto", "🇧🇷 MG Minas Gerais", "Sigma + China paralela (CRRC/Midea/BYD)"),
    ("/dragao-onca-bahia.html", "6 · T-237 · Alto", "🇧🇷 BA Bahia", "Caso de controle — padrão falha"),
    ("/dragao-onca-para.html", "7 · T-230 · Alto", "🇧🇷 PA Pará", "Ferrovia + COP30 + 39 mortes"),
    ("/dragao-onca-amazonas.html", "8 · T-231 · Alto", "🇧🇷 AM Amazonas", "Taboca/MPF/PF — mais grave"),
    ("/dragao-onca-parana.html", "9 · T-239 · Médio", "🇧🇷 PR Paraná", "Coordenação estado–união (TCP)"),
    ("/dragao-onca-rio-grande-do-sul.html", "10 · T-240 · Médio", "🇧🇷 RS Rio Grande do Sul", "CEEE-T + cortejo GWM sem captura"),
    ("/dragao-onca-rs-es-ranking-nacional.html", "11 · T-240–242 · Médio", "🇧🇷 RS · ES · Ranking CEBC", "Par de controle + ranking nacional"),
    ("/dragao-onca-sintese.html", "12 · T-233 · Consolidação", "📊 Síntese v1", "KPIs · 12 UFs · soberania do governador"),
    ("/dragao-onca-pl2780.html", "13 · T-235 · Legislativo", "📜 PL 2.780/2024", "FGAM R$ 2 bi · minerais críticos"),
    ("/dragao-onca-braco-juridico.html", "14 · T-234 · Transversal", "⚖️ Braço Jurídico", "STF, marco temporal, ADI 7919"),
    ("/dragao-onca-sintese-final-cross-state.html", "15 · T-243 · Fechamento", "🎯 Síntese final · 12 UFs", "Onde a tese confirma, enfraquece ou falha"),
    ("/dragao-onca-amapa.html", "16 · T-244 · Controle", "🇧🇷 AP Amapá", "Amazonbai + Chevron/CNPC federal"),
    ("/dragao-onca-rj.html", "17 · T-245 · Alto", "🇧🇷 RJ Rio de Janeiro", "Açu/CMPort + Castro/Hikvision"),
    ("/dragao-onca-santa-catarina.html", "18 · T-246 · Distintivo", "🇧🇷 SC Santa Catarina", "JMEV: cortejo duplo, captura zero"),
]

CSS = """
.series-nav{margin:0 auto;max-width:1200px;padding:28px 20px 0;border-top:2px solid var(--border)}
.series-nav-title{font-size:11px;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:var(--text2);margin-bottom:14px;display:flex;align-items:center;gap:10px}
.series-nav-title::before{content:'';flex:1;height:1px;background:var(--border)}
.series-nav-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-bottom:14px}
@media(max-width:720px){.series-nav-grid{grid-template-columns:1fr}}
.series-card{display:block;background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:14px 16px;text-decoration:none;color:inherit;transition:border-color .2s,transform .15s;position:relative;overflow:hidden}
.series-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--dragon,var(--red,#d4342c)),var(--jaguar,var(--gold,#e8b23d)))}
.series-card:hover{border-color:rgba(232,178,61,.45);transform:translateY(-1px)}
.series-card.is-current{border-color:var(--jaguar,var(--gold,#e8b23d));box-shadow:0 0 0 1px rgba(232,178,61,.35) inset;pointer-events:none;opacity:.92}
.series-card-id{font-family:var(--mono);font-size:10px;color:var(--jaguar2,var(--gold2,var(--gold,#e8b23d)));letter-spacing:1px;margin-bottom:4px}
.series-card-chapter{font-size:14px;font-weight:800;color:#fff;margin-bottom:4px;line-height:1.2}
.series-card-desc{font-size:12px;color:var(--text2);line-height:1.55}
.series-hub{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:700;color:var(--jaguar2,var(--gold2,var(--gold,#e8b23d)));text-decoration:none;font-family:var(--mono);margin-bottom:8px}
.series-hub:hover{color:#fff}
""".strip()

FILES = [
    "dragao-onca-brasil-federal.html",
    "dragao-onca-braco-diplomatico.html",
    "dragao-onca-sao-paulo.html",
    "dragao-onca-goias.html",
    "dragao-onca-minas-gerais.html",
    "dragao-onca-bahia.html",
    "dragao-onca-para.html",
    "dragao-onca-amazonas.html",
    "dragao-onca-parana.html",
    "dragao-onca-rio-grande-do-sul.html",
    "dragao-onca-rs-es-ranking-nacional.html",
    "dragao-onca-sintese.html",
    "dragao-onca-pl2780.html",
    "dragao-onca-braco-juridico.html",
    "dragao-onca-sintese-final-cross-state.html",
    "dragao-onca-amapa.html",
    "dragao-onca-rj.html",
    "dragao-onca-santa-catarina.html",
]

SECTION_RE = re.compile(
    r'<section class="series-nav" id="serie">.*?</section>',
    re.DOTALL,
)
CSS_RE = re.compile(
    r'\.series-nav\{.*?\.series-hub:hover\{color:#fff\}',
    re.DOTALL,
)


def build_nav(current_href: str) -> str:
    cards = []
    for href, sid, chapter, desc in ARTIFACTS:
        cls = "series-card is-current" if href == current_href else "series-card"
        cards.append(
            f'    <a class="{cls}" href="{href}">'
            f'<div class="series-card-id">{sid}</div>'
            f'<div class="series-card-chapter">{chapter}</div>'
            f'<div class="series-card-desc">{desc}</div></a>'
        )
    body = "\n".join(cards)
    return (
        '<section class="series-nav" id="serie">\n'
        '  <div class="series-nav-title">Artefatos da Série: O Dragão e a Onça</div>\n'
        '  <div class="series-nav-grid">\n'
        f"{body}\n"
        "  </div>\n"
        '  <a class="series-hub" href="index.html">← Índice da série · O Dragão e a Onça</a>\n'
        "</section>"
    )


def main() -> None:
    results = []
    for name in FILES:
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        current = f"/{name}"
        nav = build_nav(current)
        action = []

        if SECTION_RE.search(text):
            text = SECTION_RE.sub(nav, text, count=1)
            action.append("replaced-nav")
        else:
            # Prefer </main>; fallback: before <footer> or </body> (ex.: RJ sem <main>)
            if "</main>" in text:
                text = text.replace("</main>", nav + "\n\n</main>", 1)
                action.append("inserted-nav")
            elif "<footer" in text:
                text = text.replace("<footer", nav + "\n\n<footer", 1)
                action.append("inserted-nav-before-footer")
            elif "</body>" in text:
                text = text.replace("</body>", nav + "\n</body>", 1)
                action.append("inserted-nav-before-body")
            else:
                raise SystemExit(f"No </main>/<footer>/</body> in {name}")

        if ".series-nav{" not in text:
            if "</style>" not in text:
                raise SystemExit(f"No </style> in {name}")
            text = text.replace("</style>", CSS + "\n</style>", 1)
            action.append("inserted-css")
        elif CSS_RE.search(text):
            text = CSS_RE.sub(CSS, text, count=1)
            action.append("updated-css")
        elif ".series-card{" not in text:
            # CSS parcial (só .series-nav) — completa antes de </style>
            text = text.replace("</style>", CSS + "\n</style>", 1)
            action.append("completed-css")
        else:
            action.append("css-kept")

        path.write_text(text, encoding="utf-8", newline="\n")
        results.append(f"{name}: {', '.join(action)}")

    print("\n".join(results))
    print(f"\nDone: {len(results)} files · {len(ARTIFACTS)} artefatos (0–18)")


if __name__ == "__main__":
    main()
