from datetime import datetime, timedelta
from homeassistant.helpers.entity import Entity
from homeassistant.const import STATE_ON, STATE_OFF

class PiscineSensorBase(Entity):
    def __init__(self, hass):
        self.hass = hass
        self._attr = {}
        self._state = None

    async def async_update(self):
        pass

class CycleEnCoursSensor(PiscineSensorBase):
    @property
    def name(self):
        return "cycle_en_cours_txt"

    @property
    def state(self):
        cycle_state = self.hass.states.get("input_boolean.cycle_en_cours")
        return "Oui" if cycle_state and cycle_state.state == STATE_ON else "Non"

    @property
    def unique_id(self):
        return "piscine_cycle_en_cours"

class DureeCycleTotal(PiscineSensorBase):
    @property
    def name(self):
        return "duree_cycle_total"

    @property
    def state(self):
        duree = self.hass.states.get("input_number.duree_cycle")
        if duree and duree.state not in (None, ""):
            return round(float(duree.state) / 60)  # minutes
        return 0

    @property
    def unit_of_measurement(self):
        return "min"

    @property
    def unique_id(self):
        return "piscine_duree_cycle"

class DureeCycleRestante(PiscineSensorBase):
    @property
    def name(self):
        return "duree_cycle_restante"

    @property
    def state(self):
        debut = self.hass.states.get("input_datetime.cycle_debut")
        duree = self.hass.states.get("input_number.duree_cycle")
        en_cours = self.hass.states.get("input_boolean.cycle_en_cours")

        if not (debut and duree and en_cours and en_cours.state == STATE_ON):
            return 0

        try:
            debut_dt = datetime.strptime(debut.state, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            fin = debut_dt + timedelta(seconds=int(float(duree.state)))
            restante = (fin - now).total_seconds()
            return max(0, round(restante / 60))
        except Exception:
            return 0

    @property
    def unit_of_measurement(self):
        return "min"

    @property
    def unique_id(self):
        return "piscine_duree_cycle_restante"

async def async_setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([
        CycleEnCoursSensor(hass),
        DureeCycleTotal(hass),
        DureeCycleRestante(hass)
    ])