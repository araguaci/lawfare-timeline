# commit-t216-t217.ps1
# Execute dentro do diretorio raiz do repo lawfare-timeline (onde está a pasta _posts/)

git add _posts/tse/2026-06-29-tse-usaid-parceria-censura-seletiva.md
git add _posts/tse/2026-06-29-seletividade-punitiva-tse-casos-isolados.md

git commit -m "docs: adiciona T-216 (TSE-USAID) e T-217 (lacuna seletividade punitiva)" `
  -m "- T-216: parceria TSE-USAID 2021-2025, ev-contested, separa repasses confirmados (Instituto Vero, US`$250k Open Society, R`$170k Embaixada EUA) de alegacao nao-corroborada de direcionamento seletivo" `
  -m "- T-217: registra lacuna metodologica real (nao achado) sobre tese de seletividade punitiva por facao; corrige confusao com ID 180 real (inelegibilidade/cassacao, ja confirmado)" `
  -m "Patterns: P04, P04b, P09" `
  -m "Tracks: thematic 216, 217 | proximo livre: 218"

git push
