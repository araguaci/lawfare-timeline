#!/usr/bin/env python3
"""
garimpo_telegram.py — varredura de grupos/canais do Telegram para o corpus lawfare-timeline (CC0 1.0)

Procura, num período definido, mensagens sobre a custódia do 8/jan (ginásio da ANP, Papuda,
Colmeia, ônibus, óbitos, atendimento médico, autolesão, separação de famílias) e gera:
  - achados.csv      → uma linha por mensagem encontrada, no formato do garimpo-testemunhal-8jan.csv
  - achados.jsonl    → registro completo com contexto (mensagens antes/depois) e hash SHA-256
  - midia/           → fotos/vídeos/áudios das mensagens encontradas (opcional)
  - manifesto.json   → parâmetros da varredura, contagens e hash de cada arquivo gerado

DOIS MODOS
  1) export  — lê a exportação do Telegram Desktop (Configurações › Avançado › Exportar dados,
               formato JSON). Não precisa de API, não toca na conta. RECOMENDADO para começar.
       python garimpo_telegram.py export --pasta "C:/Users/voce/Downloads/Telegram Desktop/DataExport_2026-10-21"
  2) api     — lê direto da sua conta via Telethon (pip install telethon). Precisa de api_id/api_hash
               de https://my.telegram.org (Desenvolvimento de API). Só alcança grupos/canais de que
               você já participa ou que são públicos.
       python garimpo_telegram.py api --api-id 123456 --api-hash abc... --chats "Patriotas DF" "@canal_x"
       python garimpo_telegram.py api --api-id ... --api-hash ... --todos   (varre todos os seus diálogos)

OPÇÕES COMUNS
  --inicio 2023-01-08 --fim 2023-03-31   janela de datas (padrão: 08/01 a 31/03/2023)
  --termos termos.txt                    arquivo extra de termos (um por linha; "categoria: termo" opcional)
  --nomes nomes.txt                      nomes de presos a cruzar (um por linha) — busca exata sem acento
  --contexto 3                           mensagens antes/depois de cada achado
  --midia                                baixa a mídia dos achados
  --anonimizar                           troca nome/@ de remetente por código estável e mascara telefones
  --saida ./garimpo_saida

PRIVACIDADE: tudo fica local. Nada é publicado. Antes de levar qualquer achado ao corpus público,
use --anonimizar ou retire identificação de vítimas sem consentimento da família.
"""
import argparse, asyncio, csv, hashlib, json, os, re, sys, unicodedata
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ----------------------------------------------------------------------------- termos

TERMOS_PADRAO = {
    # termos de alto valor: sozinhos já tornam a mensagem um achado
    "chave": [
        "ginasio", "academia da policia", "academia nacional de policia", "papuda", "colmeia",
        "rodoviaria", "ia pra rodoviaria", "levar para a rodoviaria", "ninguem avisou",
        "nao disseram para onde", "presos politicos", "8 de janeiro", "08/01",
    ],
    "local": [
        "anp", "cdp", "penitenciaria", "presidio", "sede da pf", "policia federal",
        "qg do exercito", "quartel general", "setor militar urbano", "smu", "granja do torto",
    ],
    "transporte": [
        "onibus", "levaram a gente", "levados para", "embarcar", "embarcaram",
        "disseram que", "falaram que ia", "pensamos que", "escolta",
    ],
    "obito": [
        "faleceu", "falecido", "falecida", "morreu", "morte", "obito", "velorio", "sepultamento",
        "enterro", "nota de pesar", "descanse em paz", "luto", "infarto", "mal subito", "avc",
        "parada cardiaca", "parada cardiorrespiratoria",
    ],
    "saude": [
        "desmaiou", "desmaio", "passou mal", "convulsao", "ambulancia", "samu", "bombeiros",
        "hospital", "upa", "socorro", "medicamento", "remedio", "insulina", "pressao alta",
        "hipertenso", "diabetico", "cadeirante", "gestante", "gravida", "idoso", "idosa",
        "sem agua", "sem comida", "fome", "sede", "banheiro",
    ],
    "autolesao": [
        "autolesao", "se cortou", "se machucou", "tentou se matar", "tentativa de suicidio",
        "suicidio", "se enforcar", "crise de panico", "surto", "crise nervosa", "desespero",
    ],
    "familia": [
        "crianca", "criancas", "bebe", "filho", "filha", "menor de idade", "conselho tutelar",
        "mae com", "separaram", "separada", "nao sabemos onde", "desaparecido", "sem noticias",
        "lista de presos", "lista dos presos", "lista de nomes",
    ],
    "processo": [
        "audiencia de custodia", "custodia", "preventiva", "advogado", "defensoria", "dpu",
        "tornozeleira", "soltura", "liberado", "liberada", "liberados", "anpp", "acordo",
    ],
}

