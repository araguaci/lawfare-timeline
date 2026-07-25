#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sincroniza os batches pendentes de _data/todo/ com o corpus e publica posts Jekyll.
Processa:
1. Moraes & Transcooper (main track): renumera de 1595 a 1600.
2. Operação Sepse (thematic track): T-210 a T-214.
3. Gilmar Mendes Habeas Corpus (decano): 25 posts sem ID sequencial.
"""

from __future__ import annotations

import json
import re
import shutil
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TODO = ROOT / "_data" / "todo"
PROC = ROOT / "_data" / "processados"
POSTS = ROOT / "_posts"
LAWFARE = ROOT / "_data" / "lawfare.json"
UNIFIED = ROOT / "_data" / "lawfare-unified-corpus.json"
SYNC = ROOT / "_data" / "claude.ai-corpus-ids-sync.json"

IMAGE_BY_CATEGORY = {
    "operacoes": "/assets/solid/bullseye.svg",
    "escandalos": "/assets/solid/skull.svg",
    "stf": "/assets/solid/gavel.svg",
    "justica": "/assets/solid/hammer.svg",
    "governo": "/assets/solid/sitemap.svg",
    "impunidade": "/assets/solid/handcuffs.svg",
    "lawfare": "/assets/solid/weight-scale.svg",
    "crise-diplomatica": "/assets/solid/globe.svg",
    "bancos": "/assets/solid/landmark.svg",
    "decano": "/assets/solid/user-tie.svg",
    "estudos": "/assets/solid/book-open.svg"
}

def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")[:90]

def yaml_escape(s: str) -> str:
    return s.replace('"', '\\"')

def format_iso(d: str) -> str:
    return f"{(d or '2026-01-01')[:10]}T12:00:00.000Z"

def resolve_category(entry: dict, default="escandalos") -> str:
    title = (entry.get("titulo") or entry.get("title") or "").lower()
    cat = (entry.get("categoria") or entry.get("category") or "").lower()
    tags = [str(t).lower() for t in entry.get("tags") or []]
    
    actors = " ".join(
        (a.get("nome") or a.get("name") or str(a))
        for a in (entry.get("atores") or entry.get("actors") or entry.get("pessoas_envolvidas") or [])
        if isinstance(a, (dict, str))
    ).lower()

    if "moraes" in title or "moraes" in actors or "toffoli" in title or "toffoli" in actors or "stf" in title:
        return "stf"
    if "crise-diplomatica" in cat or "crise-diplomatica" in tags:
        return "crise-diplomatica"
    if "operacao" in cat or "operacao_policial" in cat or "operacoes" in cat or "operacao" in tags:
        return "operacoes"
    if cat in ("judicial", "justica", "justiça"):
        return "justica"
    return default

def build_tags(entry: dict, category: str) -> list[str]:
    tags: list[str] = []
    for src in (entry.get("padroes_ativados"), entry.get("patterns"), entry.get("tags")):
        if src:
            tags.extend(str(x) for x in src)
    if entry.get("slug"):
        tags.append(entry["slug"])
    if category not in tags:
        tags.insert(0, category)
    return list(dict.fromkeys(tags))[:12]

def renumber_conn(conn_list: list, id_map: dict) -> list:
    new_conns = []
    for c in conn_list or []:
        c_str = str(c)
        # Substitui ocorrências dos IDs antigos pelos novos no texto da conexão
        for old, new in id_map.items():
            c_str = re.sub(rf'\b{old}\b', str(new), c_str)
        new_conns.append(c_str)
    return new_conns

def render_post_main(u: dict) -> str:
    category = u["jekyll_categories"][0]
    tags = u.get("jekyll_tags") or []
    title = u["titulo"]
    resumo = u["resumo"]
    desc = yaml_escape((resumo[:157] + "…") if len(resumo) > 157 else resumo)
    image = IMAGE_BY_CATEGORY.get(category, "/assets/solid/circle-exclamation.svg")
    fm_tags = json.dumps(tags, ensure_ascii=False)
    perm = u.get("jekyll_permalink") or f"/posts/{Path(u['jekyll_filename']).stem}/"

    parts = [
        "- &nbsp;",
        "{:toc .large-only}",
        "",
        f"# {title}",
        "",
        "***",
        "",
        "## 🧭 Resumo",
        "",
        resumo,
        "",
        "***",
        "",
        "## 🏷️ Metadados do corpus",
        "",
        "| Campo | Valor |",
        "| --- | --- |",
        f"| `id_corpus` | **{u.get('id_corpus', '')}** |",
        f"| Categoria analítica | {u.get('categoria', '—')} |",
        f"| País / âmbito | {u.get('pais', '—')} |",
        "",
    ]
    if u.get("conflito_nota"):
        parts.extend([f"> **Nota de conflito ID:** {u['conflito_nota']}", ""])

    if u.get("atores"):
        parts.extend(["### Atores", ""] + [f"- {a}" for a in u["atores"]] + [""])
    if u.get("instituicoes"):
        parts.extend(["### Instituições", ""] + [f"- {i}" for i in u["instituicoes"]] + [""])

    if u.get("_result"):
        parts.extend(["## Resultado documentado", "", u["_result"], ""])
    if u.get("_analise") and u["_analise"] != resumo:
        parts.extend(["## Análise", "", u["_analise"], ""])
    if u.get("_legal"):
        parts.extend(["## Base legal / referências normativas", ""] + [f"- {lb}" for lb in u["_legal"]] + [""])
    if u.get("conexoes") or u.get("_conexoes"):
        conns = u.get("conexoes") or u.get("_conexoes") or []
        parts.extend(["## Conexões no corpus", ""] + [f"- {c}" for c in conns] + [""])
    lacunas = u.get("_lacunas") or []
    if lacunas:
        parts.extend(["## Lacunas investigativas", ""] + [f"- {x}" for x in lacunas] + [""])

    fontes = u.get("fontes_verificadas") or []
    if fontes:
        parts.extend(["## 📚 Fontes verificáveis", ""])
        for i, f in enumerate(fontes, 1):
            url = f.get("url", "")
            tit = f.get("titulo", "Fonte")
            if url:
                parts.append(f"{i}. [{tit}]({url})")
            elif tit:
                parts.append(f"{i}. {tit}")
        parts.append("")

    fm = f"""---
