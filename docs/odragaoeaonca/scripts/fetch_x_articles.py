#!/usr/bin/env python3
"""
Gap analysis: artigos/*-xarticle.md vs Articles publicados em X (@username).

Uso:
  python scripts/fetch_x_articles.py --username araguaci
  python scripts/fetch_x_articles.py --username araguaci --annotate

Env (.env na raiz do projeto):
  X_API_BEARER_TOKEN ou X_BEARER_TOKEN  — Bearer app-only
  X_ACCESS_TOKEN                        — OAuth user context (preferido / owned reads)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Optional
try:
    import requests
except ImportError:
    print("Instale deps: pip install -r scripts/requirements-x-articles.txt", file=sys.stderr)
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
ARTIGOS = ROOT / "artigos"
DEFAULT_OUT = ARTIGOS / "publication-status.md"
DEFAULT_MAP = ARTIGOS / "published-map.json"
MIRROR_DIR = ARTIGOS / "_published"
API = "https://api.x.com/2"

# Fingerprints por slug (T-ID, UF, termos únicos do H1 / tese)
FINGERPRINTS: dict[str, list[str]] = {
    "odragaoeaonca-xarticle": ["o dragao e a onca", "soberania mineral", "t-228", "oito capitulos"],
    "brasil-federal-xarticle": ["brasil-china desde 1993", "t-229", "parceria estrategica", "doria"],
    "braco-diplomatico-xarticle": ["waico", "serra verde", "t-236", "alinhamento", "terras raras aos eua"],
    "sao-paulo-xarticle": ["sao paulo", "crrc", "cofco", "t-238", "material rodante"],
    "goias-xarticle": ["goias", "caiado", "t-228", "serra verde", "washington em 18"],
    "minas-gerais-xarticle": ["minas gerais", "sigma", "t-232", "mecanismo", "nao e a china"],
    "bahia-xarticle": ["bahia", "jeronimo", "xi jinping", "tir", "10,88", "t-237"],
    "para-xarticle": ["para", "ferrovia", "cop30", "39 mortes", "t-230", "cccc"],
    "amazonas-xarticle": ["amazonas", "taboca", "waimiri", "t-231", "12,3"],
    "parana-xarticle": ["parana", "tcp", "cmport", "t-239", "acordos gemeos"],
    "rio-grande-do-sul-xarticle": ["rio grande do sul", "ceee", "gwm", "t-240", "rede eletrica"],
    "rs-es-ranking-xarticle": ["ranking cebc", "rs perdeu", "es ganhou", "t-241", "t-242", "85,5"],
    "sintese-xarticle": ["onde a tese confirma", "enfraquece e falha", "t-233", "r$81"],
    "pl2780-xarticle": ["pl 2.780", "pl 2780", "fgam", "inesc", "t-235"],
    "braco-juridico-xarticle": ["braco juridico", "marco temporal", "adi 7919", "t-234"],
    "sintese-final-xarticle": ["testada em", "tipologia", "t-243", "soberania na conta"],
    "amapa-xarticle": ["amapa", "amazonbai", "chevron", "cnpc", "t-244", "acai"],
    "rj-xarticle": ["rio de janeiro", "acu", "hikvision", "714", "t-245", "castro"],
    "santa-catarina-xarticle": ["santa catarina", "jmev", "alesc", "t-246", "jaguare"],
}

TITLE_THRESHOLD = 0.82
FP_MIN_HITS = 2


@dataclass
class LocalArticle:
    slug: str
    path: Path
    title: str


@dataclass
class RemoteArticle:
    post_id: str
    title: str
    plain_text: str
    created_at: str
    url: str
    text: str = ""
    metrics: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class MatchResult:
    status: str  # publicado | nao_publicado | match_ambiguo
    remote: Optional[RemoteArticle] = None
    score: float = 0.0
    reason: str = ""


def load_env() -> None:
    if load_dotenv is None:
        return
    for candidate in (ROOT / ".env", ROOT.parent / ".env", Path.cwd() / ".env"):
        if candidate.is_file():
            load_dotenv(candidate, override=False)


def bearer_token(token_file: Optional[Path] = None) -> str:
    if token_file and token_file.is_file():
        token = token_file.read_text(encoding="utf-8").strip().splitlines()[0].strip()
        if token:
            return token
    token = (
        os.getenv("X_ACCESS_TOKEN")
        or os.getenv("X_API_BEARER_TOKEN")
        or os.getenv("X_BEARER_TOKEN")
        or os.getenv("TWITTER_BEARER_TOKEN")
        or ""
    ).strip()
    if not token:
        print(
            "Token ausente. Defina X_ACCESS_TOKEN ou X_API_BEARER_TOKEN em .env\n"
            f"Veja {ROOT / '.env.example'}\n"
            "Ou: --token-file PATH  /  --from-json dump.json",
            file=sys.stderr,
        )
        sys.exit(2)
    return token


def remotes_from_json(path: Path, username: str) -> list[RemoteArticle]:
    """Import dump: list of {post_id,title,plain_text,url,created_at} or API-shaped tweets."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    items = raw if isinstance(raw, list) else raw.get("articles") or raw.get("data") or []
    out: list[RemoteArticle] = []
    for item in items:
        art = item.get("article") or {}
        post_id = str(item.get("post_id") or item.get("id") or "")
        if not post_id:
            continue
        title = (item.get("title") or art.get("title") or "").strip()
        plain = (item.get("plain_text") or art.get("plain_text") or "").strip()
        url = item.get("url") or article_url_from_entities(item, username, post_id)
        out.append(
            RemoteArticle(
                post_id=post_id,
                title=title,
                plain_text=plain,
                created_at=item.get("created_at") or "",
                url=url,
                text=item.get("text") or "",
                metrics=item.get("public_metrics") or {},
                raw=item,
            )
        )
    return out


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()


