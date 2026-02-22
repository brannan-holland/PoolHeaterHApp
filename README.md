# Raypak Pool Heater for Home Assistant

A custom Home Assistant integration for Raypak pool heaters using the [RayMoTe](https://raymote.raypak.com) cloud control system (Blynk IoT platform).

## Features

- **Water heater entity** — View current/target temperature and control operation mode and setpoint (60–104°F)
- **16 sensors** — Inlet/outlet/flue temps, flame current, ignition status, fault codes, heating cycles, flow rate, VSP speed, and more
- **2 binary sensors** — Hardware connectivity and VSP run status
- **Configurable polling** — Adjustable 10–300 second poll interval

## Installation

### HACS (recommended)

1. Open HACS in Home Assistant
2. Go to **⋮ → Custom repositories**
3. Add `https://github.com/brannan-holland/PoolHeaterHApp` with category **Integration**
4. Search for "Raypak Pool Heater" and install
5. Restart Home Assistant

### Manual

1. Copy `custom_components/raypak/` to your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **Raypak Pool Heater**
3. Enter your RayMoTe server (default: `raymote.raypak.com`) and device token
4. Optionally adjust the poll interval (default: 30 seconds)

### Finding your device token

Your device token is the static auth token used by the RayMoTe web interface to communicate with your heater via the Blynk API. You can find it by inspecting network requests in your browser while logged into [raymote.raypak.com](https://raymote.raypak.com) — look for the `token` query parameter in API calls.

## Entities

### Water Heater

| Entity | Description |
|--------|-------------|
| Pool Heater | Current temp (inlet), target temp (setpoint), operation mode (off/heat) |

### Sensors

| Entity | Pin | Description |
|--------|-----|-------------|
| Inlet Temperature | v52 | Water temperature entering the heater |
| Outlet Temperature | v5 | Water temperature leaving the heater |
| Flue Temperature | v6 | Exhaust flue temperature |
| Ignition Voltage | v55 | Ignition status (voltage or "No Demand") |
| Flame Current | v10 | Flame sense current (µA) |
| Fault Code | v11 | Active fault code |
| Error Text | v13 | Active error description |
| Capacity | v105 | Heater capacity (%) |
| Heating Cycles | v45 | Total heating cycles |
| Heating Time | v25 | Total heating hours |
| Power Cycles | v27 | Total power cycles |
| Flow Pressure | v29 | Water flow pressure |
| Flow Rate | v7 | Water flow rate |
| VSP Speed | v14 | Variable speed pump speed (%) |
| Firing Rate | v160 | Burner firing rate (%) |
| Operation Mode | v53 | Raw operation mode value |

### Binary Sensors

| Entity | Description |
|--------|-------------|
| Hardware Connected | Whether the heater is reachable via the API |
| VSP Run Status | Whether the variable speed pump is running |

## Options

After setup, you can adjust the poll interval via **Settings → Devices & Services → Raypak Pool Heater → Configure**.

## License

MIT
