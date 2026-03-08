# AGENTS.md

Este arquivo orienta agentes (humanos ou IA) que atuam neste repositório.

## Objetivo do projeto

Plataforma CRUD com:

- API transacional em FastAPI + SQLAlchemy (`api/`)
- App de operação em Streamlit (`app/`)
- Camada analítica com dbt + DuckDB (`analytics/`)
- Orquestração com Dagster (`orchestration/`)

## Fonte de verdade e escopo

- Não usar Docker neste projeto.
- Preferir mudanças pequenas, focadas e com impacto claro.
- Preservar separação de camadas na API: `routers -> services -> models/schemas`.
- Evitar alterações em arquivos gerados (`analytics/target/`, caches, logs).

## Ambiente e pré-requisitos

- Python `3.10.x` (obrigatório; ver `pyproject.toml`)
- Windows com PowerShell (scripts em `scripts/windows/`)
- PostgreSQL local para execução padrão da API

Setup:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
pip install -e .[dev]
```

## Execução local

API:

```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

App Streamlit:

```powershell
streamlit run app/streamlit_app.py --server.address 127.0.0.1 --server.port 8501
```

Ou comando único:

```powershell
crud-start --reload
```

## Configurações relevantes

Variáveis de ambiente principais:

- `DATABASE_URL` (padrão atual no código: `postgresql+psycopg://postgres:postgres@127.0.0.1:5432/crud_app`)
- `API_URL` (padrão do app: `http://localhost:8000/v1`)
- `ANALYTICS_DIR` (usado pelo Dagster; padrão: `../analytics`)

## Testes e validação

Antes de concluir qualquer tarefa:

```powershell
pytest api/tests -q
```

Quando houver alteração em analytics:

```powershell
cd analytics
dbt deps
dbt run
dbt test
```

## Regras de mudança para agentes

- Não reverter mudanças de terceiros sem pedido explícito.
- Não introduzir dependências novas sem necessidade clara.
- Atualizar documentação (`README.md` e/ou `docs/`) quando mudar comportamento.
- Se identificar inconsistências entre documentação e código, corrigir ambos no mesmo trabalho.

## Locais importantes

- API entrypoint: `api/app/main.py`
- Sessão de banco: `api/app/db/session.py`
- CLI de execução conjunta: `api/app/cli.py`
- App Streamlit: `app/streamlit_app.py`
- Testes da API: `api/tests/`

## Entregáveis esperados em PR

- Código funcional
- Testes passando (ou justificativa explícita se não executados)
- Documentação atualizada para qualquer mudança de uso/configuração
