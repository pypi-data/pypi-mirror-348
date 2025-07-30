"""Thrads SDK for accessing the Thrads ad platform."""

from .client import ThradsClient
from .exceptions import ThradsError, AuthenticationError, APIError
from .models.ad import Ad

__version__ = "0.1.0"
