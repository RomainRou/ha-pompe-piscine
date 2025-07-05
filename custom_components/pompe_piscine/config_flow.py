import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    Selector,
)
from .const import *

class PompePiscineConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Pompe Piscine", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_POMPE): EntitySelector(EntitySelectorConfig(domain="switch")),
                vol.Required(CONF_TEMP_EAU): EntitySelector(EntitySelectorConfig(domain="sensor")),
                vol.Required(CONF_TEMP_EXT): EntitySelector(EntitySelectorConfig(domain="sensor")),
                vol.Required(CONF_METEO): EntitySelector(EntitySelectorConfig(domain="weather")),
                vol.Required(CONF_TEMPS_CYCLE): vol.All(vol.Coerce(int), vol.Range(min=1)),
                vol.Required(CONF_TELEGRAM_USER): str,  # Could be a text input or selector if Telegram integration exists
                vol.Required(CONF_SAISON): vol.In(["été", "hiver", "automne", "printemps"]),  # or use selector
            })
        )
