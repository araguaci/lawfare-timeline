#!/usr/bin/env python3
"""
sync_watcher.py — Sincronização automática lawfare-timeline → Google Drive

O que faz:
  Monitora dois arquivos locais (lawfare.json e claude.ai-corpus-ids-sync.json).
  Sempre que um deles for salvo/modificado no disco, sobe a versão nova para
  o MESMO arquivo no Google Drive (sobrescreve o conteúdo, mantendo o mesmo
  file ID e o mesmo link de compartilhamento — não cria cópias duplicadas).

Por que isso resolve o problema:
  O Claude (via ferramenta de busca no Drive) só consegue ler o conteúdo real
  de um arquivo quando ele é aberto como Google Doc, ou quando está disponível
  publicamente sem tela de login. Arquivos .json brutos no Drive não são lidos
  automaticamente pela IA. Manter os IDs de arquivo estáveis + um pipeline que
  garante que a versão no Drive é sempre a mais recente é o que permite,
  no mínimo, que você linke a versão atual sempre que abrir uma conversa nova
  (e prepara terreno para uma integração mais direta, ex. MCP de Drive/GitHub).

Pré-requisitos (uma vez só):
  1. pip install -r requirements.txt
  2. Criar credenciais OAuth no Google Cloud Console (ver README.md) e salvar
     como 'credentials.json' na mesma pasta deste script.
  3. Rodar o script uma vez manualmente — vai abrir o navegador pedindo login
     na sua conta Google. Depois disso, ele salva um 'token.json' e não pede
     login de novo (a menos que o token expire/seja revogado).

Uso:
  python sync_watcher.py

  Deixe rodando em background (ou como serviço/tarefa agendada — ver README).
  Ctrl+C para parar.

Configuração dos arquivos e IDs do Drive: editar o dicionário WATCHED_FILES abaixo.
"""

import hashlib
import logging
import sys
import time
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

# ============================================================================
# CONFIGURAÇÃO — edite estes caminhos e IDs conforme seu ambiente
# ============================================================================

# Caminho para os arquivos locais que você edita normalmente.
# Ajuste para o caminho real no seu computador (ex.: dentro do repo lawfare-timeline).
WATCHED_FILES = {
    r"D:\_deploy\lawfare-timeline\_data\lawfare.json": {
        "drive_file_id": "1She6FaPxTS1jSYNovMyw5eMawgsOfesb",
        "mimetype": "application/json",
    },
    r"D:\_deploy\lawfare-timeline\claude.ai-corpus-ids-sync.json": {
        "drive_file_id": "1IOhE9CCsyG094TmoS4kgO9p-qRKaTr1A",
        "mimetype": "application/json",
    },
}

# Escopo mínimo necessário: apenas os arquivos criados/abertos por este app.
# (Se os arquivos já existirem no seu Drive e não foram criados por este app,
# pode ser necessário o escopo mais amplo 'drive' — ver README, seção "Escopos".)
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"

# Tempo de espera após a última modificação antes de subir (evita subir
# arquivo pela metade enquanto o editor ainda está gravando no disco).
DEBOUNCE_SECONDS = 3.0

# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("sync_watcher")


def get_drive_service():
    """Autentica com o Google Drive (OAuth2) e retorna o client da API."""
    creds = None
    token_path = Path(TOKEN_FILE)

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            log.info("Token expirado — renovando automaticamente...")
            creds.refresh(Request())
        else:
            if not Path(CREDENTIALS_FILE).exists():
                log.error(
                    "Arquivo '%s' não encontrado. Siga o README.md para gerar "
                    "as credenciais OAuth no Google Cloud Console antes de rodar "
                    "este script.",
                    CREDENTIALS_FILE,
                )
                sys.exit(1)
            log.info("Primeira execução — abrindo navegador para login Google...")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        token_path.write_text(creds.to_json())
        log.info("Credenciais salvas em '%s'.", TOKEN_FILE)

    return build("drive", "v3", credentials=creds)