title: "{yaml_escape(title)}"
description: "{desc}"
date: {format_iso(u.get('jekyll_date', ''))}
image:
  path: "{image}"
tags: {fm_tags}
categories: {category}
permalink: {perm}
id_corpus: "{u.get('id_corpus', '')}"
corpus_unificado: true
source_data: "{u.get('_source', '')}"
---

"""
    return fm + "\n".join(parts)

def render_post_thematic(u: dict) -> str:
    category = "estudos"
    tags = u.get("jekyll_tags") or []
    title = u.get("title") or u.get("titulo") or ""
    resumo = u.get("summary") or u.get("descricao") or u.get("resumo") or ""
    desc = yaml_escape((resumo[:157] + "…") if len(resumo) > 157 else resumo)
    image = IMAGE_BY_CATEGORY.get(category, "/assets/solid/circle-exclamation.svg")
    fm_tags = json.dumps(tags, ensure_ascii=False)
    perm = f"/posts/{Path(u['jekyll_filename']).stem}/"

    # Criar mapeamento de links para as conexões
    # Ex: "id_211" -> "/posts/2026-04-23-mpf-e-pf-deflagram-2-fase-da-operacao-sepse-contra-rede-de-lavagem-ligada-ao-hmap/"
    connections_links = []
    for c in u.get("connections", []):
        target_id_str = c.replace("id_", "")
        if target_id_str.isdigit():
            target_id = int(target_id_str)
            # Encontrar no json sepse
            target_post_url = resolve_sepse_url(target_id)
            target_title = resolve_sepse_title(target_id)
            if target_post_url and target_title:
                connections_links.append(f"[T-{target_id} · {target_title}]({target_post_url})")
            else:
                connections_links.append(f"T-{target_id}")
        else:
            connections_links.append(c)

    parts = [
        "- &nbsp;",
        "{:toc .large-only}",
        "",
        f"# {title}",
        "",
        "***",
        "",
        "## 🧭 Resumo",
        "",
        resumo,
        "",
        "***",
        "",
        "## 🏷️ Metadados do Estudo Temático",
        "",
        "| Campo | Valor |",
        "| --- | --- |",
        f"| `id_corpus` | **T-{u.get('id', '')}** |",
        f"| Categoria | {u.get('category', '—')} |",
        f"| Status de Evidência | {u.get('evidence_status', '—')} |",
        "",
    ]

    if u.get("actors"):
        parts.extend(["### Atores", ""])
        for a in u["actors"]:
            if isinstance(a, dict):
                parts.append(f"- **{a.get('name')}** ({a.get('role', '—')}) — *{a.get('institution', '—')}*")
            else:
                parts.append(f"- {a}")
        parts.append("")

    if u.get("institutions"):
        parts.extend(["### Instituições", ""] + [f"- {i}" for i in u["institutions"]] + [""])

    if u.get("legal_basis"):
        parts.extend(["## Base legal e referências normativas", ""] + [f"- {lb}" for lb in u["legal_basis"]] + [""])

    if u.get("analise"):
        parts.extend(["## Análise Estrutural e Padrão Ativado", "", u["analise"], ""])
        
    if u.get("result"):
        parts.extend(["## Resultado e Desfecho", "", u["result"], ""])
        
    if u.get("lacuna_investigativa"):
        parts.extend(["## Lacunas Investigativas", "", u["lacuna_investigativa"], ""])

    if connections_links:
        parts.extend(["## Conexões no corpus", ""] + [f"- {c}" for c in connections_links] + [""])

    fontes = u.get("sources") or []
    if fontes:
        parts.extend(["## 📚 Fontes verificáveis", ""])
        for i, f in enumerate(fontes, 1):
            if isinstance(f, dict):
                url = f.get("url", "")
                tit = f.get("title") or f.get("titulo") or "Fonte"
                outlet = f.get("outlet", "")
                d_str = f.get("date", "")
                parts.append(f"{i}. [{tit}]({url}) ({outlet}, {d_str})")
            else:
                parts.append(f"{i}. {f}")
        parts.append("")

    fm = f"""---
