import voluptuous as vol
from homeassistant import config_entries
from .const import *

class PompePiscineConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Pompe Piscine", data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_POMPE): str,
            vol.Required(CONF_TEMP_EAU): str,
            vol.Required(CONF_TEMP_EXT): str,
            vol.Required(CONF_METEO): str,
            vol.Required(CONF_TEMPS_CYCLE): int,
            vol.Required(CONF_TELEGRAM_USER): str,
            vol.Required(CONF_SAISON): str,
        })

        return self.async_show_form(step_id="user", data_schema=schema)