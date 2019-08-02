import json
import os

class iSoft:

    def __init__(self, host, user, password, serial, token_cache):
        """Initialize the connection."""
        self.lastmsg = 0
        self.events = []
        self.host = host
        self.user = user
        self.password = password
        self.serial = serial
        self.token_cache = token_cache or 'judo_isoft_token'
        self.token = self.token_read()

    def token_read(self):
        """Load the token from the cache if exists, otherwise set to None."""
        if not os.path.exists(self.token_cache):
            self.token = None
        with open(self.token_cache, 'r') as f:
            self.token = f.read()

    def token_write(self):
        """Dump the token to the cache file."""
        with open(self.token_cache, 'w') as f:
            f.write(self.token)

    def check_res_token(self, resjson):
        if self.token != resjson.token:
            self.token = resjson.token
            self.token_write()
        return resjson.data

    def get(self, group, command, params = {}):
        req = 'https://' + self.host + ':8124/?'
        req += 'group=' + group
        req += '&command=' + command
        self.msgnumber = self.msgnumber + 1
        req += '&msgnumber=' + self.msgnumber
        if command != 'login':
            req += '&token=' + self.token
        for key, value in params.items():
            req += '&' + key + '=' + value
        res = requests.get(req)
        resjson = res.json()
        if resjson.status == 'ok':
            return check_res_token()
        if resjson.error == 'error':
            if resjson.data == 'not logged in':
                self.login()
                return self.get(group, command, params)
            if resjson.data == 'not connected':
                self.connect()
                return self.get(group, command, params)
            if resjson.data == 'already connected':
                return check_res_token()
        return None

    def login(self):
        r = get('register', 'login', {
            'user': self.user,
            'password': self.password,
            'role': 'customer'
        })
        if r:
            self.connect()

    def logout(self):
        get('register', 'logout')

    def connect(self):
        get('register', 'connect', {
            'parameter': 'i-soft plus',
            'serial number': self.serial
        })

    def disconnect(self):
        get('register', 'disconnect')

    def get_devcomm_version(self):
        return get('version', 'devcomm version')

    def get_electrical_control_name(self):
        return get('version', 'electrical control name')

    def get_software_version(self):
        return get('version', 'software version')

    def get_hardware_version(self):
        return get('version', 'hardware version')

    def get_part_number(self):
        return get('spare part', 'part number')

    def get_serial_number(self):
        return get('spare part', 'serial number')

    def get_order_number(self):
        return get('spare part', 'order number')

    def get_init_date(self):
        return get('contract', 'init date')

    def get_water_current(self):
        return get('consumption', 'water current')

    def get_water_daily(self, year, month, day):
        return get('consumption', 'water daily', {
            'year': year,
            'month': month,
            'day': day
        })

    def get_water_weekly(self, year, month, day):
        return get('consumption', 'water weekly', {
            'year': year,
            'month': month,
            'day': day
        })

    def get_water_monthly(self, year, month):
        return get('consumption', 'water monthly', {
            'year': year,
            'month': month
        })

    def get_water_yearly(self, year):
        return get('consumption', 'water yearly', {
            'year': year
        })

    def get_water_total(self):
        return get('consumption', 'water total')

    def get_water_of_days(self, year, month, day, offset):
        return get('consumption', 'water of days', {
            'year': year,
            'month': month,
            'day': day,
            'offset': offset
        })

    def get_water_average(self):
        return get('consumption', 'water average')

    def get_actual_abstraction_time(self):
        return get('consumption', 'actual abstraction time')

    def get_actual_quantity(self):
        return get('consumption', 'actual quantity')

    def get_salt_quantity(self):
        return get('consumption', 'salt quantity')

    def set_salt_quantity(self, quantity):
        return get('consumption', 'water average', {
            'parameter': quantity
        })

    def get_salt_range(self):
        return get('consumption', 'salt range')

    def get_residual_hardness(self):
        return get('settings', 'residual hardness')

    def set_residual_hardness(self, hardness):
        return get('settings', 'residual hardness', {
            'parameter': hardness
        })

    def get_natural_hardness(self):
        return get('info', 'natural hardness')

    def get_regeneration(self):
        return get('info', 'regeneration')

    def start_regeneration(self):
        return get('info', 'regeneration', {
            'parameter': 'start'
        })

    def stop_regeneration(self):
        return get('info', 'regeneration', {
            'parameter': 'stop'
        })

    def set_regeneration(self, value):
        return get('info', 'regeneration', {
            'parameter': value
        })

    def get_standby(self):
        return get('waterstop', 'standby')

    def set_standby(self, value):
        return get('waterstop', 'standby', {
            'parameter': value
        })

    def get_valve(self):
        return get('waterstop', 'valve')

    def set_valve(self, value):
        return get('waterstop', 'valve', {
            'parameter': value
        })

    def open_valve(self):
        return get('waterstop', 'valve', {
            'parameter': 'open'
        })

    def close_valve(self):
        return get('waterstop', 'valve', {
            'parameter': 'close'
        })

    def get_abstraction_time(self):
        return get('waterstop', 'abstraction time')

    def set_abstraction_time(self, minutes):
        return get('waterstop', 'abstraction time', {
            'parameter': minutes
        })

    def get_flow_rate(self):
        return get('waterstop', 'flow rate')

    def set_flow_rate(self, literperminute):
        return get('waterstop', 'flow rate', {
            'parameter': literperminute
        })

    def get_quantity(self):
        return get('waterstop', 'quantity')

    def set_quantity(self, liter):
        return get('waterstop', 'quantity', {
            'parameter': liter
        })

    def get_vacation(self):
        return get('waterstop', 'vacation')

    def set_vacation(self, value):
        return get('waterstop', 'vacation', {
            'parameter': value
        })

    def get_event(self, index):
        return get('state', 'event list', {
            'line': index,
            'offset': 0
        })

    def refresh_events(self):
        i = len(self.events) + 1
        hasnew = False
        while True:
            event = get_event(i)
            if event:
                if event.line == i:
                    self.events.append(event)
                    hasnew = True
                    i = i + 1
                else:
                    break
            else:
                break
        return hasnew
