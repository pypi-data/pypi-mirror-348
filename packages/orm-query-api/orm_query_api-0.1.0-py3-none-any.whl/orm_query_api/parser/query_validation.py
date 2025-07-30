"""
This module provides functions to validate query options for a RESTful application using SQLAlchemy and custom serializers.

Functions:
    validate_query_options(qo: ActionTree, serializer: Type[BaseSerializer]):
        Validates the select and filter options in the ActionTree against the provided serializer.

    _validate_select(action: ActionTree, serializer: Type[BaseSerializer]):
        Validates the select fields in the ActionTree against the provided serializer.

    _validate_filter(action: ActionTree, serializer: Type[BaseSerializer]):
        Validates the filter criteria in the ActionTree against the provided serializer.

Exceptions:
    ValidationException: Raised when validation of the query options fails.
"""
import operator
from typing import Type

from sqlalchemy.orm import InstrumentedAttribute

from ..exceptions.error import ValidationException
from .query_parser import ActionTree, NestedField
from ..services.serialization import BaseSerializer, get_serializer, SerializerField


def validate_query_options(qo: ActionTree, serializer: Type[BaseSerializer]):
    """
        Validates the query options in an ActionTree against the provided serializer.

        Args:
            qo (ActionTree): The query options to validate.
            serializer (Type[BaseSerializer]): The serializer class to validate against.

        Raises:
            ValidationException: If any validation checks fail.
    """
    if qo.select is not None:
        _validate_select(qo, serializer)
    if qo.filters is not None:
        _validate_filter(qo, serializer)


def _validate_select(action: ActionTree, serializer: Type[BaseSerializer]):
    """
        Validates the select fields in an ActionTree against the provided serializer.

        Args:
            action (ActionTree): The select action tree to validate.
            serializer (Type[BaseSerializer]): The serializer class to validate against.

        Raises:
            ValidationException: If any select validation checks fail.
    """
    field_aliases = {f.alias: f for f in serializer.fields}
    if isinstance(action.select, list):
        for field in action.select:
            if field.startswith("!"):
                excluded_field = field[1:]
                if excluded_field not in field_aliases.keys():
                    raise ValidationException(
                        f"Unknown field to exclude: {excluded_field}"
                    )

            elif field == "*":
                continue
            else:
                if field not in field_aliases.keys():
                    raise ValidationException(f"Unknown field to select: {field}")
    model_inspection = serializer.get_model_inspection()
    for relation_name, rel_action in action.relations.items():
        if relation_name not in field_aliases.keys():
            raise ValidationException(f"Unknown relation passed: {relation_name}")
        field_def = field_aliases[relation_name]
        relation_ = model_inspection.relationships[field_def.field]
        relation_type = relation_.entity
        relation_serializer = get_serializer(relation_type.entity)
        _validate_select(rel_action, relation_serializer)


def _validate_filter(action: ActionTree, serializer: Type[BaseSerializer]):
    """
        Validates the filter criteria in an ActionTree against the provided serializer.

        Args:
            action (ActionTree): The filter action tree to validate.
            serializer (Type[BaseSerializer]): The serializer class to validate against.

        Raises:
            ValidationException: If any filter validation checks fail.
    """
    model_inspect = serializer.get_model_inspection()
    field_aliases = {f.alias: f for f in serializer.fields}

    for flt_item in action.filters:
        if isinstance(flt_item.field, NestedField):
            if flt_item.field.fields[0] not in field_aliases.keys():
                raise ValidationException(
                    f"Unknown field passed: {flt_item.field.fields[0]}"
                )
            if flt_item.field.fields[0] not in model_inspect.relationships:
                raise ValidationException(
                    f"Unknown relation passed: {flt_item.field.fields[0]}"
                )
        else:
            if flt_item.field not in field_aliases.keys():
                raise ValidationException(f"Unknown field passed: {flt_item.field}")
        if flt_item.operator in [
            operator.ge,
            operator.gt,
            operator.lt,
            operator.le,
        ] and isinstance(flt_item.value, str):
            raise ValidationException(
                f"Filter value in this scope cannot be string: {flt_item.operator} and {flt_item.value}"
            )
        if flt_item.operator in [
            InstrumentedAttribute.like,
            InstrumentedAttribute.ilike,
        ] and not isinstance(flt_item.value, str):
            raise ValidationException(
                f"Value must be string: {flt_item.value} for operator: {flt_item.operator}"
            )

        if isinstance(flt_item.value, list) and operator.eq == flt_item.operator:
            raise ValidationException(
                "Equal operator doesn`t support list of values, please provide single value"
            )
        if (
                isinstance(flt_item.value, list)
                and InstrumentedAttribute.in_ == flt_item.operator
        ):
            _types = set(type(item) for item in flt_item.value)
            if len(_types) > 1:
                raise ValidationException("List must contains single type of value")
    for relation_name, rel_action in action.relations.items():
        if relation_name not in field_aliases.keys():
            raise ValidationException(f"Unknown relation passed: {relation_name}")
        field_def = field_aliases[relation_name]
        relation_ = model_inspect.relationships[field_def.field]
        relation_type = relation_.entity
        relation_serializer = get_serializer(relation_type.entity)
        _validate_filter(rel_action, relation_serializer)
