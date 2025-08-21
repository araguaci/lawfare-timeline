**Fase 0: Planejamento & Arquitetura**

    Definição de Escopo
    - Mapear questões do Bot
    - Detalhar opções da URA
    - Definir Fluxo 3 ("perfil diferente")
    - Formato da Pesquisa de Satisfação
    Tecnologia e Contratação
    - **API WhatsApp Business (Obrigatório)**
    - Escolha do Provedor (BSP)
    - Verificação da Empresa (Meta)
    - Registro do número de telefone
    Desenho da Arquitetura
    - **Criar API Middleware (PHP/Laravel)**
    - Definir Endpoints
    - Desenhar Webhooks
    - Modelagem do Banco de Dados (MSSQL)

**Fase 1: Integração Manual (Agente -> Cliente)**
    Backend (Middleware)
    - Endpoint: `/start-conversation`
    - Lógica para "Mensagem de Modelo"
    - Endpoint: `/whatsapp-webhook`
    Frontend (Sistema PHP Atual)
    - Botão "Iniciar WhatsApp" na UI
    - Chamada da API do Middleware
    Testes e Validação
    - Teste de fluxo completo
    - Registro de logs

**Fase 2: Automação (URA & Bot)**
    Configuração da URA
    - Habilitar chamadas HTTP (Webhook)
    - Apontar para o Middleware
    Lógica no Middleware
    - Endpoint: `/ivr-handler`
    - Roteamento por Opção (1, 2, 3)
    Desenvolvimento do Bot
    - Lógica no webhook de respostas
    - Árvore de decisão no DB
    - Palavra-chave para sair/transferir

**Fase 3: Pesquisa de Satisfação**
    Gatilhos de Encerramento
    - Botão "Finalizar" para o Agente
    - Fim do fluxo do Bot
    Implementação da Pesquisa
    - Envio de "Mensagem de Modelo" de pesquisa
    - Webhook para capturar a nota
    - Salvar resultado no DB (MSSQL)
    - Mensagem final de agradecimento

**Fase 4: Implantação & Operação**
    Go-Live
    - Deploy do Middleware
    - Deploy do Frontend PHP
    - Ativação da URA
    Treinamento
    - Capacitar Agentes e Supervisores
    Monitoramento
    - Logs e Alertas de Erro
    - Dashboards de Métricas (no sistema PHP)

**Requisitos Técnicos**
    Software
    - Conta API WhatsApp (BSP)
    - Servidor Web com PHP 8+
    - MSSQL Server
    - Certificado SSL (HTTPS)
    - Git
    Hardware
    - Servidor/VPS/Container para Middleware
    - Mín: 2 vCPU, 4GB RAM
    - Firewall e Rede Estável
