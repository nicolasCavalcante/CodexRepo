@echo off
set DATABASE_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:5432/crud_app
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
