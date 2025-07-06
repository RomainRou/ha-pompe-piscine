from homeassistant.helpers.entity import Entity
from .const import DOMAIN

async def async_setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([
        CycleEnCoursSensor(hass), DureeCycleTotal(hass), DureeCycleRestante(hass)
    ])

class CycleEnCoursSensor(Entity):
    def __init__(self, hass):
        self._hass = hass
        self._attr = None
    @property
    def name(self): return "cycle_en_cours_txt"
    @property
    def state(self):
        return "Oui" if self._hass.states.is_state("input_boolean.cycle_en_cours","on") else "Non"
    @property
    def unique_id(self): return DOMAIN + "_cycle_en_cours"
    async def async_update(self): pass

# À compléter pour les durations avec calculs basés sur datetime et helpers