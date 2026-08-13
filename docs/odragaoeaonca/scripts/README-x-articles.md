# Gap analysis — X Articles vs `artigos/`

Script: [`fetch_x_articles.py`](fetch_x_articles.py)  
Deps: [`requirements-x-articles.txt`](requirements-x-articles.txt)  
Relatório: [`../artigos/publication-status.md`](../artigos/publication-status.md)  
Env exemplo: [`../.env.example`](../.env.example)

---

## Como obter os tokens

Portal: [console.x.com](https://console.x.com) (ou [developer.x.com](https://developer.x.com) → Developer Console).  
É preciso conta de desenvolvedor + **Project** + **App** + créditos/pay-per-use ativos.

### Pré-requisitos (uma vez)

1. Entre em [console.x.com](https://console.x.com) com a conta **@araguaci** (ou a conta dona do App).
2. Crie ou abra um **Project** → **App**.
3. Em **App settings → User authentication settings** (se for usar Access Token de usuário):
   - App permissions: **Read** (mínimo).
   - Type: **Web App** ou **Native App** (OAuth 2.0).
   - Callback URL: qualquer URL local válida se o console exigir (ex. `http://127.0.0.1:3000/callback`).
4. Abra **Keys and tokens** do App.

### `X_API_BEARER_TOKEN` — Bearer app-only

**O que é:** token OAuth 2.0 *application-only*. Autentica o App, **sem** contexto de usuário.  
**Uso neste projeto:** listar posts públicos de `@araguaci` (`GET /2/users/:id/tweets`) se a conta for pública.  
**Custo típico:** leitura de posts de terceiros (pay-per-use); owned reads só com token de usuário.

**Como montar no console**

1. **Keys and tokens** → seção **Bearer Token**.
2. **Generate** / **Regenerate** → copiar o valor (começa em geral com `AAAA…`).
3. No `.env`:

```env
X_API_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAA...seu_bearer...
```

**Alternativa via API** (API Key + API Secret do mesmo App):

```bash
curl -u "$API_KEY:$API_SECRET_KEY" \
  --data "grant_type=client_credentials" \
  "https://api.x.com/oauth2/token"
```

A resposta traz `"access_token": "..."` — esse valor é o Bearer. Cole em `X_API_BEARER_TOKEN`.

### `X_BEARER_TOKEN` — alias do Bearer

**O que é:** o **mesmo** Bearer app-only. Só existe como nome alternativo aceito pelo script.

```env
# Use um OU outro — não precisa dos dois
X_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAA...mesmo_bearer...
```

Prioridade: se `X_API_BEARER_TOKEN` estiver preenchido, `X_BEARER_TOKEN` é ignorado.

### `X_ACCESS_TOKEN` — token com contexto de usuário (preferido)

**O que é:** token que age **em nome do usuário** (@araguaci).  
**Por que preferir:** `GET /2/users/{id}/tweets` na **sua** conta conta como *owned read* (~mais barato no pay-per-use) e costuma ter acesso mais estável aos seus próprios posts/Articles.

Há dois jeitos comuns no console:

#### A) Access Token & Secret (OAuth 1.0a) — “Keys and tokens”

1. **Keys and tokens** → **Access Token and Secret**.
2. **Generate** (vinculado à conta X logada no portal).
3. Copie o **Access Token** (não o Access Token Secret) para:

```env
X_ACCESS_TOKEN=...seu_access_token...
```

> O script atual envia esse valor no header `Authorization: Bearer …`.  
> Se a chamada falhar com 401, use o Bearer app-only (`X_API_BEARER_TOKEN`) **ou** gere um Access Token OAuth 2.0 User Context (abaixo). OAuth 1.0a “puro” exige assinatura; nem todo Access Token 1.0a funciona como Bearer.

#### B) OAuth 2.0 User Context (recomendado se A der 401)

1. Em **User authentication settings**, ative **OAuth 2.0** com escopos pelo menos `tweet.read` + `users.read`.
2. Complete o fluxo de autorização (PKCE) com a conta @araguaci e obtenha o **access token** de usuário.
3. Cole em:

```env
X_ACCESS_TOKEN=...access_token_oauth2_user...
```

Ferramentas: Postman (OAuth 2.0 Authorization Code + PKCE) ou scripts oficiais da [X Developer Platform](https://docs.x.com/fundamentals/authentication/overview).

### Qual variável usar?

| Variável | Tipo | Quando usar |
|----------|------|-------------|
| `X_ACCESS_TOKEN` | User context | **Preferido** — seus Articles, owned reads |
| `X_API_BEARER_TOKEN` | App-only Bearer | Conta pública; setup mais simples |
| `X_BEARER_TOKEN` | Alias do Bearer | Se já tem esse nome em outros projetos |

**Prioridade no script:** `X_ACCESS_TOKEN` → `X_API_BEARER_TOKEN` → `X_BEARER_TOKEN` → `TWITTER_BEARER_TOKEN`.

### Segurança

- `.env` está no `.gitignore` — não commitar.
- Regenere tokens se vazar (console → Regenerate).
- Não cole tokens no chat, README ou commits.

---

## Setup rápido

```bash
cp .env.example .env
# editar tokens (acima)

pip install -r scripts/requirements-x-articles.txt
python scripts/fetch_x_articles.py --username araguaci --update-map
```

Alternativas sem `.env`:

```bash
python scripts/fetch_x_articles.py --token-file caminho/do/token.txt
python scripts/fetch_x_articles.py --from-json dump-articles.json
```

## Flags

| Flag | Efeito |
|------|--------|
| `--username` | Default `araguaci` |
| `--update-map` | Grava matches fortes em `artigos/published-map.json` |
| `--annotate` | Insere `<!-- published: URL -->` nos `.md` canônicos |
| `--from-json PATH` | Usa dump local em vez da API |
| `--token-file PATH` | Token em arquivo (1 linha) |
| `--no-mirror` | Não grava `artigos/_published/` |

## Matching

1. `published-map.json` (manual / seed)
2. Similaridade de título ≥ 0.82
3. Fingerprints (T-ID, UF, termos do H1)

Canônicos = `*-xarticle.md` sem `*-old.md`.
