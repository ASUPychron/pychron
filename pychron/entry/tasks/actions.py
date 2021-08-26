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
import os

from pyface.constant import OK
from pyface.file_dialog import FileDialog

from pychron.envisage.resources import icon
from pychron.envisage.tasks.actions import PAction as Action, PTaskAction as TaskAction
from pychron.pychron_constants import DVC_PROTOCOL


class AddFluxMonitorAction(Action):
    name = 'Add/Edit Flux Monitors'

    def perform(self, event):
        app = event.task.window.application
        s = app.get_service('pychron.entry.editors.flux_monitor_editor.FluxMonitorEditor')
        s.add_flux_monitor()


class SensitivityEntryAction(Action):
    name = 'Sensitivity'
    # accelerator = 'Ctrl+Shift+\\'
    id = 'pychron.sensitivity'

    def perform(self, event):
        pid = 'pychron.entry.sensitivity.task'
        app = event.task.window.application
        app.get_task(pid)


class SaveSensitivityAction(TaskAction):
    name = 'Save'
    image = icon('database_save')
    method = 'save'


class AddSensitivityAction(TaskAction):
    name = 'Add'
    image = icon('database_add')
    method = 'add'


class DatabaseSaveAction(TaskAction):
    name = 'Database Save'
    description = 'Save current changes to the database'
    method = 'save_to_db'
    image = icon('database_save')


class ClearSelectionAction(TaskAction):
    name = 'Clear Selection'
    image = icon('table_lightning')
    method = 'clear_selection'


class RecoverAction(TaskAction):
    name = 'Recover'
    method = 'recover'


class SavePDFAction(TaskAction):
    name = 'Save PDF'
    image = icon('file_pdf')

    method = 'save_pdf'


class MakeIrradiationBookPDFAction(TaskAction):
    name = 'Make Irradiation Book'
    image = icon('file_pdf')

    method = 'make_irradiation_book_pdf'


class GenerateIdentifiersAction(TaskAction):
    name = 'Generate Identifiers'
    image = icon('table_lightning')

    method = 'generate_identifiers'

    description = 'Automatically generate labnumbers (aka identifiers) for each irradiation position in the ' \
                  'currently selected irradiation.'


class PreviewGenerateIdentifiersAction(TaskAction):
    name = 'Preview Generate Identifiers'
    image = icon('table_lightning')

    method = 'preview_generate_identifiers'


class ImportIrradiationAction(TaskAction):
    name = 'Import Irradiation...'

    def perform(self, event):
        app = event.task.window.application

        mdb = 'pychron.mass_spec.database.massspec_database_adapter.MassSpecDatabaseAdapter'
        mssource = app.get_service(mdb)
        mssource.bind_preferences()

        from pychron.data_mapper import do_import_irradiation
        dvc = app.get_service('pychron.dvc.dvc.DVC')
        plugin = app.get_plugin('pychron.entry.plugin')

        sources = {obj: name for name, obj in plugin.data_sources}
        sources['Mass Spec'] = mssource
        do_import_irradiation(dvc=dvc, sources=sources, default_source='Mass Spec')


class ImportAnalysesAction(Action):
    name = 'Import Analyses...'

    def perform(self, event):
        app = event.task.window.application
        dvc = app.get_service('pychron.dvc.dvc.DVC')

        from pychron.data_mapper import do_import_analyses

        # sources = {}
        # usgsvsc = app.get_service('pychron.data_mapper.sources.usgs_vsc_source.ViewUSGSVSCSource')
        # sources[usgsvsc] = 'USGS VSC'

        plugin = app.get_plugin('pychron.entry.plugin')
        sources = {obj: name for name, obj in plugin.data_sources}

        do_import_analyses(dvc, sources)


class CorrelationEllipsesAction(Action):
    name = 'Edit Correlation Ellipses...'

    def perform(self, event):
        dvc = event.task.application.get_service(DVC_PROTOCOL)
        if dvc is not None:
            from pychron.entry.correlation_ellipses_editor import CorrelationEllipsesEditor
            v = CorrelationEllipsesEditor(dvc=dvc)
            v.load()
            info = v.edit_traits()
            if info.result:
                v.dump()


class GenerateTrayAction(Action):
    name = 'Generate Tray Image'
    image = icon('table_lightning')

    description = 'Make a irradiation tray image from an irradiation tray text file.'

    def perform(self, event):
        # p='/Users/ross/Sandbox/entry_tray'
        # p = self.open_file_dialog()
        p = None
        from pychron.paths import paths
        dlg = FileDialog(action='open', default_directory=os.path.join(paths.meta_root, 'irradiation_holders'))
        if dlg.open() == OK:
            p = dlg.path

        if p is not None:
            from pychron.entry.graphic_generator import open_txt
            bounds = (2.54, 2.54)
            radius = 0.03 * 2.54
            gcc, gm = open_txt(p,
                               bounds,
                               radius,
                               convert_mm=True,
                               make=True,
                               rotate=0)
            info = gcc.edit_traits(kind='livemodal')


