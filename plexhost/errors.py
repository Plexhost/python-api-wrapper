class WrapperException(Exception):
    """Base exception class for PlexHost API Wrapper

    This will catch any exception thrown from this library
    """
    pass


class ClientException(WrapperException):
    """Exception thrown when an operation in :class:`Client` fails

    """
    pass


class InvalidArgument(ClientException):
    """Exception thrown when an argument is invalid some way.

    Could be considered this library's version of ``ValueError`` and ```TypeError``
    """
    pass

class MissingArgument(ClientException):
    """Exception thrown when an argument is missing."""
    pass

class BadRequest(ClientException):
    """Exception thrown when the user makes a bad request"""
    pass


class InternalPanelError(ClientException):
    """Thrown when a exception happens server side"""
    pass


class Forbidden(ClientException):
    """Exception thrown when the entered api key is invalid
    """
    pass
