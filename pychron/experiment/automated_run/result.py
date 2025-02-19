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
from traits.api import HasTraits, Str, Property, Instance

# ============= standard library imports ========================
# ============= local library imports  ==========================
from uncertainties import nominal_value, std_dev

from pychron.core.helpers.formatting import uformat_percent_error, floatfmt, errorfmt
from pychron.experiment.conditional.conditional import AutomatedRunConditional
from pychron.processing.isotope_group import IsotopeGroup
from pychron.pychron_constants import NULL_STR


class AutomatedRunResult(HasTraits):
    runid = Str
    analysis_timestamp = None
    isotope_group = Instance(IsotopeGroup)
    summary = Property
    tripped_conditional = Instance(AutomatedRunConditional)
    centering_results = None

    def _get_summary(self):
        lines = ["RunID= {}".format(self.runid)]

        at = self.analysis_timestamp
        if at is not None:
            lines.append("Run Time= {}".format(at.strftime("%H:%M:%S %m-%d-%Y")))

        funcs = [
            self._intensities,
            self._tripped_conditional,
            lambda: self._make_header("Summary"),
            self._make_peak_statistics,
            self._make_summary,
        ]

        for func in funcs:
            try:
                lines.append(func())
            except BaseException:
                pass

        return "\n".join(lines)

    def _make_summary(self):
        return "No Summary Available"

    def _make_peak_statistics(self):
        ret = ""

        def f(v):
            try:
                v = "{:0.2f}".format(v)
            except (ValueError, TypeError):
                v = NULL_STR

            return v

        if self.centering_results:
            fmt = "{:<10s} {:<10s} {:<10s} {:<10s}"
            s = [fmt.format("Det", "Res.", "Low RP", "High RP")]
            for r in self.centering_results:
                s.append(
                    fmt.format(
                        r.detector,
                        f(r.resolution),
                        f(r.low_resolving_power),
                        f(r.high_resolving_power),
                    )
                )

            ret = "\n".join(s)
        return ret

    def _intensities(self):
        lines = []
        if self.isotope_group:

            def fformat(s, n=5):
                return "{{:0.{}f}}".format(n).format(s)

            names = (
                "Iso.",
                "Det.",
                "Intensity (fA)",
                "%Err",
                "Intercept (fA)",
                "%Err",
                "Baseline (fA)",
                "%Err",
                "Blank (fA)",
                "%Err",
            )

            colwidths = 6, 8, 25, 8, 25, 8, 25, 8, 25, 8
            # cols = list(map('{{:<{}s}}'.format, colwidths))
            cols = ["{{:<{}s}}".format(ci) for ci in colwidths]
            colstr = "".join(cols)

            divider = "".join(["{} ".format("-" * (x - 1)) for x in colwidths])
            table_header = colstr.format(*names)
            lines = [self._make_header("Isotopes"), table_header, divider]
            for k in self.isotope_group.isotope_keys:
                iso = self.isotope_group.isotopes[k]
                intensity = iso.get_intensity()
                line = colstr.format(
                    k,
                    iso.detector,
                    fformat(intensity),
                    uformat_percent_error(intensity),
                    fformat(iso.uvalue),
                    uformat_percent_error(iso.uvalue),
                    fformat(iso.baseline.uvalue),
                    uformat_percent_error(iso.baseline.uvalue),
                    fformat(iso.blank.uvalue),
                    uformat_percent_error(iso.blank.uvalue),
                )
                lines.append(line)
        return self._make_lines(lines)

    def _air_ratio(self):
        a4038 = self.isotope_group.get_ratio("Ar40/Ar38", non_ic_corr=True)
        a4036 = self.isotope_group.get_ratio("Ar40/Ar36", non_ic_corr=True)
        # e4038 = uformat_percent_error(a4038, include_percent_sign=True)
        # e4036 = uformat_percent_error(a4036, include_percent_sign=True)

        lines = [
            self._make_header("Ratios"),
            "Ar40/Ar36= {} {}".format(
                floatfmt(nominal_value(a4036)),
                errorfmt(nominal_value(a4036), std_dev(a4036)),
            ),
            "Ar40/Ar38= {} {}".format(
                floatfmt(nominal_value(a4038)),
                errorfmt(nominal_value(a4038), std_dev(a4038)),
            ),
        ]

        return self._make_lines(lines)

    def _tripped_conditional(self):
        ret = ""
        if self.tripped_conditional:
            lines = [
                self._make_header("Conditional"),
                "TEST= {}".format(self.tripped_conditional.teststr),
                "CTX= {}".format(self.tripped_conditional.value_context),
            ]
            ret = self._make_lines(lines)
        return ret

    def _make_header(self, h):
        return "============================= {} {}".format(h, "=" * (30 - len(h)))

    def _make_lines(self, lines):
        return "{}\n".format("\n".join(lines))


class AirResult(AutomatedRunResult):
    def _make_summary(self):
        s = self._air_ratio()
        return s


class UnknownResult(AutomatedRunResult):
    def _make_summary(self):
        lines = ["AGE= {}".format(self.isotope_group.age)]
        return "\n".join(lines)


class BlankResult(AutomatedRunResult):
    def _make_summary(self):
        s = self._air_ratio()
        return s


if __name__ == "__main__":
    from pychron.core.ui.text_editor import myTextEditor
    from pychron.processing.isotope import Isotope
    from traitsui.api import View, UItem

    ig = IsotopeGroup()
    a40 = Isotope("Ar40", "H1")
    a40.set_uvalue((50000.12345, 0.4123412341))
    a36 = Isotope("Ar36", "CDD")
    a36.set_uvalue((51230.12345 / 295.5, 0.132142341))

    a38 = Isotope("Ar38", "L1")
    a38.set_uvalue((51230.12345 / 1590.5, 0.132142341))

    ig.isotopes = dict(Ar40=a40, Ar36=a36, Ar38=a38)
    ig.age = 1.143
    a = AirResult(runid="1234123-01A", isotope_group=ig)

    a.tripped_conditional = AutomatedRunConditional("age>10")
    v = View(
        UItem(
            "summary", style="custom", editor=myTextEditor(editable=False, fontsize=14)
        ),
        title="Summary",
        width=1000,
        resizable=True,
    )
    a.configure_traits(view=v)
# ============= EOF =============================================
