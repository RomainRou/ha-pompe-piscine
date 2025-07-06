import asyncio
from homeassistant.core import HomeAssistant
from .helpers import async_create_helpers
from homeassistant.helpers.event import async_track_time_interval
from datetime import timedelta
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry):
    data = entry.data
    await async_create_helpers(hass)

    # Lance la surveillance au démarrage
    hass.async_create_task(startup(hass, data))

    return True

async def startup(hass, data):
    async def check_cycle(_now):
        en_cours = hass.states.get("input_boolean.cycle_en_cours")
        if en_cours and en_cours.state == "on":
            duree = hass.states.get("input_number.duree_cycle")
            debut = hass.states.get("input_datetime.cycle_debut")
            if debut and duree:
                # vérifier si le cycle est terminé
                from datetime import datetime, timedelta
                try:
                    debut_dt = datetime.strptime(debut.state, "%Y-%m-%d %H:%M:%S")
                    fin = debut_dt + timedelta(seconds=int(float(duree.state)))
                    if datetime.now() >= fin:
                        _LOGGER.info("Cycle terminé. Arrêt de la pompe.")
                        await hass.services.async_call("switch", "turn_off", {
                            "entity_id": "switch.pompe"
                        })
                        await hass.services.async_call("input_boolean", "turn_off", {
                            "entity_id": "input_boolean.cycle_en_cours"
                        })
                except Exception as e:
                    _LOGGER.error(f"Erreur de parsing datetime: {e}")

    # Check toutes les minutes
    async_track_time_interval(hass, check_cycle, timedelta(minutes=1))