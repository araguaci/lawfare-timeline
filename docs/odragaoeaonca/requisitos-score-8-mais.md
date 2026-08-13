# Requisitos para Score 8.0+ — Síntese Final Dragão e Onça
### O que falta entre "Special Kudos" (6-8) e "Website of the Day" (8+)

---

## 🔴 Bloqueadores reais (sem isso, não passa de 7.5 em auditoria técnica)

### 1. Fonte carregada via `@import` — penaliza performance
```css
/* Atual — bloqueia renderização, sem preconnect */
@import url('https://fonts.googleapis.com/css2?family=Syne...');
```
`@import` dentro de `<style>` é a forma **mais lenta** de carregar fontes — o browser só descobre que precisa buscar a fonte depois de já ter baixado e parseado o CSS inteiro. Jurados de Awwwards/CSSDA rodam Lighthouse; isso custa pontos diretos em performance, que pesa em UX.

**Fix:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;700;800&family=JetBrains+Mono:wght@400;500&display=swap">
```
Mover para `<head>` como `<link>`, não `@import`. Ainda melhor a médio prazo: self-host as duas fontes (arquivos `.woff2` no seu próprio domínio) — elimina a dependência externa inteiramente e é o padrão que sites premiados usam.

### 2. Tabela sem `<thead>`/`<tbody>` — falha de acessibilidade
Confirmei via inspeção: a tabela tem `<tbody>` implícito mas **nenhum `<thead>`**. Isso quebra leitores de tela (a linha de cabeçalho não é anunciada como cabeçalho) e é um item que rubricas de acessibilidade (parte do critério UX em avaliações sérias) checam diretamente.

**Fix:** envolver a linha `<tr><th>...</th></tr>` em `<thead>`, e as linhas de dados em `<tbody>`.

### 3. Botões de filtro sem estado ARIA
Os `.filter-btn` (Todos/Sim/Não/Parcial) não têm `aria-pressed`, então tecnologia assistiva não informa qual filtro está ativo — funciona visualmente, mas é invisível para quem usa teclado/leitor de tela.

**Fix:**
```html
<button class="filter-btn active" data-filter="all" aria-pressed="true">Todos</button>
```
E atualizar `aria-pressed` via JS junto com a classe `.active` no clique.

---

## 🟡 O que separa "correto" de "premiável" (Inovação + polimento)

### 4. Matriz interativa estado × mecanismo (maior alavanca de nota em Inovação)
Vocês já têm o filtro por resultado — o próximo salto é uma **visualização gráfica**, não apenas tabela filtrável. Sugestão concreta e de escopo contido:

- Grid 12×10 (estados × os 10 mecanismos tipológicos já catalogados na seção Tipologia)
- Célula colorida quando aquele mecanismo se aplica àquele estado (dá pra derivar isso diretamente da tabela comparativa que já existe — é reorganização de dado já catalogado, não pesquisa nova)
- Clique numa célula rola até o card do mecanismo correspondente (reforça a navegação, não é só decoração)

Isso é factível como SVG/HTML simples, sem biblioteca externa, e é exatamente o tipo de "assinatura de interação única" que jurados de Awwwards citam como diferencial de Inovação.

### 5. Sticky header dentro da tabela ao rolar horizontalmente
Hoje, ao rolar a tabela para o lado em mobile, o cabeçalho (`Estado / Potência / Mecanismo...`) sai de vista junto com o conteúdo. Fixar a primeira coluna (`Estado`) com `position:sticky; left:0` mantém contexto durante o scroll horizontal — padrão comum em tabelas densas premiadas.

```css
table.comp th:first-child, table.comp td:first-child{
  position:sticky; left:0; background:var(--bg2); z-index:2;
}
```

### 6. Estado vazio na busca
Testei buscar por um estado inexistente — hoje a tabela provavelmente fica em branco sem explicação. Adicionar uma mensagem simples ("Nenhum estado encontrado para '{termo}'") evita a sensação de tela quebrada.

### 7. Unificar os três sistemas de cor semântica
Ainda pendente do relatório anterior: `.tag`/`.badge-capture`/`.alert` usam paletas parecidas mas não idênticas. Consolidar em um único conjunto de tokens (`--status-sim`, `--status-nao`, `--status-parcial`) usado nos três lugares — pequeno esforço, mas é o tipo de consistência que jurados de UI notam em exame comparativo lado a lado.

---

## Resumo — ordem de execução recomendada

| # | Item | Esforço | Ganho principal |
|---|---|---|---|
| 1 | Fonte via `<link>` + preconnect | 5 min | Performance/UX |
| 2 | `<thead>`/`<tbody>` na tabela | 5 min | Acessibilidade/UX |
| 3 | `aria-pressed` nos filtros | 10 min | Acessibilidade/UX |
| 5 | Sticky first column na tabela | 15 min | UX mobile |
| 6 | Estado vazio na busca | 15 min | UX/polimento |
| 7 | Unificar tokens de cor semântica | 30-45 min | UI/consistência |
| 4 | Matriz interativa estado×mecanismo | 2-4h | **Inovação — maior alavanca isolada** |

Os itens 1–3 e 5–6 são pequenos e cumulativamente levam a nota técnica (UX + acessibilidade) para 8.5+ de forma confiável — não é estimativa otimista, são correções objetivas que qualquer auditoria (Lighthouse, WAVE, ou jurado atento) vai captar.

O item 4 é o que muda a faixa de "correto e bem executado" para "memorável" — é o único item desta lista que cria algo nunca visto nos outros 18 artefatos da série, em vez de consertar algo existente.
