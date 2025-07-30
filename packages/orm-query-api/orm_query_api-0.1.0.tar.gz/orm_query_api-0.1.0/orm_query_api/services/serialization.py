"""
This module defines a serialization framework for SQLAlchemy models, providing classes and functions
to handle the mapping between model fields and their serialized representations.

Classes:
    SerializerField:
        Represents a field in a serializer, with support for field aliasing.

    RelationField (SerializerField):
        Represents a relationship field in a serializer.

    BaseSerializer:
        Base class for serializers, providing methods to inspect model fields and relationships.

Functions:
    get_serializer(_type) -> Type[BaseSerializer]:
        Retrieves the serializer class associated with the given model type.

    get_prop_serializer(_type, prop: str):
        Retrieves the serializer for a related model based on a relationship property.

Attributes:
    __serializers__ (dict[Any, Type[BaseSerializer]]):
        A dictionary mapping model types to their corresponding serializer classes.
"""
from typing import Any, Type

from sqlalchemy import inspect


class SerializerField:
    """
        Represents a field in a serializer.

        Attributes:
            field (str): The name of the field in the model.
            alias (str | None): An optional alias for the field. Defaults to the field name if not provided.
    """

    def __init__(self, field: str, alias: str | None, type_: type | None = None):
        self.field = field
        self.alias = alias or field
        self.type_ = type_


class RelationField(SerializerField):
    """
        Represents a relationship field in a serializer.
        Inherits from SerializerField.
    """
    ...


class BaseSerializer:
    """
        Base class for serializers, providing methods to inspect model fields and relationships.

        Attributes:
            model (Any): The SQLAlchemy model associated with the serializer.
            fields (list[SerializerField]): A list of SerializerField instances representing the model's fields.

        Methods:
            get_model_inspection():
                Inspects and returns the model's metadata.

            get_db_field(db_field: str):
                Retrieves the corresponding model field for a given database field name.

            get_serializer_field(field_alias: str):
                Retrieves the SerializerField instance for a given field alias.
    """
    model: Any
    fields: list[SerializerField]

    @classmethod
    def get_model_inspection(cls):
        """
            Inspects and returns the model's metadata.

            Returns:
                Inspector: The SQLAlchemy inspector for the model.
        """
        return inspect(cls.model)

    def __init_subclass__(cls, **kwargs):
        """
           Registers the serializer class for the associated model type.
        """
        __serializers__[cls.model] = cls

    @classmethod
    def get_db_field(cls, db_field: str):
        """
            Retrieves the corresponding model field for a given database field name.

            Args:
                db_field (str): The name of the database field.

            Returns:
                InstrumentedAttribute: The corresponding model field.

            Raises:
                Exception: If the database field is unknown.
        """
        for serializer_field in cls.fields:
            if serializer_field.field == db_field:
                return cls.model.__dict__[serializer_field.field]
        raise Exception(f"Unknown db model field {db_field}")

    @classmethod
    def get_serializer_field(cls, field_alias: str) -> SerializerField:
        """
            Retrieves the SerializerField instance for a given field alias.

            Args:
                field_alias (str): The alias of the field.

            Returns:
                SerializerField: The corresponding SerializerField instance.

            Raises:
                Exception: If the field alias is unknown.
        """
        for serializer_field in cls.fields:
            if serializer_field.alias == field_alias:
                return serializer_field
        raise Exception(f"Unknown serializer field {field_alias}")


__serializers__: dict[Any, Type[BaseSerializer]] = {}


def get_serializer(_type) -> Type[BaseSerializer]:
    """
        Retrieves the serializer class associated with the given model type.

        Args:
            _type (Any): The model type.

        Returns:
            Type[BaseSerializer]: The corresponding serializer class.
    """
    return __serializers__.get(_type, None)


def get_prop_serializer(_type, prop: str) -> Type[BaseSerializer]:
    """
        Retrieves the serializer for a related model based on a relationship property.

        Args:
            _type (Any): The model type.
            prop (str): The name of the relationship property.

        Returns:
            Type[BaseSerializer]: The serializer for the related model.
    """
    serializer = get_serializer(_type)
    _mi = serializer.get_model_inspection()
    return get_serializer(_mi.relationships[prop].entity.entity)
