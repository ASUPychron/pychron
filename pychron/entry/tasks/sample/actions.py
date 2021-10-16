# ===============================================================================
# Copyright 2016 Jake Ross
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
from __future__ import absolute_import

from pyface.tasks.action.task_action import TaskAction

from pychron.envisage.resources import icon
from pychron.envisage.ui_actions import UIAction, UITaskAction


# class SampleEditAction(Action):
#     name = 'Sample Edit'
#     dname = 'Sample Edit'
#     id = 'pychron.sample_entry'
#
#     def perform(self, event):
#         from pychron.entry.tasks.sample.sample_edit_view import SampleEditView, SampleEditModel
#
#         app = event.task.window.application
#         dvc = app.get_service(DVC_PROTOCOL)
#         sem = SampleEditModel(dvc=dvc)
#         sem.init()
#         sev = SampleEditView(model=sem)
#         sev.edit_traits()


class SampleEntryAction(UIAction):
    name = "Sample"
    id = "pychron.sample_entry"

    def perform(self, event):
        pid = "pychron.entry.sample.task"
        app = event.task.window.application
        app.get_task(pid)


class SaveAction(TaskAction):
    name = "Save"
    image = icon("database_save")
    method = "save"


class LoadAction(TaskAction):
    name = "Load"
    image = icon("document-open")
    method = "load"


class DumpAction(TaskAction):
    name = "Dump"
    image = icon("document-save")
    method = "dump"


class RecoverAction(TaskAction):
    name = "Recover"
    image = icon("document-revert-3")
    method = "recover"


class ClearAction(TaskAction):
    name = "Clear"
    image = icon("clear")
    method = "clear"


class ImportSamplesAction(UITaskAction):
    name = "Import Sample File"
    method = "import_sample_from_file"


class MakeSampleTemplateAction(UITaskAction):
    name = "Make Sample Template"
    method = "make_sample_template_file"


# ============= EOF =============================================
