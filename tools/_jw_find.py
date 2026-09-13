import json
from pathlib import Path

lf = json.loads(Path("_data/lawfare.json").read_text(encoding="utf-8"))
want = {1797, 1798, 1799, 1806, 1809, 1831}
for a in lf["assuntos"]:
    if a.get("id") in want:
        print(a["id"], (a.get("titulo") or "")[:100])
        print(" ", a.get("fonte_arquivo"))
        print(" ", a.get("data_evento"))

for pat in ("*dois-pesos*", "*695*", "*oruam*", "*tanaka*", "*110kg*", "*itaguai*", "*privilegiado*"):
    for p in Path("_posts").rglob(pat):
        print("FILE", p)