def normalizar(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower()).strip()

def compilar_termos(arquivo_extra=None):
    termos = {k: list(v) for k, v in TERMOS_PADRAO.items()}
    if arquivo_extra:
        for linha in Path(arquivo_extra).read_text(encoding="utf-8").splitlines():
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue
            cat, _, termo = linha.partition(":") if ":" in linha else ("extra", "", linha)
            termos.setdefault(cat.strip() or "extra", []).append(termo.strip())
    padroes = {}
    for cat, lista in termos.items():
        alternativas = sorted({re.escape(normalizar(t)) for t in lista if t}, key=len, reverse=True)
        padroes[cat] = re.compile(r"(?<![a-z0-9])(" + "|".join(alternativas) + r")(?![a-z0-9])")
    return padroes

def compilar_nomes(arquivo):
    if not arquivo:
        return []
    nomes = [normalizar(l) for l in Path(arquivo).read_text(encoding="utf-8").splitlines() if l.strip()]
    return [(n, re.compile(r"(?<![a-z])" + re.escape(n) + r"(?![a-z])")) for n in nomes if len(n) >= 5]

# Uma mensagem só vira achado se casar LOCAL/TRANSPORTE/FAMÍLIA/PROCESSO com um evento grave,
# ou um evento grave sozinho dentro da janela, ou um nome da lista. Reduz ruído de conversa genérica.
CATEGORIAS_GRAVES = {"chave", "obito", "saude", "autolesao"}

def classificar(texto_norm, padroes, nomes):
    cats, termos = set(), set()
    for cat, rx in padroes.items():
        achados = {m.group(1) for m in rx.finditer(texto_norm)}
        if achados:
            cats.add(cat)
            termos |= achados
    nomes_hit = [n for n, rx in nomes if rx.search(texto_norm)]
    relevante = bool(nomes_hit) or bool(cats & CATEGORIAS_GRAVES) or len(cats) >= 2
    return relevante, sorted(cats), sorted(termos), nomes_hit

def tipo_evento(cats):
    for c in ("obito", "autolesao", "saude", "familia", "transporte"):
        if c in cats:
            return {"obito": "obito", "autolesao": "tentativa_autolesao", "saude": "atendimento_medico",
                    "familia": "separacao_familiar", "transporte": "transporte_destino"}[c]
    return "outro"

# ----------------------------------------------------------------------------- anonimização

RX_FONE = re.compile(r"(\+?55\s?)?\(?\d{2}\)?\s?9?\d{4}[-\s]?\d{4}")

class Anonimizador:
    def __init__(self, ativo, sal):
        self.ativo, self.sal = ativo, sal
    def pessoa(self, nome):
        if not self.ativo or not nome:
            return nome
        return "P-" + hashlib.sha256((self.sal + nome).encode()).hexdigest()[:8]
    def texto(self, t):
        return RX_FONE.sub("[telefone]", t) if self.ativo else t

# ----------------------------------------------------------------------------- saída

