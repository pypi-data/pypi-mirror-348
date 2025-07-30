from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import NoResultFound

from orm_query_api.routes import generate_crud_router
from sqlalchemy.orm import declarative_base

Base = declarative_base()

from orm_query_api.utils.auto_gen import create_schema_and_serializer


class DummyModel(Base):
    __tablename__ = "dummy"
    id = Column(Integer, primary_key=True)
    name = Column(String)


model_pydantic, model_serialize = create_schema_and_serializer(DummyModel)


@pytest.fixture
def mock_session():
    session = MagicMock()
    session.query.return_value.filter.return_value.one.side_effect = NoResultFound()
    session.query.return_value.filter.return_value.first.return_value = None
    session.query.return_value.filter.return_value.exists = False
    session.scalar.return_value = {"results": ["item1", "item2"]}
    session.query.return_value.exists.return_value.scalar.return_value = True
    return session


@pytest.fixture
def app(mock_session):
    with patch("orm_query_api.routes.get_session", return_value=mock_session), \
            patch("orm_query_api.routes.parse_query", return_value={"parsed": True}), \
            patch("orm_query_api.routes.validate_query_options") as mock_validate, \
            patch("orm_query_api.routes.get_all", return_value="some_query_result"):
        router = generate_crud_router(DummyModel, model_serialize, "dummy", pydantic_model=model_pydantic)
        from fastapi import FastAPI
        app = FastAPI()
        app.include_router(router)
        yield app


@pytest.fixture
def client(app):
    return TestClient(app)


def test_list_items(client, mock_session):
    response = client.get("/dummy/")
    assert response.status_code == 200
    assert response.json() == {"results": ["item1", "item2"]}


def test_get_one_not_found(client):
    response = client.get("/dummy/123")
    assert response.status_code == 404


def test_create_item(client, mock_session):
    data = {"name": "test"}
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None
    response = client.post("/dummy/", json=data)
    assert response.status_code == 200
    assert response.json()["name"] == "test"


def test_update_item_success(client, mock_session):
    obj = DummyModel(id=1, name="old")
    mock_session.query.return_value.filter.return_value.first.return_value = obj
    mock_session.merge.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None
    response = client.put("/dummy/1", json={"name": "updated"})
    assert response.status_code == 200
    assert response.json()["name"] == "updated"


def test_update_item_not_found(client, mock_session):
    mock_session.query.return_value.exists.return_value.scalar.return_value = None
    response = client.put("/dummy/1", json={"name": "updated"})
    assert response.status_code == 404


def test_partial_update_item_not_found(client, mock_session):
    mock_session.query.return_value.filter.return_value.first.return_value = None
    response = client.patch("/dummy/1", json={"name": "patched"})
    assert response.status_code == 404


def test_partial_update_item_success(client, mock_session):
    obj = DummyModel(id=1, name="old")
    mock_session.query.return_value.filter.return_value.first.return_value = obj
    mock_session.commit.return_value = None
    response = client.patch("/dummy/1", json={"name": "patched"})
    assert response.status_code == 200
    assert response.json()["name"] == "patched"


def test_delete_item_not_found(client, mock_session):
    mock_session.query.return_value.filter.return_value.one.side_effect = NoResultFound()
    response = client.delete("/dummy/1")
    assert response.status_code == 404


def test_delete_item_success(client, mock_session):
    obj = DummyModel(id=1)
    mock_session.query.return_value.filter.return_value.one.side_effect = None
    mock_session.query.return_value.filter.return_value.one.return_value = obj
    mock_session.delete.return_value = None
    mock_session.commit.return_value = None
    response = client.delete("/dummy/1")
    assert response.status_code == 204
