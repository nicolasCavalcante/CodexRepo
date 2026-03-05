from collections.abc import Generator
from pathlib import Path
import os
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

API_DIR = Path(__file__).resolve().parents[1]
if str(API_DIR) not in sys.path:
    sys.path.insert(0, str(API_DIR))

from app.db.session import Base, get_db


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    test_database_url = os.getenv(
        "TEST_DATABASE_URL", "postgresql+psycopg://postgres:postgres@127.0.0.1:5432/crud_app"
    )
    os.environ["DATABASE_URL"] = test_database_url

    try:
        from app.main import app
    except SQLAlchemyError as exc:
        pytest.skip(f"Postgres indisponível para testes: {exc}")

    engine = create_engine(test_database_url, pool_pre_ping=True)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    try:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError as exc:
        pytest.skip(f"Postgres indisponível para testes: {exc}")

    def override_get_db() -> Generator[Session, None, None]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
