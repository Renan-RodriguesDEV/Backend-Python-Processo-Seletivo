# Backend Python - Microsserviço de Reservas

## 📋 Descrição

Este é o microsserviço responsável pelo gerenciamento de **reservas de salas**, **salas** e **locais/filiais** da plataforma Banana Ltda. O serviço expõe uma API RESTful que permite operações de CRUD (Create, Read, Update, Delete) em reservas, com validação de conflitos de horários e integração com o microsserviço de autenticação C#.

### Responsabilidades na Arquitetura

- **CRUD Completo**: Gerenciar reservas, salas e locais
- **Validação de Conflitos de Horários**: Impedir reservas sobrepostas na mesma sala e local
- **Validação de JWT**: Validar tokens JWT emitidos pelo backend C# em todas as rotas protegidas
- **Persistência**: Armazenar dados em banco de dados relacional independente

### Fluxo de Integração

1. Frontend realiza login no Backend C# e recebe token JWT
2. Frontend envia requisições para este serviço com o JWT no header `Authorization: Bearer <token>`
3. Este serviço valida o token localmente usando a chave compartilhada (`JWT_SECRET`)
4. Se válido, processa a requisição; caso contrário, retorna erro 401

---

## 🛠️ Tecnologias e Justificativas

### Framework: FastAPI
- **Por quê?** Framework assíncrono e moderno, com excelente performance, documentação automática (Swagger/OpenAPI) e suporte nativo a validação com Pydantic
- **Vantagens**: Type hints, validação automática, documentação interativa em `/docs`

### ORM: SQLAlchemy 2.0
- **Por quê?** ORM mais maduro e robusto do Python, com suporte a múltiplos bancos relacionais
- **Vantagens**: Migrations automáticas, relacionamentos bem definidos, query builder type-safe

### Banco de Dados: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Por quê?** SQLite para facilitar desenvolvimento local sem dependências externas; PostgreSQL para produção com escalabilidade
- **Configurável via**: Variável de ambiente `DATABASE_URL`

### Autenticação: PyJWT
- **Por quê?** Biblioteca padrão para decodificação e validação de tokens JWT
- **Implementação**: Validação local do token usando chave compartilhada com Backend C#

### CORS: Middleware FastAPI
- **Por quê?** Permite requisições do Frontend React sem problemas de origem
- **Configuração**: Aceita requisições de qualquer origem em desenvolvimento

### Validação de Dados: Pydantic
- **Por quê?** Integrada ao FastAPI, oferece validação automática e serialização de dados
- **Uso**: Schemas de request/response, type hints automáticos

---

## 🚀 Como Rodar Localmente

### Pré-requisitos

- Python 3.12+
- `uv` (gerenciador de pacotes e ambiente, recomendado) ou `pip`

### Instalação

#### Usando `uv` (recomendado)

```bash
# Clonar o repositório
git clone https://github.com/Renan-RodriguesDEV/Backend-Python-Processo-Seletivo.git
cd backend-python

# Instalar dependências
uv sync

# Ativar o ambiente virtual
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

#### Usando `pip`

```bash
# Clonar o repositório
git clone https://github.com/Renan-RodriguesDEV/Backend-Python-Processo-Seletivo.git
cd backend-python

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### Executar o Servidor

```bash
# Usando uv (direto, sem ativar venv)
uv run main.py

# Ou com pip (depois de ativar o venv)
python main.py

# Ou com uvicorn diretamente
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

O servidor estará disponível em `http://localhost:8000`

- **Documentação Interativa**: http://localhost:8000/docs
- **Documentação OpenAPI**: http://localhost:8000/redoc

---

## 🧪 Rodando os Testes

### Com `pytest`
```bash
# Ativar o venv
.venv\Scripts\activate  # Windows
# ou
source .venv/bin/activate  # Linux/Mac

# Executar todos os testes
pytest
```

### Executar apenas os testes de reservas
```bash
pytest -m reservations_conflicts
```

> Observação: se `pytest` não estiver instalado, instale pelo `uv sync` ou `pip install -r requirements.txt`.

---

## 🔐 Configuração de Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Banco de Dados
DATABASE_URL=sqlite:///./test.db
# Para PostgreSQL: DATABASE_URL=postgresql://user:password@localhost/dbname

# JWT - Deve ser compartilhado com o Backend C#
JWT_SECRET=sua_chave_secreta_aqui
JWT_ALGORITHM=HS256
JWT_ISSUER=auth-service
JWT_AUDIENCE=reservation-service

# Modo Debug (False em produção)
DEBUG=False

# CORS (domínios permitidos, separados por vírgula)
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

### Variáveis Críticas

- **`JWT_SECRET`**: Chave para validar tokens JWT. **DEVE SER A MESMA DO BACKEND C#**
- **`DATABASE_URL`**: URL de conexão com banco de dados
  - Desenvolvimento: `sqlite:///./test.db` (arquivo local)
  - Produção: `postgresql://user:pass@host/db`

---

## 📡 Endpoints da API

### Autenticação
Todos os endpoints abaixo requerem token JWT no header:
```
Authorization: Bearer <token_jwt>
```

### Reservas

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/reservations/` | Criar nova reserva |
| `GET` | `/reservations/` | Listar todas as reservas |
| `GET` | `/reservations/{id}` | Obter detalhes de uma reserva |
| `PUT` | `/reservations/{id}` | Atualizar uma reserva |
| `DELETE` | `/reservations/{id}` | Deletar uma reserva |
| `DELETE` | `/reservations/` | Deletar todas as reservas |

### Salas

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/rooms/` | Criar nova sala |
| `GET` | `/rooms/` | Listar todas as salas |
| `PUT` | `/rooms/{id}` | Atualizar uma sala |

