# 📖 Como Usar o Prompt de Vaza Toga e Controle de Mídia

## 🎯 Objetivo

Este guia explica como usar o arquivo `PROMPT-VAZATOGA-MIDIA.md` com ferramentas de IA para pesquisar assuntos relacionados à Vaza Toga, perseguição a jornalistas, Eduardo Tagliaferro, aumento da censura e controle das mídias.

---

## 🤖 Ferramentas Recomendadas

### 1. **Claude (Anthropic)** ⭐ Recomendado
- Melhor para: Análise complexa de revelações e geração de JSON estruturado
- URL: https://claude.ai
- Como usar: Cole o conteúdo de `PROMPT-VAZATOGA-MIDIA.md` na conversa

### 2. **Perplexity AI** ⭐ Recomendado para Pesquisa
- Melhor para: Pesquisa com fontes verificadas de jornalismo investigativo
- URL: https://www.perplexity.ai
- Como usar: Use o prompt como base e peça para pesquisar com citações de fontes jornalísticas

### 3. **ChatGPT (OpenAI)**
- Melhor para: Pesquisa e síntese de informações sobre liberdade de imprensa
- URL: https://chat.openai.com
- Como usar: Cole o prompt completo e peça para pesquisar eventos após 18/11/2025

---

## 📝 Passo a Passo

### Passo 1: Preparar o Prompt

1. Abra o arquivo `PROMPT-VAZATOGA-MIDIA.md`
2. Copie todo o conteúdo
3. Ou use apenas a seção relevante se a ferramenta tiver limite de tokens

### Passo 2: Executar a Pesquisa

**Exemplo de comando para a IA:**

```
[Cole aqui o conteúdo de PROMPT-VAZATOGA-MIDIA.md]

Por favor, pesquise eventos relacionados à Vaza Toga, perseguição a jornalistas, Eduardo Tagliaferro, aumento da censura e controle das mídias que ocorreram após 18 de novembro de 2025 e retorne o JSON estruturado conforme especificado.
```

### Passo 3: Validar a Resposta

1. Verifique se o JSON está válido
2. Confirme que as datas são posteriores a 17/11/2025
3. Valide categorias e tags (devem estar na lista fornecida)
4. Verifique se há fontes incluídas
5. Confirme que o impacto na liberdade de imprensa foi avaliado
6. Verifique se o tipo de perseguição foi identificado

---

## 🔧 Script Python para Validação

```python
import json
from datetime import datetime
from pathlib import Path

def validar_resposta_vazatoga(arquivo_json):
    """Valida JSON retornado pela IA para Vaza Toga e controle de mídia"""
    
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
            'relevancia', 'impacto_liberdade_imprensa', 
            'tipo_perseguicao', 'pais'
        ]
        
        for campo in campos_obrigatorios:
            assert campo in assunto, f"Campo obrigatório '{campo}' ausente"
        
        # Validar data
        data_evento = datetime.fromisoformat(assunto['data_evento'])
        data_corte = datetime(2025, 11, 17)
        assert data_evento > data_corte, f"Data {assunto['data_evento']} deve ser posterior a 17/11/2025"
        
        # Validar categoria
        categorias_validas = [
            "vazatoga", "lawfare", "censura", "escandalos",
            "stf", "tse", "operacoes", "dossie", "estudos"
        ]
        assert assunto['categoria'] in categorias_validas, f"Categoria inválida: {assunto['categoria']}"
        
        # Validar impacto na liberdade de imprensa
        assert assunto['impacto_liberdade_imprensa'] in ['alto', 'medio', 'baixo'], "Impacto na liberdade de imprensa inválido"
        
        # Validar tipo de perseguição
        assert assunto['tipo_perseguicao'] in ['judicial', 'censura', 'ameaca', 'processo', 'bloqueio', 'N/A'], "Tipo de perseguição inválido"
        
        # Validar número de tags
        assert len(assunto['tags']) <= 10, f"Máximo de 10 tags permitido, encontrado {len(assunto['tags'])}"
        
        # Validar relevância
        assert assunto['relevancia'] in ['alta', 'media', 'baixa'], "Relevância deve ser 'alta', 'media' ou 'baixa'"
    
    print(f"✅ JSON válido! {dados['total']} assuntos encontrados.")
    return dados

# Exemplo de uso
if __name__ == "__main__":
    dados = validar_resposta_vazatoga("resposta-vazatoga.json")
    
    # Ordenar por prioridade e impacto na liberdade de imprensa
    assuntos_ordenados = sorted(
        dados['assuntos'], 
        key=lambda x: (
            x.get('prioridade', 999),
            {'alto': 1, 'medio': 2, 'baixo': 3}.get(x.get('impacto_liberdade_imprensa', 'baixo'), 3)
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
    
    # Exibir resumo por tipo de perseguição
    print("\n📊 Resumo por Tipo de Perseguição:")
    tipos = {}
    for assunto in assuntos_ordenados:
        tipo = assunto.get('tipo_perseguicao', 'N/A')
        tipos[tipo] = tipos.get(tipo, 0) + 1
    
    for tipo, count in sorted(tipos.items()):
        print(f"  {tipo}: {count}")
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
- [ ] Impacto na liberdade de imprensa foi avaliado
- [ ] Tipo de perseguição foi identificado
- [ ] Fontes incluídas quando disponíveis
- [ ] Pessoas envolvidas foram incluídas (Tagliaferro, jornalistas)

---

## 🎨 Criar Posts a Partir do JSON

```python
from datetime import datetime
import json
import re

