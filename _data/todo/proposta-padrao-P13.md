# PROPOSTA — Padrão P13: Captura Hierárquica em Carreira de Estado Não-Judicial

**Status:** CANDIDATO (1 evento-âncora) — não promovido a padrão confirmado.
Critério do próprio corpus (README/METHODOLOGY §"padrão sistémico"): 3+ eventos-âncora
independentes, mesmo mecanismo, mesma direção de resultado. P13 aguarda 2+ casos
adicionais antes de entrar como padrão formal em `padroes-sistemicos-dashboard.html`.
Até lá, deve ficar sinalizado como "sob observação" — não anexar ao dashboard de produção
como padrão pleno.

---

## Definição operacional

P13 está ativo quando, em uma carreira de Estado **fora do Judiciário** (serviço exterior,
carreiras policiais não-judiciais, agências reguladoras, estatais, forças armadas etc.):

1. **Concentração de autoridade unilateral** — decisões de gestão de pessoal, alocação de
   função e comunicação institucional passam a ser tomadas sem colegialidade ou consulta,
   por um único ocupante de cargo hierárquico superior.
2. **Retaliação administrativa contra quem formaliza queixa** — remoção, transferência ou
   esvaziamento de função de servidores que levantam preocupações, por via de mecanismos
   formalmente neutros (transferência, redistribuição de tarefas) que carecem de
   justificativa documentada.
3. **Fechamento por mecanismo administrativo de baixa exposição pública** — o caso é
   formalmente encerrado por instrumento correicional (ex.: Termo de Ajustamento de Conduta)
   sem que haja divulgação pública de sanção proporcional ao relato (afastamento, remoção
   do posto, processo disciplinar formal, publicização do teor do acordo).

**Distinção de padrões adjacentes (não colapsar):**

| Padrão | Diferença central |
|---|---|
| P02 (investigador vira investigado) | P02 é reversão de polo em persecução *penal/investigativa*; P13 é retaliação *administrativa* contra denunciante, sem persecução penal envolvida. |
| P06 (prescrição/exaustão do ciclo) | P06 opera por consumo de *tempo* processual (prescrição). P13-A opera por *absorção administrativa* (TAC fecha o caso independentemente do tempo decorrido). Mecanismo de exaustão análogo, mas não idêntico. |
| P09 (captura cultural) | P09 é produção de legitimidade simbólica externa; P13 é dinâmica interna de carreira de Estado, sem componente de legitimação cultural. |

## Subpadrões

- **P13-A · Fechamento por TAC** — uso de Termo de Ajustamento de Conduta (ou instrumento
  correicional equivalente) como desfecho formal que absorve a apuração sem sanção
  disciplinar pública proporcional.
- **P13-B · Retaliação por transferência** — remoção ou realocação de servidor que formaliza
  queixa, sob justificativa administrativa formalmente neutra, ampliando o receio de
  denúncia entre pares (efeito "silenciamento" documentado nas próprias cartas do caso
  fundador).

## Evento-âncora fundador

- **Consulado-Geral do Brasil em Hong Kong** — cartas coletivas de 04/03/2026 e 24/04/2026
  ao Itamaraty via Sinditamaraty; TAC assinado por Wladimir Valler Filho e Hervelter de
  Mattos após procedimento na Corregedoria do Serviço Exterior. Ver JSON staging
  `todo_consulado-hongkong-valler-filho.json`.

## Lacuna estrutural do próprio padrão candidato

Sem 2º e 3º evento-âncora, não é possível afirmar se (1) o TAC é mecanismo padrão de
fechamento de casos de assédio no Itamaraty ou instrumento pontual, e (2) se o padrão se
generaliza a outras carreiras de Estado não-judiciais. Buscar precedentes — outras
correições do serviço exterior com desfecho por TAC, casos análogos em carreiras
policiais/regulatórias — antes de qualquer classificação definitiva.

---

## Snippet HTML — pattern-card (uso condicional, NÃO mesclar ao dashboard de produção
## enquanto P13 permanecer candidato; manter em holding/"padrões emergentes")

```html
<div class="pattern-card" style="border-left-color:var(--gray); opacity:0.85;">
  <div class="pattern-title">
    <span class="badge b-gray">P13 · candidato</span>
    Captura hierárquica em carreira de Estado não-judicial
  </div>
  <div class="pattern-body">
    Concentração de autoridade unilateral em carreira de Estado fora do Judiciário +
    retaliação administrativa (transferência) contra quem formaliza queixa + fechamento
    via mecanismo correicional de baixa exposição pública (TAC), sem sanção proporcional
    divulgada. <strong>1 evento-âncora</strong> (Consulado-Geral do Brasil em Hong Kong,
    2026) — aguardando corroboração (mínimo 3 eventos-âncora, critério METHODOLOGY.md)
    antes de promoção a padrão confirmado.
  </div>
</div>
```

## Deploy checklist

- [ ] Reconsultar `claude.ai-corpus-ids-sync.json` (inacessível nesta sessão) para obter
      IDs main track e thematic track reais — substituir `__PENDENTE_SYNC__`.
- [ ] Mover JSON de `_data/todo/` para `_data/` via `merge_todo_pending.py` somente após
      atribuição de ID.
- [ ] **Não** inserir o pattern-card P13 em `padroes-sistemicos-dashboard.html` como padrão
      pleno — manter em área de "padrões emergentes/sob observação" até 2º/3º
      evento-âncora.
- [ ] Monitorar: status de Valler Filho e Mattos no posto; teor do TAC se tornar público;
      possíveis novos relatos em outras unidades do serviço exterior.
- [ ] Rodar `validate-ids.ps1` após merge definitivo.
