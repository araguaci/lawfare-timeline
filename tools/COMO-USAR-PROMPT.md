# 📖 Como Usar o Prompt de Pesquisa IA

## 🎯 Objetivo

Este guia explica como usar o arquivo `PROMPT-PESQUISA-IA.md` com ferramentas de IA para pesquisar assuntos relacionados ao projeto Lawfare Timeline.

---

## 🤖 Ferramentas Recomendadas

### 1. **Claude (Anthropic)**
- Melhor para: Análise complexa e geração de JSON estruturado
- URL: https://claude.ai
- Como usar: Cole o conteúdo de `PROMPT-PESQUISA-IA.md` na conversa

### 2. **ChatGPT (OpenAI)**
- Melhor para: Pesquisa e síntese de informações
- URL: https://chat.openai.com
- Como usar: Cole o prompt completo e peça para pesquisar eventos após 15/09/2025

### 3. **Perplexity AI**
- Melhor para: Pesquisa com fontes verificadas
- URL: https://www.perplexity.ai
- Como usar: Use o prompt como base e peça para pesquisar com citações

### 4. **Google Gemini**
- Melhor para: Pesquisa ampla e análise
- URL: https://gemini.google.com
- Como usar: Cole o prompt e solicite pesquisa de eventos recentes

---

## 📝 Passo a Passo

### Passo 1: Preparar o Prompt

1. Abra o arquivo `PROMPT-PESQUISA-IA.md`
2. Copie todo o conteúdo
3. Ou use apenas a seção relevante se a ferramenta tiver limite de tokens

### Passo 2: Executar a Pesquisa

**Exemplo de comando para a IA:**

```
[Cole aqui o conteúdo de PROMPT-PESQUISA-IA.md]

Por favor, pesquise eventos relacionados aos temas do projeto Lawfare Timeline que ocorreram após 15 de setembro de 2025 e retorne o JSON estruturado conforme especificado.
```

### Passo 3: Validar a Resposta

1. Verifique se o JSON está válido
2. Confirme que as datas são posteriores a 14/09/2025
3. Valide categorias e tags (devem estar na lista fornecida)
4. Verifique se há fontes incluídas

### Passo 4: Processar os Resultados

Use o JSON retornado para:
- Criar novos posts em `_posts/`
- Atualizar categorias e tags
- Gerar conteúdo baseado nos assuntos identificados

---

## 🔧 Script Python (Opcional)

Crie um script para processar o JSON retornado:

```python
import json
from datetime import datetime
from pathlib import Path

def processar_resposta_ia(arquivo_json):
    """Processa JSON retornado pela IA e valida estrutura"""
    
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
            'categoria', 'tags', 'descricao', 'relevancia', 'pais'
        ]
        
        for campo in campos_obrigatorios:
            assert campo in assunto, f"Campo obrigatório '{campo}' ausente"
        
        # Validar data
        data_evento = datetime.fromisoformat(assunto['data_evento'])
        data_corte = datetime(2025, 9, 14)
        assert data_evento > data_corte, f"Data {assunto['data_evento']} deve ser posterior a 14/09/2025"
        
        # Validar categoria
        categorias_validas = [
            "lawfare", "crise-diplomatica", "justica", "vazatoga",
            "stf", "tse", "escandalos", "bancos", "operacoes",
            "impunidade", "indecoro", "penduricalhos", "extravagancia",
            "dossie", "decano", "estudos"
        ]
        assert assunto['categoria'] in categorias_validas, f"Categoria inválida: {assunto['categoria']}"
        
        # Validar número de tags
        assert len(assunto['tags']) <= 10, f"Máximo de 10 tags permitido, encontrado {len(assunto['tags'])}"
        
        # Validar relevância
        assert assunto['relevancia'] in ['alta', 'media', 'baixa'], "Relevância deve ser 'alta', 'media' ou 'baixa'"
    
    print(f"✅ JSON válido! {dados['total']} assuntos encontrados.")
    return dados

# Exemplo de uso
if __name__ == "__main__":
    dados = processar_resposta_ia("exemplo-resposta-ia.json")
    
    # Ordenar por prioridade
    assuntos_ordenados = sorted(
        dados['assuntos'], 
        key=lambda x: x.get('prioridade', 999)
    )
    
    # Exibir resumo
    print("\n📊 Resumo por Categoria:")
    categorias = {}
    for assunto in assuntos_ordenados:
        cat = assunto['categoria']
        categorias[cat] = categorias.get(cat, 0) + 1
    
    for cat, count in sorted(categorias.items()):
        print(f"  {cat}: {count}")
```

