import pytest

from app.cli_db import main
from app.db.admin import DatabaseAdminError, DatabaseStatus


def test_bootstrap_executes_database_and_schema(monkeypatch, capsys):
    calls: list[str] = []

    def fake_ensure_database(database_url: str) -> bool:
        calls.append(f"ensure:{database_url}")
        return True

    def fake_create_schema(database_url: str) -> None:
        calls.append(f"schema:{database_url}")

    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@127.0.0.1:5432/test_cli")
    monkeypatch.setattr("app.cli_db.ensure_database", fake_ensure_database)
    monkeypatch.setattr("app.cli_db.create_schema", fake_create_schema)
    monkeypatch.setattr("sys.argv", ["crud-db", "bootstrap"])

    assert main() == 0
    assert calls == [
        "ensure:postgresql+psycopg://postgres:postgres@127.0.0.1:5432/test_cli",
        "schema:postgresql+psycopg://postgres:postgres@127.0.0.1:5432/test_cli",
    ]
    assert "Database criado e schema inicializado." in capsys.readouterr().out


def test_status_returns_error_code_when_connection_fails(monkeypatch, capsys):
    def fake_get_status(database_url: str) -> DatabaseStatus:
        return DatabaseStatus(database_url=database_url, connected=False, table_names=[])

    monkeypatch.setattr("app.cli_db.get_status", fake_get_status)
    monkeypatch.setattr("sys.argv", ["crud-db", "--database-url", "postgresql+psycopg://x/y", "status"])

    assert main() == 1
    output = capsys.readouterr().out
    assert "DATABASE_URL: postgresql+psycopg://x/y" in output
    assert "Conexao: falhou" in output


def test_resolve_database_url_prefers_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@127.0.0.1:5432/from_env")

    from app.db.admin import resolve_database_url

    assert resolve_database_url() == "postgresql+psycopg://postgres:postgres@127.0.0.1:5432/from_env"

    monkeypatch.delenv("DATABASE_URL")
    with pytest.raises(DatabaseAdminError):
        resolve_database_url()
