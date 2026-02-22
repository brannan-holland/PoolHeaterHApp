"""Constants for the Raypak Pool Heater integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntityDescription,
)
from homeassistant.const import (
    UnitOfTemperature,
    UnitOfElectricPotential,
    UnitOfTime,
    PERCENTAGE,
)

DOMAIN = "raypak"

CONF_SERVER = "server"
CONF_TOKEN = "token"
CONF_POLL_INTERVAL = "poll_interval"

DEFAULT_SERVER = "raymote.raypak.com"
DEFAULT_POLL_INTERVAL = 30
MIN_POLL_INTERVAL = 10
MAX_POLL_INTERVAL = 300

# Pin mappings
PIN_INLET_TEMP = "v52"
PIN_OUTLET_TEMP = "v5"
PIN_FLUE_TEMP = "v6"
PIN_OPERATION_MODE = "v53"
PIN_IGNITION_VOLTAGE = "v55"
PIN_SETPOINT = "v111"
PIN_FLAME_CURRENT = "v10"
PIN_FAULT_CODE = "v11"
PIN_ERROR_TEXT = "v13"
PIN_CAPACITY = "v105"
PIN_HEATING_CYCLES = "v45"
PIN_HEATING_TIME = "v25"
PIN_POWER_CYCLES = "v27"
PIN_FLOW_PRESSURE = "v29"
PIN_FLOW_RATE = "v7"
PIN_VSP_SPEED = "v14"
PIN_VSP_RUN_STATUS = "v162"
PIN_FIRING_RATE = "v160"

MANUFACTURER = "Raypak"
MODEL = "Pool Heater"


@dataclass(frozen=True, kw_only=True)
class RaypakSensorEntityDescription(SensorEntityDescription):
    """Describes a Raypak sensor entity."""

    pin: str
    value_fn: Callable[[Any], Any] = lambda x: x


@dataclass(frozen=True, kw_only=True)
class RaypakBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes a Raypak binary sensor entity."""

    pin: str | None = None
    value_fn: Callable[[Any], bool] = lambda x: bool(x)


SENSOR_DESCRIPTIONS: tuple[RaypakSensorEntityDescription, ...] = (
    RaypakSensorEntityDescription(
        key="inlet_temperature",
        translation_key="inlet_temperature",
        pin=PIN_INLET_TEMP,
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda x: round(float(x), 1) if x is not None else None,
    ),
    RaypakSensorEntityDescription(
        key="outlet_temperature",
        translation_key="outlet_temperature",
        pin=PIN_OUTLET_TEMP,
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda x: round(float(x), 1) if x is not None else None,
    ),
    RaypakSensorEntityDescription(
        key="flue_temperature",
        translation_key="flue_temperature",
        pin=PIN_FLUE_TEMP,
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda x: round(float(x), 1) if x is not None else None,
    ),
    RaypakSensorEntityDescription(
        key="ignition_voltage",
        translation_key="ignition_voltage",
        pin=PIN_IGNITION_VOLTAGE,
        value_fn=lambda x: str(x).strip('"') if x is not None else None,
    ),
    RaypakSensorEntityDescription(
        key="flame_current",
        translation_key="flame_current",
        pin=PIN_FLAME_CURRENT,
        native_unit_of_measurement="µA",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda x: round(float(x), 1) if x is not None else None,
    ),
    RaypakSensorEntityDescription(
        key="fault_code",
        translation_key="fault_code",
        pin=PIN_FAULT_CODE,
        value_fn=lambda x: str(x) if x is not None else None,
    ),
    RaypakSensorEntityDescription(
        key="error_text",
        translation_key="error_text",
        pin=PIN_ERROR_TEXT,
        value_fn=lambda x: str(x).strip('"') if x is not None else None,
    ),
    RaypakSensorEntityDescription(
        key="capacity",
        translation_key="capacity",
        pin=PIN_CAPACITY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda x: round(float(x), 1) if x is not None else None,
    ),
    RaypakSensorEntityDescription(
        key="heating_cycles",
        translation_key="heating_cycles",
        pin=PIN_HEATING_CYCLES,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda x: int(float(x)) if x is not None else None,
    ),
    RaypakSensorEntityDescription(
        key="heating_time",
        translation_key="heating_time",
        pin=PIN_HEATING_TIME,
        native_unit_of_measurement=UnitOfTime.HOURS,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda x: round(float(x), 1) if x is not None else None,
    ),
    RaypakSensorEntityDescription(
        key="power_cycles",
        translation_key="power_cycles",
        pin=PIN_POWER_CYCLES,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda x: int(float(x)) if x is not None else None,
    ),
    RaypakSensorEntityDescription(
        key="flow_pressure",
        translation_key="flow_pressure",
        pin=PIN_FLOW_PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda x: round(float(x), 2) if x is not None else None,
    ),
    RaypakSensorEntityDescription(
        key="flow_rate",
        translation_key="flow_rate",
        pin=PIN_FLOW_RATE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda x: round(float(x), 1) if x is not None else None,
    ),
    RaypakSensorEntityDescription(
        key="vsp_speed",
        translation_key="vsp_speed",
        pin=PIN_VSP_SPEED,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda x: round(float(x), 1) if x is not None else None,
    ),
    RaypakSensorEntityDescription(
        key="firing_rate",
        translation_key="firing_rate",
        pin=PIN_FIRING_RATE,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda x: round(float(x), 1) if x is not None else None,
    ),
    RaypakSensorEntityDescription(
        key="operation_mode",
        translation_key="operation_mode_sensor",
        pin=PIN_OPERATION_MODE,
        value_fn=lambda x: str(x) if x is not None else None,
    ),
)

BINARY_SENSOR_DESCRIPTIONS: tuple[RaypakBinarySensorEntityDescription, ...] = (
    RaypakBinarySensorEntityDescription(
        key="hardware_connected",
        translation_key="hardware_connected",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        pin=None,
    ),
    RaypakBinarySensorEntityDescription(
        key="vsp_run_status",
        translation_key="vsp_run_status",
        device_class=BinarySensorDeviceClass.RUNNING,
        pin=PIN_VSP_RUN_STATUS,
        value_fn=lambda x: bool(int(float(x))) if x is not None else False,
    ),
)
