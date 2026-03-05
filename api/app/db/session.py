from collections.abc import Generator
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

load_dotenv(Path(__file__).resolve().parents[3] / '.env')

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg://postgres:postgres@localhost:5432/crud_app')

connect_args = {'check_same_thread': False} if DATABASE_URL.startswith('sqlite') else {}
engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
