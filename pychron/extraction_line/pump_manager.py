# ===============================================================================
# Copyright 2021 ross
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
from traitsui.api import View, Item, ListEditor, InstanceEditor, VGroup, UCustom
from pychron.managers.manager import Manager


class PumpManager(Manager):
    def get_pressure(self, idx=0):
        try:
            d = self.devices[idx]
            self.debug('get pressure, idx={}, device={}'.format(idx, d))
            return d.get_pressure()
        except IndexError:
            self.warning('Invalid device index={}, totals devices={}'.format(idx, len(self.devices)))
            return 0

    def traits_view(self):
        if self.devices:
            v = View(VGroup(UCustom('devices',
                                    editor=ListEditor(mutable=False,
                                                      columns=len(self.devices),
                                                      style='custom',
                                                      editor=InstanceEditor(view='pump_view')))),
                     height=-100)
        else:
            v = View()
        return v
# ============= EOF =============================================
