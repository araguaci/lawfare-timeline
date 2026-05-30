#!/usr/bin/env python3
"""
merge_pcc_batch_1481_1505.py
Faz o merge das entradas PCC/Ndrangheta (IDs 1481-1505) em lawfare.json.

Fontes:
  - _data/processados/lawfare-1481-1496-pcc-ndrangheta.json  (16 entries, formato assuntos)
  - _data/processados/pcc-novas-entradas-1497-1510.json       (9 entries, formato new_timeline_entries)

Uso:
  python tools/merge_pcc_batch_1481_1505.py          # dry-run
  python tools/merge_pcc_batch_1481_1505.py --commit # executa o merge
"""
from __future__ import annotations
import json, sys, shutil, io
from pathlib import Path
from datetime import date

# Força UTF-8 no stdout do Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
LAWFARE = ROOT / "_data" / "lawfare.json"
PCC1 = ROOT / "_data" / "processados" / "lawfare-1481-1496-pcc-ndrangheta.json"
PCC2 = ROOT / "_data" / "processados" / "pcc-novas-entradas-1497-1510.json"
SYNC = ROOT / "_data" / "claude.ai-corpus-ids-sync.json"

COMMIT = "--commit" in sys.argv


def load_entries_1481() -> list[dict]:
    """Carrega o batch 1481-1496 — já no formato assuntos."""
    data = json.loads(PCC1.read_text(encoding="utf-8"))
    assert isinstance(data, list), "Esperado lista"
    for e in data:
        # Garantir campos obrigatórios mínimos
        e.setdefault("fontes_verificadas", e.pop("fontes", []))
        e.setdefault("pessoas_envolvidas", [])
        e.setdefault("instituicoes_envolvidas", e.pop("instituicoes_envolvidas", []))
        e.setdefault("evidencia", "ev-confirmed")
        e.setdefault("padroes_sistemicos", [])
    return data


CATEGORY_MAP = {
    "operacao_policial": "operacoes",
    "análise_estrutural": "estudos",
    "incidente_diplomatico": "crise-diplomatica",
    "crime-organizado-transnacional": "lawfare",
    "default": "lawfare",
}


def load_entries_1497() -> list[dict]:
    """Carrega o batch 1497-1505 e transforma new_timeline_entries → assuntos."""
    raw = json.loads(PCC2.read_text(encoding="utf-8"))
    ents = raw.get("new_timeline_entries", [])
    out = []
    for e in ents:
        eid = int(e["id"])
        d = e.get("date", "")
        cat_raw = e.get("category", "default")
        cat = CATEGORY_MAP.get(cat_raw, CATEGORY_MAP["default"])
        tags = (
            e.get("patterns", [])
            + [t.lower().replace(" ", "-") for t in e.get("institutions", []) if t]
        )
        # Fontes
        fontes = [s["url"] for s in e.get("sources", []) if s.get("url")]
        # Pessoas
        pessoas = [a["name"] for a in e.get("actors", []) if a.get("name")]
        instits = e.get("institutions", [])
        entry = {
            "id": eid,
            "titulo": e["title"],
            "data_evento": d,
            "data_iso": f"{d}T00:00:00.000Z" if d else "",
            "categoria": cat,
            "tags": list(dict.fromkeys(tags)),  # unique, ordered
            "descricao": e.get("summary", ""),
            "pessoas_envolvidas": pessoas,
            "instituicoes_envolvidas": instits,
            "fontes_verificadas": fontes,
            "pais": "Brasil",
            "dimensao_global": True,
            "evidencia": e.get("evidence_note", "ev-confirmed"),
            "padroes_sistemicos": e.get("patterns", []),
            "relevancia": "alta",
            "prioridade": 1,
        }
        out.append(entry)
    return out


def main() -> None:
    print("=== merge_pcc_batch_1481_1505 ===")
    print(f"  Modo: {'COMMIT (gravação)' if COMMIT else 'DRY-RUN'}\n")

    # --- Carregar lawfare.json ---
    lawfare = json.loads(LAWFARE.read_text(encoding="utf-8"))
    existing_ids = {int(a["id"]) for a in lawfare["assuntos"]}
    print(f"  lawfare.json atual: {len(lawfare['assuntos'])} entradas, último ID = {max(existing_ids)}")

    # --- Carregar novos entries ---
    batch1 = load_entries_1481()
    batch2 = load_entries_1497()
    new_entries = batch1 + batch2
    new_ids = [int(e["id"]) for e in new_entries]
    print(f"  Lote 1481-1496: {len(batch1)} entradas")
    print(f"  Lote 1497-1505: {len(batch2)} entradas")
    print(f"  Total para merge: {len(new_entries)} entradas — IDs {min(new_ids)}-{max(new_ids)}\n")

    # --- Verificar conflitos ---
    conflicts = [i for i in new_ids if i in existing_ids]
    if conflicts:
        print(f"  [ERRO] Conflito: IDs já existem em lawfare.json: {conflicts}")
        sys.exit(1)
    print(f"  [OK] Sem conflitos com IDs existentes.")

    # --- Verificar duplicatas internas ---
    dupes = [i for i in new_ids if new_ids.count(i) > 1]
    if dupes:
        print(f"  [ERRO] IDs duplicados no lote: {set(dupes)}")
        sys.exit(1)
    print(f"  [OK] Sem duplicatas internas no lote.")

    # --- Preview ---
    print("\n  Entradas a inserir:")
    for e in sorted(new_entries, key=lambda x: int(x["id"])):
        print(f"    ID {e['id']:5} | {e['titulo'][:65]}")

    if not COMMIT:
        print("\n  [DRY-RUN] Nenhuma modificação aplicada. Use --commit para gravar.")
        return

    # --- Backup ---
    backup = LAWFARE.with_suffix(f".bak-{date.today()}.json")
    shutil.copy2(LAWFARE, backup)
    print(f"\n  Backup criado: {backup.name}")

    # --- Inserir e ordenar ---
    all_entries = lawfare["assuntos"] + new_entries
    all_entries.sort(key=lambda x: int(x["id"]))
    lawfare["assuntos"] = all_entries
    LAWFARE.write_text(json.dumps(lawfare, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  lawfare.json atualizado: {len(all_entries)} entradas.")

    # --- Atualizar sync JSON ---
    sync = json.loads(SYNC.read_text(encoding="utf-8"))
    batches = sync["tracks"]["main"]["confirmed_batches"]
    # Marcar 1449-1510 como parcialmente confirmado
    for b in batches:
        if b.get("range") == [1449, 1510]:
            b["status"] = "confirmed_partial"
            b["notes"] = (
                f"Merge {date.today()}: IDs 1481-1505 (25 entries PCC/Ndrangheta + Carbono Oculto "
                f"+ crime organizado transnacional) integrados em lawfare.json. "
                f"IDs 1449-1480 e 1506-1510 sem entradas (gap permanente aceito)."
            )
            b.pop("do_not_overwrite", None)
            b.pop("pcc_namespace", None)
    sync["_meta"]["generated"] = date.today().isoformat()
    SYNC.write_text(json.dumps(sync, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  claude.ai-corpus-ids-sync.json atualizado.")
    print("\n  [CONCLUÍDO] Merge executado com sucesso.")


if __name__ == "__main__":
    main()
