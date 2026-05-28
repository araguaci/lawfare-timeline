#!/usr/bin/env python3
"""Processa fila editorial: merge lawfare.json 1527-1571 + estudos T-192..T-195."""
from __future__ import annotations

import json
import re
import shutil
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "_data" / "processados"
TODO = ROOT / "_data" / "todo"
LAWFARE = ROOT / "_data" / "lawfare.json"
SYNC = ROOT / "_data" / "claude.ai-corpus-ids-sync.json"
POSTS = ROOT / "_posts"
ESTUDOS = POSTS / "estudos"

CAT_MAP = {
    "captura-institucional": "escandalos",
    "conflito-de-interesses": "escandalos",
    "operacao": "operacoes",
    "operacoes": "operacoes",
    "judicial": "justica",
    "governo": "governo",
    "stf": "stf",
}


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")[:90]


def yaml_escape(s: str) -> str:
    return s.replace('"', '\\"')


def find_post_relpath(eid: int, slug: str, jdate: str) -> str:
    prefix = (jdate or "")[:10]
    candidates = []
    for p in POSTS.rglob("*.md"):
        stem = p.stem
        if prefix and not stem.startswith(prefix):
            continue
        if slug and slug in stem:
            candidates.append(p)
        elif f"timeline-{eid}-" in stem:
            candidates.append(p)
    if not candidates and slug:
        for p in POSTS.rglob(f"*{slug[:40]}*.md"):
            candidates.append(p)
    if candidates:
        return str(candidates[0].relative_to(ROOT)).replace("/", "\\")
    return ""


def biomm_to_assunto(raw: dict) -> dict:
    eid = int(raw["id"])
    cat = CAT_MAP.get((raw.get("categoria") or "").lower(), "escandalos")
    jdate = (raw.get("data_evento") or raw.get("data_iso", ""))[:10]
    slug = slugify(raw.get("titulo", ""))
    fontes = raw.get("fontes") or []
    if isinstance(fontes, list) and fontes and isinstance(fontes[0], dict):
        urls = [f.get("url", "") for f in fontes]
    else:
        urls = [f for f in fontes if isinstance(f, str)]
    return {
        "titulo": raw.get("titulo", ""),
        "data_evento": jdate,
        "data_iso": raw.get("data_iso") or f"{jdate}T12:00:00.000Z",
        "categoria": cat,
        "tags": (raw.get("tags") or [])[:12],
        "descricao": raw.get("descricao", ""),
        "relevancia": raw.get("relevancia", "alta"),
        "impacto_diplomatico": "N/A",
        "tipo_escandalo": raw.get("tipo_perseguicao", raw.get("categoria", "N/A")),
        "fontes": urls,
        "pessoas_envolvidas": raw.get("pessoas_envolvidas") or [],
        "instituicoes_envolvidas": raw.get("instituicoes_envolvidas") or [],
        "pais": raw.get("pais", "Brasil"),
        "valor_envolvido": "N/A",
        "prioridade": raw.get("prioridade", 2),
        "fonte_arquivo": find_post_relpath(eid, slug, jdate),
        "id": eid,
    }


