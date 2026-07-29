#!/usr/bin/env python3
"""Gera timeline/{slug}.html a partir de dragao-onca-*.html (KPIs + linha do tempo)."""
from __future__ import annotations

import html as html_lib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "timeline"

# Ordem de importância (README 1–18) — hub (0) fica só no timeline/index.html
CHAPTERS = [
    {
        "ordem": 1,
        "slug": "timeline-brasil-federal",
        "src": "dragao-onca-brasil-federal.html",
        "tid": "T-229",
        "flag": "🇧🇷 BR",
        "short": "Brasil (Federal)",
        "anchor": "federal",
        "patterns": "P04b · P05 · P10",
        "badge": "T-229 · Linha do tempo 1993–2026",
        "headline": "Parceria estratégica e o caso Doria–Sinovac",
        "blurb": "Pano de fundo federal que legitima os capítulos estaduais.",
    },
    {
        "ordem": 2,
        "slug": "timeline-braco-diplomatico",
        "src": "dragao-onca-braco-diplomatico.html",
        "tid": "T-236",
        "flag": "🌐",
        "short": "Braço Diplomático",
        "anchor": "diplomatico",
        "patterns": "P05 · P11",
        "badge": "T-236 · WAICO + Serra Verde",
        "headline": "Alinhamento assimétrico duplo",
        "blurb": "Governança de IA com a China e terras raras aos EUA no mesmo semestre.",
    },
    {
        "ordem": 3,
        "slug": "timeline-sao-paulo",
        "src": "dragao-onca-sao-paulo.html",
        "tid": "T-238",
        "flag": "🇧🇷 SP",
        "short": "São Paulo",
        "anchor": "sao-paulo",
        "patterns": "P05 · P11",
        "badge": "T-238 · Variante mercado",
        "headline": "CRRC, COFCO e a variante “mercado”",
        "blurb": "Leilões técnicos e domínio no material rodante — sem diplomacia pessoal.",
    },
    {
        "ordem": 4,
        "slug": "timeline-goias",
        "src": "dragao-onca-goias.html",
        "tid": "T-228",
        "flag": "🇧🇷 GO",
        "short": "Goiás",
        "anchor": "goias",
        "patterns": "P05 · P09 · P10",
        "badge": "T-228 · Capítulo inaugural",
        "headline": "Pivô China → EUA/Japão em terras raras",
        "blurb": "Caiado, Serra Verde, JOGMEC e instrumentalização eleitoral 2026.",
    },
    {
        "ordem": 5,
        "slug": "timeline-minas-gerais",
        "src": "dragao-onca-minas-gerais.html",
        "tid": "T-232",
        "flag": "🇧🇷 MG",
        "short": "Minas Gerais",
        "anchor": "minas-gerais",
        "patterns": "P04b · P05 · P09",
        "badge": "T-232 · Sigma + China paralela",
        "headline": "Sigma Lithium e presença chinesa em paralelo",
        "blurb": "Nasdaq/LG no lítio + CRRC/Midea/BYD — não é “MG sem China”.",
    },
    {
        "ordem": 6,
        "slug": "timeline-bahia",
        "src": "dragao-onca-bahia.html",
        "tid": "T-237",
        "flag": "🇧🇷 BA",
        "short": "Bahia",
        "anchor": "bahia",
        "patterns": "P05",
        "badge": "T-237 · Caso de controle",
        "headline": "Ponte Salvador-Itaparica — TIR↓",
        "blurb": "Jerônimo × Xi; renegociação PPP com retorno chinês reduzido.",
    },
    {
        "ordem": 7,
        "slug": "timeline-para",
        "src": "dragao-onca-para.html",
        "tid": "T-230",
        "flag": "🇧🇷 PA",
        "short": "Pará",
        "anchor": "para",
        "patterns": "P04b · P05 · P09",
        "badge": "T-230 · Ferrovia + COP30",
        "headline": "Corredor mineral e COP30 como vitrine",
        "blurb": "Barbalho, CCCC/Vale, TI Mãe Maria e custo ambiental local.",
    },
    {
        "ordem": 8,
        "slug": "timeline-amazonas",
        "src": "dragao-onca-amazonas.html",
        "tid": "T-231",
        "flag": "🇧🇷 AM",
        "short": "Amazonas",
        "anchor": "amazonas",
        "patterns": "P04b · P05 · P06 · P09",
        "badge": "T-231 · Taboca / China Nonferrous",
        "headline": "Contaminação Waimiri-Atroari e Zona Franca",
        "blurb": "Caso mais grave em escalada FUNAI + MPF + PF.",
    },
    {
        "ordem": 9,
        "slug": "timeline-parana",
        "src": "dragao-onca-parana.html",
        "tid": "T-239",
        "flag": "🇧🇷 PR",
        "short": "Paraná",
        "anchor": "parana",
        "patterns": "P05",
        "badge": "T-239 · TCP Paranaguá",
        "headline": "Coordenação estado–união (CMPort)",
        "blurb": "Acordos APPA e Ministério de Portos com 2 dias de diferença.",
    },
    {
        "ordem": 10,
        "slug": "timeline-rio-grande-do-sul",
        "src": "dragao-onca-rio-grande-do-sul.html",
        "tid": "T-240",
        "flag": "🇧🇷 RS",
        "short": "Rio Grande do Sul",
        "anchor": "rio-grande-do-sul",
        "patterns": "P05",
        "badge": "T-240 · CEEE-T ≠ GWM",
        "headline": "Rede elétrica capturada, fábrica perdida",
        "blurb": "State Grid na transmissão; GWM escolhe Aracruz (ES).",
    },
    {
        "ordem": 11,
        "slug": "timeline-rs-es-ranking",
        "src": "dragao-onca-rs-es-ranking-nacional.html",
        "tid": "T-240–242",
        "flag": "🇧🇷 RS · ES",
        "short": "RS · ES · Ranking",
        "anchor": "rs-es-ranking",
        "patterns": "P05 · P11",
        "badge": "T-240–242 · Par de controle + CEBC",
        "headline": "RS perdeu, ES ganhou — ranking CEBC",
        "blurb": "Mesma disputa GWM, desfechos opostos; US$ 85,5 bi · 355 projetos.",
    },
    {
        "ordem": 12,
        "slug": "timeline-sintese",
        "src": "dragao-onca-sintese.html",
        "tid": "T-233",
        "flag": "📊",
        "short": "Síntese v1",
        "anchor": "sintese",
        "patterns": "P04b · P05",
        "badge": "T-233 · Síntese comparativa",
        "headline": "Soberania na conta do governador",
        "blurb": "KPIs e tese — onde confirma, enfraquece e falha.",
    },
    {
        "ordem": 13,
        "slug": "timeline-pl2780",
        "src": "dragao-onca-pl2780.html",
        "tid": "T-235",
        "flag": "📜",
        "short": "PL 2.780/2024",
        "anchor": "pl2780",
        "patterns": "P05 · P10",
        "badge": "T-235 · Elo legislativo",
        "headline": "FGAM R$ 2 bi — minerais críticos",
        "blurb": "Streaming, INESC/Serra Verde e assimetria investidor × comunidade.",
    },
    {
        "ordem": 14,
        "slug": "timeline-braco-juridico",
        "src": "dragao-onca-braco-juridico.html",
        "tid": "T-234",
        "flag": "⚖️",
        "short": "Braço Jurídico",
        "anchor": "braco-juridico",
        "patterns": "P01 · P04b · P09",
        "badge": "T-234 · Arquitetura legal",
        "headline": "Marco temporal, PL da Devastação e ADI 7919",
        "blurb": "Arquitetura que viabiliza os capítulos estaduais.",
    },
    {
        "ordem": 15,
        "slug": "timeline-sintese-final",
        "src": "dragao-onca-sintese-final-cross-state.html",
        "tid": "T-243",
        "flag": "🎯",
        "short": "Síntese final",
        "anchor": "sintese-final",
        "patterns": "P04b · P05 · P11",
        "badge": "T-243 · Tipologia final",
        "headline": "Confirma / enfraquece / contraria",
        "blurb": "Fechamento tipológico · 10 mecanismos · 12 estados.",
    },
    {
        "ordem": 16,
        "slug": "timeline-amapa",
        "src": "dragao-onca-amapa.html",
        "tid": "T-244",
        "flag": "🇧🇷 AP",
        "short": "Amapá",
        "anchor": "amapa",
        "patterns": "P05 · controle",
        "badge": "T-244 · Controle + federal",
        "headline": "Amazonbai + Chevron/CNPC",
        "blurb": "Açaí cooperativista e petróleo offshore sem governador na mesa.",
    },
    {
        "ordem": 17,
        "slug": "timeline-rj",
        "src": "dragao-onca-rj.html",
        "tid": "T-245",
        "flag": "🇧🇷 RJ",
        "short": "Rio de Janeiro",
        "anchor": "rio-de-janeiro",
        "patterns": "P05 · P09 · P10",
        "badge": "T-245 · Açu + vigilância",
        "headline": "Porto do Açu + Castro × Hikvision",
        "blurb": "CMPort US$714 mi e vigilância sob sanção — IDs 1760–1762.",
    },
    {
        "ordem": 18,
        "slug": "timeline-santa-catarina",
        "src": "dragao-onca-santa-catarina.html",
        "tid": "T-246",
        "flag": "🇧🇷 SC",
        "short": "Santa Catarina",
        "anchor": "santa-catarina",
        "patterns": "P05 · P10 · controle",
        "badge": "T-246 · Cortejo duplo sem captura",
        "headline": "JMEV: Alesc × ES, fábrica zero",
        "blurb": "Cortejo legislativo + ferrovias exploratórias — nem SC nem ES confirmam planta até mar/2026.",
    },
]

CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
:root{
  --bg:#080c10;--bg2:#0f151b;--bg3:#161e26;
  --dragon:#d4342c;--dragon2:#ff6b5f;--dragon-dim:#5c1512;
  --jaguar:#e8b23d;--jaguar2:#ffd270;--jaguar-dim:#6b4e12;
  --gr:#3ecb6f;--blue:#4a9eff;--purple:#b07aff;--teal:#2ecfb0;
  --border:rgba(255,255,255,0.07);--text:#e8edf0;--text2:#8a99a8;
  --font:'Syne',sans-serif;--mono:'JetBrains Mono',monospace;
}
body{background:var(--bg);color:var(--text);font-family:var(--font);min-height:100vh}
header{padding:26px 30px 18px;border-bottom:2px solid var(--jaguar-dim);background:linear-gradient(135deg,#080c10 0%,#1a1408 55%,#080c10 100%)}
.hbadge{display:inline-flex;background:rgba(232,178,61,.14);border:1px solid var(--jaguar);border-radius:4px;padding:4px 12px;font-size:11px;font-weight:700;letter-spacing:2px;color:var(--jaguar2);text-transform:uppercase;margin-bottom:10px}
header h1{font-size:26px;font-weight:800;color:#fff;line-height:1.15}
header h1 span{color:var(--jaguar2)}
header h1 em{font-style:normal;color:var(--dragon2)}
.hmeta{display:flex;gap:18px;margin-top:10px;flex-wrap:wrap;font-size:12px;color:var(--text2);font-family:var(--mono)}
.hmeta b{color:var(--jaguar2)}
.dossie-link{display:inline-flex;margin-top:12px;font-family:var(--mono);font-size:12px;font-weight:700;color:var(--jaguar2);text-decoration:none}
.dossie-link:hover{color:#fff}
main{padding:0 20px 32px;max-width:1200px;margin:0 auto}
.sec{padding:30px 0 10px;border-bottom:1px solid var(--border)}
.sec-title{font-size:20px;font-weight:800;color:#fff;margin-bottom:4px}
.sec-sub{font-size:12px;color:var(--text2);font-family:var(--mono);margin-bottom:16px}
.kgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;padding:12px 0}
@media(max-width:720px){.kgrid{grid-template-columns:1fr}}
.kcard{background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:14px}
.klabel{font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--text2);margin-bottom:5px}
.kval{font-size:18px;font-weight:800;color:var(--jaguar2);line-height:1.2}
.ksub{font-size:11px;color:var(--text2);margin-top:4px;font-family:var(--mono)}
.kd .kval{color:var(--dragon2)}.kp .kval{color:var(--purple)}.kt .kval{color:var(--teal)}
.panel{background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:18px 20px;margin-bottom:12px}
p.body{font-size:14px;color:var(--text2);line-height:1.75;margin-bottom:10px}
.tli{display:flex;gap:12px;padding:11px 0;border-bottom:1px solid var(--border)}
.tli:last-child{border-bottom:none}
.tld{font-family:var(--mono);font-size:11px;color:var(--jaguar2);min-width:90px;font-weight:600;flex-shrink:0}
.tltitle{font-size:14px;font-weight:700;margin-bottom:3px;color:#fff}
.tldesc{font-size:12px;color:var(--text2);line-height:1.6}
.tag{display:inline-block;padding:2px 7px;border-radius:4px;font-size:10px;font-weight:600;margin-left:6px;font-family:var(--mono)}
.tg{background:rgba(62,203,111,.1);color:#78f5a8;border:1px solid rgba(62,203,111,.2)}
.tgo{background:rgba(232,178,61,.12);color:var(--jaguar2);border:1px solid rgba(232,178,61,.25)}
footer{padding:0 0 40px;border-top:2px solid var(--jaguar-dim)}
.footcc0{text-align:center;padding:20px;font-family:var(--mono);font-size:11px;color:var(--text2)}
.footcc0 b{color:var(--jaguar2)}
.footcc0 a{color:var(--jaguar2);text-decoration:none}
.series-nav{margin:0 auto;max-width:1200px;padding:28px 20px 0;border-top:2px solid var(--border)}
.series-nav-title{font-size:11px;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:var(--text2);margin-bottom:14px;display:flex;align-items:center;gap:10px}
.series-nav-title::before{content:'';flex:1;height:1px;background:var(--border)}
.series-nav-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-bottom:14px}
@media(max-width:720px){.series-nav-grid{grid-template-columns:1fr}}
.series-card{display:block;background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:14px 16px;text-decoration:none;color:inherit;transition:border-color .2s,transform .15s;position:relative;overflow:hidden}
.series-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--dragon),var(--jaguar))}
.series-card:hover{border-color:rgba(232,178,61,.45);transform:translateY(-1px)}
.series-card.is-current{border-color:var(--jaguar);box-shadow:0 0 0 1px rgba(232,178,61,.35) inset;pointer-events:none;opacity:.92}
.series-card-id{font-family:var(--mono);font-size:10px;color:var(--jaguar2);letter-spacing:1px;margin-bottom:4px}
.series-card-chapter{font-size:14px;font-weight:800;color:#fff;margin-bottom:4px;line-height:1.2}
.series-card-desc{font-size:12px;color:var(--text2);line-height:1.55}
.series-hub{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:700;color:var(--jaguar2);text-decoration:none;font-family:var(--mono);margin-bottom:8px}
.series-hub:hover{color:#fff}
""".strip()


def strip_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)
    return html_lib.unescape(s).strip()


def extract_kpis(src: str, limit: int = 3) -> list[tuple[str, str, str]]:
    out = []
    for m in re.finditer(
        r'<div class="kcard[^"]*">\s*<div class="klabel">(.*?)</div>\s*<div class="kval">(.*?)</div>(?:\s*<div class="ksub">(.*?)</div>)?',
        src,
        re.S,
    ):
        label, val, sub = strip_tags(m.group(1)), strip_tags(m.group(2)), strip_tags(m.group(3) or "")
        if label and val:
            out.append((label, val, sub))
        if len(out) >= limit:
            break
    return out


def extract_tlis(src: str) -> list[tuple[str, str, str]]:
    items = []
    for m in re.finditer(
        r'<div class="tli">\s*<div class="tld">(.*?)</div>\s*<div>\s*<div class="tltitle">(.*?)</div>\s*<div class="tldesc">(.*?)</div>',
        src,
        re.S,
    ):
        date = strip_tags(m.group(1))
        title = strip_tags(re.sub(r'<span class="tag[^"]*">.*?</span>', "", m.group(2)))
        desc = strip_tags(m.group(3))
        if title:
            items.append((date, title, desc))
    return items


def extract_tlitems(src: str) -> list[tuple[str, str, str]]:
    """Formato .tlitem / .tldate / .tltitle (ex.: Santa Catarina)."""
    items = []
    for m in re.finditer(
        r'<div class="tlitem">\s*<span class="tldate">(.*?)</span>(?:<span class="tlid">.*?</span>)?\s*'
        r'<div class="tltitle">(.*?)</div>\s*<div class="tldesc">(.*?)</div>',
        src,
        re.S,
    ):
        date = strip_tags(m.group(1))
        title = strip_tags(m.group(2))
        desc = strip_tags(m.group(3))
        if title:
            items.append((date, title, desc))
    return items


def extract_timeline_items(src: str) -> list[tuple[str, str, str]]:
    """RJ-style .timeline-item / .timeline-date / .timeline-content."""
    items = []
    for m in re.finditer(
        r'<div class="timeline-item">\s*<div class="timeline-date">(.*?)</div>\s*<div class="timeline-content">(.*?)</div>\s*</div>',
        src,
        re.S,
    ):
        date = strip_tags(m.group(1))
        raw = re.sub(r'<span class="src">.*?</span>', "", m.group(2), flags=re.S)
        text = strip_tags(raw)
        if not text:
            continue
        # First sentence as title if long
        if len(text) > 110:
            cut = text.find(". ")
            if 40 < cut < 160:
                title, desc = text[: cut + 1], text[cut + 2 :]
            else:
                title, desc = text[:100] + "…", text
        else:
            title, desc = text, ""
        items.append((date, title, desc[:420] + ("…" if len(desc) > 420 else "")))
    return items


def extract_events(src: str) -> list[tuple[str, str, str]]:
    """Fallback: evcard → (id/date, title, desc)."""
    items = []
    for m in re.finditer(
        r'class="evid"[^>]*>(.*?)</div>\s*<div class="evtitle"[^>]*>(.*?)</div>.*?class="evdesc"[^>]*>(.*?)</div>',
        src,
        re.S,
    ):
        evid = strip_tags(m.group(1))
        title = strip_tags(m.group(2))
        desc = strip_tags(m.group(3))
        if title:
            items.append((evid, title, desc[:420] + ("…" if len(desc) > 420 else "")))
    return items


def extract_findings(src: str, limit: int = 12) -> list[tuple[str, str, str]]:
    """Síntese-style: alertas / mecanismos como 'eventos' analíticos."""
    items = []
    for m in re.finditer(
        r'<div class="mech-title">(.*?)</div>\s*<div class="mech-cases">(.*?)</div>\s*<div class="mech-note">(.*?)</div>',
        src,
        re.S,
    ):
        title = strip_tags(m.group(1))
        cases = strip_tags(m.group(2))
        note = strip_tags(m.group(3))
        if title:
            items.append(("mecanismo", title, f"{cases}. {note}"[:420]))
        if len(items) >= limit:
            return items
    for m in re.finditer(
        r'<div class="alert[^"]*"[^>]*>\s*<div class="aheader">\s*<div class="aname">(.*?)</div>.*?</div>\s*<div class="adesc">(.*?)</div>',
        src,
        re.S,
    ):
        title = strip_tags(m.group(1))
        desc = strip_tags(m.group(2))
        if title:
            items.append(("alerta", title, desc[:420] + ("…" if len(desc) > 420 else "")))
        if len(items) >= limit:
            return items
    # alert crit/info with bold lead
    for m in re.finditer(r'<div class="alert[^"]*"[^>]*>\s*(.*?)\s*</div>', src, re.S):
        text = strip_tags(m.group(1))
        if len(text) < 40:
            continue
        cut = text.find(". ")
        if 10 < cut < 120:
            title, desc = text[: cut + 1], text[cut + 2 :]
        else:
            title, desc = text[:90] + "…", text
        items.append(("nota", title, desc[:420]))
        if len(items) >= limit:
            break
    return items


def extract_intro(src: str, fallback: str) -> str:
    # First substantial .body paragraph
    for m in re.finditer(r'<p class="body"[^>]*>(.*?)</p>', src, re.S):
        text = strip_tags(m.group(1))
        if len(text) > 80:
            return text[:700] + ("…" if len(text) > 700 else "")
    return fallback


def extract_meta_desc(src: str, fallback: str) -> str:
    m = re.search(r'name="description"\s+content="([^"]+)"', src)
    return m.group(1) if m else fallback


def kpi_html(kpis: list[tuple[str, str, str]]) -> str:
    if not kpis:
        return ""
    classes = ["kj", "kd", "kp", "kt"]
    parts = []
    for i, (label, val, sub) in enumerate(kpis):
        cls = classes[i % len(classes)]
        sub_h = f'<div class="ksub">{html_lib.escape(sub)}</div>' if sub else ""
        parts.append(
            f'<div class="kcard {cls}"><div class="klabel">{html_lib.escape(label)}</div>'
            f'<div class="kval">{html_lib.escape(val)}</div>{sub_h}</div>'
        )
    return '<div class="kgrid">' + "".join(parts) + "</div>"


def timeline_html(items: list[tuple[str, str, str]]) -> str:
    if not items:
        return '<div class="panel"><p class="body">Linha do tempo condensada indisponível neste extrato — consulte o dossiê completo.</p></div>'
    rows = []
    for date, title, desc in items:
        rows.append(
            f'<div class="tli"><div class="tld">{html_lib.escape(date)}</div><div>'
            f'<div class="tltitle">{html_lib.escape(title)} <span class="tag tg">ev-confirmed</span></div>'
            f'<div class="tldesc">{html_lib.escape(desc)}</div></div></div>'
        )
    return '<div class="panel">' + "".join(rows) + "</div>"


def series_nav(current_slug: str) -> str:
    cards = []
    for ch in CHAPTERS:
        href = f"./{ch['slug']}.html"
        cls = "series-card is-current" if ch["slug"] == current_slug else "series-card"
        cards.append(
            f'<a class="{cls}" href="{href}">'
            f'<div class="series-card-id">{ch["ordem"]} · {ch["tid"]}</div>'
            f'<div class="series-card-chapter">{ch["flag"]} {ch["short"]}</div>'
            f'<div class="series-card-desc">{html_lib.escape(ch["headline"])}</div></a>'
        )
    return (
        '<section class="series-nav" id="serie">\n'
        '  <div class="series-nav-title">Artefatos da série · ordem de importância</div>\n'
        '  <div class="series-nav-grid">\n    '
        + "\n    ".join(cards)
        + "\n  </div>\n"
        '  <a class="series-hub" href="./index.html">← Índice inteligente · O Dragão e a Onça</a>\n'
        "</section>"
    )


def render(ch: dict) -> str:
    src_path = ROOT / ch["src"]
    if not src_path.exists():
        raise FileNotFoundError(src_path)
    src = src_path.read_text(encoding="utf-8")
    kpis = extract_kpis(src)
    items = extract_tlis(src)
    if not items:
        items = extract_tlitems(src)
    if not items:
        items = extract_timeline_items(src)
    if not items:
        items = extract_events(src)
    if not items:
        items = extract_findings(src)
    intro = extract_intro(src, ch["blurb"])
    if intro == ch["blurb"]:
        # fallback: meta description or first long paragraph
        for m in re.finditer(r"<p[^>]*>(.*?)</p>", src, re.S):
            text = strip_tags(m.group(1))
            if len(text) > 120:
                intro = text[:700] + ("…" if len(text) > 700 else "")
                break
    desc = extract_meta_desc(src, ch["blurb"])
    n = len(CHAPTERS)
    dossier_href = f"../{ch['src']}"
    em_name = ch["short"].split("·")[0].strip()

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>O Dragão e a Onça — {html_lib.escape(ch['short'])} | Lawfare Timeline</title>
<meta name="description" content="{html_lib.escape(desc)}">
<link rel="canonical" href="https://odragaoeaonca.vercel.app/timeline/{ch['slug']}.html">
<meta property="og:title" content="O Dragão e a Onça — {html_lib.escape(ch['short'])}">
<meta property="og:description" content="{html_lib.escape(ch['headline'])}">
<meta property="og:type" content="website">
<style>
{CSS}
</style>
</head>
<body>
<header>
  <div class="hbadge">{html_lib.escape(ch['badge'])}</div>
  <h1>O <span>Dragão</span> e a Onça — <em>{html_lib.escape(em_name)}</em></h1>
  <div class="hmeta">
    <span class="hm"><b>Padrões:</b> {html_lib.escape(ch['patterns'])}</span>
    <span class="hm"><b>Ordem:</b> {ch['ordem']}/{n}</span>
    <span class="hm"><b>Âncora:</b> #{ch['anchor']}</span>
    <span class="hm"><b>{ch['tid']}</b></span>
  </div>
  <a class="dossie-link" href="{dossier_href}">→ Dossiê completo · {ch['src']}</a>
</header>
<main>
<section class="sec">
  <div class="sec-title">{ch['flag']} {html_lib.escape(ch['headline'])}</div>
  <div class="sec-sub">{html_lib.escape(ch['blurb'])}</div>
  {kpi_html(kpis)}
  <div class="panel"><p class="body">{html_lib.escape(intro)}</p></div>
</section>

<section class="sec">
  <div class="sec-title">🕐 Linha do tempo verificada</div>
  <div class="sec-sub">{len(items)} eventos extraídos do dossiê · condensado</div>
  {timeline_html(items)}
</section>
</main>
<footer>
{series_nav(ch['slug'])}
  <div class="footcc0">⚖ <b>CC0 1.0</b> — Domínio Público · <a href="./index.html">timeline/</a> · série "O Dragão e a Onça"</div>
</footer>
</body>
</html>
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for ch in CHAPTERS:
        path = OUT / f"{ch['slug']}.html"
        path.write_text(render(ch), encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")
    print(f"done · {len(CHAPTERS)} pages")


if __name__ == "__main__":
    main()
