"""Exception classes for IEEE 2030.5 client."""


class IEEE2030Error(Exception):
    """Base exception for IEEE 2030.5 client errors."""

    pass


class AuthenticationError(IEEE2030Error):
    """Authentication or certificate-related errors."""

    pass


class ConnectionError(IEEE2030Error):
    """Connection-related errors."""

    pass


class ResourceError(IEEE2030Error):
    """Resource-related errors, including not found or access denied."""

    pass


class ParseError(IEEE2030Error):
    """Error parsing server responses."""

    pass