def instancia_to_assunto(raw: dict) -> dict:
    eid = int(raw["id"])
    slug = raw.get("slug") or slugify(raw.get("titulo", ""))
    jdate = (raw.get("data_evento") or "")[:10]
    ev = raw.get("evidencia_primaria") or {}
    desc = ev.get("descricao") or raw.get("observacao_analitica", "")
    fonte_url = ev.get("url_referencia") or ""
    fontes = [fonte_url] if fonte_url else []
    if ev.get("fonte"):
        fontes.append(ev["fonte"])
    atores = [a.get("nome", "") for a in raw.get("atores") or [] if isinstance(a, dict)]
    cat = "operacoes"
    if "stf" in slug or "toffoli" in slug or "moraes" in slug:
        cat = "stf"
    elif "silveira" in slug or "governo" in slug:
        cat = "governo"
    elif "jf-" in slug or "trf" in slug or "homeschool" in slug:
        cat = "justica"
    return {
        "titulo": raw.get("titulo", ""),
        "data_evento": jdate,
        "data_iso": f"{jdate}T12:00:00.000Z",
        "categoria": cat,
        "tags": (raw.get("padroes_ativados") or [])[:8] + ["operacao-rejeito"],
        "descricao": desc[:500],
        "relevancia": "alta",
        "impacto_diplomatico": "N/A",
        "tipo_escandalo": raw.get("operacao_referencia", "N/A"),
        "fontes": fontes,
        "pessoas_envolvidas": atores,
        "instituicoes_envolvidas": [],
        "pais": "Brasil",
        "valor_envolvido": "N/A",
        "prioridade": 1,
        "fonte_arquivo": find_post_relpath(eid, slug, jdate),
        "id": eid,
    }


def merge_lawfare_batches() -> int:
    batches = [
        PROC / "lawfare-1527-1546-biomm-renumerado.json",
        PROC / "zema-1547-1550-renumerado.json",
        PROC / "entry-1551-homeschooling-jales.json",
        PROC / "lawfare-batch-rejeito-1552-1571.json",
    ]
    assuntos_in: list[dict] = []
    for path in batches:
        if not path.is_file():
            print(f"  skip missing {path.name}")
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        items = data if isinstance(data, list) else [data]
        for raw in items:
            if "operacao_referencia" in raw or raw.get("tipo") == "instancia_padrao":
                assuntos_in.append(instancia_to_assunto(raw))
            else:
                assuntos_in.append(biomm_to_assunto(raw))

    data = json.loads(LAWFARE.read_text(encoding="utf-8"))
    assuntos: list = data.get("assuntos") or []
    by_id = {a.get("id"): a for a in assuntos if a.get("id") is not None}
    for item in assuntos_in:
        eid = item["id"]
        if eid in by_id:
            by_id[eid].update(item)
        else:
            assuntos.append(item)
            by_id[eid] = item

    assuntos.sort(key=lambda a: a.get("id") or 0)
    data["assuntos"] = assuntos
    data["total"] = len(assuntos)
    data["data_extração"] = date.today().isoformat()
    datas = [a["data_evento"] for a in assuntos if a.get("data_evento") and a["data_evento"] != "0001-01-01"]
    if datas:
        data["periodo"] = f"{min(datas)} a {max(datas)}"
    data["nota"] = (
        f"Merge fila editorial {date.today().isoformat()}: "
        "lawfare.json 1527-1571 (Biomm, Zema, Homeschooling, Rejeito)."
    )
    LAWFARE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    last = max(by_id.keys()) if by_id else 1526
    print(f"  lawfare.json: {len(assuntos_in)} entradas · total {len(assuntos)} · last_id={last}")
    return last


def write_estudo(path: Path, fm_extra: str, body: str) -> None:
    ESTUDOS.mkdir(parents=True, exist_ok=True)
    content = f"""---
{fm_extra}
---

- &nbsp;
{{:toc .large-only}}

{body}
"""
    path.write_text(content, encoding="utf-8")
    print(f"  estudo {path.name}")


