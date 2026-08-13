# `_data/jusmonitor/`

Camada canônica de **enriquecimento evidencial** para o feed [JusMonitor](https://jusmonitor.vercel.app), sem reescrever em massa `lawfare.json`.

## Papel

| Arquivo | Função |
|---------|--------|
| `enrichment-patches.json` | Patches por `id` (fontes + descrições) aplicados no extract |
| `candidates-grave.json` | Fila do corpus: só `gravidade-alta` judicial + alertas críticos |
| `unresolved.json` | IDs com fonte ainda genérica — aprofundar URL nominativa |
| `schema.json` | Contrato do patch |
| `_inventory-sem-fonte.json` | Snapshot de auditoria (gerado) |

## Pipeline

```
lawfare.json + enrichment-patches.json
  → extract_jusmonitor.py
  → jusmonitor_data.json
  → copia para jusmonitor.vercel.app/data/captura.json
  → build-unified.py → unified.json
```

Decisões T-209: fonte em `_data/justicewatch/justicawatch-brasil.json` (espelho em `jusmonitor/.../decisoes-source.json`).

## Critérios evidenciais

- `ev-confirmed` — URL jornalística ou documental verificável
- `ev-alleged` — sem fonte primária; não tratar como fato confirmado

## Filtro corpus amplo

Só entram na fila `candidates-grave.json`:

- tag `gravidade-alta` + categorias/tags judiciais do extract
- alertas críticos judiciais (T-196 score ≥ 40, eixo STF/CNJ/judiciário)

## Sync

```bash
cd _data
python extract_jusmonitor.py
copy jusmonitor_data.json ..\..\jusmonitor.vercel.app\data\captura.json
cd ..\..\jusmonitor.vercel.app
python scripts/build-unified.py
python scripts/validate-schema.py
```
