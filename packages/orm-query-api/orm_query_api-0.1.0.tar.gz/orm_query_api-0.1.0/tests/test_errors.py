import pytest
from orm_query_api.exceptions.error import (
    RestException,
    ValidationException,
    SQLGenerationException,
)


def test_rest_exception_inheritance():
    with pytest.raises(RestException):
        raise RestException("Base REST exception")


def test_validation_exception():
    with pytest.raises(ValidationException) as exc_info:
        raise ValidationException("Validation failed")
    assert str(exc_info.value) == "Validation failed"


def test_sql_generation_exception():
    with pytest.raises(SQLGenerationException) as exc_info:
        raise SQLGenerationException("SQL generation error")
    assert str(exc_info.value) == "SQL generation error"


def test_subclassing():
    assert issubclass(ValidationException, RestException)
    assert issubclass(SQLGenerationException, RestException)
