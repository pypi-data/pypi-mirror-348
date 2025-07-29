class MindControlError(Exception):
    """Base class for exceptions in the MindControl API."""

    pass


class InvalidVersion(MindControlError, ValueError):
    """Exception raised when an invalid combination of version parameters is provided."""

    def __init__(self, message: str):
        super().__init__(message)


class MissingOfflineCollection(MindControlError, ValueError):
    """Exception raised when a collection_json is missing while setting offline mode."""

    def __init__(self):
        super().__init__("The collection_json should be set when in offline mode.")
