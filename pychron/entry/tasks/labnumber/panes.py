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
from datetime import datetime, timedelta

from enable.component_editor import ComponentEditor
from pyface.action.menu_manager import MenuManager
from pyface.tasks.traits_dock_pane import TraitsDockPane
from pyface.tasks.traits_task_pane import TraitsTaskPane
from traits.api import Instance, Int, Button, Event, Date, HasTraits
from traitsui.api import (
    View,
    Item,
    TabularEditor,
    VGroup,
    HGroup,
    EnumEditor,
    UItem,
    Label,
    VSplit,
    TextEditor,
    Readonly,
    Handler,
)
from traitsui.menu import Action
from traitsui.tabular_adapter import TabularAdapter

from pychron.core.helpers.traitsui_shortcuts import okcancel_view
from pychron.core.pychron_traits import PositiveInteger, BorderVGroup, BorderHGroup
from pychron.core.ui.combobox_editor import ComboboxEditor
from pychron.core.ui.enum_editor import myEnumEditor
from pychron.core.ui.qt.tabular_editors import FilterTabularEditor
from pychron.core.ui.table_configurer import TableConfigurer
from pychron.entry.irradiated_position import IrradiatedPositionAdapter
from pychron.envisage.browser.adapters import SampleAdapter, BrowserAdapter
from pychron.envisage.icon_button_editor import icon_button_editor
from pychron.envisage.tasks.pane_helpers import spacer
from pychron.git_archive.views import CommitAdapter
from pychron.pychron_constants import PLUSMINUS_ONE_SIGMA


class ProjectAdapter(BrowserAdapter):
    columns = [("Name", "name"), ("PI", "principal_investigator")]

    def get_menu(self, obj, trait, row, column):
        return MenuManager(Action(name="Unselect", action="unselect_projects"))


class LevelInfoPane(TraitsDockPane):
    id = "pychron.entry.level"
    name = "Level"

    def traits_view(self):
        v = View(
            Readonly("level_production_name", label="Production"),
            Readonly("irradiation_tray", label="Irradiation Tray"),
            Readonly("monitor_age", label="Monitor Age"),
            Readonly("monitor_decay_constant", label="LambdaK Total"),
            VGroup(
                UItem("level_note", style="custom", editor=TextEditor(read_only=True)),
                show_border=True,
                label="Note",
            ),
        )
        return v


class FluxHistoryOptions(HasTraits):
    after = Date
    before = Date
    max_count = PositiveInteger(1000)

    def traits_view(self):
        v = okcancel_view(
            Item(
                "max_count",
                tooltip="Maximum number of changes to examine",
                label="Max. Count",
            ),
            Item("after"),
            Item("before"),
            kind="modal",
        )
        return v


class FluxHistoryPane(TraitsDockPane):
    id = "pychron.entry.flux_history"
    name = "Flux History"
    load_history_button = Button
    flux_history_options = Instance(FluxHistoryOptions, ())

    def _flux_history_options_default(self):
        f = FluxHistoryOptions()
        f.before = datetime.now()
        f.after = f.before - timedelta(days=90)
        return f

    def _load_history_button_fired(self):
        self.model.load_history(
            max_count=self.flux_history_options.max_count,
            after=self.flux_history_options.after,
            before=self.flux_history_options.before,
        )

    def traits_view(self):
        t = HGroup(
            icon_button_editor("pane.load_history_button", "arrow_refresh"),
            Item(
                "pane.flux_history_options.max_count",
                tooltip="Maximum number of changes to examine",
                label="Max. Count",
            ),
            Item("pane.flux_history_options.after"),
            Item("pane.flux_history_options.before"),
        )

        v = View(
            VGroup(
                t, UItem("flux_commits", editor=TabularEditor(adapter=CommitAdapter()))
            )
        )
        return v


class ChronologyAdapter(TabularAdapter):
    columns = [("Start", "start"), ("End", "end")]
    start_width = Int(150)
    end_width = Int(150)


class ChronologyPane(TraitsDockPane):
    id = "pychron.entry.chronology"
    name = "Chronology"

    def traits_view(self):
        v = View(
            VGroup(
                HGroup(
                    Item("estimated_j_value", style="readonly", label="Est. J"),
                    Item("total_irradiation_hours", style="readonly", label="Hours"),
                ),
                UItem(
                    "chronology_items",
                    editor=TabularEditor(editable=False, adapter=ChronologyAdapter()),
                ),
            )
        )
        return v
        # v = View(VGroup(VGroup(Item('estimated_j_value',
        #                             style='readonly',
        #                             label='Est. J')),
        #                 VGroup(UItem('chronology_items',
        #                              editor=TabularEditor(editable=False,
        #                                                   adapter=ChronologyAdapter())))))
        # return v


class IrradiationEditorHandler(Handler):
    def find_associated_identifiers(self, info, obj):
        obj.find_associated_identifiers()

    def unselect_projects(self, info, obj):
        obj.selected_projects = []

    def configure_sample_table(self, info, obj):
        info.ui.context["pane"].configure_sample_table()


class SampleTableConfigurer(TableConfigurer):
    id = "irradiation.sample.configurer"


