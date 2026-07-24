#!/usr/bin/env python3
"""Gera dashboard e artefatos HTML da série O Dragão e a Onça."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODO = ROOT / "_data" / "todo"
SITE = "https://lawfare-timeline.vercel.app"

SERIES = [
    {
        "order": 1,
        "tid": "T-228",
        "file": "o-dragao-e-a-onca-goias.html",
        "chapter": "Goiás",
        "flag": "🇧🇷 GO",
        "badge": "Capítulo inaugural",
        "accent": "jaguar",
        "title": "Pivô China → EUA/Japão em terras raras",
        "subtitle": "Caiado, Serra Verde, JOGMEC e a pré-candidatura presidencial 2026",
        "patterns": ["P05", "P09", "P10"],
        "batch": None,
        "kpi": [
            ("Operador", "Serra Verde / Pela Ema"),
            ("Pivô", "China 2023 → EUA/Japão 2025"),
            ("Referência", "INESC cita caso no PL 2.780"),
        ],
        "intro": (
            "Capítulo inaugural da série. Cobre 2023–2026: acordos com China (Chint Power, Weichai, "
            "YTO, CMOC, Huawei) sob Ronaldo Caiado, o pivô 2025–2026 para JOGMEC (Japão) e USA Rare "
            "Earth (aquisição Serra Verde, US$ 2,8 bi), e a conversão do ativo mineral em plataforma "
            "da pré-candidatura presidencial (PSD, 2026)."
        ),
    },
    {
        "order": 2,
        "tid": "T-229",
        "file": "dragao-onca-brasil-federal.html",
        "chapter": "Brasil (Federal)",
        "flag": "🇧🇷 BR",
        "badge": "Linha do tempo 1993–2026",
        "accent": "dragon",
        "title": "Parceria estratégica e o caso Doria–Sinovac",
        "subtitle": "COSBAN, MoUs federais e a arquitetura que legitima os capítulos estaduais",
        "patterns": ["P04b", "P05", "P10"],
        "batch": "lawfare-batch-dragao-onca-brasil-1639-1653.json",
        "kpi": [
            ("Marco", "Parceria Estratégica 1993"),
            ("Mecanismo", "COSBAN desde 2004"),
            ("Correção", "Desinformação vacinas 2019 refutada"),
        ],
        "intro": (
            "Timeline federal completa desde a Parceria Estratégica de 1993. Inclui correção factual "
            "sobre compra de vacinas pré-pandemia por Doria, fratura interna Bolsonaro (Eduardo × Huawei) "
            "e o MoU federal de mineração sustentável Brasil–China (2025) — pano de fundo dos capítulos "
            "estaduais."
        ),
    },
    {
        "order": 3,
        "tid": "T-230",
        "file": "dragao-onca-para.html",
        "chapter": "Pará",
        "flag": "🇧🇷 PA",
        "badge": "Ferrovia CCCC + Vale",
        "accent": "teal",
        "title": "Corredor mineral e COP30 como vitrine",
        "subtitle": "Barbalho, nepotismo institucional e exclusão popular documentada",
        "patterns": ["P04b", "P05", "P09", "P10"],
        "batch": "lawfare-batch-dragao-onca-para-1654-1666.json",
        "kpi": [
            ("Projeto", "Ferrovia Marabá–Barcarena"),
            ("Valor", "R$ 7 bi → R$ 10 bi / US$ 2 bi"),
            ("Símbolo", "COP30 Belém, nov/2025"),
        ],
        "intro": (
            "Ferrovia do Pará (protocolo 2019 → MoU Pequim 2023 com CCCC e Vale), Programa Estrutura, "
            "conflito Norsk Hydro/Vale do Acará, rede de proximidade Barbalho e COP30 como ponto de "
            "convergência e contradição simbólica."
        ),
    },
    {
        "order": 4,
        "tid": "T-231",
        "file": "dragao-onca-amazonas.html",
        "chapter": "Amazonas",
        "flag": "🇧🇷 AM",
        "badge": "Taboca / China Nonferrous",
        "accent": "dragon",
        "title": "Contaminação Waimiri-Atroari e Zona Franca",
        "subtitle": "Wilson Lima, cluster PIM e escalada FUNAI + MPF + PF",
        "patterns": ["P04b", "P05", "P06", "P09"],
        "batch": "lawfare-batch-dragao-onca-amazonas-1667-1678.json",
        "kpi": [
            ("Caso grave", "Taboca / ACWA R$ 12,3 mi"),
            ("Precedente", "Quase-genocídio Waimiri-Atroari"),
            ("Padrão", "Ativo estadual → plataforma eleitoral"),
        ],
        "intro": (
            "Caso mais grave da série em escalada institucional simultânea. Pagamento suspeito firmado "
            "dois dias após comunidade declarar desconfiança total. Cluster eletroeletrônico chinês no PIM "
            "tratado à parte. Wilson Lima replica padrão Caiado."
        ),
    },
    {
        "order": 5,
        "tid": "T-232",
        "file": "dragao-onca-minas-gerais.html",
        "chapter": "Minas Gerais",
        "flag": "🇧🇷 MG",
        "badge": "Vale do Lítio",
        "accent": "jaguar",
        "title": "Sigma Lithium e o contraste ocidental",
        "subtitle": "Zema como terceiro governador em transição presidencial 2026",
        "patterns": ["P04b", "P05", "P09", "P10"],
        "batch": "lawfare-batch-dragao-onca-minas-1679-1688.json",
        "kpi": [
            ("Ativo", "Sigma Lithium / Nasdaq"),
            ("Contraste", "Capital ocidental, não chinês"),
            ("Padrão", "3º governador → Presidência"),
        ],
        "intro": (
            "Confirma que o padrão estrutural (governador + ativo mineral + região pobre) independe "
            "do bloco geopolítico do investidor. Terceiro caso da série após Caiado e Wilson Lima."
        ),
    },
    {
        "order": 6,
        "tid": "T-233",
        "file": "dragao-onca-sintese.html",
        "chapter": "Síntese Comparativa",
        "flag": "📊",
        "badge": "Cross-estadual",
        "accent": "purple",
        "title": "Soberania na conta do governador",
        "subtitle": "KPIs, alertas e tese central dos cinco capítulos territoriais",
        "patterns": ["P04b", "P05", "P06", "P09", "P10"],
        "batch": None,
        "kpi": [
            ("Capítulos", "Federal + 4 estados"),
            ("Tese", "União negocia; governador executa"),
            ("Alerta", "Exclusão popular recorrente"),
        ],
        "intro": (
            "Artefato de síntese — não introduz fatos novos. Consolida Federal, GO, PA, AM e MG. "
            "A União negocia marcos amplos, mas é o governador quem assina, executa e arca com o "
            "desgaste — enquanto o benefício segue capturado por capital externo."
        ),
        "synthesis": True,
    },
    {
        "order": 7,
        "tid": "T-234",
        "file": "dragao-onca-braco-juridico.html",
        "chapter": "Braço Jurídico",
        "flag": "⚖️",
        "badge": "Transversal · STF × Congresso",
        "accent": "purple",
        "title": "Marco temporal, PL da Devastação e ADI 7919",
        "subtitle": "OAB × ONGs socioambientais — ponte com o corpus judicial",
        "patterns": ["P01", "P04b", "P05", "P09", "P10"],
        "batch": "lawfare-batch-dragao-onca-juridico-1689-1700.json",
        "kpi": [
            ("STF", "Marco temporal 9×1"),
            ("COP30+", "6 dias → vetos derrubados"),
            ("Ponte", "INQ 4.781 · P01/P03"),
        ],
        "intro": (
            "Primeiro capítulo transversal: arquitetura legal que viabiliza os capítulos estaduais — "
            "saga do marco temporal, licenciamento flexibilizado, ADI 7919 e caso Cinta Larga."
        ),
        "existing": TODO / "dragao-onca-braco-juridico.html",
    },
    {
        "order": 8,
        "tid": "T-235",
        "file": "dragao-onca-pl2780.html",
        "chapter": "PL 2.780/2024",
        "flag": "📜",
        "badge": "Elo legislativo central",
        "accent": "jaguar",
        "title": "Política Nacional de Minerais Críticos",
        "subtitle": "FGAM R$ 2 bi, streaming e conexão Serra Verde confirmada pelo INESC",
        "patterns": ["P05", "P10"],
        "batch": "lawfare-batch-dragao-onca-pl2780-1701-1712.json",
        "kpi": [
            ("Status", "Aprovado Câmara mai/2026"),
            ("Texto", "51 artigos · substitutivo"),
            ("Senado", "Aguardando jul/2026"),
        ],
        "intro": (
            "Rodada dedicada confirmando PL 2.780/2024 como elo legislativo central. INESC cita "
            "nominalmente Serra Verde/Goiás como risco dos contratos de streaming previstos no texto."
        ),
        "existing": TODO / "dragao-onca-pl2780.html",
    },
]

SHARED_CSS = """
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
"""

DASHBOARD_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
:root{
  --bg:#080c10;--bg2:#0f151b;--bg3:#161e26;
  --dragon:#d4342c;--dragon2:#ff6b5f;--dragon-dim:#5c1512;
  --jaguar:#e8b23d;--jaguar2:#ffd270;--jaguar-dim:#6b4e12;
  --gr:#3ecb6f;--purple:#b07aff;--teal:#2ecfb0;
  --border:rgba(255,255,255,0.07);--text:#e8edf0;--text2:#8a99a8;
  --font:'Syne',sans-serif;--mono:'JetBrains Mono',monospace;
}
body{background:var(--bg);color:var(--text);font-family:var(--font);min-height:100vh}
header{padding:32px 24px 22px;border-bottom:2px solid var(--jaguar-dim);background:linear-gradient(135deg,#080c10 0%,#1a1408 55%,#120808 100%);position:relative;overflow:hidden}
header::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 20% 50%,rgba(232,178,61,.12) 0%,transparent 55%),radial-gradient(ellipse at 80% 50%,rgba(212,52,44,.08) 0%,transparent 55%)}
.hbadge{display:inline-flex;align-items:center;gap:6px;background:rgba(232,178,61,.14);border:1px solid var(--jaguar);border-radius:4px;padding:4px 12px;font-size:11px;font-weight:700;letter-spacing:2px;color:var(--jaguar2);text-transform:uppercase;margin-bottom:12px}
header h1{font-size:clamp(28px,5vw,42px);font-weight:800;color:#fff;line-height:1.1;letter-spacing:-.5px}
header h1 em{font-style:normal;color:var(--dragon2)}
header h1 span{color:var(--jaguar2)}
.sub{font-size:14px;color:var(--text2);max-width:820px;margin-top:12px;line-height:1.75}
.stats{display:flex;gap:16px;flex-wrap:wrap;margin-top:18px}
.stat{font-family:var(--mono);font-size:12px;color:var(--text2)}
.stat b{color:var(--jaguar2)}
main{max-width:1200px;margin:0 auto;padding:28px 20px 60px}
.sec-label{font-size:11px;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:var(--text2);margin:8px 0 16px;display:flex;align-items:center;gap:10px}
.sec-label::after{content:'';flex:1;height:1px;background:var(--border)}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
@media(max-width:720px){.grid{grid-template-columns:1fr}}
.card{display:block;background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:18px 20px;text-decoration:none;color:inherit;transition:border-color .2s,transform .15s;position:relative;overflow:hidden}
.card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,var(--jaguar),var(--dragon))}
.card:hover{border-color:rgba(232,178,61,.4);transform:translateY(-2px)}
.card-num{font-family:var(--mono);font-size:10px;color:var(--jaguar2);letter-spacing:1.5px;margin-bottom:6px}
.card-flag{font-size:18px;margin-bottom:8px}
.card-chapter{font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--text2);margin-bottom:4px}
.card-title{font-size:17px;font-weight:800;color:#fff;line-height:1.25;margin-bottom:8px}
.card-desc{font-size:13px;color:var(--text2);line-height:1.65;margin-bottom:12px}
.tags{display:flex;flex-wrap:wrap;gap:6px}
.tag{font-family:var(--mono);font-size:10px;padding:3px 8px;border-radius:4px;background:rgba(212,52,44,.12);color:var(--dragon2);border:1px solid rgba(212,52,44,.25)}
.tag-p{background:rgba(176,122,255,.12);color:var(--purple);border-color:rgba(176,122,255,.25)}
.thesis{margin-top:32px;padding:20px 22px;border-radius:12px;background:rgba(176,122,255,.08);border:1px solid rgba(176,122,255,.22)}
.thesis h2{font-size:16px;font-weight:800;color:var(--purple);margin-bottom:8px}
.thesis p{font-size:13px;color:var(--text2);line-height:1.75}
footer{padding:24px;text-align:center;border-top:2px solid var(--jaguar-dim)}
.foot{font-family:var(--mono);font-size:11px;color:var(--text2)}
.foot b{color:var(--jaguar2)}
""" + SHARED_CSS.replace(".series-nav", ".series-nav-d").replace("series-nav-grid", "series-nav-dgrid")


