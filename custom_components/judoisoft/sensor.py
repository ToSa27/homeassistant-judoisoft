"""
Sensor platform integration for Judo i-Soft Plus.
For more details about this component, please refer to the documentation at
https://github.com/ToSa27/homeassistant-judoisoft
"""

DURATION_MINUTES = "min" # should move to homeassistant.const
DURATION_DAYS = "d" # should move to homeassistant.const
HARDNESS_DEGREES = "°dH" # should move to homeassistant.const

from homeassistant.const import VOLUME_LITERS
from homeassistant.helpers.entity import Entity

from custom_components.judoisoft import DOMAIN as DOMAIN
from custom_components.judoisoft import ISoftEntity

#DEPENDENCIES = ['judoisoftpy']

def setup_platform(hass, config, add_entities, discovery_info=None):
    isoft = hass.data[DOMAIN]['api']
    add_entities([ISoftSensor(isoft, 'Water Current', VOLUME_LITERS, 'get_water_current')])
    add_entities([ISoftSensor(isoft, 'Water Total', VOLUME_LITERS, 'get_water_total')])
    add_entities([ISoftSensor(isoft, 'Water Average', VOLUME_LITERS, 'get_water_average')])
    add_entities([ISoftSensor(isoft, 'Actual Abstraction Time', DURATION_MINUTES, 'get_actual_abstraction_time')])
    add_entities([ISoftSensor(isoft, 'Actual Quantity', VOLUME_LITERS, 'get_actual_quantity')])
#    add_entities([ISoftSensor(isoft, 'Salt Quantity', ???, 'get_salt_quantity')])
    add_entities([ISoftSensor(isoft, 'Salt Range', DURATION_DAYS, 'get_salt_range')])
    add_entities([ISoftSensor(isoft, 'Residual Hardness', HARDNESS_DEGREES, 'get_residual_hardness')])
    add_entities([ISoftSensor(isoft, 'Natural Hardness', HARDNESS_DEGREES, 'get_natural_hardness')])

class ISoftSensor(ISoftEntity):

    def __init__(self, name, uom, getfn):
        super().__init__(name)
        self._state = None
        self._uom = uom
        self._getfn = getattr(self._isoft, getfn)

    @property
    def unit_of_measurement(self):
        return self._uom

    def update(self):
        self._state = self._getfn()
