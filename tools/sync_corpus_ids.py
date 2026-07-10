#!/usr/bin/env python3
"""Sincroniza _data/claude.ai-corpus-ids-sync.json com lawfare.json e estudos Jekyll."""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYNC = ROOT / "_data" / "claude.ai-corpus-ids-sync.json"
LAWFARE = ROOT / "_data" / "lawfare.json"
POSTS = ROOT / "_posts" / "estudos"


def main_ids() -> tuple[int, int]:
    data = json.loads(LAWFARE.read_text(encoding="utf-8"))
    ids = sorted(int(a["id"]) for a in data["assuntos"])
    last = ids[-1]
    return last, last + 1


def jekyll_t_studies() -> dict[int, str]:
    out: dict[int, str] = {}
    for p in POSTS.glob("*.md"):
        t = p.read_text(encoding="utf-8", errors="replace")
        m = re.search(r'^id_corpus:\s*["\']?(T-(\d+))["\']?\s*$', t, re.M)
        if m:
            out[int(m.group(2))] = p.stem
    return out


def main() -> None:
    last_main, next_main = main_ids()
    t_posts = jekyll_t_studies()

    data = json.loads(SYNC.read_text(encoding="utf-8"))
    data["_meta"]["generated"] = date.today().isoformat()

    main = data["tracks"]["main"]
    main["last_id"] = last_main
    main["next_available"] = next_main

    batches = main["confirmed_batches"]
    for b in batches:
        if b.get("range") == [1449, 1511]:
            b["range"] = [1449, 1510]
            b["notes"] = (
                b.get("notes", "")
                + " ID 1511+ em lawfare.json (Biazucci/crise merge 2026-05-26)."
            ).strip()
        if b.get("range") == [1527, 1551]:
            if last_main >= 1551:
                b["status"] = "confirmed"
                b["notes"] = (
                    f"Merge lawfare.json {date.today().isoformat()}: "
                    "Biomm 1527-1546, Zema 1547-1550, Homeschooling 1551."
                )
            else:
                b["status"] = "jekyll_published"
                b["notes"] = (
                    "Posts Jekyll (Biomm/Zema/Homeschooling). "
                    f"lawfare.json last={last_main} — merge pendente."
                )
        if b.get("range") == [1552, 1571]:
            if last_main >= 1571:
                b["status"] = "confirmed"
                b["notes"] = (
                    f"Merge lawfare.json {date.today().isoformat()}: "
                    "Operação Rejeito 1552-1571."
                )
            else:
                b["status"] = "jekyll_published"
                b["notes"] = (
                    "Rejeito em _posts/ — merge lawfare.json pendente "
                    f"(next={next_main})."
                )

    thematic = data["tracks"]["thematic"]
    entries = thematic["entries"]
    by_id = {e["id"]: e for e in entries}

    # T-190 ausente na lista de entries
    if 190 not in by_id:
        entries.append(
            {
                "id": 190,
                "status": "confirmed",
                "topic": "Direita Permitida — gatekeeping oposicionista (T-190)",
                "artifact": "direita-permitida-dossie",
                "notes": "Estudo Jekyll 2026-05-22. Renumerado de T-189 conflito Reforma.",
            }
        )
    entries.sort(key=lambda e: e["id"])
    by_id = {e["id"]: e for e in entries}

    if "last_produced" in thematic:
        del thematic["last_produced"]

    t_meta = {
        180: (
            "TSE — seletividade em inelegibilidade e cassação (T-180)",
            "tse-seletividade-inelegibilidade-cassacao",
        ),
        191: ("Custeio administrativo federal — P11 (T-191)", "custeio-administrativo-federal-p11"),
        192: ("Vorcaro triângulo carbono–mineração–banco (T-192)", "vorcaro-triangulo-carbono-mineracao-banco"),
        193: ("Viagens/gastos sigilo — complemento T-191 (T-193)", "viagens-gastos-sigilo-complemento-p11"),
        194: ("Máquina de Gastos P11 — índice cluster (T-194)", "maquina-gastos-p11-indice-cluster"),
        195: ("CPI Crime Organizado × PCC eleitoral (T-195)", "cpi-crime-organizado-pcc-infiltracao-eleitoral"),
        196: ("Radar de Lacunas — Top 30 sem dossiê (T-196)", "top30-alertas-criticos-operacoes-sem-dossie"),
        197: (
            "Operação Rejeito / Serra do Curral / 3 manuscritos (T-197)",
            "operacao-rejeito-serra-curral-manuscritos",
        ),
        198: (
            "COAF × Moraes — acumulação de funções / dosimetria (T-198)",
            "coaf-moraes-acumulacao-funcoes-dosimetria",
        ),
        199: (
            "Fraude Lojas Americanas — risco sacado (T-199)",
            "fraude-lojas-americanas-risco-sacado",
        ),
        200: (
            "Estatais federais rombo P11 — complemento (T-200)",
            "estatais-rombo-p11-complemento",
        ),
        201: (
            "PCC transnacional — OFAC/EUA/eixo luso (T-201)",
            "pcc-transnacional-ofac-eua-luso",
        ),
        202: (
            "Delegada × PCC — infiltração institucional SP (T-202)",
            "delegada-pcc-infiltracao-institucional-sp",
        ),
        203: (
            "Operação Zelotes — captura CARF (T-203)",
            "operacao-zelotes-carf-captura-fiscal",
        ),
        204: (
            "Gastos Paris — cluster extravância Janja (T-204)",
            "gastos-paris-cluster-extravagancia-janja",
        ),
        205: (
            "Duplo Padrão Judicial — índice corpus (T-205)",
            "duplo-padrao-judicial-corpus-bridge",
        ),
        206: (
            "SPLC Modelo Brasil — índice corpus (T-206)",
            "splc-modelo-brasil-corpus-bridge",
        ),
        207: (
            "Vaza Toga INQ 4781 — índice corpus (T-207)",
            "vaza-toga-corpus-bridge",
        ),
        208: (
            "Narrativa vs Evidência — índice corpus (T-208)",
            "narrativa-vs-evidencia-corpus-bridge",
        ),
        209: (
            "JustiçaWatch Brasil — índice corpus (T-209)",
            "justicawatch-brasil-corpus-bridge",
        ),
        210: (
            "Operação Parasitas / cluster Sepse HMAP (T-210)",
            "operacao-parasitas-pc-go-identifica-fraude-em-materiais-hospitalares-no-hmap",
        ),
        211: (
            "2ª fase Operação Sepse — PF/MPF rede lavagem HMAP (T-211)",
            "mpf-e-pf-deflagram-2-fase-da-operacao-sepse-contra-rede-de-lavagem-ligada-ao-hmap",
        ),
        212: (
            "Esquema Sepse — UTI superfaturada e repasse OS (T-212)",
            "esquema-na-operacao-sepse-contratos-superfaturados-de-uti-com-repasse-de-10-a-cupula-da-os",
        ),
        213: (
            "CGU irregularidades OS Sepse em outros estados (T-213)",
            "cgu-confirma-historico-de-irregularidades-da-mesma-os-em-outros-estados-fixacao-de-compete",
        ),
        214: (
            "Status Operação Sepse sem denúncia formal (T-214)",
            "status-atual-da-operacao-sepse-sem-denuncia-formal-ou-desfecho-judicial-ate-a-data-de-regi",
        ),
        215: (
            "Vorcaro STF — 2ª Turma mantém prisão familiares (T-215)",
            "2-turma-do-stf-mantem-prisao-de-pai-e-primo-de-daniel-vorcaro-por-31-gilmar-mendes-diverge",
        ),
        216: (
            "TSE × USAID — parceria e censura seletiva (T-216)",
            "tse-usaid-parceria-censura-seletiva",
        ),
        217: (
            "Seletividade punitiva TSE/Câmara — lacuna metodológica (T-217)",
            "seletividade-punitiva-tse-casos-isolados",
        ),
        218: (
            "Ouro ilegal — vetor P08 Amazônia PCC/CV/Venezuela (T-218)",
            "ouro-ilegal-vetor-p08-amazonia-pcc-cv-venezuela",
        ),
        219: (
            "Farra do INSS — rede completa Conafer/Careca/CPMI (T-219)",
            "farra-inss-rede-completa",
        ),
        220: (
            "Convergência PCC-OFAC × rede Arpar × INSS (T-220)",
            "pcc-ofac-arpar-farra-inss-convergencia",
        ),
    }
    for tid, (topic, artifact) in t_meta.items():
        note = f"Estudo Jekyll _posts/estudos/ ({t_posts.get(tid, '—')})."
        payload = {
            "status": "confirmed",
            "topic": topic,
            "artifact": artifact,
            "notes": note if tid in t_posts else "Entrada pendente de produção",
        }
        if tid in by_id:
            by_id[tid].update(payload)
        elif tid in t_posts:
            entries.append({"id": tid, **payload})
    entries.sort(key=lambda e: e["id"])
    thematic["entries"] = entries

    thematic_last = max((e["id"] for e in entries), default=196)
    thematic["last_id"] = thematic_last
    thematic["next_available"] = thematic_last + 1
    pending = []
    thematic["pending"] = pending
    thematic["pending_notes"] = {}

    merge_done = last_main >= 1571
    sync = data["sync_status"]
    sync["main_track_last_sync"] = date.today().isoformat()
    sync["thematic_track_last_sync"] = date.today().isoformat()
    sync["ids_confirmed_total"] = {
        "main_track": str(last_main),
        "thematic_track": thematic_last,
    }
    sync["ids_pending_production"] = pending
    stale = (
        "Merge lawfare.json: batches Jekyll 1527-1551 e Rejeito 1552-1571",
        "Fila editorial T-192 a T-195 (ver artigos/2026-05-27-top30-alertas-criticos-operacoes-sem-dossie.md)",
    )
    sync["open_items"] = [
        item
        for item in sync.get("open_items", [])
        if "MERGE PCC batch 1449" not in item and item not in stale
    ]
    for note in [
        f"lawfare.json last_id={last_main}; próximo ID livre={next_main}",
    ]:
        if note not in sync["open_items"]:
            sync["open_items"].append(note)
    if merge_done:
        done_note = f"Fila editorial {date.today().isoformat()}: merge 1527-1571; T-192–T-201 + T-196 radar em _posts/estudos/"
        if done_note not in sync["open_items"]:
            sync["open_items"].append(done_note)
    t197_done = 197 in t_posts
    if t197_done:
        t197_note = f"T-197 Operação Rejeito publicado ({date.today().isoformat()})"
        if t197_note not in sync["open_items"]:
            sync["open_items"].append(t197_note)
    t198_done = 198 in t_posts
    if t198_done:
        t198_note = f"T-198 COAF × Moraes publicado ({date.today().isoformat()})"
        if t198_note not in sync["open_items"]:
            sync["open_items"].append(t198_note)
    for tid, label in (
        (199, "Lojas Americanas"),
        (200, "Estatais rombo P11"),
        (201, "PCC transnacional"),
        (202, "Delegada × PCC"),
        (203, "Zelotes CARF"),
        (204, "Gastos Paris"),
        (205, "Duplo padrão corpus"),
        (206, "SPLC corpus"),
        (207, "Vaza Toga corpus"),
        (208, "Narrativa vs Evidência"),
        (209, "JustiçaWatch Brasil"),
        (210, "Cluster Sepse Parasitas"),
        (211, "Sepse 2ª fase"),
        (212, "Sepse UTI"),
        (213, "CGU Sepse"),
        (214, "Status Sepse"),
        (215, "Vorcaro STF"),
        (216, "TSE USAID"),
        (217, "Seletividade TSE"),
        (218, "Ouro ilegal P08"),
        (219, "Farra INSS"),
        (220, "PCC-OFAC Arpar"),
    ):
        if tid in t_posts:
            note = f"T-{tid} {label} publicado ({date.today().isoformat()})"
            if note not in sync["open_items"]:
                sync["open_items"].append(note)
    if 196 in t_posts:
        t196_note = f"T-196 Radar Top 30 publicado em estudos/ ({date.today().isoformat()})"
        if t196_note not in sync["open_items"]:
            sync["open_items"].append(t196_note)
        sync["open_items"] = [
            item
            for item in sync.get("open_items", [])
            if item != "Publicar T-196 (Radar Top 30 lacunas) de artigos/ → _posts/estudos/"
            and "T-196 pós-publicação" not in item
            and "entrada pendente de produção" not in item
        ]
    if 180 in t_posts:
        sync["open_items"] = [
            item
            for item in sync.get("open_items", [])
            if "T-180" not in item and "Produzir ID 180" not in item
        ]
    if 208 in t_posts and 209 in t_posts:
        sync["open_items"] = [
            item
            for item in sync.get("open_items", [])
            if "Formalizar IDs 208-209" not in item
            and "Integrar JustiçaWatch" not in item
        ]
    elif 180 in pending:
        t180 = "Pendente: T-180 TSE seletividade"
        if t180 not in sync["open_items"]:
            sync["open_items"].append(t180)

    sync["open_items"] = list(dict.fromkeys(sync.get("open_items", [])))
    stale_open = (
        "Fila editorial T-192 a T-195",
        "T-208/T-209 reserved",
        "ids_pending_production",
        "last_id=1576",
        "Próximo: Rombo estatais P11",
        "PCC transnacional residual",
        "Formalizar IDs 208-209",
        "Integrar JustiçaWatch",
        "Pendente: T-180",
        "Produzir ID 180",
        "T-219 (pendente)",
        "T-220 (pendente)",
    )
    sync["open_items"] = [
        item
        for item in sync.get("open_items", [])
        if not any(s in item for s in stale_open)
    ]
    next_note = f"Próximo thematic: T-{thematic_last + 1}; main next={next_main}"
    if next_note not in sync["open_items"]:
        sync["open_items"].append(next_note)

    artifact_t_map = {
        "duplo-padrao-judicial.html": 205,
        "splc-modelo-brasil.html": 206,
        "vaza-toga.html": 207,
        "narrativa-vs-evidencia.html": 208,
        "justicawatch-brasil.html": 209,
    }
    sync["artifacts_without_thematic_id"] = [
        art
        for art, tid in artifact_t_map.items()
        if tid not in t_posts
    ]

    data["id_conflict_resolutions"]["custeio_vs_top30"] = {
        "T-191": "Custeio P11 — estudo canônico",
        "T-196": "Radar Top 30 — renumerado do antigo T-191",
        "date": date.today().isoformat(),
    }

    SYNC.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    html_path = write_status_html(data, last_main, next_main, t_posts, thematic_last)
    print(
        f"sync OK: main last={last_main} next={next_main}; "
        f"thematic last={thematic_last} next={thematic_last + 1}"
    )
    print(f"status HTML: {html_path}")
    print(f"T-studies on disk: {sorted(t_posts.items())}")


