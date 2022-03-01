# ===============================================================================
# Copyright 2017 ross
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
from traits.api import HasTraits, List, Button, Str, Enum, Bool, on_trait_change, Int
from traitsui.api import (
    View,
    UItem,
    VGroup,
    InstanceEditor,
    ListEditor,
    EnumEditor,
    HGroup,
    Item,
)

from pychron.core.helpers.traitsui_shortcuts import okcancel_view
from pychron.core.pychron_traits import BorderVGroup
from pychron.envisage.icon_button_editor import icon_button_editor
from pychron.pychron_constants import NULL_STR
from pychron.regex import DETREGEX


class SQLFilter(HasTraits):
    base_attribute = Str
    attribute_modifier = Str
    modifiers = List([NULL_STR, "blank", "ic_corrected", "bs_corrected"])
    attribute_is_error = Bool
    comparator = Enum("=", "<", ">", "<=", ">=", "!=", "between", "not between")
    criterion = Str
    attributes = List

    chain_operator = Enum("and", "or")
    show_chain = Bool(True)
    remove_button = Button
    remove_visible = Bool(True)

    def _base_attribute_changed(self):
        print(self.base_attribute, DETREGEX.match(self.base_attribute))
        if not DETREGEX.match(self.base_attribute) and self.base_attribute != "age":
            self.modifiers = [NULL_STR, "blank", "ic_corrected", "bs_corrected"]
        else:
            self.attribute_modifier = NULL_STR
            self.modifiers = [NULL_STR]

    @property
    def attribute(self):
        ba = self.base_attribute
        ma = self.attribute_modifier

        a = ba
        if ma and ma != NULL_STR:
            a = "{}_{}".format(a, ma)

        if self.attribute_is_error:
            a = "{} error".format(a)
        return a

    def traits_view(self):
        v = View(
            HGroup(
                icon_button_editor(
                    "remove_button", "delete", visible_when="remove_visible"
                ),
                UItem("chain_operator", visible_when="show_chain"),
                UItem("base_attribute", editor=EnumEditor(name="attributes")),
                UItem("attribute_modifier", editor=EnumEditor(name="modifiers")),
                Item("attribute_is_error", label="Error"),
                UItem("comparator"),
                UItem("criterion"),
            )
        )
        return v


class AdvancedFilterView(HasTraits):
    filters = List
    add_filter_button = Button
    attributes = List
    samples = List
    apply_to_current_selection = Bool
    apply_to_current_samples = Bool
    limit = Int(500)
    omit_invalid = Bool(True)

    def demo(self):
        self.filters = [
            SQLFilter(
                comparator="<",
                base_attribute="Ar40",
                remove_visible=False,
                show_chain=False,
                criterion="100",
                attributes=self.attributes,
            ),
            # SQLFilter(comparator='<',
            #           attribute='Ar39',
            #           chain='and',
            #           criterion='55')
            #
        ]

    @on_trait_change("filters:remove_button")
    def _handle_remove(self, obj, name, old, new):
        self.filters.remove(obj)

    def _filters_default(self):
        return [
            SQLFilter(
                remove_visible=False, show_chain=False, attributes=self.attributes
            )
        ]

    def _add_filter_button_fired(self):
        self.filters.append(SQLFilter(attributes=self.attributes))

    def _filters_items_changed(self):
        for i, fi in enumerate(self.filters):
            fi.show_chain = i != 0

    def traits_view(self):
        fgrp = BorderVGroup(
            icon_button_editor("add_filter_button", "add"),
            UItem(
                "filters",
                editor=ListEditor(
                    mutable=False, style="custom", editor=InstanceEditor()
                ),
            ),
            label="Filters",
        )
        ogrp = BorderVGroup(
            Item("apply_to_current_selection"),
            Item("apply_to_current_samples"),
            Item("omit_invalid"),
            Item("limit"),
            label="Options",
        )
        v = okcancel_view(
            VGroup(fgrp, ogrp), title="Advanced Search", width=700, height=350
        )
        return v


if __name__ == "__main__":
    d = AdvancedFilterView()
    d.configure_traits()
# ============= EOF =============================================
