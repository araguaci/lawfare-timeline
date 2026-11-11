# Protocolo de Preservação 8/jan · INQ 4.781 (CC0 1.0)

| Arquivo | Destino no repo | O que é |
|---|---|---|
| `inventario-fontes-8jan-inq4781.json` / `.csv` | `_data/preservacao/` | 72 entradas do corpus ligadas a 8/jan e INQ 4.781, cada fonte classificada e com flags de auditoria |
| `preservar_fontes.py` | `tools/` | Baixa cada fonte, calcula SHA-256, pede snapshot ao Wayback e grava tudo no inventário |
| `thematic-T275-memoria-institucional-8jan.json` | `_data/processados/` | T-275 publicado em 2026-11-11: linha do tempo de manifestações e omissões de OAB, DPU, IDDD, HRW e ONGs brasileiras |

## Rodar a preservação (na sua máquina)
    python preservar_fontes.py --so-oficiais     # primeiro as fontes oficiais
    python preservar_fontes.py                   # depois todas (≈6 s por URL)

Cópias ficam em `./acervo/`. Fontes que só existem no `.md` do post entram automaticamente como `tipo: post_md`.

## Flags do inventário
- `SEM_FONTE_VERIFICAVEL` — `fontes: ["N/A"]` no lawfare.json
- `FONTE_SO_NO_POST_MD` — a URL existe só no post Jekyll; propagar para o JSON
- `FONTE_UNICA`, `SEM_FONTE_OFICIAL`
- `POSSIVEL_DIVERGENCIA_FONTE_EVENTO` — a fonte não sustenta o evento descrito; revisar antes de preservar

Processado em 2026-11-11. T-275 confirmado. Próximo temático livre: **T-276**.

## Batch 1986–1988 (dia 9/jan e imagens)
Processado em 2026-11-11. Os IDs 1986–1988 já pertenciam a Stoppe/COP28 e Greenwashing. Finais: **2021–2023**. Fé e voto, que também pedia 1986, foi para **2024**. Próximo main livre: **2025**.
- 2021 — Exército barra a PM na noite de 8/1; prisões adiadas para 9/1
- 2022 — ~1.200 levados ao ginásio da ANP; 599 liberados por razões humanitárias
- 2023 — imagens do Palácio da Justiça apagadas (4 de 185 câmeras); sigilo do GSI até abr/2023
