#!/usr/bin/env python3
"""
archive_org_mirror.py
Submete URLs do lawfare-timeline ao Wayback Machine (archive.org SavePageNow).

Uso:
  python tools/archive_org_mirror.py             # dry-run (lista URLs, não envia)
  python tools/archive_org_mirror.py --submit    # envia ao archive.org
  python tools/archive_org_mirror.py --submit --delay 5  # 5s entre requests

Requer: requests  (pip install requests)

Referência API: https://archive.org/help/wayback_api.php
"""
from __future__ import annotations

import argparse
import io
import json
import sys
import time
from pathlib import Path
from datetime import date

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "_posts"
LOG_FILE = ROOT / "_data" / "archive_org_log.json"

BASE_URL = "https://lawfare-timeline.vercel.app"
SAVEPAGENOW_URL = "https://web.archive.org/save/"

# Categorias Jekyll → prefixo URL
# Os posts usam permalink /posts/<slug>/ conforme _config.yml
SKIP_EXTENSIONS = {".bak"}


def collect_post_urls() -> list[dict]:
    """Coleta todos os posts .md e constrói as URLs canônicas."""
    urls = []
    for md in sorted(POSTS_DIR.rglob("*.md")):
        if md.suffix in SKIP_EXTENSIONS:
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        # Extrair permalink do front matter, se existir
        permalink = None
        in_front_matter = False
        for line in text.splitlines():
            if line.strip() == "---":
                in_front_matter = not in_front_matter
                continue
            if in_front_matter and line.startswith("permalink:"):
                permalink = line.split(":", 1)[1].strip().strip('"').strip("'")
                break
        if permalink:
            url = BASE_URL + permalink.rstrip("/") + "/"
        else:
            # Slug a partir do nome do arquivo sem data
            stem = md.stem
            # Remove prefixo YYYY-MM-DD-
            parts = stem.split("-")
            if len(parts) > 3:
                try:
                    int(parts[0]); int(parts[1]); int(parts[2])
                    slug = "-".join(parts[3:])
                except ValueError:
                    slug = stem
            else:
                slug = stem
            url = f"{BASE_URL}/posts/{slug}/"
        urls.append({"file": str(md.relative_to(ROOT)), "url": url})
    return urls


def load_log() -> dict:
    if LOG_FILE.exists():
        return json.loads(LOG_FILE.read_text(encoding="utf-8"))
    return {"archived": [], "failed": [], "last_run": None}


def save_log(log: dict) -> None:
    LOG_FILE.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")


def submit_url(session, url: str) -> tuple[bool, str]:
    """Envia URL ao SavePageNow. Retorna (sucesso, job_id/mensagem)."""
    try:
        import requests as req
    except ImportError:
        print("  [ERRO] requests não instalado. Execute: pip install requests")
        sys.exit(1)

    try:
        resp = session.post(
            SAVEPAGENOW_URL + url,
            headers={
                "User-Agent": "lawfare-timeline-archiver/1.0 (contact: github.com/araguaci/lawfare-timeline)",
                "Accept": "application/json",
            },
            timeout=30,
        )
        if resp.status_code == 200:
            data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
            job_id = data.get("job_id", "ok")
            return True, job_id
        else:
            return False, f"HTTP {resp.status_code}"
    except Exception as exc:
        return False, str(exc)


def main() -> None:
    parser = argparse.ArgumentParser(description="archive.org mirror para lawfare-timeline")
    parser.add_argument("--submit", action="store_true", help="Enviar ao archive.org (sem flag = dry-run)")
    parser.add_argument("--delay", type=float, default=3.0, help="Segundos entre requests (padrão: 3)")
    parser.add_argument("--skip-archived", action="store_true", help="Pular URLs já arquivadas no log")
    args = parser.parse_args()

    print("=== archive_org_mirror — lawfare-timeline ===")
    print(f"  Modo: {'SUBMIT (enviando ao archive.org)' if args.submit else 'DRY-RUN'}")
    print(f"  Site: {BASE_URL}")
    print(f"  Delay: {args.delay}s\n")

    urls = collect_post_urls()
    # Adicionar URL raiz e índice
    extras = [
        {"file": "index", "url": BASE_URL + "/"},
        {"file": "posts-index", "url": BASE_URL + "/posts/"},
    ]
    all_targets = extras + urls
    print(f"  Total URLs identificadas: {len(all_targets)}")

    log = load_log()
    already_done = set(log.get("archived", []))

    if args.skip_archived:
        pending = [t for t in all_targets if t["url"] not in already_done]
        print(f"  URLs pendentes (não arquivadas): {len(pending)}")
    else:
        pending = all_targets
        print(f"  URLs a processar: {len(pending)}")

    if not args.submit:
        print("\n  Prévia das primeiras 20 URLs:")
        for t in pending[:20]:
            status = "✓ já arquivada" if t["url"] in already_done else "→ pendente"
            print(f"    {status} {t['url']}")
        if len(pending) > 20:
            print(f"    ... e mais {len(pending) - 20} URLs")
        print("\n  [DRY-RUN] Use --submit para enviar ao archive.org")
        print(f"\n  Estimativa de tempo: {len(pending) * args.delay / 60:.1f} min ({len(pending)} URLs × {args.delay}s)")
        return

    # --- Submit ---
    try:
        import requests
        session = requests.Session()
    except ImportError:
        print("  [ERRO] requests não instalado. Execute: pip install requests")
        sys.exit(1)

    success_count = 0
    fail_count = 0
    newly_archived = []
    failed = []

    for i, target in enumerate(pending, 1):
        url = target["url"]
        print(f"  [{i:3}/{len(pending)}] {url} ... ", end="", flush=True)
        ok, msg = submit_url(session, url)
        if ok:
            print(f"OK ({msg})")
            success_count += 1
            newly_archived.append(url)
        else:
            print(f"FALHOU ({msg})")
            fail_count += 1
            failed.append({"url": url, "error": msg, "date": date.today().isoformat()})
        if i < len(pending):
            time.sleep(args.delay)

    # Atualizar log
    log["archived"] = list(set(log.get("archived", []) + newly_archived))
    log["failed"] = failed
    log["last_run"] = date.today().isoformat()
    log["stats"] = {
        "total": len(all_targets),
        "archived": len(log["archived"]),
        "last_batch_success": success_count,
        "last_batch_failed": fail_count,
    }
    save_log(log)
    print(f"\n  Resultado: {success_count} enviados, {fail_count} falhas")
    print(f"  Log salvo: {LOG_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