### Locais/Filiais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/locations/` | Criar novo local |
| `GET` | `/locations/` | Listar todos os locais |

### Exemplo de Requisição

```bash
# Criar uma reserva
curl -X POST http://localhost:8000/reservations/ \
  -H "Authorization: Bearer seu_token_jwt" \
  -H "Content-Type: application/json" \
  -d '{
    "room_id": 1,
    "start_datetime": "2026-05-20T10:00:00",
    "end_datetime": "2026-05-20T11:00:00",
    "responsible": "João Silva",
    "coffee": true,
    "people_count": 5,
    "description": "Reunião com stakeholders"
  }'
```

---

## 🏗️ Estrutura do Projeto

```
backend-python/
├── auth/
│   └── auth.py              # Validação JWT
├── config/
│   ├── db.py                # Configuração de banco de dados
│   └── logger.py            # Configuração de logging
├── models/
│   ├── entities/            # Modelos SQLAlchemy
│   │   ├── base.py
│   │   ├── locations.py
│   │   ├── reservations.py
│   │   └── rooms.py
│   └── schemas/             # Schemas Pydantic para validação
│       ├── locations.py
│       ├── reservations.py
│       └── rooms.py
├── routes/
│   ├── locations.py         # Endpoints de locais
│   ├── reservations.py      # Endpoints de reservas
│   └── rooms.py             # Endpoints de salas
├── main.py                  # Ponto de entrada da aplicação
├── pyproject.toml           # Definição de dependências (uv)
├── requirements.txt         # Dependências (pip)
└── README.md                # Este arquivo
```

---

## 📦 Dependências Principais

- **FastAPI 0.136.1**: Web framework assíncrono
- **Uvicorn 0.46.0+**: ASGI server para rodar FastAPI
- **SQLAlchemy 2.0.39**: ORM para banco de dados
- **Pydantic 2.13.4**: Validação de dados
- **PyJWT 2.12.1**: Decodificação e validação de JWT

Ver `pyproject.toml` para lista completa.

---

## ✅ Validações Implementadas

### Reservas
- ✅ Validação de token JWT em todas as rotas protegidas
- ✅ Verificação de disponibilidade de sala (sem conflitos de horário)
- ✅ Validação de campos obrigatórios (sala, data/hora início, data/hora fim, responsável)
- ✅ Validação de datas válidas (fim > início)

### Salas
- ✅ Validação de nome e capacidade
- ✅ Relacionamento com locais

### Locais
- ✅ Validação de nome único
- ✅ Validação de endereço

---

## 🔄 Fluxo de Autenticação

1. **Frontend faz login no Backend C#**
   ```
  POST /api/user/login
   ```
   Retorna JWT com payload contendo `sub` (user_id) e `email`

2. **Frontend envia requisição para Backend Python com JWT**
   ```
   POST /reservations/
   Authorization: Bearer eyJhbGciOiJIUzI1NiI...
   ```

3. **Backend Python valida JWT localmente**
   - Decodifica o token usando `JWT_SECRET`
   - Valida assinatura
   - Verifica se `sub` e `email` existem
   - Se válido, processa requisição
   - Se inválido, retorna 401 Unauthorized

---

## 🗄️ Migrations do Banco de Dados

### Primeira execução
O SQLAlchemy cria as tabelas automaticamente na primeira execução baseado nos modelos.

### Criar tabelas manualmente
```python
from models.entities.base import Base
from config.db import get_engine

Base.metadata.create_all(bind=get_engine())
```

---

## 📝 Exemplo de Payload JWT Esperado

```json
{
  "sub": "123",
  "email": "usuario@example.com",
  "exp": 1715945400,
  "iat": 1715858000
}
```

---

## 🧪 Testando a API

### Com Postman
1. Obter token JWT do Backend C# (`/auth/login`)
2. Ir para http://localhost:8000/docs
3. Clicar em "Authorize" e colar o token
4. Testar os endpoints

### Com cURL
```bash
# Listar locais
curl -X GET http://localhost:8000/locations/ \
  -H "Authorization: Bearer seu_token_jwt"

# Criar sala
curl -X POST http://localhost:8000/rooms/ \
  -H "Authorization: Bearer seu_token_jwt" \
  -H "Content-Type: application/json" \
  -d '{"name": "Sala A", "location_id": 1, "capacity": 10}'

# Criar reserva
curl -X POST http://localhost:8000/reservations/ \
  -H "Authorization: Bearer seu_token_jwt" \
  -H "Content-Type: application/json" \
  -d '{
    "room_id": 1,
    "start_datetime": "2026-05-20T10:00:00",
    "end_datetime": "2026-05-20T11:00:00",
    "responsible": "João Silva"
  }'
```

---

## 🚨 Tratamento de Erros

A API retorna erros padrão HTTP com descrição:

```json
{
  "detail": "Invalid token"
}
```

**Códigos HTTP**:
- `200 OK`: Sucesso
- `201 Created`: Recurso criado
- `400 Bad Request`: Dados inválidos
- `401 Unauthorized`: Token inválido ou ausente
- `404 Not Found`: Recurso não encontrado
- `409 Conflict`: Conflito de horário (reserva sobreposta)

---

## 🔐 Segurança

- ✅ Validação de JWT em todas as rotas protegidas
- ✅ Type hints para evitar erros
- ✅ Validação automática de entrada via Pydantic
- ✅ CORS configurável por ambiente
- ✅ Senha compartilhada (`JWT_SECRET`) entre serviços

---

## 📚 Referências

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org)
- [PyJWT Documentation](https://pyjwt.readthedocs.io)
- [Pydantic Documentation](https://docs.pydantic.dev)

---

## 📧 Suporte

Para dúvidas sobre o microsserviço, consulte a documentação interativa em `/docs` da aplicação.
