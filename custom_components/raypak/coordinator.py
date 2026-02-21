"""DataUpdateCoordinator for Raypak pool heater."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import RaypakApiClient, RaypakApiError, RaypakAuthError
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class RaypakDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator to poll the Raypak API."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: RaypakApiClient,
        poll_interval: int,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=poll_interval),
        )
        self.client = client
        self.connected: bool = False

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the API."""
        try:
            data = await self.client.async_get_all()
            self.connected = await self.client.async_is_connected()
        except RaypakAuthError as err:
            raise ConfigEntryAuthFailed(str(err)) from err
        except RaypakApiError as err:
            raise UpdateFailed(str(err)) from err

        return data
