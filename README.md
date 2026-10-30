# Hotel API

API de Hotelaria desenvolvida em Python com FastAPI como projeto de estudo, evoluindo de uma API REST tradicional para uma aplicação com recursos de Inteligência Artificial.

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

### Reservas

- Criar reserva
- Listar reservas
- Buscar reserva por ID
- Atualizar reserva
- Excluir reserva
- Controle de disponibilidade dos quartos

### Autenticação

- Cadastro de usuário
- Login
- Autenticação utilizando JWT

### Inteligência Artificial

A API possui integração com modelos de linguagem locais através do Ollama.

- **Summarize:** geração de resumos de textos.
- **Classify:** classificação de mensagens.
- **Analyze:** análise de textos e identificação de informações relevantes.
- **RAG (Retrieval-Augmented Generation):** respostas geradas com base em documentos do hotel.
- **Tool Calling:** consultas ao banco de dados para obter informações sobre hotéis, reservas e disponibilidade de quartos.

### RAG e banco vetorial

A funcionalidade RAG utiliza o documento `documentos/hotel.txt` como fonte de informações sobre as regras e os serviços do hotel.

O processamento segue as etapas:

1. Leitura do documento.
2. Divisão do conteúdo em chunks.
3. Geração de embeddings utilizando o modelo Nomic Embed Text.
4. Armazenamento dos vetores no ChromaDB.
5. Busca por trechos relevantes.
6. Envio do contexto recuperado ao modelo Llama 3.2.
7. Geração da resposta baseada no documento.

O ChromaDB utiliza armazenamento persistente para manter os documentos indexados.

### Tool Calling

A API também permite consultar informações diretamente no PostgreSQL por meio de funções específicas:

- `consultar_hotel()`: consulta os hotéis cadastrados.
- `consultar_reserva()`: consulta as reservas cadastradas.
- `consultar_disponibilidade()`: consulta os quartos disponíveis.

O endpoint de perguntas identifica quando a solicitação exige informações do banco de dados e retorna os resultados correspondentes.

## Documentação

A API possui documentação automática através do Swagger.

Com a API em execução, acesse:

[http://localhost:8000/docs](http://localhost:8000/docs)

## Banco de dados

O projeto utiliza PostgreSQL como banco de dados relacional.

O PostgreSQL é executado através do Docker Compose, com armazenamento persistente.

## Docker

O projeto utiliza os seguintes serviços e recursos:

- `api` — aplicação FastAPI.
- `postgres` — banco de dados PostgreSQL.
- `chroma_data` — volume persistente para o banco vetorial ChromaDB.
- `postgres_data` — volume persistente para os dados do PostgreSQL.

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

## Configuração da Inteligência Artificial

O projeto utiliza o Ollama instalado na máquina hospedeira, permitindo executar modelos de linguagem localmente.

Instale o Ollama e baixe os modelos utilizados:

```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

O modelo `llama3.2:3b` é utilizado para geração de respostas, resumos, classificações e análises.

O modelo `nomic-embed-text` é utilizado para gerar embeddings dos documentos e das perguntas.

A aplicação executada no Docker acessa o Ollama através do endereço:

```text
http://host.docker.internal:11434
```

É necessário manter o Ollama em execução na máquina hospedeira para utilizar os recursos de IA.

## Endpoints principais

### Autenticação

```http
POST /auth/register
POST /auth/login
```

### Hotéis

```http
POST   /hoteis/
GET    /hoteis/
GET    /hoteis/{hotel_id}
PUT    /hoteis/{hotel_id}
DELETE /hoteis/{hotel_id}
```

### Quartos

```http
POST   /quartos/
GET    /quartos/
GET    /quartos/{quarto_id}
PUT    /quartos/{quarto_id}
DELETE /quartos/{quarto_id}
```

### Reservas

```http
POST   /reservas/
GET    /reservas/
GET    /reservas/{reserva_id}
PUT    /reservas/{reserva_id}
DELETE /reservas/{reserva_id}
```

### Inteligência Artificial

```http
POST /ai/summarize
POST /ai/classify
POST /ai/analyze
POST /ai/ask
```

Os endpoints de processamento de texto recebem um campo `text`.

O endpoint `/ai/ask` recebe uma pergunta no mesmo formato e pode consultar documentos ou informações do banco de dados.

Exemplo:

```json
{
  "text": "Qual o horário de check-in?"
}
```

## Como executar o projeto

Clone o repositório:

```bash
git clone https://github.com/CauaLionel/hotel-api-local-entrega-semana2.git
```

Entre na pasta do projeto:

```bash
cd hotel-api-local-entrega-semana2
```

Inicie os containers:

```bash
docker compose up -d --build
```

Verifique se os serviços estão funcionando:

```bash
docker compose ps
```

Acesse a documentação da API:

```text
http://localhost:8000/docs
```

Para executar os testes automatizados:

```bash
docker compose exec api python -m pytest
```

**Observação:** para utilizar os recursos de Inteligência Artificial, também é necessário instalar e executar o Ollama na máquina hospedeira e baixar os modelos llama3.2:3b e nomic-embed-text.
