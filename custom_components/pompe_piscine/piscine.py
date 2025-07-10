import logging
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    async def handle_filtration_service(call):
        mode = call.data.get("mode")
        pompe = call.data.get("pompe")
        duree = call.data.get("duree", 3600)

        _LOGGER.info(f"[Piscine Manager] Lancement en mode {mode} pour {duree}s")

        await hass.services.async_call("switch", "turn_on", {"entity_id": pompe})
        
        await asyncio.sleep(duree)
        
        await hass.services.async_call("switch", "turn_off", {"entity_id": pompe})

        _LOGGER.info(f"[Piscine Manager] Pompe arrêtée après {duree}s")

    hass.services.async_register("piscine_manager", "start_filtration", handle_filtration_service)

    return True
