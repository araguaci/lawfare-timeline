# Sync automático lawfare-timeline → Google Drive

Monitora `lawfare.json` e `claude.ai-corpus-ids-sync.json` no seu disco e, a cada
salvamento, sobe a versão nova para o mesmo arquivo no Google Drive (mesmo ID,
mesmo link — não cria cópias).

## O que isso resolve e o que **não** resolve

✅ Resolve: o arquivo no Drive nunca mais fica desatualizado em relação ao seu disco.
✅ Resolve: você não precisa lembrar de subir manualmente depois de cada merge.

❌ Não resolve sozinho: o Claude **ainda não lê `.json` bruto do Drive automaticamente**
em toda conversa nova — as ferramentas de Drive do Claude leem nativamente Google Docs,
não arquivos `.json`. Isso mantém o Drive sempre correto, que é o pré-requisito para
qualquer solução de leitura (anexar o arquivo na conversa, converter para Google Doc,
ou — a opção mais robusta — conectar um MCP de Drive/GitHub que leia arquivos brutos
diretamente). Depois de rodar isso por um tempo, se quiser fechar esse último elo,
me chame numa conversa nova que eu te ajudo a configurar essa ponta.

---

## Passo 1 — Instalar dependências

```bash
pip install -r requirements.txt
```

## Passo 2 — Criar credenciais OAuth no Google Cloud Console

Isso só existe porque o Google exige que qualquer programa que acesse SEU Drive
seja autorizado explicitamente por você. É uma configuração única.

1. Acesse https://console.cloud.google.com/
2. Crie um projeto novo (ou use um existente) — canto superior esquerdo, "Novo Projeto".
3. No menu lateral, vá em **APIs e serviços → Biblioteca**.
4. Busque por **Google Drive API** e clique em **Ativar**.
5. Vá em **APIs e serviços → Tela de consentimento OAuth**.
   - Tipo de usuário: **Externo** (a menos que você tenha Google Workspace).
   - Preencha nome do app (ex.: "lawfare-timeline sync"), seu e-mail em contato do desenvolvedor.
   - Em "Escopos", não precisa adicionar nada manualmente.
   - Em "Usuários de teste", adicione o seu próprio e-mail Google (o mesmo do Drive).
   - Salve e continue até o fim (não precisa publicar o app).
6. Vá em **APIs e serviços → Credenciais**.
   - **Criar credenciais → ID do cliente OAuth**.
   - Tipo de aplicativo: **App para computador (Desktop app)**.
   - Nome: qualquer um (ex.: "lawfare-sync-desktop").
   - Clique em **Criar**.
7. Baixe o JSON gerado (botão de download ao lado da credencial criada).
8. Renomeie o arquivo baixado para `credentials.json` e coloque na mesma pasta do `sync_watcher.py`.

## Passo 3 — Ajustar os caminhos no script

Abra `sync_watcher.py` e edite o dicionário `WATCHED_FILES` no topo do arquivo:
troque os caminhos (`D:\_deploy\lawfare-timeline\...`) pelos caminhos reais dos
dois arquivos no seu computador. Os IDs do Drive (`drive_file_id`) já estão
preenchidos com os arquivos que você me enviou — não precisa mexer neles, a
menos que queira apontar para arquivos diferentes.

## Passo 4 — Primeira execução (login único)

```bash
python sync_watcher.py
```

Na primeira vez, isso abre o navegador pedindo para você logar na conta Google
dona do Drive e autorizar o app. Depois disso, um arquivo `token.json` é criado
e você não precisa logar de novo (o token se renova sozinho).

Se aparecer aviso de "app não verificado" — é esperado, porque o app é seu e não
passou pelo processo de verificação pública do Google (não precisa, já que só
você vai usar). Clique em "Avançado" → "Acessar [nome do app] (não seguro)".

## Passo 5 — Deixar rodando

O script fica em loop escutando mudanças nos arquivos. Opções para deixá-lo
sempre ativo:

- **Mais simples:** deixar o terminal aberto em segundo plano enquanto trabalha.
- **Windows:** criar uma tarefa no Agendador de Tarefas que rode
  `pythonw sync_watcher.py` na inicialização (pythonw evita abrir janela de console).
- **Como serviço:** usar `nssm` (Windows) ou `systemd`/`supervisor` (Linux/Mac) para
  rodar como serviço de background persistente.

## Escopos — se os arquivos não foram criados por este app

O script usa o escopo `drive.file`, que só permite ao app acessar arquivos que
ELE MESMO criou ou que foram explicitamente abertos com ele. Como os arquivos
`lawfare.json` e `claude.ai-corpus-ids-sync.json` provavelmente já existiam no
seu Drive antes (você me passou os IDs deles), pode ser que o `files().update()`
falhe com erro 404 "File not found" — isso não significa que o arquivo não existe,
significa que o app não tem permissão para vê-lo com esse escopo restrito.

**Se isso acontecer:** troque, no topo do `sync_watcher.py`:

```python
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
```

por:

```python
SCOPES = ["https://www.googleapis.com/auth/drive"]
```

Isso dá ao app acesso de leitura/escrita a todo o seu Drive (não só aos arquivos
que ele criou) — necessário neste caso porque os arquivos já existiam. Depois de
trocar, apague o `token.json` e rode o script de novo para re-autenticar com o
novo escopo.

## Testando se está funcionando

1. Rode o script.
2. Abra `claude.ai-corpus-ids-sync.json` em qualquer editor, mude uma vírgula, salve.
3. Em até `DEBOUNCE_SECONDS` (3 segundos por padrão) + alguns segundos de rede,
   deve aparecer no terminal:
   ```
   Enviando 'claude.ai-corpus-ids-sync.json' para o Google Drive (file id ...)...
   OK — 'claude.ai-corpus-ids-sync.json' atualizado no Drive. modifiedTime=...
   ```
4. Confira no Drive (web) que o "Modificado em" do arquivo mudou para agora.

## Erros comuns

| Sintoma | Causa provável | Solução |
|---|---|---|
| `credentials.json não encontrado` | Passo 2 não concluído | Repita o Passo 2 |
| Erro 404 ao subir | Escopo insuficiente (arquivo não foi criado por este app) | Ver seção "Escopos" acima |
| Erro 403 `insufficientPermissions` | Conta logada não é a dona do arquivo, ou app não autorizado como usuário de teste | Confirme que logou com a conta certa e que ela está em "Usuários de teste" na tela de consentimento |
| Nada acontece ao salvar | Caminho errado em `WATCHED_FILES`, ou editor salva em local temporário antes de mover | Confira o caminho exato (copie do Explorer/Finder); alguns editores (Vim, alguns IDEs) usam "salvar como novo arquivo + renomear" — o handler `on_created` já cobre esse caso, mas confirme o comportamento do seu editor específico |
