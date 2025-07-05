from homeassistant.core import HomeAssistant
from .const import DOMAIN

def setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass, config_entry):
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "automation")
    )
    return True

async def async_unload_entry(hass, config_entry):
    return await hass.config_entries.async_forward_entry_unload(config_entry, "automation")