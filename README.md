# Hotel API

API de hotelaria desenvolvida em Python com FastAPI como projeto de estudo. O projeto evoluiu de uma API REST tradicional para uma aplicação com recursos de Inteligência Artificial, integração com banco de dados e recuperação de informações por documentos.

## Tecnologias utilizadas

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker e Docker Compose
- Pytest
- JWT para autenticação
- Pydantic
- Ollama
- Llama 3.2
- ChromaDB
- Nomic Embed Text

## Funcionalidades

### Hotéis

- Criar hotel
- Listar hotéis
- Buscar hotel por ID
- Atualizar hotel
- Excluir hotel

### Quartos

- Criar quarto
- Listar quartos
- Buscar quarto por ID
- Atualizar quarto
- Excluir quarto
- Controle de disponibilidade dos quartos

### Reservas

- Criar reserva
- Listar reservas
- Buscar reserva por ID
- Atualizar reserva
- Excluir reserva

### Autenticação

- Cadastro de usuário
- Login
- Autenticação utilizando JWT

### Inteligência Artificial

A API possui integração com modelos de linguagem locais através do Ollama.

- **Summarize:** geração de resumos de textos.
- **Classify:** classificação de mensagens.
- **Analyze:** análise de textos e identificação de informações relevantes.
- **RAG (Retrieval-Augmented Generation):** geração de respostas com base em documentos do hotel.
- **Consultas ao banco de dados:** utilização de funções específicas para consultar hotéis, reservas e disponibilidade de quartos.

## RAG e banco de dados vetorial

A funcionalidade RAG utiliza o documento `documentos/hotel.txt` como fonte de informações sobre as regras e os serviços do hotel.

O processamento segue as seguintes etapas:

1. Leitura do documento.
2. Divisão do conteúdo em chunks.
3. Geração de embeddings utilizando o modelo Nomic Embed Text.
4. Armazenamento dos vetores no ChromaDB.
5. Busca por trechos relevantes de acordo com a pergunta.
6. Envio do contexto recuperado ao modelo Llama 3.2.
7. Geração de uma resposta baseada nas informações encontradas.

O ChromaDB utiliza armazenamento persistente para manter os documentos indexados.

## Consultas ao banco de dados (Tool Calling)

A API também permite consultar informações diretamente no PostgreSQL por meio de funções específicas:

- `consultar_hotel()`: consulta os hotéis cadastrados.
- `consultar_reserva()`: consulta as reservas cadastradas.
- `consultar_disponibilidade()`: consulta os quartos disponíveis.

O endpoint `/ai/ask` identifica o tipo de pergunta e direciona a consulta para a função correspondente ou para o mecanismo RAG, quando a informação está nos documentos.

## Documentação

A API possui documentação automática através do Swagger.

Com a aplicação em execução, acesse:

[http://localhost:8000/docs](http://localhost:8000/docs)

## Banco de dados

O projeto utiliza PostgreSQL como banco de dados relacional.

O PostgreSQL é executado através do Docker Compose e possui armazenamento persistente por meio de volume Docker.

## Docker

O projeto utiliza os seguintes serviços e recursos:

- `api` — aplicação FastAPI.
- `postgres` — banco de dados PostgreSQL.
- `postgres_data` — volume persistente para os dados do PostgreSQL.
- `chroma_data` — volume persistente para o banco vetorial ChromaDB.

### Comandos Docker

Para iniciar ou reconstruir os containers:

```bash
docker compose up -d --build
```

Para verificar os containers:

```bash
docker compose ps
```

Para visualizar os logs da API:

```bash
docker compose logs api --tail 100
```

Para parar os containers:

```bash
docker compose down
```

> **Importante:** o comando `docker compose down` preserva os volumes. Não utilize `docker compose down -v` se quiser manter os dados armazenados.

## Configuração da Inteligência Artificial

O projeto utiliza o Ollama instalado na máquina hospedeira, permitindo executar modelos de linguagem localmente.

### 1. Instalar o Ollama

Instale o Ollama através do site oficial:

[https://ollama.com/download](https://ollama.com/download)

### 2. Baixar os modelos utilizados

Com o Ollama instalado e em execução, abra o terminal e execute:

```bash
ollama pull llama3.2:3b
```

```bash
ollama pull nomic-embed-text
```

### 3. Modelos utilizados

- **llama3.2:3b:** utilizado para geração de respostas, resumos, classificações e análises.
- **nomic-embed-text:** utilizado para gerar embeddings dos documentos e das perguntas.

A aplicação executada no Docker acessa o Ollama através do endereço:

```text
http://host.docker.internal:11434
```

É necessário manter o Ollama em execução na máquina hospedeira para utilizar os recursos de Inteligência Artificial.

## Endpoints principais

### Autenticação

| Método | Endpoint |
|---|---|
| POST | `/auth/register` |
| POST | `/auth/login` |

### Hotéis

| Método | Endpoint |
|---|---|
| POST | `/hoteis/` |
| GET | `/hoteis/` |
| GET | `/hoteis/{hotel_id}` |
| PUT | `/hoteis/{hotel_id}` |
| DELETE | `/hoteis/{hotel_id}` |

### Quartos

| Método | Endpoint |
|---|---|
| POST | `/quartos/` |
| GET | `/quartos/` |
| GET | `/quartos/{quarto_id}` |
| PUT | `/quartos/{quarto_id}` |
| DELETE | `/quartos/{quarto_id}` |

### Reservas

| Método | Endpoint |
|---|---|
| POST | `/reservas/` |
| GET | `/reservas/` |
| GET | `/reservas/{reserva_id}` |
| PUT | `/reservas/{reserva_id}` |
| DELETE | `/reservas/{reserva_id}` |

### Inteligência Artificial

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/ai/summarize` | Resumo de textos |
| POST | `/ai/classify` | Classificação de mensagens |
| POST | `/ai/analyze` | Análise de textos |
| POST | `/ai/ask` | Perguntas sobre documentos e dados do sistema |

Os endpoints de processamento de texto recebem um campo `text`.

Exemplo de requisição para `/ai/ask`:

```json
{
  "text": "Qual o horário de check-in?"
}
```

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/CauaLionel/hotel-api-local-entrega-semana2.git
```

### 2. Entrar na pasta do projeto

```bash
cd hotel-api-local-entrega-semana2
```

### 3. Iniciar os containers

```bash
docker compose up -d --build
```

### 4. Verificar os serviços

```bash
docker compose ps
```

### 5. Acessar a documentação

Com a API em execução, acesse:

[http://localhost:8000/docs](http://localhost:8000/docs)

### 6. Executar os testes automatizados

```bash
docker compose exec api python -m pytest
```

**Observação:** para utilizar os recursos de Inteligência Artificial, também é necessário instalar e executar o Ollama na máquina hospedeira e baixar os modelos `llama3.2:3b` e `nomic-embed-text`.

## Testes

Além dos testes automatizados com Pytest, foram realizados testes funcionais dos recursos de Inteligência Artificial através do Swagger:

- Geração de resumos.
- Classificação de mensagens.
- Análise de textos.
- Recuperação de informações através do RAG.
- Consultas ao banco de dados através das funções de Tool Calling.

## Objetivo

Este projeto foi desenvolvido com o objetivo de praticar conceitos de desenvolvimento Backend, criação de APIs REST, integração com bancos de dados relacionais, autenticação, testes automatizados, Docker e Inteligência Artificial.

O desenvolvimento também explora conceitos de RAG, embeddings, bancos de dados vetoriais e integração de modelos de linguagem com sistemas existentes.