def file_hash(path: Path) -> str:
    """Hash do conteúdo, para evitar upload duplicado quando nada mudou de fato."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


class DriveSyncHandler(FileSystemEventHandler):
    """Reage a eventos de modificação nos arquivos monitorados."""

    def __init__(self, service, watched_files: dict):
        super().__init__()
        self.service = service
        # Normaliza caminhos para comparação robusta entre SO diferentes
        self.watched = {str(Path(p).resolve()): cfg for p, cfg in watched_files.items()}
        self._pending = {}  # path -> timestamp da última modificação detectada
        self._last_hash = {}  # path -> hash do último conteúdo já enviado

    def on_modified(self, event):
        if event.is_directory:
            return
        path = str(Path(event.src_path).resolve())
        if path in self.watched:
            self._pending[path] = time.time()

    def on_created(self, event):
        # Alguns editores salvam via "criar novo arquivo temporário + renomear"
        self.on_modified(event)

    def process_pending(self):
        """Chamado periodicamente pelo loop principal — aplica o debounce
        e sobe qualquer arquivo cuja última modificação já 'assentou'."""
        now = time.time()
        for path, last_mod_ts in list(self._pending.items()):
            if now - last_mod_ts < DEBOUNCE_SECONDS:
                continue  # ainda dentro da janela de debounce, espera mais

            del self._pending[path]
            self._upload_if_changed(path)

    def _upload_if_changed(self, path: str):
        p = Path(path)
        if not p.exists():
            log.warning("Arquivo '%s' não existe mais no disco — pulando.", path)
            return

        try:
            current_hash = file_hash(p)
        except OSError as e:
            log.error("Não consegui ler '%s' agora (%s) — tentando de novo no próximo ciclo.", path, e)
            self._pending[path] = time.time()  # reagenda
            return

        if self._last_hash.get(path) == current_hash:
            log.debug("Conteúdo de '%s' não mudou de fato — não subindo.", path)
            return

        cfg = self.watched[path]
        try:
            self._upload(p, cfg["drive_file_id"], cfg["mimetype"])
            self._last_hash[path] = current_hash
        except HttpError as e:
            log.error("Erro da API do Drive ao subir '%s': %s", path, e)
        except Exception as e:
            log.error("Erro inesperado ao subir '%s': %s", path, e)

    def _upload(self, path: Path, drive_file_id: str, mimetype: str):
        media = MediaFileUpload(str(path), mimetype=mimetype, resumable=True)
        log.info("Enviando '%s' para o Google Drive (file id %s)...", path.name, drive_file_id)
        updated_file = (
            self.service.files()
            .update(fileId=drive_file_id, media_body=media, fields="id, modifiedTime")
            .execute()
        )
        log.info(
            "OK — '%s' atualizado no Drive. modifiedTime=%s",
            path.name,
            updated_file.get("modifiedTime"),
        )


def main():
    log.info("Iniciando sync_watcher — monitorando %d arquivo(s):", len(WATCHED_FILES))
    for p in WATCHED_FILES:
        exists = "OK" if Path(p).exists() else "!! NÃO ENCONTRADO !!"
        log.info("  - %s  [%s]", p, exists)

    service = get_drive_service()
    handler = DriveSyncHandler(service, WATCHED_FILES)

    observer = Observer()
    # Agrupa por diretório-pai para registrar cada pasta uma única vez
    watched_dirs = {str(Path(p).resolve().parent) for p in WATCHED_FILES}
    for d in watched_dirs:
        if Path(d).exists():
            observer.schedule(handler, d, recursive=False)
            log.info("Observando diretório: %s", d)
        else:
            log.warning("Diretório não encontrado, não será monitorado: %s", d)

    observer.start()
    log.info("Pronto. Aguardando modificações... (Ctrl+C para parar)")

    try:
        while True:
            time.sleep(1)
            handler.process_pending()
    except KeyboardInterrupt:
        log.info("Encerrando...")
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
