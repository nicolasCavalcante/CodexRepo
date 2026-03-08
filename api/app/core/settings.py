from __future__ import annotations

import os
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
ENV_PATH = REPO_ROOT / ".env"


def load_env_file(path: Path = ENV_PATH) -> None:
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        current = line.strip()
        if not current or current.startswith("#") or "=" not in current:
            continue

        key, value = current.split("=", 1)
        key = key.strip()
        value = value.strip()

        if value.startswith('"') and value.endswith('"') and len(value) >= 2:
            value = value[1:-1]
        elif value.startswith("'") and value.endswith("'") and len(value) >= 2:
            value = value[1:-1]

        if key:
            os.environ.setdefault(key, value)


def get_env(name: str, default: str | None = None, required: bool = False) -> str:
    value = os.getenv(name, default)
    if required and (value is None or value.strip() == ""):
        raise RuntimeError(f"Variavel de ambiente obrigatoria ausente: {name}")
    if value is None:
        return ""
    return value


load_env_file()
