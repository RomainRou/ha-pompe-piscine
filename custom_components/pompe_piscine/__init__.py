from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

DOMAIN = "pompe_piscine"

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "switch")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    return await hass.config_entries.async_forward_entry_unload(config_entry, "switch")