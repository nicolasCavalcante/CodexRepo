from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import URL, make_url
from sqlalchemy.exc import SQLAlchemyError

from app.core.settings import get_env
from app.db.session import Base


class DatabaseAdminError(RuntimeError):
    """Raised when a database administration operation fails."""


@dataclass(frozen=True)
class DatabaseStatus:
    database_url: str
    connected: bool
    table_names: list[str]


def _load_models() -> None:
    # Importing entities registers table metadata on Base.
    from app.models import entities  # noqa: F401


def resolve_database_url(database_url: str | None = None) -> str:
    if database_url:
        return database_url
    try:
        return get_env("DATABASE_URL", required=True)
    except RuntimeError as exc:
        raise DatabaseAdminError(str(exc)) from exc


def _is_postgres(url: URL) -> bool:
    return url.get_backend_name().startswith("postgresql")


def ensure_database(database_url: str) -> bool:
    """Ensure target database exists. Returns True when created, False when already existed."""

    url = make_url(database_url)
    if not _is_postgres(url):
        return False

    database_name = url.database
    if not database_name:
        raise DatabaseAdminError("A DATABASE_URL precisa informar o nome do database.")

    admin_url = url.set(database="postgres")
    engine = create_engine(admin_url, pool_pre_ping=True, isolation_level="AUTOCOMMIT")

    try:
        with engine.connect() as conn:
            exists = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :name"),
                {"name": database_name},
            ).scalar_one_or_none()
            if exists:
                return False

            quoted_name = conn.dialect.identifier_preparer.quote(database_name)
            conn.execute(text(f"CREATE DATABASE {quoted_name}"))
            return True
    except SQLAlchemyError as exc:
        raise DatabaseAdminError(f"Falha ao criar database '{database_name}': {exc}") from exc
    finally:
        engine.dispose()


def create_schema(database_url: str) -> None:
    _load_models()
    engine = create_engine(database_url, pool_pre_ping=True)
    try:
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError as exc:
        raise DatabaseAdminError(f"Falha ao criar tabelas: {exc}") from exc
    finally:
        engine.dispose()


def drop_schema(database_url: str) -> None:
    _load_models()
    engine = create_engine(database_url, pool_pre_ping=True)
    try:
        Base.metadata.drop_all(bind=engine)
    except SQLAlchemyError as exc:
        raise DatabaseAdminError(f"Falha ao remover tabelas: {exc}") from exc
    finally:
        engine.dispose()


def reset_schema(database_url: str) -> None:
    drop_schema(database_url)
    create_schema(database_url)


def get_status(database_url: str) -> DatabaseStatus:
    engine = create_engine(database_url, pool_pre_ping=True)
    try:
        with engine.connect():
            inspector = inspect(engine)
            table_names = sorted(inspector.get_table_names())
            return DatabaseStatus(database_url=database_url, connected=True, table_names=table_names)
    except SQLAlchemyError:
        return DatabaseStatus(database_url=database_url, connected=False, table_names=[])
    finally:
        engine.dispose()
