"""Blynk HTTP API client for Raypak pool heaters."""

from __future__ import annotations

import asyncio
from typing import Any

import aiohttp


class RaypakApiError(Exception):
    """General API error."""


class RaypakAuthError(RaypakApiError):
    """Authentication error."""


class RaypakApiClient:
    """Async HTTP client for the Raypak/Blynk API."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        server: str,
        token: str,
    ) -> None:
        """Initialize the API client."""
        self._session = session
        self._base_url = f"https://{server}/external/api"
        self._token = token

    async def _request(self, endpoint: str, params: dict[str, Any] | None = None) -> Any:
        """Make an API request."""
        url = f"{self._base_url}/{endpoint}"
        request_params = {"token": self._token}
        if params:
            request_params.update(params)

        try:
            async with asyncio.timeout(10):
                resp = await self._session.get(url, params=request_params)
        except asyncio.TimeoutError as err:
            raise RaypakApiError(f"Timeout connecting to {url}") from err
        except aiohttp.ClientError as err:
            raise RaypakApiError(f"Error connecting to {url}: {err}") from err

        if resp.status == 401:
            raise RaypakAuthError("Invalid token")
        if resp.status != 200:
            raise RaypakApiError(f"API returned status {resp.status}")

        content_type = resp.content_type or ""
        if "json" in content_type:
            return await resp.json()
        return await resp.text()

    async def async_get_all(self) -> dict[str, Any]:
        """Get all pin values."""
        result = await self._request("getAll")
        if not isinstance(result, dict):
            raise RaypakApiError(f"Unexpected response type: {type(result)}")
        return result

    async def async_update_pin(self, pin: str, value: Any) -> None:
        """Update a pin value."""
        await self._request("update", {pin: str(value)})

    async def async_is_connected(self) -> bool:
        """Check if the hardware is connected."""
        result = await self._request("isHardwareConnected")
        if isinstance(result, bool):
            return result
        return str(result).strip().lower() == "true"