def api_get(path: str, token: str, params: Optional[dict] = None) -> dict:
    headers = {"Authorization": f"Bearer {token}", "User-Agent": "odragaoeaonca-fetch-x-articles/1.0"}
    url = f"{API}{path}"
    r = requests.get(url, headers=headers, params=params or {}, timeout=60)
    if r.status_code != 200:
        raise RuntimeError(f"X API {r.status_code} {path}: {r.text[:500]}")
    return r.json()


def resolve_user_id(username: str, token: str) -> str:
    data = api_get(f"/users/by/username/{username}", token)
    user = data.get("data") or {}
    uid = user.get("id")
    if not uid:
        raise RuntimeError(f"Usuário @{username} não encontrado: {data}")
    return str(uid)


def article_url_from_entities(tweet: dict, username: str, post_id: str) -> str:
    urls = ((tweet.get("entities") or {}).get("urls")) or []
    for u in urls:
        expanded = u.get("expanded_url") or u.get("url") or ""
        if re.search(r"x\.com/.+/article/|x\.com/i/article/", expanded, re.I):
            return expanded
    # Fallback estável para o post que carrega o Article
    return f"https://x.com/{username}/status/{post_id}"


def is_article_tweet(tweet: dict) -> bool:
    if tweet.get("article"):
        return True
    urls = ((tweet.get("entities") or {}).get("urls")) or []
    for u in urls:
        expanded = (u.get("expanded_url") or "") + " " + (u.get("url") or "")
        if re.search(r"x\.com/.+/article/|x\.com/i/article/|/articles/", expanded, re.I):
            return True
    return False


def fetch_user_articles(user_id: str, username: str, token: str, max_pages: int = 40) -> list[RemoteArticle]:
    articles: list[RemoteArticle] = []
    params: dict[str, Any] = {
        "max_results": 100,
        "tweet.fields": "article,created_at,entities,public_metrics,note_tweet,text",
        "expansions": "article.cover_media,article.media_entities",
        "exclude": "retweets,replies",
    }
    pages = 0
    while pages < max_pages:
        pages += 1
        data = api_get(f"/users/{user_id}/tweets", token, params)
        for tweet in data.get("data") or []:
            if not is_article_tweet(tweet):
                continue
            art = tweet.get("article") or {}
            post_id = str(tweet["id"])
            title = (art.get("title") or "").strip()
            plain = (art.get("plain_text") or "").strip()
            if not title and not plain:
                # Article link only — still track for orphan / URL match
                title = (tweet.get("text") or "")[:120]
            remote = RemoteArticle(
                post_id=post_id,
                title=title,
                plain_text=plain,
                created_at=tweet.get("created_at") or "",
                url=article_url_from_entities(tweet, username, post_id),
                text=tweet.get("text") or "",
                metrics=tweet.get("public_metrics") or {},
                raw=tweet,
            )
            articles.append(remote)
        meta = data.get("meta") or {}
        nxt = meta.get("next_token")
        if not nxt:
            break
        params["pagination_token"] = nxt
    return articles


def load_local_articles() -> list[LocalArticle]:
    items: list[LocalArticle] = []
    for path in sorted(ARTIGOS.glob("*-xarticle.md")):
        if path.name.endswith("-old.md") or "-old." in path.name:
            continue
        if path.name.startswith("_"):
            continue
        slug = path.stem  # foo-xarticle
        first = ""
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                if line.startswith("# "):
                    first = line[2:].strip()
                    break
        items.append(LocalArticle(slug=slug, path=path, title=first or slug))
    return items


def load_manual_map(path: Path) -> dict[str, dict]:
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("matches") or {}


