import asyncio, datetime
import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from . import const

_LOGGER = logging.getLogger(__name__)

class PiscineCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, entry):
        super().__init__(hass, _LOGGER, name="piscine", update_interval=None)
        self.hass = hass
        self.data = entry.data
        hass.loop.create_task(self._setup_helpers())

    async def _setup_helpers(self):
        # Création dynamique des helpers
        for dt in const.INPUT_DATETIME:
            eid = f"input_datetime.piscine_{dt}"
            if not self.hass.states.get(eid):
                await self.hass.services.async_call(
                    "input_datetime", "create", {
                        "name": f"Heure {dt.replace('_',' ')}",
                        "has_date": False,
                        "has_time": True,
                        "entity_id": eid
                    }, blocking=True
                )
        for num in const.INPUT_NUMBER:
            eid = f"input_number.piscine_{num}"
            if not self.hass.states.get(eid):
                await self.hass.services.async_call(
                    "input_number", "create", {
                        "name": num.replace('_', ' ').capitalize(),
                        "min": 0,
                        "max": 100,
                        "step": 1,
                        "mode": "slider",
                        "unit_of_measurement": "h" if num in ["filtration_min_hiver",] else "m³/h" if num=="debit_pompe" else "°C" if num=="ph" else "min",
                        "entity_id": eid,
                        "initial": const.INPUT_NUMBER_DEFAULTS[num]
                    }, blocking=True
                )
        eid = "input_boolean.piscine_cycle_en_cours"
        if not self.hass.states.get(eid):
            await self.hass.services.async_call(
                "input_boolean", "create", {"name": "Cycle en cours", "entity_id": eid}, blocking=True
            )
        eid = "input_select.piscine_mode"
        if not self.hass.states.get(eid):
            await self.hass.services.async_call(
                "input_select", "create", {
                    "name": "Mode piscine",
                    "options": const.MODE_OPTIONS,
                    "initial": "Filtration normale",
                    "entity_id": eid
                }, blocking=True
            )
        # Scheduler
        await self._schedule_cycle("matin")
        await self._schedule_cycle("apresmidi")

    async def _schedule_cycle(self, period):
        eid = f"input_datetime.piscine_heure_{period}"
        state = self.hass.states.get(eid)
        if state and state.state:
            now = datetime.datetime.now()
            t = datetime.datetime.fromisoformat(f"{now.date()}T{state.state}")
            if t < now:
                t += datetime.timedelta(days=1)
            delay = (t - now).total_seconds()
            self.hass.loop.call_later(delay, lambda: asyncio.create_task(self.run_cycle(period)))

    async def run_cycle(self, period):
        # lancement du cycle (Matin ou Aprem)
        # Calcul durée, gestion météo, envoyer Telegram, etc.
        # À implémenter complet selon ton blueprint
        ...