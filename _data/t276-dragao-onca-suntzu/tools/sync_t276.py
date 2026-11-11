#!/usr/bin/env python3
"""
sync_t276.py — aplica o patch do capítulo T-276 (O Dragão e a Onça · Sun Tzu)
no repositório lawfare-timeline.

O que faz:
  1. Lê o lawfare.json ATUAL (o do Drive/local, não o do patch) e calcula max_id.
  2. Renumera as 7 entradas main do patch (provisórias 1986-1992) para max_id+1...
     e reescreve as referências (id_NNNN, connections, links de post) no patch,
     no capítulo HTML e no post T-276.
  3. Gera fonte_arquivo de cada entrada com a mesma regra de slug do repo.
  4. Acrescenta as entradas ao lawfare.json e ao dragao-onca.json (+ T-276),
     atualiza totais, id_ranges, thematic_order, o .yml de ordem temática e o
     manifesto claude.ai-corpus-ids-sync.json.
  5. Copia dragao-onca-suntzu.html e o post T-276 para o repo e, com
     --update-nav, insere o card do capítulo 19 na navegação dos demais
     capítulos dragao-onca-*.html.

Uso (rodar a partir da pasta do pacote t276):
  python tools/sync_t276.py --repo D:\\_deploy\\lawfare-timeline --dry-run
  python tools/sync_t276.py --repo D:\\_deploy\\lawfare-timeline --lawfare C:\\Downloads\\lawfare.json --update-nav

--lawfare: caminho do lawfare.json mais recente (ex.: o baixado do Drive).
           Se omitido, usa <repo>/_data/lawfare.json. O arquivo atualizado é
           sempre gravado em <repo>/_data/lawfare.json.
Antes de gravar, cria cópias .bak-t276 de cada arquivo alterado.
"""
import argparse, json, re, shutil, sys, unicodedata
from datetime import date
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
PATCH = PKG / "_data" / "patch-t276-dragao-onca-suntzu.json"
CHAPTER = PKG / "dragao-onca-suntzu.html"
POST = PKG / "_posts" / "dragao-onca" / "2026-11-11-t276-dragao-onca-suntzu.md"
THEMATIC_ID = 276
TODAY = date.today().isoformat()

NAV_CARD = ('    <a class="series-card" href="/dragao-onca-suntzu.html"><div class="series-card-id">'
            '19 · T-276 · Prospectivo</div><div class="series-card-chapter">⚔️ Sun Tzu — vencer sem lutar'
            '</div><div class="series-card-desc">Janela de 33 dias pós-Lava Jato · 4 cenários</div></a>\n')


def slug(title: str) -> str:
    t = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode().lower()
    t = re.sub(r"[^a-z0-9\s-]", "", t)
    t = re.sub(r"\s+", "-", t.strip())
    t = re.sub(r"-+", "-", t)
    return t[:80].rstrip("-")


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def dump(p, obj, dry):
    p = Path(p)
    if dry:
        print(f"  [dry-run] gravaria {p}")
        return
    if p.exists():
        shutil.copy2(p, p.with_name(p.name + ".bak-t276"))
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  gravado {p}")


