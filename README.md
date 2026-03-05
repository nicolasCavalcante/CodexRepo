# Plataforma CRUD Completa (Python + FastAPI + Postgres + dbt + DuckDB + Dagster + Streamlit)

## Estrutura

- `api/`: API transacional CRUD com FastAPI + SQLAlchemy.
- `app/`: Front-end Streamlit para operar CRUD.
- `analytics/`: projeto dbt com modelos em DuckDB.
- `orchestration/`: assets Dagster para executar `dbt run` e `dbt test`.
- `infra/`: `docker-compose` para subir stack local.

## Como rodar localmente

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
