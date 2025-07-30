from orm_query_api.registry import ModelRegistry
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
import pytest

from orm_query_api.services.db_services import init_db

Base = declarative_base()


class DummyModel(Base):
    __tablename__ = "dummy"
    id = Column(Integer, primary_key=True)
    name = Column(String)


def test_model_registration():
    init_db()
    registry = ModelRegistry()
    registry.register_model(DummyModel)

    assert "DummyModel" in registry.registry
    assert "model" in registry.registry["DummyModel"]
    assert "serializer" in registry.registry["DummyModel"]