def publish_t192() -> None:
    raw = json.loads((TODO / "T-192-vorcaro-triangulo-carbono-mineracao-banco.json").read_text(encoding="utf-8"))
    v = raw.get("vertices_do_triangulo") or {}
    body = f"""# T-192 · Família Vorcaro — triângulo carbono–mineração–banco

A Folha (20/jan/2026) documentou que **Henrique e Natália Vorcaro** controlam a Alliance Participações com **R$ 45,5 bi** em UECs sem lastro em terras públicas em Apuí/AM — cerca de **80%** dos créditos de carbono fictícios do Amazonas. O Banco Master (Daniel Vorcaro, liquidado nov/2025) financiou o eixo mineral (Tamisa, 3D Minerals/ANM) enquanto o STF mantinha sigilo sobre Compliance Zero.

> {raw.get('observacao_analitica', '')[:400]}…

## Os três vértices

| Vértice | Entidade | Mecanismo |
| --- | --- | --- |
| Carbono | {v.get('carbono', {}).get('entidade', 'Alliance')} | {v.get('carbono', {}).get('mecanismo', '—')} |
| Mineração | Tamisa / 3D Minerals | Captura ANM · TAC Zema |
| Banco | Banco Master | Carteiras fictícias · sigilo Toffoli |

## Cadeia lógica

{raw.get('cadeia_logica', '')}

## Conexões no corpus

"""
    for c in raw.get("conexoes_corpus") or []:
        ref = c.get("id_ref")
        link = ""
        if isinstance(ref, int) and ref >= 1500:
            link = f" (ID {ref})"
        body += f"- {c.get('descricao', '')}{link}\n"

    body += f"""
## Padrões

{', '.join(raw.get('padroes_ativados') or [])}

## Fontes e dossiês

- [Folha / timeline 132](/posts/2026-01-20-timeline-132-folha-revela-familia-vorcaro-controla-80-de-creditos-de-carbono-ficticio/)
- [T-191 Custeio P11](/posts/custeio-administrativo-federal-p11/) — face orçamentária vs. patrimônio natural
- [Dossiê HTML](/artigos/t192-vorcaro-triangulo-carbono-mineracao-banco.html)

*Dossiê T-192 · CC0 · lawfare-timeline*
"""
    write_estudo(
        ESTUDOS / "2026-05-28-vorcaro-triangulo-carbono-mineracao-banco.md",
        """id_corpus: "T-192"
thematic_track: true
title: "T-192 · Vorcaro — Triângulo Carbono–Mineração–Banco"
description: Alliance/Apuí, Tamisa/ANM e Banco Master como arquitetura de extração — vértice familiar do Carbono Oculto e da Operação Rejeito.
date: 2026-05-28T12:00:00-03:00
image:
  path: "/assets/solid/landmark.svg"
tags: ["estudo", "vorcaro", "carbono", "mineracao", "banco-master", "p08", "p11"]
categories: estudos
mermaid: false
pin: false""",
        body,
    )
    dst = PROC / "T-192-vorcaro-triangulo-carbono-mineracao-banco.json"
    if (TODO / "T-192-vorcaro-triangulo-carbono-mineracao-banco.json").is_file():
        shutil.move(str(TODO / "T-192-vorcaro-triangulo-carbono-mineracao-banco.json"), str(dst))


def publish_t193() -> None:
    body = """# T-193 · Viagens e gastos sob sigilo — complemento ao T-191

O [T-191 Custeio P11](/posts/custeio-administrativo-federal-p11/) mapeia o custeio federal agregado (R$ 32,4 bi). Este dossiê foca a **opacidade seletiva**: viagens e cartão corporativo com classificação sigilosa que impede controle social.

## Núcleo documentado

| Episódio | Valor | Opacidade |
| --- | --- | --- |
| [Viagens federais 2024](/posts/2024-01-01-timeline-177-viagens-federais-sob-sigilo-r-405-milhoes-em-2024/) | R$ 405 mi | 99% sigiloso |
| [Cartão Presidência](/posts/2023-01-01-timeline-167-cartao-corporativo-da-presidencia-99-dos-r-555-mil/) | R$ 55,5 mi | 99% opaco |

STF e Senado mantêm o sigilo via recursos próprios — **P03** (chokepoint) aplicado ao próprio orçamento de transparência.

## Leitura com T-191

T-191 = escala macro (P11 orçamentário). T-193 = mecanismo de **blindagem informacional** que torna o P11 auditável só em agregados, nunca em detalhe.

*Dossiê T-193 · CC0*
"""
    write_estudo(
        ESTUDOS / "2026-05-28-viagens-gastos-sigilo-complemento-p11.md",
        """id_corpus: "T-193"
thematic_track: true
title: "T-193 · Viagens e Gastos sob Sigilo — Complemento P11"
description: Opacidade orçamentária federal — viagens R$ 405 mi e cartão corporativo como blindagem informacional do P11.
date: 2026-05-28T12:00:00-03:00
image:
  path: "/assets/solid/sitemap.svg"
tags: ["estudo", "p11", "sigilo", "viagens", "governo"]
categories: estudos
mermaid: false""",
        body,
    )


