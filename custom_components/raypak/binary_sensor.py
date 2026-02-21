"""Binary sensor platform for Raypak pool heater."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    BINARY_SENSOR_DESCRIPTIONS,
    RaypakBinarySensorEntityDescription,
)
from .coordinator import RaypakDataUpdateCoordinator
from .entity import RaypakEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Raypak binary sensor entities."""
    coordinator: RaypakDataUpdateCoordinator = entry.runtime_data
    async_add_entities(
        RaypakBinarySensor(coordinator, entry.entry_id, description)
        for description in BINARY_SENSOR_DESCRIPTIONS
    )


class RaypakBinarySensor(RaypakEntity, BinarySensorEntity):
    """Raypak binary sensor entity."""

    entity_description: RaypakBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: RaypakDataUpdateCoordinator,
        entry_id: str,
        description: RaypakBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator, entry_id)
        self.entity_description = description
        self._attr_unique_id = f"{entry_id}_{description.key}"

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        if self.entity_description.pin is None:
            # Hardware connected — use coordinator property
            return self.coordinator.connected
        raw = self.coordinator.data.get(self.entity_description.pin)
        if raw is None:
            return None
        try:
            return self.entity_description.value_fn(raw)
        except (ValueError, TypeError):
            return None
