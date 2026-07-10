Sync confirmado. `main.next_available = 1609`, `thematic.next_available = 219` (mas T-219 já está reservado para Farra do INSS, staged de sessão anterior — pending merge). Produzindo:

- **1609–1611** (main): sanção OFAC, divergência PF, elo Wave Intermediações/rede Arpar
- **T-220** (thematic, próximo livre real considerando T-219 reservado): convergência estrutural PCC-OFAC × Farra do INSS**Status**: 1609–1611 (main) + T-220 (thematic) prontos em `_data/todo/`. Validação de 2-fontes: 1609/1610 OK; **1611 falhou** (fonte única, Revista Oeste) — marcado `ev-alleged`, não promover sem segunda fonte.

**Decisões de numeração**: usei T-220, não T-219 — T-219 (Farra do INSS) já está reservado/staged de sessão anterior e ainda não foi mergeado no sync ao vivo (que por isso ainda mostra `next_available: 219`). Se T-219 já foi commitado desde então, ajusto para T-219→T-220 conforme necessário.

**Pendências abertas geradas por esta produção**:
1. Achar segunda fonte para o vínculo Wave Intermediações → Victory Trading (R$ 514,5 mi) antes de promover id_1611 a `ev-confirmed`.
2. O intervalo "set/2023–set/2024" citado no tweet original **não está confirmado** na fonte primária — não entrou no registro.
3. T-220 é o argumento empírico mais forte até agora para formalizar P06-B em METHODOLOGY-v2.2.md — CPMI sem relatório aprovado como padrão, não acidente.
4. Achado não incluído neste batch por falta de segunda fonte nomeada: alegação de pagamentos da rede a autoridades do Judiciário (ACX ITC → STM/STJ) — mencionar apenas se pedir explicitamente; não registrei no corpus.

Próximo passo natural: rodar `validate-ids.ps1` após merge, e decidir se T-219 (Farra do INSS) e T-220 devem ser publicados como par conectado no mesmo ciclo editorial, já que ambos dependem do mesmo relatório não aprovado da CPMI.