def fingerprint_score(slug: str, remote: RemoteArticle) -> tuple[float, int]:
    keys = FINGERPRINTS.get(slug) or []
    hay = normalize(f"{remote.title}\n{remote.plain_text}\n{remote.text}")
    hits = sum(1 for k in keys if normalize(k) in hay)
    if not keys:
        return 0.0, 0
    return hits / len(keys), hits


def match_one(
    local: LocalArticle,
    remotes: list[RemoteArticle],
    manual: dict[str, dict],
    used_ids: set[str],
) -> MatchResult:
    # 1) Manual map
    m = manual.get(local.slug)
    if m and m.get("post_id"):
        pid = str(m["post_id"])
        for r in remotes:
            if r.post_id == pid:
                used_ids.add(pid)
                return MatchResult("publicado", r, 1.0, "published-map.json")
        # Mapped but not in current fetch — still count as published if URL given
        url = m.get("url") or f"https://x.com/i/status/{pid}"
        stub = RemoteArticle(pid, m.get("title") or local.title, "", m.get("created_at") or "", url)
        used_ids.add(pid)
        return MatchResult("publicado", stub, 1.0, "published-map.json (offline)")

    candidates: list[tuple[float, str, RemoteArticle]] = []
    for r in remotes:
        if r.post_id in used_ids:
            continue
        title_score = similarity(local.title, r.title) if r.title else 0.0
        fp_ratio, fp_hits = fingerprint_score(local.slug, r)
        # Combined: prefer title, boost fallback fingerprints
        score = max(title_score, 0.55 * title_score + 0.45 * fp_ratio)
        if title_score >= TITLE_THRESHOLD:
            candidates.append((title_score, f"title:{title_score:.2f}", r))
        elif fp_hits >= FP_MIN_HITS and fp_ratio >= 0.35:
            candidates.append((score, f"fingerprint:{fp_hits}/{len(FINGERPRINTS.get(local.slug) or [])}", r))

    if not candidates:
        return MatchResult("nao_publicado", None, 0.0, "sem match")

    candidates.sort(key=lambda x: x[0], reverse=True)
    best_score, best_reason, best = candidates[0]
    # Ambiguous if second is close
    if len(candidates) > 1 and (best_score - candidates[1][0]) < 0.05 and candidates[1][0] >= 0.75:
        return MatchResult("match_ambiguo", best, best_score, f"{best_reason}; rival={candidates[1][2].post_id}")

    used_ids.add(best.post_id)
    return MatchResult("publicado", best, best_score, best_reason)


