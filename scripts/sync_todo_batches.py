#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sincroniza os batches pendentes de _data/todo/ com o corpus e publica posts Jekyll.
Mapeia os IDs conflitantes sequencialmente a partir de 1577.
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
}

def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")[:90]

def yaml_escape(s: str) -> str:
    return s.replace('"', '\\"')

def format_iso(d: str) -> str:
    return f"{(d or '2026-01-01')[:10]}T12:00:00.000Z"

def resolve_category(entry: dict) -> str:
    if entry.get("jekyll_categories"):
        c = entry["jekyll_categories"]
        return c[0] if isinstance(c, list) else str(c)

    titulo = (entry.get("titulo") or entry.get("title") or "").lower()
    cat = (entry.get("categoria") or entry.get("category") or "").lower()
    tags = [str(t).lower() for t in entry.get("tags") or []]

    mapping = {
        "captura-institucional": "escandalos",
        "conflito-de-interesses": "escandalos",
        "crise-diplomatica": "crise-diplomatica",
        "incidente_diplomatico": "crise-diplomatica",
        "censura-digital": "lawfare",
        "judicial": "justica",
        "documentado": "escandalos",
        "operacao": "operacoes",
        "operacoes": "operacoes",
    }
    if cat in mapping:
        return mapping[cat]

    if "crise-diplomatica" in cat or "crise-diplomatica" in tags:
        return "crise-diplomatica"
    if any(k in cat for k in ("stf", "moraes", "supremo")):
        return "stf"
    if "operacao" in cat or "operacao" in tags:
        return "operacoes"
    if cat == "judicial":
        return "justica"
    return "escandalos"

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
        m = re.search(r'\d+', str(c))
        if m:
            old_num = int(m.group(0))
            if old_num in id_map:
                new_num = id_map[old_num]
                new_conns.append(str(c).replace(str(old_num), str(new_num)))
            else:
                new_conns.append(str(c))
        else:
            new_conns.append(str(c))
    return new_conns

