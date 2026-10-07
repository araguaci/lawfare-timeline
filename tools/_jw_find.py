# inventory queue IDs vs occupied
import json, re
from pathlib import Path

root = Path(".")
lf = json.loads((root / "_data/lawfare.json").read_text(encoding="utf-8"))
occ = sorted(int(a["id"]) for a in lf["assuntos"] if isinstance(a.get("id"), int))
print(f"lawfare.json n={len(occ)} last={occ[-1]} next={occ[-1]+1} max={max(occ)}")
gaps = [i for i in range(occ[0], occ[-1]) if i not in set(occ)]
print(f"gaps count={len(gaps)} sample={gaps[:20]}")

t_posts = []
for p in (root / "_posts/estudos").glob("*.md"):
    t = p.read_text(encoding="utf-8", errors="replace")
    m = re.search(r'id_corpus:\s*["\']?T-(\d+)', t)
    if m:
        t_posts.append(int(m.group(1)))
print(f"thematic posts last={max(t_posts) if t_posts else None} n={len(t_posts)}")

def ids_in_obj(obj, found):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("id", "id_corpus") and isinstance(v, int):
                found.append(v)
            elif k in ("id", "id_corpus") and isinstance(v, str):
                found.append(v)
            else:
                ids_in_obj(v, found)
    elif isinstance(obj, list):
        for x in obj:
            ids_in_obj(x, found)

for folder in ("_data/todo", "_data/lock"):
    print(f"\n== {folder} ==")
    for p in sorted(Path(folder).glob("*")):
        if p.suffix.lower() not in {".json", ".html", ".md"}:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        found = []
        if p.suffix == ".json":
            try:
                ids_in_obj(json.loads(text), found)
            except Exception as e:
                found = [f"JSON_ERR {e}"]
        else:
            found = re.findall(r"\bT-\d+\b|\bid[_\s:=]+(\d{3,4})\b", text)[:20]
        print(f"  {p.name}: {found[:30]}{'...' if len(found)>30 else ''} n={len(found)}")
