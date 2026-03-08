from __future__ import annotations

import argparse

from app.db.admin import (
    DatabaseAdminError,
    create_schema,
    ensure_database,
    get_status,
    reset_schema,
    resolve_database_url,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="crud-db",
        description="Cria e gerencia o database da plataforma CRUD.",
    )
    parser.add_argument(
        "--database-url",
        default=None,
        help="Sobrescreve DATABASE_URL para esta execução.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("create-db", help="Cria o database PostgreSQL caso ele não exista.")
    subparsers.add_parser("create-schema", help="Cria as tabelas da aplicação.")
    subparsers.add_parser("bootstrap", help="Cria database (se necessário) e tabelas.")
    subparsers.add_parser("reset-schema", help="Recria todas as tabelas da aplicação.")
    subparsers.add_parser("status", help="Mostra status de conexão e tabelas detectadas.")
    return parser


def _print_status(database_url: str) -> int:
    status = get_status(database_url)
    print(f"DATABASE_URL: {status.database_url}")
    if not status.connected:
        print("Conexao: falhou")
        return 1

    print("Conexao: ok")
    if status.table_names:
        print("Tabelas: " + ", ".join(status.table_names))
    else:
        print("Tabelas: nenhuma encontrada")
    return 0


def main() -> int:
    args = _build_parser().parse_args()
    database_url = resolve_database_url(args.database_url)

    try:
        if args.command == "create-db":
            created = ensure_database(database_url)
            print("Database criado." if created else "Database ja existe.")
            return 0

        if args.command == "create-schema":
            create_schema(database_url)
            print("Schema criado com sucesso.")
            return 0

        if args.command == "bootstrap":
            created = ensure_database(database_url)
            create_schema(database_url)
            if created:
                print("Database criado e schema inicializado.")
            else:
                print("Database existente e schema inicializado.")
            return 0

        if args.command == "reset-schema":
            reset_schema(database_url)
            print("Schema recriado com sucesso.")
            return 0

        if args.command == "status":
            return _print_status(database_url)
    except DatabaseAdminError as exc:
        print(str(exc))
        return 1

    print("Comando invalido.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
