import asyncio
import logging
from datetime import datetime, timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval
from .helpers import async_validate_helpers

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry):
    """Configure l'intégration Piscine Intelligente."""

    is_valid = await async_validate_helpers(hass)
    if not is_valid:
        _LOGGER.error("Des entités requises sont manquantes. L'intégration ne peut pas être chargée.")
        return False

    data = entry.options  # Options contient les entités choisies

    hass.async_create_task(startup(hass, data))
    return True


async def startup(hass: HomeAssistant, data: dict):
    """Surveillance du cycle de filtration."""

    switch_pompe = data.get("switch_pompe")

    async def check_cycle(_now):
        en_cours = hass.states.get("input_boolean.cycle_en_cours")
        if en_cours and en_cours.state == "on":
            duree = hass.states.get("input_number.duree_cycle")
            debut = hass.states.get("input_datetime.cycle_debut")
            if debut and duree:
                try:
                    debut_dt = datetime.strptime(debut.state, "%Y-%m-%d %H:%M:%S")
                    fin = debut_dt + timedelta(seconds=int(float(duree.state)))
                    if datetime.now() >= fin:
                        _LOGGER.info("Cycle terminé. Arrêt de la pompe.")
                        await hass.services.async_call("switch", "turn_off", {
                            "entity_id": switch_pompe
                        })
                        await hass.services.async_call("input_boolean", "turn_off", {
                            "entity_id": "input_boolean.cycle_en_cours"
                        })
                except Exception as e:
                    _LOGGER.error(f"[Piscine] Erreur de parsing datetime: {e}")

    # Vérifie toutes les minutes si le cycle doit être arrêté
    async_track_time_interval(hass, check_cycle, timedelta(minutes=1))