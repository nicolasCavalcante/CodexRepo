# Configurações e variáveis

## Variáveis principais

- `DATABASE_URL`: string de conexão da API.
- `API_URL`: endpoint base consumido pelo Streamlit.
- `ANALYTICS_DIR`: caminho do projeto dbt para Dagster.

## Valores padrão

- `DATABASE_URL=sqlite:///./crud_app.db`
- `API_URL=http://localhost:8000/v1`
- `ANALYTICS_DIR=../analytics`

## Exemplo (Linux/macOS)

```bash
export DATABASE_URL=sqlite:///./crud_app.db
export API_URL=http://localhost:8000/v1
export ANALYTICS_DIR=../analytics
```
