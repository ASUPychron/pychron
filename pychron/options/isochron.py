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
from enable.markers import MarkerTrait
from traits.api import Str, Bool, Float, Property, Enum, Range, Int

# ============= standard library imports ========================
# ============= local library imports  ==========================
from pychron.options.group.inverse_isochron_group_options import (
    InverseIsochronGroupOptions,
)
from pychron.options.spectrum import PlateauOptions
from pychron.options.views.isochron_views import INVERSE_ISOCHRON_VIEWS, ISOCHRON_VIEWS
from pychron.pychron_constants import (
    ELLIPSE_KINDS,
    FONTS,
    SIZES,
    MAIN,
    APPEARANCE,
    GROUPS,
    CALCULATIONS,
    INSET,
    ISOCHRON_ERROR_TYPES,
    ISOCHRON_METHODS,
)


class IsochronOptions(PlateauOptions):
    age_sig_figs = Int(2)
    yintercept_sig_figs = Int(2)

    def initialize(self):
        self.subview_names = [MAIN, APPEARANCE, GROUPS]

    def get_subview(self, name):
        name = name.lower()
        klass = self._get_subview(name)
        obj = klass(model=self)
        return obj

    def _get_subview(self, name):
        return ISOCHRON_VIEWS[name]

    def _aux_plots_default(self):
        return [self.aux_plot_klass(plot_enabled=True, name="inverse_isochron")]


class InverseIsochronOptions(IsochronOptions):
    error_calc_method = Enum(*ISOCHRON_ERROR_TYPES)
    fill_ellipses = Bool(False)
    ellipse_kind = Enum(ELLIPSE_KINDS)

    show_labels = Bool(True)
    show_results_info = Bool(True)
    show_nominal_intercept = Bool(False)
    nominal_intercept_label = Str("Atm", enter_set=True, auto_set=False)
    nominal_intercept_value = Float(295.5)

    # inset
    inset_marker_size = Float(1.0)
    inset_show_error_ellipse = Bool(True)
    inset_fill_ellipses = Bool(False)
    inset_ellipse_kind = Enum(ELLIPSE_KINDS)
    inset_link_status = Bool(True)

    regressor_kind = Enum(ISOCHRON_METHODS)
    group_options_klass = InverseIsochronGroupOptions

    results_font = Property
    results_fontname = Enum(*FONTS)
    results_fontsize = Enum(*SIZES)

    info_font = Property
    info_fontname = Enum(*FONTS)
    info_fontsize = Enum(*SIZES)

    results_info_spacing = Range(2, 20)

    include_sample = Bool
    include_4036_mse = Bool
    include_age_mse = Bool
    include_age_percent_error = Bool

    include_error_envelope = Bool(True)
    include_percent_error = Bool

    marker_size = Float(2)
    marker = MarkerTrait()

    omit_non_plateau = Bool(False)
    exclude_non_plateau = Bool(False)

    def initialize(self):
        self.subview_names = [MAIN, CALCULATIONS, APPEARANCE, INSET, GROUPS]

    def _get_results_font(self):
        return "{} {}".format(self.results_fontname, self.results_fontsize)

    def _get_info_font(self):
        return "{} {}".format(self.info_fontname, self.info_fontsize)

    @property
    def inominal_intercept_value(self):
        try:
            return 1 / self.nominal_intercept_value
        except ZeroDivisionError:
            return 0

    def _get_subview(self, name):
        return INVERSE_ISOCHRON_VIEWS[name]


# ============= EOF =============================================
