"""
Pipeline: Cruzamento TSE x CNAE Receita Federal
Objetivo: Resolver o gap de "doações do setor farmacêutico por partido"
que não existe pré-consolidado em nenhuma fonte pública.

FONTES NECESSÁRIAS (baixar manualmente antes de rodar):
1. TSE - Prestação de Contas Eleitorais
   https://dadosabertos.tse.jus.br/dataset/prestacao-de-contas-eleitorais-{ANO}
   Arquivo relevante: receitas_candidatos_{ANO}_BRASIL.csv
   (ou receitas_partidos_{ANO}_BRASIL.csv para doações a diretórios)

2. Receita Federal - Dados Públicos CNPJ
   https://dados.rfb.gov.br/CNPJ/
   Arquivos: Estabelecimentos*.zip (contém CNPJ básico + CNAE fiscal)
   Aviso: são ~20GB descompactados para a base nacional inteira.
   Alternativa mais leve: Receita Federal disponibiliza também consulta
   por CNAE via BigQuery público (base "basedosdados") se preferir SQL.

CNAEs FARMACÊUTICOS RELEVANTES (conferir tabela CNAE 2.3 do IBGE antes de rodar,
pois estes códigos podem receber revisões):
  - 2110-6/00  Fabricação de produtos farmoquímicos
  - 2121-1/01  Fabricação de medicamentos alopáticos para uso humano
  - 2121-1/02  Fabricação de medicamentos homeopáticos para uso humano
  - 2122-0/00  Fabricação de medicamentos para uso veterinário
  - 4644-3/01  Comércio atacadista de medicamentos e drogas de uso humano
  - 4771-7/01  Comércio varejista de produtos farmacêuticos, com manipulação
  - 4771-7/02  Comércio varejista de produtos farmacêuticos, sem manipulação

Uso:
  python pipeline_tse_farmaceutico.py \
      --receitas receitas_candidatos_2022_BRASIL.csv \
      --estabelecimentos Estabelecimentos0.csv \
      --ano 2022 \
      --saida ranking_partidos_farma_2022.csv
"""

import argparse
import pandas as pd
import unicodedata

CNAES_FARMA = {
    "2110600", "2121101", "2121102", "2122000",
    "4644301", "4771701", "4771702",
}


def normaliza_cnpj_basico(serie_cnpj: pd.Series) -> pd.Series:
    """Extrai os 8 primeiros dígitos (CNPJ básico) de uma coluna de CNPJ/CPF,
    ignorando CPFs (11 dígitos) que não têm equivalente de CNPJ básico."""
    digitos = serie_cnpj.astype(str).str.replace(r"\D", "", regex=True)
    cnpj_basico = digitos.where(digitos.str.len() >= 14).str[:8]
    return cnpj_basico


def carrega_estabelecimentos_farma(path_estabelecimentos: str) -> set:
    """Lê o arquivo de Estabelecimentos da RF em chunks (arquivo é grande)
    e retorna o conjunto de CNPJs básicos com CNAE farmacêutico."""
    # Layout oficial RF (sem cabeçalho, separador ';', encoding latin1):
    # col 0 = CNPJ básico, col 1 = CNPJ ordem, col 2 = CNPJ DV,
    # ... col 11 = CNAE fiscal principal (índice pode variar - CONFERIR
    # o layout oficial em https://www.gov.br/receitafederal antes de rodar)
    colunas_layout = [
        "cnpj_basico", "cnpj_ordem", "cnpj_dv", "identificador_matriz_filial",
        "nome_fantasia", "situacao_cadastral", "data_situacao_cadastral",
        "motivo_situacao_cadastral", "nome_cidade_exterior", "pais",
        "data_inicio_atividade", "cnae_fiscal_principal", "cnae_fiscal_secundaria",
    ]
    cnpjs_farma = set()
    leitor = pd.read_csv(
        path_estabelecimentos,
        sep=";",
        encoding="latin1",
        header=None,
        names=colunas_layout,
        usecols=["cnpj_basico", "cnae_fiscal_principal"],
        dtype=str,
        chunksize=500_000,
    )
    for chunk in leitor:
        farma = chunk[chunk["cnae_fiscal_principal"].isin(CNAES_FARMA)]
        cnpjs_farma.update(farma["cnpj_basico"].tolist())
    return cnpjs_farma


def cruza_receitas_tse(path_receitas: str, cnpjs_farma: set) -> pd.DataFrame:
    """Lê o arquivo de receitas do TSE e filtra apenas doadores cujo CNPJ
    básico está no conjunto farmacêutico."""
    df = pd.read_csv(
        path_receitas,
        sep=";",
        encoding="latin1",
        dtype=str,
        low_memory=False,
    )
    # Nomes de coluna variam por ano; ajuste conforme o dicionário de dados
    # publicado junto ao dataset (arquivo leiame.pdf do TSE).
    col_cnpj_doador = "NR_CPF_CNPJ_DOADOR"
    col_valor = "VR_RECEITA"
    col_partido = "SG_PARTIDO"

    df["cnpj_basico"] = normaliza_cnpj_basico(df[col_cnpj_doador])
    df[col_valor] = (
        df[col_valor].str.replace(",", ".", regex=False).astype(float)
    )

    farma = df[df["cnpj_basico"].isin(cnpjs_farma)].copy()
    return farma[[col_partido, col_valor, "cnpj_basico", col_cnpj_doador]]


def gera_ranking(df_farma: pd.DataFrame) -> pd.DataFrame:
    ranking = (
        df_farma.groupby("SG_PARTIDO")["VR_RECEITA"]
        .agg(total_recebido="sum", numero_doacoes="count")
        .sort_values("total_recebido", ascending=False)
        .reset_index()
    )
    return ranking


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receitas", required=True, help="CSV de receitas do TSE")
    parser.add_argument("--estabelecimentos", required=True, help="CSV de Estabelecimentos da RF")
    parser.add_argument("--ano", required=True, help="Ano eleitoral de referência")
    parser.add_argument("--saida", default="ranking_partidos_farma.csv")
    args = parser.parse_args()

    print(f"[1/4] Carregando CNPJs farmacêuticos de {args.estabelecimentos} ...")
    cnpjs_farma = carrega_estabelecimentos_farma(args.estabelecimentos)
    print(f"      {len(cnpjs_farma)} CNPJs básicos farmacêuticos identificados.")

    print(f"[2/4] Cruzando com receitas eleitorais de {args.ano} ...")
    df_farma = cruza_receitas_tse(args.receitas, cnpjs_farma)
    print(f"      {len(df_farma)} doações identificadas do setor.")

    print("[3/4] Consolidando ranking por partido ...")
    ranking = gera_ranking(df_farma)

    print(f"[4/4] Salvando resultado em {args.saida} ...")
    ranking.to_csv(args.saida, index=False)
    print(ranking.to_string(index=False))


if __name__ == "__main__":
    main()
