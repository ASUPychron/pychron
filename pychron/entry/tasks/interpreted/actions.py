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
from pychron.entry.interpreted.etl import InterpretedETL
from pychron.envisage.tasks.actions import PAction as Action
from pychron.pychron_constants import DVC_PROTOCOL


class ImportInterpretedAction(Action):
    name = 'Import Interpreted File'

    def perform(self, event):
        dvc = event.task.application.get_service(DVC_PROTOCOL)
        s = InterpretedETL(dvc=dvc)
        s.etl()

# ============= EOF =============================================
