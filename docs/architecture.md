# Visão geral da arquitetura

A aplicação segue uma estrutura em módulos:

- `api/`: camada transacional (CRUD)
- `app/`: interface para operação manual
- `analytics/`: modelagem analítica com dbt
- `orchestration/`: automação das etapas analíticas

## Fluxo de dados

1. Usuário interage no Streamlit.
2. Streamlit chama endpoints da API.
3. API persiste entidades no banco transacional.
4. dbt transforma tabelas transacionais em modelos analíticos.
5. Dagster orquestra `dbt run` e `dbt test`.

## Decisões de design

- Camada `services` para reutilização de lógica CRUD.
- `schemas` para validação de entrada/saída.
- Setup simples para onboarding (SQLite por padrão).
