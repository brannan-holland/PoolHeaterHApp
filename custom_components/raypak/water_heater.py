"""Water heater platform for Raypak pool heater."""

from __future__ import annotations

from typing import Any

from homeassistant.components.water_heater import (
    WaterHeaterEntity,
    WaterHeaterEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import PIN_INLET_TEMP, PIN_OPERATION_MODE, PIN_SETPOINT
from .coordinator import RaypakDataUpdateCoordinator
from .entity import RaypakEntity

OPERATION_OFF = "off"
OPERATION_HEAT = "heat"
OPERATION_LIST = [OPERATION_OFF, OPERATION_HEAT]

MIN_TEMP = 60
MAX_TEMP = 104


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the water heater platform."""
    coordinator: RaypakDataUpdateCoordinator = entry.runtime_data
    async_add_entities([RaypakWaterHeater(coordinator, entry.entry_id)])


class RaypakWaterHeater(RaypakEntity, WaterHeaterEntity):
    """Raypak pool heater water heater entity."""

    _attr_supported_features = (
        WaterHeaterEntityFeature.TARGET_TEMPERATURE
        | WaterHeaterEntityFeature.OPERATION_MODE
    )
    _attr_temperature_unit = UnitOfTemperature.FAHRENHEIT
    _attr_operation_list = OPERATION_LIST
    _attr_min_temp = MIN_TEMP
    _attr_max_temp = MAX_TEMP
    _attr_translation_key = "pool_heater"

    def __init__(
        self,
        coordinator: RaypakDataUpdateCoordinator,
        entry_id: str,
    ) -> None:
        """Initialize the water heater."""
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_water_heater"

    @property
    def current_temperature(self) -> float | None:
        """Return the current inlet temperature."""
        value = self.coordinator.data.get(PIN_INLET_TEMP)
        if value is None:
            return None
        try:
            return round(float(value), 1)
        except (ValueError, TypeError):
            return None

    @property
    def target_temperature(self) -> float | None:
        """Return the target temperature (setpoint)."""
        value = self.coordinator.data.get(PIN_SETPOINT)
        if value is None:
            return None
        try:
            return round(float(value), 1)
        except (ValueError, TypeError):
            return None

    @property
    def current_operation(self) -> str:
        """Return the current operation mode."""
        value = self.coordinator.data.get(PIN_OPERATION_MODE)
        if value is None:
            return OPERATION_OFF
        try:
            return OPERATION_HEAT if int(float(value)) != 0 else OPERATION_OFF
        except (ValueError, TypeError):
            return OPERATION_OFF

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set the target temperature."""
        temperature = kwargs.get("temperature")
        if temperature is None:
            return
        await self.coordinator.client.async_update_pin(
            PIN_SETPOINT, int(temperature)
        )
        await self.coordinator.async_request_refresh()

    async def async_set_operation_mode(self, operation_mode: str) -> None:
        """Set the operation mode."""
        value = 0 if operation_mode == OPERATION_OFF else 1
        await self.coordinator.client.async_update_pin(PIN_OPERATION_MODE, value)
        await self.coordinator.async_request_refresh()
