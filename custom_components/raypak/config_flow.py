"""Config flow for Raypak Pool Heater."""

from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import callback

from .api import RaypakApiClient, RaypakApiError, RaypakAuthError
from .const import (
    CONF_POLL_INTERVAL,
    CONF_SERVER,
    CONF_TOKEN,
    DEFAULT_POLL_INTERVAL,
    DEFAULT_SERVER,
    DOMAIN,
    MAX_POLL_INTERVAL,
    MIN_POLL_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)

USER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_SERVER, default=DEFAULT_SERVER): str,
        vol.Required(CONF_TOKEN): str,
        vol.Optional(
            CONF_POLL_INTERVAL, default=DEFAULT_POLL_INTERVAL
        ): vol.All(int, vol.Range(min=MIN_POLL_INTERVAL, max=MAX_POLL_INTERVAL)),
    }
)


class RaypakConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Raypak."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            token = user_input[CONF_TOKEN]
            server = user_input[CONF_SERVER]

            await self.async_set_unique_id(token)
            self._abort_if_unique_id_configured()

            session = aiohttp.ClientSession()
            client = RaypakApiClient(session, server, token)
            try:
                await client.async_is_connected()
            except RaypakAuthError:
                errors["base"] = "invalid_auth"
            except RaypakApiError:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected error")
                errors["base"] = "unknown"
            finally:
                await session.close()

            if not errors:
                return self.async_create_entry(
                    title="Raypak Pool Heater",
                    data={
                        CONF_SERVER: server,
                        CONF_TOKEN: token,
                    },
                    options={
                        CONF_POLL_INTERVAL: user_input.get(
                            CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL
                        ),
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=USER_SCHEMA,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Get the options flow."""
        return RaypakOptionsFlow(config_entry)


class RaypakOptionsFlow(OptionsFlow):
    """Handle options flow for Raypak."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        current_interval = self._config_entry.options.get(
            CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL
        )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_POLL_INTERVAL, default=current_interval
                    ): vol.All(
                        int,
                        vol.Range(min=MIN_POLL_INTERVAL, max=MAX_POLL_INTERVAL),
                    ),
                }
            ),
        )
