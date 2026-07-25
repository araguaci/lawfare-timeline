import pandas as pd
import numpy as np

# ==============================================================================
# CONFIGURAÇÕES DE CAMINHOS E PARÂMETROS
# ==============================================================================
# Caminhos para os arquivos baixados (ajuste conforme seu diretório local)
ARQUIVO_RECEITAS_TSE = "receitas_candidatos_2022_BRASIL.csv"
ARQUIVO_EMPRESAS_RF = "EMPRESAS_DATA_DUMP.csv"  # Ou os arquivos de Estabelecimentos da RF

# CNAEs principais relacionados ao setor farmacêutico (Fabricação e Distribuição)
# 2110-6/00: Fabricação de produtos farmoquímicos
# 2121-1/01: Fabricação de medicamentos para uso humano
# 4644-8/01: Comércio atacadista de medicamentos e drogas de uso humano
CNAES_FARMA = ["2110600", "2121101", "4644801"]

ARQUIVO_SAIDA_JSON = "lawfare_timeline_farma_2022.json"


def limpar_cnpj(coluna):
    """Remove caracteres especiais de CNPJ/CPF para garantir casamento de chaves."""
    return coluna.astype(str).str.replace(r"\D", "", regex=True).str.zfill(14)


# ==============================================================================
# ETAPA 1: FILTRAGEM DA BASE DA RECEITA FEDERAL (CNAE)
# ==============================================================================
print("⏳ Passo 1: Filtrando empresas do setor farmacêutico na base da RF...")

# Como a base da RF é massiva, lemos em chunks (pedaços) para não estourar a RAM
chunks_rf = pd.read_csv(
    ARQUIVO_EMPRESAS_RF,
    sep=";",
    usecols=["CNPJ_BASICO", "CNAE_FISCAL_PRINCIPAL"],  # Ajuste os nomes das colunas conforme o layout da RF
    dtype={"CNPJ_BASICO": str, "CNAE_FISCAL_PRINCIPAL": str},
    chunksize=100000
)

cnpj_farma_set = set()

for chunk in chunks_rf:
    # Remove formatação do CNAE para bater com a lista limpa
    chunk["CNAE_LEAN"] = chunk["CNAE_FISCAL_PRINCIPAL"].str.replace(r"\D", "", regex=True)
    
    # Filtra apenas os que pertencem ao escopo farmacêutico
    filtrado = chunk[chunk["CNAE_LEAN"].isin(CNAES_FARMA)]
    
    # Adiciona os CNPJs básicos (primeiros 8 dígitos) ao nosso Set de busca rápida
    cnpj_farma_set.update(filtrado["CNPJ_BASICO"].tolist())

print(f"✅ Mapeadas {len(cnpj_farma_set)} empresas do setor farmacêutico.")


# ==============================================================================
# ETAPA 2: PROCESSAMENTO DOS DADOS DO TSE
# ==============================================================================
print("\n⏳ Passo 2: Carregando e limpando dados de receitas do TSE...")

# Carrega a base do TSE mantendo apenas colunas cruciais para performance
colunas_tse = [
    "SG_PARTIDO", 
    "NM_CANDIDATO", 
    "DS_CARGO", 
    "NR_CPF_CNPJ_DOADOR", 
    "NM_DOADOR", 
    "VR_RECEITA"
]

df_tse = pd.read_csv(
    ARQUIVO_RECEITAS_TSE,
    sep=";",
    encoding="latin-1",  # TSE costuma usar ISO-8859-1 ou Latin-1
    usecols=colunas_tse,
    dtype={"NR_CPF_CNPJ_DOADOR": str, "VR_RECEITA": float}
)

# Limpa a chave de junção (CNPJ)
df_tse["CNPJ_LIMPO"] = limpar_cnpj(df_tse["NR_CPF_CNPJ_DOADOR"])

# Extrai o CNPJ Básico (8 primeiros dígitos) para cruzar com o padrão da Receita
df_tse["CNPJ_BASICO"] = df_tse["CNPJ_LIMPO"].str[:8]


# ==============================================================================
# ETAPA 3: DATA MATCHING (O INNER JOIN)
# ==============================================================================
print("\n⏳ Passo 3: Executando cruzamento (Match) entre as bases...")

# Filtra o dataframe do TSE mantendo apenas onde o CNPJ Básico está no nosso Set farmacêutico
df_match = df_tse[df_tse["CNPJ_BASICO"].isin(cnpj_farma_set)].copy()

print(f"✅ Cruzamento concluído! Encontradas {len(df_match)} doações originadas do setor farma.")


# ==============================================================================
# ETAPA 4: AGREGAÇÃO E EXPORTAÇÃO PARA JSON
# ==============================================================================
print("\n⏳ Passo 4: Agregando dados por partido e gerando payload...")

# 1. Visão Geral por Partido
ranking_partidos = (
    df_match.groupby("SG_PARTIDO")["VR_RECEITA"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

# 2. Visão Detalhada (Top Beneficiários) para o seu modelo de Timeline
top_beneficiarios = (
    df_match.groupby(["NM_CANDIDATO", "SG_PARTIDO", "DS_CARGO", "NM_DOADOR"])["VR_RECEITA"]
    .sum()
    .reset_index()
    .sort_values(by="VR_RECEITA", ascending=False)
    .head(50)  # Mantém o Top 50 refinado
)

# Monta a estrutura JSON final pronta para o seu frontend/banco de dados
payload_timeline = {
    "ano_eleitoral": 2022,
    "metodologia": "Cruzamento automatizado TSE x CNAE Receita Federal",
    "total_setor_identificado": float(df_match["VR_RECEITA"].sum()),
    "ranking_partidos": ranking_partidos.to_dict(orient="records"),
    "casos_relevantes": top_beneficiarios.to_dict(orient="records")
}

# Salva o arquivo localmente
import json
with open(ARQUIVO_SAIDA_JSON, "w", encoding="utf-8") as f:
    json.dump(payload_timeline, f, ensure_ascii=False, indent=2)

print(f"🚀 Sucesso! Dados consolidados salvos em: '{ARQUIVO_SAIDA_JSON}'")

# Exibe prévia do resultado no terminal para validação imediata
print("\n--- PRÉVIA: TOP 5 PARTIDOS MAIS FINANCIADOS PELO SETOR (2022) ---")
print(ranking_partidos.head(5).to_string(index=False))