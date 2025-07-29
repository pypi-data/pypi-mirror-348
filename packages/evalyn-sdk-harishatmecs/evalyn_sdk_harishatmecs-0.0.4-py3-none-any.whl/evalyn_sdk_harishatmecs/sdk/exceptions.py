

class SDKException(Exception):
    """Base class for SDK-related exceptions."""
    pass


class InvalidFileFormatException(SDKException):
    """Raised when an unsupported file format is encountered."""
    pass


class MissingEnvironmentVariableException(SDKException):
    """Raised when an environment variable is missing."""
    pass