def write_status_html(
    data: dict,
    last_main: int,
    next_main: int,
    t_posts: dict[int, str],
    thematic_last: int,
) -> Path:
    """Gera painel HTML alinhado ao design system LAWFARE."""
    today = date.today().isoformat()
    out = ROOT / "_data" / f"sync_status_{today}.html"
    latest = ROOT / "_data" / "sync_status_latest.html"
    merge_done = last_main >= 1571
    jekyll_pending = 0 if merge_done else max(0, 1571 - 1527 + 1)
    pending = data["tracks"]["thematic"].get("pending") or []
    pending_str = ", ".join(str(p) for p in pending) or "—"
    merge_row = (
        f'<div class="row"><div class="dot d-ok"></div><div class="desc">'
        f'<span class="tag t-ok">confirmed</span>1527–1571 merge em lawfare.json ({today})</div></div>'
        if merge_done
        else (
            '<div class="row"><div class="dot d-warn"></div><div class="desc">'
            '<span class="tag t-warn">jekyll_published</span>1527–1571 em _posts/ — merge pendente</div></div>'
        )
    )
    t192_row = (
        '<div class="row"><div class="dot d-ok"></div><div class="lbl">T-192</div>'
        '<div class="desc">Vorcaro triângulo — publicado em <code>_posts/estudos/</code></div></div>'
        if 192 in t_posts
        else (
            '<div class="row"><div class="dot d-danger"></div><div class="lbl">T-192</div>'
            '<div class="desc">Vorcaro — publicar em <code>_posts/estudos/</code></div></div>'
        )
    )
    thematic_pending_rows = ""
    if 180 in pending:
        thematic_pending_rows += (
            '<div class="row"><div class="dot d-danger"></div><div class="desc">'
            '<span class="tag t-danger">pending</span>180 TSE seletividade</div></div>'
        )
    for tid in (192, 193, 194, 195):
        if tid not in t_posts and tid in pending:
            thematic_pending_rows += (
                f'<div class="row"><div class="dot d-warn"></div><div class="desc">'
                f'<span class="tag t-warn">pending</span>{tid}</div></div>'
            )

    next_thematic = thematic_last + 1
    t180_dot = "d-ok" if 180 in t_posts else "d-warn"
    t180_tag = "t-ok" if 180 in t_posts else "t-warn"
    t180_lbl = "confirmed" if 180 in t_posts else "pendente sync"
    t197_row = (
        '<div class="row"><div class="dot d-ok"></div><div class="lbl">T-197</div>'
        '<div class="desc">Operação Rejeito / Serra do Curral — publicado em <code>_posts/estudos/</code></div></div>'
        if 197 in t_posts
        else (
            '<div class="row"><div class="dot d-danger"></div><div class="lbl">T-197</div>'
            '<div class="desc">Operação Rejeito cluster 1552–1571 — produzir dossiê</div></div>'
        )
    )
    t198_row = (
        '<div class="row"><div class="dot d-ok"></div><div class="lbl">T-198</div>'
        '<div class="desc">COAF × Moraes / dosimetria — publicado em <code>_posts/estudos/</code></div></div>'
        if 198 in t_posts
        else (
            '<div class="row"><div class="dot d-danger"></div><div class="lbl">T-198</div>'
            '<div class="desc">COAF × Moraes — produzir dossiê</div></div>'
        )
    )
    t199_row = (
        '<div class="row"><div class="dot d-ok"></div><div class="lbl">T-199</div>'
        '<div class="desc">Fraude Lojas Americanas — publicado em <code>_posts/estudos/</code></div></div>'
        if 199 in t_posts
        else (
            '<div class="row"><div class="dot d-danger"></div><div class="lbl">T-199</div>'
            '<div class="desc">Fraude Lojas Americanas — produzir dossiê</div></div>'
        )
    )
    t200_row = (
        '<div class="row"><div class="dot d-ok"></div><div class="lbl">T-200</div>'
        '<div class="desc">Estatais rombo P11 — publicado em <code>_posts/estudos/</code></div></div>'
        if 200 in t_posts
        else (
            '<div class="row"><div class="dot d-info"></div><div class="lbl">T-200</div>'
            '<div class="desc">Próximo: Rombo estatais P11</div></div>'
        )
    )
    t201_row = (
        '<div class="row"><div class="dot d-ok"></div><div class="lbl">T-201</div>'
        '<div class="desc">PCC transnacional OFAC/EUA/luso — publicado</div></div>'
        if 201 in t_posts
        else (
            '<div class="row"><div class="dot d-info"></div><div class="lbl">T-201</div>'
            '<div class="desc">PCC transnacional residual</div></div>'
        )
    )
    t196_row = (
        '<div class="row"><div class="dot d-ok"></div><div class="lbl">T-196</div>'
        '<div class="desc">Radar Top 30 lacunas — publicado</div></div>'
        if 196 in t_posts
        else (
            '<div class="row"><div class="dot d-warn"></div><div class="lbl">T-196</div>'
            '<div class="desc">Radar Top 30 — publicar em estudos/</div></div>'
        )
    )
    t202_row = (
        '<div class="row"><div class="dot d-ok"></div><div class="lbl">T-202</div>'
        '<div class="desc">Delegada × PCC — publicado</div></div>'
        if 202 in t_posts else ""
    )
    t203_row = (
        '<div class="row"><div class="dot d-ok"></div><div class="lbl">T-203</div>'
        '<div class="desc">Zelotes CARF — publicado</div></div>'
        if 203 in t_posts else ""
    )
    t204_row = (
        '<div class="row"><div class="dot d-ok"></div><div class="lbl">T-204</div>'
        '<div class="desc">Gastos Paris cluster — publicado</div></div>'
        if 204 in t_posts else ""
    )
    t205_row = (
        '<div class="row"><div class="dot d-ok"></div><div class="lbl">T-205</div>'
        '<div class="desc">Duplo padrão corpus — publicado</div></div>'
        if 205 in t_posts else ""
    )
    t206_row = (
        '<div class="row"><div class="dot d-ok"></div><div class="lbl">T-206</div>'
        '<div class="desc">SPLC corpus — publicado</div></div>'
        if 206 in t_posts else ""
    )
    t207_row = (
        '<div class="row"><div class="dot d-ok"></div><div class="lbl">T-207</div>'
        '<div class="desc">Vaza Toga corpus — publicado</div></div>'
        if 207 in t_posts else ""
    )

    body = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Corpus sync · {today}</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Syne:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
