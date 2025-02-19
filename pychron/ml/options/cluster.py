# ===============================================================================
# Copyright 2019 ross
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
from traits.api import Enum

from pychron.ml import CLUSTER_KINDS
from pychron.ml.options.cluster_views import VIEWS
from pychron.options.options import FigureOptions
from pychron.options.options_manager import FigureOptionsManager
from pychron.pychron_constants import APPEARANCE, DISPLAY, MAIN


class ClusterOptions(FigureOptions):
    cluster_kind = Enum(CLUSTER_KINDS)

    def initialize(self):
        self.subview_names = [MAIN, APPEARANCE, DISPLAY]

    def _get_subview(self, name):
        return VIEWS[name]


class ClusterOptionsManager(FigureOptionsManager):
    id = "cluster"
    options_klass = ClusterOptions


# ============= EOF =============================================
