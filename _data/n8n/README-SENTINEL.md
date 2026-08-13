# SENTINEL — Agente n8n de Extração Diária (lawfare-timeline)

## O que este agente faz e o que ele NÃO faz

**Faz:** roda 1x/dia, busca notícias por categoria via Google News RSS, filtra as últimas 48h,
pede ao Claude para classificar cada artigo contra P01–P12 e as 7 categorias operacionais do
schema, tenta achar automaticamente uma 2ª fonte independente para cada candidato, monta um lote
JSON no formato de `prompt-sistema-lawfare-ai.md` e sobe pro Google Drive em
`candidatos-triagem/candidatos-triagem-{data}.json`.

**NÃO faz:**
- Não atribui `id`. IDs continuam exclusivamente atribuídos por você (ou por mim, em sessão),
  sempre consultando `claude.ai-corpus-ids-sync.json` ao vivo. Todo candidato sai com
  `"id": null` e uma nota `_nota_id`.
- Não grava `evidence_status: "ev-confirmed"` nunca, mesmo quando acha uma 2ª fonte. Marca
  `_flag_possivel_ev_confirmed: true` + `_flag_motivo` explicando o que achou, para você verificar
  o **conteúdo** do link (não só o título) antes de promover.
- Não escreve em `_data/todo/` nem faz merge em `lawfare.json`. Fica no Drive até você revisar.

Isso preserva o protocolo anti-confirmation-bias e a regra "nunca ev-confirmed de memória do
modelo sem fonte verificada por humano".

## Arquitetura (3 fases dentro de um único workflow)

```
Schedule Trigger (07:00 BRT)
  → Config Categorias (7 categorias, cada uma com patterns P0X prioritários + query RSS)
  → LOOP 1 (categorias)
      → busca RSS da categoria (janela 2 dias)
      → parse XML→JSON
      → extrai itens + dedupe (contra URLs já vistas, guardadas em static data)
      → para cada artigo: Claude classifica (candidato | descartar)
      → acumula candidatos "Fase 1" em static data
  → LOOP 2 (candidatos da Fase 1)
      → busca RSS de corroboração (termos extraídos pelo próprio Claude na Fase 1)
      → conta fontes independentes (domínio ≠ domínio original)
      → monta objeto final no schema do corpus
      → acumula em static data
  → Monta lote final (JSON) + limpa acumuladores
  → Upload no Google Drive (candidatos-triagem/)
```

## Passo a passo de instalação

1. **Importar o workflow**
   No n8n: Workflows → Import from File → selecione `sentinel-extracao-diaria-lawfare.json`.

2. **Credencial Anthropic**
   O node "Classificar com Claude (Fase 1)" espera uma API key da Anthropic. Duas opções:
   - Mais simples: trocar o header `x-api-key` no node por um valor fixo (sua key), ou
   - Recomendado: criar uma credencial genérica no n8n (HTTP Header Auth ou Anthropic, se seu n8n
     tiver o node nativo) e referenciar `{{ $credentials... }}` — ajuste conforme a versão do seu n8n.
   - Verifique o nome do modelo (`claude-sonnet-4-6`) contra o que está disponível na sua conta —
     troque se necessário.

3. **Credencial Google Drive**
   No node "Upload Google Drive": conectar sua conta OAuth2, e trocar
   `folderId.value` (hoje `COLOCAR_ID_DA_PASTA_candidatos-triagem`) pelo ID real da pasta
   `candidatos-triagem/` no seu Drive. Crie essa pasta antes se ainda não existir.

4. **Fuso horário**
   O cron está em `0 10 * * *` (10:00 UTC = 07:00 America/Sao_Paulo). Se o timezone do seu n8n
   (Settings → Timezone) já estiver em `America/Sao_Paulo`, troque o cron para `0 7 * * *` direto.

5. **Testar manualmente antes de ativar**
   Rode "Execute Workflow" manualmente uma vez. Cheque o node "Montar Lote Final" — confira se
   `total_candidatos` é um número razoável (não zero por erro de config, não centenas por RSS mal
   filtrado). Só depois ative o Schedule Trigger.

## Ajustando as categorias e queries

O node "Config Categorias" (Code) tem o array `categorias` com `categoria`, `patterns` e `query`
por categoria. É texto puro — editar ali para afinar termos de busca conforme o corpus evoluir
(ex.: adicionar nomes de operações ativas, atores recorrentes). `analise_editorial` e
`lacuna_investigativa` ficam de fora de propósito — são categorias de síntese que você/eu
produzimos manualmente, não são "notícia do dia".

## Fluxo de revisão diária (o que você faz com a saída)

1. Abra `candidatos-triagem-{data}.json` no Drive.
2. Para cada candidato com `_flag_possivel_ev_confirmed: true`: abra os 2-3 links em `sources[]`,
   confirme que tratam do MESMO evento (não falso-positivo de busca), então decida se sobe pra
   `ev-confirmed` manualmente.
3. Descarte candidatos malformados ou fora de escopo (o classificador erra ocasionalmente —
   é triagem, não veredito).
4. Cole os sobreviventes em `lawfare-batch-YYYY-MM-DD.json` no schema completo, atribuindo `id`
   só depois de consultar `claude.ai-corpus-ids-sync.json` ao vivo (comigo, em sessão, se preferir
   automatizar essa parte também).
5. Salve em `_data/todo/`, rode `merge_todo_pending.py`, valide com `validate-ids.ps1`.

## Limitações conhecidas

- Google News RSS não tem rate-limit documentado publicamente, mas é bom não reduzir o intervalo
  abaixo de 1x/dia sem checar comportamento.
- A "corroboração automática" busca por título/termos, não por conteúdo semântico — pode falso-
  positivar (achar artigo correlato mas não idêntico) ou falso-negativar (2ª fonte existe mas usa
  termos muito diferentes). Por isso o teto é `ev-alleged` sempre, nunca `ev-confirmed` automático.
- `date` do evento (campo `date` no schema) vem do que o Claude extraiu do texto — pode ser a data
  da publicação em vez da data do evento relatado, quando o artigo não deixa isso claro. Checar em
  revisão manual, especialmente para `date_precision: "month"` ou `"year"`.
