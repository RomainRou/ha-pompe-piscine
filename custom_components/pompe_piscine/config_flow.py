import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

class PiscineConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Piscine Intelligente", data=user_input)
        schema = vol.Schema({
            vol.Required("switch_pompe"): str,
            vol.Required("sensor_temp_piscine"): str,
            vol.Required("sensor_temp_exterieure"): str,
            vol.Required("sensor_saison"): str,
            vol.Required("weather_entity"): str,
            vol.Required("telegram_user"): str
        })
        return self.async_show_form(step_id="user", data_schema=schema)