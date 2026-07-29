#!/usr/bin/env python3
from pathlib import Path

p = Path(__file__).resolve().parent.parent / "timeline" / "index.html"
t = p.read_text(encoding="utf-8")
repls = {
    "../dragao-onca-brasil-federal.html": "./timeline-brasil-federal.html",
    "../dragao-onca-braco-diplomatico.html": "./timeline-braco-diplomatico.html",
    "../dragao-onca-sao-paulo.html": "./timeline-sao-paulo.html",
    "../dragao-onca-goias.html": "./timeline-goias.html",
    "../dragao-onca-minas-gerais.html": "./timeline-minas-gerais.html",
    "../dragao-onca-bahia.html": "./timeline-bahia.html",
    "../dragao-onca-para.html": "./timeline-para.html",
    "../dragao-onca-amazonas.html": "./timeline-amazonas.html",
    "../dragao-onca-parana.html": "./timeline-parana.html",
    "../dragao-onca-rio-grande-do-sul.html": "./timeline-rio-grande-do-sul.html",
    "../dragao-onca-rs-es-ranking-nacional.html": "./timeline-rs-es-ranking.html",
    "../dragao-onca-sintese.html": "./timeline-sintese.html",
    "../dragao-onca-pl2780.html": "./timeline-pl2780.html",
    "../dragao-onca-braco-juridico.html": "./timeline-braco-juridico.html",
    "../dragao-onca-sintese-final-cross-state.html": "./timeline-sintese-final.html",
    "../dragao-onca-amapa.html": "./timeline-amapa.html",
    "../dragao-onca-rj.html": "./timeline-rj.html",
    "../dragao-onca-santa-catarina.html": "./timeline-santa-catarina.html",
}
for a, b in repls.items():
    t = t.replace(f'href="{a}"', f'href="{b}"')
t = t.replace(
    "Cards apontam ao dossiê HTML",
    "Cards apontam à timeline condensada (dossiê no topo de cada página)",
)
# Contagens alinhadas a README 0–18
t = t.replace("<b>18</b> artefatos</span>", "<b>19</b> artefatos</span>")
t = t.replace("<b>17</b> timelines + dossiês</span>", "<b>18</b> timelines + dossiês</span>")
t = t.replace("<b>17</b> dossiês HTML</span>", "<b>18</b> timelines + dossiês</span>")
t = t.replace("<b>11</b> UFs</span>", "<b>12</b> UFs</span>")
t = t.replace("T-228 → T-245", "T-228 → T-246")
t = t.replace("IDs <b>1639–1762</b>", "IDs <b>1639–1770</b>")
t = t.replace("0→17 · deep-link estável", "0→18 · deep-link estável")
t = t.replace("ordem de importância (0–17)", "ordem de importância (0–18)")
t = t.replace("Mesma ordem 0–17.", "Mesma ordem 0–18.")
t = t.replace("README 0–17", "README 0–18")
p.write_text(t, encoding="utf-8")
print("updated", p)
