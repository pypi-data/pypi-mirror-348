"""
Клиент платежного API WATA.

Модульный асинхронный клиент для взаимодействия с платежным API WATA.
"""

from .client import WataClient
from .manager import WataClientManager
from .logging_config import WataLoggingConfig, enable_wata_debug_logging
from .exceptions import (
    ApiAuthError,
    ApiConnectionError,
    ApiError,
    ApiForbiddenError,
    ApiParsingError,
    ApiResourceNotFoundError,
    ApiServerError,
    ApiServiceUnavailableError,
    ApiTimeoutError,
    ApiValidationError,
)

__all__ = [
    "WataClient",
    "WataClientManager",
    "WataLoggingConfig",
    "enable_wata_debug_logging",
    "ApiError",
    "ApiConnectionError",
    "ApiTimeoutError",
    "ApiAuthError",
    "ApiForbiddenError",
    "ApiResourceNotFoundError",
    "ApiValidationError",
    "ApiServerError",
    "ApiServiceUnavailableError",
    "ApiParsingError",
]

__version__ = "1.0.0"
