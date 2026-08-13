# Avaliação "Padrão Diamante" — O Dragão e a Onça: Síntese Final
### Artefato: `dragao-onca-sintese-final-cross-state.html` · testado em desktop (1400px) e mobile (390px)

---

## Nota estimada (rubrica CSS Design Awards: UI 40% / UX 30% / Inovação 30%)

| Critério | Nota estimada /10 | Corte CSSDA |
|---|---|---|
| **UI Design** | 7.8 | — |
| **UX Design** | **5.5** | abaixo do corte de 8.0 para WOTD |
| **Inovação** | 6.5 | — |
| **Conteúdo** (Awwwards, 10%) | 9.5 | ponto mais forte, de longe |

**Diagnóstico central:** este é um dos conteúdos mais densos e metodologicamente honestos que eu já vi em auditoria de design — a seção "Correções Metodológicas (anti-confirmation-bias)" sozinha já é mais rigor do que 90% do jornalismo investigativo publicado. O problema não é o que foi escrito. É que **um bug real de UX no mobile está entre o leitor e esse conteúdo.**

---

## 🔴 Achado crítico — Tabela comparativa quebra no mobile

Testei o carregamento real da página em viewport de 390px (iPhone padrão). Resultado:

- A `table.comp` renderiza com **610px de largura fixa** dentro de uma tela de 390px
- Isso força a **página inteira** a rolar horizontalmente (`body scrollWidth: 652px`)
- Na prática: ao abrir a Tabela Comparativa — que é o coração analítico do dossiê, com os 12 estados + federal — o leitor mobile vê 2 de 5 colunas (Estado, Potência, Mecanismo) e precisa descobrir sozinho que pode arrastar a tela inteira para o lado para ver "Resultado" e "Captura", que são as colunas com a conclusão de cada linha

Isso não é um detalhe — é o critério #1 que qualquer jurado de Awwwards/CSSDA testa primeiro (mobile real, não emulador), e reprova instantaneamente sites com scroll horizontal não-intencional.

### Fix recomendado (baixo esforço, alto impacto)
Envolver a tabela em um contêiner com scroll próprio, sem afetar o layout da página:

```css
.table-scroll{
  overflow-x:auto;
  -webkit-overflow-scrolling:touch;
  margin:0 -20px;      /* opcional: sangra até a borda em mobile */
  padding:0 20px;
}
.table-scroll table.comp{ min-width:640px; }
```
```html
<div class="table-scroll">
  <table class="comp">...</table>
</div>
```

Isso confina o scroll horizontal à tabela — o padrão universalmente aceito para tabelas densas em telas pequenas — e mantém o resto da página estável. Ganho estimado: +1.5 a +2.0 pontos em UX sozinho, porque hoje esse é o único ponto de fricção real em todo o artefato.

**Alternativa mais ambiciosa** (recomendada para o médio prazo, ligada ao item de Inovação do checklist anterior): em vez de tabela, um **card empilhável por estado** em mobile — cada UF vira um cartão com os 5 campos em layout vertical, mantendo a tabela apenas em desktop via media query. Mais trabalho, mas transforma a leitura mobile de "decodificar uma tabela apertada" para "ler um dossiê por estado", que é mais alinhado ao tom editorial do resto do site.

---

## 🎨 UI Design — 7.8/10

**Pontos fortes:**
- Paleta escura com verde-selva/dourado é coerente com a identidade "Dragão e Onça" e diferente da paleta genérica de dashboard corporativo
- Sistema de badges de captura (`bc-sim` / `bc-nao` / `bc-parcial`) com borda lateral colorida na tabela é um ótimo dispositivo visual — decodificável em um relance, mesmo antes de ler o texto
- Tipografia (Syne + JetBrains Mono) tem personalidade — foge do Inter/Helvetica padrão que domina 80% dos dashboards de dados
- Cards de KPI no topo (`.kgrid`) com barra de cor superior por categoria — recurso visual eficiente, replicável em outros artefatos do hub