:root {{
  --bg:#080c10;--bg1:#0d1218;--bg2:#121820;--border:rgba(255,255,255,.06);--border2:rgba(255,255,255,.12);
  --fg:#e8ecf0;--fg2:#8a9ab0;--fg3:#4a5a6a;
  --red:#e84040;--amber:#e8a020;--blue:#3090e8;--green:#28c880;
  --font-mono:'IBM Plex Mono',monospace;--font-display:'Syne',sans-serif;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--fg);font-family:var(--font-mono);font-size:13px;line-height:1.6;padding:24px 20px;max-width:960px;margin:0 auto}}
h1{{font-family:var(--font-display);font-size:22px;margin-bottom:4px}}
.sub{{font-size:12px;color:var(--fg2);margin-bottom:20px}}
.stat-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin-bottom:20px}}
.stat{{background:var(--bg1);border:1px solid var(--border);border-radius:6px;padding:12px 14px}}
.stat-n{{font-family:var(--font-display);font-size:22px;font-weight:700}}
.stat-l{{font-size:10px;color:var(--fg3);margin-top:4px;line-height:1.4}}
.grid2{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px;margin-bottom:20px}}
.card{{background:var(--bg1);border:1px solid var(--border);border-radius:6px;padding:14px 16px}}
.sh{{font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--fg3);border-bottom:1px solid var(--border);padding-bottom:8px;margin-bottom:10px}}
.row{{display:flex;gap:10px;padding:8px 0;border-bottom:1px solid var(--border);font-size:12px}}
.row:last-child{{border:none}}
.dot{{width:7px;height:7px;border-radius:50%;flex-shrink:0;margin-top:5px}}
.d-ok{{background:var(--green)}}.d-warn{{background:var(--amber)}}.d-info{{background:var(--blue)}}.d-danger{{background:var(--red)}}.d-gray{{background:var(--fg3)}}
.tag{{font-size:9px;font-weight:600;padding:2px 6px;border-radius:3px;margin-right:6px;text-transform:uppercase;letter-spacing:.06em}}
.t-ok{{background:rgba(40,200,128,.12);color:var(--green);border:1px solid rgba(40,200,128,.3)}}
.t-warn{{background:rgba(232,160,32,.12);color:var(--amber);border:1px solid rgba(232,160,32,.3)}}
.t-info{{background:rgba(48,144,232,.12);color:var(--blue);border:1px solid rgba(48,144,232,.3)}}
.t-gray{{background:var(--bg2);color:var(--fg2);border:1px solid var(--border)}}
.t-danger{{background:rgba(232,64,64,.12);color:var(--red);border:1px solid rgba(232,64,64,.3)}}
.lbl{{font-family:var(--font-mono);font-size:10px;font-weight:600;color:var(--blue);min-width:48px}}
.desc{{color:var(--fg2);flex:1;line-height:1.5}}
code{{font-size:11px;color:var(--fg)}}
.footer{{margin-top:24px;font-size:10px;color:var(--fg3);border-top:1px solid var(--border);padding-top:12px}}
a{{color:var(--blue)}}
</style>
</head>
<body>
<h1>Corpus sync · lawfare-timeline</h1>
<p class="sub">Gerado em {today} · <code>python tools/sync_corpus_ids.py</code> · fonte <a href="claude.ai-corpus-ids-sync.json">claude.ai-corpus-ids-sync.json</a></p>

