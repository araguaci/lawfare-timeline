"""Extract JusMonitor captura cards from lawfare.json + enrichment patches."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAWFARE = HERE / "lawfare.json"
PATCHES = HERE / "jusmonitor" / "enrichment-patches.json"
OUT = HERE / "jusmonitor_data.json"

KEYWORDS = [
    "venda-de-sentencas",
    "corrupcao-judicial",
    "cnj",
    "desembargador",
    "judiciario",
    "magistrado",
    "aposentadoria-compulsoria",
    "vazatoga",
    "vaza-toga",
]


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def relevant(e: dict) -> bool:
    if e.get("categoria") in (
        "justica",
        "vazatoga",
        "penduricalhos",
        "stf",
        "tse",
    ):
        return True
    if e.get("tipo_escandalo") == "Judiciário":
        return True
    tags = e.get("tags", [])
    return any(k in tags for k in KEYWORDS)


def classify(e: dict) -> str:
    tags = e.get("tags", [])
    cat = e.get("categoria")
    if "venda-de-sentencas" in tags or "corrupcao-judicial" in tags:
        return "corrupcao_judicial"
    if cat == "penduricalhos":
        return "penduricalhos"
    if cat in ("stf", "vazatoga"):
        return "chokepoint_stf"
    if cat == "tse":
        return "eleitoral_tse"
    if cat == "justica":
        if (
            "cnj" in tags
            or "aposentadoria-compulsoria" in tags
            or "assedio-sexual" in tags
        ):
            return "cnj_disciplinar"
        return "outros_judiciario"
    return "outros_judiciario"


def evidence_status(fontes: list) -> str:
    real = [s for s in fontes if s and s != "N/A"]
    return "ev-confirmed" if real else "ev-alleged"


def load_patches() -> dict:
    if not PATCHES.exists():
        return {}
    raw = load_json(PATCHES)
    out = {}
    for p in raw.get("patches", []):
        pid = p.get("id")
        if pid is None:
            continue
        out[pid] = p
        # also index stringified int keys
        out[str(pid)] = p
    return out


def apply_patch(card: dict, patch: dict | None) -> dict:
    if not patch:
        return card
    fontes = [s for s in (patch.get("fontes") or []) if s and s != "N/A"]
    if fontes:
        card["fontes"] = fontes
    resumo = (patch.get("descricao_resumo") or "").strip()
    detalhada = (patch.get("descricao_detalhada") or "").strip()
    if detalhada:
        card["descricao"] = detalhada
    elif resumo:
        card["descricao"] = resumo
    if patch.get("evidence_status"):
        card["evidence_status"] = patch["evidence_status"]
    else:
        card["evidence_status"] = evidence_status(card.get("fontes") or [])
    if patch.get("gravidade"):
        card["gravidade"] = patch["gravidade"]
    if patch.get("alerta_critico"):
        card["alerta_critico"] = True
    if resumo:
        card["descricao_resumo"] = resumo
    if detalhada:
        card["descricao_detalhada"] = detalhada
    return card


def main() -> None:
    data = load_json(LAWFARE)
    assuntos = data["assuntos"]
    sync_date = data.get("data_extração") or data.get("data_extracao")
    patches = load_patches()

    filtered = [e for e in assuntos if relevant(e)]
    good = [
        e
        for e in filtered
        if e.get("descricao")
        and e["descricao"] not in ("", ">", "N/A")
        and len(e["descricao"]) > 20
    ]
    excluded = [e for e in filtered if e not in good]

    cards = []
    for e in good:
        real_sources = [s for s in e.get("fontes", []) if s and s != "N/A"]
        card = {
            "id": e.get("id"),
            "data": (e.get("data_iso") or "")[:10],
            "titulo": (e.get("titulo") or "").strip(),
            "descricao": (e.get("descricao") or "").strip(),
            "grupo": classify(e),
            "gravidade": next(
                (
                    t.replace("gravidade-", "")
                    for t in e.get("tags", [])
                    if t.startswith("gravidade-")
                ),
                None,
            ),
            "relevancia": e.get("relevancia"),
            "instituicoes": e.get("instituicoes_envolvidas", []),
            "tags": [t for t in e.get("tags", []) if not t.startswith("gravidade-")],
            "fontes": real_sources,
            "evidence_status": evidence_status(real_sources),
            "valor_envolvido": e.get("valor_envolvido")
            if e.get("valor_envolvido") not in ("N/A", None)
            else None,
        }
        patch = patches.get(card["id"]) or patches.get(str(card["id"]))
        card = apply_patch(card, patch)
        # R1 JusMonitor: ev-confirmed exige URL http(s)
        real = [
            s
            for s in (card.get("fontes") or [])
            if isinstance(s, str) and s.startswith(("http://", "https://"))
        ]
        card["fontes"] = real
        if not real:
            card["evidence_status"] = "ev-alleged"
        cards.append(card)

    cards.sort(key=lambda c: c["data"] or "", reverse=True)

    print("total cards:", len(cards))
    print(Counter(c["grupo"] for c in cards))
    print(Counter(c["evidence_status"] for c in cards))
    print("excluded (data gap, pending enrichment):", len(excluded))
    print(
        "sem fonte apos patch:",
        sum(1 for c in cards if not c.get("fontes")),
    )

    payload = {
        "gerado_de": "lawfare.json + jusmonitor/enrichment-patches.json",
        "sync_date": sync_date,
        "total": len(cards),
        "excluidos_pendente_enriquecimento": len(excluded),
        "cards": cards,
    }
    with OUT.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    print(f"OK {OUT}")


if __name__ == "__main__":
    main()
