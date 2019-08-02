"""
Binary sensor platform integration for Judo i-Soft Plus.
For more details about this component, please refer to the documentation at
https://github.com/ToSa27/homeassistant-judoisoft
"""

from homeassistant.helpers.entity import Entity
from homeassistant.components.switch import Switch

from custom_components.judoisoft import DOMAIN as DOMAIN
from custom_components.judoisoft import ISoftEntity

#DEPENDENCIES = ['judoisoftpy']

def setup_platform(hass, config, add_entities, discovery_info=None):
    isoft = hass.data[DOMAIN]['api']
    add_entities([ISoftSwitch(isoft, 'Regeneration', 'get_regeneration', 'set_regeneration', 'start', 'stop')])
#    add_entities([ISoftSwitch(isoft, 'Valve', 'get_valve', 'set_valve', 'open', 'close')])

class ISoftSwitch(ISoftEntity, Switch):

    def __init__(self, name, getfn, setfn, onval, offval):
        super().__init__(name)
        self._state = None
        self._getfn = getattr(self._isoft, getfn)
        self._setfn = getattr(self._isoft, getfn)
        self._onval = onval
        self._offval = offval

    @property
    def state(self):
        return self._state

    @property
    def is_on(self):
        return self._state == self._onval

    def turn_on(self):
        self._setfn(self._onval)

    def turn_off(self):
        self._setfn(self._offval)

    def update(self):
        self._state = self._getfn()
