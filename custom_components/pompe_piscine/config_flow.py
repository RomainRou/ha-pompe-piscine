import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    TextSelector,
    TextSelectorConfig
)
from .const import DOMAIN


class PiscineConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Piscine Intelligente", data={}, options=user_input)

        schema = vol.Schema({
            vol.Required("switch_pompe"): EntitySelector(
                EntitySelectorConfig(domain="switch")
            ),
            vol.Required("sensor_temp_piscine"): EntitySelector(
                EntitySelectorConfig(domain="sensor", device_class="temperature")
            ),
            vol.Required("sensor_temp_exterieure"): EntitySelector(
                EntitySelectorConfig(domain="sensor", device_class="temperature")
            ),
            vol.Required("sensor_saison"): EntitySelector(
                EntitySelectorConfig(domain="sensor")
            ),
            vol.Required("weather_entity"): EntitySelector(
                EntitySelectorConfig(domain="weather")
            ),
            vol.Required("input_select_mode"): EntitySelector(
                EntitySelectorConfig(domain="input_select")
            ),
            vol.Required("telegram_user"): TextSelector(
                TextSelectorConfig()
            )
        })

        return self.async_show_form(step_id="user", data_schema=schema)

    async def async_step_options(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = self.options if hasattr(self, 'options') else self.config_entry.options

        schema = vol.Schema({
            vol.Required("switch_pompe", default=options.get("switch_pompe", "")): EntitySelector(
                EntitySelectorConfig(domain="switch")
            ),
            vol.Required("sensor_temp_piscine", default=options.get("sensor_temp_piscine", "")): EntitySelector(
                EntitySelectorConfig(domain="sensor", device_class="temperature")
            ),
            vol.Required("sensor_temp_exterieure", default=options.get("sensor_temp_exterieure", "")): EntitySelector(
                EntitySelectorConfig(domain="sensor", device_class="temperature")
            ),
            vol.Required("sensor_saison", default=options.get("sensor_saison", "")): EntitySelector(
                EntitySelectorConfig(domain="sensor")
            ),
            vol.Required("weather_entity", default=options.get("weather_entity", "")): EntitySelector(
                EntitySelectorConfig(domain="weather")
            ),
            vol.Required("input_select_mode", default=options.get("input_select_mode", "")): EntitySelector(
                EntitySelectorConfig(domain="input_select")
            ),
            vol.Required("telegram_user", default=options.get("telegram_user", "")): TextSelector(
                TextSelectorConfig()
            )
        })

        return self.async_show_form(step_id="options", data_schema=schema)