# Plataforma CRUD Completa (Python + FastAPI + dbt + DuckDB + Dagster + Streamlit)

## Estrutura

- `api/`: API transacional CRUD com FastAPI + SQLAlchemy.
- `app/`: Front-end Streamlit para operar CRUD.
- `analytics/`: projeto dbt com modelos em DuckDB.
- `orchestration/`: assets Dagster para executar `dbt run` e `dbt test`.
- `scripts/windows/`: scripts alternativos para iniciar API e app no Windows.

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

## Como rodar localmente no Windows (1 comando)

Com o ambiente virtual ativo, execute:

```powershell
crud-start --reload
```

Esse comando de CLI (registrado no `pyproject.toml`) sobe:
- API FastAPI em `http://127.0.0.1:8000/docs`
- Streamlit em `http://127.0.0.1:8501`

Parar tudo: `Ctrl + C` no terminal.

### Opções úteis da CLI

```powershell
crud-start --api-port 9000 --app-port 8601
crud-start --database-url "sqlite:///./meu_banco.db"
crud-start --help
```

## Scripts alternativos (opcional)

Se preferir manter dois terminais separados, use os scripts em `scripts/windows/`.

## Banco de dados padrão

A aplicação está configurada para usar SQLite por padrão (`crud_app.db` na raiz do projeto), eliminando a necessidade de Postgres e Docker para desenvolvimento local no Windows.

Se quiser mudar o banco, defina a variável de ambiente `DATABASE_URL` antes de iniciar a API, ou use `crud-start --database-url ...`.

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
