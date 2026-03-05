# Plataforma CRUD Completa (Python + FastAPI + PostgreSQL + dbt + DuckDB + Dagster + Streamlit)

## Estrutura

- `api/`: API transacional CRUD com FastAPI + SQLAlchemy.
- `app/`: Front-end Streamlit para operar CRUD.
- `analytics/`: projeto dbt com modelos em DuckDB.
- `orchestration/`: assets Dagster para executar `dbt run` e `dbt test`.
- `scripts/windows/`: scripts para iniciar API e app no Windows (com PostgreSQL).

## Pré-requisitos (Windows)

- Windows 10/11
- Python **3.10**
- PowerShell (recomendado) ou Prompt de Comando

## Instalação (sem Docker)

No PowerShell, na raiz do projeto:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
```

Dependências de desenvolvimento (testes da API):

```powershell
pip install -e .[dev]
```

## Como rodar localmente no Windows

### 1) Subir PostgreSQL

A API usa PostgreSQL por padrão. Você pode subir o banco com Docker Compose:

```powershell
docker compose -f infra/docker-compose.yml up -d postgres
```

Banco disponível em:
- `postgresql+psycopg://postgres:postgres@127.0.0.1:5432/crud_app`

### 2) Subir API FastAPI

Em um terminal:

```powershell
.\.venv\Scripts\Activate.ps1
.\scripts\windows\start-api.ps1
```

Alternativa via CMD:

```bat
.\.venv\Scripts\activate.bat
scripts\windows\start-api.bat
```

API disponível em:
- http://127.0.0.1:8000/docs

### 3) Subir Streamlit

Em outro terminal:

```powershell
.\.venv\Scripts\Activate.ps1
.\scripts\windows\start-app.ps1
```

Alternativa via CMD:

```bat
.\.venv\Scripts\activate.bat
scripts\windows\start-app.bat
```

App disponível em:
- http://127.0.0.1:8501

## Banco de dados padrão

A aplicação está configurada para usar PostgreSQL por padrão:

- `postgresql+psycopg://postgres:postgres@127.0.0.1:5432/crud_app`

Se quiser usar outro banco PostgreSQL, defina a variável de ambiente `DATABASE_URL` antes de iniciar a API.
Para testes automatizados da API, você também pode definir `TEST_DATABASE_URL`.

## Analytics (dbt + DuckDB)

Com o ambiente ativo:

```powershell
cd analytics
dbt deps
dbt run
dbt test
```

## Modelo de dados inicial

Entidades CRUD iniciais:
- `users(id, email, name, created_at)`
- `products(id, sku, name, price, created_at)`
- `orders(id, user_id, product_id, quantity, created_at)`

## Rotas principais

- `GET/POST/PATCH/DELETE /v1/users`
- `GET/POST /v1/products`
- `GET/POST /v1/orders`
- `GET /health`
