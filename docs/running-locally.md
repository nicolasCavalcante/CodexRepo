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

## Banco de dados padrão

Se `DATABASE_URL` não estiver definida, o projeto usa SQLite no arquivo `crud_app.db`.
