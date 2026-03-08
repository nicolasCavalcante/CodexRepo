from collections.abc import Generator
from pathlib import Path

import psycopg
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

CONFIG_PATH = Path("config.yaml")


def load_postgres_config() -> dict[str, str | int]:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            "Arquivo config.yaml nao encontrado. Use config.yaml.example como template."
        )

    raw = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}
    postgres_cfg = raw.get("postgres", {})

    required_keys = ["port", "admin_user", "admin_password", "db_name"]
    missing = [key for key in required_keys if key not in postgres_cfg]
    if missing:
        raise ValueError(
            f"Chaves obrigatorias ausentes em postgres: {', '.join(missing)}"
        )

    return {
        "port": int(postgres_cfg["port"]),
        "admin_user": str(postgres_cfg["admin_user"]),
        "admin_password": str(postgres_cfg["admin_password"]),
        "db_name": str(postgres_cfg["db_name"]),
    }


def load_database_url() -> str:
    cfg = load_postgres_config()
    return (
        "postgresql+psycopg://"
        f"{cfg['admin_user']}:{cfg['admin_password']}@127.0.0.1:{cfg['port']}/{cfg['db_name']}"
    )


def _admin_dsn(cfg: dict[str, str | int]) -> str:
    return (
        f"host=127.0.0.1 port={cfg['port']} dbname=postgres "
        f"user={cfg['admin_user']} password={cfg['admin_password']}"
    )


def _target_dsn(cfg: dict[str, str | int]) -> str:
    return (
        f"host=127.0.0.1 port={cfg['port']} dbname={cfg['db_name']} "
        f"user={cfg['admin_user']} password={cfg['admin_password']}"
    )


def ensure_server_available(cfg: dict[str, str | int]) -> None:
    try:
        with psycopg.connect(_admin_dsn(cfg)):
            return
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            "Servidor PostgreSQL indisponivel em "
            f"127.0.0.1:{cfg['port']} com usuario '{cfg['admin_user']}'.\n"
            "Como resolver:\n"
            "1) Inicie o servidor PostgreSQL.\n"
            "2) Valide host/porta/usuario/senha no config.yaml.\n"
            "3) Teste conexao: psql -h 127.0.0.1 -p "
            f"{cfg['port']} -U {cfg['admin_user']} -d postgres"
        ) from exc


def ensure_database_created(cfg: dict[str, str | int]) -> None:
    try:
        with psycopg.connect(_admin_dsn(cfg), autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (cfg["db_name"],))
                exists = cur.fetchone()
                if exists:
                    return
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            "Falha ao consultar catalogo de bancos no PostgreSQL.\n"
            "Verifique permissoes do usuario admin configurado no config.yaml."
        ) from exc

    raise RuntimeError(
        f"Banco '{cfg['db_name']}' nao existe no servidor PostgreSQL.\n"
        "Como resolver:\n"
        f"1) createdb -h 127.0.0.1 -p {cfg['port']} -U {cfg['admin_user']} {cfg['db_name']}\n"
        "ou\n"
        f"2) psql -h 127.0.0.1 -p {cfg['port']} -U {cfg['admin_user']} -d postgres "
        f"-c \"CREATE DATABASE {cfg['db_name']};\""
    )


DATABASE_URL = load_database_url()

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def ensure_database_exists() -> None:
    cfg = load_postgres_config()
    ensure_server_available(cfg)
    ensure_database_created(cfg)
    try:
        with psycopg.connect(_target_dsn(cfg)):
            return
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            f"Banco '{cfg['db_name']}' existe, mas conexao com ele falhou.\n"
            "Verifique credenciais e permissoes do usuario no config.yaml."
        ) from exc


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
