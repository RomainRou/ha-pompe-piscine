from homeassistant.components.switch import SwitchEntity
from . import const

async def async_setup_entry(hass, entry, async_add_entities):
    data = entry.data
    async_add_entities([PompeSwitch(hass, data[const.CONF_POMPE_SWITCH])])

class PompeSwitch(SwitchEntity):
    def __init__(self, hass, entity_id):
        self._entity_id = entity_id
        self._hass = hass

    @property
    def name(self):
        return "Pompe Piscine"

    @property
    def is_on(self):
        return self._hass.states.is_state(self._entity_id, "on")

    async def async_turn_on(self, **kwargs):
        await self._hass.services.async_call("switch", "turn_on", {"entity_id": self._entity_id})

    async def async_turn_off(self, **kwargs):
        await self._hass.services.async_call("switch", "turn_off", {"entity_id": self._entity_id})