def publish_t194() -> None:
    body = """# T-194 · Máquina de gastos P11 — índice do cluster orçamentário

Índice editorial dos episódios com maior score no [radar T-196](/artigos/2026-05-27-top30-alertas-criticos-operacoes-sem-dossie.md) — **score combinado ~374,8** no cluster P11.

## Estudos base

- [T-191 Custeio federal](/posts/custeio-administrativo-federal-p11/) — R$ 32,4 bi (1º sem/2025)
- [T-193 Sigilo viagens/cartão](/posts/viagens-gastos-sigilo-complemento-p11/) — opacidade

## Timeline (links)

- [Custeio 178](/posts/2025-01-01-timeline-178-custeio-administrativo-federal-r-324-bilhoes-no-1o/)
- [Viagens sigilo 177](/posts/2024-01-01-timeline-177-viagens-federais-sob-sigilo-r-405-milhoes-em-2024/)
- [Cartão 167](/posts/2023-01-01-timeline-167-cartao-corporativo-da-presidencia-99-dos-r-555-mil/)
- [TST Lexus 174](/posts/2025-08-08-timeline-174-tst-30-lexus-es-300h-a-r-3465-mil-cada-r-1039-mi-s/)
- [Câmara diárias 176](/posts/2024-04-01-timeline-176-camara-dos-deputados-diarias-disparam-78-em-2025-r/)
- [Orçamento secreto](/posts/2025-01-01-novo-orcamento-secreto-stf-suspende-repasses-de-r-4-2-bilhoes-em-emendas-parlamentares/)

*Dossiê T-194 · índice · CC0*
"""
    write_estudo(
        ESTUDOS / "2026-05-28-maquina-gastos-p11-indice-cluster.md",
        """id_corpus: "T-194"
thematic_track: true
title: "T-194 · Máquina de Gastos P11 — Índice do Cluster"
description: Índice editorial do cluster orçamentário P11 — liga T-191, T-193 e episódios timeline de maior score.
date: 2026-05-28T12:00:00-03:00
image:
  path: "/assets/solid/chart-line.svg"
tags: ["estudo", "p11", "indice", "governo", "orçamento"]
categories: estudos
mermaid: false""",
        body,
    )


def publish_t195() -> None:
    body = """# T-195 · CPI Crime Organizado × infiltração eleitoral PCC

Conecta o mapeamento institucional da [CPI do Crime Organizado e CPMI do INSS](/posts/2026-01-28-timeline-134-cpi-do-crime-organizado-e-cpmi-do-inss-convergem-nos-mesmos-atores-do-ba/) com a trilha **PCC × fintech × eleições 2024** (main track 1495, 1505).

## Eixo institucional

A CPI/CPMI documenta convergência de atores do BA com o mesmo ecossistema investigado no INSS (Hydra) — **P10** (infraestrutura de serviço compartilhada).

## Eixo eleitoral

- [Infiltração fintech 2024](/posts/pcc-infiltracao-eleitoral-fintech-campanha-municipal-2024-contratos/) — operador preso
- [CPI CO mapeamento](/posts/cpi-crime-organizado-mapeamento-pcc-cv-infiltracao-municipal/)

## Padrões

P10 + P08 (fintech) + lawfare eleitoral.

*Dossiê T-195 · CC0*
"""
    write_estudo(
        ESTUDOS / "2026-05-28-cpi-crime-organizado-pcc-infiltracao-eleitoral.md",
        """id_corpus: "T-195"
thematic_track: true
title: "T-195 · CPI Crime Organizado × PCC Eleitoral"
description: Convergência CPI/CPMI, Hydra/INSS e infiltração eleitoral via fintech — P10 e lawfare eleitoral.
date: 2026-05-28T12:00:00-03:00
image:
  path: "/assets/solid/bullseye.svg"
tags: ["estudo", "pcc", "cpi", "eleitoral", "fintech", "p10"]
categories: estudos
mermaid: false""",
        body,
    )