**Pontos a melhorar:**
- Existem **três sistemas de cor competindo** para o mesmo conceito (confirma/refuta a tese): `.tag`/`.tr`/`.tgo` no corpo do texto, `.badge-capture`/`bc-sim`/`bc-nao`/`bc-parcial` na tabela, e `.alert.ok`/`.alert.crit`/`.alert.info` na seção de Tese Refinada. São paletas parecidas mas não idênticas (verde/vermelho/dourado vs. verde/vermelho/azul) — pequena inconsistência que um jurado exigente notaria como falta de um design system único
- Variáveis CSS redundantes com fallback em cascata (`var(--jaguar,var(--gold,var(--gr2,#e8b23d)))`) sugerem que o token `--jaguar` não está definido neste arquivo mas é esperado do hub — isso é sintoma de que os tokens de cor **não estão centralizados** entre os 19 artefatos da série, exatamente o ponto 2 da prioridade que discutimos antes

## 🧭 UX Design — 5.5/10 (rebaixado pelo bug de tabela)

**Pontos fortes:**
- Nav sticky com highlight de seção ativa via `IntersectionObserver` — implementação limpa, sem dependência externa
- Botão "Copiar dossiê completo para IA" é um toque de usabilidade rara e inteligente — antecipa que pesquisadores/jornalistas vão querer levar o conteúdo para outro contexto de análise
- Botão "voltar ao topo" com fade-in a partir de 400px de scroll — detalhe de polimento correto

**Pontos a melhorar (além do bug crítico acima):**
- Sem busca ou filtro dentro da própria tabela — em uma matriz de 12 estados com 5 dimensões, um filtro por "resultado" (sim/não/parcial) ajudaria o leitor a testar hipóteses próprias sem ler tudo
- A navegação por seções (`nav`) não indica **quantos itens** tem cada seção antes de clicar — "Tabela Comparativa" não avisa que são 12 linhas, "Todos os Capítulos" não avisa que são 19 links
- Grid de "Artefatos da Série" no rodapé (19 cards) é longo e redundante com a nav de "Todos os Capítulos" logo acima — dois índices da mesma coisa na mesma página aumenta carga cognitiva sem ganho

## 💡 Inovação — 6.5/10

**Pontos fortes:**
- A seção "Correções Metodológicas" é, honestamente, um diferencial editorial raro — few investigative sites publicly retract/correct their own prior framing with dated, ID-referenced changelogs. Isso é o tipo de coisa que jurados de conteúdo/jornalismo de dados adorariam, se um jurado desse tipo existisse nas rubricas de design puro
- Tipologia de 10 mecanismos como taxonomia própria (não apenas lista de casos) é um dispositivo analítico genuinamente original

**O que falta para nota alta:**
- Com 12 estados + 10 mecanismos + resultado sim/não/parcial, este é o caso de uso perfeito para uma **visualização de rede ou matriz cruzada interativa** (estado × mecanismo, com destaque de correlação) em vez de tabela + cards de texto sequenciais. É exatamente o item 3 da prioridade que já estava no seu roadmap ("visualização de rede dos padrões P01–P13") — este artefato específico, com sua estrutura tabular tão rica, é o candidato ideal para prototipar isso primeiro antes de escalar para o lawfare-timeline inteiro

---

## Resumo executivo — 3 ações, em ordem de impacto/esforço

1. **[Crítico, ~15 min de trabalho]** Envolver `table.comp` em `.table-scroll` — resolve o único bug real de UX do artefato
2. **[Médio prazo, alto valor]** Unificar os três sistemas de cor semântica (tag/badge/alert) em um único token set compartilhado entre os 19 artefatos da série
3. **[Maior esforço, maior retorno de Inovação]** Prototipar uma matriz interativa estado×mecanismo aqui, como piloto antes de aplicar ao lawfare-timeline completo

Com o item 1 resolvido, este artefato sobe de ~6.6 para ~7.8 de nota geral estimada — já competitivo para Special Kudos em CSSDA. Os itens 2 e 3 são o que separaria "bom dossiê" de "site premiável".
