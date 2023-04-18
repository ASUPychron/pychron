# ===============================================================================
# Copyright 2023 ross
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
import json
from pychron.hardware.core.core_device import CoreDevice


class AquaController(CoreDevice):
    """

    def main():
        aqua = get_device('aqua_controller')
        aqua.trigger()
        waitfor(dev.is_ready)

    """

    def get_report(self):
        r = self.ask("report")
        if r:
            try:
                r = json.loads(r)
            except BaseException:
                self.warning("failed reading response")
                self.debug_exception()
                return

            return r

    def trigger(self):
        self.ask("trigger")

    def is_ready(self):
        r = self.ask("status")

        if r:
            try:
                r = json.loads(r)
            except BaseException:
                self.warning("failed reading response")
                self.debug_exception()
                return

            return r["completed"]


# ============= EOF =============================================
