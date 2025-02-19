# ===============================================================================
# Copyright 2015 Jake Ross
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

from envisage.ui.tasks.task_factory import TaskFactory
from traits.api import List

from pychron.envisage.tasks.base_task_plugin import BaseTaskPlugin
from pychron.furnace.ifurnace_manager import IFurnaceManager


class BaseFurnacePlugin(BaseTaskPlugin):
    id = "pychron.furnace.base.plugin"
    managers = List(contributes_to="pychron.hardware.managers")
    klass = None
    task_klass = None

    panes = List(contributes_to="pychron.experiment.dock_pane_factories")
    activations = List(contributes_to="pychron.experiment.activations")
    deactivations = List(contributes_to="pychron.experiment.deactivations")

    def _manager_factory(self):
        factory = __import__(self.klass[0], fromlist=[self.klass[1]])
        m = getattr(factory, self.klass[1])()

        # m.bootstrap()
        m.name = self.name
        m.plugin_id = self.id
        # m.bind_preferences(self.id)

        return m

    def _task_factory(self):
        if self.task_klass is None:
            raise NotImplementedError

        return self.task_klass(
            manager=self._get_manager(), application=self.application
        )

    def _get_manager(self):
        return self.application.get_service(
            IFurnaceManager, 'name=="{}"'.format(self.name)
        )

    def _managers_default(self):
        d = []

        if self.klass is not None:
            d = [
                dict(
                    name=self.name,
                    plugin_name=self.name,
                    manager=self.application.get_service(
                        IFurnaceManager, 'name=="{}"'.format(self.name)
                    ),
                )
            ]

        return d

    def _service_offers_default(self):
        so = self.service_offer_factory(
            protocol=IFurnaceManager, factory=self._manager_factory
        )
        return [so]

    def _tasks_default(self):
        return [
            TaskFactory(
                name="Furnace",
                task_group="hardware",
                factory=self._task_factory,
                protocol=self.task_klass,
            )
        ]


# ============= EOF =============================================
