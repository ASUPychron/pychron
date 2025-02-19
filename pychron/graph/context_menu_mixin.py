# ===============================================================================
# Copyright 2012 Jake Ross
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

from traits.api import HasTraits
from traitsui.menu import Action, Menu as MenuManager

from pychron.pychron_constants import PLUSMINUS, EXPONENTIAL


# from pyface.action.group import Group
# from pyface.action.api import Group, MenuManager

# ============= standard library imports ========================
# ============= local library imports  ==========================


class ContextMenuMixin(HasTraits):
    use_context_menu = True

    def close_popup(self):
        pass

    def action_factory(self, name, func, **kw):
        return Action(name=name, on_perform=getattr(self, func), **kw)

    def contextual_menu_contents(self):
        """ """
        save = [("PDF", "save_pdf", {}), ("PNG", "save_png", {})]
        save_actions = [self.action_factory(n, f, **kw) for n, f, kw in save]
        save_menu = MenuManager(name="Save Figure", *save_actions)

        export_actions = [self.action_factory("CSV", "export_data")]
        export_menu = MenuManager(name="Export", *export_actions)

        rescale = [
            ("X", "rescale_x_axis", {}),
            ("Y", "rescale_y_axis", {}),
            ("Both", "rescale_both", {}),
        ]
        a = self.get_rescale_actions()

        if a:
            rescale.extend(a)

        rescale_actions = [self.action_factory(n, f, **kw) for n, f, kw in rescale]
        rescale_menu = MenuManager(name="Rescale", *rescale_actions)

        contents = [save_menu, export_menu, rescale_menu]
        c = self.get_child_context_menu_actions()
        if c:
            contents.extend(c)

        return contents

    def get_rescale_actions(self):
        return

    def get_child_context_menu_actions(self):
        return

    def get_contextual_menu(self):
        """ """
        ctx_menu = MenuManager(*self.contextual_menu_contents())

        return ctx_menu


# class IsotopeContextMenuMixin(ContextMenuMixin):
#     def set_status_omit(self):
#         '''
#             override this method in a subclass
#         '''
#         pass
#
#     def set_status_include(self):
#         '''
#             override this method in a subclass
#         '''
#         pass
#
#     def recall_analysis(self):
#         '''
#             override this method in a subclass
#         '''
#         pass
#
#     def contextual_menu_contents(self):
#
#         contents = super(IsotopeContextMenuMixin, self).contextual_menu_contents()
#         contents.append(self.action_factory('Edit Analyses', 'edit_analyses'))
#         actions = []
#         if hasattr(self, 'selected_analysis'):
#             if self.selected_analysis:
#                 actions.append(self.action_factory('Recall', 'recall_analysis'))
#                 if self.selected_analysis.status == 0:
#                     actions.append(self.action_factory('Omit', 'set_status_omit'))
#                 else:
#                     actions.append(self.action_factory('Include', 'set_status_include'))
#                 actions.append(self.action_factory('Void', 'set_status_void'))
#
#                 contents.append(MenuManager(name='Analysis', *actions))
#
#                 #        contents.append(MenuManager(
#                 #                             self.action_factory('Recall', 'recall_analysis', enabled=enabled),
#                 #                             self.action_factory('Omit', 'set_status_omit', enabled=enabled),
#                 #                             self.action_factory('Include', 'set_status_include', enabled=enabled),
#                 #                             name='Analysis'))
#         return contents


class RegressionContextMenuMixin(ContextMenuMixin):
    def contextual_menu_contents(self):
        contents = super(RegressionContextMenuMixin, self).contextual_menu_contents()
        actions = [
            ("linear", "cm_linear"),
            ("parabolic", "cm_parabolic"),
            ("cubic", "cm_cubic"),
            ("quartic", "cm_quartic"),
            (EXPONENTIAL, "cm_exponential"),
            ("auto_linear_parabolic", "cm_auto_linear_parabolic"),
            (u"average {}SD".format(PLUSMINUS), "cm_average_std"),
            (u"average {}SEM".format(PLUSMINUS), "cm_average_sem"),
        ]

        menu = MenuManager(
            *[self.action_factory(name, func) for name, func in actions], name="Fit"
        )
        actions = [
            ("SD", "cm_sd"),
            ("SEM", "cm_sem"),
            ("CI", "cm_ci"),
            ("MonteCarlo", "cm_mc"),
        ]

        emenu = MenuManager(
            *[self.action_factory(name, func) for name, func in actions], name="Error"
        )

        fmenu = MenuManager(
            self.action_factory("Show/Hide Filter Region", "cm_toggle_filter_bounds"),
            self.action_factory(
                "Show/Hide All Filter Region", "cm_toggle_filter_bounds_all"
            ),
            self.action_factory("Toggle Filtering", "cm_toggle_filtering"),
            name="Filtering",
        )
        contents.append(menu)
        contents.append(emenu)
        contents.append(fmenu)
        return contents


# ============= EOF =============================================
