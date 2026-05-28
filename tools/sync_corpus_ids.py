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
            b["status"] = "jekyll_published"
            b["notes"] = (
                "Posts/estudos Jekyll (Biomm 1527-1546, Zema 1547-1550, Homeschooling 1551). "
                f"lawfare.json termina em {last_main} — merge batch pendente."
            )
        if b.get("range") == [1552, 1571]:
            b["status"] = "jekyll_published"
            b["notes"] = (
                "Operação Rejeito — ~20 posts em _posts/ (source_data lawfare-batch-rejeito-1552-1571.json). "
                f"IDs reservados; lawfare.json merge pendente (next_available={next_main})."
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

    # Confirmar T-191 / T-196 alinhados aos posts
    for tid, topic, artifact, notes in [
        (191, "Custeio administrativo federal — P11 (T-191)", "custeio-administrativo-federal-p11", "Estudo Jekyll 2026-05-27/28."),
        (196, "Radar de Lacunas — Top 30 sem dossiê (T-196)", "top30-alertas-criticos-operacoes-sem-dossie", "Artigo Jekyll/artigos; ex-T-191 radar."),
    ]:
        if tid in by_id:
            by_id[tid].update({"status": "confirmed", "topic": topic, "artifact": artifact, "notes": notes})

    thematic["entries"] = entries
    thematic["last_id"] = 196
    thematic["next_available"] = 197
    thematic["pending"] = [180, 192, 193, 194, 195]
    thematic["pending_notes"] = {
        "180": "TSE seletividade — entrada pronta para produção",
        "192": "Operação Rejeito / Serra do Curral / manuscritos (cluster 1552–1571)",
        "193": "Gastos públicos sob sigilo — parcialmente coberto por T-191",
        "194": "Vorcaro carbono fictício × Compliance Zero × Rejeito",
        "195": "CPI Crime Organizado × infiltração eleitoral PCC",
    }

    sync = data["sync_status"]
    sync["main_track_last_sync"] = date.today().isoformat()
    sync["thematic_track_last_sync"] = date.today().isoformat()
    sync["ids_confirmed_total"] = {
        "main_track": f"{last_main} (lawfare.json); jekyll batches 1527-1571 merge pendente",
        "thematic_track": 196,
    }
    sync["ids_pending_production"] = [180, 192, 193, 194, 195]
    sync["open_items"] = [
        item
        for item in sync.get("open_items", [])
        if "MERGE PCC batch 1449" not in item
    ]
    for note in [
        f"lawfare.json last_id={last_main}; próximo ID livre={next_main}",
        "Merge lawfare.json: batches Jekyll 1527-1551 e Rejeito 1552-1571",
        "Estudos T-189, T-190, T-191, T-196 publicados em _posts/estudos/",
        "Fila editorial T-192 a T-195 (ver artigos/2026-05-27-top30-alertas-criticos-operacoes-sem-dossie.md)",
    ]:
        if note not in sync["open_items"]:
            sync["open_items"].append(note)

    data["id_conflict_resolutions"]["custeio_vs_top30"] = {
        "T-191": "Custeio P11 — estudo canônico",
        "T-196": "Radar Top 30 — renumerado do antigo T-191",
        "date": date.today().isoformat(),
    }

    SYNC.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"sync OK: main last={last_main} next={next_main}; thematic last=196 next=197")
    print(f"T-studies on disk: {sorted(t_posts.items())}")


if __name__ == "__main__":
    main()
