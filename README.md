# Assistente Virtual

Este é um projeto de assistente virtual desenvolvido com Streamlit e Amazon Bedrock, oferecendo uma interface de chat interativa com capacidade de processamento de linguagem natural.

## Sobre o Projeto

O assistente virtual é uma aplicação web que permite:
- Interação via chat com processamento de linguagem natural
- Sistema de autenticação por senha
- Feedback do usuário para respostas do assistente
- Persistência de dados das conversas
- Interface amigável e responsiva

## Tecnologias Utilizadas

- **Frontend e Backend**: Python com Streamlit
- **Processamento de Linguagem Natural**: Amazon Bedrock com LangChain
- **Armazenamento de Dados**: Amazon DynamoDB
- **Gerenciamento de Ambiente**: Python dotenv
- **Agente de IA**: LangGraph com ReAct Agent
- **Base de Conhecimento**: Amazon Bedrock Knowledge Base

## Pré-requisitos

- Python 3.8 ou superior
- Pip (gerenciador de pacotes Python)
- Conta AWS com acesso ao Bedrock e DynamoDB
- Credenciais AWS configuradas localmente

## Configuração do Ambiente de Desenvolvimento

1. Clone o repositório:
```bash
git clone https://github.com/nuage-it/nuageit-poc-models
cd nuageit-poc-models/agent_bedrock_with_streamlit
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente copiando o arquivo `.env.example` para `.env` na raiz do projeto:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações. Abaixo está a descrição de cada variável de ambiente:

### Configurações da Aplicação
- `TITLE`: Define o título principal da aplicação que aparece na interface do usuário
- `SUBTITLE`: Define o subtítulo ou mensagem de boas-vindas da aplicação
- `PASSWORD`: Senha de acesso para a interface administrativa (altere para uma senha segura)

### Configuração do SDK AWS
- `AWS_DEFAULT_REGION`: Região AWS padrão para a aplicação

### Configurações AWS DynamoDB
- `DYNAMODB_TABLE`: Nome da tabela no DynamoDB onde serão armazenados os dados da aplicação
- `DYNAMODB_REGION`: Região AWS onde a tabela do DynamoDB está localizada (ex: us-east-1)

### Configurações Amazon Bedrock
- `BEDROCK_MODEL_ID`: Identificador do modelo de IA do Amazon Bedrock (padrão: amazon.nova-pro-v1:0)
- `BEDROCK_REGION`: Região AWS onde o serviço Bedrock está disponível
- `BEDROCK_MODEL_TEMPERATURE`: Controla a aleatoriedade das respostas do modelo (0.0 a 1.0)
- `BEDROCK_MODEL_MAX_TOKENS`: Limite máximo de tokens na resposta do modelo
- `BEDROCK_KB_ID`: Identificador da Knowledge Base no Amazon Bedrock
- `BEDROCK_KB_MAX_RESULTS`: Número máximo de resultados retornados pela Knowledge Base
- `BEDROCK_AGENT_PROMPT`: Prompt inicial que define o comportamento e contexto do assistente virtual
```

## Executando o Projeto Localmente

1. Ative o ambiente virtual (se ainda não estiver ativo)

2. Execute a aplicação:
```bash
streamlit run app.py
```

3. Acesse a aplicação em seu navegador através do endereço: `http://localhost:8501`

## Deployment em Produção

### Usando Docker

O projeto já inclui um Dockerfile configurado. Para executar:

```bash
# Construir a imagem
docker build -t brb-seguros-assistant .

# Executar o container
docker run -d -p 80:80 \
  --env-file .env \
  brb-seguros-assistant
```

O Dockerfile utiliza Python 3.12 e configura automaticamente todas as dependências necessárias para a execução do projeto.

## Estrutura do Projeto

```
├── app.py              # Aplicação principal
├── config.py           # Configurações e variáveis de ambiente
├── persist.py          # Funções de persistência de dados
├── llm.py              # Integração com Amazon Bedrock e LangChain
├── requirements.txt    # Dependências do projeto
├── Dockerfile          # Configuração para containerização
└── .env               # Variáveis de ambiente (não versionado)
```

## Considerações de Segurança

- Nunca compartilhe ou comite o arquivo `.env` com credenciais
- Mantenha as credenciais AWS seguras e use políticas de IAM adequadas
- Utilize senhas fortes para a autenticação da aplicação
- Em produção, considere adicionar camadas adicionais de segurança

## Monitoramento e Logs

- A aplicação registra informações sobre:
  - Criação e atualização de chats
  - Mensagens trocadas
  - Feedbacks dos usuários
  - Tokens consumidos nas interações

## Suporte

Para questões e suporte, por favor abra uma issue no repositório do projeto.