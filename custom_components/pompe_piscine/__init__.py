"""Init integration"""
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = entry.data

    await hass.helpers.discovery.async_load_platform(entry, "switch")
    await hass.helpers.discovery.async_load_platform(entry, "sensor")
    
    from .coordinator import PiscineCoordinator
    coordinator = PiscineCoordinator(hass, entry)
    hass.data[DOMAIN][entry.entry_id + "_coord"] = coordinator

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data[DOMAIN].pop(entry.entry_id + "_coord", None)
    return True