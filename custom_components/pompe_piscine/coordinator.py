import asyncio, datetime
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant, callback
from . import const

class PiscineCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, config):
        super().__init__(hass, _LOGGER, name="Pompe Piscine", update_interval=None)
        self.config = config
        hass.loop.create_task(self._init_entities())

    async def _init_entities(self):
        ent = self.config
        # creation dynamic of inputs (datetime, number, boolean)
        # example:
        await self.hass.services.async_call(
            "input_datetime", "set_datetime",
            {"entity_id": f"input_datetime.piscine_heure_matin", "time": "06:00:00"}
        )
        # similar for apres-midi, input_numbers for modes, input_boolean.piscine_cycle_en_cours

        # schedule next runs
        self._schedule_cycle("matin", ent)
        self._schedule_cycle("apresmidi", ent)

    def _schedule_cycle(self, period: str, ent: dict):
        # compute next datetime from input_datetime...
        # then use hass.helpers.event.async_call_later to plan run_cycle

    async def async_update(self):
        # update sensor temps, saison, weather state...
        pass

    async def run_cycle(self):
        # logic: compute duration, turn on/off switch, send Telegram
        pass