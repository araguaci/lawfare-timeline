#!/usr/bin/env python3
"""Adiciona tag de estado/capítulo nos posts da série Dragão e a Onça."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

POSTS = Path(__file__).resolve().parents[1] / "_posts" / "dragao-onca"

IMAGE_TO_STATE = {
    "dragao-onca-amazonas.webp": "amazonas",
    "dragao-onca-para.webp": "para",
    "dragao-onca-minas-gerais.webp": "minas-gerais",
    "dragao-onca-goias.webp": "goias",
    "dragao-onca-brasil-federal.webp": "brasil-federal",
    "dragao-onca.webp": "brasil-federal",
    "dragao-onca-braco-juridico.webp": "brasil-federal",
    "dragao-onca-pl2780.webp": "brasil-federal",
    "dragao-onca-bahia.webp": "bahia",
    "dragao-onca-sao-paulo.webp": "sao-paulo",
    "dragao-onca-parana.webp": "parana",
    "dragao-onca-rio-grande-do-sul.webp": "rio-grande-do-sul",
    "dragao-onca-espirito-santo.webp": "espirito-santo",
    "dragao-onca-ranking-cebc.webp": "brasil-federal",
}

ID_OVERRIDES = {
    "1648": "sao-paulo",
    "1649": "sao-paulo",
    "1650": "sao-paulo",
    "1710": "goias",  # Serra Verde/GO citado no PL
}

FILE_OVERRIDES = {
    "t228": "goias",
    "t229": "brasil-federal",
    "t230": "para",
    "t231": "amazonas",
    "t232": "minas-gerais",
    "t234": "brasil-federal",
    "t235": "brasil-federal",
    "t236": "brasil-federal",
    "t237": "bahia",
    "t238": "sao-paulo",
    "t239": "parana",
    "t240": "rio-grande-do-sul",
    "t241": "espirito-santo",
    "t242": "brasil-federal",
    "t243": "brasil-federal",
}

STATE_TAGS = {
    "goias",
    "para",
    "amazonas",
    "minas-gerais",
    "sao-paulo",
    "brasil-federal",
    "bahia",
    "parana",
    "rio-grande-do-sul",
    "espirito-santo",
}

SINTESE_TAGS = [
    "goias", "para", "amazonas", "minas-gerais", "brasil-federal",
    "bahia", "sao-paulo", "parana", "rio-grande-do-sul", "espirito-santo",
]


def parse_tags(raw: str) -> list[str]:
    return re.findall(r'"([^"]+)"|\'([^\']+)\'', raw)


def flatten_tag_matches(matches: list[tuple[str, str]]) -> list[str]:
    return [a or b for a, b in matches]


def main() -> None:
    changed: list[tuple[str, str, str]] = []
    skipped: list[tuple[str, str]] = []

    for path in sorted(POSTS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            skipped.append((path.name, "no fm"))
            continue

        parts = text.split("---", 2)
        if len(parts) < 3:
            skipped.append((path.name, "bad fm"))
            continue

        fm, body = parts[1], parts[2]

        m_img = re.search(r"image:\s*([^\r\n]+)", fm)
        img = m_img.group(1).strip() if m_img else ""
        img_name = Path(img).name if img else ""

        m_tags = re.search(r"^tags:\s*(\[[^\]]*\])\s*$", fm, re.M)
        if not m_tags:
            skipped.append((path.name, "no tags"))
            continue

        stem = path.stem.lower()
        if "t233" in stem or "t243" in stem or "sintese" in stem:
            states = list(SINTESE_TAGS)
        else:
            state = None
            for key, val in FILE_OVERRIDES.items():
                if key in stem:
                    state = val
                    break
            if state is None:
                m_id = re.search(r"id(\d+)", stem)
                if m_id and m_id.group(1) in ID_OVERRIDES:
                    state = ID_OVERRIDES[m_id.group(1)]
            if state is None:
                state = IMAGE_TO_STATE.get(img_name)
            if state is None:
                skipped.append((path.name, f"unmapped img={img_name}"))
                continue
            states = [state]

        raw = m_tags.group(1)
        existing = flatten_tag_matches(parse_tags(raw))
        new_tags = [t for t in existing if t not in STATE_TAGS]
        for s in states:
            if s not in new_tags:
                new_tags.append(s)

        if len(new_tags) > 10:
            non_state = [t for t in new_tags if t not in STATE_TAGS]
            state_only = [t for t in new_tags if t in STATE_TAGS]
            new_tags = (non_state + state_only)[:10]

        new_raw = "[" + ", ".join(f'"{t}"' for t in new_tags) + "]"
        if new_raw == raw:
            skipped.append((path.name, "unchanged"))
            continue

        new_fm = fm[: m_tags.start(1)] + new_raw + fm[m_tags.end(1) :]
        path.write_text("---" + new_fm + "---" + body, encoding="utf-8")
        changed.append((path.name, ",".join(states), new_raw))

    counts: Counter[str] = Counter()
    for _, st, _ in changed:
        for s in st.split(","):
            counts[s] += 1

    print(f"CHANGED: {len(changed)}")
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v}")
    print(f"SKIPPED: {len(skipped)}")
    for item in skipped:
        print(" ", item)


if __name__ == "__main__":
    main()
