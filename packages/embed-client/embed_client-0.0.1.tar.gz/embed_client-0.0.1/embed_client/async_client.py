"""
Async client for Embedding Service API (OpenAPI 3.0.2)

- 100% type-annotated
- English docstrings and examples
- Ready for PyPi
"""

from typing import Any, Dict, List, Optional, Union
import aiohttp

class EmbeddingServiceError(Exception):
    """Base exception for EmbeddingServiceAsyncClient."""

class EmbeddingServiceConnectionError(EmbeddingServiceError):
    """Raised when the service is unavailable or connection fails."""

class EmbeddingServiceHTTPError(EmbeddingServiceError):
    """Raised for HTTP errors (4xx, 5xx)."""
    def __init__(self, status: int, message: str):
        super().__init__(f"HTTP {status}: {message}")
        self.status = status
        self.message = message

class EmbeddingServiceAPIError(EmbeddingServiceError):
    """Raised for errors returned by the API in the response body."""
    def __init__(self, error: Any):
        super().__init__(f"API error: {error}")
        self.error = error

class EmbeddingServiceAsyncClient:
    """
    Asynchronous client for the Embedding Service API.
    Args:
        base_url (str): Base URL of the embedding service (e.g., "http://localhost").
        port (int): Port of the embedding service (e.g., 8001).
    Raises:
        ValueError: If base_url or port is not provided.
    """
    def __init__(self, base_url: str, port: int):
        if not base_url:
            raise ValueError("base_url must be provided.")
        if port is None:
            raise ValueError("port must be provided.")
        self.base_url = base_url.rstrip("/")
        self.port = port
        self._session: Optional[aiohttp.ClientSession] = None

    def _make_url(self, path: str, base_url: Optional[str] = None, port: Optional[int] = None) -> str:
        url = (base_url or self.base_url).rstrip("/")
        port_val = port if port is not None else self.port
        return f"{url}:{port_val}{path}"

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self._session:
            await self._session.close()
            self._session = None

    async def health(self, base_url: Optional[str] = None, port: Optional[int] = None) -> Dict[str, Any]:
        """
        Check the health of the service.
        Args:
            base_url (str, optional): Override base URL.
            port (int, optional): Override port.
        Returns:
            dict: Health status and model info.
        """
        url = self._make_url("/health", base_url, port)
        try:
            async with self._session.get(url) as resp:
                await self._raise_for_status(resp)
                return await resp.json()
        except EmbeddingServiceHTTPError:
            raise
        except EmbeddingServiceConnectionError:
            raise
        except aiohttp.ClientConnectionError as e:
            raise EmbeddingServiceConnectionError(f"Connection error: {e}") from e
        except aiohttp.ClientResponseError as e:
            raise EmbeddingServiceHTTPError(e.status, e.message) from e
        except Exception as e:
            raise EmbeddingServiceError(f"Unexpected error: {e}") from e

    async def get_openapi_schema(self, base_url: Optional[str] = None, port: Optional[int] = None) -> Dict[str, Any]:
        """
        Get the OpenAPI schema of the service.
        Args:
            base_url (str, optional): Override base URL.
            port (int, optional): Override port.
        Returns:
            dict: OpenAPI schema.
        """
        url = self._make_url("/openapi.json", base_url, port)
        try:
            async with self._session.get(url) as resp:
                await self._raise_for_status(resp)
                return await resp.json()
        except EmbeddingServiceHTTPError:
            raise
        except EmbeddingServiceConnectionError:
            raise
        except aiohttp.ClientConnectionError as e:
            raise EmbeddingServiceConnectionError(f"Connection error: {e}") from e
        except aiohttp.ClientResponseError as e:
            raise EmbeddingServiceHTTPError(e.status, e.message) from e
        except Exception as e:
            raise EmbeddingServiceError(f"Unexpected error: {e}") from e

    async def get_commands(self, base_url: Optional[str] = None, port: Optional[int] = None) -> Dict[str, Any]:
        """
        Get the list of available commands.
        Args:
            base_url (str, optional): Override base URL.
            port (int, optional): Override port.
        Returns:
            dict: List of commands and their descriptions.
        """
        url = self._make_url("/api/commands", base_url, port)
        try:
            async with self._session.get(url) as resp:
                await self._raise_for_status(resp)
                return await resp.json()
        except EmbeddingServiceHTTPError:
            raise
        except EmbeddingServiceConnectionError:
            raise
        except aiohttp.ClientConnectionError as e:
            raise EmbeddingServiceConnectionError(f"Connection error: {e}") from e
        except aiohttp.ClientResponseError as e:
            raise EmbeddingServiceHTTPError(e.status, e.message) from e
        except Exception as e:
            raise EmbeddingServiceError(f"Unexpected error: {e}") from e

    async def cmd(self, command: str, params: Optional[Dict[str, Any]] = None, base_url: Optional[str] = None, port: Optional[int] = None) -> Dict[str, Any]:
        """
        Execute a command via JSON-RPC protocol.
        Args:
            command (str): Command to execute (embed, models, health, help, config).
            params (dict, optional): Parameters for the command.
            base_url (str, optional): Override base URL.
            port (int, optional): Override port.
        Returns:
            dict: Command execution result.
        """
        url = self._make_url("/cmd", base_url, port)
        payload = {"command": command}
        if params is not None:
            payload["params"] = params
        try:
            async with self._session.post(url, json=payload) as resp:
                await self._raise_for_status(resp)
                data = await resp.json()
                # Обработка ошибок, возвращаемых сервером в теле ответа
                if "error" in data:
                    raise EmbeddingServiceAPIError(data["error"])
                return data
        except EmbeddingServiceAPIError:
            raise
        except EmbeddingServiceHTTPError:
            raise
        except EmbeddingServiceConnectionError:
            raise
        except aiohttp.ClientConnectionError as e:
            raise EmbeddingServiceConnectionError(f"Connection error: {e}") from e
        except aiohttp.ClientResponseError as e:
            raise EmbeddingServiceHTTPError(e.status, e.message) from e
        except Exception as e:
            raise EmbeddingServiceError(f"Unexpected error: {e}") from e

    async def _raise_for_status(self, resp: aiohttp.ClientResponse):
        try:
            resp.raise_for_status()
        except aiohttp.ClientResponseError as e:
            raise EmbeddingServiceHTTPError(e.status, e.message) from e

    # TODO: Add methods for /cmd, /api/commands, etc. 