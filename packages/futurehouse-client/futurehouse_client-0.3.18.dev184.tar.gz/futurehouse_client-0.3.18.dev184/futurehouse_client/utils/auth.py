import asyncio
import logging
from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any, Final, Optional, ParamSpec, TypeVar, overload

import httpx
from httpx import HTTPStatusError

logger = logging.getLogger(__name__)

T = TypeVar("T")
P = ParamSpec("P")

AUTH_ERRORS_TO_RETRY_ON: Final[set[int]] = {
    httpx.codes.UNAUTHORIZED,
    httpx.codes.FORBIDDEN,
}


class AuthError(Exception):
    """Raised when authentication fails with 401/403 status."""

    def __init__(self, status_code: int, message: str, request=None, response=None):
        self.status_code = status_code
        self.request = request
        self.response = response
        super().__init__(message)


def is_auth_error(e: Exception) -> bool:
    if isinstance(e, AuthError):
        return True
    if isinstance(e, HTTPStatusError):
        return e.response.status_code in AUTH_ERRORS_TO_RETRY_ON
    return False


def get_status_code(e: Exception) -> Optional[int]:
    if isinstance(e, AuthError):
        return e.status_code
    if isinstance(e, HTTPStatusError):
        return e.response.status_code
    return None


@overload
def refresh_token_on_auth_error(
    func: Callable[P, Coroutine[Any, Any, T]],
) -> Callable[P, Coroutine[Any, Any, T]]: ...


@overload
def refresh_token_on_auth_error(
    func: None = None, *, max_retries: int = ...
) -> Callable[[Callable[P, T]], Callable[P, T]]: ...


def refresh_token_on_auth_error(func=None, max_retries=1):
    """Decorator that refreshes JWT token on 401/403 auth errors."""

    def decorator(fn):
        @wraps(fn)
        def sync_wrapper(self, *args, **kwargs):
            retries = 0
            while True:
                try:
                    return fn(self, *args, **kwargs)
                except Exception as e:
                    if is_auth_error(e) and retries < max_retries:
                        retries += 1
                        status = get_status_code(e) or "Unknown"
                        logger.info(
                            f"Received auth error {status}, "
                            f"refreshing token and retrying (attempt {retries}/{max_retries})..."
                        )
                        self.auth_jwt = self._run_auth()
                        self._clients = {}
                        continue
                    raise

        @wraps(fn)
        async def async_wrapper(self, *args, **kwargs):
            retries = 0
            while True:
                try:
                    return await fn(self, *args, **kwargs)
                except Exception as e:
                    if is_auth_error(e) and retries < max_retries:
                        retries += 1
                        status = get_status_code(e) or "Unknown"
                        logger.info(
                            f"Received auth error {status}, "
                            f"refreshing token and retrying (attempt {retries}/{max_retries})..."
                        )
                        self.auth_jwt = self._run_auth()
                        self._clients = {}
                        continue
                    raise

        if asyncio.iscoroutinefunction(fn):
            return async_wrapper
        return sync_wrapper

    if callable(func):
        return decorator(func)
    return decorator
