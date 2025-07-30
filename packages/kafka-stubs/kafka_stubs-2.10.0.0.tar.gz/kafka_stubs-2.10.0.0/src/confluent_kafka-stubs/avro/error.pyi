class ClientError(Exception):
    message: str
    http_code: int | None
    def __init__(self, message: str, http_code: int | None = None) -> None: ...