class ImportIrradiationFileAction(TaskAction):
    name = 'Import Irradiation File'
    image = icon('file_xls')

    method = 'import_irradiation_load_xls'
    description = 'Import irradiation information from an Excel file. Use "Irradiation Template" ' \
                  'to generate a boilerplate irradiation template'


class MakeIrradiationTemplateAction(Action):
    name = 'Irradiation Template'
    image = icon('file_xls')

    description = 'Make an Excel irradiation template that can be used to import irradiation information.'

    def perform(self, event):
        from pyface.file_dialog import FileDialog
        dialog = FileDialog(action='save as', default_filename='IrradiationTemplate.xls')

        from pyface.constant import OK
        if dialog.open() == OK:
            path = dialog.path
            if path:
                from pychron.core.helpers.filetools import add_extension
                path = add_extension(path, '.xls')

                from pychron.entry.loaders.irradiation_template import IrradiationTemplate
                i = IrradiationTemplate()
                i.make_template(path)

                from pyface.confirmation_dialog import confirm
                if confirm(None, 'Template saved to {}.\n\nWould you like to open the template?'):
                    from pychron.core.helpers.filetools import view_file
                    application = 'Microsoft Office 2011/Microsoft Excel'
                    view_file(path, application=application)

                    # from pyface.message_dialog import information
                    # information(None, 'Template saved to {}'.format(path))


# class ImportSampleMetadataAction(TaskAction):
#     name = 'Import Sample Metadata...'
#     method = 'import_sample_metadata'


class ExportIrradiationAction(TaskAction):
    name = 'Export Irradiation...'
    method = 'export_irradiation'


class GenerateIrradiationTableAction(TaskAction):
    name = 'Generate Irradiation Table'
    accelerator = 'Ctrl+0'

    # ddescription = 'Do not use!'

    def perform(self, event):
        # from pychron.entry.irradiation_table_writer import IrradiationTableWriter
        # a = IrradiationTableWriter()
        # a.make()

        from pychron.entry.irradiation_xls_writer import IrradiationXLSTableWriter
        dvc = self.task.window.application.get_service(DVC_PROTOCOL)
        if dvc is not None:
            if dvc.db.connect():
                names = dvc.get_irradiation_names()

                a = IrradiationXLSTableWriter(dvc=dvc)
                a.make(names)
        else:
            from pyface.message_dialog import warning
            warning(None, 'DVC Plugin is required. Please enable')


class ImportIrradiationGeometryAction(Action):
    name = 'Import Irradiation Geometry'

    def perform(self, event):
        dvc = event.task.application.get_service(DVC_PROTOCOL)
        if dvc is not None:
            dialog = FileDialog(action='open', default_directory=os.path.join(os.path.expanduser('~'), 'Desktop'))
            if dialog.open() == OK:
                if dialog.path:
                    dvc.meta_repo.add_irradiation_geometry_file(dialog.path)


# class EditIrradiationGeometryAction(Action):
#     name = 'Edit Irradiation Geometry'
#
#     def perform(self, event):
#         dvc = event.task.application.get_service(DVC_PROTOCOL)
#         if dvc is not None:
#             eiv = EditIrradiationGeometry(dvc=dvc)
#             eiv.edit_traits()


class TransferJAction(TaskAction):
    name = 'Transfer J Data...'
    method = 'transfer_j'


# class GetIGSNAction(TaskAction):
#     name = 'Get IGSNs'
#     method = 'get_igsns'


class GenerateStatusReportAction(TaskAction):
    name = 'Status Report...'
    method = 'generate_status_report'


class SyncMetaDataAction(TaskAction):
    name = 'Sync Repo/DB Metadata'
    method = 'sync_metadata'


class ManualEditIdentifierAction(TaskAction):
    name = 'Manual Edit'
    method = 'manual_edit_identifier'
    image = 'add'

    # def perform(self, event):
    #     app = event.task.window.application
    #     app.information_dialog('Sync Repo disabled')
    #     return
    #
    #     dvc = app.get_service('pychron.dvc.dvc.DVC')
    #     if dvc:
    #         dvc.repository_db_sync('IR986', dry_run=False)


class EditMaterialAction(TaskAction):
    name = 'Edit Material'
    method = 'manual_edit_material'

# ============= EOF =============================================