class IrradiationEditorPane(TraitsDockPane):
    id = "pychron.labnumber.editor"
    name = "Editor"
    sample_tabular_adapter = Instance(SampleAdapter, ())
    table_configurer = Instance(SampleTableConfigurer)
    refresh_needed = Event

    def __init__(self, *args, **kw):
        super(IrradiationEditorPane, self).__init__(*args, **kw)
        self.table_configurer.set_columns()

    def refresh(self):
        self.refresh_needed = True

    def configure_sample_table(self):
        self.table_configurer.edit_traits()

    def traits_view(self):
        pi_grp = BorderVGroup(
            UItem(
                "principal_investigator",
                editor=EnumEditor(name="principal_investigator_names"),
            ),
            label="Principal Investigator",
        )
        project_grp = BorderVGroup(
            UItem(
                "projects",
                editor=FilterTabularEditor(
                    editable=False,
                    use_fuzzy=True,
                    selected="selected_projects",
                    adapter=ProjectAdapter(),
                    multi_select=True,
                ),
                # width=175
            ),
            label="Projects",
        )

        sample_grp = VGroup(
            HGroup(
                UItem(
                    "sample_filter_parameter",
                    editor=EnumEditor(name="sample_filter_parameters"),
                ),
                UItem(
                    "sample_filter",
                    editor=ComboboxEditor(name="sample_filter_values"),
                    # width=75
                ),
                # icon_button_editor('edit_sample_button', 'database_edit',
                #                    tooltip='Edit sample in database'),
                # icon_button_editor('add_sample_button', 'database_add',
                #                    tooltip='Add sample to database')
                icon_button_editor(
                    "clear_sample_button", "clear", tooltip="Clear selected sample"
                ),
            ),
            UItem(
                "samples",
                editor=TabularEditor(
                    adapter=self.sample_tabular_adapter,
                    editable=False,
                    refresh="pane.refresh_needed",
                    selected="selected_samples",
                    dclicked="dclicked",
                    multi_select=True,
                    column_clicked="column_clicked",
                    stretch_last_section=False,
                ),
                # width=75
            ),
        )

        sagrp = BorderHGroup(
            UItem(
                "sample_search_str", tooltip="Search for sample from entire Database"
            ),
            label="Sample",
        )

        g1 = VGroup(HGroup(pi_grp, sagrp), project_grp)

        v = View(VSplit(g1, sample_grp), handler=IrradiationEditorHandler())
        return v

    def _table_configurer_default(self):
        t = SampleTableConfigurer(auto_set=True, refresh_func=self.refresh)
        t.set_adapter(self.sample_tabular_adapter)
        return t


class IrradiationMetadataEditorPane(TraitsDockPane):
    name = "Irradiation MetaData"

    def traits_view(self):
        jgrp = BorderHGroup(
            UItem("j"),
            Label(PLUSMINUS_ONE_SIGMA),
            UItem("j_err"),
            icon_button_editor(
                "estimate_j_button",
                "cog",
                tooltip="Estimate J based on irradiation "
                "chronology and the J/hr rate set in "
                "Preferences/Entry",
            ),
            label="J",
        )
        ngrp = BorderHGroup(UItem("note"), Item("weight"), label="Note")
        packet_grp = BorderHGroup(
            UItem(
                "packet",
                tooltip="Packet label. Must be in the form "
                "<number> or <prefix><number>. e.g. 1 or p1 or packet01",
            ),
            icon_button_editor(
                "set_packet_event",
                "arrow_right",
                enabled_when="packet",
                tooltip="Apply the Packet to current selection",
            ),
            Item("use_increment_packet", label="Auto-increment"),
            label="Packet",
        )
        v = View(VGroup(HGroup(jgrp, ngrp), packet_grp))
        return v


class LabnumbersPane(TraitsTaskPane):
    def traits_view(self):
        v = View(
            UItem(
                "irradiated_positions",
                editor=TabularEditor(
                    adapter=IrradiatedPositionAdapter(),
                    editable=False,
                    refresh="refresh_table",
                    multi_select=True,
                    selected="selected",
                ),
            )
        )
        return v


class IrradiationCanvasPane(TraitsDockPane):
    name = "Canvas"
    id = "pychron.entry.irradiation_canvas"

    def traits_view(self):
        v = View(
            VGroup(
                HGroup(Item("irradiation_tray", style="readonly")),
                UItem("canvas", editor=ComponentEditor()),
            )
        )
        return v


class IrradiationPane(TraitsDockPane):
    name = "Irradiation"
    id = "pychron.labnumber.irradiation"
    closable = False

    def traits_view(self):
        irrad = HGroup(
            spacer(),
            Item(
                "irradiation",
                width=-150,
                editor=myEnumEditor(name="irradiations"),
                label="Package",
            ),
            icon_button_editor(
                "edit_irradiation_button",
                "database_edit",
                enabled_when="edit_irradiation_enabled",
                tooltip="Edit Package",
            ),
            icon_button_editor(
                "add_irradiation_button", "database_add", tooltip="Add Package"
            ),
            icon_button_editor(
                "import_irradiation_button", "database_go", tooltip="Import Package"
            ),
        )

        level = HGroup(
            spacer(),
            Label("Level:"),
            spacer(-23),
            UItem("level", width=-150, editor=myEnumEditor(name="levels")),
            icon_button_editor(
                "edit_level_button",
                "database_edit",
                tooltip="Edit level",
                enabled_when="edit_level_enabled",
            ),
            icon_button_editor("add_level_button", "database_add", tooltip="Add level"),
        )

        v = View(VGroup(irrad, level))
        return v


# ============= EOF =============================================
