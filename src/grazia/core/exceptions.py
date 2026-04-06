class GraziaError(Exception):
    """Base exception for all errors raised by Grazia."""

    pass


class KeyNotFoundError(GraziaError):
    """Raised when a requested key does not exist in the store."""

    def __init__(self, key: str) -> None:
        self.key = key
        message = f"The given key '{key}' was not found."
        super().__init__(message)