def criar_post_vazatoga(assunto, output_dir="_posts"):
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
    
    # Escolher emoji baseado no tipo de perseguição
    emojis = {
        'judicial': '⚖️',
        'censura': '🚫',
        'ameaca': '⚠️',
        'processo': '📜',
        'bloqueio': '🔒',
        'N/A': '📰'
    }
    emoji = emojis.get(assunto.get('tipo_perseguicao', 'N/A'), '📰')
    
    # Escolher ícone baseado na categoria
    icones = {
        'vazatoga': '/assets/solid/shield-virus.svg',
        'lawfare': '/assets/solid/scale.svg',
        'censura': '/assets/solid/ban.svg',
        'escandalos': '/assets/solid/file-shield.svg',
        'stf': '/assets/solid/gavel.svg',
        'tse': '/assets/solid/check-circle.svg',
        'operacoes': '/assets/solid/shield-check.svg',
        'dossie': '/assets/solid/folder.svg',
        'estudos': '/assets/solid/file-shield.svg'
    }
    icone = icones.get(categoria, '/assets/solid/file-shield.svg')
    
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

**Impacto na Liberdade de Imprensa:** {assunto.get('impacto_liberdade_imprensa', 'N/A').title()}  
**Tipo de Perseguição:** {assunto.get('tipo_perseguicao', 'N/A').title()}

***

## 🏁 Introdução

[Conteúdo a ser desenvolvido baseado nas fontes fornecidas e contexto da Vaza Toga]

## 📊 Análise

### Impacto na Liberdade de Imprensa

[Análise do impacto na liberdade de imprensa e democracia]

### Detalhes do Caso

[Detalhamento da perseguição, censura ou controle de mídia]

### Reações e Consequências

[Reações de organizações de defesa da imprensa, jornalistas, sociedade]

## 🎯 Conclusão

[Conclusões sobre o impacto na liberdade de imprensa, democracia e estado de direito]

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
with open("resposta-vazatoga.json", 'r', encoding='utf-8') as f:
    dados = json.load(f)

# Ordenar por prioridade
assuntos_ordenados = sorted(
    dados['assuntos'], 
    key=lambda x: x.get('prioridade', 999)
)

for assunto in assuntos_ordenados:
    criar_post_vazatoga(assunto)
```

---

## 🔄 Fluxo Completo

1. **Pesquisar** → Use o prompt com ferramenta de IA (Claude ou Perplexity recomendados)
2. **Validar** → Verifique o JSON retornado usando o script Python
3. **Processar** → Organize por prioridade e impacto na liberdade de imprensa
4. **Criar Posts** → Gere arquivos markdown automaticamente
5. **Revisar** → Adicione conteúdo detalhado aos posts
6. **Publicar** → Commit e push para o repositório

---

## ⚠️ Avisos Importantes

- **Sempre valide** o JSON antes de usar
- **Verifique as fontes** fornecidas pela IA
- **Priorize** assuntos com alto impacto na liberdade de imprensa
- **Não publique** conteúdo sem revisão humana
- **Mantenha** o tom neutro e factual do projeto
- **Respeite** as regras de categorias e tags
- **Foque** em eventos com impacto na democracia e liberdade de imprensa

---

## 📚 Recursos Adicionais

- `PROMPT-VAZATOGA-MIDIA.md` - Prompt completo para pesquisa
- `.cursorrules` - Regras completas do projeto
- `REGRAS-CURSOR.md` - Resumo rápido das regras

---

## 🎯 Dicas de Pesquisa

### Para Melhores Resultados:

1. **Use Perplexity AI** para pesquisas com fontes jornalísticas verificadas
2. **Especifique fontes jornalísticas** (The Intercept, O Antagonista, etc.)
3. **Peça citações** de organizações de defesa da imprensa
4. **Solicite informações** sobre Tagliaferro e outros denunciantes
5. **Peça avaliação de impacto** na liberdade de imprensa específica
6. **Solicite contexto** sobre Vaza Toga e sistema de censura

### Exemplo de Comando Avançado:

```
[Cole o prompt]

Por favor, pesquise eventos relacionados à Vaza Toga, perseguição a jornalistas e controle de mídia que ocorreram após 18/11/2025, priorizando:
1. Novas revelações da Vaza Toga
2. Situação de Eduardo Tagliaferro e outros denunciantes
3. Perseguição a jornalistas (processos, prisões, bloqueios)
4. Aumento da censura digital
5. Controle de mídia e propaganda

Inclua fontes de:
- Jornalismo investigativo (The Intercept, O Antagonista)
- Organizações de defesa da imprensa (Artigo 19, CPJ, RSF)
- Veículos independentes (Gazeta do Povo, Jovem Pan)
- Investigadores (David Ágape, Eli Vieira)

Retorne o JSON estruturado conforme especificado.
```

---

**Última atualização:** 2025-01-27

