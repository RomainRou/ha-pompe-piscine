from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

DOMAIN = "pompe_piscine"

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([PompePiscineSwitch()])


class PompePiscineSwitch(SwitchEntity):
    def __init__(self):
        self._attr_is_on = False
        self._attr_name = "Pompe Piscine"

    @property
    def is_on(self) -> bool:
        return self._attr_is_on

    def turn_on(self, **kwargs) -> None:
        self._attr_is_on = True
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs) -> None:
        self._attr_is_on = False
        self.schedule_update_ha_state()