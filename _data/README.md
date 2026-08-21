# `_data/` — Corpus Lawfare Timeline

**Última revisão:** 2026-08-20  
**Site:** [lawfare-timeline.vercel.app](https://lawfare-timeline.vercel.app)  
**Painel de sync:** [`sync_status_latest.html`](./sync_status_latest.html)

Este diretório concentra **dados tabulares do corpus editorial** e **metadados de sincronização de IDs**. Parte dos ficheiros é consumida pelo Jekyll (tema Chirpy); o restante alimenta scripts, exports e sessões claude.ai.

---

## Estado atual (2026-08-20)

| Track | Último confirmado | Próximo livre | Fonte |
|-------|-------------------|---------------|-------|
| **Main** | **1888** | **1889** | `lawfare.json` |
| **Temático (T-)** | **T-262** | **T-263** | `claude.ai-corpus-ids-sync.json` |
| **Dragão e a Onça** | 132 main + 19 temáticos | — | `dragao-onca.json` + `_posts/dragao-onca/` (151 posts) |

- **`lawfare.json`:** **1849** assuntos · max ID **1888** (gap intencional **1820** → **T-248**)
- **`todo/`:** sem batches JSON (20/08: 1874–1888 + VT4 duplicado arquivados) · staging HTML/MD permanece
- **Drive:** `python tools/gdrive_sync_export.py` → `G:/Meu Drive/claude.ai-corpus-ids-sync.json` (+ `lawfare.json`)

Regenerar dashboard + sync Drive: `python tools/sync_corpus_ids.py`

---

## Mapa do diretório

```
_data/
├── README.md                          ← este ficheiro
│
├── ── NÚCLEO DO CORPUS (fonte de verdade) ──
├── lawfare.json                       Main track — assuntos[] com id, datas, categoria
├── claude.ai-corpus-ids-sync.json     Mapa IDs main + temático, batches, session_log
├── lawfare-unified-corpus.json        Entradas unificadas (id_corpus, fontes_verificadas)
├── dragao-onca.json                   Export série (124 main + 18 temáticos)
├── export-vazatoga.json               Export série Vaza Toga 1–5 (_posts + IDs do corpus)
├── vazatoga_thematic_order.yml        Ordem T-255→T-262 no hub /vazatoga/
├── dragao_onca_thematic_order.yml     Ordem temática hub /dragao-onca/
├── precedentes-republica.json         Sidecar PREC-AAAA-NN (1890–1930)
├── precedentes-pos-1990.json          Sidecar pos-1990 (PREC-1997-05)
│
├── ── PIPELINE EDITORIAL ──
├── todo/                              Entradas pendentes (merge → lawfare + _posts)
├── processados/                       Batches arquivados pós-merge (ver README local)
│
├── ── RELATÓRIOS E DASHBOARDS ──
├── sync_status_latest.html            Dashboard humano (symlink lógico ao snapshot mais recente)
├── sync_status_YYYY-MM-DD.html        Snapshots datados do sync
├── relatorio-top30-sem-estudo.md      Lacunas sem dossiê (rank_ops_sem_estudo.py)
├── top30-alertas-criticos-operacoes-sem-dossie.md
│
├── ── EXPORTS POR CATEGORIA (legado / metodologia) ──
├── export-lawfare-methodology.json
├── export-operacoes-methodology.json
├── export-*-methodology.json          (bancos, stf, tse, vazatoga, etc.)
├── export-bolsonaro-timeline.json
├── lawfare-full.json                  Export completo para busca
├── lawfare-export-timeline-15abr2026.json
├── posts-extraidos.json               Inventário _posts/ (IDs posicionais — não usar p/ tracking)
├── posts-since-2026-05-26.json
│
├── ── SIDECARS E DOMÍNIOS ESPECÍFICOS ──
├── jusmonitor/                        Enriquecimento evidencial captura → https://jusmonitor.vercel.app
│   ├── enrichment-patches.json        Patches por id (fontes + descrições)
│   ├── candidates-grave.json          Fila gravidade-alta / alertas críticos
│   ├── schema.json                    Contrato do patch
│   └── README.md
├── justicewatch/                      Corpus JustiçaWatch (bridge T-209) → canônico https://jusmonitor.vercel.app
│   ├── justicawatch-brasil.json
│   └── decisoes-seed.json             (via extract_decisoes.py)
├── atores-gilmar-mendes-carmen-lucia.json
├── bloqueios-nikolas_dm*.json
├── tinyurls_related.json
├── lawfare-design-system.json
│
├── ── JEKYLL / TEMA CHIRPY (não mover sem atualizar _config) ──
├── authors.yml
├── contact.yml
├── media.yml
├── share.yml
├── locales/                           i18n do tema (24 idiomas)
├── origin/                            cors.yml, basic.yml
│
├── ── CONFIG AUXILIAR ──
├── gdrive-sync-export.json            Destino Google Drive (sync automático)
├── gdrive-sync-export.example.json
├── TEMPLATE-registro-rapido.json
│
└── ── CANDIDATOS A ARQUIVO (ver plano Fase 3) ──
    lawfare.bak-*.json
    claude.ai-corpus-ids-sync.json.backup*
    _data.rar
    jekyll-posts-p11-cluster.tar.gz
    PROMPT-*.md, OPERACOES-*.md, walkthrough.md, SYNC-REPORT-*.md
```

---

## Papéis dos ficheiros principais

### `lawfare.json`

Fonte de verdade do **main track**. Cada `assunto` tem:

- `id` (inteiro sequencial, com gaps conhecidos)
- `titulo`, `data_evento`, `categoria`, `tags`, `fontes`, `fonte_arquivo`
- Campos analíticos: `analise`, `lacuna_investigativa`, `connections`

**Regra:** não sobrescrever faixa 1449–1510 sem validação explícita.

### `claude.ai-corpus-ids-sync.json`

Mapa operacional entre sessões editoriais e o repo:

- `tracks.main` — batches confirmados, `last_confirmed`, `next_available`
- `tracks.thematic` — entradas T-100+, capítulos Dragão T-228–T-246; estudos **T-248–T-254**; hub Vaza Toga **T-255–T-262** (mislabels T-1512/1765/1766 fora do registry)
- `sync_status` — contadores e fila
- `session_log` — histórico de merges

Cruzamento obrigatório com `lawfare.json` + `_posts/**/*.md` após cada merge.

### `dragao-onca.json`

Export dedicado da série **O Dragão e a Onça**. Inclui entradas temáticas (T-228→T-245) que **não** entram em `lawfare.json` — os IDs 228–245 já pertencem a entradas históricas antigas no corpus principal.

Regenerar: `python scripts/export_dragao_onca_json.py`

### `export-vazatoga.json`

Export dedicado da série **Vaza Toga 1–5**. Fonte primária: `_posts/vazatoga/` + posts relacionados (jornalistas Ágape/Vieira, crise INQ 4781, índice T-207). Campo `id` / `id_corpus` = ID do corpus (`lawfare.json`); **não** reutiliza os IDs posicionais de `export-vazatoga-methodology.json`.

Regenerar: `python scripts/export_vazatoga_json.py`

Hub Jekyll: `/vazatoga/` (`_layouts/vazatoga.html` + `_data/vazatoga_thematic_order.yml`). Regenerar capítulos temáticos: `python scripts/gerar_artigos_vazatoga.py`

### Sidecars (`precedentes-*.json`)

Namespace `PREC-AAAA-NN`. Indexados em T-224. Não mesclados ao main track.

---

## Fluxo editorial (pipeline)

```
┌─────────────────┐     merge_todo / sync_todo_current      ┌──────────────┐
│  _data/todo/    │ ───────────────────────────────────────►│ lawfare.json │
│  *.json         │                                         └──────┬───────┘
│  NOTAS-MERGE.md │                                                │
└────────┬────────┘                                                ▼
         │ arquivar                                    ┌─────────────────────┐
         └────────────────────────────────────────────►│ _data/processados/  │
                                                       └─────────────────────┘
         gerar_artigos_dragao_onca.py (série)                    │
         sync_todo_current.py (geral)                            │
                │                                                │
                ▼                                                ▼
         ┌─────────────┐                              claude.ai-corpus-ids-sync.json
         │ _posts/     │                              sync_status_*.html
         └─────────────┘                              dragao-onca.json (export)
```

### Comandos habituais

| Ação | Comando |
|------|---------|
| Publicar batch todo | `python scripts/sync_todo_current.py` (ou `--dry-run`) |
| Atualizar mapa IDs + HTML | `python tools/sync_corpus_ids.py` |
| Validar IDs | `pwsh -File tools/validate-ids.ps1` |
| Export Dragão e a Onça | `python scripts/export_dragao_onca_json.py` |
| Export Vaza Toga 1–5 | `python scripts/export_vazatoga_json.py` |
| Reconciliar batch vs lawfare | `python tools/reconcile_lawfare_batch.py` |
| Sync Google Drive | automático via `tools/gdrive_sync_export.py` |

### Convenções de nomenclatura

| Padrão | Exemplo | Destino |
|--------|---------|---------|
| `lawfare-batch-<tema>-<id>-<id>.json` | `lawfare-batch-dragao-onca-rs-1735-1737.json` | main track |
| `lawfare-thematic-T<nnn>-*.json` | `lawfare-thematic-T245-dragao-onca-rj.json` | thematic track |
| `patch-*.json` | `patch-id1100-margem-equatorial-fza59.json` | correção pontual |
| `NOTAS-MERGE-*.md` | `NOTAS-MERGE-ceee-t-1763.md` | instruções humanas em `todo/` |

---

## O que **não** editar manualmente

| Ficheiro | Motivo |
|----------|--------|
| `sync_status_*.html` | Gerado por `sync_corpus_ids.py` |
| `claude.ai-corpus-ids-sync.json` (secções derivadas) | Parcialmente regenerado pelo sync |
| `posts-extraidos.json` | Snapshot de inventário |
| `docs/**` | Build Jekyll (`destination: docs`) |

---

## Plano de reorganização

Objetivo: reduzir ruído na raiz de `_data/`, separar **corpus**, **tema Jekyll**, **exports legados** e **arquivo**, sem quebrar paths referenciados em scripts e posts.

### Fase 0 — Documentação (concluída)

- [x] Criar `_data/README.md` (este ficheiro)
- [x] Atualizar secção `_data/` em [`README.md`](../README.md) com link para aqui e IDs atuais (**1888** / **T-254**)

### Fase 1 — Higiene imediata (baixo risco)

Ações que não exigem mover ficheiros consumidos pelo Jekyll:

| Ação | Ficheiros | Notas |
|------|-----------|-------|
| Arquivar backups | `lawfare.bak-*.json`, `claude.ai-corpus-ids-sync.json.backup*` | Mover para `_data/archive/backups/` |
| Arquivar binários | `_data.rar`, `jekyll-posts-p11-cluster.tar.gz` | Mover para `_data/archive/` |
| Consolidar relatórios MD soltos | `SYNC-REPORT-*.md`, `walkthrough.md` | Mover para `_data/reports/` |
| Atualizar `processados/README.md` | — | Contagens desatualizadas (90→142 posts); apontar para este README |

**Critério de done:** raiz com ≤25 ficheiros `.json` ativos (excluindo exports).

### Fase 2 — Subpastas semânticas (risco médio)

Criar estrutura e mover exports legados; **atualizar paths** em scripts/docs que referenciam ficheiros movidos.

```
_data/
  corpus/          ← lawfare.json, sync, dragao-onca.json, precedentes-*
  exports/         ← export-*.json, lawfare-full.json, posts-extraidos.json
  reports/         ← sync_status_*.html, relatorio-*.md, SYNC-REPORT-*
  archive/         ← backups, .rar, snapshots antigos
  todo/            (mantém)
  processados/     (mantém)
  jekyll/          ← authors.yml, contact.yml, locales/, origin/  [OPCIONAL]
```

**Pré-requisito:** grep repo por cada path movido; atualizar:

- `tools/sync_corpus_ids.py`, `gdrive_sync_export.py`, `sync_watcher.py`
- `scripts/sync_todo_current.py`, `export_dragao_onca_json.py`
- Posts em `_posts/estudos/` com links `_data/...`

**Alternativa conservadora (recomendada):** manter núcleo na raiz; mover apenas `export-*` → `exports/` e snapshots → `reports/sync/`.

### Fase 3 — Política de retenção

| Tipo | Retenção | Destino |
|------|----------|---------|
| `sync_status_*.html` | Últimos 30 dias na raiz; resto em `reports/sync/` | Automatizar em `sync_corpus_ids.py` |
| `todo/*.json` pós-merge | 0 — arquivar imediatamente em `processados/` | Regra editorial |
| `processados/*.json` | Permanente | Referência histórica |
| Exports metodologia | Permanente em `exports/` | Somente leitura |
| Backups manuais | 90 dias → `archive/` | Não versionar `.backup*` no git |

### Fase 4 — Validação contínua

Adicionar (ou estender) script de auditoria:

```bash
python tools/audit_data_dir.py   # proposto
```

Checks mínimos:

1. `max(lawfare.assuntos[].id)` == `sync.tracks.main.last_confirmed`
2. `sync.tracks.thematic.last_id` == max T- confirmado em `_posts/`
3. `todo/` vazio após merge (ou só NOTAS + HTML staging)
4. `lawfare.json total` == `len(assuntos)`
5. Contagem `_posts/dragao-onca/` == `dragao-onca.json total`

Integrar no fluxo pós-merge junto com `validate-ids.ps1`.

---

## Fila atual (`todo/`)

**Sem batches JSON** (20/08/2026): 1865–1868, 1869–1873 e 1874–1888 em `processados/`.

| Local | Conteúdo |
|-------|----------|
| `_data/todo/*.html` / `*.md` | Staging (`p13-porta-giratoria.html`, `prompt-tratamento-pdfs-mensalao.md`, `CR-0006.md`) |
| `_data/processados/lawfare-thematic-T254-*.json` | P13 Porta Giratória (reassign de T-253) |
| `_data/processados/README-hold-resolvido-1749-1768.md` | `_hold/` encerrado: Lula/Havengate publicados como **1821–1826** |

---

## Referências cruzadas

| Documento | Conteúdo |
|-----------|----------|
| [`README.md`](../README.md) | Visão geral do repo + comandos |
| [`METHODOLOGY.md`](../METHODOLOGY.md) | P01–P11, schema JSON |
| [`processados/README.md`](./processados/README.md) | Histórico batch Dragão (jul/2026) |
| [`processados/MANIFEST.md`](./processados/MANIFEST.md) | Manifesto técnico de processamento |
| [`tools/instrucao-claude-ai-ids.md`](../tools/instrucao-claude-ai-ids.md) | Protocolo IDs para sessões claude.ai |
| [`odragaoeaonca/README.md`](../odragaoeaonca/README.md) | Hub estático da série Dragão e a Onça |

---

## Regras para agentes e editores

1. **Nunca** atribuir ID main sem consultar `claude.ai-corpus-ids-sync.json` → `next_available`.
2. **Sempre** cruzar `_data/*.json` + `_posts/**/*.md` antes de declarar sync OK.
3. Capítulos temáticos Dragão: usar `timeline_id` no front matter; ordem hub em `dragao_onca_thematic_order.yml`.
4. Após merge: arquivar JSON em `processados/`, esvaziar `todo/`, rodar `sync_corpus_ids.py`.
5. Ficheiros `authors.yml`, `locales/`, `origin/` pertencem ao **tema Jekyll** — não misturar com pipeline editorial.

---

*Mantenedor: @araguaci · CC0 1.0*
