# Notas de merge — backfill CEEE-T (id_1763)

## O que foi encontrado
Os dois artefatos de síntese citavam a privatização da CEEE-T (RS, 2021) com **IDs 1758–1759**.
Esses IDs pertencem, no corpus real (`dragao-onca.json`, confirmado no `claude_ai-corpus-ids-sync.json`),
aos dois eventos do **Amapá** (contrato Amazonbai de açaí + pendência GACC) — não à CEEE-T.
Busquei "CEEE" em `dragao-onca.json`, `lawfare.json` e no sync file: **nenhuma entrada existia**.
Era um gap retroativo (mesma classe do fix já feito em Goiás/T-228), não um erro de digitação.

## O que foi verificado (web, 4 fontes independentes)
Leilão B3, 16/jul/2021. CPFL Energia (grupo State Grid) arremata 66,08% da CEEE-T por R$2,67bi,
ágio de 57,13% sobre mínimo de R$1,699bi. Segunda privatização do grupo CEEE sob Eduardo Leite
(após CEEE-D/Equatorial, mar/2021). Conclusão prevista out/2021, sujeita a ANEEL/CADE.

## Arquivos entregues nesta rodada
1. `lawfare-batch-dragao-onca-rs-ceee-t-1763.json` → mover para `_data/todo/`, processar com
   `merge_todo_pending.py`. Novo ID main track: **1763** (consome o próximo ID livre do sync file).
2. `dragao-onca-sintese.html` e `dragao-onca-sintese-final-cross-state.html` → versões corrigidas,
   substituem os uploads. Mudanças: citação de ID (1758–1759 → id_1763), nota metodológica
   distinguindo leilão público (CEEE-T) de negociação bilateral direta (padrão "governador-negociador"),
   contagens agregadas atualizadas (142→143 posts, 1639–1762→1639–1763).

## Pendências que você precisa aplicar localmente (não tenho acesso ao repo)
- **`_posts/dragao-onca/2026-07-24-t240-dragao-onca-rs.md`** (T-240): a `descricao` do capítulo diz
  "3 entradas main track, 1735-1737" — deve passar a citar também **id_1763**. Sugestão de texto:
  > "...Rio Grande do Sul. Período: 2021 (CEEE-T) e 2025-09 a 2026-06 (GWM, 3 entradas, 1735-1737).
  > Capítulo combina captura energética confirmada (CEEE-T→State Grid, id_1763) com cortejo industrial
  > perdido (GWM→ES)..."
- **`claude_ai-corpus-ids-sync.json`**: após merge, atualizar `tracks.main.last_confirmed` de 1762
  para **1763** e `notes` do próximo ID livre para **1764**.
- Criar o post Jekyll correspondente: `_posts/dragao-onca/2021-07-16-id1763-ceee-t-privatizacao-cpfl-state-grid.md`.

## Nota metodológica (anti-confirmation-bias)
CEEE-T é licitação pública competitiva estruturada pelo BNDES, não negociação bilateral do governador —
mecanismo estruturalmente distinto do "governador-negociador" dominante na série, ainda que convergente
no resultado (infraestrutura crítica → capital estatal chinês). Isso já está refletido no campo `analise`
da entrada 1763 e nos textos corrigidos dos dois HTMLs. Não forçar o evento no padrão dominante.
