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
# ============= standard library imports ========================
# ============= local library imports  ==========================
from __future__ import absolute_import

from pychron.spectrometer.tasks.thermo.base import ThermoSpectrometerPlugin
from pychron.spectrometer.thermo.manager.helix import (
    HelixSpectrometerManager,
    HelixSFTSpectrometerManager,
)


class HelixSpectrometerPlugin(ThermoSpectrometerPlugin):
    id = "pychron.spectrometer.helix"
    spectrometer_manager_klass = HelixSpectrometerManager
    manager_name = "helix_spectrometer_manager"
    name = "HelixSpectrometer"


class HelixSFTSpectrometerPlugin(ThermoSpectrometerPlugin):
    id = "pychron.spectrometer.helix_sft"
    spectrometer_manager_klass = HelixSFTSpectrometerManager
    manager_name = "helix_spectrometer_manager"
    name = "HelixSFTSpectrometer"


# ============= EOF =============================================