<div class="stat-grid">
  <div class="stat"><div class="stat-n" style="color:var(--amber)">{last_main}</div><div class="stat-l">last_id lawfare.json<br>next: {next_main}</div></div>
  <div class="stat"><div class="stat-n" style="color:var(--blue)">{thematic_last}</div><div class="stat-l">thematic last_id<br>next: {next_thematic}</div></div>
  <div class="stat"><div class="stat-n" style="color:var(--green)">{len(pending)}</div><div class="stat-l">pending production<br>{pending_str}</div></div>
  <div class="stat"><div class="stat-n" style="color:var(--{'green' if merge_done else 'red'})">{jekyll_pending}</div><div class="stat-l">IDs faixa 1527–1571<br>{'merged' if merge_done else 'sem merge'}</div></div>
</div>

<div class="grid2">
  <div class="card">
    <div class="sh">main track</div>
    <div class="row"><div class="dot d-ok"></div><div class="desc"><span class="tag t-ok">confirmed</span>1–{last_main} em lawfare.json</div></div>
    {merge_row}
    <div class="row"><div class="dot d-gray"></div><div class="desc"><span class="tag t-gray">batch_file_only</span>1449–1510 em _data/</div></div>
    <div class="row"><div class="dot d-info"></div><div class="desc"><span class="tag t-info">próximo</span>ID {next_main}+ (batch Flávio/Trump)</div></div>
  </div>
  <div class="card">
    <div class="sh">thematic track</div>
    <div class="row"><div class="dot d-ok"></div><div class="desc"><span class="tag t-ok">confirmed</span>100–{thematic_last} (estudos T em disco: {len(t_posts)})</div></div>
    {thematic_pending_rows}
    <div class="row"><div class="dot d-gray"></div><div class="desc"><span class="tag t-gray">sem ID</span>5 artefatos → candidatos {next_thematic}–{next_thematic + 4}</div></div>
  </div>
