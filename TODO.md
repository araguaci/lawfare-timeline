# Próximos passos · lawfare-timeline

**Atualizado:** 2026-08-05 (batch 1827–1835 + T-249/T-250 + correção conexões 1835)

> Espelho: `docs/TODO.md` · Notas: `_data/processados/todo.md` · Legado: `docs/TODO-LEGACY.md`

---

## Snapshot

| Track | Last | Próximo | Validação |
|-------|------|---------|-----------|
| Main | **1838** | **1839** | lawfare.json **1799** entradas |
| Thematic | **T-250** | **T-251** | sync 100–250 |
| Dragão e a Onça | **1770** / **T-246** | — | `dragao-onca.json` **151** |
| Fila `_data/todo/` | **vazia** | — | `_hold/` legado |

---

## Rodada 04/08/2026 ✅ — Sequência corrigida + merge

| Faixa | Conteúdo |
|-------|----------|
| **1797–1799** | Teodoro / Oruam / Japa PCC |
| **1800–1803** | Drones Complexo da Penha |
| **1804–1809** | P01-B garantismo seletivo (ex-1763–1768 → **sem** colisão dragao-onca) |
| **1810–1819** | Outorgas MP747, ADPF 165, lacunas rádio, cartórios BA (main) |
| **T-248** | Editorial cartórios BA (ex-T-1820 — colisão main) |
| **1821–1824** | Cluster Lula/Flávio “traidor” (ex `_hold` 1749–1752) |
| **1825–1826** | Havengate / Mercury Legacy (ex `_hold` 1767–1768) |
| **T-247** | Dedo na Balança T2 — vídeo IA convenção PL |

**Scripts:** `reassign_todo_batch_ids.py` · `fix_havengate_1826_main.py` · `fix_thematic_sync_track.py` · patch `sync_todo_current.py` (main ≥1000 ≠ temático)

---

## Pendências abertas

| Item | Prioridade |
|------|------------|
| Reatribuir IDs batches `_hold/` (cópias legadas) | ✅ Realocados em 1821–1826 |
| Renomear estudos `T-1765`/`T-1766` → faixa T-249+ (opcional) | Baixa |
| Gap main **1820** (editorial → T-248, não entra em lawfare.json) | Informativo |
| Batch Pantera/Severino/Gugu | ✅ **1836–1838** (05/08/2026) |
| Jonathan Macedo (SP) — 2ª fonte | Baixa |
| Formalizar P04b em METHODOLOGY | Média |
| `bundle exec jekyll build` | Rodar após esta rodada |

---

## Comandos

```bash
python scripts/reassign_todo_batch_ids.py   # antes de sync, se batch conflitar
python scripts/sync_todo_current.py
python scripts/fix_thematic_sync_track.py   # se thematic.last_id divergir
pwsh -File tools/validate-ids.ps1
bundle exec jekyll build
```

---

## Referências

- Corpus: `_data/lawfare.json` (1796 entradas · main até **1835**)
- Unified: `_data/lawfare-unified-corpus.json` (174 entradas)
- Sidecar dragão: `_data/dragao-onca.json` (151 · **1763/1764** = CEEE-T / JMEV intactos)
