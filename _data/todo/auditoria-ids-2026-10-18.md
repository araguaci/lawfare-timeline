# Auditoria de IDs — lawfare.json × claude.ai-corpus-ids-sync.json
**Data:** 2026-10-18 · ambos os arquivos atualizados 2026-10-18 14:57 (BRT) · CC0

## Veredito
**Ponteiros sincronizados; inventário do sync com 6 divergências.** Pode gerar IDs novos a partir de **main 1986 / T-275** com segurança.

| Métrica | lawfare.json | sync | OK? |
|---|---|---|---|
| Último ID main | 1985 | 1985 (`last_id`, `_meta`, raiz) | ✅ |
| Próximo livre main | — | 1986 | ✅ |
| Entradas (`total`) | 1946 = `len(assuntos)` | "1–1985 confirmed" (não declara total) | ⚠️ |
| IDs únicos / duplicados | 1946 / 0 | — | ✅ |
| Tipo do `id` | 100% int | — | ✅ |
| Ordem do array | crescente, 0 inversões | — | ✅ |
| Thematic | n/a (namespace separado) | T-100…T-274, sem gaps/dups; próximo T-275 | ✅ |

## Gaps em lawfare.json (39 IDs ausentes)
| Faixa | Qtde | Status no sync |
|---|---|---|
| 1449–1480 | 32 | Documentado: "gap permanente aceito" |
| 1506–1510 | 5 | Documentado: "gap permanente aceito" |
| **1774** | 1 | ❌ Sync declara `1771-1774 confirmed` — **ID não existe** |
| **1820** | 1 | ⚠️ Gap intencional (renumerado → T-248), mas a faixa `1797-1826` o declara confirmed |

## Divergências sync → corrigir no `confirmed_batches`
1. **1774 fantasma** — batch 2026-07-28 deveria ser `1771-1773`.
2. **1775–1776 órfãos** — existem no lawfare (sigilo 100 anos Vorcaro/MJ; Alcolumbre/Careca do INSS) mas não constam em nenhum batch.
3. **1624 órfão** — existe (Bolsonaro protocola revisão criminal, 08/05/2026), não consta em batch.
4. **Nota de resolução errada** — `id_conflict_resolutions.1520_176…` diz que a revisão criminal canônica é **1621**; no lawfare, 1621 = "Moraes mantém domiciliar…" (17/07/2026). A revisão criminal está em **1624**. Corrigir a nota para 1624.
5. **Faixas sobrepostas** — `1577-1620` e `1577-1578` reescrevem batches já listados; `1612-1612` aparece duas vezes; `1763-1764` duplica parte de `1763-1770`. Ruído, sem colisão real.
6. **1820** — dividir `1797-1826` em `1797-1819` + `1821-1826`, ou anotar o gap.

## Bugs do script de auto-sync (cursor/gdrive_sync_export.py)
- **Reescreve datas históricas com a data do run:** notas "Merge lawfare.json **2026-10-18**: Biomm…/Rejeito" (eram 2026-05-28 → 2026-10-06 → agora 10-18); `custeio_vs_top30.date` idem; notas T-251…T-254 "(auto-sync 2026-10-18)". Perda de proveniência.
- **`open_items` inflando:** bloco "Fila editorial … T-196…T-221 publicado (DATA)" é reanexado a cada run — centenas de linhas repetidas com conteúdo idêntico.
- **`last_session_produced` inconsistente:** `_meta` = 1762; `tracks.main` = 1770 (`last_produced` também 1770).
- **`artifacts_id_reserved_pending_formalization: [208, 209]`** — ambos já `confirmed`. Esvaziar.
- `_meta.session` estático ("sessão editorial 2026-05-28") em todo run.

## Duplicatas de CONTEÚDO em lawfare.json (IDs distintos, mesmo evento)
### Recentes (prioridade — afetam contagem e citações)
| IDs | Evidência | Ação sugerida |
|---|---|---|
| **1827 = 1970** | mesmo post `2026-08-04-coronel-pm-…pcc` | remover 1970 (manter 1827) |
| **1828 = 1971** | mesmo post `2026-08-04-eua-revogam-visto-da-embaixadora…` | remover 1971 |
| 1637 ≈ 1822 | "Flávio protocola notícia-crime contra Lula no STF" (11/06) | revisar |
| 1849 ≈ 1856 | "Moraes autoriza busca contra fonte de jornalista" (11/08) | revisar |
| 1330 ≈ 1843 | contrato R$ 129 mi escritório esposa Moraes (09/12/2025) | revisar |
| 1183 ≈ 1184 | EUA revogam visto de Moraes (18/07/2025) | revisar |

1970/1971 entraram no merge 2026-10-06 (1943–1973) reprocessando posts já indexados — o `merge_todo_pending.py` não deduplica por `fonte_arquivo`.

### Legado (1–1400)
58 títulos idênticos e 31 pares com mesmo arquivo de post (ex.: 357/358 Zelotes, 412/413, 436/437 … 863/864; 528/718/794/841/962/1085 "prorrogação INQ fake news 180 dias" — estes últimos são eventos distintos com título genérico, não duplicatas). Lista completa: rodar `audit.py`.

## Regra para remoções
**Não renumerar.** Remover duplicata = gap documentado (padrão 1820). Registrar em `id_conflict_resolutions`.

## Documentos desatualizados no projeto
- `instrucao-claude-ai-ids.md` (2026-05-12): diz last=1448 / next=1512 / T-189. Real: 1985 / 1986 / T-275.
- Instruções do projeto: "referência: 1570s". Real: 1986.

## Fila
- `lawfare-batch-fe-e-voto-1986.json` (renumerado de 1974, que foi consumido por T-273/T-274) → `_data/todo/`.