</div>

<div class="card" style="margin-bottom:12px">
  <div class="sh">fila editorial</div>
  {t192_row if merge_done else '<div class="row"><div class="dot d-danger"></div><div class="lbl">merge</div><div class="desc">lawfare.json 1527–1571 · <code>python tools/process_editorial_queue.py</code></div></div>'}
  {t197_row}
  {t198_row}
  <div class="row"><div class="dot {t180_dot}"></div><div class="lbl">T-180</div><div class="desc">TSE seletividade punitiva · <span class="tag {t180_tag}">{t180_lbl}</span></div></div>
  {t199_row}
  {t200_row}
  {t201_row}
  {t196_row}
  {t202_row}
  {t203_row}
  {t204_row}
  {t205_row}
  {t206_row}
  {t207_row}
  <div class="row"><div class="dot d-info"></div><div class="lbl">T-208+</div><div class="desc">Narrativa vs Evidência · JustiçaWatch · batch 1572+</div></div>
</div>

<div class="card">
  <div class="sh">open items</div>
  <div class="row"><div class="dot d-warn"></div><div class="desc">IPFS/archive.org · JustiçaWatch · P04b em METHODOLOGY-v2.2 · shadowban @araguaci</div></div>
</div>

<p class="footer">CC0 · lawfare-timeline · Atualizar: <code>python tools/sync_corpus_ids.py</code></p>
</body>
</html>
"""
    out.write_text(body, encoding="utf-8")
    latest.write_text(body, encoding="utf-8")
    return out


if __name__ == "__main__":
    main()
