import asyncio, datetime
from homeassistant.core import HomeAssistant
from .helpers import async_create_helpers
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry):
    data = entry.data
    await async_create_helpers(hass)

    hass.config_entries.async_setup_platforms(entry, [])

    hass.bus.async_listen_once("homeassistant_start", lambda evt: asyncio.create_task(startup(hass, data)))
    return True

async def startup(hass, data):
    # à compléter : lancement d’un coordinator, scheduler, etc.
    pass