# ===============================================================================
# Copyright 2011 Jake Ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================


# ============= enthought library imports =======================
from traits.api import Str, HasTraits
from apptools.preferences.preference_binding import bind_preference
# ============= standard library imports ========================
from threading import RLock, Lock
# ============= local library imports  ==========================

from pychron.hardware.core.core_device import CoreDevice


class QuaderaController(CoreDevice):
    pass
    # lock = None
    #
    # def set(self, *args, **kw):
    #     return HasTraits.set(self, *args, **kw)
    #
    # def initialize(self, *args, **kw):
    #     ret = super(QuaderaController, self).initialize(*args, **kw)
    #
    #     # trying a new locking mechanism see ngx.trigger for more details
    #     # self.lock = Lock()
    #
    #     return ret


# ============= EOF =============================================
