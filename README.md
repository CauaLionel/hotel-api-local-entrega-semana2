# Hotel API

API de Hotelaria desenvolvida em Python com FastAPI como projeto de estudo.

## Tecnologias utilizadas

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker
- Pytest
- JWT para autenticação
- Pydantic

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

### Documentação
A API possui documentação automática através do Swagger.

Com a API em execução, acesse:

http://localhost:8000/docs

## Banco de dados

O projeto utiliza PostgreSQL como banco de dados.

O PostgreSQL é executado através do Docker Compose.

## Docker

O projeto possui dois serviços principais:

- `api` — aplicação FastAPI
- `postgres` — banco de dados PostgreSQL

Para iniciar os containers:

```bash
docker compose up -d
```

Para verificar os containers:

```bash
docker compose ps
```

Para parar os containers:

```bash
docker compose down
```

## Testes

Os testes automatizados são executados com Pytest.

Como a API e o PostgreSQL estão rodando em containers, os testes podem ser executados dentro do container da API:

```bash
docker compose exec api python -m pytest
```

Atualmente, os testes do projeto estão passando.

## Endpoints principais

### Autenticação

```text
POST /auth/register
POST /auth/login
```

### Hotéis

```text
POST   /hoteis/
GET    /hoteis/
GET    /hoteis/{hotel_id}
PUT    /hoteis/{hotel_id}
DELETE /hoteis/{hotel_id}
```

### Quartos

```text
POST   /quartos/
GET    /quartos/
GET    /quartos/{quarto_id}
PUT    /quartos/{quarto_id}
DELETE /quartos/{quarto_id}
```

### Reservas

```text
POST   /reservas/
GET    /reservas/
GET    /reservas/{reserva_id}
PUT    /reservas/{reserva_id}
DELETE /reservas/{reserva_id}
```

## Como executar o projeto

Clone o projeto e entre na pasta:

```bash
cd hotel-api-local
```

Inicie os containers:

```bash
docker compose up -d
```

Verifique se os serviços estão funcionando:

```bash
docker compose ps
```

Acesse a documentação da API:

```text
http://localhost:8000/docs
```

Para executar os testes:

```bash
docker compose exec api python -m pytest
```

## Objetivo

Este projeto foi desenvolvido com objetivo de praticar conceitos de desenvolvimento Backend, criação de APIs REST, banco de dados, autenticação, testes automatizados e Docker.