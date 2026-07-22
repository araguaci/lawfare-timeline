#!/usr/bin/env python3
"""
Analisador de ameaças e sentimento em respostas coletadas via coletar_respostas.py

Lê o respostas.json gerado pelo coletor e classifica cada reply em categorias,
para verificação independente de alegações do tipo "N ameaças de morte em 24h".

Metodologia (léxico PT-BR, transparente e auditável — nada de caixa-preta):

  1. AMEACA_EXPLICITA   — verbo de violência letal + referência direta ao alvo
                          (ex: "vai morrer", "vamos te matar", "bala nele")
  2. INCITACAO          — chamado à ação coletiva sem verbo de 1a pessoa
                          (ex: "alguém tem que", "merece o mesmo que", "façam algo")
  3. RETORICA_AGRESSIVA — insulto/hostilidade sem ameaça de vida
  4. CRITICA            — discordância política sem hostilidade
  5. APOIO              — manifestação de apoio ao alvo
  6. NEUTRO             — não classificável nas anteriores

Cada reply recebe UMA categoria (a mais grave que der match) + score de
sentimento (-2 a +2) para dar textura além da classificação binária.

IMPORTANTE — limites deste método:
  - Léxico captura padrões conhecidos, não substitui revisão humana para
    decisões de denúncia/exposição pública de contas.
  - Falsos positivos/negativos existem (ironia, negação, citação de terceiros).
  - Uso pretendido: gerar CONTAGEM AGREGADA verificável para contrastar com
    alegações de imprensa/defesa jurídica — não para publicar lista de nomes
    sem revisão manual caso a caso.

Uso:
    python3 analisar_ameacas.py --input respostas.json --outdir ./analise
"""

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict

# ---------------------------------------------------------------------------
# LÉXICO — cada termo é uma regex simples, case-insensitive, com \b quando
# aplicável para evitar match dentro de outras palavras.
# ---------------------------------------------------------------------------

AMEACA_EXPLICITA_PATTERNS = [
    r"\bvai morrer\b", r"\bvou te matar\b", r"\bvamos te matar\b",
    r"\bmerece morrer\b", r"\bprecisa morrer\b", r"\bdeveria morrer\b",
    r"\bbala nele\b", r"\bbala nesse\b", r"\btoma uma facada\b",
    r"\blevar uma facada\b", r"\benforcar (ele|esse|o|essa)\b",
    r"\bmorte a\b", r"\bmate (ele|esse)\b", r"\bexecut(a|ar|em)\b.{0,15}\btraidor",
    r"\bfuzil(a|ar|em)\b", r"\bacabar com a vida\b",
]

INCITACAO_PATTERNS = [
    r"\balguém (tem|precisa) que fazer\b", r"\bfaltou (é )?fazer o que\b",
    r"\bnão vai ter perdão\b", r"\bhora da vingança\b",
    r"\bfação (deveria|devia)\b", r"\bmerece o mesmo (destino|fim)\b",
    r"\bmesma coisa que fizeram com\b", r"\bsigam o exemplo\b",
]

RETORICA_AGRESSIVA_PATTERNS = [
    r"\blixo\b", r"\bverme\b", r"\bcanalha\b", r"\bmiseráv", r"\bsafad",
    r"\bnojent", r"\bvagabund", r"\bimbecil\b", r"\bcorrupto\b.{0,10}\bfilho\b",
    r"\bvendilh", r"\btraidor\b",
]

APOIO_PATTERNS = [
    r"\bfor(ç|c)a, senador\b", r"\bcom você\b", r"\bapoio total\b",
    r"\bestamos com você\b", r"\bcoragem\b", r"\bDeus (te|o) proteja\b",
]

CRITICA_PATTERNS = [
    r"\bdiscordo\b", r"\bnão concordo\b", r"\bpolítica ruim\b",
    r"\bmau senador\b", r"\bvotou contra\b", r"\bhipócrita\b",
]

# Léxico simples de sentimento (não é análise de sentimento robusta —
# é um contador de polaridade lexical para dar sinal complementar).
POSITIVO = ["força", "apoio", "coragem", "justiça", "parabéns", "correto", "certo"]
NEGATIVO = ["ódio", "raiva", "nojo", "vergonha", "revoltante", "absurdo", "inaceitável"]


def compile_patterns(patterns):
    return [re.compile(p, re.IGNORECASE) for p in patterns]


AMEACA_RE = compile_patterns(AMEACA_EXPLICITA_PATTERNS)
INCITACAO_RE = compile_patterns(INCITACAO_PATTERNS)
RETORICA_RE = compile_patterns(RETORICA_AGRESSIVA_PATTERNS)
APOIO_RE = compile_patterns(APOIO_PATTERNS)
CRITICA_RE = compile_patterns(CRITICA_PATTERNS)


