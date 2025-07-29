from ..error import MindControlError


class MissingKeys(MindControlError, ValueError):
    """Exception raised when wrapper adapter can't find keys."""

    def __init__(self, message: str):
        super().__init__(message)


class MissingAdapter(MindControlError, ValueError):
    """Exception raised when wrapper can't find suitable adapter."""

    def __init__(self, message: str):
        super().__init__(message)
