# Analytics (dbt + DuckDB)

## Organização

- `models/staging`: camada de preparação (views).
- `models/marts`: camada de consumo analítico (tabelas).
- `models/schema.yml`: testes de qualidade.

## Execução

Na pasta `analytics/`:

```bash
dbt deps
dbt run
dbt test
```

## Modelo atual

- `stg_orders`: normaliza dados de `main.orders`.
- `fct_order_items`: tabela fato básica com `total_items`.

## Evolução sugerida

- Adicionar dimensões (`dim_users`, `dim_products`).
- Criar métricas agregadas (faturamento, ticket médio).
- Expandir testes de integridade referencial.
