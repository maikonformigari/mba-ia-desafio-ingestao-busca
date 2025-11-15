# Desafio MBA Engenharia de Software com IA - Full Cycle

## Ingestão e Busca Semântica com LangChain e Postgres

Este projeto implementa um sistema RAG (Retrieval-Augmented Generation) completo para ingestão de documentos PDF, busca vetorial semântica e chat interativo usando LangChain e PGVector.

## 🚀 Tecnologias Utilizadas

- **Python 3.x** - Linguagem de programação principal
- **LangChain** - Framework para desenvolvimento de aplicações com LLMs
- **OpenAI API** - Modelos de embeddings e chat (GPT)
- **PGVector** - Extensão do PostgreSQL para armazenamento e busca vetorial
- **PostgreSQL** - Banco de dados relacional
- **Docker** - Containerização do banco de dados

## 📋 Requisitos

- Python 3.8 ou superior
- Docker e Docker Compose
- Conta na OpenAI com API Key ativa

### Obter API Key da OpenAI

1. Acesse [platform.openai.com](https://platform.openai.com/)
2. Faça login ou crie uma conta
3. Navegue até **API Keys** no menu
4. Clique em **Create new secret key**
5. Copie a chave gerada (você não poderá vê-la novamente)

## 🔧 Instruções de Execução

### 1. Clonar o Repositório

```bash
git clone https://github.com/maikonformigari/mba-ia-desafio-ingestao-busca.git
cd mba-ia-desafio-ingestao-busca
```

### 2. Configurar Ambiente Virtual Python

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar o arquivo .env e configurar as variáveis necessárias
```

Edite o arquivo `.env` e configure:
- `OPENAI_API_KEY` - Sua chave de API da OpenAI
- Demais variáveis já estão pré-configuradas

### 5. Subir o Banco de Dados PostgreSQL com PGVector

```bash
docker compose up -d
```

Aguarde alguns segundos para o banco inicializar completamente.

### 6. Executar Ingestão do PDF

```bash
python src/ingest.py
```

Este script irá:
- Carregar o arquivo PDF especificado
- Dividir o documento em chunks
- Gerar embeddings usando OpenAI
- Armazenar no banco de dados PGVector

### 7. Iniciar o Chat Interativo

```bash
python src/chat.py
```

Agora você pode fazer perguntas sobre o conteúdo do PDF ingerido. O sistema irá:
- Buscar os trechos mais relevantes usando busca vetorial
- Gerar respostas contextualizadas usando o modelo GPT
- Responder apenas com base no conteúdo do documento

Para sair do chat, digite: `sair`, `exit` ou `quit`

## 💬 Exemplos de Interação

### Perguntas sobre conteúdo do documento (respostas baseadas no PDF):

**Pergunta:** Qual o faturamento da Empresa SuperTechIABrazil?  
**Resposta:** O faturamento foi de 10 milhões de reais.

**Pergunta:** Quanto a Cobalto Telecom Serviços faturou e em qual ano foi isto?  
**Resposta:** Cobalto Telecom Serviços faturou R$ 903.084.047,52 em 1994.

### Perguntas fora do contexto do documento:

**Pergunta:** Qual o faturamento da Red Bull?  
**Resposta:** Não tenho informações necessárias para responder sua pergunta.

**Pergunta:** Qual a maior cidade do Brasil?  
**Resposta:** Não tenho informações necessárias para responder sua pergunta.

> **Nota:** O sistema responde apenas com base no conteúdo do documento PDF ingerido. Perguntas sobre informações não presentes no documento receberão a resposta padrão informando a ausência de informações necessárias.

## 📁 Estrutura do Projeto

```
.
├── docker-compose.yml      # Configuração do PostgreSQL com PGVector
├── requirements.txt        # Dependências Python
├── .env.example           # Exemplo de variáveis de ambiente
├── README.md              # Este arquivo
└── src/
    ├── ingest.py          # Script de ingestão de PDF
    ├── search.py          # Busca vetorial e geração de respostas
    └── chat.py            # Interface de chat interativo
```

## 🎯 Funcionalidades

- ✅ Ingestão de documentos PDF com chunking inteligente
- ✅ Geração de embeddings com OpenAI
- ✅ Armazenamento vetorial com PGVector
- ✅ Busca semântica por similaridade
- ✅ Geração de respostas contextualizadas com LLM
- ✅ Interface de chat interativa
- ✅ Respostas baseadas exclusivamente no contexto fornecido

## 📝 Notas

- Certifique-se de que o arquivo PDF especificado em `PDF_PATH` existe
- O modelo de embeddings padrão é `text-embedding-3-small`
- As respostas são geradas apenas com base no conteúdo do documento ingerido
- O sistema não utiliza conhecimento externo para responder perguntas