---

## 📋 Checklist de Validação

Antes de usar os resultados, verifique:

- [ ] JSON está válido e parseável
- [ ] Todos os eventos são posteriores a 14/09/2025
- [ ] Categorias estão na lista válida
- [ ] Tags estão na lista válida
- [ ] Máximo de 10 tags por assunto
- [ ] Descrições têm no máximo 200 caracteres
- [ ] Títulos estão em português (pt-BR)
- [ ] Datas estão no formato correto (YYYY-MM-DD)
- [ ] Relevância classificada corretamente
- [ ] Fontes incluídas quando disponíveis

---

## 🎨 Criar Posts a Partir do JSON

Após validar o JSON, você pode criar posts automaticamente:

```python
from datetime import datetime
import json

def criar_post_markdown(assunto, output_dir="_posts"):
    """Cria arquivo markdown de post a partir de assunto do JSON"""
    
    # Gerar nome do arquivo
    data = assunto['data_evento']
    titulo_slug = assunto['titulo'].lower()
    titulo_slug = titulo_slug.replace(' ', '-')
    titulo_slug = ''.join(c for c in titulo_slug if c.isalnum() or c == '-')
    
    nome_arquivo = f"{data}-{titulo_slug}.md"
    
    # Determinar pasta da categoria
    categoria = assunto['categoria']
    pasta = f"{output_dir}/{categoria}"
    Path(pasta).mkdir(parents=True, exist_ok=True)
    
    caminho_completo = f"{pasta}/{nome_arquivo}"
    
    # Criar front matter
    front_matter = f"""---
title: "{assunto['titulo']}"
description: "{assunto['descricao']}"
date: {assunto['data_iso']}
image:
  path: "/assets/solid/scale.svg"
tags: {assunto['tags']}
categories: {categoria}
---

- &nbsp;
{{:toc .large-only}}

# {assunto['titulo']}

***

## 🧭 Resumo

{assunto['descricao']}

***

## 🏁 Introdução

[Conteúdo a ser desenvolvido baseado nas fontes fornecidas]

## 📊 Análise

[Análise detalhada do assunto]

## 🎯 Conclusão

[Conclusões e implicações]

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
with open("exemplo-resposta-ia.json", 'r', encoding='utf-8') as f:
    dados = json.load(f)

for assunto in dados['assuntos']:
    criar_post_markdown(assunto)
```

---

## 🔄 Fluxo Completo

1. **Pesquisar** → Use o prompt com ferramenta de IA
2. **Validar** → Verifique o JSON retornado
3. **Processar** → Use script Python para validar e organizar
4. **Criar Posts** → Gere arquivos markdown automaticamente
5. **Revisar** → Adicione conteúdo detalhado aos posts
6. **Publicar** → Commit e push para o repositório

---

## ⚠️ Avisos Importantes

- **Sempre valide** o JSON antes de usar
- **Verifique as fontes** fornecidas pela IA
- **Não publique** conteúdo sem revisão humana
- **Mantenha** o tom neutro e factual do projeto
- **Respeite** as regras de categorias e tags

---

## 📚 Recursos Adicionais

- `.cursorrules` - Regras completas do projeto
- `REGRAS-CURSOR.md` - Resumo rápido das regras
- `exemplo-resposta-ia.json` - Exemplo de JSON válido

---

**Última atualização:** 2025-01-27

