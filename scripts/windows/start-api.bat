@echo off
set DATABASE_URL=sqlite:///./crud_app.db
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
