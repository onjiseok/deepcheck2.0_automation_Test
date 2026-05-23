from __future__ import annotations

import httpx


class ApiClient:
    """Thin wrapper around httpx for backend API tests.

    Add domain helpers (login, create_resource, ...) here as flows are written,
    so individual tests stay declarative.
    """

    def __init__(self, base_url: str, timeout: float = 30.0) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def get(self, path: str, **kwargs) -> httpx.Response:
        return self._client.get(path, **kwargs)

    def post(self, path: str, **kwargs) -> httpx.Response:
        return self._client.post(path, **kwargs)

    def put(self, path: str, **kwargs) -> httpx.Response:
        return self._client.put(path, **kwargs)

    def delete(self, path: str, **kwargs) -> httpx.Response:
        return self._client.delete(path, **kwargs)

    def set_auth_token(self, token: str) -> None:
        self._client.headers["Authorization"] = f"Bearer {token}"

    def close(self) -> None:
        self._client.close()
