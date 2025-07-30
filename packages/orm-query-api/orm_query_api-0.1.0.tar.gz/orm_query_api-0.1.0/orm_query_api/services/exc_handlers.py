"""
Exception handlers for custom ORM Query API errors.

This module defines Starlette-compatible exception handlers for validation
and SQL generation errors. These can be registered with a FastAPI app to
ensure consistent error responses across the API.

Exports:
    - validation_exception_handler
    - sql_exception_handler
    - register_exception_handlers
"""

from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi import FastAPI

from ..exceptions.error import ValidationException, SQLGenerationException

__all__ = [
    "validation_exception_handler",
    "sql_exception_handler",
    "register_exception_handlers"
]


def validation_exception_handler(_request: Request, exc: ValidationException) -> JSONResponse:
    """
    Handle validation errors raised during request processing.

    Args:
        _request (Request): Incoming HTTP request.
        exc (ValidationException): The raised validation exception.

    Returns:
        JSONResponse: A 422 error response with details.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": {"type": "ValidationException", "message": str(exc)}},
    )


def sql_exception_handler(_request: Request, exc: SQLGenerationException) -> JSONResponse:
    """
    Handle SQL generation errors during query processing.

    Args:
        _request (Request): Incoming HTTP request.
        exc (SQLGenerationException): The raised SQL generation exception.

    Returns:
        JSONResponse: A 500 error response with details.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"type": "SQLGenerationException", "message": str(exc)}},
    )


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register custom exception handlers with a FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    app.add_exception_handler(ValidationException, validation_exception_handler)
    app.add_exception_handler(SQLGenerationException, sql_exception_handler)
