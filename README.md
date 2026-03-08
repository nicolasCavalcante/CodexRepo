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

## Instalação local

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

## Arquivo de ambiente (`.env`)

As variáveis de ambiente padrão do projeto estão no arquivo `.env`.
Para compartilhar o template no repositório, use `.env.example`.

Se precisar recriar o arquivo local:

```powershell
Copy-Item .env.example .env
```

## Como rodar localmente no Windows

### 1) Preparar banco PostgreSQL via CLI do projeto

A API usa PostgreSQL por padrão:

- `postgresql+psycopg://postgres:postgres@127.0.0.1:5432/crud_app`

Com o ambiente virtual ativo, você pode criar e gerenciar o banco sem sair do repo:

```powershell
crud-db bootstrap
crud-db status
```

Comandos disponíveis:
- `crud-db create-db`: cria o database se ele não existir.
- `crud-db create-schema`: cria apenas as tabelas.
- `crud-db bootstrap`: cria database (quando necessário) e tabelas.
- `crud-db reset-schema`: recria todas as tabelas.
- `crud-db status`: testa conexão e lista tabelas.

Para usar outra conexão:

```powershell
crud-db --database-url "postgresql+psycopg://postgres:postgres@127.0.0.1:5432/meu_novo_banco" bootstrap
```

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

Para subir API e Streamlit já com bootstrap do banco:

```powershell
crud-start --bootstrap-db --reload
```

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

## Documentação para iniciantes (MkDocs)

Foi adicionada uma documentação completa em `docs/`, com navegação via MkDocs.

Rodar localmente:

```bash
pip install -e .[docs]
mkdocs serve
```

Build local:

```bash
mkdocs build --strict
```

Deploy automático no GitHub Pages:

- Workflow: `.github/workflows/docs.yml`
- Trigger: push para `main`/`master` (ou execução manual)
- No GitHub, em **Settings > Pages**, selecione **Build and deployment: GitHub Actions**.
- URL publicada: `https://<seu-usuario>.github.io/<seu-repositorio>/`
