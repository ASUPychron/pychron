# ===============================================================================
# Copyright 2014 Jake Ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

# ============= standard library imports ========================
import time
# ============= enthought library imports =======================
from datetime import datetime

from traits.api import Str, Any, Bool, Float, List, Int

# ============= local library imports  ==========================
from pychron.globals import globalv
from pychron.loggable import Loggable
from pychron.pychron_constants import NULL_STR


class BaseSwitch(Loggable):
    display_name = Str
    description = Str
    prefix_name = 'BASE_SWITCH'
    state = Bool(False)
    software_lock = Bool(False)
    ignore_lock_warning = Bool(False)
    enabled = Bool(True)
    owner = Str
    track_actuation = Bool(True)
    actuations = Int
    last_actuation = Str
    explain_enabled = Bool(False)
    use_state_word = Bool(False)

    def __init__(self, name, *args, **kw):
        """
        """
        self.display_name = name
        kw['name'] = '{}-{}'.format(self.prefix_name, name)
        super(BaseSwitch, self).__init__(*args, **kw)

    def _state_changed(self):
        self.last_actuation = datetime.now().isoformat()

    def set_state(self, state):
        self.state = bool(state)

    def set_open(self, *args, **kw):
        pass

    def set_closed(self, *args, **kw):
        pass

    def lock(self):
        self.debug('Locking')
        self.software_lock = True

    def unlock(self):
        self.debug('Unlocking')
        self.software_lock = False

    def get_hardware_state(self, **kw):
        return self.state

    def get_hardware_indicator_state(self, **kw):
        return self.state

    def summary(self, width, keys):
        return self.name


class ManualSwitch(BaseSwitch):
    prefix_name = 'MANUAL_SWITCH'

    def state_str(self):
        return '{}{}'.format(self.name, self.state)

    def set_open(self, *args, **kw):
        self.state = True
        return True, True

    def set_closed(self, *args, **kw):
        self.state = False
        return True, True


class Switch(BaseSwitch):
    address = Str
    actuator = Any
    state_device = Any

    state_device_name = Str
    actuator_name = Str

    state_address = Str
    query_state = Bool(True)

    prefix_name = 'SWITCH'
    parent = Str
    parent_inverted = Bool(False)
    interlocks = List
    positive_interlocks = List

    state_invert = Bool(False)
    settling_time = Float(0)

    inverted_logic = Bool(False)

    def summary(self, widths, keys):
        vs = (getattr(self, k) for k in keys)
        args = ['{{:<{}s}}'.format(w).format(str(v) if v not in (None, '') else NULL_STR) for w,v in zip(widths, vs)]
        return ''.join(args)

    def state_str(self):
        return '{}{}{}'.format(self.name, self.state, self.software_lock)

    def _state_call(self, func, *args, **kw):
        result = None
        dev = None
        if self.state_device is not None:
            dev = self.state_device
            address = self.state_address
            # result = self.state_device.get_indicator_state(self, 'closed', **kw)
        elif self.actuator is not None:
            dev = self.actuator
            address = self.address
            # result = self.actuator.get_indicator_state(self, 'closed', **kw)

        if dev:
            func = getattr(dev, func)
            if func:
                result = func(address, *args, **kw)

        return result

    def get_hardware_indicator_state(self, verbose=True):
        msg = 'Get hardware indicator state err'

        result = self._state_call('get_indicator_state', 'closed', verbose)
        s = result
        if not isinstance(result, bool):
            self.debug('{}: {}'.format(msg, result))
            s = None
        else:
            if self.state_invert or self.inverted_logic:
                s = not s

        if s is None and globalv.communication_simulation:
            s = self.state
            result = s

        self.set_state(s)
        return result

    def get_hardware_state(self, verbose=True):
        """
        """
        result = None
        msg = 'Get hardware state err'
        if self.actuator is not None:
            result = self.actuator.get_channel_state(self.address, verbose=verbose)

        s = result
        if not isinstance(result, bool):
            self.warning('{}: {}'.format(msg, result))
            s = None
        self.set_state(s)
        return result

    def get_lock_state(self, **kw):
        return self._state_call('get_lock_state')
        # if self.actuator:
        #     return self.actuator.get_lock_state(self)

    def get_owner(self, **kw):
        return self.get_lock_state(**kw)

    def set_open(self, mode='normal', force=False):
        return self._actuate_state(self._open, mode, True, True, force)

    def set_closed(self, mode='normal', force=False):
        return self._actuate_state(self._close, mode, True, False, force)

    # private
    def _actuate_state(self, func, mode, cur, set_value, force):
        """
            func: self._close, self._open
            mode: normal, client
            cur: bool, not self.state if open, self.state if close
            set_value: open-True, close-False
        """
        self.info('actuate state mode={}, software_lock={}'.format(mode, self.software_lock))
        state_change = False
        success = True
        if self.software_lock:
            self._software_locked()
        else:
            success = func(mode, force)

            if success:
                if cur:
                    state_change = True
                self.state = set_value

        return success, state_change

    def _open(self, mode='normal', force=False):
        """
        """
        cmd = 'close_channel' if self.inverted_logic else 'open_channel'
        return self._act(mode, cmd, not self.state or force)

    def _close(self, mode='normal', force=False):
        """
        """
        cmd = 'open_channel' if self.inverted_logic else 'close_channel'
        return self._act(mode, cmd, self.state or force)

    def _act(self, mode, func, do_actuation):
        """

        :param mode:
        :param func:
        :param do_actuation:
        :return:
        """
        self.debug('doing actuation mode={} func={}'.format(mode, func))
        r = True
        actuator = self.actuator
        if mode == 'debug':
            r = True

        elif actuator is not None:
            func = getattr(actuator, func)
            r = func(self)

        if self.settling_time:
            time.sleep(self.settling_time)

        return r

    @property
    def state_device_obj(self):
        if self.state_device:
            return '{}({})'.format(self.state_device.__class__.__name__, id(self.state_device))

    @property
    def actuator_obj(self):
        if self.actuator:
            return '{}({})'.format(self.actuator.__class__.__name__, id(self.actuator))
# ============= EOF =============================================
