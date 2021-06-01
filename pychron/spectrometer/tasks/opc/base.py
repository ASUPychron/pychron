# ===============================================================================
# Copyright 2013 Jake Ross
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

# ============= enthought library imports =======================
from pychron.spectrometer.pfeiffer.manager.quadera import QuaderaSpectrometerManager
from pychron.spectrometer.tasks.base_spectrometer_plugin import BaseSpectrometerPlugin


class OPCSpectrometerPlugin(BaseSpectrometerPlugin):
    id = 'pychron.spectrometer.argus'
    spectrometer_manager_klass = QuaderaSpectrometerManager
    manager_name = 'quadera_spectrometer_manager'
    name = 'OPCSpectrometer'

    def start(self):
        super(OPCSpectrometerPlugin, self).start()

# ============= EOF =============================================
