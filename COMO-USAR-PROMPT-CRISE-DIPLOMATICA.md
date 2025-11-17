# 📖 Como Usar o Prompt de Crise Diplomática Brasil/EUA

## 🎯 Objetivo

Este guia explica como usar o arquivo `PROMPT-CRISE-DIPLOMATICA.md` com ferramentas de IA para pesquisar assuntos relacionados à crise diplomática Brasil-EUA, relações internacionais, escândalos de corrupção, mau uso de verba pública e vexames do governo brasileiro.

---

## 🤖 Ferramentas Recomendadas

### 1. **Claude (Anthropic)** ⭐ Recomendado
- Melhor para: Análise complexa de relações internacionais e geração de JSON estruturado
- URL: https://claude.ai
- Como usar: Cole o conteúdo de `PROMPT-CRISE-DIPLOMATICA.md` na conversa

### 2. **Perplexity AI** ⭐ Recomendado para Pesquisa
- Melhor para: Pesquisa com fontes verificadas e citações internacionais
- URL: https://www.perplexity.ai
- Como usar: Use o prompt como base e peça para pesquisar com citações de fontes internacionais

### 3. **ChatGPT (OpenAI)**
- Melhor para: Pesquisa e síntese de informações diplomáticas
- URL: https://chat.openai.com
- Como usar: Cole o prompt completo e peça para pesquisar eventos após 18/11/2025

### 4. **Google Gemini**
- Melhor para: Pesquisa ampla e análise de relações internacionais
- URL: https://gemini.google.com
- Como usar: Cole o prompt e solicite pesquisa de eventos recentes

---

## 📝 Passo a Passo

### Passo 1: Preparar o Prompt

1. Abra o arquivo `PROMPT-CRISE-DIPLOMATICA.md`
2. Copie todo o conteúdo
3. Ou use apenas a seção relevante se a ferramenta tiver limite de tokens

### Passo 2: Executar a Pesquisa

**Exemplo de comando para a IA:**

```
[Cole aqui o conteúdo de PROMPT-CRISE-DIPLOMATICA.md]

Por favor, pesquise eventos relacionados à crise diplomática Brasil-EUA, escândalos de corrupção, mau uso de verba pública e vexames do governo brasileiro que ocorreram após 18 de novembro de 2025 e retorne o JSON estruturado conforme especificado.
```

### Passo 3: Validar a Resposta

1. Verifique se o JSON está válido
2. Confirme que as datas são posteriores a 17/11/2025
3. Valide categorias e tags (devem estar na lista fornecida)
4. Verifique se há fontes incluídas
5. Confirme que o impacto diplomático foi avaliado
6. Verifique se o tipo de escândalo foi identificado

### Passo 4: Processar os Resultados

Use o JSON retornado para:
- Criar novos posts em `_posts/`
- Priorizar por impacto diplomático
- Organizar por tipo de escândalo
- Gerar conteúdo baseado nos assuntos identificados

---

## 🔧 Script Python para Validação

