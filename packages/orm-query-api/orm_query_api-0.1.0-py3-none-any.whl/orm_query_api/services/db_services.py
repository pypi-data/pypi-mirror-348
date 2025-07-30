from typing import Optional
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()

_engine = None
_SessionLocal = None


def init_db(
        db_path: str = "ToDoDB.db",
        echo: bool = True,
        auto_create: bool = True
):
    """
    Initialize the SQLite database.

    Args:
        db_path (str): Path or name of the SQLite database file.
        echo (bool): Whether to echo SQL commands.
        auto_create (bool): Whether to create the DB file/tables if not exists.
    """
    global _engine, _SessionLocal

    db_uri = f"sqlite:///{db_path}"
    _engine = create_engine(
        db_uri,
        connect_args={"check_same_thread": False},
        echo=echo
    )
    _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

    if auto_create and not database_exists(_engine.url):
        create_database(_engine.url)
        Base.metadata.create_all(bind=_engine)


def get_session():
    if _SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _SessionLocal()
