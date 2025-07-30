import pytest
from pydantic import BaseModel
from sqlalchemy import Column, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declarative_base

Base = declarative_base()


from orm_query_api.services.serialization import BaseSerializer, SerializerField, get_serializer, get_prop_serializer


class MyModel(Base):
    __tablename__ = "mymodel"
    id: Mapped[int] = Column(Integer, primary_key=True)


class MyModelPydantic(BaseModel):
    pass


class MyModelSerializer(BaseSerializer):
    model = MyModel
    fields = [SerializerField("id", alias="identifier")]


def test_SerializerField_init():
    field = SerializerField("name", alias="full_name")
    assert field.field == "name"
    assert field.alias == "full_name"


def test_SerializerField_default_alias():
    field = SerializerField("name", None)
    assert field.field == "name"
    assert field.alias == "name"


def test_BaseSerializer_get_model_inspection():
    inspection = MyModelSerializer.get_model_inspection()
    assert inspection is not None


def test_BaseSerializer_get_db_field():
    db_field = MyModelSerializer.get_db_field("id")
    assert db_field is not None


def test_BaseSerializer_get_serializer_field():
    serializer_field = MyModelSerializer.get_serializer_field("identifier")
    assert serializer_field is not None


def test_get_serializer():
    serializer_class = get_serializer(MyModel)
    assert serializer_class == MyModelSerializer


def test_get_serializer_missing():
    serializer_class = get_serializer(type("UnknownModel", (), {}))
    assert serializer_class is None


def test_get_prop_serializer_exception():
    with pytest.raises(Exception):
        get_prop_serializer(MyModel, "unknown_relation")
