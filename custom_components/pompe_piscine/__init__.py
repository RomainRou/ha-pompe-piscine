from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .coordinator import async_setup_entry as setup_coordinator


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Piscine Intelligente integration from YAML (non utilisé ici)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Piscine Intelligente from a config entry."""
    # Initialisation du coordinator
    await setup_coordinator(hass, entry)

    # Écoute les modifications d'options pour redémarrer proprement
    entry.async_on_unload(entry.add_update_listener(update_listener))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Si tu ajoutes des plateformes (sensor, switch...), décharge-les ici aussi
    return True


async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)