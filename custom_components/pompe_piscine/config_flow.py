import voluptuous as vol
from homeassistant import config_entries
from . import const

STEP_SCHEMA = vol.Schema({
    vol.Required(const.CONF_POMPE_SWITCH): str,
    vol.Required(const.CONF_SENSOR_TEMP): str,
    vol.Required(const.CONF_SENSOR_TEMP_EXT): str,
    vol.Required(const.CONF_SENSOR_SAISON): str,
    vol.Required(const.CONF_WEATHER): str,
    vol.Required(const.CONF_MODE_SELECT): str,
    vol.Required(const.CONF_TELEGRAM_ID): str,
})

class ConfigFlow(config_entries.ConfigFlow, domain=const.DOMAIN):
    VERSION = 1
    
    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=STEP_SCHEMA)
        return self.async_create_entry(title="Pompe Piscine", data=user_input)