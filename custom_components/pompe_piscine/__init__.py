from .const import DOMAIN
from .automation_logic import setup_automation

async def async_setup_entry(hass, entry):
    setup_automation(hass, entry.data)
    return True

async def async_unload_entry(hass, entry):
    return True