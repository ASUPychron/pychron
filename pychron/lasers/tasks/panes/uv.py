# ===============================================================================
# Copyright 2013 Jake Ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

# ============= enthought library imports =======================
from __future__ import absolute_import
from pyface.tasks.traits_dock_pane import TraitsDockPane
from traitsui.api import (
    View,
    Item,
    VGroup,
    HGroup,
    spring,
    UItem,
    ButtonEditor,
    Group,
    EnumEditor,
)

from pychron.core.ui.led_editor import LEDEditor
from pychron.core.ui.qt.reference_mark_editor import ReferenceMarkEditor
from pychron.envisage.icon_button_editor import icon_button_editor
from pychron.lasers.tasks.laser_panes import (
    BaseLaserPane,
    ClientPane,
    StageControlPane,
    AxesPane,
    SupplementalPane,
)


# ============= standard library imports ========================
# ============= local library imports  ==========================
class FusionsUVClientPane(ClientPane):
    pass


class FusionsUVPane(BaseLaserPane):
    pass


class FusionsUVStagePane(StageControlPane):
    id = "pychron.fusions.uv.stage"

    def _get_tabs(self):
        tabs = super(FusionsUVStagePane, self)._get_tabs()
        refmark_grp = VGroup(
            HGroup(
                UItem(
                    "object.reference_marks.mark",
                    editor=EnumEditor(name="object.reference_marks.mark_ids"),
                ),
                icon_button_editor("add_reference_mark_button", "add"),
            ),
            Item("object.reference_marks.mark_display", editor=ReferenceMarkEditor()),
            UItem("reset_reference_marks_button"),
            Item("object.reference_marks.spacing"),
            Item("save_reference_marks_canvas_button"),
            label="Ref. Marks",
        )
        tabs.content.append(refmark_grp)
        return tabs


class FusionsUVAxesPane(AxesPane):
    id = "pychron.fusions.uv.axes"


class FusionsUVSupplementalPane(SupplementalPane):
    id = "pychron.fusions.uv.supplemental"
    name = "UV"

    def traits_view(self):
        v = View(
            Group(
                VGroup(
                    Item("fiber_light", style="custom", show_label=False),
                    label="FiberLight",
                ),
                layout="tabbed",
            )
        )
        return v


def button_editor(name, label, **kw):
    return UItem(name, editor=ButtonEditor(label_value=label))


class FusionsUVControlPane(TraitsDockPane):
    id = "pychron.fusions.uv.control"

    def traits_view(self):
        grp = VGroup(
            HGroup(
                Item(
                    "enabled",
                    show_label=False,
                    style="custom",
                    editor=LEDEditor(colors=["red", "green"]),
                ),
                button_editor("enable", "enable_label"),
                spring,
            ),
            HGroup(
                Item("action_readback", width=100, style="readonly", label="Action"),
                Item("status_readback", style="readonly", label="Status"),
            ),
            HGroup(
                button_editor("fire_button", "fire_label"),
                Item("fire_mode", show_label=False),
                enabled_when='object.enabled and object.status_readback=="Laser On"',
            ),
            HGroup(
                Item("burst_shot", label="N Burst", enabled_when='fire_mode=="Burst"'),
                Item("reprate", label="Rep. Rate"),
            ),
            HGroup(
                Item("burst_readback", label="Burst Rem.", width=50, style="readonly"),
                Item(
                    "energy_readback",
                    label="Energy (mJ)",
                    style="readonly",
                    format_str="%0.2f",
                ),
                Item(
                    "pressure_readback",
                    label="Pressure (mbar)",
                    style="readonly",
                    width=100,
                    format_str="%0.1f",
                ),
                spring,
                enabled_when="object.enabled",
            ),
        )
        v = View(grp)
        return v


# ============= EOF =============================================
