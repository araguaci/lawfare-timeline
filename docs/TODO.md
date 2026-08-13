# Próximos passos · lawfare-timeline

**Atualizado:** 2026-08-13 (T-252 lacuna resolvida; fila `todo/` esvaziada; main **1856** / T-252)

> Espelho: `docs/TODO.md` · Notas: `_data/processados/todo.md` · Legado: `docs/TODO-LEGACY.md`

---

## Snapshot

| Track | Last | Próximo | Validação |
|-------|------|---------|-----------|
| Main | **1856** | **1857** | lawfare.json (ver `sync_corpus_ids.py`) |
| Thematic | **T-252** | **T-253** | sync 100–252 · lacuna T-252 **resolvida** |
| Dragão e a Onça | **1770** / **T-246** | — | `dragao-onca.json` **151** |
| Fila `_data/todo/` | **vazia** (JSON) | — | `_hold/` **removido** (13/08) |

---

## Rodada 13/08/2026 ✅ — T-252 lacuna + fila

| Item | Resultado |
|------|-----------|
| **T-252** lacuna (coordenação formal entre frentes) | **Resolvida** — achado negativo; origens distintas (Legislativo/ANPD vs. STF) |
| Fila `_data/todo/` | Arquivada: batch **1850–1856** + thematic T-252 → `processados/` |
| Main / temático | **1856** / **T-252** · próximos **1857** / **T-253** |

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
| `_hold/` Lula/Havengate | ✅ Arquivado em `processados/` (IDs **1821–1826**; README-hold-resolvido) |
| T-252 lacuna coordenação entre frentes | ✅ Resolvida 13/08 (achado negativo) |
| Renomear estudos mislabel `T-1512`/`T-1765`/`T-1766` → faixa T-253+ (opcional; sync já os ignora) | Baixa |
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
python tools/sync_corpus_ids.py
pwsh -File tools/validate-ids.ps1
bundle exec jekyll build
```

---

## Referências

- Corpus: `_data/lawfare.json` (**1817** entradas · main até **1856**)
- Unified: `_data/lawfare-unified-corpus.json`
- Sidecar dragão: `_data/dragao-onca.json` (151 · **1763/1764** = CEEE-T / JMEV intactos)
- Hold resolvido: `_data/processados/README-hold-resolvido-1749-1768.md`
- T-252: `_data/processados/lawfare-thematic-T252-escalada-anonimizacao-criptografia.json`