title: "T-{u.get('id', '')} · {yaml_escape(title)}"
description: "{desc}"
date: {format_iso(u.get('date', ''))}
image:
  path: "{image}"
tags: {fm_tags}
categories: {category}
permalink: {perm}
id_corpus: "T-{u.get('id', '')}"
thematic_track: true
source_data: "{u.get('_source', '')}"
---

"""
    return fm + "\n".join(parts)

sepse_data_cache = {}
def load_sepse_cache():
    sepse_path = TODO / "lawfare-210-214-operacao-sepse.json"
    if sepse_path.is_file():
        with open(sepse_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data.get("assuntos", []):
                sepse_data_cache[int(item["id"])] = item

def resolve_sepse_url(tid: int) -> str | None:
    if not sepse_data_cache:
        load_sepse_cache()
    item = sepse_data_cache.get(tid)
    if item:
        slug = slugify(item["title"])
        jdate = item["date"][:10]
        return f"/posts/{jdate}-{slug}/"
    return None

def resolve_sepse_title(tid: int) -> str | None:
    if not sepse_data_cache:
        load_sepse_cache()
    item = sepse_data_cache.get(tid)
    if item:
        return item["title"]
    return None

def render_post_decano(u: dict) -> str:
    category = "decano"
    title = u["titulo"]
    resumo = u["descricao"]
    desc = yaml_escape((resumo[:157] + "…") if len(resumo) > 157 else resumo)
    image = IMAGE_BY_CATEGORY.get(category, "/assets/solid/user-tie.svg")
    tags = u.get("tags") or ['gilmar-mendes', 'decano', 'habeas-corpus', 'stf']
    fm_tags = json.dumps(tags, ensure_ascii=False)
    
    # Resolver permalink
    slug = slugify(title)
    jdate = u["data"][:10]
    perm = f"/posts/{jdate}-{slug}/"

    parts = [
        "- &nbsp;",
        "{:toc .large-only}",
        "",
        f"# {title}",
        "",
        "***",
        "",
        "## 🧭 Resumo",
        "",
        resumo,
        "",
        "***",
        "",
    ]

    if u.get("envolvidos"):
        parts.extend(["### Envolvidos", ""] + [f"- {e}" for e in u["envolvidos"]] + [""])

    fontes = u.get("fonte") or []
    if fontes:
        parts.extend(["## 📚 Fontes verificáveis", ""])
        for i, f in enumerate(fontes, 1):
            parts.append(f"{i}. {f}")
        parts.append("")

    fm = f"""---
