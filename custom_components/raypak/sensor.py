"""Sensor platform for Raypak pool heater."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import RaypakSensorEntityDescription, SENSOR_DESCRIPTIONS
from .coordinator import RaypakDataUpdateCoordinator
from .entity import RaypakEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Raypak sensor entities."""
    coordinator: RaypakDataUpdateCoordinator = entry.runtime_data
    async_add_entities(
        RaypakSensor(coordinator, entry.entry_id, description)
        for description in SENSOR_DESCRIPTIONS
    )


class RaypakSensor(RaypakEntity, SensorEntity):
    """Raypak sensor entity."""

    entity_description: RaypakSensorEntityDescription

    def __init__(
        self,
        coordinator: RaypakDataUpdateCoordinator,
        entry_id: str,
        description: RaypakSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry_id)
        self.entity_description = description
        self._attr_unique_id = f"{entry_id}_{description.key}"

    @property
    def native_value(self):
        """Return the sensor value."""
        raw = self.coordinator.data.get(self.entity_description.pin)
        try:
            return self.entity_description.value_fn(raw)
        except (ValueError, TypeError):
            return None
