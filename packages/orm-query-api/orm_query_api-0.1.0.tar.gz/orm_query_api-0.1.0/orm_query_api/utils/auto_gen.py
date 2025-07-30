from typing import Type, List
from pydantic import create_model
from sqlalchemy.orm import DeclarativeMeta
from ..services.serialization import BaseSerializer, SerializerField


def sqlalchemy_to_pydantic(
    model: Type[DeclarativeMeta],
    exclude_fields: List[str] = None,
):
    """
    Auto-generate a Pydantic model from a SQLAlchemy model.

    Args:
        model: SQLAlchemy declarative model class
        exclude_fields: list of field names to exclude

    Returns:
        Pydantic model class
    """
    exclude_fields = exclude_fields or []

    annotations = {}
    defaults = {}

    for col in model.__table__.columns:
        if col.name in exclude_fields:
            continue
        # Use the column type hint or fallback to `str` (simplified)
        annotations[col.name] = (col.type.python_type if hasattr(col.type, 'python_type') else str)
        if not col.nullable and not col.primary_key:
            defaults[col.name] = ...

    # Create a Pydantic model dynamically
    pydantic_model = create_model(
        f"{model.__name__}Pydantic",
        __base__=None,
        **{name: (typ, defaults.get(name, None)) for name, typ in annotations.items()}
    )
    return pydantic_model


def create_default_serializer(model: Type[DeclarativeMeta]):
    """
    Auto-generate a simple serializer class from a SQLAlchemy model.

    It will include all columns as SerializerFields with the same name.
    """
    fields = [SerializerField(col.name, col.name) for col in model.__table__.columns]

    # Dynamically create a serializer class
    serializer_cls = type(
        f"{model.__name__}Serializer",
        (BaseSerializer,),
        {
            "model": model,
            "fields": fields,
        }
    )
    return serializer_cls


def create_schema_and_serializer(model: Type[DeclarativeMeta]):
    """
    Factory function to create both schema and serializer for registration.
    """
    Schema = sqlalchemy_to_pydantic(model)
    Serializer = create_default_serializer(model)
    return Schema, Serializer
