# MIT License

# Copyright (c) 2023 Lauren Rad

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from tbptest.reporter import Reporter # noqa
from tbptest.tbox_common import TestMenu

import riscos_toolbox as toolbox
from riscos_toolbox.events import toolbox_handler
from riscos_toolbox.objects.menu import Menu, SelectionEvent
from riscos_toolbox.objects.window import Window
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.gadgets.writablefield import WritableField
from riscos_toolbox.gadgets.stringset import StringSet
from riscos_toolbox.gadgets.stringset import StringSetValueChangedEvent
from riscos_toolbox.gadgets.stringset import StringSetAboutToBeShownEvent

# Gadget Constants
G_STRINGSET = 0x01
G_INPUT = 0x02
G_INPUT_W = 0x04
G_INPUT_H = 0x06
G_OUTPUT = 0x08


class StringSetWindow(Window):
    template = "StrSetWin"

    def __init__(self, *args):
        super().__init__(*args)

        # Set up gadgets
        self.g_stringset = StringSet(self, G_STRINGSET)
        self.g_input = WritableField(self, G_INPUT)
        self.g_input_w = WritableField(self, G_INPUT_W)
        self.g_input_h = WritableField(self, G_INPUT_H)
        self.g_output = DisplayField(self, G_OUTPUT)

    # Methods for testing StringSet ops
    def stringset_set_available(self):
        self.g_stringset.set_available(self.g_input.value)

    def stringset_set_selected_text(self):
        self.g_stringset.selected = self.g_input.value

    def stringset_get_selected_text(self):
        self.g_output.value = self.g_stringset.selected

    def stringset_set_selected_index(self):
        try:
            self.g_stringset.index = int(self.g_input.value)
        except ValueError:
            self.g_output.value = "Err: expected int input"

    def stringset_get_selected_index(self):
        self.g_output.value = repr(self.g_stringset.index)

    def stringset_set_allowable(self):
        self.g_stringset.set_allowable(self.g_input.value)

    def stringset_get_alphanum(self):
        self.g_output.value = repr(self.g_stringset.alphanumeric_field)

    def stringset_get_popup(self):
        self.g_output.value = repr(self.g_stringset.popup_menu)

    def stringset_set_font(self):
        try:
            name = self.g_input.value
            width = int(self.g_input_w.value)
            height = int(self.g_input_h.value)
        except ValueError:
            self.g_output.value = "Err: expected int input"
        else:
            self.g_stringset.set_font(name, width, height)

    # Event handlers for StringSet
    @toolbox_handler(StringSetValueChangedEvent)
    def _stringset_value_changed(self, event, id_block, poll_block):
        self.g_output.value = f"Value changed: {poll_block.new_string}"

    @toolbox_handler(StringSetAboutToBeShownEvent)
    def _stringset_about_to_be_shown(self, event, id_block, poll_block):
        self.g_output.value = "About to be shown"


class StringSetMenu(Menu, TestMenu):
    template = "StrSetMenu"

    # Entry constants
    ENTRY_SET_AVAILABLE = 0x00
    ENTRY_SET_SEL_TEXT = 0x01
    ENTRY_GET_SEL_TEXT = 0x08
    ENTRY_SET_SEL_INDEX = 0x07
    ENTRY_GET_SEL_INDEX = 0x02
    ENTRY_SET_ALLOWABLE = 0x03
    ENTRY_GET_ALPHANUM = 0x04
    ENTRY_GET_POPUP = 0x05
    ENTRY_SET_FONT = 0x06

    @toolbox_handler(SelectionEvent)
    def menu_selected(self, event, id_block, poll_block):
        if id_block.self.id != self.id:
            return False

        window = toolbox.get_object(id_block.parent.id)
        self.menu_tick(id_block.self.component)

        if id_block.self.component == StringSetMenu.ENTRY_SET_AVAILABLE:
            window.stringset_set_available()
        elif id_block.self.component == StringSetMenu.ENTRY_SET_SEL_TEXT:
            window.stringset_set_selected_text()
        elif id_block.self.component == StringSetMenu.ENTRY_GET_SEL_TEXT:
            window.stringset_get_selected_text()
        elif id_block.self.component == StringSetMenu.ENTRY_SET_SEL_INDEX:
            window.stringset_set_selected_index()
        elif id_block.self.component == StringSetMenu.ENTRY_GET_SEL_INDEX:
            window.stringset_get_selected_index()
        elif id_block.self.component == StringSetMenu.ENTRY_SET_ALLOWABLE:
            window.stringset_set_allowable()
        elif id_block.self.component == StringSetMenu.ENTRY_GET_ALPHANUM:
            window.stringset_get_alphanum()
        elif id_block.self.component == StringSetMenu.ENTRY_GET_POPUP:
            window.stringset_get_popup()
        elif id_block.self.component == StringSetMenu.ENTRY_SET_FONT:
            window.stringset_set_font()

        return True