def update_sync_after_queue(last_main: int) -> None:
    data = json.loads(SYNC.read_text(encoding="utf-8"))
    main = data["tracks"]["main"]
    main["last_id"] = last_main
    main["next_available"] = last_main + 1
    for b in main.get("confirmed_batches", []):
        if b.get("range") == [1527, 1551]:
            b["status"] = "confirmed"
            b["notes"] = f"Merge lawfare.json {date.today().isoformat()}."
        if b.get("range") == [1552, 1571]:
            b["status"] = "confirmed"
            b["notes"] = f"Merge lawfare.json {date.today().isoformat()}."

    thematic = data["tracks"]["thematic"]
    entries = thematic["entries"]
    by_id = {e["id"]: e for e in entries}
    for tid, topic, artifact in [
        (192, "Vorcaro triângulo carbono–mineração–banco (T-192)", "vorcaro-triangulo-carbono-mineracao-banco"),
        (193, "Viagens/gastos sigilo — complemento T-191 (T-193)", "viagens-gastos-sigilo-complemento-p11"),
        (194, "Máquina de Gastos P11 — índice cluster (T-194)", "maquina-gastos-p11-indice-cluster"),
        (195, "CPI Crime Organizado × PCC eleitoral (T-195)", "cpi-crime-organizado-pcc-infiltracao-eleitoral"),
    ]:
        if tid not in by_id:
            entries.append({"id": tid, "status": "confirmed", "topic": topic, "artifact": artifact})
        else:
            by_id[tid].update({"status": "confirmed", "topic": topic, "artifact": artifact})
    entries.sort(key=lambda e: e["id"])
    thematic["entries"] = entries
    thematic["last_id"] = 195
    thematic["next_available"] = 196
    thematic["pending"] = [180]
    thematic["pending_notes"] = {
        "180": "TSE seletividade — entrada pronta para produção (sem estudo Jekyll ainda)",
    }

    sync = data["sync_status"]
    sync["main_track_last_sync"] = date.today().isoformat()
    sync["thematic_track_last_sync"] = date.today().isoformat()
    sync["ids_confirmed_total"] = {
        "main_track": str(last_main),
        "thematic_track": 195,
    }
    sync["ids_pending_production"] = [180]
    open_items = sync.get("open_items", [])
    for note in [
        f"Fila editorial 2026-05-28: merge main até {last_main}; T-192–T-195 publicados",
        "Pendente: T-180 TSE seletividade",
        "Pendente: batch 1572+ Flávio/Trump após validação",
    ]:
        if note not in open_items:
            open_items.append(note)
    sync["open_items"] = open_items

    SYNC.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  sync: main={last_main}, thematic last=195, pending=[180]")


def main() -> None:
    import subprocess
    import sys

    print("=== Fila editorial ===\n1. Merge lawfare.json")
    last = merge_lawfare_batches()
    print("\n2. Estudos temáticos")
    publish_t192()
    publish_t193()
    publish_t194()
    publish_t195()
    print("\n3. Sync JSON")
    update_sync_after_queue(last)
    print("\n4. Status HTML")
    subprocess.run([sys.executable, str(ROOT / "tools" / "sync_corpus_ids.py")], check=False)


if __name__ == "__main__":
    main()
