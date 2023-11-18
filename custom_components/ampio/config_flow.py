"""Config flow to configure Ampio System."""
from collections import OrderedDict
from typing import Optional

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.mqtt.config_flow import try_connection
from homeassistant.components.mqtt.const import CONF_BROKER
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT, CONF_USERNAME

DOMAIN = "ampio"
CLIENT_ID = "HomeAssistant-{}".format("12312312")
KEEPALIVE = 600


@config_entries.HANDLERS.register("ampio")
class AmpioFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a Ampio config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    def __init__(self):
        """Initialize flow."""
        self._broker: Optional[str] = None
        self._port: Optional[int] = None

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        return await self.async_step_broker()

    async def async_step_broker(self, user_input=None):
        """Confirm the setup."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_BROKER], data=user_input
            )

        #     can_connect = await self.hass.async_add_executor_job(
        #         try_connection,
        #         user_input[CONF_BROKER],
        #         user_input[CONF_PORT],
        #         user_input.get(CONF_USERNAME),
        #         user_input.get(CONF_PASSWORD),
        #     )

        #     if can_connect:
        #         return self.async_create_entry(
        #             title=user_input[CONF_BROKER], data=user_input
        #         )

        #     errors["base"] = "cannot_connect"
        
        fields = OrderedDict()
        fields[vol.Required(CONF_BROKER, default=self._broker or vol.UNDEFINED)] = str
        fields[vol.Required(CONF_PORT, default=self._port or 1883)] = vol.Coerce(int)
        fields[vol.Optional(CONF_USERNAME)] = str
        fields[vol.Optional(CONF_PASSWORD)] = str

        return self.async_show_form(
            step_id="broker", data_schema=vol.Schema(fields), errors=errors
        )

    async def async_step_zeroconf(self, discovery_info):
        """Prepare configuration for a discovered Ampio device."""
        print(discovery_info)
        self._broker = discovery_info.host
        self._port = discovery_info.port
        return self.async_show_form(
            step_id="broker", description_placeholders={"name": self._broker}
        )