```python
import json
from datetime import datetime
from pathlib import Path

def validar_resposta_crise_diplomatica(arquivo_json):
    """Valida JSON retornado pela IA para crise diplomática"""
    
    with open(arquivo_json, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    # Validar estrutura
    assert 'assuntos' in dados, "JSON deve conter 'assuntos'"
    assert 'total' in dados, "JSON deve conter 'total'"
    
    # Validar cada assunto
    for assunto in dados['assuntos']:
        # Verificar campos obrigatórios
        campos_obrigatorios = [
            'titulo', 'data_evento', 'data_iso', 
            'categoria', 'tags', 'descricao', 
            'relevancia', 'impacto_diplomatico', 
            'tipo_escandalo', 'pais'
        ]
        
        for campo in campos_obrigatorios:
            assert campo in assunto, f"Campo obrigatório '{campo}' ausente"
        
        # Validar data
        data_evento = datetime.fromisoformat(assunto['data_evento'])
        data_corte = datetime(2025, 11, 17)
        assert data_evento > data_corte, f"Data {assunto['data_evento']} deve ser posterior a 17/11/2025"
        
        # Validar categoria
        categorias_validas = [
            "crise-diplomatica", "escandalos", "extravagancia",
            "indecoro", "bancos", "operacoes", "lawfare",
            "justica", "estudos"
        ]
        assert assunto['categoria'] in categorias_validas, f"Categoria inválida: {assunto['categoria']}"
        
        # Validar impacto diplomático
        assert assunto['impacto_diplomatico'] in ['alto', 'medio', 'baixo'], "Impacto diplomático inválido"
        
        # Validar tipo de escândalo
        assert assunto['tipo_escandalo'] in ['corrupcao', 'gastos', 'vexame', 'diplomatico', 'N/A'], "Tipo de escândalo inválido"
        
        # Validar número de tags
        assert len(assunto['tags']) <= 10, f"Máximo de 10 tags permitido, encontrado {len(assunto['tags'])}"
        
        # Validar relevância
        assert assunto['relevancia'] in ['alta', 'media', 'baixa'], "Relevância deve ser 'alta', 'media' ou 'baixa'"
    
    print(f"✅ JSON válido! {dados['total']} assuntos encontrados.")
    return dados

# Exemplo de uso
if __name__ == "__main__":
    dados = validar_resposta_crise_diplomatica("resposta-crise-diplomatica.json")
    
    # Ordenar por prioridade e impacto diplomático
    assuntos_ordenados = sorted(
        dados['assuntos'], 
        key=lambda x: (
            x.get('prioridade', 999),
            {'alto': 1, 'medio': 2, 'baixo': 3}.get(x.get('impacto_diplomatico', 'baixo'), 3)
        )
    )
    
    # Exibir resumo por categoria
    print("\n📊 Resumo por Categoria:")
    categorias = {}
    for assunto in assuntos_ordenados:
        cat = assunto['categoria']
        categorias[cat] = categorias.get(cat, 0) + 1
    
    for cat, count in sorted(categorias.items()):
        print(f"  {cat}: {count}")
    
    # Exibir resumo por tipo de escândalo
    print("\n📊 Resumo por Tipo de Escândalo:")
    tipos = {}
    for assunto in assuntos_ordenados:
        tipo = assunto.get('tipo_escandalo', 'N/A')
        tipos[tipo] = tipos.get(tipo, 0) + 1
    
    for tipo, count in sorted(tipos.items()):
        print(f"  {tipo}: {count}")
    
    # Exibir resumo por impacto diplomático
    print("\n📊 Resumo por Impacto Diplomático:")
    impactos = {}
    for assunto in assuntos_ordenados:
        impacto = assunto.get('impacto_diplomatico', 'baixo')
        impactos[impacto] = impactos.get(impacto, 0) + 1
    
    for impacto, count in sorted(impactos.items()):
        print(f"  {impacto}: {count}")
```

---

## 📋 Checklist de Validação

Antes de usar os resultados, verifique:

- [ ] JSON está válido e parseável
- [ ] Todos os eventos são posteriores a 17/11/2025
- [ ] Categorias estão na lista válida
- [ ] Tags estão na lista válida
- [ ] Máximo de 10 tags por assunto
- [ ] Descrições têm no máximo 200 caracteres
- [ ] Títulos estão em português (pt-BR)
- [ ] Datas estão no formato correto (YYYY-MM-DD)
- [ ] Impacto diplomático foi avaliado (alto/médio/baixo)
- [ ] Tipo de escândalo foi identificado
- [ ] Valores envolvidos foram incluídos quando aplicável
- [ ] Fontes incluídas quando disponíveis

---

## 🎨 Criar Posts a Partir do JSON

