class ThradsError(Exception):
    """Base exception for Thrads SDK errors."""

    def __init__(self, message, request_id=None):
        self.message = message
        self.request_id = request_id
        super().__init__(self.message)


class AuthenticationError(ThradsError):
    """Raised when authentication fails."""
    pass


class APIError(ThradsError):
    """Raised when API returns an error."""

    def __init__(self, message, status_code=None, request_id=None):
        self.status_code = status_code
        super().__init__(message, request_id)

    def __str__(self):
        if self.status_code:
            return f"{self.message} (Status: {self.status_code}, Request ID: {self.request_id})"
        return super().__str__()


class RateLimitExceeded(APIError):
    """Raised when API rate limits are exceeded."""
    pass


class InvalidParameterError(APIError):
    """Raised when invalid parameters are provided."""
    pass


class NetworkError(ThradsError):
    """Raised for network connectivity issues."""
    pass
