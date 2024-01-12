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
from riscos_toolbox.objects.menu import Menu, SelectionEvent
from riscos_toolbox.objects.window import Window
from riscos_toolbox.gadgets.writablefield import WritableField, WritableFieldValueChangedEvent
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.events import toolbox_handler


class WritableWindow(Window):
    template = "WritableWin"

    # Gadget constants
    G_WRITABLE = 0x00
    G_INPUT1 = 0x01
    G_INPUT2 = 0x06
    G_OUTPUT = 0x02

    def __init__(self, *args):
        super().__init__(*args)

        self.g_writable = WritableField(self, WritableWindow.G_WRITABLE)
        self.g_input1 = WritableField(self, WritableWindow.G_INPUT1)
        self.g_input2 = WritableField(self, WritableWindow.G_INPUT2)
        self.g_output = DisplayField(self, WritableWindow.G_OUTPUT)

    # Methods for testing WritableField
    def writablefield_set_text(self):
        self.g_writable.value = self.g_input1.value

    def writablefield_get_text(self):
        self.g_output.value = self.g_writable.value

    def writablefield_set_allow(self):
        self.g_writable.allowable = self.g_input1.value

    def writablefield_get_allow(self):
        self.g_output.value = self.g_writable.allowable

    def writablefield_set_font(self):
        try:
            name = self.g_input1.value
            size = int(self.g_input2.value)
        except ValueError:
            self.g_output.value = "Input1=name, Input2=size"
        else:
            self.g_writable.set_font(name=name, size=size)

    # Event handlers for WritableField
    @toolbox_handler(WritableFieldValueChangedEvent)
    def WritableFieldValueChanged(self, event, id_block, poll_block):
        self.g_output.value = "Writable field change: "+repr(poll_block.string)


class WritableFieldMenu(Menu, TestMenu):
    template = "WritFldMenu"

    # Constants for menu entries
    SET_TEXT = 0x00
    GET_TEXT = 0x01
    SET_FONT = 0x04
    SET_ALLOWABLE = 0x02
    GET_ALLOWABLE = 0x03

    @toolbox_handler(SelectionEvent)
    def menu_selected(self, event, id_block, poll_block):
        if id_block.self.id != self.id:
            return False

        window = toolbox.get_object(id_block.parent.id)
        self.menu_tick(id_block.self.component)

        if id_block.self.component == WritableFieldMenu.SET_TEXT:
            window.writablefield_set_text()
        elif id_block.self.component == WritableFieldMenu.GET_TEXT:
            window.writablefield_get_text()
        elif id_block.self.component == WritableFieldMenu.SET_FONT:
            window.writablefield_set_font()
        elif id_block.self.component == WritableFieldMenu.SET_ALLOWABLE:
            window.writablefield_set_allow()
        # This method isn't implemented in the Toolbox, but it is in riscos-toolbox,
        # hence the inclusion here. An issue is open on riscos-toolbox for this.
        # But yes, this will throw an error if called.
        elif id_block.self.component == WritableFieldMenu.GET_ALLOWABLE:
            window.writablefield_get_allow()

        return True
