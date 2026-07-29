# Notas de merge — capítulo Santa Catarina (T-246, IDs 1764–1770)

## IDs consumidos
Main track: **1764–1770** (7 entradas, sequência a partir do 1763 já usado no backfill CEEE-T).
Thematic: **T-246** (síntese do capítulo).
Próximo ID livre após este merge: main **1771**, thematic **T-247**.

## O que foi verificado (todas ev-confirmed, fontes oficiais ou imprensa especializada)
1. **id_1764** — JMEV/E-Motors firmam parceria para fábrica SKD em Jaguaré (ES), anunciada em BH, 26/mai/2025. Fonte: UAI, BHAZ.
2. **id_1765** — Deputados da Alesc (Krelling, De Nadal, Fabiano da Luz, Minotto) se reúnem com a JMEV em Nanchang, 16/jun/2025. Fonte: Agência Alesc (oficial).
3. **id_1766** — Alesc assina termo de intenção com a JMEV em Pequim, 22/jun/2025, governador presente. Fonte: site institucional da Alesc.
4. **id_1767** — Governador visita PowerChina (21/jun) e CRRC (22/jun) para discutir ferrovias. Fonte: SPAF-SC (oficial).
5. **id_1768** — Governador pede à GACC retomada de exportação de frango, 24/jun/2025, no contexto do embargo nacional por gripe aviária (RS). Fonte: Sec. Agricultura SC (oficial), Exame.
6. **id_1769** — CRCC/CRRC Changchun confirmam visita técnica a SC (jul/2025); Inspur Group convidado para data center. Fonte: NSC Total, SCTD.
7. **id_1770** — Mar/2026: nem SC nem ES confirmam fábrica operacional da JMEV; carros vendidos por importação direta. Fonte: Carango Elétrico.

## Achado central (mesmo padrão de rigor do backfill CEEE-T)
A JMEV já tinha firmado acordo com o Espírito Santo (id_1764, 26/mai/2025) **um mês antes** de a comitiva da Alesc iniciar o cortejo a Santa Catarina (id_1765, 16/jun/2025). O termo de intenção assinado em Pequim (id_1766) foi celebrado publicamente como avanço, mas nenhuma das duas fábricas (SC ou ES) está confirmada operacional até mar/2026 (id_1770) — variante mais severa que o padrão RS/GWM (T-240), onde ao menos o "vencedor" (ES) obteve a fábrica.

## Nota de simetria (protocolo anti-confirmation-bias)
O episódio do frango (id_1768) foi deliberadamente classificado como **caso de controle**, não como capítulo de captura — é embargo sanitário nacional, não negociação de ativo estratégico. Não forçar no padrão P05/P10 dominante da série.

## Arquivos entregues
1. `lawfare-batch-dragao-onca-santa-catarina-1764-1770.json` → mover para `_data/todo/`, processar com `merge_todo_pending.py`.
2. `dragao-onca-santa-catarina.html` → novo artefato, capítulo completo (T-246), colocar na raiz do projeto.
3. `dragao-onca-sintese.html` e `dragao-onca-sintese-final-cross-state.html` → atualizados: SC como 12ª UF, tabelas comparativas, KPIs, nav da série, contagens agregadas (12 UFs, T-246, 150 posts).

## Pendências no seu repo (não tenho acesso direto)
- Criar posts Jekyll para `_posts/dragao-onca/` correspondentes aos 7 `fonte_arquivo` indicados no batch JSON.
- Atualizar `claude_ai-corpus-ids-sync.json`: `tracks.main.last_confirmed` 1763→**1770**; `tracks.thematic.last_confirmed` 245→**246**.
- Adicionar SC ao `_tabs/dragao-onca.md` (navegação da série) e ao índice `odragaoeaonca/index.html`.
- Gerar asset webp regional para Santa Catarina (padrão dos demais capítulos).
