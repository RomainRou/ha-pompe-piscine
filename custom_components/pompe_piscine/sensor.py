from homeassistant.components.sensor import SensorEntity
from . import const

async def async_setup_entry(hass, entry, async_add_entities):
    data = entry.data
    async_add_entities([
        CycleEnCoursSensor(), CycleNomSensor(),
        DureeTotaleSensor(), TempsRestantSensor()
    ])

class BaseSensor(SensorEntity):
    @property
    def available(self):
        return True

class CycleEnCoursSensor(BaseSensor):
    @property
    def unique_id(self):
        return "piscine_cycle_en_cours"
    @property
    def name(self):
        return "Cycle en cours"
    @property
    def state(self):
        return self.hass.states.get("input_boolean.piscine_cycle_en_cours").state.title()

class CycleNomSensor(BaseSensor):
    @property
    def unique_id(self):
        return "piscine_cycle_nom"
    @property
    def name(self):
        return "Nom cycle"
    @property
    def state(self):
        return self.hass.states.get("input_select.piscine_mode").state or "Aucun"

class DureeTotaleSensor(BaseSensor):
    @property
    def unique_id(self):
        return "piscine_duree_cycle"
    @property
    def name(self):
        return "Durée cycle (h:mm)"
    @property
    def state(self):
        return self.hass.states.get("sensor._durée_total").state or "0:00"

class TempsRestantSensor(BaseSensor):
    @property
    def unique_id(self):
        return "piscine_temps_restant"
    @property
    def name(self):
        return "Temps restant (h:mm)"
    @property
    def state(self):
        return self.hass.states.get("sensor._temps_restant").state or "0:00"