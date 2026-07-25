#!/usr/bin/env bash
# Pílula de Ironia — tese Loop de Extração Perpétua (Correios/BNDES)
# lawfare-timeline · gerado 21/07/2026
#
# Uso: bash enviar_pilula_correios_bndes.sh
# Requer: curl. Opcional: jq (para pretty-print da resposta).

set -euo pipefail

ENDPOINT="https://pilula-de-ironia.vercel.app/api/gerar"

read -r -d '' PAYLOAD <<'EOF' || true
{
  "texto": "Estatal acumula 14 trimestres seguidos de prejuízo. União garante novo empréstimo bancário para cobrir o rombo. Contrato obriga o próprio Tesouro a injetar mais dinheiro depois, sob pena de vencimento antecipado da dívida. Bancos cobram até 120% do CDI, sem risco. O risco é todo do pagador de imposto, que também é quem, no fim, garante o próprio empréstimo que financia seu próprio calote.",
  "autores": ["millor", "lessa"],
  "acidez": 3
}
EOF

echo "→ Enviando paciente para ${ENDPOINT} ..." >&2

RESPONSE=$(curl -sS -X POST "${ENDPOINT}" \
  -H "Content-Type: application/json" \
  -d "${PAYLOAD}")

if command -v jq >/dev/null 2>&1; then
  echo "${RESPONSE}" | jq .
else
  echo "${RESPONSE}"
fi

echo "" >&2
echo "Nota: rate limit é 8 requisições / 10min por IP. Se estourar (429), aguarde." >&2
