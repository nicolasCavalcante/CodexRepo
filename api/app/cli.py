from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

from app.core.settings import get_env
from app.db.admin import DatabaseAdminError, create_schema, ensure_database


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="crud-start",
        description="Inicia API FastAPI e app Streamlit com um único comando.",
    )
    parser.add_argument("--api-host", default="127.0.0.1")
    parser.add_argument("--api-port", type=int, default=8000)
    parser.add_argument("--app-port", type=int, default=8501)
    parser.add_argument(
        "--database-url",
        default=None,
        help="Sobrescreve DATABASE_URL para esta execução.",
    )
    parser.add_argument(
        "--bootstrap-db",
        action="store_true",
        help="Cria o database (PostgreSQL) e as tabelas antes de iniciar os processos.",
    )
    parser.add_argument(
        "--reload", action="store_true", help="Habilita reload no uvicorn"
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    streamlit_app = repo_root / "app" / "streamlit_app.py"
    database_url = args.database_url or get_env("DATABASE_URL", required=True)

    env = os.environ.copy()
    env["DATABASE_URL"] = database_url
    env["API_URL"] = f"http://{args.api_host}:{args.api_port}/v1"

    if args.bootstrap_db:
        try:
            created = ensure_database(database_url)
            create_schema(database_url)
        except DatabaseAdminError as exc:
            print(str(exc))
            return 1
        if created:
            print("Database criado e schema inicializado.")
        else:
            print("Database existente e schema inicializado.")

    uvicorn_cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "app.main:app",
        "--host",
        args.api_host,
        "--port",
        str(args.api_port),
    ]
    if args.reload:
        uvicorn_cmd.append("--reload")

    streamlit_cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(streamlit_app),
        "--server.address",
        args.api_host,
        "--server.port",
        str(args.app_port),
    ]

    api_proc = subprocess.Popen(uvicorn_cmd, env=env, cwd=repo_root)
    app_proc = subprocess.Popen(streamlit_cmd, env=env, cwd=repo_root)

    print(f"API: http://{args.api_host}:{args.api_port}/docs")
    print(f"Streamlit: http://{args.api_host}:{args.app_port}")

    try:
        while True:
            api_code = api_proc.poll()
            app_code = app_proc.poll()
            if api_code is not None or app_code is not None:
                return (
                    api_code
                    if api_code is not None
                    else app_code
                    if app_code is not None
                    else 0
                )
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        for proc in (api_proc, app_proc):
            if proc.poll() is None:
                proc.terminate()
        for proc in (api_proc, app_proc):
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
