"""
Support for Judo i-Soft Plus.
For more details about this component, please refer to the documentation at
https://github.com/ToSa27/homeassistant-judoisoft
"""

#REQUIREMENTS = ['judoisoftpy==0.1.0']

from api import iSoft

DOMAIN = 'isoft'
TOKEN_PATH = '.judo-isoft-token'

def setup(hass, config):
    from judoisoftpy import iSoft

    token_cache = hass.config.path(TOKEN_PATH)
    isoft = iSoft(host = config.get(DOMAIN, {}).get('host', ''),
                  user = config.get(DOMAIN, {}).get('user', ''),
                  password = config.get(DOMAIN, {}).get('password', ''),
                  serial = config.get(DOMAIN, {}).get('serial', ''),
                  token_cache = hass.config.path(TOKEN_PATH))

    hass.data[DOMAIN] = {}
    hass.data[DOMAIN]['api'] = isoft
    return True

class ISoftEntity(Entity):

    def __init__(self, api, name):
        self._isoft = api
        self._name = name
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def available(self):
        return self._state is not None

    @property
    def should_poll(self):
        return True

    @callback
    def async_entity_update(self):
        self.schedule_update_ha_state(True)
