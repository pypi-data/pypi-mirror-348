import os
import pytest
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from orm_query_api.services.db_services import init_db, get_session, Base, _engine

TEST_DB_PATH = "test_temp.db"


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    init_db(db_path=":memory:", echo=False, auto_create=True)
    yield
    try:
        session = get_session()
        session.close()
    except Exception:
        pass

    if _engine:
        _engine.dispose()

    import gc
    gc.collect()
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


def test_get_session_returns_valid_session():
    session = get_session()
    assert isinstance(session, Session)
    session.close()


def test_db_initialized_tables():
    inspector = inspect(Base.metadata)
    tables = inspector.sorted_tables
    assert isinstance(tables, list)