def write_text(p, text, dry):
    p = Path(p)
    if dry:
        print(f"  [dry-run] gravaria {p}")
        return
    if p.exists():
        shutil.copy2(p, p.with_name(p.name + ".bak-t276"))
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print(f"  gravado {p}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--lawfare", default=None)
    ap.add_argument("--update-nav", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    repo = Path(a.repo)
    data = repo / "_data"
    src_lawfare = Path(a.lawfare) if a.lawfare else data / "lawfare.json"
    patch = load(PATCH)
    lawfare = load(src_lawfare)
    dragao = load(data / "dragao-onca.json")

    # ---------- 1. calcular IDs ----------
    ids = [e["id"] for e in lawfare["assuntos"] if isinstance(e.get("id"), int)]
    max_id = max(ids)
    old_ids = [e["id"] for e in patch["main"]]
    start = max_id + 1
    mapping = {old: start + i for i, old in enumerate(sorted(old_ids))}
    print(f"lawfare.json: {len(ids)} entradas, max_id={max_id}")
    print("renumeração:", ", ".join(f"{o}->{n}" for o, n in mapping.items()))

    if any(e.get("id") == THEMATIC_ID and e.get("track") == "thematic" for e in dragao["assuntos"]):
        sys.exit("ERRO: T-276 já existe em dragao-onca.json — abortando.")
    titles = {e.get("titulo") for e in lawfare["assuntos"]}
    dup = [e["titulo"] for e in patch["main"] if e["titulo"] in titles]
    if dup:
        sys.exit(f"ERRO: entradas já presentes no lawfare.json: {dup}")

    def remap_text(s: str) -> str:
        def rep(m):
            n = int(m.group(2))
            return f"{m.group(1)}{mapping.get(n, n)}"
        s = re.sub(r"(id_|id)(\d{4})\b", rep, s)
        lo, hi = min(mapping), max(mapping)
        s = s.replace(f"{lo}-{hi}", f"{mapping[lo]}-{mapping[hi]}")
        s = s.replace(f"{lo}–{hi}", f"{mapping[lo]}–{mapping[hi]}")
        # células "<td>1986</td>" da tabela de fontes (passagem única, sem encadear)
        s = re.sub(r"<td>(\d{4})</td>",
                   lambda m: f"<td>{mapping.get(int(m.group(1)), int(m.group(1)))}</td>", s)
        return s

    def remap_obj(o):
        if isinstance(o, str):
            return remap_text(o)
        if isinstance(o, list):
            return [remap_obj(x) for x in o]
        if isinstance(o, dict):
            out = {}
            for k, v in o.items():
                if k == "id" and isinstance(v, int):
                    out[k] = mapping.get(v, v)
                elif k == "connections":
                    out[k] = [mapping.get(x, x) for x in v]
                else:
                    out[k] = remap_obj(v)
            return out
        return o

    main_entries = [remap_obj(e) for e in patch["main"]]
    thematic = remap_obj(patch["thematic"])

    post_paths = {}
    for e in main_entries:
        stem = f"{e['data_evento']}-id{e['id']}-{slug(e['titulo'])}"
        e["fonte_arquivo"] = f"_posts\\dragao-onca\\{stem}.md"
        post_paths[e["id"]] = f"/posts/{stem}/"

    # ---------- 2. lawfare.json ----------
    lawfare["assuntos"].extend(main_entries)
    if "total" in lawfare:
        lawfare["total"] = len(lawfare["assuntos"])
    if "data_extração" in lawfare:
        lawfare["data_extração"] = TODAY
    dump(data / "lawfare.json", lawfare, a.dry_run)

    # ---------- 3. dragao-onca.json ----------
    for e in main_entries:
        d = dict(e); d["track"] = "main"
        dragao["assuntos"].append(d)
    dragao["assuntos"].append(thematic)
    a_ = dragao["assuntos"]
    dragao["total"] = len(a_)
    dragao["total_main"] = sum(1 for e in a_ if e.get("track") == "main")
    dragao["total_thematic"] = sum(1 for e in a_ if e.get("track") == "thematic")
    dragao["data_extracao"] = TODAY
    rng = dragao.setdefault("id_ranges", {})
    rng.setdefault("main", {})["max"] = max(e["id"] for e in a_ if e.get("track") == "main")
    rng["main"]["next"] = rng["main"]["max"] + 1
    rng.setdefault("thematic", {})["max"] = THEMATIC_ID
    rng["thematic"]["next"] = THEMATIC_ID + 1
    if THEMATIC_ID not in dragao.get("thematic_order", []):
        dragao.setdefault("thematic_order", []).append(THEMATIC_ID)
    lo, hi = mapping[min(mapping)], mapping[max(mapping)]
    dragao["nota"] = (dragao.get("nota", "") +
                      f" · {TODAY}: capítulo 19 Sun Tzu (T-276) + main {lo}-{hi}.").strip()
    dump(data / "dragao-onca.json", dragao, a.dry_run)

    # ---------- 4. ordem temática (.yml) ----------
    yml = data / "dragao_onca_thematic_order.yml"
    if yml.exists():
        y = yml.read_text(encoding="utf-8")
        if not re.search(r"^\s*-\s*276\b", y, re.M):
            y = y.rstrip("\n") + "\n  - 276  # Sun Tzu — Prospectivo (janela 33 dias + cenários)\n"
            write_text(yml, y, a.dry_run)

    # ---------- 5. manifesto de IDs ----------
    man_p = data / "claude.ai-corpus-ids-sync.json"
    if man_p.exists():
        man = load(man_p)
        tm, tt = man["tracks"]["main"], man["tracks"]["thematic"]
        prev_t = tt.get("last_confirmed")
        if prev_t not in (275, None):
            print(f"  AVISO: manifesto registra thematic last_confirmed={prev_t}; "
                  "T-275 não consta. Verifique se T-275 foi registrado em outro arquivo.")
        tm.setdefault("confirmed_batches", []).append(
            {"range": [lo, hi], "status": "confirmed",
             "notes": f"{TODAY}: Dragão e a Onça cap. 19 Sun Tzu (T-276)."})
        for k in ("last_id", "last_jekyll_published", "last_confirmed"):
            tm[k] = hi
        tm["next_available"] = hi + 1
        tt.setdefault("entries", []).append(
            {"id": THEMATIC_ID, "status": "confirmed",
             "topic": "T-276 Dragão e a Onça — Sun Tzu: vencer sem lutar",
             "artifact": "2026-11-11-t276-dragao-onca-suntzu.md",
             "notes": f"dragao-onca-suntzu.html · main {lo}-{hi}"})
        tt["last_id"] = tt["last_confirmed"] = THEMATIC_ID
        tt["next_available"] = THEMATIC_ID + 1
        man["last_main_id"] = hi
        man["next_available"] = hi + 1
        man["updated"] = TODAY
        meta = man["_meta"]
        meta["updated"] = TODAY
        mt = meta["tracks"]
        mt["main"].update({"last_confirmed": hi, "last_jekyll_published": hi,
                           "id_range": f"1–{hi} (confirmed)",
                           "notes": f"lawfare.json confirmado até {hi}. Próximo ID livre: {hi + 1}."})
        mt["thematic"].update({"last_confirmed": THEMATIC_ID, "last_session_produced": THEMATIC_ID,
                               "id_range": f"100–{THEMATIC_ID}",
                               "notes": f"T-{THEMATIC_ID} confirmado. Próximo thematic livre: T-{THEMATIC_ID + 1}."})
        ss = man.get("sync_status", {})
        ss["main_track_last_sync"] = ss["thematic_track_last_sync"] = TODAY
        ss["dragao_onca_series_sync"] = TODAY
        dump(man_p, man, a.dry_run)

    # ---------- 6. capítulo HTML e post ----------
    def fix_links(s):
        for n, path in post_paths.items():
            s = re.sub(rf"/posts/\d{{4}}-\d{{2}}-\d{{2}}-id{n}/", path, s)
        return s

    post = POST.read_text(encoding="utf-8")
    # links curtos do post usam os IDs provisórios: remapear primeiro, depois expandir
    post = fix_links(remap_text(post))
    write_text(repo / "_posts" / "dragao-onca" / POST.name, post, a.dry_run)

    html = remap_text(CHAPTER.read_text(encoding="utf-8"))
    write_text(repo / CHAPTER.name, html, a.dry_run)

    # ---------- 7. navegação dos demais capítulos ----------
    if a.update_nav:
        for f in sorted(repo.glob("dragao-onca-*.html")):
            if f.name == CHAPTER.name:
                continue
            h = f.read_text(encoding="utf-8")
            if "dragao-onca-suntzu.html" in h or 'class="series-hub"' not in h:
                continue
            new = re.sub(r'(\n)(\s*</div>\s*<a class="series-hub")',
                         lambda m: m.group(1) + NAV_CARD + m.group(2).lstrip("\n"), h, count=1)
            if new != h:
                write_text(f, new, a.dry_run)

    # ---------- 8. validação ----------
    if not a.dry_run:
        for p in (data / "lawfare.json", data / "dragao-onca.json"):
            json.loads(p.read_text(encoding="utf-8"))
        print("JSON válido.")
    print(f"\nPronto: main {lo}-{hi} · T-{THEMATIC_ID}. Próximos livres: {hi + 1} · T-{THEMATIC_ID + 1}.")


if __name__ == "__main__":
    main()