def write_mirror(remotes: list[RemoteArticle]) -> None:
    MIRROR_DIR.mkdir(parents=True, exist_ok=True)
    for r in remotes:
        (MIRROR_DIR / f"{r.post_id}.json").write_text(
            json.dumps(r.raw, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        md = f"# {r.title or '(sem título)'}\n\n"
        md += f"- post_id: `{r.post_id}`\n"
        md += f"- url: {r.url}\n"
        md += f"- created_at: {r.created_at}\n\n"
        md += (r.plain_text or r.text or "") + "\n"
        (MIRROR_DIR / f"{r.post_id}.md").write_text(md, encoding="utf-8")


def write_report(
    path: Path,
    username: str,
    locals_: list[LocalArticle],
    results: dict[str, MatchResult],
    remotes: list[RemoteArticle],
    used_ids: set[str],
) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    pub = [s for s, r in results.items() if r.status == "publicado"]
    pend = [s for s, r in results.items() if r.status == "nao_publicado"]
    amb = [s for s, r in results.items() if r.status == "match_ambiguo"]
    orphans = [r for r in remotes if r.post_id not in used_ids]

    lines = [
        "# Publication status — X Articles",
        "",
        f"**Conta:** [@{username}/articles](https://x.com/{username}/articles)  ",
        f"**Gerado:** {now}  ",
        f"**Fonte:** X API v2 `GET /2/users/:id/tweets` + `tweet.fields=article`  ",
        f"**Locais:** {len(locals_)} canônicos · **Remotos (Article):** {len(remotes)}",
        "",
        "## Resumo",
        "",
        f"| Status | Qtd |",
        f"|--------|----:|",
        f"| Publicados (match) | {len(pub)} |",
        f"| Não publicados | {len(pend)} |",
        f"| Match ambíguo | {len(amb)} |",
        f"| Remotos órfãos (sem par local) | {len(orphans)} |",
        "",
        "## Pendentes de publicar",
        "",
    ]
    if pend:
        lines.append("| Slug | Título local |")
        lines.append("|------|--------------|")
        for s in pend:
            loc = next(x for x in locals_ if x.slug == s)
            lines.append(f"| `{s}` | {loc.title} |")
    else:
        lines.append("_Nenhum — todos os canônicos têm match._")

    lines += ["", "## Tabela completa", ""]
    lines.append("| Slug | Título local | Status | Score | Motivo | URL X |")
    lines.append("|------|--------------|--------|------:|--------|-------|")
    for loc in locals_:
        res = results[loc.slug]
        url = res.remote.url if res.remote else "—"
        title_cell = loc.title.replace("|", "\\|")
        lines.append(
            f"| `{loc.slug}` | {title_cell} | {res.status} | {res.score:.2f} | {res.reason} | {url} |"
        )

    if orphans:
        lines += ["", "## Remotos sem par local", ""]
        lines.append("| post_id | Título remoto | URL |")
        lines.append("|---------|---------------|-----|")
        for r in orphans:
            t = (r.title or r.text[:80]).replace("|", "\\|")
            lines.append(f"| `{r.post_id}` | {t} | {r.url} |")

    lines += [
        "",
        "## Como regenerar",
        "",
        "```bash",
        "pip install -r scripts/requirements-x-articles.txt",
        f"python scripts/fetch_x_articles.py --username {username}",
        "```",
        "",
        "Mapa manual (override): [`published-map.json`](published-map.json).",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def update_manual_map(path: Path, results: dict[str, MatchResult]) -> None:
    existing = load_manual_map(path) if path.is_file() else {}
    matches = dict(existing)
    for slug, res in results.items():
        if res.status == "publicado" and res.remote and res.score >= TITLE_THRESHOLD:
            matches[slug] = {
                "post_id": res.remote.post_id,
                "url": res.remote.url,
                "title": res.remote.title,
                "created_at": res.remote.created_at,
                "score": round(res.score, 3),
                "reason": res.reason,
            }
    out = {
        "_comment": "Mapa slug → post X. Atualizado por fetch_x_articles.py (matches score altos).",
        "matches": matches,
    }
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def annotate_locals(results: dict[str, MatchResult], locals_: list[LocalArticle]) -> None:
    marker_re = re.compile(r"<!--\s*published:\s*.*?-->\s*\n?", re.I)
    for loc in locals_:
        res = results.get(loc.slug)
        if not res or res.status != "publicado" or not res.remote:
            continue
        if res.score < TITLE_THRESHOLD and "published-map" not in res.reason:
            continue
        text = loc.path.read_text(encoding="utf-8")
        text = marker_re.sub("", text)
        comment = f"<!-- published: {res.remote.url} -->\n"
        loc.path.write_text(comment + text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Gap analysis X Articles vs artigos/")
    parser.add_argument("--username", default="araguaci")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--map", type=Path, default=DEFAULT_MAP)
    parser.add_argument("--max-pages", type=int, default=40)
    parser.add_argument("--annotate", action="store_true", help="Insere <!-- published: URL --> nos .md")
    parser.add_argument("--no-mirror", action="store_true")
    parser.add_argument("--update-map", action="store_true", help="Grava matches fortes em published-map.json")
    parser.add_argument("--from-json", type=Path, help="Dump local de Articles (pula API)")
    parser.add_argument("--token-file", type=Path, help="Arquivo com Bearer/access token (1 linha)")
    args = parser.parse_args()

    load_env()
    username = args.username.lstrip("@")

    if args.from_json:
        print(f"Importando remotes de {args.from_json}…")
        remotes = remotes_from_json(args.from_json, username)
    else:
        token = bearer_token(args.token_file)
        print(f"Resolvendo @{username}…")
        user_id = resolve_user_id(username, token)
        print(f"user_id={user_id}")
        print("Buscando posts (filtro Article)…")
        remotes = fetch_user_articles(user_id, username, token, max_pages=args.max_pages)

    print(f"Articles remotos: {len(remotes)}")

    if not args.no_mirror and remotes:
        write_mirror(remotes)
        print(f"Espelho: {MIRROR_DIR}")

    locals_ = load_local_articles()
    manual = load_manual_map(args.map)
    used: set[str] = set()
    results: dict[str, MatchResult] = {}
    for loc in locals_:
        results[loc.slug] = match_one(loc, remotes, manual, used)

    write_report(args.out, username, locals_, results, remotes, used)
    print(f"Relatório: {args.out}")

    if args.update_map:
        update_manual_map(args.map, results)
        print(f"Mapa: {args.map}")

    if args.annotate:
        annotate_locals(results, locals_)
        print("Annotate: <!-- published --> inserido nos matches fortes")

    pend = sum(1 for r in results.values() if r.status == "nao_publicado")
    pub = sum(1 for r in results.values() if r.status == "publicado")
    amb = sum(1 for r in results.values() if r.status == "match_ambiguo")
    print(f"Resumo: publicados={pub} pendentes={pend} ambíguos={amb}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
