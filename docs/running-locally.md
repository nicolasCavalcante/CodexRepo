# Rodando localmente

## Opção 1: dois processos separados

### API (FastAPI)

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Acesse: <http://127.0.0.1:8000/docs>

### App (Streamlit)

Em outro terminal:

```bash
streamlit run app/streamlit_app.py --server.address 127.0.0.1 --server.port 8501
```

Acesse: <http://127.0.0.1:8501>

## Opção 2: comando único

```bash
crud-start --reload
```

Esse comando sobe API e Streamlit juntos.

Para inicializar automaticamente o banco e as tabelas antes de subir os processos:

```bash
crud-start --bootstrap-db --reload
```

## Gerenciamento de banco pelo repo

```bash
crud-db bootstrap
crud-db status
```

Comandos:
- `crud-db create-db`
- `crud-db create-schema`
- `crud-db bootstrap`
- `crud-db reset-schema`
- `crud-db status`

## Banco de dados padrão

Use `DATABASE_URL` no `.env` com o valor recomendado `postgresql+psycopg://postgres:postgres@127.0.0.1:5432/crud_app`.

Na prática de desenvolvimento local, defina as variáveis no arquivo `.env` (veja `.env.example`).
