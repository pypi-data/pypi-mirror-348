"""
This module defines custom exception classes for handling errors in a RESTful application.

Classes:
    RestException (Exception): A base class for exceptions in the RESTful application.
    ValidationException (RestException): Raised when validation of input data fails.
    SQLGenerationException (RestException): Raised when there is an error in SQL generation.

Usage:
    These custom exceptions can be used to provide more specific error handling in the application.

Example:
    try:
        # Some code that might raise an exception
    except ValidationException as e:
        # Handle validation error
    except SQLGenerationException as e:
        # Handle SQL generation error
    except RestException as e:
        # Handle general REST-related error
"""


class RestException(Exception):
    """Base class for exceptions in the RESTful application."""
    pass


class ValidationException(RestException):
    """Exception raised for errors in the validation of input data."""
    pass


class SQLGenerationException(RestException):
    """Exception raised for errors during SQL generation."""
    pass
