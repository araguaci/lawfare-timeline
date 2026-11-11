#!/usr/bin/env python3
"""
Protocolo de Preservação 8/jan / INQ 4.781 — lawfare-timeline (CC0 1.0)

Lê inventario-fontes-8jan-inq4781.json e, para cada URL:
  1. Baixa o conteúdo original e calcula SHA-256 (cópia local em ./acervo/).
  2. Pede snapshot ao Wayback Machine (Save Page Now) e registra a URL do snapshot.
  3. Grava o resultado de volta no inventário (wayback_snapshot, sha256, arquivado_em).

Uso:  python preservar_fontes.py [--inventario ARQ] [--so-oficiais] [--pausa 6]
Só biblioteca padrão. Rode na sua máquina (o Wayback limita ~1 pedido a cada 5 s).
archive.today exige captcha: fica manual para as fontes oficiais_primarias.
"""
import argparse, hashlib, json, os, re, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone

UA = "lawfare-timeline-preservacao/1.0 (+https://lawfare-timeline.vercel.app)"

def baixar(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers.get("Content-Type", "")

def wayback(url, timeout=120):
    req = urllib.request.Request("https://web.archive.org/save/" + url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            loc = r.headers.get("Content-Location") or r.geturl()
            if loc.startswith("/"):
                loc = "https://web.archive.org" + loc
            return loc
    except urllib.error.HTTPError as e:
        return f"ERRO_HTTP_{e.code}"
    except Exception as e:  # noqa
        return f"ERRO_{type(e).__name__}"

def nome_arquivo(url, ctype):
    base = re.sub(r"[^A-Za-z0-9._-]+", "_", url.split("://", 1)[-1])[:120]
    ext = ".pdf" if "pdf" in ctype else ".html"
    return base if base.endswith(ext) else base + ext

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventario", default="inventario-fontes-8jan-inq4781.json")
    ap.add_argument("--so-oficiais", action="store_true")
    ap.add_argument("--pausa", type=float, default=6.0)
    a = ap.parse_args()

    inv = json.load(open(a.inventario, encoding="utf-8"))
    os.makedirs("acervo", exist_ok=True)
    feitos = 0
    for ent in inv["entradas"]:
        alvos = [f for f in ent["fontes"] if f.get("url")]
        # fontes que só existem no .md do post entram como pendentes
        for u in ent.get("urls_no_post", []):
            if not any(f.get("url") == u for f in alvos):
                f = {"url": u, "tipo": "post_md", "wayback_snapshot": None, "sha256": None, "arquivado_em": None}
                ent["fontes"].append(f); alvos.append(f)
        for f in alvos:
            if f.get("sha256") and f.get("wayback_snapshot", "").startswith("http"):
                continue
            if a.so_oficiais and f.get("tipo") != "oficial_primaria":
                continue
            url = f["url"]
            print(f"[{ent['id']}] {url}", flush=True)
            try:
                corpo, ctype = baixar(url)
                f["sha256"] = hashlib.sha256(corpo).hexdigest()
                with open(os.path.join("acervo", nome_arquivo(url, ctype)), "wb") as fh:
                    fh.write(corpo)
            except Exception as e:  # noqa
                f["sha256"] = None
                f["erro_download"] = f"{type(e).__name__}: {e}"[:200]
            f["wayback_snapshot"] = wayback(url)
            f["arquivado_em"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
            feitos += 1
            json.dump(inv, open(a.inventario, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            time.sleep(a.pausa)
    inv["_meta"]["estado_preservacao"] = f"rodada {datetime.now(timezone.utc).date()} — {feitos} URLs processadas"
    json.dump(inv, open(a.inventario, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"OK — {feitos} URLs processadas. Hashes e snapshots gravados no inventário.")

if __name__ == "__main__":
    sys.exit(main())
