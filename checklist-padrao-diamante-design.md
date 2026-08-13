# Checklist "Padrão Diamante" — Design Web de Elite
### Baseado nos critérios reais de Awwwards e CSS Design Awards, aplicado ao seu ecossistema

---

## 1. As duas rubricas oficiais (o que os jurados de verdade pontuam)

### Awwwards — 4 critérios, pesos declarados
| Critério | Peso | O que avalia |
|---|---|---|
| **Design** | 40% | Estética, tipografia, paleta, hierarquia visual |
| **Usabilidade (UX)** | 30% | Navegação, clareza, fricção zero |
| **Criatividade** | 20% | Originalidade conceitual, não-genérico |
| **Conteúdo** | 10% | Qualidade e relevância do texto/mídia |

### CSS Design Awards — 3 critérios, pesos declarados
| Critério | Peso | O que avalia |
|---|---|---|
| **UI Design** | 40% | Craft visual — grid, espaçamento, cor, tipo |
| **UX Design** | 30% | Fluxo, arquitetura de informação, acessibilidade |
| **Inovação** | 30% | Técnica nova ou aplicação inédita de técnica conhecida |

**Corte de qualidade CSSDA:** nota média acima de 8.00 = Website of the Day. Abaixo de 8, mas acima de 6 = Special Kudos.

---

## 2. Onde isso bate direto com seus projetos

Seu ecossistema já tem uma vantagem que a maioria dos concorrentes de prêmio não tem: **conteúdo real, taxonomia rigorosa, e uma identidade visual coerente** (Playfair Display / EB Garamond / IBM Plex Mono, fundo escuro, estampas de classificação de evidência). Isso cobre sozinho quase 40% da nota em qualquer uma das duas rubricas — a maioria dos sites premiados tem UI bonita e conteúdo vazio; o seu tem o oposto do problema comum.

O gap está em **UX/Navegação** e **Inovação técnica de interface**, que são pontos que exigem decisões de front-end, não de conteúdo.

---

## 3. Checklist aplicável — República Sequestrada / lawfare-timeline / Sabor Brazil

### 🎨 Design / UI (40%)
- [ ] Escala tipográfica consistente definida em tokens (não "achismo" por página) — Playfair Display para headlines, EB Garamond para corpo longo, IBM Plex Mono para metadados/timestamps/IDs (ev-confirmed, P01–P13 etc.)
- [ ] Paleta com no máximo 1 cor de destaque sobre o fundo escuro (evitar "efeito painel de alerta" com múltiplas cores de status competindo)
- [ ] Espaçamento vertical rítmico (8px ou 4px grid) — timelines com 1.700+ entradas sofrem muito quando o espaçamento é inconsistente
- [ ] Estados de hover/focus desenhados intencionalmente, não deixados no default do browser
- [ ] Ícones de classificação de evidência (ev-confirmed/contested/alleged/inference) como sistema visual único e reconhecível — hoje isso é sua marca registrada, vale reforçar como um "selo"

### 🧭 UX / Navegação (30%)
- [ ] Busca funcional e visível acima da dobra em qualquer página com mais de ~50 itens (lawfare-timeline com 1.700+ entradas — confirmar se Pagefind já está em produção ou ainda no plano de migração)
- [ ] Filtro por padrão sistêmico (P01–P12) e por classificação de evidência disponível na UI, não só no schema JSON
- [ ] Breadcrumb ou indicador de "onde estou" dentro do hub (com 6 propriedades sob República Sequestrada, perder o usuário é fácil)
- [ ] Tempo de carregamento da timeline principal sob 2s mesmo com 1.700+ entries (paginação de 50/página ajuda, mas confirmar lazy-load de mídia)
- [ ] Mobile first de verdade — jurados testam em device real, não emulador

### 💡 Criatividade / Inovação (20–30%)
- [ ] Visualização de dados própria para os padrões P01–P13 (rede/grafo de atores transversais entre operações — Castelo de Areia → Lava Jato → Compliance Zero) em vez de apenas lista cronológica
- [ ] Modo de leitura "camada rasa vs. camada profunda" — resumo executivo colapsável antes do corpo denso de cada entrada, para diferenciar leitor casual de pesquisador
- [ ] Uma assinatura de interação exclusiva do hub (ex: scroll que revela a "linha do tempo" fisicamente conforme o usuário avança) — isso é o tipo de detalhe que garante nota de Inovação alta

### 📄 Conteúdo (10%, mas seu ponto mais forte)
- [x] Atribuição nomeada, fontes checáveis, datas — já é padrão do seu workflow
- [x] Separação estrita ev-confirmed vs. ev-inference — já implementado
- [ ] Meta descriptions e OG images customizadas por entrada relevante (afeta como o conteúdo aparece quando compartilhado no X — conecta direto com sua estratégia de distribuição)

---

## 4. Prioridade de ataque (ordem sugerida)

1. **Pagefind em produção** no lawfare-timeline — resolve UX de busca, é o maior ganho por menor esforço dado que já está no seu roadmap de migração Astro
2. **Sistema de tokens de design** (cor/tipo/espaçamento) documentado uma vez e aplicado nas 6 propriedades do hub — resolve a maior parte de "Design" e "UI"
3. **Visualização de rede dos padrões P01–P13** — é o item de maior impacto em "Criatividade/Inovação" porque não existe hoje e é conceitualmente único ao seu projeto
4. Selo visual de classificação de evidência como componente reutilizável — pequeno esforço, reforça identidade em toda navegação

---

*Este checklist não é um selo oficial de nenhuma das duas premiações — é uma tradução prática dos critérios publicados por Awwwards e CSS Design Awards aplicada ao seu stack (Astro migration, Pagefind, schema v2.4).*