def render_post(u: dict) -> str:
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
    if u.get("_conexoes"):
        parts.extend(["## Conexões no corpus", ""] + [f"- {c}" for c in u["_conexoes"]] + [""])
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
        "fontes": fontes,
        "pessoas_envolvidas": u.get("atores") or [],
        "instituicoes_envolvidas": u.get("instituicoes") or [],
        "pais": u.get("pais", "Brasil"),
        "valor_envolvido": u.get("valor_envolvido", "N/A"),
        "prioridade": u.get("prioridade", 2),
        "fonte_arquivo": fonte,
        "id": int(u["id_corpus"]),
    }

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    # 1. Definir arquivos e mapeamento de IDs
    # IDs 1511-1576 já estão ocupados no lawfare.json canônico.
    # Próximo ID inicial é 1577.
    files_to_sync = [
        ("lawfare-1525-1531-pt-pcc-p04b-retroativo.json", 1577),
        ("lawfare-1532-1537-contexto-fto-internacional.json", 1584),
        ("lawfare-1572-1576-bloqueio-internet.json", 1590),
    ]

    id_map = {}
    
    # Gerar o mapeamento completo primeiro
    for fname, start_id in files_to_sync:
        fpath = TODO / fname
        if not fpath.is_file():
            print(f"Erro: arquivo {fpath} não encontrado.")
            return 1
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            items = data
        else:
            items = data.get("entries") or data.get("assuntos") or []
        for i, item in enumerate(items):
            old_id = item.get("id")
            if old_id is not None:
                id_map[int(old_id)] = start_id + i

    print("Mapeamento de IDs gerado:")
    for old, new in sorted(id_map.items()):
        print(f"  {old} -> {new}")

    # 2. Carregar e processar entradas
    normalized_entries = []
    
    for fname, start_id in files_to_sync:
        fpath = TODO / fname
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            items = data
        else:
            items = data.get("entries") or data.get("assuntos") or []

        for i, item in enumerate(items):
            old_id = item.get("id")
            new_id = id_map[int(old_id)]
            
            # Normalizar campos
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
            for f in fontes_raw:
                if isinstance(f, dict):
                    fontes.append({
                        "titulo": f.get("title") or f.get("titulo") or f.get("veiculo") or "Fonte",
                        "url": f.get("url", ""),
                        "veiculo": f.get("outlet") or f.get("veiculo", ""),
                        "data": f.get("date") or f.get("data", "")
                    })
                elif f:
                    fontes.append({"titulo": "Fonte", "url": str(f)})

            # Conexões internas
            conns = renumber_conn(item.get("connections") or item.get("conexoes") or [], id_map)

            note = f"Renumerado de {old_id} (evitando conflitos com Biomm/Flávio Bolsonaro no lawfare.json)."

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
                "prioridade": item.get("prioridade", 2),
                "_analise": item.get("analise") or item.get("analytical_note") or "",
                "_result": item.get("result") or "",
                "_legal": item.get("legal_basis") or item.get("legal_refs") or [],
                "_lacunas": item.get("lacuna_investigativa") or [],
                "_source": fname,
            }
            normalized_entries.append(u)

    print(f"\nCarregadas e normalizadas {len(normalized_entries)} entradas.")

    if args.dry_run:
        print("\n[DRY-RUN] Entradas a serem geradas:")
        for u in normalized_entries:
            print(f"  ID {u['id_corpus']}: {u['titulo']} ({u['jekyll_filename']}) under {u['jekyll_categories'][0]}")
        return 0

    # 3. Gerar Jekyll Posts
    written_posts = 0
    for u in normalized_entries:
        cat = u["jekyll_categories"][0]
        target = POSTS / cat / u["jekyll_filename"]
        target.parent.mkdir(parents=True, exist_ok=True)
        content = render_post(u)
        target.write_text(content, encoding="utf-8")
        print(f"Jekyll post criado: {target.relative_to(ROOT)}")
        written_posts += 1

    # 4. Atualizar lawfare.json
    with open(LAWFARE, "r", encoding="utf-8") as f:
        lf_data = json.load(f)
    assuntos = lf_data.get("assuntos", [])
    
    # Remover duplicados se existirem por ID para segurança
    new_ids = {int(u["id_corpus"]) for u in normalized_entries}
    assuntos = [a for a in assuntos if a.get("id") not in new_ids]
    
    # Adicionar novos
    for u in normalized_entries:
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
    print(f"\nlawfare.json atualizado com {len(normalized_entries)} novos assuntos (total {len(assuntos)}).")

    # 5. Atualizar lawfare-unified-corpus.json
    with open(UNIFIED, "r", encoding="utf-8") as f:
        uni_data = json.load(f)
    entradas = uni_data.get("entradas", [])
    
    # Remover duplicados
    entradas = [e for e in entradas if int(e.get("id_corpus", 0)) not in new_ids]
    
    # Adicionar novos
    for u in normalized_entries:
        clean = {k: v for k, v in u.items() if not k.startswith("_")}
        clean["verificado"] = True
        clean["status_publicacao"] = "coberto_por_artigo"
        clean["id_original"] = u["id_original"]
        clean["id_corpus"] = u["id_corpus"]
        clean["conflito_nota"] = u["conflito_nota"]
        entradas.append(clean)
        
    entradas.sort(key=lambda x: int(x.get("id_corpus") or 0))
    uni_data["entradas"] = entradas
    
    with open(UNIFIED, "w", encoding="utf-8") as f:
        json.dump(uni_data, f, ensure_ascii=False, indent=2)
    print(f"lawfare-unified-corpus.json atualizado com {len(normalized_entries)} novas entradas.")

    # 6. Atualizar claude.ai-corpus-ids-sync.json
    with open(SYNC, "r", encoding="utf-8") as f:
        sync_data = json.load(f)
        
    main_track = sync_data.setdefault("tracks", {}).setdefault("main", {})
    last_id = max(new_ids)
    main_track["last_confirmed"] = last_id
    main_track["last_jekyll_published"] = last_id
    main_track["last_session_produced"] = last_id
    main_track["last_id"] = last_id
    main_track["next_available"] = last_id + 1
    
    # Adicionar nos confirmed_batches
    confirmed = main_track.setdefault("confirmed_batches", [])
    min_id = min(new_ids)
    confirmed.append({
        "range": [min_id, last_id],
        "status": "confirmed",
        "notes": f"Merge todo batches {date.today().isoformat()}: retroativo {min_id}-1583; fto {1584}-1589; bloqueio-internet {1590}-{last_id}."
    })
    
    # Atualizar meta
    meta_main = sync_data.setdefault("_meta", {}).setdefault("tracks", {}).setdefault("main", {})
    meta_main["last_confirmed"] = last_id
    meta_main["last_jekyll_published"] = last_id
    meta_main["last_session_produced"] = last_id
    meta_main["id_range"] = f"1–{last_id} (confirmed)"
    
    # Atualizar sync_status
    sync_status = sync_data.setdefault("sync_status", {})
    sync_status["main_track_last_sync"] = date.today().isoformat()
    sync_status["ids_confirmed_total"]["main_track"] = f"{last_id} (Jekyll + lawfare.json)"
    
    # Remover nota do open_items se houver
    open_items = sync_status.setdefault("open_items", [])
    open_items = [item for item in open_items if "1525" not in item and "1532" not in item and "1572" not in item]
    sync_status["open_items"] = open_items
    
    with open(SYNC, "w", encoding="utf-8") as f:
        json.dump(sync_data, f, ensure_ascii=False, indent=2)
    print(f"claude.ai-corpus-ids-sync.json atualizado. Próximo disponível: {last_id + 1}.")

    # 7. Mover arquivos JSON processados para processados/
    PROC.mkdir(parents=True, exist_ok=True)
    for fname, _ in files_to_sync:
        src = TODO / fname
        dst = PROC / fname
        shutil.move(src, dst)
        print(f"Arquivado: todo/{fname} -> processados/{fname}")
        
    # Mover consolidado também
    cons_file = "lawfare-consolidado-1518-1572.json"
    src_cons = TODO / cons_file
    if src_cons.is_file():
        dst_cons = PROC / cons_file
        shutil.move(src_cons, dst_cons)
        print(f"Arquivado: todo/{cons_file} -> processados/{cons_file}")

    print("\nSincronização concluída com sucesso!")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