def load_batch(name: str | None) -> list[dict]:
    if not name:
        return []
    path = TODO / name
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("entries", [])


def fmt_date(entry: dict) -> str:
    d = entry.get("date", "")
    prec = entry.get("date_precision", "day")
    if prec == "year" and len(d) >= 4:
        return d[:4]
    if prec == "month" and len(d) >= 7:
        parts = d.split("-")
        months = ["", "jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
        return f"{months[int(parts[1])]}/{parts[0]}"
    if len(d) >= 10:
        return "/".join(reversed(d[:10].split("-")))
    return d


def ev_tag(status: str) -> str:
    s = (status or "").lower()
    if "confirmed" in s or "confirmado" in s:
        return '<span class="tag tg">ev-confirmed</span>'
    if "alleged" in s:
        return '<span class="tag tgo">ev-alleged</span>'
    return '<span class="tag tgo">ev-inference</span>'


def series_nav_html(current_file: str) -> str:
    cards = []
    for item in SERIES:
        if item["file"] == current_file:
            continue
        cards.append(
            f'<a class="series-card" href="/{item["file"]}">'
            f'<div class="series-card-id">{item["tid"]} · {item["badge"]}</div>'
            f'<div class="series-card-chapter">{item["flag"]} {item["chapter"]}</div>'
            f'<div class="series-card-desc">{item["title"]}</div>'
            f"</a>"
        )
    return f"""
<section class="series-nav" id="serie">
  <div class="series-nav-title">Outros artefatos da série</div>
  <div class="series-nav-grid">
    {''.join(cards)}
  </div>
  <a class="series-hub" href="/odragaoeaonca">← Índice da série · O Dragão e a Onça</a>
</section>
"""


def artifact_template(item: dict, body_sections: str) -> str:
    patterns = " · ".join(item["patterns"])
    kpi_html = "".join(
        f'<div class="kcard k{["j","d","p","t"][i % 4]}">'
        f'<div class="klabel">{label}</div><div class="kval">{val}</div></div>'
        for i, (label, val) in enumerate(item["kpi"])
    )
    nav = series_nav_html(item["file"])
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>O Dragão e a Onça — {item["chapter"]} | Lawfare Timeline</title>
<meta name="description" content="{item["subtitle"]}">
<link rel="canonical" href="{SITE}/{item["file"]}">
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
*{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
:root{{
  --bg:#080c10;--bg2:#0f151b;--bg3:#161e26;
  --dragon:#d4342c;--dragon2:#ff6b5f;--dragon-dim:#5c1512;
  --jaguar:#e8b23d;--jaguar2:#ffd270;--jaguar-dim:#6b4e12;
  --gr:#3ecb6f;--blue:#4a9eff;--purple:#b07aff;--teal:#2ecfb0;
  --border:rgba(255,255,255,0.07);--text:#e8edf0;--text2:#8a99a8;
  --font:'Syne',sans-serif;--mono:'JetBrains Mono',monospace;
}}
body{{background:var(--bg);color:var(--text);font-family:var(--font);min-height:100vh}}
header{{padding:26px 30px 18px;border-bottom:2px solid var(--jaguar-dim);background:linear-gradient(135deg,#080c10 0%,#1a1408 55%,#080c10 100%)}}
.hbadge{{display:inline-flex;background:rgba(232,178,61,.14);border:1px solid var(--jaguar);border-radius:4px;padding:4px 12px;font-size:11px;font-weight:700;letter-spacing:2px;color:var(--jaguar2);text-transform:uppercase;margin-bottom:10px}}
header h1{{font-size:26px;font-weight:800;color:#fff;line-height:1.15}}
header h1 span{{color:var(--jaguar2)}}
header h1 em{{font-style:normal;color:var(--dragon2)}}
.hmeta{{display:flex;gap:18px;margin-top:10px;flex-wrap:wrap;font-size:12px;color:var(--text2);font-family:var(--mono)}}
.hmeta b{{color:var(--jaguar2)}}
main{{padding:0 20px 32px;max-width:1200px;margin:0 auto}}
.sec{{padding:30px 0 10px;border-bottom:1px solid var(--border)}}
.sec-title{{font-size:20px;font-weight:800;color:#fff;margin-bottom:4px}}
.sec-sub{{font-size:12px;color:var(--text2);font-family:var(--mono);margin-bottom:16px}}
.kgrid{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;padding:12px 0}}
@media(max-width:720px){{.kgrid{{grid-template-columns:1fr}}}}
.kcard{{background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:14px}}
.klabel{{font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--text2);margin-bottom:5px}}
.kval{{font-size:18px;font-weight:800;color:var(--jaguar2);line-height:1.2}}
.kd .kval{{color:var(--dragon2)}}.kp .kval{{color:var(--purple)}}.kt .kval{{color:var(--teal)}}
.panel{{background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:18px 20px;margin-bottom:12px}}
p.body{{font-size:13px;color:var(--text2);line-height:1.75;margin-bottom:10px}}
.tli{{display:flex;gap:12px;padding:11px 0;border-bottom:1px solid var(--border)}}
.tli:last-child{{border-bottom:none}}
.tld{{font-family:var(--mono);font-size:11px;color:var(--jaguar2);min-width:90px;font-weight:600;flex-shrink:0}}
.tltitle{{font-size:13px;font-weight:700;margin-bottom:3px;color:#fff}}
.tldesc{{font-size:12px;color:var(--text2);line-height:1.6}}
.tag{{display:inline-block;padding:2px 7px;border-radius:4px;font-size:10px;font-weight:600;margin-left:6px;font-family:var(--mono)}}
.tg{{background:rgba(62,203,111,.1);color:#78f5a8;border:1px solid rgba(62,203,111,.2)}}
.tgo{{background:rgba(232,178,61,.12);color:var(--jaguar2);border:1px solid rgba(232,178,61,.25)}}
footer{{padding:0 0 40px;border-top:2px solid var(--jaguar-dim)}}
.footcc0{{text-align:center;padding:20px;font-family:var(--mono);font-size:11px;color:var(--text2)}}
.footcc0 b{{color:var(--jaguar2)}}
{SHARED_CSS}
</style>
</head>
<body>
<header>
  <div class="hbadge">{item["tid"]} · {item["badge"]}</div>
  <h1>O <span>Dragão</span> e a Onça — <em>{item["chapter"]}</em></h1>
  <div class="hmeta">
    <span class="hm"><b>Padrões:</b> {patterns}</span>
    <span class="hm"><b>Ordem:</b> {item["order"]}/8</span>
    <span class="hm"><b>Série:</b> Brasil × China · braços institucionais</span>
  </div>
</header>
<main>
<section class="sec">
  <div class="sec-title">{item["flag"]} {item["title"]}</div>
  <div class="sec-sub">{item["subtitle"]}</div>
  <div class="kgrid">{kpi_html}</div>
  <div class="panel"><p class="body">{item["intro"]}</p></div>
</section>
{body_sections}
</main>
<footer>
{nav}
  <div class="footcc0">⚖ <b>CC0 1.0</b> — Domínio Público · lawfare-timeline · série "O Dragão e a Onça"</div>
</footer>
</body>
</html>
"""


def timeline_section(entries: list[dict], title: str = "Linha do tempo verificada") -> str:
    if not entries:
        return ""
    items = []
    for e in entries[:20]:
        ev = e.get("evidence_status", e.get("status", ""))
        items.append(
            f'<div class="tli"><div class="tld">{fmt_date(e)}</div><div>'
            f'<div class="tltitle">{e.get("title", "")} {ev_tag(ev)}</div>'
            f'<div class="tldesc">{e.get("summary", "")}</div></div></div>'
        )
    extra = ""
    if len(entries) > 20:
        extra = f'<p class="body">+ {len(entries) - 20} entradas adicionais no corpus batch.</p>'
    return f"""
<section class="sec">
  <div class="sec-title">🕐 {title}</div>
  <div class="sec-sub">{len(entries)} eventos mapeados neste capítulo</div>
  <div class="panel">{''.join(items)}{extra}</div>
</section>
"""


def synthesis_section() -> str:
    rows = []
    for item in SERIES:
        if item.get("synthesis"):
            continue
        rows.append(
            f'<div class="tli"><div class="tld">{item["tid"]}</div><div>'
            f'<div class="tltitle">{item["flag"]} {item["chapter"]}</div>'
            f'<div class="tldesc">{item["intro"][:220]}…</div></div></div>'
        )
    return f"""
<section class="sec">
  <div class="sec-title">📊 Matriz comparativa</div>
  <div class="sec-sub">Consolidação transversal — sem fatos novos</div>
  <div class="panel">
    <p class="body"><b style="color:var(--jaguar2)">Tese central:</b> a União negocia os marcos amplos (tratados, MoUs, cúpulas), mas é o governador estadual quem assina, executa, enfrenta a comunidade e arca com o desgaste político — enquanto o benefício segue capturado por capital externo e a exclusão popular se repete independentemente do bloco geopolítico do investidor.</p>
    {''.join(rows)}
  </div>
</section>
"""


def inject_series_nav(existing_html: str, current_file: str) -> str:
    nav = series_nav_html(current_file)
    if "series-nav" in existing_html:
        existing_html = re.sub(
            r'<section class="series-nav" id="serie">.*?</section>\s*',
            nav,
            existing_html,
            count=1,
            flags=re.DOTALL,
        )
        return existing_html
    css_block = SHARED_CSS
    if ".series-nav" not in existing_html:
        existing_html = existing_html.replace("</style>", css_block + "\n</style>", 1)
    existing_html = re.sub(
        r"(<footer>\s*)",
        r"<footer>\n" + nav + "\n",
        existing_html,
        count=1,
    )
    return existing_html


def build_dashboard() -> str:
    cards = []
    for item in SERIES:
        ptags = "".join(
            f'<span class="tag tag-p">{p}</span>' if p.startswith("P0") else f'<span class="tag">{p}</span>'
            for p in item["patterns"]
        )
        cards.append(
            f'<a class="card" href="/{item["file"]}">'
            f'<div class="card-num">{item["order"]:02d} · {item["tid"]}</div>'
            f'<div class="card-flag">{item["flag"]}</div>'
            f'<div class="card-chapter">{item["chapter"]}</div>'
            f'<div class="card-title">{item["title"]}</div>'
            f'<div class="card-desc">{item["subtitle"]}</div>'
            f'<div class="tags">{ptags}</div>'
            f"</a>"
        )
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>O Dragão e a Onça — Série Brasil × China | Lawfare Timeline</title>
<meta name="description" content="Dashboard da série especializada sobre relações Brasil–China e braços institucionais envolvidos — 8 capítulos verificáveis.">
<link rel="canonical" href="{SITE}/odragaoeaonca">
<meta property="og:title" content="O Dragão e a Onça — Série Brasil × China">
<meta property="og:url" content="{SITE}/odragaoeaonca">
<meta property="og:type" content="website">
<style>{DASHBOARD_CSS}</style>
</head>
<body>
<header>
  <div class="hbadge">Série especializada · Lawfare Timeline</div>
  <h1>O <span>Dragão</span> e a <em>Onça</em></h1>
  <p class="sub">Investigação verificável sobre relações Brasil–China, captura mineral estadual, arquitetura jurídica e braços institucionais (STF, Congresso, governos, capital estrangeiro). Oito artefatos em ordem sugerida — dois cards por linha.</p>
  <div class="stats">
    <span class="stat"><b>8</b> capítulos</span>
    <span class="stat"><b>5</b> eixos territoriais + federal</span>
    <span class="stat"><b>2</b> transversais (jurídico + PL 2.780)</span>
    <span class="stat">Corpus <b>T-228 → T-235</b></span>
  </div>
</header>
<main>
  <div class="sec-label">Artefatos da série · ordem sugerida</div>
  <div class="grid">
    {''.join(cards)}
  </div>
  <div class="thesis">
    <h2>Tese estrutural</h2>
    <p>A soberania mineral negociada em Pequim ou Brasília desembarca na conta do governador estadual. A série documenta execução (GO, PA, AM, MG), pano de fundo federal (1993–2026), síntese comparativa, braço jurídico (marco temporal, licenciamento, ADI 7919) e o elo legislativo PL 2.780/2024 — confirmado pelo INESC como referência nacional ao caso Serra Verde.</p>
  </div>
</main>
<footer>
  <div class="foot">⚖ <b>CC0 1.0</b> — Domínio Público · <a href="/" style="color:var(--jaguar2);text-decoration:none">lawfare-timeline.vercel.app</a></div>
</footer>
</body>
</html>
"""


def main() -> None:
    # Dashboard hub (clean URL via duplicate index)
    hub_dir = ROOT / "odragaoeaonca"
    hub_dir.mkdir(exist_ok=True)
    dashboard = build_dashboard()
    (hub_dir / "index.html").write_text(dashboard, encoding="utf-8")
    (ROOT / "odragaoeaonca.html").write_text(dashboard, encoding="utf-8")

    for item in SERIES:
        out = ROOT / item["file"]
        if item.get("existing") and item["existing"].exists():
            html = item["existing"].read_text(encoding="utf-8")
            html = inject_series_nav(html, item["file"])
            out.write_text(html, encoding="utf-8")
            continue

        entries = load_batch(item.get("batch"))
        if item.get("synthesis"):
            body = synthesis_section()
        else:
            body = timeline_section(entries)

        html = artifact_template(item, body)
        out.write_text(html, encoding="utf-8")

    print("Gerado:")
    print(f"  - {hub_dir / 'index.html'}")
    print(f"  - {ROOT / 'odragaoeaonca.html'}")
    for item in SERIES:
        print(f"  - {ROOT / item['file']}")


if __name__ == "__main__":
    main()