```python
from datetime import datetime
import json
import re

def criar_post_crise_diplomatica(assunto, output_dir="_posts"):
    """Cria arquivo markdown de post a partir de assunto do JSON"""
    
    # Gerar nome do arquivo
    data = assunto['data_evento']
    titulo_slug = assunto['titulo'].lower()
    titulo_slug = re.sub(r'[^\w\s-]', '', titulo_slug)
    titulo_slug = re.sub(r'[-\s]+', '-', titulo_slug)
    
    nome_arquivo = f"{data}-{titulo_slug}.md"
    
    # Determinar pasta da categoria
    categoria = assunto['categoria']
    pasta = f"{output_dir}/{categoria}"
    Path(pasta).mkdir(parents=True, exist_ok=True)
    
    caminho_completo = f"{pasta}/{nome_arquivo}"
    
    # Escolher emoji baseado no tipo de escândalo
    emojis = {
        'corrupcao': '💰',
        'gastos': '💸',
        'vexame': '😳',
        'diplomatico': '🌍',
        'N/A': '📰'
    }
    emoji = emojis.get(assunto.get('tipo_escandalo', 'N/A'), '📰')
    
    # Escolher ícone baseado na categoria
    icones = {
        'crise-diplomatica': '/assets/solid/globe.svg',
        'escandalos': '/assets/solid/shield-exclamation.svg',
        'extravagancia': '/assets/solid/currency-dollar.svg',
        'indecoro': '/assets/solid/face-frown.svg',
        'bancos': '/assets/solid/banknotes.svg',
        'operacoes': '/assets/solid/shield-check.svg',
        'lawfare': '/assets/solid/scale.svg',
        'justica': '/assets/solid/gavel.svg',
        'estudos': '/assets/solid/document-text.svg'
    }
    icone = icones.get(categoria, '/assets/solid/document-text.svg')
    
    # Criar front matter
    front_matter = f"""---
title: "{assunto['titulo']}"
description: "{assunto['descricao']}"
date: {assunto['data_iso']}
image:
  path: "{icone}"
tags: {assunto['tags']}
categories: {categoria}
---

- &nbsp;
{{:toc .large-only}}

# {emoji} {assunto['titulo']}

***

## 🧭 Resumo

{assunto['descricao']}

**Impacto Diplomático:** {assunto.get('impacto_diplomatico', 'N/A').title()}  
**Tipo de Escândalo:** {assunto.get('tipo_escandalo', 'N/A').title()}  
**Valor Envolvido:** {assunto.get('valor_envolvido', 'N/A')}

***

## 🏁 Introdução

[Conteúdo a ser desenvolvido baseado nas fontes fornecidas e contexto da crise diplomática]

## 📊 Análise

### Impacto Diplomático

[Análise do impacto nas relações internacionais]

### Detalhes do Caso

[Detalhamento do escândalo, corrupção, gastos ou vexame]

### Reações Internacionais

[Reações de outros países, organizações internacionais, mídia estrangeira]

## 🎯 Conclusão

[Conclusões sobre o impacto na imagem do Brasil, relações diplomáticas e credibilidade internacional]

## Referências

"""
    
    # Adicionar fontes se disponíveis
    if assunto.get('fontes'):
        for i, fonte in enumerate(assunto['fontes'], 1):
            front_matter += f"- [^{i}]: {fonte}\n"
    
    # Escrever arquivo
    with open(caminho_completo, 'w', encoding='utf-8') as f:
        f.write(front_matter)
    
    print(f"✅ Post criado: {caminho_completo}")
    return caminho_completo

# Exemplo de uso
with open("resposta-crise-diplomatica.json", 'r', encoding='utf-8') as f:
    dados = json.load(f)

# Ordenar por prioridade
assuntos_ordenados = sorted(
    dados['assuntos'], 
    key=lambda x: x.get('prioridade', 999)
)

for assunto in assuntos_ordenados:
    criar_post_crise_diplomatica(assunto)
```

---

## 🔄 Fluxo Completo

1. **Pesquisar** → Use o prompt com ferramenta de IA (Claude ou Perplexity recomendados)
2. **Validar** → Verifique o JSON retornado usando o script Python
3. **Processar** → Organize por prioridade e impacto diplomático
4. **Criar Posts** → Gere arquivos markdown automaticamente
5. **Revisar** → Adicione conteúdo detalhado aos posts
6. **Publicar** → Commit e push para o repositório

---

## ⚠️ Avisos Importantes

- **Sempre valide** o JSON antes de usar
- **Verifique as fontes** fornecidas pela IA
- **Priorize** assuntos com alto impacto diplomático
- **Não publique** conteúdo sem revisão humana
- **Mantenha** o tom neutro e factual do projeto
- **Respeite** as regras de categorias e tags
- **Foque** em eventos com impacto internacional

---

## 📚 Recursos Adicionais

- `PROMPT-CRISE-DIPLOMATICA.md` - Prompt completo para pesquisa
- `.cursorrules` - Regras completas do projeto
- `REGRAS-CURSOR.md` - Resumo rápido das regras
- `exemplo-resposta-ia.json` - Exemplo de JSON válido

---

## 🎯 Dicas de Pesquisa

### Para Melhores Resultados:

1. **Use Perplexity AI** para pesquisas com fontes verificadas
2. **Especifique fontes internacionais** (Reuters, AP, Bloomberg)
3. **Peça citações** de organizações diplomáticas
4. **Solicite valores** quando houver gastos ou desvios
5. **Peça avaliação de impacto** diplomático específica
6. **Solicite contexto** sobre relações bilaterais

### Exemplo de Comando Avançado:

```
[Cole o prompt]

Por favor, pesquise eventos relacionados à crise diplomática Brasil-EUA que ocorreram após 18/11/2025, priorizando:
1. Sanções e retaliações comerciais
2. Escândalos de corrupção com impacto internacional
3. Gastos públicos excessivos que geraram críticas internacionais
4. Vexames diplomáticos em eventos internacionais

Inclua fontes de:
- Agências de notícias internacionais (Reuters, AP, Bloomberg)
- Organizações diplomáticas (Departamento de Estado dos EUA, ONU, OEA)
- Mídia brasileira confiável (G1, Folha, Estadão)

Retorne o JSON estruturado conforme especificado.
```

---

**Última atualização:** 2025-01-27

