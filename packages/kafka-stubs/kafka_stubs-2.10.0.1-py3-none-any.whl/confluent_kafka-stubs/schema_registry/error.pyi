from typing import Final

try:  # noqa: SIM105
    from fastavro.schema import SchemaParseException, UnknownType
except ImportError:
    pass

__all__ = ['OAuthTokenError', 'SchemaParseException', 'SchemaRegistryError', 'UnknownType']

class SchemaRegistryError(Exception):
    UNKNOWN: Final[int] = ...
    http_status_code: int
    error_code: int
    error_message: str

    def __init__(self, http_status_code: int, error_code: int, error_message: str) -> None: ...

class OAuthTokenError(Exception):
    message: str
    status_code: int | None
    response_text: str | None

    def __init__(self, message: str, status_code: int | None = None, response_text: str | None = None) -> None: ...