layout: post
title: "{yaml_escape(title)}"
description: "{desc}"
date: {format_iso(u.get('data', ''))}
image:
  path: "{image}"
tags: {fm_tags}
categories: {category}
permalink: {perm}
source_data: "gilmar-mendes-hc.json"
---

"""
    return fm + "\n".join(parts)

def to_lawfare_assunto(u: dict, category: str) -> dict:
    rel = POSTS / category / u["jekyll_filename"]
    fonte = str(rel.relative_to(ROOT)).replace("/", "\\")
    tags = u.get("jekyll_tags") or [category]
    fontes = [f.get("url") for f in u.get("fontes_verificadas") or [] if f.get("url")]
    return {
        "titulo": u["titulo"],
        "data_evento": u["jekyll_date"],
        "data_iso": format_iso(u["jekyll_date"]),
        "categoria": category,
        "tags": tags if isinstance(tags, list) else [tags],
        "descricao": u["resumo"],
        "relevancia": u.get("relevancia", "media"),
        "impacto_diplomatico": u.get("_impacto", "N/A"),
        "tipo_escandalo": u.get("_tipo", "N/A"),
        "fontes": fontes if fontes else ["N/A"],
        "pessoas_envolvidas": u.get("atores") or [],
        "instituicoes_envolvidas": u.get("instituicoes") or [],
        "pais": u.get("pais", "Brasil"),
        "valor_envolvido": u.get("valor_envolvido", "N/A"),
        "prioridade": u.get("prioridade", 2),
        "fonte_arquivo": fonte,
        "id": int(u["id_corpus"]),
    }

def main() -> int:
    # 1. Definir mapeamento de renumeração para Moraes/Transcooper
    # Próximo ID inicial disponível no main track é 1595.
    moraes_files = [
        ("lawfare-1512-1515-acronimo-moraes-pcc-transcooper.json", 1595),
        ("lawfare-1516-erosao-consenso-moraes.json", 1599),
        ("lawfare-1517-master-moraes-chokepoint.json", 1600),
    ]

    id_map = {
        1512: 1595,
        1513: 1596,
        1514: 1597,
        1515: 1598,
        1516: 1599,
        1517: 1600,
    }

    print("Mapeamento de IDs da Timeline:")
    for old, new in sorted(id_map.items()):
        print(f"  {old} -> {new}")

    # 2. Carregar e normalizar entradas Moraes/Transcooper
    normalized_moraes = []
    
    for fname, start_id in moraes_files:
        fpath = TODO / fname
        if not fpath.is_file():
            print(f"Aviso: arquivo {fname} não encontrado em todo/.")
            continue
            
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        items = data if isinstance(data, list) else (data.get("assuntos") or data.get("entries") or [data])
        
        for i, item in enumerate(items):
            old_id = int(item["id"])
            new_id = id_map[old_id]
            
            title = item.get("title") or item.get("titulo")
            jdate = item.get("date") or item.get("data_evento") or item.get("data_iso") or ""
            jdate = jdate[:10]
            resumo = item.get("summary") or item.get("descricao") or item.get("resumo") or ""
            
            cat = resolve_category(item)
            fname_slug = slugify(title)
            fname_md = f"{jdate}-{fname_slug}.md"
            
            # Atores
            actors = []
            for a in item.get("actors") or item.get("atores") or item.get("pessoas_envolvidas") or []:
                if isinstance(a, dict):
                    name = a.get("name") or a.get("nome", "")
                    role = a.get("role") or a.get("papel", "")
                    actors.append(f"{name} ({role})" if role else name)
                else:
                    actors.append(str(a))
            
            # Instituições
            inst = item.get("institutions") or item.get("instituicoes") or item.get("instituicoes_envolvidas") or []
            
            # Fontes
            fontes_raw = item.get("sources") or item.get("fontes") or []
            fontes = []
            for f_item in fontes_raw:
                if isinstance(f_item, dict):
                    fontes.append({
                        "titulo": f_item.get("title") or f_item.get("titulo") or f_item.get("veiculo") or "Fonte",
                        "url": f_item.get("url", ""),
                        "veiculo": f_item.get("outlet") or f_item.get("veiculo", ""),
                        "data": f_item.get("date") or f_item.get("data", "")
                    })
                elif f_item:
                    fontes.append({"titulo": "Fonte", "url": str(f_item)})
            
            # Conexões internas renumeradas
            conns = renumber_conn(item.get("connections") or item.get("conexoes") or [], id_map)
            
            note = f"Renumerado de {old_id} (conflito com Biazucci/crise diplomática no lawfare.json)."
            
            u = {
                "id_corpus": str(new_id),
                "id_original": old_id,
                "conflito_nota": note,
                "jekyll_filename": fname_md,
                "jekyll_date": jdate,
                "jekyll_categories": [cat],
                "jekyll_tags": build_tags(item, cat),
                "jekyll_permalink": f"/posts/{Path(fname_md).stem}/",
                "titulo": title,
                "resumo": resumo,
                "categoria": item.get("category") or item.get("categoria") or cat,
                "pais": item.get("pais", "Brasil"),
                "atores": actors,
                "instituicoes": inst,
                "fontes_verificadas": fontes,
                "padroes": item.get("patterns") or item.get("padroes") or [],
                "artigos_gosurf": item.get("artigos_gosurf") or [],
                "conexoes": conns,
                "dimensao_global": item.get("pais") in ("Global", "EUA") or item.get("dimensao_global", False),
                "relevancia": item.get("relevancia", "media"),
                "prioridade": item.get("prioridade", 1),
                "_analise": item.get("analise") or item.get("analytical_note") or "",
                "_result": item.get("result") or "",
                "_legal": item.get("legal_basis") or item.get("legal_refs") or [],
                "_lacunas": item.get("lacuna_investigativa") or [],
                "_source": fname,
            }
            normalized_moraes.append(u)

    print(f"Carregadas e renomeadas {len(normalized_moraes)} entradas da timeline.")

    # 3. Criar Posts Jekyll para Moraes/Transcooper
    for u in normalized_moraes:
        cat = u["jekyll_categories"][0]
        target = POSTS / cat / u["jekyll_filename"]
        target.parent.mkdir(parents=True, exist_ok=True)
        content = render_post_main(u)
        target.write_text(content, encoding="utf-8")
        print(f"Jekyll post criado (timeline): {target.relative_to(ROOT)}")

    # 4. Atualizar lawfare.json com Moraes/Transcooper
    with open(LAWFARE, "r", encoding="utf-8") as f:
        lf_data = json.load(f)
    assuntos = lf_data.get("assuntos", [])
    
    new_ids = {int(u["id_corpus"]) for u in normalized_moraes}
    assuntos = [a for a in assuntos if a.get("id") not in new_ids]
    
    for u in normalized_moraes:
        cat = u["jekyll_categories"][0]
        item = to_lawfare_assunto(u, cat)
        assuntos.append(item)
        
    assuntos.sort(key=lambda x: x.get("id") or 0)
    lf_data["assuntos"] = assuntos
    lf_data["total"] = len(assuntos)
    lf_data["data_extração"] = date.today().isoformat()
    
    datas = [a["data_evento"] for a in assuntos if a.get("data_evento") and a["data_evento"] != "0001-01-01"]
    if datas:
        lf_data["periodo"] = f"{min(datas)} a {max(datas)}"
        
    with open(LAWFARE, "w", encoding="utf-8") as f:
        json.dump(lf_data, f, ensure_ascii=False, indent=2)
    print(f"lawfare.json atualizado com as {len(normalized_moraes)} entradas da timeline.")

    # 5. Atualizar lawfare-unified-corpus.json com Moraes/Transcooper
    with open(UNIFIED, "r", encoding="utf-8") as f:
        uni_data = json.load(f)
    entradas = uni_data.get("entradas", [])
    entradas = [e for e in entradas if int(e.get("id_corpus", 0)) not in new_ids]
    
    for u in normalized_moraes:
        clean = {k: v for k, v in u.items() if not k.startswith("_")}
        clean["verificado"] = True
        clean["status_publicacao"] = "coberto_por_artigo"
        entradas.append(clean)
        
    entradas.sort(key=lambda x: int(x.get("id_corpus") or 0))
    uni_data["entradas"] = entradas
    
    with open(UNIFIED, "w", encoding="utf-8") as f:
        json.dump(uni_data, f, ensure_ascii=False, indent=2)
    print(f"lawfare-unified-corpus.json atualizado.")

    # 6. Processar Operação Sepse (thematic track T-210 a T-214)
    sepse_file = TODO / "lawfare-210-214-operacao-sepse.json"
    sepse_posts_count = 0
    if sepse_file.is_file():
        with open(sepse_file, "r", encoding="utf-8") as f:
            sepse_data = json.load(f)
        
        items = sepse_data.get("assuntos", [])
        for item in items:
            tid = int(item["id"])
            title = item["title"]
            jdate = item["date"][:10]
            
            slug = slugify(title)
            fname_md = f"{jdate}-{slug}.md"
            
            u = dict(item)
            u["jekyll_filename"] = fname_md
            u["jekyll_tags"] = ["estudo", "operacao-sepse"] + (item.get("patterns") or [])
            u["_source"] = sepse_file.name
            
            content = render_post_thematic(u)
            target = POSTS / "estudos" / fname_md
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            print(f"Jekyll post criado (estudo Sepse): {target.relative_to(ROOT)}")
            sepse_posts_count += 1
            
    # 6.5. Processar Compliance Zero (T-215, ex-T-210)
    compliance_file = TODO / "lawfare-T210-gilmar-compliance-zero-vorcaro.json"
    compliance_posts_count = 0
    if compliance_file.is_file():
        with open(compliance_file, "r", encoding="utf-8") as f:
            comp_data = json.load(f)
        
        items = comp_data.get("assuntos", [])
        for item in items:
            tid = 215 # Renomeado para evitar conflito com Sepse T-210
            title = item["title"]
            jdate = item["date"][:10]
            
            slug = slugify(title)
            fname_md = f"{jdate}-{slug}.md"
            
            u = dict(item)
            u["id"] = tid
            u["jekyll_filename"] = fname_md
            u["jekyll_tags"] = ["estudo", "compliance-zero", "gilmar-mendes"] + (item.get("patterns") or [])
            u["_source"] = compliance_file.name
            
            content = render_post_thematic(u)
            target = POSTS / "estudos" / fname_md
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            print(f"Jekyll post criado (estudo Compliance Zero T-215): {target.relative_to(ROOT)}")
            compliance_posts_count += 1
            
    # 7. Processar Habeas Corpus - Gilmar Mendes (decano)
    gilmar_file = TODO / "gilmar-mendes-hc.json"
    gilmar_posts_count = 0
    if gilmar_file.is_file():
        with open(gilmar_file, "r", encoding="utf-8") as f:
            gilmar_data = json.load(f)
            
        for year, events in gilmar_data.items():
            for ev in events:
                content = render_post_decano(ev)
                
                title = ev["titulo"]
                jdate = ev["data"][:10]
                slug = slugify(title)
                fname_md = f"{jdate}-{slug}.md"
                
                target = POSTS / "decano" / fname_md
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
                # print(f"Jekyll post criado (decano HC): {target.relative_to(ROOT)}")
                gilmar_posts_count += 1
        print(f"Criados {gilmar_posts_count} posts de Habeas Corpus do ministro Gilmar Mendes em _posts/decano/.")

    # 8. Atualizar claude.ai-corpus-ids-sync.json
    with open(SYNC, "r", encoding="utf-8") as f:
        sync_data = json.load(f)
        
    # Atualizar main track
    main_track = sync_data.setdefault("tracks", {}).setdefault("main", {})
    last_main_id = max(new_ids)
    main_track["last_confirmed"] = last_main_id
    main_track["last_jekyll_published"] = last_main_id
    main_track["last_session_produced"] = last_main_id
    main_track["last_id"] = last_main_id
    main_track["next_available"] = last_main_id + 1
    
    confirmed = main_track.setdefault("confirmed_batches", [])
    confirmed.append({
        "range": [min(new_ids), last_main_id],
        "status": "confirmed",
        "notes": f"Merge todo batches {date.today().isoformat()}: Acrônimo & Transcooper renumeração {min(new_ids)}-1600."
    })
    
    meta_main = sync_data.setdefault("_meta", {}).setdefault("tracks", {}).setdefault("main", {})
    meta_main["last_confirmed"] = last_main_id
    meta_main["last_jekyll_published"] = last_main_id
    meta_main["last_session_produced"] = last_main_id
    meta_main["id_range"] = f"1–{last_main_id} (confirmed)"
    
    # Atualizar thematic track
    thematic_track = sync_data.setdefault("tracks", {}).setdefault("thematic", {})
    thematic_track["last_id"] = 215
    thematic_track["next_available"] = 216
    
    # Adicionar nos thematic entries
    thematic_entries = thematic_track.setdefault("entries", [])
    
    # Remover duplicados da Sepse e do Compliance Zero
    sepse_tids = {210, 211, 212, 213, 214, 215}
    thematic_entries = [e for e in thematic_entries if int(e["id"]) not in sepse_tids]
    
    if sepse_file.is_file():
        with open(sepse_file, "r", encoding="utf-8") as f:
            sepse_data = json.load(f)
        for item in sepse_data.get("assuntos", []):
            tid = int(item["id"])
            title = item["title"]
            jdate = item["date"][:10]
            slug = slugify(title)
            fname_md = f"{jdate}-{slug}.md"
            thematic_entries.append({
                "id": tid,
                "status": "confirmed",
                "topic": f"{title[:50]}... (T-{tid})",
                "artifact": fname_md,
                "notes": f"Estudo Jekyll _posts/estudos/ ({fname_md[:-3]})."
            })
            
    if compliance_file.is_file():
        with open(compliance_file, "r", encoding="utf-8") as f:
            comp_data = json.load(f)
        for item in comp_data.get("assuntos", []):
            tid = 215
            title = item["title"]
            jdate = item["date"][:10]
            slug = slugify(title)
            fname_md = f"{jdate}-{slug}.md"
            thematic_entries.append({
                "id": tid,
                "status": "confirmed",
                "topic": f"{title[:50]}... (T-{tid})",
                "artifact": fname_md,
                "notes": f"Estudo Jekyll _posts/estudos/ ({fname_md[:-3]})."
            })
            
    thematic_entries.sort(key=lambda x: int(x["id"]))
    thematic_track["entries"] = thematic_entries
    
    meta_thematic = sync_data.setdefault("_meta", {}).setdefault("tracks", {}).setdefault("thematic", {})
    meta_thematic["last_confirmed"] = 215
    meta_thematic["id_range"] = "100–215"
    
    # Atualizar sync status
    sync_status = sync_data.setdefault("sync_status", {})
    sync_status["main_track_last_sync"] = date.today().isoformat()
    sync_status["thematic_track_last_sync"] = date.today().isoformat()
    sync_status["ids_confirmed_total"]["main_track"] = f"{last_main_id} (Jekyll + lawfare.json)"
    sync_status["ids_confirmed_total"]["thematic_track"] = 215
    
    # Limpar itens resolvidos da lista de open items
    open_items = sync_status.setdefault("open_items", [])
    open_items = [item for item in open_items if "1512" not in item and "1516" not in item and "1517" not in item and "Sepse" not in item and "210" not in item]
    sync_status["open_items"] = open_items
    
    with open(SYNC, "w", encoding="utf-8") as f:
        json.dump(sync_data, f, ensure_ascii=False, indent=2)
    print("claude.ai-corpus-ids-sync.json atualizado com sucesso.")
 
    # 9. Arquivar arquivos processados em processados/
    PROC.mkdir(parents=True, exist_ok=True)
    all_files = [f[0] for f in moraes_files] + ["lawfare-210-214-operacao-sepse.json", "lawfare-T210-gilmar-compliance-zero-vorcaro.json", "gilmar-mendes-hc.json"]
    for fname in all_files:
        src = TODO / fname
        if src.is_file():
            dst = PROC / fname
            shutil.move(src, dst)
            print(f"Arquivado: todo/{fname} -> processados/{fname}")
 
    print("\nSincronização editorial e geração de posts Jekyll concluídas!")
    return 0
 
if __name__ == "__main__":
    import sys
    sys.exit(main())
