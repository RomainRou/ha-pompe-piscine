from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([
        CycleEnCours(), CycleNom(), DureeTotale(), TempsRestant()
    ], True)

class Base(SensorEntity):
    @property
    def available(self):
        return True

class CycleEnCours(Base):
    @property
    def name(self): return "Cycle en cours"
    @property
    def state(self):
        return self.hass.states.get("input_boolean.piscine_cycle_en_cours", {}).state.title()

class CycleNom(Base):
    @property
    def name(self): return "Nom cycle"
    @property
    def state(self):
        return self.hass.states.get("input_select.piscine_mode", {}).state or "Aucun"

class DureeTotale(Base):
    @property
    def name(self): return "Durée cycle"
    @property
    def state(self):
        return self.hass.states.get("sensor.piscine_duree_secondes", {}).state or "0"

class TempsRestant(Base):
    @property
    def name(self): return "Temps restant"
    @property
    def state(self):
        return self.hass.states.get("sensor.piscine_temps_restant_secondes", {}).state or "0"