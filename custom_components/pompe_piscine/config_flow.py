import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    TextSelector,
    TextSelectorConfig
)
from . import const

class ConfigFlow(config_entries.ConfigFlow, domain=const.DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Pompe Piscine", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(const.CONF_POMPE_SWITCH): EntitySelector(
                    EntitySelectorConfig(domain="switch")
                ),
                vol.Required(const.CONF_SENSOR_TEMP): EntitySelector(
                    EntitySelectorConfig(domain="sensor", device_class="temperature")
                ),
                vol.Required(const.CONF_SENSOR_TEMP_EXT): EntitySelector(
                    EntitySelectorConfig(domain="sensor", device_class="temperature")
                ),
                vol.Required(const.CONF_SENSOR_SAISON): EntitySelector(
                    EntitySelectorConfig(domain="sensor")
                ),
                vol.Required(const.CONF_WEATHER): EntitySelector(
                    EntitySelectorConfig(domain="weather")
                ),
                vol.Required(const.CONF_MODE_SELECT): EntitySelector(
                    EntitySelectorConfig(domain="input_select")
                ),
                vol.Required(const.CONF_TELEGRAM_ID): TextSelector(
                    TextSelectorConfig(type="text", multiline=False)
                ),
            })
        )