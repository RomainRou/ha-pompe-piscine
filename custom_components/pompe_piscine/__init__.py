from .piscine import async_setup as piscine_setup

async def async_setup(hass, config):
    return await piscine_setup(hass, config)

async def async_setup_entry(hass, entry):
    """Méthode requise par Home Assistant si une config_entry existe."""
    return True
