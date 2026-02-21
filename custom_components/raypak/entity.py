"""Base entity for Raypak pool heater."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER, MODEL
from .coordinator import RaypakDataUpdateCoordinator


class RaypakEntity(CoordinatorEntity[RaypakDataUpdateCoordinator]):
    """Base entity for Raypak devices."""

    has_entity_name = True

    def __init__(
        self,
        coordinator: RaypakDataUpdateCoordinator,
        entry_id: str,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry_id)},
            manufacturer=MANUFACTURER,
            model=MODEL,
            name="Raypak Pool Heater",
        )
