# Configurações e variáveis

## Variáveis principais

- `DATABASE_URL`: string de conexão da API.
- `TEST_DATABASE_URL`: string de conexão usada nos testes da API.
- `API_URL`: endpoint base consumido pelo Streamlit.
- `ANALYTICS_DIR`: caminho do projeto dbt para Dagster.

## Arquivos de ambiente

- `.env`: valores locais usados no ambiente de desenvolvimento.
- `.env.example`: template versionado com os valores padrão do projeto.

No Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

## Valores padrão

- `DATABASE_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:5432/crud_app`
- `API_URL=http://localhost:8000/v1`
- `ANALYTICS_DIR=../analytics`

## Exemplo (Linux/macOS)

```bash
export DATABASE_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:5432/crud_app
export API_URL=http://localhost:8000/v1
export ANALYTICS_DIR=../analytics
```
