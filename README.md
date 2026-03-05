# Plataforma CRUD Completa (Python + FastAPI + Postgres + dbt + DuckDB + Dagster + Streamlit)

## Estrutura

- `api/`: API transacional CRUD com FastAPI + SQLAlchemy.
- `app/`: Front-end Streamlit para operar CRUD.
- `analytics/`: projeto dbt com modelos em DuckDB.
- `orchestration/`: assets Dagster para executar `dbt run` e `dbt test`.
- `infra/`: `docker-compose` (opcional) para quem quiser subir stack via containers.
- `scripts/windows/`: scripts PowerShell para rodar API e Streamlit localmente no Windows.

## Configuração de variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto a partir do modelo:

```bash
cp .env.example .env
```

> No Windows (PowerShell):

```powershell
Copy-Item .env.example .env
```

A API, o Streamlit e a orquestração carregam variáveis diretamente do arquivo `.env`.

## Rodando localmente **sem Docker** (Windows)

### 1) Instale dependências do sistema

- Python 3.10+
- PostgreSQL 16+ (ou compatível)

### 2) Crie o banco Postgres local

Com o `psql`, execute:

```sql
CREATE DATABASE crud_app;
```

Depois, ajuste `POSTGRES_*` e `DATABASE_URL` no `.env` se necessário.

### 3) Suba a API (terminal 1)

```powershell
.\scripts\windows\run_api.ps1
```

API disponível em: `http://localhost:8000/docs`

### 4) Suba o Streamlit (terminal 2)

```powershell
.\scripts\windows\run_streamlit.ps1
```

Streamlit disponível em: `http://localhost:8501`

## Execução manual (sem scripts)

### API

```bash
cd api
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Streamlit

```bash
cd app
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py --server.port 8501
```

## (Opcional) Como rodar com Docker Compose

```bash
cd infra
docker compose up --build
```

Serviços:
- API: http://localhost:8000/docs
- Streamlit: http://localhost:8501
- Postgres: localhost:5432

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

## Roadmap técnico por issues

1. **ISSUE-01 — Setup e observabilidade base**
   - Logging estruturado (JSON).
   - Healthchecks em todos serviços.
   - Métricas básicas com Prometheus.

2. **ISSUE-02 — Segurança da API**
   - JWT + refresh token.
   - RBAC por perfil (admin, analyst, operator).
   - Rate limiting nas rotas públicas.

3. **ISSUE-03 — CRUD avançado**
   - Paginação, busca full-text e ordenação composta.
   - Soft delete e trilha de auditoria.

4. **ISSUE-04 — dbt analytics robusto**
   - Modelos `dim_users`, `dim_products`, `fct_orders`.
   - `sources.yml` com testes de freshness.
   - Exposures para dashboards.

5. **ISSUE-05 — Dagster produção**
   - Schedules diários + sensors por evento.
   - Retry policies e alertas Slack.

6. **ISSUE-06 — Streamlit produto**
   - Edição e exclusão no front.
   - Dashboard de receita e ticket médio.
   - Controle de sessão por usuário.

7. **ISSUE-07 — CI/CD**
   - Pipeline com lint, testes de API, `dbt test`.
   - Build e deploy automatizados.

8. **ISSUE-08 — Qualidade de dados**
   - Great Expectations (opcional) ou validações customizadas.
   - Contratos de schema entre API e analytics.