def classificar(texto):
    """Retorna (categoria, termos_encontrados) — categoria mais grave vence."""
    if not texto:
        return "NEUTRO", []

    for regex_list, categoria in [
        (AMEACA_RE, "AMEACA_EXPLICITA"),
        (INCITACAO_RE, "INCITACAO"),
    ]:
        matches = [r.pattern for r in regex_list if r.search(texto)]
        if matches:
            return categoria, matches

    matches = [r.pattern for r in RETORICA_RE if r.search(texto)]
    if matches:
        return "RETORICA_AGRESSIVA", matches

    matches = [r.pattern for r in APOIO_RE if r.search(texto)]
    if matches:
        return "APOIO", matches

    matches = [r.pattern for r in CRITICA_RE if r.search(texto)]
    if matches:
        return "CRITICA", matches

    return "NEUTRO", []


def sentimento_score(texto):
    if not texto:
        return 0
    t = texto.lower()
    score = 0
    for palavra in POSITIVO:
        score += t.count(palavra)
    for palavra in NEGATIVO:
        score -= t.count(palavra)
    return max(-2, min(2, score))


def carregar_respostas(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("tweets", []), data.get("users", {})


def analisar(tweets, users):
    resultados = []
    contagem_categoria = Counter()
    por_autor = defaultdict(lambda: {"total": 0, "ameacas": 0, "categorias": Counter()})

    for t in tweets:
        texto = t.get("text", "")
        categoria, termos = classificar(texto)
        score = sentimento_score(texto)
        author_id = t.get("author_id")
        author = users.get(author_id, {})
        username = author.get("username", "desconhecido")

        contagem_categoria[categoria] += 1
        por_autor[username]["total"] += 1
        por_autor[username]["categorias"][categoria] += 1
        if categoria in ("AMEACA_EXPLICITA", "INCITACAO"):
            por_autor[username]["ameacas"] += 1

        resultados.append({
            "tweet_id": t.get("id"),
            "created_at": t.get("created_at"),
            "username": username,
            "name": author.get("name", ""),
            "verified": author.get("verified", False),
            "text": texto.replace("\n", " "),
            "categoria": categoria,
            "termos_match": "; ".join(termos),
            "sentimento": score,
            "likes": t.get("public_metrics", {}).get("like_count", 0),
            "retweets": t.get("public_metrics", {}).get("retweet_count", 0),
        })

    return resultados, contagem_categoria, por_autor


def salvar_csv_detalhado(resultados, path):
    if not resultados:
        return
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(resultados[0].keys()))
        writer.writeheader()
        writer.writerows(resultados)


def salvar_resumo(contagem_categoria, por_autor, total, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("RESUMO DA ANÁLISE\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total de replies analisadas: {total}\n\n")
        f.write("Distribuição por categoria:\n")
        for cat, n in contagem_categoria.most_common():
            pct = (n / total * 100) if total else 0
            f.write(f"  {cat:22s} {n:6d}  ({pct:5.1f}%)\n")

        ameacas = contagem_categoria.get("AMEACA_EXPLICITA", 0) + contagem_categoria.get("INCITACAO", 0)
        f.write(f"\nTotal AMEACA_EXPLICITA + INCITACAO: {ameacas}\n")
        f.write("(Compare este número com qualquer alegação de imprensa antes de aceitar a estatística.)\n\n")

        f.write("Contas com mais de 1 reply classificada como ameaça/incitação:\n")
        f.write("-" * 60 + "\n")
        reincidentes = {u: d for u, d in por_autor.items() if d["ameacas"] > 1}
        for u, d in sorted(reincidentes.items(), key=lambda x: -x[1]["ameacas"]):
            f.write(f"  @{u}: {d['ameacas']} ameaças/incitações em {d['total']} replies totais\n")

        if not reincidentes:
            f.write("  (nenhuma conta com mais de 1 ocorrência)\n")

    print(f"Salvo: {path}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Analisa ameaças/sentimento em respostas coletadas")
    parser.add_argument("--input", default="respostas.json", help="arquivo JSON gerado pelo coletor")
    parser.add_argument("--outdir", default=".", help="diretório de saída")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"ERRO: arquivo não encontrado: {args.input}", file=sys.stderr)
        print("Rode antes: python3 coletar_respostas.py --tweet-id ... ", file=sys.stderr)
        sys.exit(1)

    tweets, users = carregar_respostas(args.input)
    if not tweets:
        print("AVISO: nenhum tweet no arquivo de entrada — nada a analisar.", file=sys.stderr)
        sys.exit(1)

    resultados, contagem_categoria, por_autor = analisar(tweets, users)

    os.makedirs(args.outdir, exist_ok=True)
    salvar_csv_detalhado(resultados, os.path.join(args.outdir, "classificacao_detalhada.csv"))
    salvar_resumo(contagem_categoria, por_autor, len(resultados), os.path.join(args.outdir, "resumo.txt"))

    print(f"\nTotal analisado: {len(resultados)} replies", file=sys.stderr)
    for cat, n in contagem_categoria.most_common():
        print(f"  {cat}: {n}", file=sys.stderr)


if __name__ == "__main__":
    main()
