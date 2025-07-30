class ThradsError(Exception):
    """Base exception for Thrads SDK errors."""
    pass


class AuthenticationError(ThradsError):
    """Raised when authentication fails."""
    pass


class APIError(ThradsError):
    """Raised when API returns an error."""
    pass
