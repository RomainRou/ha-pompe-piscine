from homeassistant.components.switch import SwitchEntity
from .const import CONF_POMPE_SWITCH

async def async_setup_entry(hass, entry, async_add_entities):
    entity_id = entry.data[CONF_POMPE_SWITCH]
    async_add_entities([PompeSwitch(hass, entity_id)])

class PompeSwitch(SwitchEntity):
    def __init__(self, hass, entity_id):
        self.hass, self._entity_id = hass, entity_id

    @property
    def name(self):
        return "Pompe Piscine"

    @property
    def is_on(self):
        return self.hass.states.is_state(self._entity_id, "on")

    async def async_turn_on(self, **kwargs):
        await self.hass.services.async_call("switch", "turn_on", {"entity_id": self._entity_id})

    async def async_turn_off(self, **kwargs):
        await self.hass.services.async_call("switch", "turn_off", {"entity_id": self._entity_id})