CAMPOS_CSV = ["ref_interno", "iniciais_ou_codigo", "data_evento", "local", "tipo_evento",
              "descricao_factual", "registro_contemporaneo", "data_do_registro", "hash_do_registro",
              "fonte_secundaria_url", "consentimento_familia", "status_evidencia", "observacoes"]

def sha256_txt(*partes):
    return hashlib.sha256("\x1f".join(str(p) for p in partes).encode("utf-8")).hexdigest()

def sha256_arq(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()

class Coletor:
    def __init__(self, saida, anon):
        self.saida = Path(saida); self.saida.mkdir(parents=True, exist_ok=True)
        self.anon = anon; self.n = 0
        self.jsonl = open(self.saida / "achados.jsonl", "w", encoding="utf-8")
        self.csvf = open(self.saida / "achados.csv", "w", encoding="utf-8-sig", newline="")
        self.csv = csv.DictWriter(self.csvf, fieldnames=CAMPOS_CSV); self.csv.writeheader()
        self.por_cat, self.por_chat = {}, {}

    def adicionar(self, chat, msg, cats, termos, nomes, contexto, midia=None):
        self.n += 1
        ref = f"TG-{self.n:05d}"
        texto = self.anon.texto(msg["texto"])
        h = sha256_txt(chat["id"], msg["id"], msg["data"], msg["texto"])
        reg = {
            "ref": ref, "chat": chat["nome"], "chat_id": chat["id"], "msg_id": msg["id"],
            "link": msg.get("link"), "data": msg["data"], "remetente": self.anon.pessoa(msg.get("remetente")),
            "texto": texto, "categorias": cats, "termos": termos, "nomes_lista": nomes,
            "encaminhada_de": self.anon.pessoa(msg.get("encaminhada_de")),
            "midia": midia, "hash_sha256": h,
            "contexto": [{"data": c["data"], "remetente": self.anon.pessoa(c.get("remetente")),
                          "texto": self.anon.texto(c["texto"])} for c in contexto],
        }
        self.jsonl.write(json.dumps(reg, ensure_ascii=False) + "\n")
        self.csv.writerow({
            "ref_interno": ref, "iniciais_ou_codigo": "", "data_evento": "",
            "local": ", ".join(t for t in termos if t in TERMOS_PADRAO["local"] + TERMOS_PADRAO["chave"]),
            "tipo_evento": tipo_evento(cats), "descricao_factual": texto[:500].replace("\n", " "),
            "registro_contemporaneo": f"Telegram — {chat['nome']} — msg {msg['id']}" + (" (com mídia)" if midia else ""),
            "data_do_registro": msg["data"], "hash_do_registro": h,
            "fonte_secundaria_url": msg.get("link") or "", "consentimento_familia": "",
            "status_evidencia": "ev-alleged",
            "observacoes": "nomes da lista: " + "; ".join(nomes) if nomes else "",
        })
        for c in cats:
            self.por_cat[c] = self.por_cat.get(c, 0) + 1
        self.por_chat[chat["nome"]] = self.por_chat.get(chat["nome"], 0) + 1

    def fechar(self, parametros):
        self.jsonl.close(); self.csvf.close()
        arquivos = {}
        for p in sorted(self.saida.rglob("*")):
            if p.is_file() and p.name != "manifesto.json":
                arquivos[str(p.relative_to(self.saida))] = sha256_arq(p)
        manifesto = {"gerado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                     "parametros": parametros, "total_achados": self.n,
                     "por_categoria": self.por_cat, "por_chat": self.por_chat, "sha256": arquivos}
        (self.saida / "manifesto.json").write_text(json.dumps(manifesto, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n{self.n} achados → {self.saida.resolve()}")
        for c, q in sorted(self.por_cat.items(), key=lambda x: -x[1]):
            print(f"  {c:12s} {q}")

# ----------------------------------------------------------------------------- modo export (Telegram Desktop)

def texto_export(campo):
    if isinstance(campo, str):
        return campo
    if isinstance(campo, list):
        return "".join(p if isinstance(p, str) else p.get("text", "") for p in campo)
    return ""

def chats_do_export(pasta):
    pasta = Path(pasta)
    arquivos = list(pasta.rglob("result.json"))
    if not arquivos:
        sys.exit(f"Nenhum result.json em {pasta}. Exporte em formato JSON (não HTML).")
    for arq in arquivos:
        dados = json.loads(arq.read_text(encoding="utf-8"))
        lista = dados.get("chats", {}).get("list") if "chats" in dados else [dados]
        for c in lista or []:
            if "messages" in c:
                yield arq.parent, c

def link_publico(chat_username, chat_id, msg_id):
    if chat_username:
        return f"https://t.me/{chat_username}/{msg_id}"
    cid = str(chat_id)
    cid = cid[4:] if cid.startswith("-100") else cid.lstrip("-")
    return f"https://t.me/c/{cid}/{msg_id}"

def rodar_export(a, padroes, nomes, col):
    ini, fim = a.inicio, a.fim + timedelta(days=1)
    for base, chat in chats_do_export(a.pasta):
        info = {"id": chat.get("id"), "nome": chat.get("name") or f"chat_{chat.get('id')}"}
        msgs = []
        for m in chat["messages"]:
            if m.get("type") != "message":
                continue
            try:
                d = datetime.fromisoformat(m["date"])
            except Exception:
                continue
            if not (ini <= d < fim):
                continue
            txt = texto_export(m.get("text"))
            if m.get("caption"):
                txt += "\n" + texto_export(m["caption"])
            msgs.append({"id": m["id"], "data": m["date"], "texto": txt,
                         "remetente": m.get("from"), "encaminhada_de": m.get("forwarded_from"),
                         "arquivo": m.get("photo") or m.get("file"),
                         "link": link_publico(None, chat.get("id"), m["id"])})
        print(f"[export] {info['nome']}: {len(msgs)} mensagens na janela")
        for i, m in enumerate(msgs):
            rel, cats, termos, nomes_hit = classificar(normalizar(m["texto"]), padroes, nomes)
            if not rel:
                continue
            ctx = msgs[max(0, i - a.contexto):i] + msgs[i + 1:i + 1 + a.contexto]
            midia = None
            if m.get("arquivo") and a.midia:
                origem = base / m["arquivo"]
                if origem.exists():
                    destino = Path(a.saida) / "midia" / f"{info['id']}_{m['id']}_{origem.name}"
                    destino.parent.mkdir(parents=True, exist_ok=True)
                    destino.write_bytes(origem.read_bytes())
                    midia = {"arquivo": str(destino.relative_to(a.saida)), "sha256": sha256_arq(destino)}
            elif m.get("arquivo"):
                midia = {"arquivo_no_export": m["arquivo"]}
            col.adicionar(info, m, cats, termos, nomes_hit, ctx, midia)

# ----------------------------------------------------------------------------- modo api (Telethon)

async def rodar_api(a, padroes, nomes, col):
    try:
        from telethon import TelegramClient
        from telethon.utils import get_display_name
    except ImportError:
        sys.exit("Instale o Telethon:  pip install telethon")
    ini = a.inicio.replace(tzinfo=timezone.utc)
    fim = (a.fim + timedelta(days=1)).replace(tzinfo=timezone.utc)
    cliente = TelegramClient(a.sessao, a.api_id, a.api_hash, flood_sleep_threshold=120)
    await cliente.start()  # pede telefone e código na primeira vez; a sessão fica salva localmente

    alvos = []
    if a.todos:
        async for d in cliente.iter_dialogs():
            if d.is_group or d.is_channel:
                alvos.append(d.entity)
    for c in a.chats or []:
        alvos.append(await cliente.get_entity(c))

    for ent in alvos:
        nome = get_display_name(ent) or str(ent.id)
        username = getattr(ent, "username", None)
        info = {"id": ent.id, "nome": nome}
        msgs = []
        async for m in cliente.iter_messages(ent, offset_date=fim):
            if m.date < ini:
                break
            remet = None
            try:
                s = await m.get_sender()
                remet = get_display_name(s) if s else None
            except Exception:
                pass
            fwd = None
            if m.fwd_from:
                fwd = getattr(m.fwd_from, "from_name", None) or "encaminhada"
            msgs.append({"id": m.id, "data": m.date.isoformat(), "texto": m.message or "",
                         "remetente": remet, "encaminhada_de": fwd, "_obj": m,
                         "link": link_publico(username, getattr(ent, "id", ""), m.id)})
        msgs.reverse()
        print(f"[api] {nome}: {len(msgs)} mensagens na janela")
        for i, m in enumerate(msgs):
            rel, cats, termos, nomes_hit = classificar(normalizar(m["texto"]), padroes, nomes)
            if not rel:
                continue
            ctx = msgs[max(0, i - a.contexto):i] + msgs[i + 1:i + 1 + a.contexto]
            midia = None
            if a.midia and m["_obj"].media:
                pasta = Path(a.saida) / "midia"; pasta.mkdir(parents=True, exist_ok=True)
                caminho = await m["_obj"].download_media(file=str(pasta / f"{ent.id}_{m['id']}"))
                if caminho:
                    midia = {"arquivo": str(Path(caminho).relative_to(a.saida)), "sha256": sha256_arq(caminho)}
            m2 = {k: v for k, v in m.items() if k != "_obj"}
            ctx2 = [{k: v for k, v in c.items() if k != "_obj"} for c in ctx]
            col.adicionar(info, m2, cats, termos, nomes_hit, ctx2, midia)
    await cliente.disconnect()

# ----------------------------------------------------------------------------- CLI

def data(s):
    return datetime.strptime(s, "%Y-%m-%d")

def main():
    ap = argparse.ArgumentParser(description="Garimpo Telegram — custódia 8/jan")
    sub = ap.add_subparsers(dest="modo", required=True)
    comum = argparse.ArgumentParser(add_help=False)
    comum.add_argument("--inicio", type=data, default=data("2023-01-08"))
    comum.add_argument("--fim", type=data, default=data("2023-03-31"))
    comum.add_argument("--termos"); comum.add_argument("--nomes")
    comum.add_argument("--contexto", type=int, default=3)
    comum.add_argument("--midia", action="store_true")
    comum.add_argument("--anonimizar", action="store_true")
    comum.add_argument("--sal", default="lawfare-timeline", help="sal do código de anonimização (guarde-o)")
    comum.add_argument("--saida", default="garimpo_saida")
    e = sub.add_parser("export", parents=[comum]); e.add_argument("--pasta", required=True)
    p = sub.add_parser("api", parents=[comum])
    p.add_argument("--api-id", type=int, required=True); p.add_argument("--api-hash", required=True)
    p.add_argument("--sessao", default="garimpo"); p.add_argument("--chats", nargs="*")
    p.add_argument("--todos", action="store_true")
    a = ap.parse_args()
    if a.modo == "api" and not (a.todos or a.chats):
        ap.error("informe --chats ... ou --todos")

    padroes, nomes = compilar_termos(a.termos), compilar_nomes(a.nomes)
    col = Coletor(a.saida, Anonimizador(a.anonimizar, a.sal))
    params = {k: (v.isoformat() if isinstance(v, datetime) else v) for k, v in vars(a).items()
              if k not in ("api_hash", "sal")}
    if a.modo == "export":
        rodar_export(a, padroes, nomes, col)
    else:
        asyncio.run(rodar_api(a, padroes, nomes, col))
    col.fechar(params)

if __name__ == "__main__":
    main()
