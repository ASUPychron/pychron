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

# ============= enthought library imports =======================
from enable.markers import marker_names
from traitsui.api import View, UItem, Item, HGroup, VGroup, EnumEditor, Label

# ============= standard library imports ========================
# ============= local library imports  ==========================
from pychron.core.pychron_traits import BorderVGroup
from pychron.options.options import (
    SubOptions,
    AppearanceSubOptions,
    MainOptions,
    object_column,
    checkbox_column,
)
from pychron.pychron_constants import MAIN, APPEARANCE


class RatioSeriesMainOptions(MainOptions):
    def _get_edit_view(self):
        v = View(
            VGroup(
                self._get_ic_group(),
                self._get_scatter_group(),
                self._get_ylimits_group(),
            )
        )
        return v

    def _get_ic_group(self):
        return BorderVGroup(
            HGroup(
                UItem("numerator", editor=EnumEditor(name="detectors")),
                Label("/"),
                UItem("denominator", editor=EnumEditor(name="detectors")),
            ),
            HGroup(
                Item("fit", editor=EnumEditor(name="fit_types")),
                UItem("error_type", editor=EnumEditor(name="error_types")),
            ),
            Item("standard_ratio"),
            label="IC",
        )

    def _get_scatter_group(self):
        return BorderVGroup(
            Item("height"),
            HGroup(
                Item("marker", editor=EnumEditor(values=marker_names)),
                Item("marker_size"),
            ),
            label="Scatter",
        )

    def _get_columns(self):
        return [
            object_column(name="numerator", editor=EnumEditor(name="detectors")),
            object_column(name="denominator", editor=EnumEditor(name="detectors")),
            checkbox_column(name="plot_enabled", label="Plot"),
            # checkbox_column(name='save_enabled', label='Save'),
            object_column(name="standard_ratio", label="Standard Ratio"),
            object_column(name="fit", editor=EnumEditor(name="fit_types"), width=75),
            object_column(
                name="error_type",
                editor=EnumEditor(name="error_types"),
                width=75,
                label="Error",
            ),
            object_column(name="height", label="Height"),
        ]


class RatioSeriesSubOptions(SubOptions):
    def traits_view(self):
        v = View(
            VGroup(
                Item("show_statistics"),
                Item(
                    "link_plots",
                    label="Link Plots",
                    tooltip="Link plots together so that omitting an "
                    "analysis from any plot omits the analysis on "
                    "all other plots",
                ),
            )
        )
        return v


class RatioSeriesAppearance(AppearanceSubOptions):
    pass


# ===============================================================
# ===============================================================
VIEWS = {
    MAIN.lower(): RatioSeriesMainOptions,
    "ratio series": RatioSeriesSubOptions,
    APPEARANCE.lower(): RatioSeriesAppearance,
}

# ============= EOF =============================================
