# T-276 · O Dragão e a Onça — Capítulo 19: Sun Tzu, vencer sem lutar

Pacote para o repo `lawfare-timeline`. Mesma árvore de pastas do repo.

| Arquivo | Destino |
|---|---|
| `dragao-onca-suntzu.html` | raiz do repo (capítulo, padrão visual da série) |
| `_posts/dragao-onca/2026-11-11-t276-dragao-onca-suntzu.md` | post Jekyll do capítulo |
| `_data/patch-t276-dragao-onca-suntzu.json` | 7 entradas main + entrada temática T-276 (schema v2.4) |
| `tools/sync_t276.py` | aplica o patch no repo |

## IDs

- Temático: **T-276** (conforme `next_thematic` informado).
- Main: **1986–1992 provisórios**. Calculados contra o clone do GitHub de 18/out/2026 (último confirmado 1985). O `lawfare.json` do Drive (2,9 MB, modificado 11/nov/2026) não pôde ser lido por inteiro nesta sessão, só os primeiros ~80 KB.
- O script lê o `lawfare.json` atual, pega `max_id` e renumera tudo para `max_id+1…`, incluindo `connections`, `id_NNNN` no texto, tabela de fontes do HTML e links do post.

## Como aplicar

```
python tools/sync_t276.py --repo D:\ai-projects\lawfare-timeline --lawfare d:/ai-projects/_data/lawfare.json --dry-run
python tools/sync_t276.py --repo D:\ai-projects\lawfare-timeline --lawfare d:/ai-projects/_data/lawfare.json --update-nav
```

- `--lawfare`: o `lawfare.json` do Drive. O resultado é gravado em `<repo>/_data/lawfare.json`.
- `--update-nav`: insere o card do capítulo 19 na navegação dos 18 capítulos existentes.
- Grava `.bak-t276` de cada arquivo antes de alterar. Aborta se T-276 já existir.
- Atualiza: `lawfare.json`, `dragao-onca.json` (totais, `id_ranges`, `thematic_order`), `dragao_onca_thematic_order.yml`, `claude.ai-corpus-ids-sync.json`.
- Os posts Jekyll das 7 entradas main ficam para o extrator do repo (`fonte_arquivo` já vem preenchido com a regra de slug do repo).

## Pendências editoriais (lacunas marcadas nas entradas)

1. id 1986: o nexo Lava Jato → venda da Camargo Corrêa vem de uma única fonte (CartaCapital/IHU). Classificado ev-alleged.
2. id 1988: 23% (Camargo, jul/2016) × 31,6% (fechamento, jan/2017). Conferir no 20-F 2017 da CPFL.
3. id 1989: data exata da votação na comissão e se o dispositivo entrou no texto sancionado.
4. id 1992 × id 1983: R$ 23 bi × R$ 18,1 bi para o bipolo UHV.
5. O manifesto do repo registra T-274 como último temático. Conferir onde T-275 foi registrado.

CC0 1.0
